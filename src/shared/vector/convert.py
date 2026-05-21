"""Vector format conversion using pyogrio."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pyogrio
from fastmcp import Context
from fastmcp.exceptions import ToolError
from pydantic import BaseModel, ConfigDict, Field

from src.shared.resourceref import ResourceRef


def convert(
    input_path: str,
    output_path: str | Path,
    driver: str | None = None,
    encoding: str = "UTF-8",
    ctx: Context | None = None,
) -> dict[str, Any]:
    """Convert a vector dataset to a different format using pyogrio.

    Args:
        input_path: Path to source vector dataset
        output_path: Path for output vector file
        driver: Optional output driver (auto-detected from extension if None)
        encoding: Character encoding for output (default UTF-8)
        ctx: Optional FastMCP context for logging

    Returns:
        Dictionary with conversion metadata:
        - src_driver: Source driver detected
        - dst_driver: Destination driver used
        - feature_count: Number of features
        - geometry_type: Primary geometry type
        - encoding: Character encoding used

    Raises:
        ToolError: If conversion fails
    """
    try:
        # Read source info to get driver and metadata
        source_info = pyogrio.read_info(input_path)
        src_driver = source_info.get("driver", "Unknown")

        # Determine output driver from extension if not specified
        output_path_obj = Path(output_path)
        extension = output_path_obj.suffix.lower()

        if driver is None:
            # Auto-detect driver from file extension
            driver_map = {
                ".shp": "ESRI Shapefile",
                ".gpkg": "GPKG",
                ".geojson": "GeoJSON",
                ".json": "GeoJSON",
                ".kml": "KML",
                ".gml": "GML",
            }
            dst_driver = driver_map.get(extension, "GPKG")  # Default to GeoPackage
        else:
            dst_driver = driver

        # Read entire dataset into GeoDataFrame
        gdf = pyogrio.read_dataframe(input_path)

        # Write to output format
        # Layer name for certain formats
        layer_name = output_path_obj.stem

        # Build write options
        write_kwargs: dict[str, Any] = {
            "driver": dst_driver,
        }

        # Add encoding for drivers that support it
        if dst_driver in ["ESRI Shapefile", "GML"]:
            write_kwargs["encoding"] = encoding

        # Add layer name for formats that support it
        if dst_driver in ["GPKG", "GML"]:
            write_kwargs["layer"] = layer_name

        pyogrio.write_dataframe(gdf, output_path, **write_kwargs)

        # Get output metadata
        output_info = pyogrio.read_info(str(output_path))

        return {
            "src_driver": src_driver,
            "dst_driver": dst_driver,
            "feature_count": int(output_info.get("features", 0) or 0),
            "geometry_type": output_info.get("geometry_type"),
            "encoding": encoding,
        }

    except Exception as e:
        if "driver" in str(e).lower():
            raise ToolError(
                f"Unsupported driver: {driver}. "
                f"Supported formats: Shapefile (.shp), GeoPackage (.gpkg), "
                f"GeoJSON (.geojson), KML (.kml), GML (.gml). "
                f"Original error: {e}"
            ) from e
        elif "cannot open" in str(e).lower() or "does not exist" in str(e).lower():
            raise ToolError(
                f"Cannot open source vector dataset at '{input_path}'. "
                f"Ensure file exists and is a supported format. "
                f"Original error: {e}"
            ) from e
        elif "encoding" in str(e).lower():
            raise ToolError(
                f"Encoding error during conversion. "
                f"Try different encoding (e.g., 'ISO-8859-1' for legacy data). "
                f"Original error: {e}"
            ) from e
        else:
            raise ToolError(f"Vector format conversion failed: {e}") from e


class Params(BaseModel):
    """Parameters for vector format conversion."""

    driver: str | None = Field(
        None,
        description="Output driver (auto-detected from extension if None). "
        "Options: 'ESRI Shapefile', 'GPKG', 'GeoJSON', 'KML', 'GML'",
    )
    encoding: str = Field(
        "UTF-8",
        description="Character encoding for output (UTF-8 recommended, "
        "ISO-8859-1 for legacy shapefile compatibility)",
    )

    model_config = ConfigDict()


class Result(BaseModel):
    """Result of a vector format conversion operation."""

    output: ResourceRef = Field(description="Reference to the output vector file")
    src_driver: str = Field(description="Source driver detected")
    dst_driver: str = Field(description="Destination driver used")
    feature_count: int = Field(ge=0, description="Number of features converted")
    geometry_type: str | None = Field(
        None, description="Primary geometry type (Point, LineString, Polygon, etc.)"
    )
    encoding: str = Field(description="Character encoding used")
