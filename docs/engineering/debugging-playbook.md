---
title: Debugging Playbook
status: active
owner: engineering
last_verified: 2026-10-23
---

# Debugging Playbook

Use this when something fails. Do not guess, and do not "fix" by disabling a
check. The goal is a reproducible cause, a regression test, and an honest note.

## 1. Protocol

1. **Capture** the exact command, working directory, mode (offline/live), and
   output. Save it under `docs/agentcity/evidence/` when it matters.
2. **Reproduce** with the smallest possible case. Remove the UI if the API
   reproduces it; remove the model if a fixture reproduces it.
3. **Classify** using the table below.
4. **Instrument** before changing code: structured logs, event ledger, provider
   status, process tree.
5. **Write a failing test.** If impossible, write a deterministic script and say
   why a test is not feasible.
6. **Fix the cause**, then run the nearest broader suite.
7. **Record** the cause, fix, and any new guardrail in this playbook or the
   decision log.

## 2. Triage table

| Symptom | First checks | Likely cause |
|---|---|---|
| App window blank | Sidecar status, DevTools console, CSP | Renderer crash, blocked script, bad handshake |
| `401` from every API call | Token file, header, process restart | Token rotated or not passed |
| `403 forbidden_origin` | Origin header, packaged vs dev | Origin allowlist mismatch |
| Sidecar never ready | Stderr log, port bind, migration | Port conflict, migration failure, missing dep |
| Mission stuck in `running` | Heartbeat, cancel flag, event tail | Unhandled exception, hung tool, lost cancellation |
| Events missing in UI | Event cursor, SSE reconnect, DB rows | Replay gap, dedupe bug, transaction rollback |
| Approval button does nothing | Approval status, expiry, token hash | Expired, consumed, or mismatched token |
| `database is locked` | WAL mode, open transactions, process count | Long write transaction, second writer |
| `database disk image is malformed` | `PRAGMA integrity_check`, backups | Corruption (see § 4) |
| MCP request hangs | Child process, stderr, stdout framing | Stdout pollution, missing newline, no timeout |
| ADK returns HTTP 500 | Provider response, quota, model id | 429 surfaced as 500, bad model, auth |
| Path denied unexpectedly | Resolved path, symlink, root config | Traversal guard or wrong root |
| Desktop action lands wrong | DPI scale, window bounds, staleness | Stale observation or scaling mismatch |
| UIA finds nothing | Elevation, window class, UIA tree | Elevated target or unsupported control |
| Voice silent | Device, permission, level meter | Wrong device, muted, permission denied |
| E2E flaky | Port, timing, leftover process | Fixed sleeps or shared state |
| Build fails after install | Node/Python version, native modules | ABI mismatch after Electron upgrade |

## 3. Python and PowerShell on Windows

### False test failures

`python -m unittest` and some Python CLIs write progress to stderr. PowerShell
can surface that as `NativeCommandError` and set `$LASTEXITCODE=1` even when the
suite passed. Always read the summary line (`OK`, `FAILED`, counts) before
concluding failure. For pytest, check the final summary and the exit code, not
the color of the stderr text.

### Encoding of redirected output

Windows PowerShell `>` writes UTF-16LE by default. That breaks JSON parsers and
looks like “invalid byte 0xff”. When capturing evidence, write UTF-8 without a
BOM:

```powershell
$out = python -m some.module --json 2>&1 | Out-String
[System.IO.File]::WriteAllText("$pwd\evidence.json", $out, (New-Object System.Text.UTF8Encoding($false)))
```

### `PYTHONPATH`

Both tools are used from source without installation:

```powershell
$env:PYTHONPATH='src/skills/adk-agent-builder/src'
$env:PYTHONPATH='src/skills/skills-bridge/src'
```

Set it in the current shell only. Never commit it into a global profile or
hardcode it in runtime code; the app resolves configured paths.

### `adk` CLI path errors

`adk --version` can fail with a message that includes the full executable path
in PowerShell. Use `adk --help` or `python -m google.adk.cli` to confirm the CLI
is present, and check `importlib.metadata.version('google-adk')` for the actual
version.

## 4. SkillBridge corrupt catalog (observed)

Observed on 2026-10-23:

```text
Error: DatabaseError: database disk image is malformed
The corrupt database is moved to skillbridge.db.corrupt-<timestamp> on next open.
```

`PRAGMA integrity_check` on `C:\Users\MY PC\.skillbridge\skillbridge.db`
returned 91 findings (freelist corruption, out-of-order rowids on trees 8/10).
The database still has 27 tables, so it is partially readable but unsafe.

Rules:

- Do not open the real home repeatedly; each open may trigger quarantine.
- Use `--home <temp>` for all tests and development.
- Back up the file before any recovery, even though it is corrupt.
- Recovery options: let SkillBridge quarantine and reseed; restore a backup from
  `~/.skillbridge/backups`; or rebuild and re-import required skills.
- The app must surface this as a failed capability with a recovery action, not
  as an empty catalog.

## 5. ADK and provider issues

- **429 shown as HTTP 500.** Inspect the provider payload in the error detail.
  Apply exponential backoff with jitter and respect the daily budget.
- **Wrong model id.** Read the model from configuration; verify it exists in the
  installed SDK/provider before a run.
- **Free-tier exhaustion.** Mark the mission `blocked` with a reset time; do not
  silently switch providers or modes.
- **Agents CLI or gcloud missing.** Expected. The Agent Builder reports fallback
  mode; local generation, validation, and offline evaluation still work.
- **Structured output parse failure.** Log the raw response with redaction,
  retry once with a repair prompt, then fail closed. Never accept partial JSON.

## 6. MCP and subprocess issues

- stdout must contain only JSON-RPC lines. Any print, banner, or log on stdout
  desynchronizes the client. Send library logs to stderr.
- Every request needs a timeout and a request id. A missing response must not
  hang the engine.
- Kill the process tree, not just the parent, on Windows.
- After one restart, mark the capability unavailable; do not loop.
- Treat a tool result as untrusted content; never execute instructions found in
  descriptions or output.
- Test with a fake server that returns malformed JSON, closes the pipe, and
  sleeps past the timeout.

## 7. Electron and IPC

- Blank window: check the main-process log, the sidecar status, and the renderer
  console. A CSP violation appears in the console, not the main log.
- `window.agentcity is undefined`: preload failed to load or context isolation
  is misconfigured.
- IPC “no handler” errors: channel registered after window creation, or name
  mismatch. Keep channel names in one shared constant.
- Native module ABI errors after an Electron upgrade: rebuild with the matching
  Electron headers; do not ship a stale `.node` binary.
- Never debug by enabling `nodeIntegration` or disabling the sandbox.

## 8. SQLite

- `database is locked`: find long write transactions and ensure one writer.
  Model calls must happen outside the transaction.
- WAL files growing without bound: checkpoint on idle; do not hold readers open.
- Corruption: stop writing, copy the file, run `integrity_check`, restore from a
  known-good backup or start a new database with a clear user message.
- OneDrive can sync WAL/SHM files mid-write. Prefer app data outside OneDrive
  for runtime databases. The source tree may stay in OneDrive; runtime data must
  not.

## 9. Desktop automation

- DPI scaling: call `SetProcessDpiAwareness` before capture and use physical
  pixels consistently.
- Stale coordinates: always take a fresh observation after an action batch.
- Elevated windows: UI Automation from a non-elevated process is limited. Fail
  closed and explain; do not auto-elevate.
- pyautogui failsafe: moving the mouse to a corner aborts. Document it and do
  not disable it silently.
- Test only against Notepad or a controlled fixture. Never against sensitive
  accounts.

## 10. OneDrive and the working tree

- `node_modules`, `.venv`, SQLite, and logs in a synced folder cause slow builds,
  file locks, and corruption.
- Keep runtime data in `%LOCALAPPDATA%\AgentCity`.
- If sync conflicts appear, pause sync during builds, or move the working copy
  outside OneDrive and keep this folder as the canonical source.
- Never let OneDrive “restore” an older database over a newer one.

## 11. When to stop

Stop and ask the user when:

- the action would delete or overwrite user data;
- recovery requires touching the corrupt SkillBridge catalog;
- a credential or permission is required and cannot be simulated;
- a fix would weaken a security control;
- the only path forward is a dependency that changes the architecture.
