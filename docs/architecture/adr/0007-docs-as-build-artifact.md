---
title: "ADR-0007: Documentation and context as a build artifact"
status: active
owner: integration
last_verified: 2026-10-23
---

# ADR-0007: Documentation and context as a build artifact

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** integration

## Context

AgentCity will be built and maintained largely by AI agents with limited context
windows. Prose that drifts from the code is worse than no prose: it causes
confident wrong changes. The user explicitly requires that another AI can
understand the project without reading the whole codebase.

## Decision

Treat the context pack as a build artifact with mechanical checks:

- `docs/AI_CONTEXT.md` is the one-page onboarding source.
- `docs/PROJECT_MANIFEST.json` is the machine-readable truth for versions,
  paths, commands, tools, and feature status.
- `docs/agentcity/state-of-build.md` and `docs/repo-map.md` are generated from
  the manifest, never hand-edited.
- Every doc has frontmatter (`title`, `status`, `owner`, `last_verified`) and
  resolves its links.
- `scripts/check-docs.py` fails the build on broken links, invalid status,
  missing required docs, malformed Mermaid, or manifest drift.
- `docs/engineering/change-recipes.md` gives exact file checklists so an agent
  does not have to rediscover the wiring.

## Consequences

**Positive**

- A fresh agent can start correctly in minutes.
- Stale claims are caught mechanically rather than by memory.
- Status cannot silently inflate: evidence paths must exist.

**Negative**

- Documentation changes add overhead to every feature.
- Generated files must be regenerated after manifest edits.
- The checker itself must be maintained.

## Guardrails

- CI (and the local pre-commit routine) runs the doc check.
- A feature PR that changes behavior without changing docs is rejected.
- Templates are exempt from frontmatter but must remain valid Markdown.
- Historical source material lives under `docs/agentcity/source-brief/` and is
  clearly marked non-authoritative.
