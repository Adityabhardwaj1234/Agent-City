# Release Verification: v<version>

- **Date:**
- **Commit SHA:**
- **Base commit:**
- **Branch:**
- **Provider mode:** offline | mocked | live
- **Installer:**

## Result summary

| Suite | Command | Result | Counts | Evidence |
|---|---|---|---|---|
| Docs | `python scripts/check-docs.py` | | | |
| Python unit/contract | `uv run pytest -m "not live"` | | | |
| Integration | `uv run pytest tests/integration` | | | |
| Security | `uv run pytest -m security` | | | |
| Frontend | `npm test -w src/desktop` | | | |
| E2E | `npm run e2e -w src/desktop` | | | |
| ADK offline eval | builder `eval` | | | |
| ADK live eval | paced slice | | | |
| Packaging | installer smoke test | | | |

Counts are passed / failed / skipped / blocked. “Passed” requires a real run.

## Environment

- Windows version:
- Python / Node:
- google-adk / MCP:
- RAM / disk:
- Provider and quota state:
- SkillBridge mode and home:
- Installer signing:

## Integrations

| Integration | State | Evidence | Notes |
|---|---|---|---|
| ADK runtime | | | |
| ADK Agent Builder | | | |
| SkillBridge MCP | | | |
| Gemini provider | | | |
| Desktop capture | | | |
| Voice | | | |
| Coding CLI adapter | | | |

## Performance

| Metric | Budget | Measured | Result |
|---|---:|---:|---|
| Idle total memory | 600 MB | | |
| Sidecar idle | 250 MB | | |
| Cold start | 5 s | | |
| Sidecar ready | 3 s | | |

## Security and license

- Security suite result:
- Dependency scan:
- Secret scan:
- License/notice review:
- Known exceptions:

## Known issues

| Severity | Issue | Repro | Status |
|---|---|---|---|
| | | | |

## Blocked or unrun work

List every check that could not run, why, and what the user must configure.

## Attestation

I verified that this report matches the commands and evidence in this release
directory. Screenshots were supplemental only. No result was edited to pass.

- Verifier:
- Date:
