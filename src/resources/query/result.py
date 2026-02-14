"""Resource for spatial query results."""

from fastmcp import Context
from fastmcp.exceptions import ToolError

from src.app import mcp
from src.shared.query_registry import get_query_result


@mcp.resource("query://result/{query_id}")
def get_query_result_resource(query_id: str, ctx: Context | None = None) -> dict:
    """Return metadata for a query result by id."""
    result = get_query_result(query_id)
    if result is None:
        raise ToolError(f"Query result '{query_id}' not found or expired.")

    if ctx:
        ctx.debug(f"[query://result] Returned metadata for {query_id}")

    return result
