---
title: AI Context — Read This First
status: active
owner: integration
last_verified: 2026-10-23
---

# AI Context — Read This First

You are working on **AgentCity**, a Windows-first, local-first desktop AI
command center. This page is the compressed context pack. It is designed so a
new agent can make correct changes without reading the whole codebase first.

If anything here conflicts with `AGENTS.md`, the constitution wins. If reality
conflicts with this page, fix this page in the same change.

## 1. Product in five lines

1. A desktop app where the user talks, types, or points at work; AgentCity
   assembles a bounded team of Google ADK agents to do it.
2. Every agent, task, tool call, approval, cost, and artifact shown in the UI is
   a projection of a persisted runtime event, never an animation.
3. The user supervises through a live City Overview, an approval queue, a
   mission inspector, and an emergency stop.
4. Computer use, voice, files, research, and coding CLIs are adapters behind one
   deterministic permission broker.
5. Local-first: SQLite, loopback-only API, no telemetry, no cloud requirement.

## 2. Current state (be precise)

| Area | State |
|---|---|
| Documentation and context pack | **Complete (M0)** |
| Tool clones and pins | **Complete (M0)** |
| Application source | **Not started** |
| Live model runs | **Blocked** — no provider key configured |
| Desktop control / voice | **Planned** — M4 |

The full status matrix is generated in `docs/agentcity/state-of-build.md`. Never
describe a planned feature as working.

## 3. Architecture in ten lines

1. Electron main process owns windows, hotkeys, and the sidecar lifecycle.
2. A context-isolated preload exposes a narrow, typed IPC allowlist.
3. The React renderer renders state and sends intents; it never touches Node.
4. A Python FastAPI sidecar binds `127.0.0.1` with a per-launch token.
5. The deterministic Mission Engine owns the task DAG, budgets, approvals,
   retries, checkpoints, cancellation, and restart recovery.
6. Google ADK agents reason inside a step; they do not own durable state.
7. SkillBridge runs as a stdio MCP subprocess; its 19 tools map into the
   capability registry with risk classes.
8. Every transition appends a typed event; the UI streams and replays by cursor.
9. SQLite (WAL) is the source of truth; artifacts live in an app-owned folder.
10. A code-level policy broker grants or denies actions; the model never can.

## 4. Where to change what

| Task | Start here |
|---|---|
| Add an API endpoint | `docs/engineering/change-recipes.md` § API |
| Add a UI route | `docs/engineering/change-recipes.md` § UI route |
| Add or edit an ADK agent | `docs/engineering/change-recipes.md` § ADK agent |
| Add an MCP/SkillBridge capability | `docs/engineering/change-recipes.md` § MCP tool |
| Add a mission event type | `docs/engineering/change-recipes.md` § Event |
| Add a DB column or table | `docs/engineering/change-recipes.md` § Migration |
| Change approval rules | `docs/agentcity/security-model.md` + policy tests |
| Add a desktop action | `docs/engineering/change-recipes.md` § Desktop action |
| Investigate a failure | `docs/engineering/debugging-playbook.md` |
| Cut a release | `docs/runbooks/release-verification.md` |

## 5. Invariants (never violate)

- The model proposes; code decides. No self-granted permissions.
- Events persist before the UI consumes them; sequence is monotonic per mission.
- A mission cannot complete without a verifier decision and required approvals.
- Screen capture is off by default and visibly indicated when on.
- Wake word is off by default and always visible when on.
- Secrets never appear in logs, prompts, fixtures, screenshots, or Git.
- No fake agents, metrics, costs, or dead controls in real mode.
- Local API binds loopback only and rejects requests without the launch token.
- Paths are validated against approved roots; symlinks and junctions resolved.
- Cancellation propagates to ADK runs, child processes, MCP calls, and desktop
  loops within the documented timeout.

## 6. Environment facts

- Windows 11 Home, PowerShell; 7.8 GB RAM; Intel UHD graphics.
- Python 3.12.10, `uv` 0.12.5, Node 24.19.0, npm 11.17.0.
- `google-adk` 2.12.0, `mcp` 2.3.0, FastAPI, pytest, pyautogui installed.
- `psutil`, pnpm, Rust, Playwright, and pywinauto are **not** installed yet.
- PowerShell 7 (`pwsh`) is absent; use built-in Windows PowerShell 5.1
  (`powershell -File ...`).
- No provider API key configured. Offline Mode is the default test path.
- The project sits in a OneDrive folder: keep build output, databases, and
  `.venv` out of sync where possible; see the troubleshooting runbook.

## 7. Tool roles

| Tool | When | How |
|---|---|---|
| ADK Agent Builder | Build time | CLI in `src/skills/adk-agent-builder`; generates and validates committed agent code |
| SkillBridge | Runtime | `python -m skillbridge --home <temp> mcp-serve` from `src/skills/skills-bridge/src`, spoken to over stdio MCP |
| Google ADK | Runtime | Imported library inside the sidecar |
| OpenCode CLI | Optional adapter | Detected only when installed; never auto-installed |

Do not edit `src/skills/**`; it is a read-only clone, gitignored by design.

## 8. Commands that exist today

Run from the repository root.

```powershell
python scripts/check-docs.py          # documentation gate
python scripts/generate-context.py    # rewrites state-of-build + repo map
powershell -File scripts/bootstrap-skills.ps1 -VerifyOnly
powershell -File scripts/bootstrap-skills.ps1 -AdkRepoUrl <url> -SkillsRepoUrl <url>
$env:PYTHONPATH='src/skills/skills-bridge/src'; python -m skillbridge --version
```

Application commands are marked `planned` in `PROJECT_MANIFEST.json`. Do not
invent scripts that are not there.

## 9. Known traps

- ADK free tier: ~5 RPM and ~20 requests/day per model; 429 can surface as
  HTTP 500. Pace live runs and never retry blindly.
- PowerShell may report `NativeCommandError` and a nonzero exit code even when
  Python tests pass. Read the summary line.
- OneDrive sync can corrupt SQLite WAL and slow `node_modules` dramatically.
- The real SkillBridge catalog is corrupt (91 integrity findings). Never open
  it; use a throwaway `--home` until the user recovers it.
- MCP stdio requires newline-delimited JSON and no stray stdout logging.
- A child process going idle is not success; require exit code plus evidence.
- UI Automation cannot control elevated windows; fail closed and explain.

## 10. Documentation map

- `docs/README.md` — index and reading orders.
- `docs/agentcity/` — product, security, reuse, tooling, agent roster, testing.
- `docs/architecture/` — overview, diagrams, contracts, data model, ADRs.
- `docs/engineering/` — standards, playbooks, recipes, performance budget.
- `docs/runbooks/` — setup, providers, MCP, desktop, voice, packaging, release.
- `docs/templates/` — ADR, feature, incident, release, handoff, onboarding prompt.

## 11. Next task

M1 vertical slice. Read `docs/agentcity/implementation-plan.md` § M1 and
`docs/architecture/contracts.md`, then build the smallest end-to-end mission:
launch → health → plan → approval → local tool → verifier → artifact → cancel →
restart recovery. Update the manifest and regenerate status when it passes.
