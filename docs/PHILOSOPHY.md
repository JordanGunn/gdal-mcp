# gdal-mcp Philosophy

**Status:** Living document. Last revised 2026-05-21.

## What this is, in one sentence

A foundation for AI agents to perform geospatial analysis through conversation
with the agent being required to justify methodological choices (CRS, resampling,
query extent) instead of executing silently.

## The problem

Two kinds of expertise rarely live in the same person:

- **Domain knowledge** — terrain, hydrology, ecology, urban planning.
- **Geospatial tooling** — projections, resampling, format quirks, CLI syntax.

The result is friction: someone who understands watersheds gets blocked at
"which GDAL flag" rather than at "what question am I asking." gdal-mcp doesn't
remove the tooling — it lets an AI agent operate the tooling on behalf of the
domain expert, but only after the agent has demonstrated that its methodological
choices are sound.

## Why "justified" instead of just "automated"

The same geospatial operation can produce a correct number or a quietly wrong
one depending on a methodological choice:

- Nearest-neighbour resampling on continuous elevation creates step artifacts.
- Web Mercator distorts area by ~40% at high latitudes; using it for an area
  calculation gives the wrong answer.
- Bilinear interpolation on a categorical classification produces invalid class
  values.

A tool that always succeeds tells you nothing about whether the result is
methodologically defensible. The reflection middleware exists to surface these
decisions: before `raster_reproject` runs, the agent has to record (intent,
alternatives considered, choice, tradeoffs, confidence) in a
[Justification](REFLECTION.md) schema. The justification is cached
domain-keyed, so the same rationale serves both `raster_reproject` and
`vector_reproject`.

## Principles

1. **Wrap, don't reimplement.** Rasterio, pyogrio, Shapely, pyproj already do
   the geospatial work well. gdal-mcp is a conversational + methodological
   layer on top.

2. **Qualitative → quantitative through dialogue.** "Find flat surfaces for
   calibration" becomes "slope < 2°, area > 100 m², distance to roads < 1 km"
   via clarifying questions, not via the agent guessing the thresholds.

3. **Domain language at the interface, technical language inside.** Users say
   *watershed* or *riparian zone*; tools accept geometries, CRS strings, and
   buffer distances. The agent is responsible for the translation, and the
   reflection layer is where the translation gets recorded.

4. **Iteration over up-front correctness.** Run, evaluate, refine. The cost
   of an extra round of dialogue is small; the cost of misplaced precision
   is large.

5. **Reproducibility.** Every methodological choice writes a justification
   that another agent (or human) can read months later and reconstruct the
   reasoning.

## What this is not

- **Not a chat front-end for QGIS** — the goal is reasoning over operations,
  not replicating a GUI.
- **Not a "natural language to gdalwarp" translator** — there is no
  command-string generation; tools are typed Python wrappers.
- **Not a replacement for the analyst** — the system requires their judgement
  at the methodological choice points; it just stops requiring it at the
  syntax points.
- **Not a research project on epistemic AI.** It's a working MCP server with
  a specific opinionated middleware.

## Phased direction

See [ROADMAP.md](ROADMAP.md) for milestone detail. The shape:

| Phase | Theme                                  | Status                    |
|-------|----------------------------------------|---------------------------|
| 1     | Core tools (info/convert/reproject/stats) and packaging | Shipped (v0.1–v0.4)       |
| 2     | Reflection middleware and vector parity                  | Shipped (v1.0–v1.1)       |
| 3     | Spatial query primitives and result resources            | Shipped (v1.1.3)          |
| 4     | Workflow composition (multi-step orchestration)          | Direction; not implemented |
| 5     | Domain-concept recognition (watershed, viewshed, etc.)  | Direction; not implemented |

Phases 4 and 5 are intentionally vague. They describe a direction, not a
commitment.

## How to evaluate a proposed change

Before adding something to the codebase, ask:

- Does it enable a new conversational pattern, or just compress existing
  syntax?
- Does it surface a methodological choice that should be reflected on, or
  hide one that's currently visible?
- Does it compose with the existing tool surface, or stand alone?
- Is it worth the maintenance cost relative to its conversational value?

If the answers tend toward "compress / hide / standalone / no," it probably
belongs upstream in Rasterio or pyogrio, not here.

## References

- [README.md](../README.md) — what ships today
- [REFLECTION.md](REFLECTION.md) — middleware internals and cache layout
- [ROADMAP.md](ROADMAP.md) — milestone history and direction
