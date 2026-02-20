"""Raster spatial query tool using Rasterio windowed reads."""

from typing import Any

import rasterio
from fastmcp import Context
from fastmcp.exceptions import ToolError
from rasterio.features import geometry_window
from rasterio.io import MemoryFile
from rasterio.windows import Window, from_bounds

from src.app import mcp
from src.config import resolve_path
from src.models.resourceref import ResourceRef
from src.shared.query_registry import register_query_result

BBOX_COORD_COUNT = 4
RASTER_NDIMS_MULTIBAND = 3
RASTER_NDIMS_SINGLE_BAND = 2


def _normalize_bbox(geometry: list[float]) -> tuple[float, float, float, float]:
    if len(geometry) != BBOX_COORD_COUNT:
        raise ToolError("Bounding box must be [minx, miny, maxx, maxy].")
    minx, miny, maxx, maxy = geometry
    if minx >= maxx or miny >= maxy:
        raise ToolError("Bounding box must satisfy minx < maxx and miny < maxy.")
    return float(minx), float(miny), float(maxx), float(maxy)


def _window_from_geometry(src: rasterio.io.DatasetReader, geometry: dict[str, Any]) -> Window:
    try:
        window = geometry_window(src, [geometry], pad_x=0, pad_y=0, boundless=False)
    except Exception as exc:  # noqa: BLE001
        raise ToolError(f"Invalid geometry for raster query: {exc}") from exc

    window = window.round_offsets().round_lengths()
    if window.width <= 0 or window.height <= 0:
        raise ToolError("Query geometry does not intersect raster bounds.")
    return window


def _window_from_bbox(
    src: rasterio.io.DatasetReader,
    bbox: tuple[float, float, float, float],
) -> Window:
    window = from_bounds(*bbox, transform=src.transform)
    window = window.round_offsets().round_lengths()
    if window.width <= 0 or window.height <= 0:
        raise ToolError("Query bounding box does not intersect raster bounds.")
    return window


@mcp.tool(
    name="raster_query",
    description=(
        "Query raster data by spatial extent. "
        "USE WHEN: Need to extract a subset of a raster for analysis or downstream processing. "
        "REQUIRES: uri (source raster path) and geometry (GeoJSON polygon or "
        "[minx, miny, maxx, maxy] bbox). "
        "OPTIONAL: output path for persistence, bands list to limit bands. "
        "OUTPUT: Query metadata with optional output reference and "
        "query://result/{id} for inspection."
    ),
)
async def raster_query(
    uri: str,
    geometry: dict[str, Any] | list[float],
    output: str | None = None,
    bands: list[int] | None = None,
    purpose: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Query a raster by geometry or bbox and optionally persist the result."""
    source_path = resolve_path(uri)

    if ctx:
        await ctx.debug(f"[raster_query] Reading raster: {source_path}")

    try:
        with rasterio.Env():
            with rasterio.open(source_path) as src:
                if isinstance(geometry, dict):
                    window = _window_from_geometry(src, geometry)
                    geometry_used: dict[str, Any] | list[float] = geometry
                elif isinstance(geometry, list):
                    bbox = _normalize_bbox(geometry)
                    window = _window_from_bbox(src, bbox)
                    geometry_used = list(bbox)
                else:
                    raise ToolError(
                        "geometry must be GeoJSON dict or [minx, miny, maxx, maxy] list."
                    )

                data = src.read(indexes=bands, window=window)
                height, width = data.shape[-2], data.shape[-1]
                band_count = data.shape[0] if data.ndim == RASTER_NDIMS_MULTIBAND else 1
                pixel_count = int(height * width)

                meta = src.meta.copy()
                meta.update(
                    {
                        "height": height,
                        "width": width,
                        "count": band_count,
                        "transform": src.window_transform(window),
                    }
                )

                output_ref: ResourceRef | None = None
                persisted = False
                size_bytes: int | None = None
                payload = None

                if output:
                    output_path = resolve_path(output)
                    if ctx:
                        await ctx.info(f"[raster_query] Writing output to: {output_path}")
                    with rasterio.open(output_path, "w", **meta) as dst:
                        if data.ndim == RASTER_NDIMS_SINGLE_BAND:
                            dst.write(data, 1)
                        else:
                            dst.write(data)
                    size_bytes = output_path.stat().st_size
                    output_ref = ResourceRef(
                        uri=f"file://{output_path}",
                        path=str(output_path),
                        size=size_bytes,
                        driver=meta.get("driver"),
                    )
                    persisted = True
                else:
                    # Store in memory for composition; registry handles lifecycle.
                    with MemoryFile() as memfile:
                        with memfile.open(**meta) as dst:
                            if data.ndim == RASTER_NDIMS_SINGLE_BAND:
                                dst.write(data, 1)
                            else:
                                dst.write(data)
                        payload = memfile.read()
                    size_bytes = data.nbytes

                result_meta = {
                    "kind": "raster",
                    "source_uri": str(source_path),
                    "geometry": geometry_used,
                    "filters": {
                        "bands": bands or list(range(1, band_count + 1)),
                        "purpose": purpose,
                    },
                    "counts": {"pixel_count": pixel_count},
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

    except rasterio.errors.RasterioIOError as exc:
        raise ToolError(f"Cannot open raster at '{uri}'.") from exc
    except PermissionError as exc:
        raise ToolError(f"Permission denied for '{output or uri}'.") from exc
    except OSError as exc:
        raise ToolError(f"Raster query failed: {exc}") from exc
