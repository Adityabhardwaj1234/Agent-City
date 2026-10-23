---
title: Test Plan
status: active
owner: qa
last_verified: 2026-10-23
---

# Test Plan

Tests exist to prevent false claims. A feature is not done because it compiles,
renders, or returns a happy-path response.

## 1. Layers

| Layer | Tool | Scope | Runs |
|---|---|---|---|
| Unit | pytest | Engine, policy, schemas, parsers, path guards | Every change |
| Contract | pytest | API, event, IPC, MCP schemas | Every change |
| Integration | pytest + httpx | SQLite, sidecar, MCP subprocess, artifacts | Every change |
| Component | Vitest + Testing Library | Renderer states, accessibility | Every UI change |
| End-to-end | Playwright | Launch, mission, approval, cancel, restart | M1 onward |
| Security | pytest + custom cases | Injection, approvals, paths, origin, budgets | Every security-relevant change |
| Agent evaluation | ADK eval + builder CLI | Tool trajectories and answer quality | M2 onward |
| Desktop smoke | Manual + fixture app | Capture, UIA, emergency stop | M4 |
| Packaging | Installer + clean profile | Launch, migration, uninstall | M6 |

## 2. Mandatory scenarios

### Launch and setup

- [ ] Clean launch with no provider key shows Offline Mode and a setup path.
- [ ] Sidecar failure is displayed with the log path and a retry action.
- [ ] Migration failure refuses to start and explains the version mismatch.
- [ ] Missing SkillBridge shows an actionable capability error.

### Missions

- [ ] Request produces a typed plan with dependencies, risk, budget, acceptance.
- [ ] Approval rejection prevents the gated action and records the reason.
- [ ] Pause stops scheduling; resume continues from the last checkpoint.
- [ ] Cancel during a running step stops it within the timeout.
- [ ] Failed worker marks the task failed and cannot yield a successful mission.
- [ ] Verifier rejection blocks completion and names missing evidence.
- [ ] Budget exhaustion stops execution and marks the mission blocked.
- [ ] Restart marks in-flight runs interrupted and resumes only idempotent steps.
- [ ] Duplicate event replay does not duplicate UI state.

### Events and storage

- [ ] Events persist before the UI receives them.
- [ ] Sequence is monotonic per mission with no gaps after rollback.
- [ ] Reconnect from a cursor replays exactly the missed events.
- [ ] Artifact provenance links to mission, task, run, and tool invocation.
- [ ] Path traversal, symlink, junction, and UNC inputs are rejected.
- [ ] Database retention deletes what it claims and nothing else.

### SkillBridge and MCP

- [ ] Handshake and tool discovery succeed against an isolated home.
- [ ] A read-only search returns results within the timeout.
- [ ] Missing binary, crash, timeout, malformed JSON, and unknown tool are handled.
- [ ] A corrupt catalog produces a clear diagnostic and does not crash the app.
- [ ] Tool output containing instructions cannot alter policy or permissions.
- [ ] Cancel propagates to the MCP request and kills a hung child.

### Desktop and voice

- [ ] Capture is off until consent; indicator appears immediately on grant.
- [ ] Revoking consent stops capture and queued actions.
- [ ] Out-of-scope window and stale observation are denied.
- [ ] Action batch triggers a fresh observation and result check.
- [ ] Emergency stop halts queued and in-flight actions.
- [ ] Missing microphone, denied permission, and provider failure degrade cleanly.
- [ ] Voice transcript alone cannot approve a consequential action.
- [ ] Wake word is off by default and visibly indicated when enabled.

### Security

- [ ] Prompt injection in a web page, document, skill, screenshot OCR, and tool
      output cannot grant permission or change system rules.
- [ ] Forged, expired, replayed, and cross-mission approval tokens are rejected.
- [ ] Non-loopback bind is refused; missing or wrong token is rejected.
- [ ] Origin and custom-header checks reject browser-origin attacks.
- [ ] Shell arguments are passed as arrays; injection strings remain literals.
- [ ] Tool input and output size limits are enforced.
- [ ] Secrets never appear in logs, errors, fixtures, or test snapshots.
- [ ] Repeated failures hit a circuit breaker instead of a retry loop.
- [ ] Child agent explosion is capped by depth and concurrency limits.

### Performance and reliability

- [ ] Idle memory stays under the budget; active memory is measured.
- [ ] UI remains responsive during a long tool call.
- [ ] Event and log buffers are bounded and prune correctly.
- [ ] Provider 429, timeout, malformed response, and disconnect are handled.
- [ ] Crash mid-mission recovers to a truthful state.

## 3. Fixtures and isolation

| Fixture | Rule |
|---|---|
| App home | Temporary directory per test; never `%LOCALAPPDATA%\AgentCity` |
| SkillBridge home | Temporary directory; never `~/.skillbridge` |
| Provider | Fake model by default; live only behind an explicit env flag |
| Desktop | Notepad or a controlled test window; never sensitive apps |
| Filesystem | Temp project root with generated files |
| Time | Injectable clock for expiry and retention tests |
| Network | Blocked in unit tests; mocked at the adapter boundary |

## 4. Agent evaluation

Use the ADK evaluation format and the Agent Builder's `eval` command. Datasets
must cover:

1. Simple read-only question with no tools.
2. SkillBridge read-only lookup.
3. Research with required citations.
4. Sequential multi-step mission.
5. Independent tasks that should run in parallel.
6. Ambiguous request that should ask or choose Plan mode.
7. Prompt injection in retrieved content.
8. Attempted unapproved desktop action.
9. Worker failure requiring escalation.
10. Action requiring human approval.
11. Budget exhaustion.
12. Cancellation and resume recovery.
13. Missing provider or credential.
14. Report generation with verifiable artifacts.

Score trajectory correctness, task completion, policy correctness, citation
provenance, and resource limits. A good final answer with the wrong tool path is
a failure.

## 5. Evidence and reporting

For every run capture:

- exact command and working directory;
- exit code and duration;
- pass/fail/skip counts and failing names;
- environment mode (offline or live) and provider;
- artifact paths;
- any check that was mocked or blocked.

Write to `docs/agentcity/evidence/<date>-<check>/` and summarize in
`release-verification.md`. Never report “all tests passed” when tests were
skipped, mocked, or never run.

## 6. Commands (as milestones land)

```powershell
uv run pytest
uv run pytest -m security
npm test -w src/desktop
npm run e2e -w src/desktop
python -m adk_agent_builder.cli test --project-dir src/backend/agentcity/agents/generated
python -m adk_agent_builder.cli eval --project-dir src/backend/agentcity/agents/generated --output docs/agentcity/evidence/adk-eval.json
python scripts/check-docs.py
```

Until a command exists, it is marked `planned` in the manifest. Do not run or
cite a command that has not been implemented.

## 7. Quarantine and flaky tests

- A flaky test is quarantined with an owner, a reason, and an expiry date.
- Quarantined tests do not count as passing evidence.
- Security tests are never quarantined; fix or block the feature.
