# gdal-mcp

MCP server exposing GDAL/Rasterio operations to AI agents, with a reflection
middleware that requires structured justification before executing operations
whose methodology matters (CRS choice, resampling method, query extent).

[![CI](https://github.com/Wayfinder-Foundry/gdal-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Wayfinder-Foundry/gdal-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP 2.0](https://img.shields.io/badge/FastMCP-2.0-blue.svg)](https://github.com/jlowin/fastmcp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/gdal-mcp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/gdal-mcp)

## Install

### Via uvx (recommended)

```bash
uvx --from gdal-mcp gdal --transport stdio
```

### Via Docker

```bash
docker build -t gdal-mcp .
docker run -i gdal-mcp gdal --transport stdio
```

### Local development

```bash
git clone https://github.com/Wayfinder-Foundry/gdal-mcp.git
cd gdal-mcp
uv sync
uv run gdal --transport stdio
```

## Configure your MCP client

### Claude Desktop

Add to `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`,
Windows: `%APPDATA%\Claude\`, Linux: `~/.config/Claude/`):

```json
{
  "mcpServers": {
    "gdal-mcp": {
      "command": "uvx",
      "args": ["--from", "gdal-mcp", "gdal", "--transport", "stdio"],
      "env": {
        "GDAL_MCP_WORKSPACES": "/path/to/your/geospatial/data"
      }
    }
  }
}
```

Restart Claude Desktop. The MCP server indicator should appear, and the
`raster_*` and `vector_*` tools become available.

### Workspace scoping

`GDAL_MCP_WORKSPACES` is a colon-separated list of directories the server
is allowed to touch (per [ADR-0022](docs/ADR/0022-workspace-scoping-and-access-control.md)).
If unset, all paths are allowed and a warning is logged.

Optional tool-surface flags: `RASTER=true`, `VECTOR=true`. See
[docs/ENVIRONMENT_VARIABLES.md](docs/ENVIRONMENT_VARIABLES.md) for the full set.

## Tools

- **Raster:** `raster_info`, `raster_convert`, `raster_reproject`, `raster_stats`, `raster_query`
- **Vector:** `vector_info`, `vector_convert`, `vector_reproject`, `vector_clip`, `vector_buffer`, `vector_simplify`, `vector_query`
- **Resources:** catalog (`workspace://...`), metadata (`metadata://...`), reference (`reference://...`), query results (`query://result/{id}`)
- **Prompts:** `justify_crs_selection`, `justify_resampling_method`, `justify_query_extent` (and more under `src/prompts/`)

See [TOOLS.md](TOOLS.md) for parameters, return shapes, and worked examples.

## The reflection middleware

Tools whose methodology matters refuse to execute until the calling agent
produces a structured justification. The flow is:

1. Agent calls e.g. `raster_reproject(dst_crs="EPSG:3857", resampling="cubic", ...)`.
2. Middleware checks `.preflight/justifications/{domain}/` for a matching hash.
3. On miss, the call raises `ToolError` with a hint pointing at the
   relevant prompt (e.g. `justify_crs_selection`).
4. Agent calls the prompt, fills out the `Justification` schema (intent,
   alternatives considered, choice, tradeoffs, confidence), and re-invokes
   the tool with a `__reflection` payload.
5. The justification is cached domain-keyed, so a CRS rationale for
   EPSG:3857 satisfies both `raster_reproject` and `vector_reproject`
   on subsequent calls.

See [docs/REFLECTION.md](docs/REFLECTION.md) for the schema and cache layout,
and [docs/VISION.md](docs/VISION.md) for why this exists.

## Documentation

- [TOOLS.md](TOOLS.md) — tool reference
- [docs/ENVIRONMENT_VARIABLES.md](docs/ENVIRONMENT_VARIABLES.md) — runtime config
- [docs/REFLECTION.md](docs/REFLECTION.md) — reflection middleware internals
- [docs/VISION.md](docs/VISION.md) — long-term direction
- [docs/ADR/](docs/ADR/) — architecture decision records
- [CHANGELOG.md](CHANGELOG.md) — release history
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution guide

## Troubleshooting

**`Access denied: path outside allowed workspaces`** — set `GDAL_MCP_WORKSPACES`
to include the directory in question (see "Workspace scoping").

**MCP client doesn't see the server** — verify `uvx --from gdal-mcp gdal --help`
runs on its own, then restart the client after editing its config file.

## License

MIT — see [LICENSE](LICENSE).

Built on [FastMCP](https://github.com/jlowin/fastmcp),
[Rasterio](https://github.com/rasterio/rasterio), [pyogrio](https://github.com/geopandas/pyogrio),
and [Shapely](https://github.com/shapely/shapely).
