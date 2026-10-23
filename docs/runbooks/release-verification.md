---
title: Release Verification Runbook
status: active
owner: release
last_verified: 2026-10-23
---

# Release Verification Runbook

A release is a claim. This runbook makes the claim falsifiable.

## 1. Gate

Do not tag or publish when any of these is true:

- a critical security test fails;
- a claimed feature has no evidence;
- the packaged app fails to launch on a clean profile;
- docs contradict the implementation;
- live and offline results are mixed without labels;
- a dependency or license obligation is unresolved;
- a required test is skipped without a recorded reason.

## 2. Before running

1. Freeze the version in `docs/PROJECT_MANIFEST.json`.
2. Regenerate context:

   ```powershell
   python scripts/generate-context.py
   python scripts/check-docs.py
   ```

3. Clean the environment: stop dev servers, close the app, use a temp app home.
4. Confirm the provider mode for each suite (offline, mocked, live).
5. Confirm the Git SHA and branch.

## 3. Suites

| Suite | Command | Mode | Required |
|---|---|---|---|
| Docs | `python scripts/check-docs.py` | offline | yes |
| Python unit/contract | `uv run pytest -m "not live"` | offline | yes |
| Integration | `uv run pytest tests/integration` | offline | yes |
| Security | `uv run pytest -m security` | offline | yes |
| Frontend | `npm test -w src/desktop` | offline | yes |
| E2E | `npm run e2e -w src/desktop` | offline | yes for release |
| ADK offline eval | builder `test`/`eval` | offline | yes |
| ADK live eval | paced, small slice | live | optional/blocked |
| Packaging | installer + clean profile | offline | yes for release |

Commands are `planned` until the corresponding files exist. Do not report a
suite as passed if the command is not implemented.

## 4. Evidence layout

```text
docs/agentcity/evidence/<date>-release-<version>/
  docs-check.txt
  pytest.txt
  pytest-security.txt
  vitest.txt
  e2e/
  adk-eval.json
  adk-eval.md
  packaging.txt
  environment.json
  screenshots/            (supplemental only)
```

Each text file starts with the command, cwd, exit code, mode, timestamp, and
result. JSON from tools is stored as-is with a `.meta.txt` sibling.

## 5. Report

Create `docs/agentcity/release-verification.md` from
`docs/templates/release-verification.md`. It must include:

- version, commit SHA, base commit, date;
- build commands and exit codes;
- test counts: passed, failed, skipped, blocked;
- failing test names and concise evidence;
- ADK evaluation scores and scenarios not run;
- security and license review summary;
- real integrations, unconfigured integrations, mocked paths, blocked work;
- performance measurements against the budget;
- installer/launch smoke-test environment and outcome;
- known issues with exact reproduction steps.

Screenshots are supplemental, never the sole proof.

## 6. Status vocabulary

| Status | Meaning |
|---|---|
| passed | Ran and met the criteria |
| failed | Ran and did not meet the criteria |
| skipped | Not run, with a reason |
| mocked | Ran against a fake; proves wiring only |
| blocked | Cannot run due to a credential, permission, or dependency |

Never write “all tests passed” when any test is skipped, mocked, or blocked.

## 7. Sign-off checklist

- [ ] Every suite has a result and evidence path.
- [ ] Critical failures are fixed or the release is blocked.
- [ ] Non-critical issues are listed with severity and repro.
- [ ] The manifest and state-of-build match reality.
- [ ] README and runbooks match the build.
- [ ] The installer was tested on a clean profile.
- [ ] The license and notices are current.
- [ ] The report is committed before the tag.

## 8. Post-release

- Archive evidence with the tag.
- Record quota usage if live tests ran.
- Open follow-up issues for known limitations.
- Do not delete failed evidence; it is part of the record.
