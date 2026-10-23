---
title: Troubleshooting Runbook
status: active
owner: engineering
last_verified: 2026-10-23
---

# Troubleshooting Runbook

Start with the evidence, not with a guess.

## 1. Collect first

```powershell
# Run from the repository root.
git status --short --branch
python --version
node --version
python -c "import importlib.metadata as m; print(m.version('google-adk'))"
python scripts/check-docs.py
Get-Process | Where-Object { $_.ProcessName -match "electron|python|node" } |
  Select-Object Id, ProcessName, WorkingSet64, StartTime
```

Copy the relevant log tail and the exact command that failed. Redact secrets.

## 2. Quick table

| Symptom | Section |
|---|---|
| App does not start | § 3 |
| API returns 401/403 | § 4 |
| Mission stuck or wrong state | § 5 |
| Events missing or duplicated | § 6 |
| ADK/provider failure | § 7 |
| SkillBridge failure | § 8 |
| Desktop capture/control failure | § 9 |
| Voice failure | § 10 |
| Packaging/install failure | § 11 |
| OneDrive or disk issues | § 12 |
| Git/worktree issues | § 13 |

## 3. App does not start

1. Check the sidecar log path shown in the error dialog.
2. Run the sidecar manually with the same Python and data home.
3. Check port binding: `Get-NetTCPConnection -LocalPort <port>`.
4. Check migrations: a failed migration refuses startup by design.
5. Check the handshake file exists and is readable by the current user.
6. Blank window: open DevTools, check CSP and preload errors.

Do not fix a startup failure by disabling auth, migrations, or the sandbox.

## 4. API 401 or 403

- `401`: missing/wrong token, or the sidecar restarted. Reload the shell so main
  re-reads the handshake.
- `403 forbidden_origin`: the renderer origin changed (dev server port, packaged
  path). Update the allowlist, not the check.
- Missing `X-AgentCity-Client`: the typed client is bypassed.
- Never print the token in logs or share it between launches.

## 5. Mission stuck

1. Inspect mission status, task statuses, and the last 20 events.
2. Check the run heartbeat; heartbeat is not success.
3. Check for a hung tool: tool invocation status and duration.
4. Check the cancel flag; a cancellation that did not propagate is a bug.
5. Check the budget: an exhausted budget blocks new steps.
6. If the process died, the run should be `interrupted`, not `running`.

Reproduce with a deterministic task and a fake provider before blaming the model.

## 6. Events missing or duplicated

- Compare SQLite rows with the UI cursor.
- Sequence must be monotonic per mission; duplicates are allowed on reconnect but
  must be deduplicated by event id.
- A gap means the client must refetch from `/missions/{id}/events?after=`.
- Missing events after a state change indicate a transaction bug: state and event
  must commit together.
- Do not “fix” by polling faster; fix the ledger or the stream.

## 7. ADK or provider failure

| Error | Check | Action |
|---|---|---|
| `provider_auth_failed` | Key validity, provider account | Replace credential |
| `provider_quota_exceeded` | 429 details, daily counter | Wait, use Offline Mode |
| HTTP 500 with quota detail | Provider error envelope | Backoff with jitter |
| `model_not_found` | Model id in config | Choose a supported model |
| Structured output parse error | Raw response (redacted) | Repair once, then fail closed |
| Timeout | Network, proxy, latency | Retry with a bounded timeout |

Run the offline suite first. If it passes and live fails, the defect is in the
provider path, not the engine.

## 8. SkillBridge failure

**Known on this machine:** the production catalog is corrupt (91 integrity
findings). See `mcp-and-skills.md`.

- Use `--home <temp>` for all development.
- A malformed database is a failed capability, not an empty catalog.
- MCP hangs usually mean stdout pollution or a missing newline; check stderr.
- A missing tool means discovery failed or the server is the wrong version.
- Kill the process tree on Windows; a parent-only kill can leave children.
- Never edit the clone to work around a bug; use configuration or an adapter.

## 9. Desktop capture and control

- Black frame: secure desktop, DRM, or permission missing.
- Wrong coordinates: DPI scaling; set awareness before capture.
- UIA empty: elevated target or unsupported control.
- Stale observation: refresh after every action batch.
- Stop not working: check global hotkey registration and the main-process path.
- Never test on sensitive accounts; use Notepad or a fixture.

## 10. Voice

- No microphone: check Windows privacy settings and device selection.
- Silent capture: check the level meter and the selected device.
- Provider failure: keep audio local, show the error, do not auto-retry.
- TTS stuck: cancel playback, release the audio device, then retry.
- Wake word false positives: disable it; it is opt-in and off by default.

## 11. Packaging

- Installer fails: check the build log, signing, and path length.
- App launches but sidecar missing: verify the sidecar artifact is included.
- Native module error: rebuild against the packaged Electron version.
- Antivirus quarantine: document the false positive and sign the binaries.
- Upgrade failure: test migrations from the previous release, not only fresh.

## 12. OneDrive and disk

- Slow installs or locks: pause OneDrive during builds.
- SQLite corruption: move runtime data to `%LOCALAPPDATA%`.
- `node_modules` conflicts: exclude from sync or move the working copy.
- Disk below 2 GB: stop artifact writes and free space.
- Never let sync restore an older database over a newer one.

## 13. Git and worktrees

- Verify `git rev-parse --show-toplevel` and `git branch --show-current`.
- A worktree pointing at the wrong branch: re-add it from the correct branch.
- Merge conflict: resolve in the owning worktree, rerun tests.
- Do not force-push or run `git clean` to “reset” a confused worker.
- If a worker reports a different directory, stop and fix isolation first.

## 14. PowerShell traps

- `NativeCommandError` with exit 1 can still mean tests passed; read the summary.
- `>` writes UTF-16; use `[System.IO.File]::WriteAllText` for UTF-8 evidence.
- `PYTHONPATH` must be set in the current shell for source-based tools.
- `adk --version` may print a path error; use `adk --help` and the Python package
  version.
- Long paths and spaces in a Windows profile path require quoting.

## 15. When to stop

Stop and ask when recovery requires deleting user data, touching the corrupt
catalog, weakening a security control, or installing a dependency that changes
the architecture. Record the blocker and the safest next step.
