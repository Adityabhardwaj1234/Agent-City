---
title: Open-Source Reuse Audit
status: active
owner: architecture
last_verified: 2026-10-23
---

# Open-Source Reuse Audit

Snapshot date: **2026-10-23**. Method: repository metadata reviewed, local
checkouts inspected for the two adopted tools, and architectural fit assessed
against this machine. No candidate source was imported.

## 1. Candidate matrix

| Candidate | Size | Stars | Language | License | Last push | Verdict |
|---|---:|---:|---|---|---|---|
| Personal Jarvis | ~1.2 GB | — | Python (PySide6) | Apache-2.0 | 2026-10-23 | **Reference only** |
| Google ADK | ~93 MB | 21,979 | Python | Apache-2.0 | 2026-10-23 | **Adopted runtime** |
| OpenDex | ~33 MB | 69 | TypeScript | MIT | 2026-09-18 | Reference only |
| Mission Control | ~14 MB | — | — | MIT | 2026-04-21 | Reference only |
| OpenHands | ~541 MB | 91,645 | TypeScript | MIT | 2026-10-23 | Reference only |
| OpenComputer | ~186 KB | 21 | TypeScript | MIT | 2026-10-01 | Reference only |
| ADK Agent Builder Skill | ~0.9 MB | — | Python | Apache-2.0 | 2026-10-19 | **Adopted build tool** |
| SkillBridge | ~6 MB | — | Python | MIT | 2026-10-22 | **Adopted runtime tool** |

Star counts are not quality evidence; they are recorded to show activity and
community scale. Sizes are repository sizes reported by the host, not install
footprints.

## 2. Findings and decisions

### Personal Jarvis — rejected as foundation

Evidence:

- It is a **PySide6/Qt application**, not an Electron/React product.
- Repository size ~1.2 GB, with a 178,542-byte requirements file and optional
  Kafka, RabbitMQ, MQTT, and Redis dependencies.
- Its own orchestrator and agent model would compete with Google ADK.
- Apache-2.0 obligations and trademark guidance would apply to a derivative.
- The host machine has 7.8 GB RAM, making the combined footprint risky.

Decision: reference for product behavior only. ADR-0001 records the rationale.

### Google ADK — adopted

Installed `google-adk` 2.12.0, Apache-2.0, active. It supplies agents, workflow
composition, session state, guardrail callbacks, MCP tools, voice integrations,
and evaluation. We use the library directly and pin the version in the
manifest.

### ADK Agent Builder Skill — adopted at build time

Pinned at `a74d73b20447c8d9beab999bbfa5ddb7d6d748b4`, Apache-2.0. Its 18-command
CLI generates, validates, tests, evaluates, and packages ADK projects. It is a
development tool, not a runtime dependency. See `tooling-inventory.md`.

### SkillBridge — adopted at runtime

Pinned at `25c352e6219e0f9ca45bdbc9a2ff0bafae4ddb06`, MIT. It exposes 19 broker
tools over a stdio MCP server and owns a large skill catalog with verification,
quarantine, and memory governance. We integrate over MCP rather than importing
its internals or reimplementing discovery.

### OpenHands — reference only

A large, mature coding-agent platform with a separate control plane and runtime.
Adopting it would add a second orchestration system and a heavy footprint. The
coding-CLI adapter contract is sufficient for our scope.

### OpenDex — reference only

A narrow Electron voice-first harness. Useful as a UX and provider-adapter
reference, but it does not provide the mission engine, policy model, or ADK
integration we require.

### Mission Control — reference only

An agent fleet dashboard, explicitly alpha per its own documentation. Useful for
panel and event-stream ideas, but its schemas and security posture are not a
foundation for a privileged desktop app.

### OpenComputer — reference only

A small, experimental cross-platform computer-use wrapper whose own README calls
Windows support experimental. We prefer native Windows UI Automation with a
vision fallback, implemented behind our policy broker.

## 3. License and provenance gate

| Requirement | Status |
|---|---|
| Base decision documented | Met (ADR-0001) |
| Exact commits recorded for adopted tools | Met (`a74d73b`, `25c352e`) |
| Upstream licenses preserved | Met (notices in `THIRD_PARTY_NOTICES.md`) |
| No upstream branding or assets copied | Met |
| No source copied from reference projects | Met |
| Dependency footprint measured on target | Pending M1 (idle memory budget defined) |
| Third-party asset/model review | Not applicable yet; gate defined |
| Update strategy for adopted tools | Pin and upgrade intentionally with regression tests |

Newly authored code is MIT. Adopted tools keep their own licenses. Published
builds must not depend on the local clones existing in the source tree; the
runtime locates SkillBridge by configuration and reports a precise setup error
when it is missing.

## 4. Re-evaluation triggers

Re-open this audit only when:

- a concrete capability gap cannot be met by ADK, SkillBridge, or native APIs;
- a candidate fixes a security or Windows compatibility defect we cannot;
- the resource budget changes materially (for example, a RAM upgrade);
- a license or maintenance change affects an adopted tool.

Any future import must record the exact commit, files, modifications, license
text, and notice obligations before merge.
