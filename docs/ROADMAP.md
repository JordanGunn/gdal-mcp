---
type: product_context
title: GDAL MCP Roadmap
tags: [gdal, mcp, roadmap, planning]
---

# GDAL MCP Roadmap

## ✅ Completed Milestones

### M1: Foundation & Compliance (v0.1.0)
- ✅ FastMCP 2.0 foundation with native middleware support
- ✅ Stdio transport for Claude Desktop integration
- ✅ MCP compliance: initialization, versioning, capabilities
- ✅ Structured logging to stderr

### M2: Core Tools (v0.2.0)
- ✅ `raster_info` - Metadata inspection with Rasterio
- ✅ `raster_convert` - Format conversion with compression/overviews
- ✅ `raster_reproject` - CRS transformation with explicit resampling
- ✅ `raster_stats` - Statistical analysis with histograms
- ✅ `vector_info` - Vector metadata with pyogrio/fiona

### M3: Packaging & Distribution (v0.3.0)
- ✅ uvx entrypoint `gdal-mcp`
- ✅ Dockerfile with GDAL 3.8+ base
- ✅ PyPI publishing with CI/CD
- ✅ Docker Hub automated builds

### M4: Observability & Quality (v0.4.0)
- ✅ Full type safety (mypy strict mode)
- ✅ 72 comprehensive tests with fixtures
- ✅ PathValidationMiddleware for workspace security
- ✅ Real-time feedback via FastMCP Context API

### M5: Resource Taxonomy (v0.5.0)
- ✅ Workspace catalog: `catalog://workspace/{all|raster|vector}/{subpath}`
- ✅ Metadata resources: `metadata://{file}/format`
- ✅ Reference library: `reference://crs/common/{coverage}`
- ✅ Compression guide, resampling guide, glossary

### M6: Epistemic Governance (v1.0.0) 🎉
- ✅ Reflection middleware with FastMCP interception
- ✅ Structured justification schema (intent, alternatives, choice, tradeoffs, confidence)
- ✅ Persistent cache: `.preflight/justifications/{domain}/sha256:{hash}.json`
- ✅ CRS selection reasoning (`justify_crs_selection`)
- ✅ Resampling method reasoning (`justify_resampling_method`)
- ✅ Integration with `raster_reproject` tool
- ✅ Cache intelligence (parameter-based hit/miss)
- ✅ 7-scenario testing guide with validation

## 🚧 Active Development

### v1.0.1 — Advisory Prompting Pattern (Released 2025-10-26) ✅
- ✅ All reflection prompts updated to advisory tone
- ✅ Conversational intervention over blocking
- ✅ Educational design principle documented
- ✅ ADR-0026 amendment
- **Classification:** Patch release (UX refinement, non-breaking)

### v1.1.0 — Vector Tool Parity & Composition (Q1 2025)

**Strategic Pivot:** Focus on vector tool expansion and natural composition patterns before deeper reflection domains.

**Goal:** Achieve raster-vector feature parity and explore how models naturally compose operations through tool discovery.

**Vector tool expansion:**
- [ ] `vector_reproject` - CRS transformation for vector datasets
  - Match `raster_reproject` capabilities
  - Reuse `justify_crs_selection` reflection (cross-tool consistency)
- [ ] `vector_convert` - Format conversion (Shapefile → GeoPackage, etc.)
  - Match `raster_convert` pattern
  - Leverage existing compression/format resources
- [ ] `vector_clip` - Spatial subsetting by bounding box or geometry
- [ ] `vector_buffer` - Buffer/proximity analysis
- [ ] `vector_simplify` - Geometry simplification (Douglas-Peucker, Visvalingam)

**Tool composition exploration:**
- [ ] Natural composition testing
  - Can models discover multi-step workflows without explicit prompting?
  - Example: "Prepare data for web display" → reproject + convert + tile
  - Example: "Extract city boundaries" → clip vector + reproject + simplify
- [ ] Composition guidance resources
  - `reference://workflows/common-patterns` - Typical operation sequences
  - Document: raster prep, vector cleaning, format migration patterns
- [ ] Cross-domain operations
  - Vector-raster interaction: clip raster by vector, zonal stats (future)
  - Test if models naturally chain: reproject vector → clip raster → analyze

**Observability for composition:**
- [ ] Session tracking for multi-step workflows
  - Log operation sequences
  - Identify common patterns
  - Measure: Does the model chain tools effectively?

**Deferred to v2.x:**
- Hydrology conditioning (raster_fill_sinks, flow analysis)
- Aggregation tools (raster_zonal_stats with vector zones)
- Deep reflection domains (format selection already covered by resources)
  - `history://operations/{session_id}` - operation log with justifications

### v1.2.0 — Semantic Primitives (Q2 2025)

**Goal:** Enable higher-level geospatial reasoning

**Terrain analysis:**
- [ ] `terrain_derivatives` - slope, aspect, hillshade, curvature
  - Reflection: algorithm choice (Horn, Zevenbergen-Thorne), edge handling
- [ ] `viewshed` - visibility analysis from observer points
  - Reflection: Earth curvature, atmospheric refraction parameters

**Classification:**
- [ ] `raster_classify` - threshold-based classification
  - Reflection: threshold selection justification, class boundaries
- [ ] `spectral_indices` - NDVI, NDWI, EVI calculation
  - Reflection: index selection for land cover type

**Discovery resources:**
- [ ] `catalog://workspace/by-crs/{epsg}` - CRS-organized file index
- [ ] `summary://workspace/coverage` - spatial extent union
- [ ] Richer metadata stats in catalog responses

## 🔮 Future Vision

### v2.0.0 — Full Analysis Suite (Q3 2025)

**Vector analysis:**
- Spatial joins (point-in-polygon, intersects, contains)
- Overlay operations (union, intersection, difference)
- Buffer/clip with distance unit reasoning
- Attribute queries with SQL generation

**Raster analysis:**
- Raster calculator with band math validation
- Zonal statistics with aggregation reflection
- Contour generation with interval selection
- Cost distance and path analysis

**Semantic capabilities:**
- Urban detection from multispectral imagery
- Water body classification with spectral indices
- Land cover change detection workflows
- Automated feature extraction with confidence scores

### Beyond v2.0

**Advanced reasoning:**
- Uncertainty propagation through analysis chains
- Alternative workflow suggestions ("You could also...")
- Quality assessment prompts (check for artifacts, validate ranges)
- Multi-modal reasoning (imagery + vector + terrain)

**Collaboration:**
- Shared justification libraries (team knowledge base)
- Methodology templates for common workflows
- Export justifications to research documentation

## Implementation Priorities

### Immediate (v1.1.0 development)
1. Implement hydrology reflection domain
2. Create aggregation reasoning prompts
3. Add format selection justification
4. Build multi-step workflow chains
5. Add provenance tracking

### Near-term (v1.2.0 planning)
1. Design terrain analysis tool suite
2. Draft classification reflection prompts
3. Prototype semantic index calculations
4. Enhance catalog with CRS organization
5. Create workspace summary resources

### Long-term (v2.0.0 vision)
1. Vector spatial analysis primitives
2. Advanced raster operations
3. Workflow discovery intelligence
4. Uncertainty quantification
5. Team collaboration features

## Success Metrics

**v1.0.0 achievements:**
- ✅ Reflection system operational (7/7 test scenarios passing)
- ✅ Cache hit rate > 80% in multi-operation workflows
- ✅ Zero silent methodological errors (all require justification)
- ✅ 72 tests passing with full type safety

**v1.1.0 targets:**
- [ ] 3+ reflection domains operational
- [ ] Multi-step workflow composition demonstrated
- [ ] Provenance chain validation
- [ ] 100+ tests with extended coverage

**v2.0.0 targets:**
- [ ] 10+ analysis primitives with reflection
- [ ] Semantic reasoning demonstrations
- [ ] Automated workflow discovery
- [ ] Production deployment case studies

---

**Status:** v1.2.0 released (cleanup release on top of v1.1.3).

See [README.md](../README.md) for current capabilities and [CHANGELOG.md](../../CHANGELOG.md) for the full release history.
