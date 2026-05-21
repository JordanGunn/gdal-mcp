"""Base catalog collection logic for workspace scanning."""

from collections.abc import Sequence
from typing import Literal

from fastmcp import Context

from src.shared.catalog import scan
from src.shared.catalog.models import CatalogResponse


def collect_entries(
    *,
    ctx: Context | None,
    kind: Literal["all", "raster", "vector"],
    include_hidden: bool = False,
    extensions: Sequence[str] | None = None,
) -> CatalogResponse:
    """Collect and format catalog entries for a given dataset kind."""
    entries = scan(
        kind=kind,
        include_hidden=include_hidden,
        allowed_extensions=extensions,
        ctx=ctx,
    )
    return CatalogResponse(
        kind=None if kind == "all" else kind,
        entries=[entry.to_dict() for entry in entries],
        total=len(entries),
    )
