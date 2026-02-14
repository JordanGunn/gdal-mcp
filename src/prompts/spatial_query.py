"""Spatial query extent justification prompt."""

from fastmcp import FastMCP
from fastmcp.prompts import Message, PromptMessage


def register(mcp: FastMCP) -> None:
    """Register spatial query extent justification prompt."""

    @mcp.prompt(
        name="justify_query_extent",
        description="Advisory guidance for spatial query extent selection.",
        tags={"reasoning", "spatial_query"},
    )
    def justify_query_extent(
        geometry: dict | list[float],
        purpose: str | None = None,
    ) -> list[PromptMessage]:
        """Guide reasoning about spatial query extent choice.

        Args:
            geometry: GeoJSON geometry or [minx, miny, maxx, maxy] bbox.
            purpose: Optional purpose for the query.
        """
        purpose_text = purpose or "unspecified"
        content = (
            "You are about to perform a spatial query. "
            "Provide methodological justification for the "
            "chosen spatial extent.\n\n"
            f"**Purpose:** {purpose_text}\n"
            f"**Geometry:** {geometry}\n\n"
            "**Provide structured reasoning:**\n"
            "```json\n"
            "{\n"
            '  "intent": "what spatial property must this area satisfy?",\n'
            '  "alternatives": [\n'
            '    {"extent": "broader or narrower alternative", "why_not": "reason"}\n'
            "  ],\n"
            '  "choice": {\n'
            '    "extent": "summary of chosen extent",\n'
            '    "rationale": "why this extent fits the intent",\n'
            '    "tradeoffs": "coverage vs detail, speed vs precision"\n'
            "  },\n"
            '  "confidence": "low|medium|high"\n'
            "}\n"
            "```\n\n"
            "If the extent seems too narrow or too broad for the purpose, "
            "ask for clarification before proceeding."
        )
        return [Message(content=content, role="user")]
