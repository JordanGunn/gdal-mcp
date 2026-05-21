"""Constructs the FastMCP instance and wires all tools, resources, prompts, and middleware.

Tool / resource modules import `mcp` from this module and register
themselves on import via `@mcp.tool` / `@mcp.resource` / `@mcp.prompt`
decorators. The `mcp` symbol must be defined before those side-effect
imports run; subsequent `from src.server import mcp` calls from within
those modules resolve against the partially-loaded module (cf. circular-
import-by-attribute-attachment).
"""

from __future__ import annotations

from fastmcp import FastMCP

from src.config import is_raster_tools_enabled, is_vector_tools_enabled
from src.middleware.paths import PathValidationMiddleware
from src.middleware.reflection_middleware import ReflectionMiddleware
from src.prompts import register_prompts

mcp = FastMCP(
    name="GDAL-MCP",
    instructions=(
        "GDAL-MCP provides geospatial data processing tools, resources, and methodology "
        "guidance. You have access to: (1) Tools for raster/vector operations "
        "(reproject, convert, info, stats), (2) Resources for discovering workspace data, "
        "file metadata, and reference knowledge (CRS, compression, resampling methods), "
        "(3) Prompts for epistemic reasoning when scientific correctness requires "
        "methodological justification. Operations touching CRS/datum, resampling, hydrology "
        "conditioning, or aggregation may trigger epistemic preflight to ensure scientific "
        "validity."
    ),
)

# ===============================================================
# resources/catalog (always available)
# ===============================================================
import src.resources.catalog.all  # noqa: E402, F401, I001
import src.resources.catalog.by_crs  # noqa: E402, F401
import src.resources.catalog.summary  # noqa: E402, F401
import src.tools.reflection.store_justification  # noqa: E402, F401

if is_raster_tools_enabled():
    import src.resources.catalog.raster  # noqa: E402, F401

if is_vector_tools_enabled():
    import src.resources.catalog.vector  # noqa: E402, F401

# ===============================================================
# resources/metadata
# ===============================================================
if is_raster_tools_enabled():
    import src.resources.metadata.band  # noqa: E402, F401
    import src.resources.metadata.raster  # noqa: E402, F401
    import src.resources.metadata.statistics  # noqa: E402, F401

if is_vector_tools_enabled():
    import src.resources.metadata.vector  # noqa: E402, F401

if is_raster_tools_enabled() or is_vector_tools_enabled():
    import src.resources.query.result  # noqa: E402, F401

# ===============================================================
# tools
# ===============================================================
if is_raster_tools_enabled():
    import src.tools.raster.convert  # noqa: E402, F401
    import src.tools.raster.info  # noqa: E402, F401
    import src.tools.raster.query  # noqa: E402, F401
    import src.tools.raster.reproject  # noqa: E402, F401
    import src.tools.raster.stats  # noqa: E402, F401

if is_vector_tools_enabled():
    import src.tools.vector.buffer  # noqa: E402, F401
    import src.tools.vector.clip  # noqa: E402, F401
    import src.tools.vector.convert  # noqa: E402, F401
    import src.tools.vector.info  # noqa: E402, F401
    import src.tools.vector.query  # noqa: E402, F401
    import src.tools.vector.reproject  # noqa: E402, F401
    import src.tools.vector.simplify  # noqa: E402, F401

# ===============================================================
# prompts
# ===============================================================
register_prompts(mcp)

# ===============================================================
# middleware
# ===============================================================
# Path validation enforces workspace boundaries and prevents directory traversal.
mcp.add_middleware(PathValidationMiddleware())
# Reflection middleware intercepts tool calls and checks for required justifications.
mcp.add_middleware(ReflectionMiddleware())

__all__ = ["mcp"]
