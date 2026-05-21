# ADR-0016-distribution-strategy.md

## Title

Distribution: local `uvx` and remote container

## Status

Superseded by ADR-0003

## Context

Users may not have native GDAL locally.

## Decision

* Support **local dev** via `uvx` with pinned wheels.
* Provide **Docker image** with the full stack for remote HTTP deployments; document MCP host config for remote connections.

## Consequences

* Pro: Frictionless adoption; works for both dev and teams.
* Con: Maintain image and tag discipline.
