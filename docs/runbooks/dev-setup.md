---
title: Development Setup Runbook
status: active
owner: engineering
last_verified: 2026-10-23
---

# Development Setup Runbook

## 1. Prerequisites

| Tool | Version | Check |
|---|---|---|
| Windows | 11 | `winver` |
| Python | 3.12+ | `python --version` |
| uv | 0.12+ | `uv --version` |
| Node | 24+ | `node --version` |
| npm | 11+ | `npm --version` |
| Git | 2.55+ | `git --version` |
| PowerShell | 5.1 or 7 | `$PSVersionTable.PSVersion` |

PowerShell 7 (`pwsh`) is optional; the built-in Windows PowerShell 5.1 runs the
scripts. Examples use `powershell -File`; substitute `pwsh -File` if installed.
If the default execution policy blocks a script, rerun that command with
`-ExecutionPolicy Bypass` for the process only, after reviewing the script.

Node, npm, and uv are required from M1 onward; the M0 documentation pack uses
only Python and Git. Optional for later milestones: Playwright browsers,
`pywinauto`, a Gemini API key. None are required to read docs or run Offline
Mode tests.

## 2. Repository

```powershell
# Run from the repository root.
git status --short --branch
```

Expected after the M0 commit: `## main` and no unexpected changes. If the tree
is not committed, the untracked files are expected only during initial setup.

The two tools are already cloned at pinned commits on this machine. Verify them
without changing anything:

```powershell
powershell -File scripts/bootstrap-skills.ps1 -VerifyOnly
```

On a fresh machine, restore them with explicit sources (URLs are never
hardcoded):

```powershell
powershell -File scripts/bootstrap-skills.ps1 `
  -AdkRepoUrl "<adk-agent-builder-repo>" `
  -SkillsRepoUrl "<skills-bridge-repo>"
```

Or copy from local checkouts:

```powershell
powershell -File scripts/bootstrap-skills.ps1 `
  -AdkFromLocal "C:\path\to\adk-agent-builder" `
  -SkillsFromLocal "C:\path\to\skills-bridge"
```

Verify the pins:

```powershell
git -C src/skills/adk-agent-builder rev-parse HEAD   # a74d73b...
git -C src/skills/skills-bridge rev-parse HEAD       # 25c352e...
```

## 3. Environment file

```powershell
Copy-Item .env.example .env
```

Defaults are safe: no provider, capture off, wake word off. Never commit `.env`.
In production, secrets live in the OS credential store.

**M0 note:** no application code reads `.env` yet. The file records the M1
contract; the shell scripts do not load it. `SKILLBRIDGE_HOME` is read only by
the SkillBridge process itself, and only when set in that process's environment.

## 4. Tool verification

```powershell
python -c "import google.adk; print('adk ok')"
python -c "import mcp; print('mcp ok')"

$env:PYTHONPATH='src/skills/adk-agent-builder/src'
python -m adk_agent_builder.cli doctor --json

$env:PYTHONPATH='src/skills/skills-bridge/src'
python -m skillbridge --version
```

Pass criteria: exit code 0, `google-adk` 2.12.0, Agent Builder `adk_cli` 2.12.0
with only optional Agents CLI/gcloud absent, and SkillBridge 2.0.1. The doctor's
`fallback_mode_active: true` is expected on this machine, not a failure. A JSON
blob alone is not proof; check those fields.

## 5. SkillBridge isolation

The production catalog on this machine is corrupt. Do not use the real home for
development until it is recovered.

Run from the repository root; the relative `PYTHONPATH` matters:

```powershell
$env:PYTHONPATH='src/skills/skills-bridge/src'
$testHome = Join-Path $env:TEMP "agentcity-sb-test"
python -m skillbridge --home $testHome --offline --json search-skills "pdf" --limit 1
```

Every test and dev command must pass `--home <temp>` or set `SKILLBRIDGE_HOME`.
The environment variable is read by SkillBridge, not by the bootstrap script.

## 6. Documentation checks

```powershell
python scripts/check-docs.py
python scripts/generate-context.py
```

`check-docs.py` is the gate; it must pass before committing docs. The generator
is not a check: it unconditionally rewrites `docs/agentcity/state-of-build.md`
and `docs/repo-map.md` from the manifest. Run it only when you intend to update
those files, and commit the result with the change.

## 7. Application setup (M1, not available yet)

When M1 lands, this section will list the exact commands:

```powershell
# planned
uv sync --project src/backend
npm install --workspace src/desktop
npm run dev --workspace src/desktop
uv run pytest --project src/backend
```

Do not run these until `src/backend/pyproject.toml` and
`src/desktop/package.json` exist.

## 8. Test data rules

- App home: a temp directory per test. Never `%LOCALAPPDATA%\AgentCity`.
- SkillBridge home: a temp directory. Never `~/.skillbridge`.
- Provider: fake by default. Live tests are opt-in.
- Desktop: Notepad or a fixture window only.
- Artifacts: temp directory, cleaned up by the fixture.

## 9. First-run troubleshooting

| Symptom | Fix |
|---|---|
| `adk` path error in PowerShell | Use `adk --help`; verify `google-adk` version |
| Agent Builder reports fallback | Expected; Agents CLI/gcloud are optional |
| SkillBridge malformed DB | Use `--home`; see `docs/runbooks/mcp-and-skills.md` |
| `PYTHONPATH` not applied | Set it in the current shell; verify with `python -c "import skillbridge"` |
| Node command not found | Reopen the shell after install; check PATH |
| OneDrive locks | Pause sync during builds; runtime data outside the tree |

## 10. Evidence

Save setup verification output under `docs/agentcity/evidence/` when it supports
a claim. Use UTF-8 without BOM. Include the command, working directory, exit
code, and date.
