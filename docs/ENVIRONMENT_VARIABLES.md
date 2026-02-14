# Environment Variables

GDAL MCP supports a small set of environment variables to control workspace access,
tool registration, and query result lifecycle.

## Workspace Scoping

- `GDAL_MCP_WORKSPACES` (string, optional)
  - Purpose: Restrict tool access to a colon-separated allowlist of workspace directories.
  - Example: `GDAL_MCP_WORKSPACES="/data/projects:/home/user/gis"`
  - Default: Unset -> all paths allowed (not recommended for production).

## Tool Surface Controls

Use these switches to reduce the available tool surface area.
Values are case-insensitive and must be explicit.

- `VECTOR` (boolean, default: `true`)
  - Purpose: Enable (`1`/`true`) or disable (`0`/`false`) registration of vector tools and vector-only resources.
  - Acceptable values: `1`, `true`, `0`, `false`.
- `RASTER` (boolean, default: `true`)
  - Purpose: Enable (`1`/`true`) or disable (`0`/`false`) registration of raster tools and raster-only resources.
  - Acceptable values: `1`, `true`, `0`, `false`.

When a category is disabled, its tools and single-domain resources are not registered
with FastMCP. Shared prompts and reflection tooling remain available.

## Spatial Query Registry Controls

These tune the in-memory registry for `query://result/{id}` metadata.

- `GDAL_MCP_QUERY_TTL_SECONDS` (integer, default: `900`)
  - Purpose: Time-to-live for query result records.
  - Minimum: `60`
- `GDAL_MCP_QUERY_MAX_RESULTS` (integer, default: `25`)
  - Purpose: Maximum number of query records retained in memory.
  - Minimum: `1`
