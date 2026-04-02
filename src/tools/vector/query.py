"""Vector spatial query tool using pyogrio filtering."""

from typing import Any

import pyogrio
from fastmcp import Context
from fastmcp.exceptions import ToolError
from shapely.geometry import shape

from src.app import mcp
from src.config import resolve_path
from src.models.resourceref import ResourceRef
from src.shared.query_registry import register_query_result

BBOX_COORD_COUNT = 4


def _normalize_bbox(geometry: list[float]) -> tuple[float, float, float, float]:
    if len(geometry) != BBOX_COORD_COUNT:
        raise ToolError("Bounding box must be [minx, miny, maxx, maxy].")
    minx, miny, maxx, maxy = geometry
    if minx >= maxx or miny >= maxy:
        raise ToolError("Bounding box must satisfy minx < maxx and miny < maxy.")
    return float(minx), float(miny), float(maxx), float(maxy)


def _bbox_from_geometry(geometry: dict[str, Any]) -> tuple[float, float, float, float]:
    try:
        geom = shape(geometry)
    except Exception as exc:  # noqa: BLE001
        raise ToolError(f"Invalid geometry for vector query: {exc}") from exc
    minx, miny, maxx, maxy = geom.bounds
    if minx >= maxx or miny >= maxy:
        raise ToolError("Geometry bounds are empty.")
    return float(minx), float(miny), float(maxx), float(maxy)


@mcp.tool(
    name="vector_query",
    description=(
        "Query vector data by spatial extent and optional filters. "
        "USE WHEN: Need to subset features by area and/or attribute filters. "
        "REQUIRES: uri (source vector path) and geometry (GeoJSON polygon or "
        "[minx, miny, maxx, maxy] bbox). "
        "OPTIONAL: output path for persistence, attributes list, SQL where filter. "
        "OUTPUT: Query metadata with optional output reference and "
        "query://result/{id} for inspection."
    ),
)
async def vector_query(
    uri: str,
    geometry: dict[str, Any] | list[float],
    output: str | None = None,
    attributes: list[str] | None = None,
    where: str | None = None,
    purpose: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Query a vector dataset by geometry/bbox and optional attribute filters."""
    source_path = resolve_path(uri)

    if ctx:
        await ctx.debug(f"[vector_query] Reading vector: {source_path}")

    try:
        if isinstance(geometry, dict):
            bbox = _bbox_from_geometry(geometry)
            geometry_used: dict[str, Any] | list[float] = geometry
        elif isinstance(geometry, list):
            bbox = _normalize_bbox(geometry)
            geometry_used = list(bbox)
        else:
            raise ToolError("geometry must be GeoJSON dict or [minx, miny, maxx, maxy] list.")

        gdf = pyogrio.read_dataframe(
            str(source_path),
            bbox=bbox,
            where=where,
            columns=attributes,
        )

        feature_count = len(gdf)
        size_bytes: int | None = None
        output_ref: ResourceRef | None = None
        persisted = False
        payload = None

        if output:
            output_path = resolve_path(output)
            if ctx:
                await ctx.info(f"[vector_query] Writing output to: {output_path}")
            gdf.to_file(output_path)
            size_bytes = output_path.stat().st_size
            output_ref = ResourceRef(
                uri=f"file://{output_path}",
                path=str(output_path),
                size=size_bytes,
                driver="auto",
            )
            persisted = True
        else:
            payload = gdf
            size_bytes = int(gdf.memory_usage(deep=True).sum())

        result_meta = {
            "kind": "vector",
            "source_uri": str(source_path),
            "geometry": geometry_used,
            "filters": {"attributes": attributes, "where": where, "purpose": purpose},
            "counts": {"feature_count": feature_count},
            "size_bytes": size_bytes,
            "persisted": persisted,
            "output": output_ref.model_dump() if output_ref else None,
        }

        query_meta = register_query_result(result_meta, payload=payload)
        query_ref = ResourceRef(uri=f"query://result/{query_meta['id']}")

        return {
            "query": query_ref.model_dump(),
            "output": output_ref.model_dump() if output_ref else None,
            "metadata": query_meta,
        }

    except ToolError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise ToolError(f"Unexpected error during vector query: {exc}") from exc
