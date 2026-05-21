"""Resource for spatial query results."""

from fastmcp.exceptions import ToolError

from src.server import mcp
from src.shared.query_registry import get_query_result


@mcp.resource("query://result/{query_id}")
def get_query_result_resource(query_id: str) -> dict:
    """Return metadata for a query result by id."""
    result = get_query_result(query_id)
    if result is None:
        raise ToolError(f"Query result '{query_id}' not found or expired.")

    return result
