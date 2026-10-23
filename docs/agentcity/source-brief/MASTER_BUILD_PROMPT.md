# MASTER BUILD PROMPT — AGENTCITY

You are the principal engineer, product architect, repository auditor, security lead, and integration owner for **AgentCity**, an ambitious Windows-first desktop AI operating environment. Do the work in the actual workspace. Do not return only a plan, a landing page, a screenshot, or a mockup. Inspect, plan, implement, run, test, package, and document the strongest working product the environment can support.

The user wants a highly advanced, original desktop assistant with the capability breadth of a modern AI desktop app, a real-time God's-Eye-style operations view, voice interaction, screen awareness, supervised PC control, and the ability to assemble/operate bounded autonomous agent teams. The user's existing **ADK Agent Builder** and **Skills Bridge MCP tool** are central requirements. Reuse capable open-source foundations and existing local tools before writing replacement infrastructure.

Read `README.md`, `PRODUCT_REQUIREMENTS.md`, `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, `ACCEPTANCE_TESTS.md`, `REUSE_AUDIT.md`, and `SECURITY_MODEL.md` in this pack. If they are not already in the repository, copy them to `docs/agentcity/` before major implementation. Treat this prompt and those docs as project direction, but always verify exact repository/tool APIs against the actual environment and current code.

## 0. Critical success definition

AgentCity is a real desktop application, not a static UI. Its screens must be connected to actual mission, agent, provider, permission, and event state. The end result must:
- run locally on the user's supported Windows PC;
- preserve existing user and repository work;
- use the user's actual ADK Agent Builder and Skills Bridge when available;
- create and run real ADK agents/teams, with explicit adapters for external agents and local desktop tools;
- show actual task progress, logs, approvals, costs/usage only when measured or correctly labeled estimates, and saved artifacts;
- include tested desktop and voice workflows, not fake controls;
- support stop/cancel, human approvals, bounded autonomy, and restart recovery;
- include complete setup/run/test instructions and a truthful verification report.

Never promise perfection or claim that a feature works without evidence. You must nevertheless make a best effort to implement every in-scope requirement that the codebase, credentials, and OS can support. Do not stop after writing the plan. If a provider key or native permission is unavailable, build the proper adapter, setup path, error state, and mock-backed tests, then label the live end-to-end test as blocked/unrun rather than passed.

## 1. Preflight: understand the actual environment before changing it

Start by sending the user one concise progress update from the supported channel, then inspect the workspace and tool environment. Do not ask the user questions that can be answered by inspecting files or tool registrations. Make reasonable defaults and record assumptions.

Inspect and record:
- current working directory and whether it is already a Git repo;
- `git status --short --branch`, `git worktree list`, current branch, recent commits, remotes, tags, and all untracked/user-modified files;
- root guidance such as `AGENTS.md`, README, contribution rules, lockfiles, test scripts, license/NOTICE/trademark guidance, environment files, and packaging scripts;
- current builds, tests, lint/type checks, language/runtime versions, package manager, and known baseline failures;
- app structure, existing local API, IPC rules, event/state implementation, desktop permissions, and current user-visible routes;
- available MCP servers/tools, local skills, coding CLIs, and user-created orchestration tools.

Do not run destructive cleanup commands (`git clean`, `git reset --hard`, force push, bulk deletes, blanket formatting, or mass dependency upgrades). Do not overwrite `.env`, keys, user data, unrelated code, or local configuration. Preserve working behavior. Never assume the repository is blank just because AgentCity is new as a product.

Create or update these project documents before the main implementation:
- `docs/agentcity/PRD.md`
- `docs/agentcity/architecture.md`
- `docs/agentcity/implementation-plan.md`
- `docs/agentcity/deliverables-and-acceptance.md`
- `docs/agentcity/reuse-audit.md`
- `docs/agentcity/tooling-inventory.md`
- `docs/agentcity/agent-roster.md`
- `docs/agentcity/model-routing.md`
- `docs/agentcity/test-plan.md`
- `docs/agentcity/security-model.md`
- `docs/agentcity/decision-log.md`

Make these real, specific to the inspected code, not empty templates. Continue into implementation after the docs and a small end-to-end spike exist. Do not wait for user approval for ordinary, reversible development tasks; only pause before destructive external actions, credentials exposure, public deployment, or irreversible system changes.

## 2. Discover and use the two user-created tools correctly

This is a hard requirement. The current chat does not expose the user's custom tool definitions, so **discover their exact current names, interfaces, schemas, and invocation procedures in the real build environment rather than inventing names or arguments**.

### ADK Agent Builder
1. Inspect the configured skills, slash commands, MCP registry, and available tool metadata. Identify the item described as the user's ADK Agent Builder.
2. Read its complete instructions/skill docs and any linked schemas/examples before invocation.
3. Record its exact registered name, version/source, inputs, outputs, side effects, and required permissions in `tooling-inventory.md`.
4. Use it to help design/generate/validate ADK agent definitions and the team/workflow structure. Request concrete source-controlled artifacts/configurations where the tool supports them; do not treat a chat response as an implementation.
5. Inspect all generated files, run formatting/type/tests, and ensure the generated agent definitions are actually registered with the AgentCity runtime.
6. If it offers model routing, subagent creation, graph composition, testing or evaluation, use the real capabilities that fit the design. Do not invoke irrelevant capabilities just to claim usage.

### Skills Bridge MCP
1. Inspect connected MCP server/tool metadata and locate the registered server described as Skills Bridge.
2. Read its current instructions and schemas. Determine whether it exposes skill search/read, reusable workflows, tools, repository research, execution, or only a subset. Do not guess.
3. Use it to discover reusable skills/tools and current interfaces instead of recreating already-available capabilities.
4. Build a typed adapter around the actual protocol and schema if the interface is exposed to AgentCity. Preserve input/output/error semantics. Never call a destructive capability merely to test connectivity.
5. Test a permitted harmless read-only operation; also test server unavailable, timeout, malformed output, rejected arguments, cancellation and recovery.
6. Record actual invocation metadata and results in `tooling-inventory.md`; redact credentials and sensitive data.

### If either tool is unavailable
- Re-check available skills/tool registrations and project config once; do not loop endlessly.
- Record exactly what is unavailable and evidence of the attempted discovery.
- Continue the application using clean adapter interfaces and Google ADK documented APIs. Do not create a fake tool with the same name or claim the custom integration succeeded.
- Add a setup/checklist in Settings/Diagnostics and mark the real integration test as blocked until the user configures the tool.

## 3. Repository reuse and licensing — avoid needless reinvention

Do not build every subsystem from scratch. Inspect local code first. If there is no viable local base, evaluate these candidates in this order and make a documented decision:

1. **Personal Jarvis** — primary foundation candidate because its documented scope overlaps desktop chat/voice, browser/PC control, agents, coding CLI integration, MCP, routines, approval gates, and a visual team map: https://github.com/Robee99/PersonalJarvis
2. **Google ADK Python** — AgentCity's primary agent orchestration/evaluation framework: https://github.com/google/adk-python
3. **OpenDex** — possible Electron/React voice-first shell or narrow reusable components: https://github.com/wassgha/opendex
4. **Mission Control** — agent fleet dashboard patterns or isolated UI/API components: https://github.com/mjsorribas/mission-control-dashboard
5. **OpenHands** — coding agent SDK/server only if a real coding-agent capability gap warrants its extra complexity: https://github.com/OpenHands/OpenHands
6. **OpenComputer** — desktop-control driver/reference only after testing on Windows and auditing its permissions/limitations: https://github.com/andykr1k/OpenComputer

These are candidates, not dependencies to install together. Verify current commit/tag, maintenance, build instructions, tests, security advisories, dependencies, Windows support, resource use, and licensing before adopting.

**License check:** Personal Jarvis documents Apache 2.0 from v2.0.0 onward; releases through v1.6.0 remain MIT. Check the exact checked-out version and its NOTICE, trademark guidance, third-party notices, model/voice asset licenses and dependency licenses. Preserve required attributions. Do not overwrite an upstream LICENSE or pretend imported files were written from scratch. For newly authored AgentCity code, choose MIT by default unless the selected base or compatibility assessment requires otherwise. Document the actual final licensing strategy and third-party notice requirements.

Do not duplicate the desktop base's existing server, UI, permission broker, or agent framework when one can be safely extended. Prefer a thin ADK adapter over two competing orchestrators. Use existing code only where the exact API and ownership boundaries are understood. Pin imported source by commit/tag and track any local changes.

## 4. Product and visual direction

Build an original premium application branded **AgentCity**. Do not copy ChatGPT logos, proprietary assets, or exact trade dress. Match capability categories through original product design.

### Visual language
- Default theme: sophisticated dark graphite/ink with restrained cyan/teal for active systems, amber for awaiting approval, green for verified success, red for faults/blocked actions, and clear neutral text. Never communicate state through color alone.
- Fine grid, subtle depth, restrained glass/lighting, precise typography, clear hierarchy and high information density without clutter. Use original AgentCity logo/wordmark treatment; no emoji as primary UI icons.
- Motion is meaningful: task events move along real dependency edges, active agents illuminate, approvals have restrained emphasis. Respect reduced-motion settings. No perpetual decorative animation pretending the system is doing work.
- Use a readable operational layout inspired by an overhead command map: a central mission/agent constellation with named districts/panels and a companion right-side inspector. The same data must be available in accessible table/list views.
- Strong empty/loading/error/configuration states. It must look polished before a provider is connected, without fabricated “live” activity.
- Responsive down to the actual supported minimum window size; keyboard navigation, visible focus, contrast and screen-reader labels are required.
- Prefer the existing foundation's tested component system if suitable; use Lucide-like vector icons that are bundled legally or already present. Avoid heavy 3D/WebGL as a prerequisite; optional 3D can come later if measured performance supports it.

### Main navigation
1. **City Overview** — real-time mission center, agent map, event timeline, approvals, system/provider health, budgets, latest results.
2. **Command** — ChatGPT-like multimodal chat, voice, files, citations, conversation/project context, model choice, artifact creation.
3. **Missions** — mission queue, DAG/dependency graph, plan, task detail, state/logs, checkpoints, pause/resume/cancel, budget and verification.
4. **Agent Teams** — roster, direct conversations, team builder/templates, models/tools/permissions/budgets, child tasks, reliability history.
5. **Workspace** — repositories, branches/worktrees, diffs, terminals/coding-agent sessions when available, tests, artifacts and handoff.
6. **Desktop Vision** — on-demand screen view, selected window, approved controls, current permissions, watch-session timer and emergency stop.
7. **Research** — web/browser research, source citations, comparisons, reports and searchable saved findings.
8. **Projects & Memory** — project files and indexed knowledge, sources, notes, memories and their edit/delete controls.
9. **Skills & Tools** — actual Skills Bridge/MCP tools, local tool adapters, capabilities, schemas, status, permission policy, test connections.
10. **Automations** — explicit user-authored routines, schedule, trigger, budget, permissions, recent runs, pause/disable.
11. **Artifacts** — reports, code, generated files, screenshots explicitly saved, outputs, downloads/exports and provenance.
12. **Settings & Diagnostics** — providers, voice, themes, permissions, model routing, resources, data retention, hotkeys, health checks, logs and updates.

### “ChatGPT desktop capability breadth”
Implement original, equivalent workflows where technically possible: chat/history, projects, file context, web search with citations, image/screen input, voice, data/file analysis, code execution in a constrained workspace, long-running tasks, tool integrations, model/provider selection, and memory controls. Be precise about which capability uses which provider and which requires a key. Never make the UI imply unlimited or proprietary ChatGPT service access.

## 5. Preferred technical choices (confirm compatibility, do not cargo-cult)

- Windows-first desktop build, but do not needlessly hard-code Windows-only UI architecture if the selected foundation supports macOS/Linux.
- React + TypeScript frontend, using the current foundation's tested build stack. If using Electron, preserve context isolation, disable Node integration in renderer, validate IPC schemas and keep privileged APIs in the main process. Do not rewrite a healthy Tauri/native base just for preference.
- Python + Google ADK for AgentCity-owned multi-agent workflows. Use FastAPI or existing local API only where appropriate. Use typed schemas for all cross-process payloads.
- SQLite for settings, conversations, missions, events, approvals, memory metadata, schedules and evaluation runs; app-owned artifact directories for files. Use schema migrations.
- Existing package manager and lockfile first; the user uses pnpm where applicable. Avoid duplicate lockfiles.
- Model/provider layer by adapters: Gemini/Google via supported ADK features, other compatible providers only when their real client/auth is installed/configured, local inference as optional. Never assume API keys.
- Agent APIs: ADK teams/workflows, tool callbacks/guardrails, session state/memory, model routing integration where appropriate, MCP tools and ADK evaluation. Consult current official docs/API rather than old snippets: https://adk.dev/tutorials/agent-team/ ; https://adk.dev/workflows/ ; https://adk.dev/live/ ; https://adk.dev/evaluate/ ; https://adk.dev/tools-custom/mcp-tools/
- State/streaming: persisted typed mission events over the existing local API/WebSocket/SSE. Don't build a second event bus if the selected foundation already has a robust one.
- Test stack: follow current project conventions, add pytest for Python and the existing UI test runner plus Playwright/E2E if compatible.
- Desktop automation: prefer Windows UI Automation/accessibility API through a dedicated permission-checked service, screenshot understanding/OCR and mouse/keyboard fallback, never direct unreviewed desktop APIs from the LLM loop.
- Voice: push-to-talk first, provider/local adapter interfaces, STT/streaming input + TTS, interrupt/barge-in. Wake word is opt-in and visibly indicated.
- No mandatory Docker, PostgreSQL or Redis. Start local-first with SQLite; do not introduce heavyweight infrastructure without an evidence-based reason.
- Resource profile: the target PC is a modest Windows desktop with 16 GB RAM and very limited graphics memory. Keep default parallel agent count at 2–3, use hosted API providers only when configured, do not launch multiple local models automatically, and measure CPU/RAM before raising concurrency.
- Use `.env.example` for placeholder configuration only. Secret values go into the operating system's credential store where possible; never check keys into Git.

## 6. Agent architecture and orchestration behavior

The user wants agents that can plan, create agent teams, delegate and verify. Implement this with ADK, not a pile of uncontrolled recursive loops.

### Root system
`agentcity_root` receives task, interaction mode, active project/workspace scope, permission policy, and budgets. It produces a structured mission plan before side effects. The plan includes objective, assumptions, task DAG, dependencies, selected agents/tools, data sources, risk categories, approvals needed, budget caps, timeout/cancellation, and verifiable completion criteria.

### Initial specialist agents
- Planner: task decomposition and dependency/risk/budget plan.
- Researcher: source-grounded web/file research.
- Architect: repo fit, design, interfaces, dependencies.
- Coder: changes in assigned branch/worktree and scope.
- Debugger: reproduction and root-cause investigations.
- Test Engineer: focused tests and integration/eval cases.
- Reviewer: independent diff/risk review.
- Security Guard: checks permission, prompt injection, secrets, and data egress.
- Desktop Operator: uses only the governed desktop service.
- Verifier: final objective/acceptance checks against evidence.

Use ADK-supported workflow/team patterns and appropriate callbacks/guardrails. Parallelize truly independent tasks; sequence dependent work. Each delegated task includes objective, context, input contract, output schema, file ownership (for coding), budget, timeout, tests, and completion evidence. Parent agents must inspect results and can reject incomplete work. Child agents cannot change parent permissions.

### Runtime mission lifecycle
`draft → planned → waiting_for_approval (if needed) → queued → running → verifying → completed | failed | cancelled | blocked`.
Persist every transition. Use heartbeat, timeout, bounded retry, circuit breaker, and safe resume semantics. A child agent's idle process is not a success signal. A mission only completes when its verifier checks concrete criteria and artifacts.

### Model routing
Select model per task using capability, context size, structured output/tool-use support, latency, quality evaluations, user choice, availability, and budget. Show chosen model/provider, rationale, fallback and measured/estimated use. Provide manual override. Don't assume subscriptions authorize API access. Never bypass provider auth, limits or terms.

### Coding-agent handoff
Detect installed, authorized coding CLIs (e.g., OpenCode/Claude Code/Codex/Gemini CLI) and call their official supported interface/CLI. Every coding mission must declare repository root, worktree path, branch, files it owns, commands permitted, run timeout, and acceptance tests. Record branch, commit SHA where applicable, changed files, exit code, tests and known issues. Verify actual directory and branch from process context.

## 7. Development-time agents and worktree discipline

The agents building AgentCity are separate from the agents that the finished app will run. Create a development roster and model-routing record.

Recommended workers when the tooling supports them:
- Lead orchestrator/integrator: plans and owns schemas, merges, review and final acceptance.
- Repo/reuse auditor: candidate code, license and provenance; owns reuse documentation.
- Backend/ADK worker: runtime, tools, APIs, SQLite, events, approvals and backend tests.
- Desktop UI worker: design system, routes, maps, mission inspector, empty/error/diagnostic states and UI tests.
- Voice/desktop worker: screen permission, Windows control adapter, voice adapters, emergency stop and isolated tests.
- QA/security/eval worker: test harness, threat cases, ADK evaluation set, security review and results.
- Optional docs/release worker: packaging, migration and setup docs.

Run only as many workers as useful; default 2–3 concurrent coding agents on this machine. Do not spawn an agent just to appear autonomous.

**Real worktrees are mandatory when supported.**
1. Inspect `git status`, current branch/worktrees, and preserve user changes.
2. Create actual non-overlapping branches/worktrees for separable work, such as `feat/agentcity-backend`, `feat/agentcity-ui`, `feat/agentcity-desktop-voice`, `test/agentcity-qa`.
3. Assign each worker its exact worktree directory, branch name, file ownership, interface contract, definition of done, and tests.
4. Verify actual isolation from each worker context with `git rev-parse --show-toplevel` and `git branch --show-current`; record evidence. Do not claim worktrees were used unless this check succeeds.
5. If this environment cannot create isolated worktrees, explicitly document it and enforce exclusive file ownership/serialized merges instead. Do not let agents edit the same files concurrently.
6. One owner controls `package.json`, lockfiles, shared schemas, shared migrations and release config. Other agents request changes through a reviewed handoff.
7. Integrator reviews diff, tests, unexpected files and secrets before merging. No force pushes or destructive history rewrites.
8. Every worker reports files/commits, commands/tests/results, deviations, unresolved risks and actual completion evidence.

## 8. Actual build and delivery sequence

### Step A — reproduce baseline and publish a plan
Complete preflight, reuse/license audit, tool discovery, docs and worktree setup. Run existing build/tests and record baseline failures. Make no broad refactor before understanding dependencies.

### Step B — end-to-end foundation spike
Within the existing app, make one harmless vertical slice: launch app → health check → create mission → ADK plan → persist events → UI stream → approved safe test tool → verifier → artifact → cancel/restart tests. Prove the main integration before expanding.

### Step C — production-quality shared core
Implement typed API contracts, SQLite migrations, mission lifecycle, ADK team/workflows, Skills Bridge/MCP adapter, model adapter, policy/approval engine, event stream, audit trail, artifact storage, cancellation/recovery, errors and diagnostics.

### Step D — premium interface
Implement the full route structure in Section 4 using live backend state. Add usable agent-team editor, task graph, inspector, event history, settings, keyboard navigation, accessibility, search, loading/empty/error states, and coherent responsive layout. Do not use dummy metrics in real mode.

### Step E — desktop and voice
Implement consent-based screenshot/screen awareness, permission-checked Windows UI automation, action verification, visible activity state, emergency stop, push-to-talk STT/TTS and interruption. Add optional wake word only after visible indication and opt-in flow exist.

### Step F — higher-level capabilities
Add project RAG/source provenance, files and artifacts, coding agents/worktrees, routines, model routing and evaluation dashboard; integrate rather than duplicate upstream features where possible.

### Step G — hardening and packaging
Run full tests, security tests, ADK evaluations, dependency/license scans, resource checks and a clean-install Windows packaging/launch test. Fix failures and rerun. Produce release verification report with measured results. Do not deploy publicly, publish a package, push to remote or make irreversible host changes unless expressly authorized.

## 9. Security boundaries are feature requirements

- User-consent desktop permissions and persistent screen/mic activity indicator.
- On-demand screen capture default. Explicit, time-limited watch session only if enabled.
- Prompt injection from pages/files/skills/screenshots/output cannot grant permissions.
- Separate deterministic policy broker decides tools/approvals; LLM does not decide its own privileges.
- Read-only vs local mutation vs external/consequential vs blocked risk levels.
- Confirm exact target/content for sends, publishing, deletion, purchases, remote resource changes, installations, and elevated/system settings.
- Bounded agent depth/concurrency/time/tool calls; per-mission cost/time budgets.
- Loopback-only local API, authenticated IPC, schema checks, path/symlink defenses, no shell concatenation, timeouts/output caps.
- Secrets in credential manager; logs redacted; no telemetry/cloud sync by default.
- Emergency stop works even if model hangs; failed safety checks fail closed.
- No hidden microphone/screen surveillance, no bypassing OS protections/provider limitations, no uncontrolled administrator shell.

## 10. Required feature completeness rules

For each visible control, implement a real action and state result. No dead buttons. No TODO-only critical pathway. No mock data in production state. Demo mode may exist but must be opt-in and clearly marked.

Each capability must include:
- implementation and UI;
- validation and permission checks;
- meaningful loading/success/error/disabled states;
- event/audit trail with redaction;
- unit/integration/E2E tests as relevant;
- documentation and setup/troubleshooting instructions;
- clear provider/permission requirements;
- acceptance evidence.

If a feature is blocked by external credentials, native permissions, an unavailable custom tool, or incompatible upstream code, implement the integration seam and honest setup state, explain exactly what remains, and never claim the live feature is complete. Do not conceal an issue under “future work” if a safe, scoped implementation is possible now.

## 11. Required tests and release acceptance

Use `ACCEPTANCE_TESTS.md` as the gate. Add tests for normal behavior, failure, timeouts, cancellation, restart recovery, permissions, malicious tool/page/document content, tool schema errors, rate limits, missing providers, and output provenance. Use ADK evaluation for tool trajectory as well as final-answer quality; do not rely on one happy-path answer.

Run all available checks from the selected project's own scripts, at minimum:
- format/lint/type checks;
- unit tests;
- backend integration tests;
- UI tests;
- API/IPC security tests;
- ADK evals for the scenario dataset;
- Playwright or equivalent end-to-end tests;
- packaged Windows app smoke test where the environment supports it;
- license and dependency audit.

For each run capture exact command, exit code, counts, duration if available, and report path. Distinguish pass/fail/skip/blocked. A source-code build alone is not enough.

## 12. Final deliverables

Must be created in the repository and linked/referenced in the final response:
1. Working AgentCity source app and all real runtime modules.
2. Original visual system, complete navigation, operational City Overview and user settings.
3. ADK agents/teams/workflows built or validated using the existing ADK Agent Builder when present.
4. Skills Bridge integration using actual registered schemas when present.
5. Desktop control/voice/provider adapters, permission broker, cancellation and audit trail.
6. SQLite migrations, seed/setup path, artifact storage and app diagnostics.
7. `README.md` with Windows setup, launch, configuration, provider setup, MCP/Skills Bridge setup, permissions, tests, packaging, update and troubleshooting instructions.
8. Documents listed in preflight and API/tool schemas.
9. Unit, integration, E2E, security and ADK evaluation tests.
10. `docs/agentcity/release-verification.md` with all results and caveats.
11. `docs/agentcity/deliverables-and-acceptance.md` with each item marked implemented/tested, partial, blocked, or not implemented with a reason.
12. A launch script or supported start command and a clean Windows package if feasible in the current environment.
13. License/NOTICE and third-party attribution aligned with actual adopted source.

## 13. Completion report format

At completion, summarize:
- base repo and pinned commit/tag, selected license, and reuse decisions;
- exact custom ADK Agent Builder and Skills Bridge tool names found, what was invoked, and evidence of resulting artifacts;
- main implemented user workflows, with no unsupported claims;
- worktrees/branches actually used and verification evidence;
- commands executed, test counts, ADK evaluation outcomes, failed/skipped/blocked checks;
- resource/build/install results;
- external keys/permissions still required;
- known issues ranked by severity and exact reproduction steps;
- file paths for README, runbook, tests, and release report;
- exact command to launch AgentCity.

If the coding environment has no access to the user's actual repository or custom tool servers, do not pretend to have changed their PC. Produce the most complete portable source/build deliverable possible, document the integration boundary, and state exactly what must run in the user's environment.

**Now execute:** begin preflight; inspect the actual tools, repo and existing code; use the existing ADK Agent Builder and Skills Bridge interfaces where available; create verified isolation for parallel coding; implement the vertical slice; then build the remaining product in dependency order; run all tests and package/report. Continue until concrete deliverables exist, not just a plan.
