"""FastMCP middleware for reflection preflight checks."""

from __future__ import annotations

import logging
from typing import Any

from fastmcp.server.middleware.middleware import CallNext, Middleware, MiddlewareContext

from src.middleware.reflection_transform import reflection_preflight_check

logger = logging.getLogger(__name__)


class ReflectionMiddleware(Middleware):
    """Middleware that performs reflection preflight checks before tool execution.

    This middleware intercepts tool calls and checks if required epistemic
    justifications exist in the cache. If not, it raises a ToolError that
    instructs the LLM to call the appropriate prompt first.
    """

    async def on_call_tool(
        self,
        context: MiddlewareContext[Any],
        call_next: CallNext[Any, Any],
    ) -> Any:
        """Intercept tool calls to perform reflection preflight check."""
        tool_name = context.message.name
        arguments: dict[str, Any] = context.message.arguments or {}

        logger.debug(f"Reflection middleware intercepting tool call: {tool_name}")

        # Raises ToolError if a required justification is missing.
        await reflection_preflight_check(tool_name, arguments)

        return await call_next(context)
