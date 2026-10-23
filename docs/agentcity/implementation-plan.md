---
title: Implementation Plan
status: active
owner: integration
last_verified: 2026-10-23
---

# Implementation Plan

The plan is ordered by dependency, not ambition. Each milestone ends with a
demoable, tested slice and recorded evidence. No milestone is complete on
screenshots.

## M0 — Context, rules, and tool pins (complete)

Deliverables:

- Git repository, MIT license, NOTICE, third-party notices.
- `AGENTS.md`, `docs/AI_CONTEXT.md`, `docs/PROJECT_MANIFEST.json`.
- Architecture overview, 16 diagrams, contracts, data model, 7 ADRs.
- Engineering standards, change recipes, debugging playbook, runbooks,
  templates.
- Pinned clones of ADK Agent Builder and SkillBridge in `src/skills/`.
- Documentation checker and context generator.

Exit criteria:

- `python scripts/check-docs.py` passes.
- A fresh agent can answer “what is this, how do I run it, what works, what
  next” from `AI_CONTEXT.md` alone.
- Tool SHAs and commands are recorded with evidence.

## M1 — Vertical slice

Scope:

1. Electron main + preload + minimal React shell with health status.
2. Sidecar spawn with random token, handshake file, loopback bind.
3. SQLite migrations for missions, tasks, events, approvals, artifacts.
4. Mission Engine: create, plan (Offline Mode), approve, run a deterministic
   local tool, verify, complete; pause/cancel/retry.
5. SSE stream with replay from cursor.
6. Artifact write with provenance and path containment.
7. Restart recovery: interrupted detection, no replay of unsafe steps.

Exit criteria:

- No provider configured: app launches, explains Offline Mode, and completes one
  mission end to end.
- Approval rejection prevents the gated action and records why.
- Cancel stops an in-flight deterministic step and records the state.
- Restart after a simulated crash marks the run interrupted and allows safe
  resume.
- Tests pass for the happy path, rejection, cancellation, recovery, token auth,
  origin rejection, and path traversal.

## M2 — ADK agents and SkillBridge

Scope:

1. Generate the ADK agent package with the Agent Builder CLI; commit generated
   source, validation report, and eval report.
2. Wire the `agentcity_root`, planner, specialists, and verifier to the engine.
3. Live mode with Gemini; quota pacing and health checks.
4. SkillBridge stdio client: handshake, tool discovery, risk mapping, health.
5. Capability registry and safe test actions.
6. MCP failure tests: unavailable, timeout, malformed, reconnect, cancellation.

Exit criteria:

- Real read-only SkillBridge call succeeds against the local catalog with
  evidence.
- ADK agents load from committed definitions; offline and live paths are
  separately labeled.
- A failed worker surfaces as blocked/failed and cannot produce a successful
  parent mission.
- Live tests are quota-paced and recorded; blocked tests are named.

## M3 — Product interface

Scope:

1. Twelve workspace routes with real state and honest empty/error states.
2. City Overview: mission constellation, agent map, event timeline, approvals,
   health, budgets, artifacts.
3. Mission inspector with DAG, plan, logs, approvals, artifacts, retry.
4. Chat with streaming, cancel, citations, and artifact previews.
5. Agent roster and team template editor.
6. Artifacts, projects, skills/tools, automations, settings, diagnostics shells
   wired to real endpoints (automations can be disabled until M5).
7. Accessibility, keyboard navigation, reduced motion, responsive layout.

Exit criteria:

- Every visible control performs a real action or is clearly disabled with a
  reason.
- Reconnect recovers without duplicate or out-of-order events.
- No mock data in real mode; Demo Mode is visibly labeled.
- UI tests and Playwright E2E cover the primary journeys.

## M4 — Desktop and voice

Scope:

1. Permission grants with scope and duration; persistent capture indicator.
2. Screenshot capture, window inventory, UI Automation tree.
3. Action batches with policy checks, fresh observation, and verification.
4. Emergency stop hotkey independent of the model.
5. Push-to-talk capture, transcript editing, STT adapter, local TTS, barge-in.
6. Microphone permission and device error states.

Exit criteria:

- Tests run against Notepad or a controlled fixture only.
- Capture is off until consent and stops immediately on revoke.
- Stale observation and out-of-scope window are denied.
- Emergency stop halts queued and in-flight actions.
- Voice transcript alone cannot approve a consequential action.

## M5 — Knowledge, coding agents, routines, evaluation

Scope:

1. Project knowledge index with SQLite FTS and provenance.
2. Memory browser and retention controls.
3. Coding CLI adapters with worktree verification, diff capture, test evidence.
4. Routines with schedules, budgets, and per-run approvals.
5. Evaluation lab with trajectory, answer, safety, and cost cases.

Exit criteria:

- Retrieval answers can show supporting excerpts.
- A coding task reports the real worktree, branch, changed files, exit code, and
  test result.
- An automation with an external side effect cannot run without approval.
- Evaluation results appear in diagnostics and are labeled by mode.

## M6 — Hardening and packaging

Scope:

1. Security tests: injection, forged approvals, origin/CSRF, path escape,
   argument injection, budget overflow, stuck timeouts.
2. Dependency, license, and secret scans.
3. Performance profile against the budget.
4. Windows installer, clean-install smoke test, migration test, uninstall policy.
5. `docs/agentcity/release-verification.md` with real results.

Exit criteria:

- Critical tests pass; everything else is explicitly listed as failed, skipped,
  mocked, or blocked.
- Packaged app launches on a clean profile.
- README, runbooks, and acceptance matrix match reality.

## Dependencies

```text
M0 ──► M1 ──► M2 ──► M3 ──► M4
                    └─────► M5 ──► M6
```

M3 can begin once the M1 API contracts are stable. M4 depends on the policy
broker from M1 and the capability registry from M2. M5 depends on storage and
routing. M6 depends on all.

## Worktree and agent protocol

1. Preserve the current branch and working tree; inspect status first.
2. Create real worktrees for separable streams:
   `worktrees/agentcity-backend` → `feat/backend-core`,
   `worktrees/agentcity-ui` → `feat/desktop-ui`,
   `worktrees/agentcity-desktop-voice` → `feat/desktop-voice`,
   `worktrees/agentcity-qa` → `test/qa`.
3. Give each worker its path, branch, file ownership, contract version, task,
   acceptance criteria, and allowed write scope.
4. Verify isolation from inside each worker with `git rev-parse --show-toplevel`
   and `git branch --show-current`; record the output.
5. If worktrees are unavailable, use exclusive file ownership and serialized
   integration, and say so. Never claim isolation that did not happen.
6. One owner for `package.json`, lockfiles, migrations, and shared schemas.
7. The integrator reviews diffs, unexpected files, and secrets before merging.
8. Workers report files, commands, tests, deviations, risks, branch and SHA.

Default concurrency on this machine: **2 workers**, raised only after measuring
RAM and CPU.

## Session-end publication protocol

Every session ends with a verified push of the finalized, production-ready work
to the configured `origin` remote. The integrator owns this gate.

1. Run the nearest tests and `python scripts/check-docs.py`.
2. Confirm the working tree is clean and that no secrets, runtime data,
   databases, `.env` files, or `src/skills/**` clones are staged.
3. Commit the verified work with a Conventional Commit message.
4. Push `main` and verify the remote SHA:

   ```powershell
   git push origin main
   git fetch origin
   git rev-parse main
   git rev-parse origin/main
   ```

5. Record the branch, local SHA, remote SHA, checks run, and push result in the
   session handoff or evidence when the session makes a release or acceptance
   claim.

The push is not optional for finished work. If it fails, report the exact
command and error, leave the verified commit local, and mark the session
**blocked on publication**. Never force-push, never publish failing or
secret-bearing work, and never describe an unpushed session as delivered.

## Development roster

| Role | Owns | Does not own |
|---|---|---|
| Lead integrator | Contracts, merges, acceptance, final evidence | Worker internals |
| Backend/ADK | `src/backend`, migrations, engine, adapters | UI components, lockfiles |
| Desktop UI | `src/desktop/src`, design system, UI tests | Backend schemas, manifests |
| Desktop/voice | Desktop and voice adapters, isolated tests | Hidden capture, policy bypass |
| QA/security | Tests, fixtures, threat cases, eval data | Feature code without handoff |
| Docs/release | Packaging, runbooks, release report | Uncoordinated shared config |

The agents AgentCity runs at runtime are a separate roster; see
`agent-roster.md`.

## Model routing record

See `model-routing.md`. The short version: Gemini through ADK is the default;
Offline Mode is always available; coding agents use their own provider auth;
no key is assumed and no subscription is treated as API access.
