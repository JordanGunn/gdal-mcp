"""Prompt registration for GDAL-MCP server."""

from __future__ import annotations

from fastmcp import FastMCP

from . import crs, resampling, spatial_query

__all__ = ["register_prompts"]


def register_prompts(mcp: FastMCP) -> None:
    """Register epistemic-guidance prompt templates with the FastMCP server."""
    crs.register(mcp)
    resampling.register(mcp)
    spatial_query.register(mcp)
