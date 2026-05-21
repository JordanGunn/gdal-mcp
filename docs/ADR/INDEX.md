# ADR Index

Architecture Decision Records for gdal-mcp. Status reflects what's in the
codebase as of v1.1.3, not what the ADR originally proposed.

| #    | Title                                                   | Status                              |
|------|---------------------------------------------------------|-------------------------------------|
| [0001](0001-fastmcp-foundation.md) | FastMCP foundation                                      | Implemented                         |
| [0002](0002-transport-stdio-http.md) | Transport (stdio first, optional HTTP)                  | Implemented                         |
| [0003](0003-distribution-uvx-docker.md) | Distribution via uvx and Docker                         | Implemented                         |
| [0004](0004-adopt-fastmcp-and-python-native-stack.md) | Adopt FastMCP + Python-native stack                     | Implemented                         |
| [0005](0005-mvp-scope-tools-and-primitives.md) | MVP scope: tools and primitives                         | Implemented                         |
| [0006](0006-transport-and-deployment.md) | Transport & deployment strategy                         | Superseded by ADR-0002 and ADR-0003 |
| [0007](0007-structured-outputs-and-schemas.md) | Structured outputs and schemas                          | Implemented                         |
| [0008](0008-error-handling-and-safety.md) | Error handling and safety                               | Implemented                         |
| [0009](0009-concurrency-and-memory-model.md) | Concurrency and memory model                            | Implemented                         |
| [0011](0011-crs-and-resampling-policy.md) | CRS and resampling policy                               | Implemented                         |
| [0012](0012-resource-strategy-and-binary-io.md) | Resource strategy and binary I/O                        | Implemented                         |
| [0013](0013-configuration-isolation.md) | Configuration isolation                                 | Implemented                         |
| [0014](0014-observability-and-logging.md) | Observability and logging                               | Implemented                         |
| [0015](0015-testing.md) | Testing strategy                                        | Implemented                         |
| [0016](0016-distribution.md) | Distribution strategy                                   | Superseded by ADR-0003              |
| [0017](0017-pydantic-models-for-structured-io.md) | Pydantic models for structured I/O                      | Implemented                         |
| [0018](0018-hybrid-vector-processing-stack.md) | Hybrid vector processing stack (pyogrio + geopandas)    | Implemented                         |
| [0019](0019-parallel-processing-strategy-dask.md) | Parallel processing (Dask)                              | Proposed                            |
| [0020](0020-context-driven-tool-design.md) | Context-driven tool design                              | Implemented                         |
| [0021](0021-llm-optimized-tool-descriptions.md) | LLM-optimized tool descriptions                         | Implemented                         |
| [0022](0022-workspace-scoping-and-access-control.md) | Workspace scoping and access control                    | Implemented                         |
| [0023](0023-resource-taxonomy-and-hierarchy.md) | Resource taxonomy and hierarchy                         | Implemented                         |
| [0024](0024-context-usage-and-logging-policy.md) | Context usage and logging policy                        | Implemented                         |
| [0025](0025-catalog-resources.md) | Catalog resources                                       | Implemented                         |
| [0026](0026-epistemic-governance.md) | Epistemic governance (reflection middleware)            | Implemented                         |
| [0027](0027-spatial-query-primitives.md) | Conversational spatial query layer                      | Implemented                         |

## Numbering

There is no ADR-0010. Numbers are otherwise contiguous from 0001 to 0027.

## Notes on status assignment

- **Implemented** — the decision is reflected in code as of v1.1.3.
- **Proposed** — accepted as a direction but not yet in the codebase
  (only ADR-0019 / Dask is in this state).
- **Superseded by ADR-NNNN** — an older draft whose content was rewritten
  in a later, more detailed ADR. The original is retained for historical
  context but the later ADR is authoritative.

When opening a new ADR, add it to this index.
