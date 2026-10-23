# AGENTS.md — AgentCity Project Constitution

This file is the operating contract for every AI agent and human contributor
working in this repository. It overrides personal preference. If a task
conflicts with this file, stop and surface the conflict instead of guessing.

## 1. What AgentCity is

AgentCity is a Windows-first, local-first desktop AI command center. It runs
Google ADK agent teams, integrates the SkillBridge MCP broker, observes real
mission state, and gives the user supervised control of the desktop, voice, and
coding agents. The product is defined by **real execution**, not animated demos.

Read in this order before touching code:

1. `docs/AI_CONTEXT.md` — the one-page source of truth.
2. `docs/PROJECT_MANIFEST.json` — versions, commands, paths, feature status.
3. `docs/agentcity/state-of-build.md` — what actually works today.
4. The one document relevant to your task (see `docs/README.md`).
5. Only then, the code.

## 2. Non-negotiable rules

1. **No fiction.** Never render a fake agent, fake tool call, fake cost, fake
   test result, or dead button in real mode. Demo data is allowed only behind an
   explicit, visibly labeled Demo Mode.
2. **Deterministic policy.** The LLM proposes actions; code grants or denies
   them. Agents cannot modify their own permissions, approvals, or budgets.
3. **Secrets never leak.** No keys in Git, logs, prompts, screenshots, fixtures,
   or test snapshots. Use the OS credential store or environment variables.
4. **Docs in the same change.** A feature is not done until its docs, status
   matrix, and tests are updated in the same commit.
5. **Evidence discipline.** Every claim of success maps to a command and output
   stored under `docs/agentcity/evidence/`. Label each check `passed`, `failed`,
   `skipped`, `mocked`, or `blocked`.
6. **Fail closed.** If policy, permission, schema, or runtime state cannot be
   established, deny the action and explain the blocker.
7. **Preserve user work.** No `git clean`, `git reset --hard`, force-push, bulk
   rewrite, or deletion of untracked files. Ask before destructive actions.
8. **Commit discipline.** Commit every production-stable update after checks
   pass. One logical change per commit. Conventional Commits format.
9. **Resource budget.** The target machine has 7.8 GB RAM. Default to at most
   two concurrent agent workers, no local models, bounded queues and buffers.
10. **Honest integration boundaries.** If a provider key, native permission, or
    tool is unavailable, implement the adapter and the honest unconfigured
    state, and mark live tests blocked. Never claim a mocked path is live.

## 3. Verified environment facts

| Fact | Value |
|---|---|
| OS | Windows 11 Home, PowerShell |
| RAM | 7.8 GB total (not 16 GB) |
| Python | 3.12.10, `uv` 0.12.5 |
| Node | v24.19.0, npm 11.17.0; **pnpm and Rust are not installed** |
| ADK | google-adk 2.12.0, `adk` CLI present |
| MCP | Python `mcp` 2.3.0 |
| SkillBridge | cloned at `src/skills/skills-bridge` (MIT), pinned `25c352e` |
| ADK Agent Builder | cloned at `src/skills/adk-agent-builder` (Apache-2.0), pinned `a74d73b` |
| Providers | No API key configured by default; Offline Mode is the baseline |
| Desktop libs | `pyautogui` present; `pywinauto`, Playwright not yet installed |

Re-verify facts that affect your task instead of trusting stale prose. Update
`docs/PROJECT_MANIFEST.json` when a version or path changes.

## 4. Tool roles (do not confuse them)

- **ADK Agent Builder is a build-time tool.** Invoke its CLI to produce,
  validate, test, and evaluate committed ADK agent definitions. It is not a
  runtime service and must not be exposed as one.
- **SkillBridge is a runtime dependency.** AgentCity spawns
  `python -m skillbridge mcp-serve` over stdio, speaks MCP JSON-RPC, and maps
  its broker tools into the capability registry with risk classes.
- **Google ADK is the reasoning runtime.** It does not own durable mission
  state. The deterministic Mission Engine owns lifecycle, retries, approvals,
  checkpoints, cancellation, and restart recovery.

## 5. Repository map

```
src/desktop/      Electron main, preload, React renderer (M1)
src/backend/      FastAPI sidecar, mission engine, ADK agents, adapters (M1)
src/skills/       Locally cloned tools; gitignored, restored by script
docs/             Context, architecture, engineering rules, runbooks
scripts/          Bootstrap, doc checks, context generation
```

Never edit files under `src/skills/` to make AgentCity work. Treat cloned tools
as read-only dependencies; patch by configuration or an adapter in our source.

## 6. Environment setup

```powershell
# Restore the two local tool clones at their pinned commits.
# Sources are never hardcoded; pass URLs or local paths.
powershell -File scripts/bootstrap-skills.ps1 `
  -AdkRepoUrl "<adk-agent-builder-url>" `
  -SkillsRepoUrl "<skills-bridge-url>"

# Verify an existing installation without changing it
powershell -File scripts/bootstrap-skills.ps1 -VerifyOnly

# Verify tooling
python -c "import google.adk; print('adk ok')"
$env:PYTHONPATH='src/skills/skills-bridge/src'
python -m skillbridge --version
```

Project commands will be added to `PROJECT_MANIFEST.json` as M1 lands. Until
then, do not invent `npm run` scripts that do not exist.

## 7. Code rules (summary)

- Python: 3.12+, full type hints on public functions, Pydantic models at every
  boundary, `ruff` and `pytest`, 4-space indent, 100-column lines.
- TypeScript: `strict: true`, no `any` at API boundaries, discriminated unions
  for state, components small and testable, 2-space indent.
- Errors: typed error codes, actionable messages, no bare `except:` and no
  swallowed promises. Every failure has a user-visible state.
- Logging: structured JSON, include `mission_id`/`run_id`/`task_id` when known,
  redact secrets and sensitive paths.
- Async: every long operation accepts cancellation; every external call has a
  timeout; no unbounded loops or queues.
- Data: SQLite WAL, explicit migrations, transactions around state transitions,
  UTC timestamps, schema-versioned event payloads.
- UI: loading, empty, error, disabled, and blocked states are mandatory. No
  color-only state. Keyboard navigation and focus visibility required.

Full standards: `docs/engineering/coding-standards.md`,
`backend-guidelines.md`, `frontend-guidelines.md`.

## 8. Issue-solving protocol

Follow this sequence for bugs and incidents:

1. **Reproduce** with the smallest command; record expected vs actual and
   environment.
2. **Classify** the failure: UI, IPC, API, mission engine, ADK, MCP/SkillBridge,
   desktop, voice, storage, packaging.
3. **Write a failing test** before the fix. If a test is impossible, document
   why and capture a deterministic reproduction script.
4. **Instrument**, do not guess: structured logs, event ledger, provider
   response codes.
5. **Fix the root cause**, not the symptom. Check for the same defect elsewhere.
6. **Regression test** and run the nearest broader suite.
7. **Record evidence** in `docs/agentcity/evidence/` and update
   `state-of-build.md`, the decision log, or the troubleshooting runbook.
8. If blocked by credentials or permissions, implement the honest blocked state
   and assign a precise setup instruction.

Known Windows traps and their playbooks: `docs/engineering/debugging-playbook.md`.

## 9. Documentation rules

- Every document has frontmatter: `title`, `status`, `owner`, `last_verified`.
- `AI_CONTEXT.md` and `PROJECT_MANIFEST.json` are updated in the same commit as
  any architectural, path, or status change.
- Architecture decisions use ADRs; one-way doors require an ADR before code.
- Diagrams are Mermaid inside Markdown, valid on GitHub, and stored in
  `docs/architecture/diagrams.md`.
- No duplicate sources of truth. Link to the canonical document instead.
- Run `python scripts/check-docs.py` before committing documentation changes.

## 10. Git and agent delegation

- Branches: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`, `test/<scope>`.
- Use real Git worktrees for separable parallel work. Verify each worker with
  `git rev-parse --show-toplevel` and `git branch --show-current`; never claim
  isolation that was not verified.
- Maximum two or three concurrent workers on this machine. One owner for shared
  files (`package.json`, lockfiles, migrations, API contracts).
- Every worker reports: files changed, commands run, test results, deviations,
  unresolved risks, branch and commit SHA.
- The integrator reviews diffs, unexpected files, and secrets before merging.

## 11. Definition of done

A capability is complete only when all of these exist:

- [ ] Implemented behavior wired to real state.
- [ ] Visible loading, empty, error, disabled, and blocked states.
- [ ] Permission and policy checks with tests.
- [ ] Structured logs with redaction.
- [ ] Unit/integration/E2E test appropriate to the risk.
- [ ] Documentation updated, including setup and limitations.
- [ ] Acceptance evidence recorded with a truthful status.
- [ ] No dead controls, TODO-only critical paths, or mocked data in real mode.

## 12. Fresh-user test

Before declaring a tool, CLI, or workflow complete, hand it to a subagent with
no prior context and ask it to use the feature from scratch. Fix every point of
confusion it reports. Record the session in the evidence folder.
