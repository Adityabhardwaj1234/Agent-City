---
title: Architecture Overview
status: active
owner: architecture
last_verified: 2026-10-23
---

# Architecture Overview

AgentCity is a privileged local application. The architecture is organized
around one rule: **durable truth lives in deterministic code, intelligence lives
in agents, and the UI only projects persisted state.**

Diagrams for every view in this document live in
[`diagrams.md`](diagrams.md). Wire-level contracts live in
[`contracts.md`](contracts.md). Tables and retention live in
[`data-model.md`](data-model.md).

## 1. System context

AgentCity runs on the user's Windows PC and connects outward only when the user
has configured a provider or explicitly enabled an integration.

- **User** — speaks, types, points at a screen, approves or rejects actions.
- **AgentCity** — desktop shell, local runtime, agent teams, mission state.
- **Model providers** — Gemini by default through ADK; optional compatible
  providers only when configured.
- **SkillBridge** — local skill catalog and MCP broker.
- **Other MCP servers** — optionally registered, each risk-classified.
- **Coding CLIs** — OpenCode, Claude Code, Codex, Gemini CLI when installed and
  authorized; never installed silently.
- **Operating system** — screen, microphone, UI Automation, files, processes.

## 2. Containers

| Container | Responsibility | Trust level |
|---|---|---|
| Electron main | Window lifecycle, sidecar spawn, hotkeys, IPC validation | Trusted host code |
| Preload bridge | Narrow typed API exposed to the renderer | Trusted, minimal |
| React renderer | Presentation and user intent | Untrusted web content rules |
| FastAPI sidecar | Auth, API, SSE, orchestration entry | Trusted local service |
| Mission Engine | DAG, budgets, approvals, retries, recovery | Trusted deterministic core |
| ADK runtime | Agent reasoning and tool selection | Untrusted model output |
| Policy broker | Grants or denies every tool/action | Trusted deterministic core |
| MCP client | SkillBridge and other MCP servers over stdio | Untrusted tool output |
| Desktop service | Capture and UI Automation behind permission | Privileged, gated |
| SQLite + artifacts | Durable state, events, provenance | Local source of truth |

### Why Electron

Rust/cargo is not installed, the machine has 7.8 GB RAM, and the required
desktop/voice/automation libraries are mature on Electron. Electron also gives a
single Chromium version for predictable UI and accessibility behavior. Tauri was
rejected for this environment; see ADR-0003.

### Why a deterministic mission engine

ADK workflows are excellent at reasoning and composition inside a run, but they
are not a durable scheduler for a UI that must survive crashes, approvals that
wait minutes, and cancellation from a button. The engine persists the plan,
executes each ADK step, records evidence, and enforces limits. ADK remains the
only reasoning framework; we are not adding a competing orchestrator. See
ADR-0002.

## 3. Process and boundary model

```text
Electron main (Node)
  ├─ spawns: python -m agentcity.api --port 0 --token-file <handshake>
  ├─ owns: window, tray, global stop hotkey, updater
  └─ IPC: typed channels only, schema validated in main and preload

FastAPI sidecar (Python)
  ├─ binds 127.0.0.1:<ephemeral>
  ├─ requires Authorization: Bearer <per-launch-token>
  ├─ validates Origin and Content-Type
  ├─ hosts: Mission Engine, ADK runner, policy, MCP client, desktop, voice
  └─ writes: SQLite WAL, artifacts, structured logs
```

The renderer never receives the sidecar token directly from disk. Electron main
reads the handshake file and hands the renderer a scoped client configuration
through preload. The token is rotated on every launch and invalid after exit.

## 4. Mission lifecycle

```text
draft → planned → waiting_for_approval → queued → running → verifying
      → completed | failed | cancelled | blocked
```

Rules:

- The plan is persisted **before** any side effect.
- Approval requests are persisted with an expiry and a single-use token.
- A retry creates a new `agent_run` with a reason; it never rewrites history.
- `interrupted` is recorded on startup for runs that were `running` when the
  process died. Only idempotent steps resume automatically.
- Completion requires a verifier decision whose evidence references artifacts.
- Cancellation is cooperative but bounded: every adapter observes a cancel event
  and enforces a hard timeout.

## 5. Event model

Every state change appends an immutable row to `events` inside the same
transaction as the state change. The UI consumes SSE from a sequence cursor and
can replay from zero after reconnect. Event payloads are schema-versioned.

Minimum event families: mission, task, agent, tool, approval, artifact, budget,
provider, verification, system. The full type list and payload rules are in
[`contracts.md`](contracts.md).

## 6. Agent design

| Agent | Responsibility | Side effects |
|---|---|---|
| `agentcity_root` | Intent intake, mode selection, typed plan | None directly |
| `planner` | Decompose, dependencies, risk, budget, acceptance | None |
| `researcher` | Source-grounded retrieval with citations | Read-only tools |
| `architect` | Design and repo fit | Read-only tools |
| `coder` | Scoped changes in an assigned worktree | Gated writes |
| `debugger` | Reproduction and root cause | Read-only + gated commands |
| `test_engineer` | Tests and test evidence | Gated writes/commands |
| `reviewer` | Independent diff and risk review | None |
| `security_guard` | Injection, secrets, egress, permission review | None |
| `desktop_operator` | Governed screen/UI actions | Via desktop service only |
| `verifier` | Acceptance evidence and completion decision | Reads artifacts |

Agents receive a task contract: objective, context references, input schema,
output schema, allowed tools, file scope, budget, timeout, and completion
evidence. A child cannot widen its own scope. Parallelism is allowed only for
tasks with disjoint inputs and ownership; the default worker cap is 2.

## 7. Tool and permission architecture

Every capability is registered with:

- stable id, display name, source (local, SkillBridge, MCP, coding CLI);
- JSON schema for input and output;
- risk class: `read_only`, `reversible_local`, `state_change`, `consequential`,
  `blocked`;
- required approval policy and scope constraints;
- timeout, output size cap, and cancellation behavior.

The policy broker evaluates the request against the mission policy, the
workspace roots, the user's approvals, and the current screen state. It returns
an allow/deny decision with a reason code. The model never evaluates its own
permission.

SkillBridge's 19 broker tools map to risk classes as follows: search, preview,
status, memory, and audit are `read_only`; import/load/unload mutate local
staging and are `state_change`; `run_skill_script`, `enable_mcp_server`, and
`call_mcp_tool` are `consequential` and always require an explicit per-action
approval in the first release.

## 8. Desktop control

1. The user grants screen permission for a scope and duration.
2. The agent requests an observation; the desktop service captures a fresh
   frame and records timestamp, window, and monitor.
3. The policy broker checks the target window against the allowlist.
4. UI Automation is preferred. Vision and mouse/keyboard are fallbacks.
5. After an action batch, a fresh observation is mandatory before the next
   batch; stale coordinates are rejected.
6. The emergency stop hotkey cancels the queue and the in-flight action without
   waiting for the model.

## 9. Voice

Push-to-talk is the default. Audio is captured in the renderer, streamed to the
sidecar, transcribed by the configured provider, shown as editable text, and
only then submitted. TTS runs locally through Windows SAPI by default. A spoken
transcript never constitutes approval for a consequential action. Wake word is
an opt-in feature with a persistent indicator.

## 10. Storage

- `%LOCALAPPDATA%\AgentCity\agentcity.db` — SQLite in WAL mode.
- `%LOCALAPPDATA%\AgentCity\artifacts\<mission-id>\` — outputs.
- `%LOCALAPPDATA%\AgentCity\logs\` — structured logs with retention.
- `%LOCALAPPDATA%\AgentCity\handshake.json` — port and token file, ACL-restricted,
  deleted on clean exit.

The repository is never used as runtime storage. Tests use a temp home and a
throwaway SQLite database.

## 11. Failure and recovery

| Failure | Behavior |
|---|---|
| Sidecar fails to start | Shell shows actionable error + log path; no blank window |
| Provider missing or invalid | Missions can plan in Offline Mode; live steps blocked with setup link |
| Provider 429 | Exponential backoff with jitter, budget-aware; no silent retry storm |
| Tool timeout | Cancel, record failure, mark task blocked, offer retry |
| MCP server crash | Restart once, then mark capability unavailable |
| App crash mid-run | Mark run interrupted; resume only idempotent steps |
| Policy evaluation error | Deny and report the blocker (fail closed) |
| Disk full | Stop artifact writes, keep state consistent, surface error |

## 12. Packaging topology

Development runs the Electron shell and the Python sidecar from the working
tree. The packaged build ships the renderer, Electron main, and a Python runtime
or a frozen sidecar, with a signed installer. Packaging details and the clean
installation test are defined in `docs/runbooks/packaging.md`.

## 13. Deliberate non-goals

No Docker, Kubernetes, PostgreSQL, Redis, or local model server is required to
launch. No hidden screen or microphone capture. No unbounded autonomous
computer use. No automatic commit, push, purchase, or message without the
configured approval policy.
