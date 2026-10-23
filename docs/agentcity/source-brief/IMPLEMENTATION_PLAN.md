# AgentCity — Implementation and Agent Orchestration Plan

## Phase 0 — discover, preserve, and select a foundation

1. Confirm current working directory/repository, current branch, working tree, untracked files, local changes, remotes, README/AGENTS files, package manager, language versions, and test state.
2. Never discard or reformat unrelated user work. Do not reset/clean/force-push or overwrite secrets.
3. Inspect the exact installed custom tools and MCP registrations. Find the user's ADK Agent Builder and Skills Bridge by metadata/schema. Record the exact identifiers, invocation shapes, permissions, and returned artifacts in `docs/agentcity/tooling-inventory.md`.
4. Read relevant repository-specific instructions including `AGENTS.md`, license/NOTICE, security guidance, and relevant docs before changing code.
5. Build a reuse table: capability, candidate code/repo, version/commit, license, last activity, dependency burden, OS status, threat concerns, fit, and decision.
6. If no suitable local project exists, evaluate Personal Jarvis as the first foundation candidate; evaluate OpenDex if a smaller voice-first desktop shell is a better fit. Assess Mission Control for dashboard concepts/components, OpenHands for coding-agent infrastructure, OpenComputer for desktop control. Do not add every project as a dependency.
7. Run the base project's baseline tests/build before modifications where possible; capture pre-existing failures separately.
8. Write the Product Requirements, Architecture, Implementation Plan, Deliverables/Acceptance Checklist, Agent Roster and Model-Routing Record, and Test Plan before feature implementation.
9. Choose MIT for newly authored AgentCity code unless the selected base/license strategy demands another compatible license. Keep original third-party license and notice obligations; do not overwrite upstream notices or mislabel all imported code as newly authored.

## Phase 1 — integration spike and architecture proof

Implement the smallest end-to-end slice:
- launch desktop shell;
- open local gateway and SQLite;
- list ADK/Skills Bridge integration status;
- submit a mission through the UI;
- ADK returns a typed plan;
- UI streams persisted events;
- user approves a harmless tool invocation;
- agent executes a deterministic mocked task;
- verifier checks output and saves an artifact;
- cancellation and restart recovery tests pass.

Do not parallelize beyond this until the main data/event/permission contracts are stable.

## Phase 2 — core platform

- Secure desktop-to-backend connection and diagnostics.
- Database migrations and typed API contracts.
- ADK root agent, role-specific agents, mission engine, model adapter, Skills Bridge adapter, MCP integration, and event persistence.
- Risk classification and approval queue.
- Artifact store and local conversation/project state.
- Run cancellation, timeout, retry, and restart recovery.

## Phase 3 — interface and operational dashboard

- City Overview with real persisted state.
- Navigation, chat, missions, agents/teams, workspaces, integrations, artifacts, settings, logs/diagnostics.
- Streaming event updates, reconnection, accessibility, and responsive behavior.
- Design must work with zero configured providers and display setup tasks honestly.

## Phase 4 — desktop use and voice

- Explicit permissions and visible screen-capture indicator.
- Native UI Automation first, controlled screenshot fallback, action verification, emergency stop.
- Push-to-talk and streaming voice round trip.
- Optional wake word only behind explicit opt-in and local/visible status.
- Tests use a sandbox app/window or mocks; never perform destructive tests on the user's real desktop.

## Phase 5 — projects, retrieval, coding agents, routines

- Project knowledge index with source provenance.
- Coding agent adapters, real worktree paths, diff/test capture, and handoff.
- Team templates and bounded parallel missions.
- Routines/automation with disabled-by-default external side effects.
- Model routing policy and budget/usage telemetry.

## Phase 6 — hardening and packaging

- Security, dependency, secret scanning, and license scans.
- ADK evaluation datasets and regression gates.
- Playwright and platform-specific smoke tests.
- Clean-install packaging, upgrade path, database migration test, uninstall data-retention behavior, and update verification.
- Accessibility pass, performance/memory profile, crash recovery, and installer validation.

## Development-time subagent/team plan

These are coding agents used to build AgentCity; they are distinct from the agents AgentCity will create at runtime.

### Lead: Principal orchestrator / integrator
Owns requirements, architecture, schemas, merges, acceptance criteria, scope and final verification. Calls the existing ADK Agent Builder and Skills Bridge tools where available and records exact invocations. Does not delegate final acceptance judgment blindly.

### Worker 1: Repository and reuse auditor
Owns `docs/agentcity/reuse-audit.md` and provenance/license review. It inspects candidate repos and base architecture; it does not modify runtime code unless explicitly reassigned.

### Worker 2: Backend and ADK
Owns `backend/agentcity/` and backend tests. Implements mission API, ADK workflows/agents, provider and MCP/Skills Bridge adapters, budgets, approvals, event persistence, and recovery. It does not edit UI components or package lock files.

### Worker 3: Desktop UI and design system
Owns `desktop/src/` or the equivalent frontend source directory and UI tests. Implements navigation, city map, chat, mission/task graph, agents, approvals, artifacts, diagnostics, accessibility, and error/empty states. It does not edit backend schemas or package manifests except through integrator-approved changes.

### Worker 4: Desktop control and voice
Owns the dedicated desktop-control and voice adapter folders plus isolated tests. Implements permission broker, capture/control driver, visible indicators, TTS/STT integration, interrupt, and emergency stop. It may not create a hidden microphone/screen service or bypass approval policy.

### Worker 5: QA, security, and evaluation
Owns `tests/`, eval fixtures, threat cases, and test documentation. Runs baseline and feature tests; writes reproduction cases. Can recommend changes but should not fix code owned by other workers without handoff.

### Worker 6: Integration/release documentation (optional, only if concurrency helps)
Owns docs, packaging scripts, migration/runbooks, and release smoke-test report. No uncoordinated changes to shared config files.

Use fewer agents if the codebase is small. Spawning an agent is not a goal; measurable parallel progress is.

## Worktree protocol (mandatory when coding-agent environment supports it)

1. Preserve the original branch and working tree. Create a dedicated integration branch only after checking the current state.
2. Create real Git worktrees with unique branches for separable work, for example:
   - `worktrees/agentcity-backend` → `feat/agentcity-backend`
   - `worktrees/agentcity-ui` → `feat/agentcity-ui`
   - `worktrees/agentcity-desktop-voice` → `feat/agentcity-desktop-voice`
   - `worktrees/agentcity-qa` → `test/agentcity-qa`
3. Give each agent its exact worktree path, branch, file ownership, contract/version, task, acceptance checklist, and allowed write scope.
4. Verify from each worker environment that its `git rev-parse --show-toplevel` and `git branch --show-current` point to the assigned worktree/branch. Record evidence. Do not merely tell multiple agents to use worktrees while leaving them in the same directory.
5. If the coding environment does not support real parallel worktrees, say so explicitly and enforce exclusive, non-overlapping file ownership plus serialized integration. Never claim isolation that did not occur.
6. Only the integrator merges branches after tests, diff review, no unexpected generated files/secrets, and acceptance checks. Preserve original changes and use normal merge commits or reviewed cherry-picks; no force-push.
7. Do not have several agents independently change `package.json`, lockfiles, database migrations, or shared API schemas. Assign one owner; other workers submit change requests.
8. Keep agent prompts small, concrete, and testable. Pass only relevant docs/context. Each agent must report files changed, commands run, tests/result, known issues, and commit SHA/branch.

## Model-routing record

Create `docs/agentcity/model-routing.md` with:
- agent/task role;
- selected model and provider;
- reason (capability, code quality, latency, budget, policy);
- fallback model/provider;
- context/usage limits;
- known limitations;
- actual reported usage or explicitly labeled estimates.

Use the user's configured credentials/providers only. Never assume API access from a product subscription, and never store keys in prompts or Git. Default local computer-control and QA code paths to mocked deterministic tests. Keep parallel worker count low by default (2–3) on a 16 GB RAM desktop; raise only after measuring workload.

## Definition of done for each phase

No phase is complete on screenshots alone. Produce source code, tests, run instructions, test output, documented limitations, security review notes, and a phase acceptance report. Features that need external credentials must have a real integration path plus a clear unconfigured state; do not mark credential-dependent E2E tests passed without the credentials.
