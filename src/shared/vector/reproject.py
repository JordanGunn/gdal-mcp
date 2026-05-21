"""Vector reprojection using pyogrio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pyogrio
from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, ConfigDict, Field

from src.shared.resourceref import ResourceRef


def reproject(
    input_path: str,
    output_path: str | Path,
    dst_crs: str,
    src_crs: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Reproject a vector dataset to a new CRS using pyogrio.

    Args:
        input_path: Path to source vector dataset
        output_path: Path for output vector file
        dst_crs: Destination CRS (e.g., 'EPSG:3857', 'EPSG:4326')
        src_crs: Optional source CRS override (auto-detected if None)
        ctx: Optional FastMCP context for logging

    Returns:
        Dictionary with reprojection metadata:
        - src_crs: Source CRS used
        - dst_crs: Destination CRS
        - feature_count: Number of features
        - geometry_type: Primary geometry type
        - bounds: Spatial extent in destination CRS
        - driver: Output driver used

    Raises:
        ToolError: If reprojection fails
    """
    try:
        # Read source info to determine CRS and metadata
        source_info = pyogrio.read_info(input_path)

        # Determine source CRS
        detected_crs = source_info.get("crs")
        if src_crs:
            used_src_crs = src_crs
        elif detected_crs:
            used_src_crs = str(detected_crs)
        else:
            raise ToolError(
                f"Source CRS not found in '{input_path}' and not provided. "
                "Please specify src_crs parameter (e.g., 'EPSG:4326')."
            )

        # Read geometries and attributes from source
        # pyogrio returns: (geometry, field_data)
        gdf = pyogrio.read_dataframe(input_path)

        # Set CRS if override provided
        if src_crs and str(gdf.crs) != src_crs:
            gdf = gdf.set_crs(src_crs, allow_override=True)

        # Reproject to destination CRS
        gdf_reprojected = gdf.to_crs(dst_crs)

        # Determine output driver from extension
        output_path_obj = Path(output_path)
        extension = output_path_obj.suffix.lower()
        driver_map = {
            ".shp": "ESRI Shapefile",
            ".gpkg": "GPKG",
            ".geojson": "GeoJSON",
            ".json": "GeoJSON",
            ".kml": "KML",
            ".gml": "GML",
        }
        driver = driver_map.get(extension, "GPKG")  # Default to GeoPackage

        # Write reprojected data
        pyogrio.write_dataframe(gdf_reprojected, output_path, driver=driver)

        # Get output metadata
        output_info = pyogrio.read_info(str(output_path))

        # Extract bounds
        bounds_tuple = None
        if "total_bounds" in output_info and output_info["total_bounds"] is not None:
            b = output_info["total_bounds"]
            bounds_tuple = [float(b[0]), float(b[1]), float(b[2]), float(b[3])]

        return {
            "src_crs": used_src_crs,
            "dst_crs": dst_crs,
            "feature_count": int(output_info.get("features", 0) or 0),
            "geometry_type": output_info.get("geometry_type"),
            "bounds": bounds_tuple,
            "driver": driver,
            "output_path": str(output_path),
        }

    except Exception as e:
        if "CRS" in str(e) or "projection" in str(e).lower():
            raise ToolError(
                f"Invalid CRS specification. "
                f"Source: {src_crs or 'auto-detect'}, Destination: {dst_crs}. "
                f"Please use standard formats like 'EPSG:3857', 'EPSG:4326'. "
                f"Original error: {e}"
            ) from e
        elif "cannot open" in str(e).lower() or "does not exist" in str(e).lower():
            raise ToolError(
                f"Cannot open vector dataset at '{input_path}'. "
                f"Ensure: (1) file exists, (2) valid vector format "
                f"(Shapefile, GeoPackage, GeoJSON, KML). "
                f"Original error: {e}"
            ) from e
        else:
            raise ToolError(f"Vector reprojection failed: {e}") from e


class Params(BaseModel):
    """Parameters for vector reprojection."""

    dst_crs: str = Field(
        description="Destination CRS (e.g., 'EPSG:4326', 'EPSG:3857')",
        pattern=r"^(EPSG:\d+|[A-Z]+:.+)$",
    )
    src_crs: str | None = Field(
        None,
        description="Source CRS override (auto-detected if None)",
    )

    model_config = ConfigDict()


class Result(BaseModel):
    """Result of a vector reprojection operation."""

    output: ResourceRef = Field(description="Reference to the output vector file")
    src_crs: str = Field(description="Source CRS that was used")
    dst_crs: str = Field(description="Destination CRS")
    feature_count: int = Field(ge=0, description="Number of features in output")
    geometry_type: str | None = Field(
        None, description="Primary geometry type (Point, LineString, Polygon, etc.)"
    )
    bounds: list[float] | None = Field(
        None,
        min_length=4,
        max_length=4,
        description="Output bounds [minx, miny, maxx, maxy] in dst_crs",
    )
