"""Vector buffering using pyogrio and shapely."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pyogrio
from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, ConfigDict, Field

from src.shared.resourceref import ResourceRef


def buffer(
    input_path: str,
    output_path: str | Path,
    distance: float,
    resolution: int = 16,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Create buffer around vector geometries.

    Args:
        input_path: Path to source vector dataset
        output_path: Path for output vector file
        distance: Buffer distance in CRS units
        resolution: Segments per quadrant (default 16)
        ctx: Optional FastMCP context for logging

    Returns:
        Dictionary with buffer metadata:
        - feature_count: Number of features buffered
        - buffer_distance: Distance applied
        - resolution: Segments per quadrant
        - bounds: Output spatial extent

    Raises:
        ToolError: If buffering fails
    """
    try:
        # Read source data
        gdf = pyogrio.read_dataframe(input_path)

        # Check CRS - warn if geographic
        # Note: ctx logging would require async, so we just return info in result
        # The tool wrapper will handle warning the user
        is_geographic = gdf.crs and gdf.crs.is_geographic

        # Create buffers
        # resolution parameter: number of segments per quadrant
        # Higher values create smoother circles but are slower
        gdf_buffered = gdf.copy()
        gdf_buffered["geometry"] = gdf.geometry.buffer(distance, resolution=resolution)

        # Determine output driver from extension
        output_path_obj = Path(output_path)
        extension = output_path_obj.suffix.lower()
        driver_map = {
            ".shp": "ESRI Shapefile",
            ".gpkg": "GPKG",
            ".geojson": "GeoJSON",
            ".json": "GeoJSON",
        }
        driver = driver_map.get(extension, "GPKG")

        # Write buffered data
        pyogrio.write_dataframe(gdf_buffered, output_path, driver=driver)

        # Get output metadata
        output_info = pyogrio.read_info(str(output_path))

        # Extract bounds
        bounds_tuple = None
        if "total_bounds" in output_info and output_info["total_bounds"] is not None:
            b = output_info["total_bounds"]
            bounds_tuple = [float(b[0]), float(b[1]), float(b[2]), float(b[3])]

        return {
            "feature_count": len(gdf_buffered),
            "buffer_distance": distance,
            "resolution": resolution,
            "bounds": bounds_tuple,
            "is_geographic": is_geographic,
        }

    except Exception as e:
        if "distance" in str(e).lower():
            raise ToolError(
                f"Invalid buffer distance: {distance}. "
                f"Distance must be positive and in CRS units "
                f"(meters for projected CRS, degrees for geographic). "
                f"Original error: {e}"
            ) from e
        else:
            raise ToolError(f"Vector buffering failed: {e}") from e


class Params(BaseModel):
    """Parameters for vector buffering."""

    distance: float = Field(
        description="Buffer distance in CRS units (meters for projected, degrees for geographic)",
        gt=0,
    )
    resolution: int = Field(
        16,
        ge=4,
        le=64,
        description="Segments per quadrant for buffer polygon (higher = smoother, slower)",
    )

    model_config = ConfigDict()


class Result(BaseModel):
    """Result of a vector buffer operation."""

    output: ResourceRef = Field(description="Reference to the output vector file")
    feature_count: int = Field(ge=0, description="Number of features buffered")
    buffer_distance: float = Field(description="Buffer distance applied")
    resolution: int = Field(description="Segments per quadrant used")
    bounds: list[float] | None = Field(
        None,
        min_length=4,
        max_length=4,
        description="Output bounds [minx, miny, maxx, maxy]",
    )
