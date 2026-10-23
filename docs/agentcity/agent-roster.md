---
title: Agent Roster
status: active
owner: architecture
last_verified: 2026-10-23
---

# Agent Roster

Two rosters exist and must not be confused:

- **Runtime agents** — the ADK agents AgentCity assembles for the user.
- **Development workers** — coding agents that build AgentCity.

## 1. Runtime agents

All runtime agents are defined in code, versioned, and validated with the ADK
Agent Builder before commit. Every agent has typed input/output contracts, an
explicit tool allowlist, a timeout, and a failure mode. Sub-agents used inside a
workflow run with `mode="single_turn"` and `include_contents="default"` unless a
documented reason requires otherwise.

| Agent | Purpose | Tools | Output | Risk |
|---|---|---|---|---|
| `agentcity_root` | Intent intake, mode selection, routing to a plan | None directly | `MissionPlan` or clarification | read-only |
| `planner` | Decompose objective, dependencies, risk, budget, acceptance | None | `MissionPlan.tasks[]` | read-only |
| `researcher` | Source-grounded retrieval with citations | web/file read, SkillBridge search | `ResearchFindings` | read-only |
| `architect` | Design, repo fit, interface contracts | repo read, docs | `ArchitectureProposal` | read-only |
| `coder` | Implement changes in an assigned worktree | file write, test runner, coding CLI | `ChangeSet` | state change |
| `debugger` | Reproduce and isolate failures | repo read, test runner, logs | `RootCauseReport` | read-only |
| `test_engineer` | Add and run tests, capture evidence | file write, test runner | `TestReport` | state change |
| `reviewer` | Independent diff and risk review | repo read, diff | `ReviewDecision` | read-only |
| `security_guard` | Injection, secrets, egress, permissions | policy read, scan | `SecurityVerdict` | read-only |
| `desktop_operator` | Governed screen observation and action | desktop service only | `DesktopActionReport` | consequential |
| `verifier` | Acceptance evidence and completion decision | artifact read, test results | `VerificationResult` | read-only |

### Delegation contract

Every delegated task includes:

```json
{
  "task_id": "tsk_...",
  "objective": "string",
  "context_refs": ["artifact:art_...", "file:..."],
  "input_schema": "schema-id",
  "output_schema": "schema-id",
  "allowed_tools": ["capability-id"],
  "file_scope": ["src/backend/..."],
  "budget": { "max_tool_calls": 20, "max_tokens": 40000, "timeout_seconds": 300 },
  "acceptance_criteria": ["string"],
  "evidence_required": ["test_report", "diff"]
}
```

Rules:

- A child receives only the context it needs; no blanket conversation history.
- A child cannot widen its tool list, file scope, or budget.
- Maximum delegation depth is 2 and maximum concurrent children is 2 by default.
- The parent inspects the result and may reject it; rejection is an event.
- The verifier is independent from the coder and reviewer.

### Verification gate

A mission can be marked `completed` only when:

1. Every required task is `completed` with an output matching its schema.
2. The verifier returns `passed` with references to concrete artifacts.
3. All approvals required by policy are recorded.
4. The budget was not exceeded.
5. No open `security_guard` block remains.

## 2. Development workers

See `implementation-plan.md` § Development roster. Summary:

| Role | Owns | Concurrency |
|---|---|---|
| Lead integrator | Contracts, merges, acceptance, evidence | 1 |
| Backend/ADK | `src/backend`, engine, adapters, migrations | 1 |
| Desktop UI | `src/desktop/src`, design system, UI tests | 1 |
| Desktop/voice | desktop and voice adapters | 1 (after M2) |
| QA/security | tests, fixtures, threat cases, evals | 1 |
| Docs/release | packaging, runbooks, release report | on demand |

Default simultaneous workers: **2** on this machine. The integrator is always
one of them. Shared files have a single owner: `package.json`, lockfiles,
migrations, API contracts, and this roster.

## 3. Agent definition standards

- Instructions are specific, short, and testable; no contradictory rules.
- Tool descriptions state side effects and risk class.
- Outputs are Pydantic models, not free-form prose where code consumes them.
- Failure paths are explicit: retry, ask for clarification, or block.
- Every prompt treats retrieved content as data, not instructions.
- Agent evaluation datasets include trajectory checks, not only final answers.

## 4. Model policy per role

| Role | Default | Fallback | Notes |
|---|---|---|---|
| Planner, reviewer, verifier | Gemini 2.5 Pro | Gemini 2.5 Flash | Quality matters; low volume |
| Coder, debugger, test engineer | Gemini 2.5 Pro | Gemini 2.5 Flash | Prefer coding strength; budget-capped |
| Researcher, summarizer | Gemini 2.5 Flash | Pro | High volume, lower cost |
| Desktop operator | Gemini 2.5 Flash | Pro | Short observations; strict schema |
| Security guard | Gemini 2.5 Pro | Flash | Conservative; fail closed |

No provider is assumed. See `model-routing.md` for availability, quota, and the
live/offline split.
