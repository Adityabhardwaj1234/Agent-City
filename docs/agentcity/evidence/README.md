---
title: Evidence Index
status: active
owner: qa
last_verified: 2026-10-23
---

# Evidence Index

Evidence is how AgentCity avoids confident fiction. Every claim of a passing
check points to a file here.

## Naming

```text
YYYY-MM-DD-<check>[-<variant>].<ext>
```

Examples:

- `2026-10-23-adk-builder-doctor.json`
- `2026-10-23-skillbridge-isolated-search.json`
- `2026-10-23-skillbridge-integrity.txt`
- `2026-10-24-backend-pytest.txt`
- `2026-10-25-e2e-launch/` (directory with report and screenshots)

## Required metadata

Text evidence starts with:

```text
command: <exact command>
cwd: <working directory>
exit_code: <number>
mode: offline | live | mocked
provider: none | gemini | ...
started_at: <ISO-8601>
duration_seconds: <number>
result: passed | failed | skipped | blocked
notes: <short>
```

Tool-generated JSON is stored as-is, with a sibling `.meta.txt` containing the
command and context when the JSON has no envelope.

## Status vocabulary

| Status | Meaning |
|---|---|
| `passed` | Command ran and met the stated criteria |
| `failed` | Command ran and did not meet criteria |
| `skipped` | Intentionally not run, with a reason |
| `blocked` | Cannot run because a credential, permission, or dependency is absent |
| `mocked` | Ran against a fake provider or adapter; proves wiring, not live behavior |

## Current evidence

| File | Claim | Result |
|---|---|---|
| `2026-10-23-tool-pins.txt` | Both tool clones exist at the pinned commits and import | passed |
| `2026-10-23-docs-check.txt` | Documentation pack passes the checker | passed (60 files) |
| `2026-10-23-fresh-user-docs-test.md` | A new contributor can follow the README M0 setup | passed after fixes (round 2 go) |
| `2026-10-23-adk-builder-doctor.json` | ADK Agent Builder CLI runs and reports environment | passed (fallback mode, optional tools absent) |
| `2026-10-23-skillbridge-isolated-search.json` | SkillBridge MCP package works from an isolated home | passed (read-only search; metadata in `.meta.txt`) |
| `2026-10-23-skillbridge-corrupt-open.txt` | Opening the real production catalog fails safely | failed as expected (malformed database; no quarantine created) |
| `2026-10-23-skillbridge-integrity.txt` | Production catalog integrity | failed (corrupt, 91 findings) |

## Rules

- Never edit a captured result to make it pass. Re-run and add a new file.
- Redact secrets and personal data before saving.
- Keep screenshots supplemental; a screenshot is not proof of behavior.
- Link evidence from the manifest, acceptance table, or release report.
- Delete stale evidence only when the corresponding claim is removed.
