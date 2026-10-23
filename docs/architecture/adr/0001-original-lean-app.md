---
title: "ADR-0001: Build an original lean application, not a fork"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0001: Build an original lean application, not a fork

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** architecture
- **Supersedes:** the build pack's "Personal Jarvis first" assumption

## Context

The build pack recommends evaluating Personal Jarvis as the primary foundation.
A real audit of the published repository and this machine changed the calculus:

- Personal Jarvis is a **PySide6/Qt Python application**, not a React desktop
  shell. Adopting it means adopting its UI stack, not the planned one.
- The repository is about **1.2 GB**, with 178 KB of pinned requirements and
  optional Kafka, RabbitMQ, MQTT, and Redis extras.
- Its orchestrator would compete with Google ADK unless large parts were
  removed, which is a rewrite with extra licensing obligations.
- Its license is Apache-2.0 from v2, with older MIT releases. Preserving NOTICE,
  trademark, and third-party obligations is additional work.
- The target machine has **7.8 GB RAM**, making a heavy Qt app plus a Python
  sidecar plus a browser-engine UI a poor fit.
- The other candidates are also mismatched: OpenHands is 541 MB and a separate
  platform; OpenComputer is a 186 KB experimental wrapper; Mission Control is an
  alpha dashboard; OpenDex is a narrow voice harness.

## Decision

AgentCity is an original application. We reuse **capabilities and protocols**
through adapters (Google ADK, SkillBridge MCP, OS APIs) and reference the
candidate projects only for product and interaction ideas. No source is copied.
Licensing is MIT for our code, with third-party notices for tools.

## Consequences

**Positive**

- Full control of architecture, security model, UI, and resource footprint.
- No upstream trademark, NOTICE, or dependency entanglement.
- One orchestration brain (ADK) and one deterministic engine.
- The codebase stays small enough for AI agents to reason about.

**Negative**

- We must build the desktop shell, mission UI, and permission broker ourselves.
- We forgo any mature computer-use code in Personal Jarvis.
- Feature parity with a large project will take longer; scope must stay honest.

## Guardrails

- Before adding a dependency, record the need, size, license, and Windows
  support. No candidate becomes a dependency without an ADR update.
- Review the candidate projects again only if a concrete gap appears, and pin
  the exact commit if any code is ever imported.

## References

- `docs/agentcity/reuse-audit.md`
- `docs/agentcity/tooling-inventory.md`
- `THIRD_PARTY_NOTICES.md`
