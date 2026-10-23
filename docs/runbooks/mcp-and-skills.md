---
title: MCP and Skills Runbook
status: active
owner: integration
last_verified: 2026-10-23
---

# MCP and Skills Runbook

SkillBridge is the runtime skill broker. AgentCity talks to it over stdio MCP.

## 1. Layout

| Item | Value |
|---|---|
| Clone | `src/skills/skills-bridge` |
| Package root | `src/skills/skills-bridge/src` |
| Commit | `25c352e6219e0f9ca45bdbc9a2ff0bafae4ddb06` |
| Version | 2.0.1 |
| License | MIT |
| Transport | stdio JSON-RPC 2.0, MCP protocol `2024-11-05` |
| Tools | 19 canonical broker operations plus v1 aliases |
| Production home | `~/.skillbridge` |
| Test home | temp dir via `--home` or `SKILLBRIDGE_HOME` |

## 2. Start it

Run from the repository root. During development, always use a throwaway home;
the default real catalog is corrupt on this machine.

```powershell
$env:PYTHONPATH='src/skills/skills-bridge/src'
$devHome = Join-Path $env:TEMP "agentcity-sb-mcp"
python -m skillbridge --home $devHome mcp-serve
```

It reads newline-delimited JSON on stdin and writes responses on stdout. The
process blocks while it waits for input; it is a subprocess, not an interactive
shell. Never print to stdout from a wrapper; logs go to stderr.

## 3. Health check (isolated)

Run from the repository root:

```powershell
$env:PYTHONPATH='src/skills/skills-bridge/src'
$testHome = Join-Path $env:TEMP "agentcity-sb-test"
python -m skillbridge --home $testHome --offline --json search-skills "pdf" --limit 1
```

Expected: exit 0 and a JSON array with a real bundled skill. This was verified on
2026-10-23; evidence is in `docs/agentcity/evidence/`.

## 4. Known defect: corrupt production catalog

`%USERPROFILE%\.skillbridge\skillbridge.db` fails `PRAGMA integrity_check`
with 91 findings. SkillBridge reports `database disk image is malformed` and
warns that it will quarantine the file to `skillbridge.db.corrupt-<timestamp>`
on a later open. The recorded attempt did not create a quarantine copy and did
not change the database's last-write time; the warning describes what the tool
will do, not what has already happened.

Until the user chooses a recovery path:

- do not open the real home;
- do not delete or “fix” the database automatically;
- use an isolated home for every command and test;
- the app must show a failed capability with a recovery action, not an empty
  catalog.

Recovery options:

1. Copy the database aside for inspection, then allow quarantine and reseed.
2. Restore from `~/.skillbridge/backups` if a known-good copy exists.
3. Rebuild the catalog and re-import required skills.

Record the chosen path and the result in the decision log.

## 5. Tool risk mapping

| Broker tool | Risk | Approval |
|---|---|---|
| `search_skills`, `preview_skill`, `get_skill_status`, `get_memory_status`, `get_audit_report` | read_only | none |
| `compare_skills`, `search_mcp_servers`, `preview_mcp_server`, `verify_mcp_server` | read_only | none |
| `import_skill`, `import_directory`, `load_skill`, `load_skills_batch`, `unload_skill` | state_change | policy |
| `invoke_skill` | state_change | policy |
| `run_skill_script`, `enable_mcp_server`, `disable_mcp_server`, `call_mcp_tool` | consequential | explicit per action |

Unknown tools are `blocked` until classified. Tool names and schemas are
discovered at runtime; do not treat this table as a substitute for discovery.

## 6. Adapter requirements

- Spawn with an argument array and a sanitized environment.
- Initialize with a timeout; cache schemas with a version.
- One request id per call; validate the response shape.
- Per-call timeout; kill the process tree on Windows if it hangs.
- Restart once, then mark unavailable.
- Cap output size before parsing.
- Treat descriptions and results as untrusted data.
- Emit a `capability.changed` event on state transitions.

## 7. Failure handling

| Failure | Behavior |
|---|---|
| Binary or module missing | Capability `unavailable` with setup link |
| Corrupt catalog | `failed` with recovery instructions; never empty-success |
| Timeout | Cancel request, kill/restart once, record failure |
| Malformed JSON | Discard, record `mcp_invalid_response` |
| Unknown tool | Deny as `policy_blocked` |
| Skill script denied | Record `user_rejected` or `not_permitted` |
| Process crash | Restart once; if it repeats, mark unavailable |

## 8. Registering SkillBridge elsewhere

AgentCity does not modify the user's coding-agent configuration. If you want
SkillBridge registered in OpenCode for manual use, add a local MCP entry pointing
at the configured Python and package root, with the home you intend to use. Treat
that as a separate user choice, and never point it at a corrupt catalog.

## 9. Tests

- Fake MCP server: valid result, error, timeout, malformed, closed pipe,
  oversized output, unknown tool.
- Isolated real server: one read-only search.
- Corrupt-home variant: clear diagnostic, no crash, no data loss.
- Cancellation: request cancelled, child terminated, no success event.

## 10. Evidence

Save the command, home path (redacted if personal), result summary, and date.
Do not save full skill instructions or catalog contents.
