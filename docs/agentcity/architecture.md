---
title: Architecture Entry Point
status: active
owner: architecture
last_verified: 2026-10-23
---

# Architecture Entry Point

The canonical architecture documents live in `docs/architecture/`. This page
exists so the build-pack document set is complete without duplicating content.

- [Architecture overview](../architecture/overview.md) — context, containers,
  components, lifecycle, failures, packaging.
- [System diagrams](../architecture/diagrams.md) — 16 Mermaid views.
- [Interface contracts](../architecture/contracts.md) — API, IPC, events, risk
  classes, errors.
- [Data model](../architecture/data-model.md) — tables, transactions,
  migrations, retention.
- [ADRs](../architecture/adr/) — one-way-door decisions.

## Summary

AgentCity uses one Electron/React desktop shell, one Python FastAPI sidecar, one
deterministic mission engine, and Google ADK as the only agent reasoning
runtime. SkillBridge is integrated as a stdio MCP subprocess. SQLite is the
source of truth; events persist before the UI consumes them. A deterministic
policy broker grants every action; the model never grants its own permission.

## Decisions that shape the system

| ADR | Decision |
|---|---|
| [0001](../architecture/adr/0001-original-lean-app.md) | Original lean app, no fork |
| [0002](../architecture/adr/0002-deterministic-mission-engine.md) | Engine owns durable state |
| [0003](../architecture/adr/0003-electron-shell.md) | Electron + React shell |
| [0004](../architecture/adr/0004-skillbridge-stdio-mcp.md) | SkillBridge over stdio MCP |
| [0005](../architecture/adr/0005-offline-first.md) | Offline-first baseline |
| [0006](../architecture/adr/0006-policy-broker.md) | Deterministic approvals |
| [0007](../architecture/adr/0007-docs-as-build-artifact.md) | Docs are checked artifacts |

## Status

The architecture is designed and documented. Application code begins at M1; see
`implementation-plan.md` and `state-of-build.md`.
