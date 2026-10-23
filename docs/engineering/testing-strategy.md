---
title: Testing Strategy
status: active
owner: qa
last_verified: 2026-10-23
---

# Testing Strategy

The scenario catalog is in `docs/agentcity/test-plan.md`. This document covers
how tests are built, isolated, and run.

## 1. Test pyramid

```text
many      unit tests          engine, policy, schemas, parsers, guards
some      contract tests      API, SSE, IPC, MCP, event envelopes
some      integration tests   SQLite, sidecar, artifacts, subprocesses
fewer     component tests     renderer states and keyboard paths
few       E2E tests           launch, mission, approval, cancel, restart
few       agent evaluations   trajectories and answer quality
```

Security tests cut across every layer and are never quarantined.

## 2. Python tests

- Framework: pytest, `asyncio_mode=auto`.
- Layout: `src/backend/tests/{unit,integration,security,evaluation}`.
- Fixtures: `tmp_path` app home, temp SkillBridge home, fake clock, fake IDs,
  fake provider, fake MCP server, temp project root.
- No network in unit tests. Provider and MCP clients are injected.
- Live tests are marked `@pytest.mark.live` and skipped by default.
- Use `pytest-timeout` for every test that can hang; default 30 s, tools 10 s.
- Assert on persisted state and events, not only return values.
- For cancellation, assert that no success event was written.

### Minimum fixtures

| Fixture | Guarantees |
|---|---|
| `app_home` | Isolated data dir; never the real `%LOCALAPPDATA%` |
| `db` | Migrated SQLite in WAL mode, cleaned up |
| `skillbridge_home` | Isolated catalog; includes a corrupt-DB variant |
| `fake_llm` | Deterministic plans and tool calls; records requests |
| `fake_mcp` | Scriptable responses, delays, malformed payloads, crashes |
| `clock` | Frozen/injectable time for expiry and retention |
| `project_root` | Temp files with symlink and traversal cases |

## 3. Frontend tests

- Vitest + Testing Library for components and the event store.
- Test four states for every data view: loading, empty, error, blocked.
- Test keyboard navigation for navigation, approvals, and stop.
- Test event ordering, duplicate delivery, and reconnect.
- Playwright for the real shell: launch, mission, approval, cancel, restart.
- No screenshot-only assertions for status correctness.

## 4. Contract tests

- API responses validate against the documented schemas.
- Event payloads validate against `schema_version` and required fields.
- IPC channels reject malformed payloads and unknown channels.
- MCP client handles: valid result, error result, timeout, malformed JSON,
  closed pipe, unknown tool, oversized output.
- Contracts and clients change in the same commit.

## 5. Agent evaluation

- Use ADK eval sets and the Agent Builder `eval` command.
- Trajectory correctness is scored separately from answer quality.
- Offline and live evaluation results are stored separately and labeled.
- The 14 scenarios in the test plan are the minimum dataset.
- A prompt or tool change re-runs the affected trajectory cases.

## 6. Determinism rules

- No `sleep` for synchronization; use events, condition variables, or timeouts.
- Freeze time for expiry, retention, and scheduling tests.
- Fake ULIDs or assert prefixes and uniqueness, not exact values.
- Avoid real filesystem timestamps in assertions.
- A flaky test is quarantined with an owner and expiry date; it is not evidence.

## 7. Commands (as milestones land)

```powershell
uv run pytest
uv run pytest -m "not live"
uv run pytest -m security
uv run pytest --timeout=30
npm test -w src/desktop
npm run e2e -w src/desktop
python -m adk_agent_builder.cli test --project-dir src/backend/agentcity/agents/generated
python -m adk_agent_builder.cli eval --project-dir src/backend/agentcity/agents/generated --output docs/agentcity/evidence/adk-eval.json
python scripts/check-docs.py
```

Report the exact command, exit code, counts, and mode. A skipped or mocked test
is not a pass.

## 8. CI shape (later)

```text
job 1: docs check + manifest consistency
job 2: python lint, type check, unit + contract tests
job 3: integration tests with fake MCP and temp homes
job 4: frontend type check, lint, component tests
job 5: E2E on a packaged or dev shell (serial, low concurrency)
job 6: security tests (never allowed to fail)
```

No job may require a provider key except the explicit, manually triggered live
evaluation job. That job records quota usage and is allowed to be blocked.
