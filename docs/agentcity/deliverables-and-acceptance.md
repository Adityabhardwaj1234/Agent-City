---
title: Deliverables and Acceptance
status: active
owner: integration
last_verified: 2026-10-23
---

# Deliverables and Acceptance

Status vocabulary: `implemented`, `partial`, `blocked`, `planned`. A capability
is never `implemented` without a test command, evidence, and honest UI state.
This table must match `PROJECT_MANIFEST.json`; `state-of-build.md` is generated
from it.

## 1. Foundation

| Deliverable | Status | Evidence / next step |
|---|---|---|
| Repository, license, notices | implemented | `LICENSE`, `NOTICE`, `THIRD_PARTY_NOTICES.md` |
| Project constitution | implemented | `AGENTS.md` |
| AI context pack | implemented | `docs/AI_CONTEXT.md`, manifest |
| Architecture and 16 diagrams | implemented | `docs/architecture/` |
| Engineering standards and recipes | implemented | `docs/engineering/` |
| Runbooks and templates | implemented | `docs/runbooks/`, `docs/templates/` |
| Documentation checker | implemented | `scripts/check-docs.py` |
| Context generator | implemented | `scripts/generate-context.py` |
| Pinned tool clones | implemented | `docs/agentcity/tooling-inventory.md` |
| Application source | planned | M1 |

## 2. Core runtime

| Deliverable | Status | Acceptance |
|---|---|---|
| Electron shell and preload bridge | planned | Window launches, health visible, IPC validated |
| Loopback sidecar with token | planned | Unauthorized requests rejected; handshake verified |
| SQLite migrations | planned | Fresh and upgrade migrations pass |
| Mission engine | planned | Full lifecycle with pause, cancel, retry, recovery |
| Event ledger and SSE | planned | Replay from cursor without duplicates or gaps |
| Approval broker | planned | Forged, stale, and replayed approvals rejected |
| Artifact store | planned | Provenance and path containment tested |
| Structured logs and redaction | planned | Secret scan of logs passes |

## 3. Agents and tools

| Deliverable | Status | Acceptance |
|---|---|---|
| ADK agent package | planned | Generated with the builder, committed, loads and runs |
| Offline planner | planned | Deterministic plan passes the same schema tests |
| Live Gemini mode | blocked | No key configured; adapter and blocked state to be built |
| SkillBridge MCP client | planned | Real read-only call against isolated home |
| Capability registry | planned | Risk classes and schemas visible in UI |
| MCP failure handling | planned | Timeout, crash, malformed, reconnect tested |
| Verifier gate | planned | Mission cannot complete without evidence |

## 4. Interface

| Deliverable | Status | Acceptance |
|---|---|---|
| City Overview | planned | Every metric tied to a persisted event |
| Command chat | planned | Streaming, cancel, citations, artifacts |
| Missions workspace | planned | Plan, DAG, logs, approvals, retry |
| Agent Teams | planned | Roster, scopes, templates, direct chat |
| Workspace | planned | Repo status, worktrees, diffs, tests |
| Desktop Vision | planned | Consent, indicator, stop, fresh observation |
| Research | planned | Citations with timestamps and provenance |
| Projects and Memory | planned | FTS retrieval and memory controls |
| Skills and Tools | planned | Real capability status and safe test |
| Artifacts | planned | Preview, reveal, export, provenance |
| Automations | planned | Schedules, budgets, approval per run |
| Settings and Diagnostics | planned | Self-test and redacted logs |

## 5. Desktop and voice

| Deliverable | Status | Acceptance |
|---|---|---|
| Screenshot capture | planned | Off by default; indicator; scoped grant |
| Windows UI Automation | planned | Falls back safely; elevation denied |
| Action verification | planned | Fresh observation and result check |
| Emergency stop | planned | Halts queue and in-flight action |
| Push-to-talk STT | planned | Editable transcript, device errors handled |
| Local TTS and barge-in | planned | Interruption works; no stale speech |
| Wake word | planned | Off by default, opt-in, visible |

## 6. Quality and release

| Deliverable | Status | Acceptance |
|---|---|---|
| Unit and contract tests | planned | CI and local pass with counts recorded |
| UI component tests | planned | States and accessibility covered |
| Playwright E2E | planned | Launch, mission, approval, cancel, restart |
| Security test suite | planned | All threat cases pass or block release |
| ADK evaluation dataset | planned | 14 scenarios with trajectories |
| Performance measurement | planned | Idle under 600 MB, active measured |
| Windows installer | planned | Clean-profile launch and migration |
| Release verification report | planned | Pass/fail/skip/blocked listed truthfully |

## 7. Definition of done (per capability)

- [ ] Behavior implemented and wired to real state.
- [ ] Authorization and policy checks.
- [ ] Loading, empty, error, disabled, and blocked UI states.
- [ ] Structured logs with redaction.
- [ ] Unit/integration/E2E tests as appropriate.
- [ ] Docs updated, including setup and limitations.
- [ ] Evidence recorded with a status.
- [ ] No dead controls or mock data in real mode.

## 8. Release gate

A release is blocked if any of these is true:

- a critical security test fails;
- a claimed feature has no evidence;
- the packaged app fails to launch on a clean profile;
- the docs contradict the implementation;
- live and offline results are mixed in a report;
- a dependency or license obligation is unresolved.
