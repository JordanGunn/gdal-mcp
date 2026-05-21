# GDAL MCP

**Geospatial AI with epistemic reasoning**

GDAL MCP is a Model Context Protocol (MCP) server that provides AI agents with geospatial analysis capabilities while requiring them to **justify their methodological choices** through a reflection middleware system.

**v1.1.3 Released (2026-02-25)**

- Added sub-regional spatial query capability.
- Added environment variable config options.

[![CI](https://github.com/Wayfinder-Foundry/gdal-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Wayfinder-Foundry/gdal-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP 2.0](https://img.shields.io/badge/FastMCP-2.0-blue.svg)](https://github.com/jlowin/fastmcp)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/gdal-mcp?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/gdal-mcp)
[![Listed on Spark](https://spark.entire.vc/badges/listed.svg)](https://spark.entire.vc/assets/vb-gdal?utm_source=github&utm_medium=readme)
[![Install via Spark](https://spark.entire.vc/badges/vb-gdal/install.svg)](https://spark.entire.vc/assets/vb-gdal?utm_source=github&utm_medium=readme)

---

## Documentation

1. **[Installation, setup, and MCP configuration](QUICKSTART.md)**
2. **[Complete tool documentation with examples](TOOLS.md)**
3. **[Runtime configuration and tool surface controls](docs/ENVIRONMENT_VARIABLES.md)**
4. **[Long-term roadmap and philosophy](docs/VISION.md)**
5. **[Release history and updates](CHANGELOG.md)**

---

## Quick Start

### Install via uvx (Recommended)

```bash
# Run directly from PyPI
uvx --from gdal-mcp gdal --transport stdio
```

### MCP Configuration (Claude Desktop)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

**See [QUICKSTART.md](QUICKSTART.md) for:**
- Alternative installation methods (Docker, local development)
- Detailed MCP client configuration
- Workspace security setup
- Troubleshooting guide

---

## Key Features

### Reflection Middleware

- Pre-execution reasoning for CRS selection, resampling methods.
- Structured justifications: intent, alternatives, choice, tradeoffs, confidence.
- Persistent cache with 75% hit rates in multi-operation workflows.
- Cross-domain cache sharing. Justifications span both raster and vector operations.

### Comprehensive Toolset

- **Raster tools:** info, convert, reproject, stats, query
- **Vector tools:** info, reproject, convert, clip, buffer, simplify, query

> See **[Tools Reference](TOOLS.md)** for complete documentation

---

## The Reflection System

### What Makes GDAL MCP Different?

Most AI tool systems execute operations immediately when requested. GDAL MCP requires the AI to **justify methodological decisions** before execution, creating a conversation about the "why" rather than just executing the "what."

**Traditional AI tool approach:**
```text
User: "Reproject this DEM to Web Mercator"
AI: *silently executes operation*
Result: DEM reprojected (but with what resampling? why that CRS? what tradeoffs?)
```

**GDAL MCP:**
```text
---
User:
  > Reproject this DEM to Web Mercator for my web map
---
AI:
  [[reflection middleware intercepts]]
---
AI:
  """
  Before reprojecting to EPSG:3857, let me justify this CRS choice:
     
  Intent:
    Web Mercator preserves angles (conformal projection), essential for web tile rendering and navigation
     
  Alternatives considered:
  - EPSG:4326 (WGS84) → rejected:
    - not conformal, distorts shapes
  - Local UTM → rejected:
    - limited extent, not web-standard
     
  Tradeoffs:
    Area distortion increases at high latitudes (acceptable for web visualization)
     
  Confidence:
    High; This is the standard for web mapping.

  [[justification stored, operation proceeds]]
  """
---
Result:
  DEM reprojected with documented methodology
```

### Why This Matters

**1. Utilizes Full MCP Protocol Capabilities**

The Model Context Protocol isn't just about tool exposure. MCP exposes other primitives for agentic reasoning and interaction. 

The reflection system leverages MCP's design to enable:
- Pre-execution prompting (tool dependencies)
- Structured reasoning (schema-validated justifications)
- Stateful workflows (justification caching)
- Human-in-the-loop interaction (advisory prompts)

**2. Prevents Silent Failures**

Geospatial operations can execute successfully while producing methodologically incorrect results:
- Nearest-neighbor resampling on continuous elevation data creates artifacts
- Web Mercator for area calculations creates up to 40%+ distortion
- Bilinear interpolation on categorical data creates invalid class values

The reflection system surfaces these choices for validation.

**3. Educational, Not Restrictive**

The AI model isn't blocked from executing operations. it's required to demonstrate understanding:
- First use: Explains reasoning, teaches methodology
- Cached: Instant execution (knowledge persists)
- Result: 75%+ cache hit rates, minimal friction

**4. Creates Audit Trail**

Every methodological decision is documented with:
- Intent: what property must be preserved?
- Alternatives: what else was considered?
- Rationale: why this choice?
- Tradeoffs: what are the limitations?
- Confidence: high/medium/low

This enables **reproducible geospatial science**.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Rasterio](https://github.com/rasterio/rasterio) and [GDAL](https://gdal.org)
- Inspired by the [Model Context Protocol](https://modelcontextprotocol.io)

---

**Built with ❤️ for the geospatial AI community**

*Geospatial operations that think, not just execute.*
