---
title: Change Recipes
status: active
owner: engineering
last_verified: 2026-10-23
---

# Change Recipes

Exact checklists for common changes. Follow the recipe so a fresh agent does not
have to rediscover the wiring. Paths marked (M1) are the planned layout.

## 1. Add an API endpoint

**Files**

- `src/backend/agentcity/api/routes/<area>.py` — route handler.
- `src/backend/agentcity/api/app.py` — register the router.
- `src/backend/agentcity/schemas/<area>.py` — request/response models.
- `src/backend/tests/integration/test_<area>_api.py` — tests.
- `docs/architecture/contracts.md` — endpoint table and schema.
- `docs/PROJECT_MANIFEST.json` — only if a command or feature status changes.

**Steps**

1. Define Pydantic request and response models. Bound sizes and validate enums.
2. Add the handler; keep business logic in a service, not the route.
3. Require auth and the client header for mutations.
4. Add a typed error mapping with a stable code.
5. Register the router.
6. Test success, validation failure, unauthorized, forbidden origin, and the
   service error path.
7. Update the contract table.

**Done when** the route is documented, authorized, typed, tested, and returns a
`trace_id` on errors.

## 2. Add an SSE event type

**Files**

- `src/backend/agentcity/events/types.py` — payload model and type string.
- `src/backend/agentcity/events/ledger.py` — append helper if needed.
- `src/backend/agentcity/engine/*` — emit inside the state transaction.
- `src/backend/tests/unit/test_event_ledger.py` — ordering and replay.
- `src/desktop/src/lib/events.ts` — client union and reducer.
- `docs/architecture/contracts.md` — event family table.

**Steps**

1. Add the dotted type and a versioned payload model.
2. Decide visibility (`user`, `debug`, `audit`) and risk metadata.
3. Emit it in the same transaction as the state change.
4. Extend the client union; handle unknown types by ignoring them.
5. Ensure replay and dedupe still work.
6. Test: event written once, sequence monotonic, replay from cursor, UI reducer
   handles duplicates.

## 3. Add a database migration

**Files**

- `src/backend/agentcity/db/migrations/NNNN_<name>.sql`.
- `src/backend/agentcity/db/repositories/<area>.py`.
- `docs/architecture/data-model.md`.
- Tests for fresh migration and upgrade from the previous schema.

**Steps**

1. Pick the next number; never reuse or edit an applied migration.
2. Write forward SQL only. Add a separate note for rollback if needed.
3. Update repository code and models.
4. Add a backup step if the migration is destructive.
5. Test from zero and from the previous fixture schema.
6. Record the schema version in the manifest if it is externally visible.

## 4. Add a UI route

**Files**

- `src/desktop/src/features/<name>/<Name>Page.tsx`.
- `src/desktop/src/app/router.tsx`.
- `src/desktop/src/features/<name>/components/*`.
- `src/desktop/src/features/<name>/*.test.tsx`.
- `docs/agentcity/PRD.md` — only if the workspace scope changes.
- `docs/repo-map.md` — regenerate.

**Steps**

1. Add the route with a lazy import.
2. Implement loading, empty, error, blocked, and ready states.
3. Wire real API data; no fixture values in real mode.
4. Add keyboard navigation and focus behavior.
5. Add the navigation entry with an accessible label.
6. Test each state and the primary interaction.
7. Check the 1100 × 700 layout and 125% scaling.

## 5. Add or change an ADK agent

**Files**

- `src/backend/agentcity/agents/definitions/<agent>.py`.
- `src/backend/agentcity/agents/runner.py` — registration if needed.
- `docs/agentcity/agent-roster.md`.
- `docs/agentcity/model-routing.md` — if the model policy changes.
- Eval set under `src/backend/tests/evaluation/`.

**Steps**

1. Write the task contract: objective, inputs, outputs, tools, budget, failure
   modes.
2. Define the agent with a typed output model and a narrow tool list.
3. Run the Agent Builder `validate` and `test` commands on the generated
   project.
4. Add trajectory eval cases, including a refusal/injection case.
5. Register the agent; ensure it cannot bypass the policy broker.
6. Update the roster and model routing.
7. Record the eval report in evidence.

**Never** let an agent decide its own permissions or spawn unbounded children.

## 6. Add a local capability (tool)

**Files**

- `src/backend/agentcity/capabilities/local_tools.py`.
- `src/backend/agentcity/policy/risk.py` — risk classification.
- `src/backend/tests/security/test_<tool>.py`.
- `docs/agentcity/security-model.md` — if a new risk class behavior appears.
- `docs/architecture/contracts.md` — capability schema.

**Steps**

1. Define the input/output schema and the risk class.
2. Implement with path guard, timeouts, and output caps.
3. Register it with a stable id and description.
4. Add policy tests: allowed, denied, out of scope, oversized input.
5. Add an audit event on every invocation.
6. Expose a safe test action only if it is read-only.

## 7. Map a SkillBridge / MCP capability

**Files**

- `src/backend/agentcity/capabilities/skillbridge.py` — tool mapping.
- `src/backend/agentcity/capabilities/registry.py` — capability record.
- Tests with a fake MCP server.
- `docs/runbooks/mcp-and-skills.md`.

**Steps**

1. Discover the tool and schema from the live broker; do not guess.
2. Assign a capability id and risk class. Unknown tools are `blocked`.
3. Add argument validation and output size limits.
4. Add timeout, cancellation, and one-restart behavior.
5. Test: success, error result, timeout, malformed JSON, closed pipe, oversized
   output, unknown tool.
6. Confirm no tool output can change policy.

## 8. Add a desktop action

**Files**

- `src/backend/agentcity/desktop/service.py`.
- `src/backend/agentcity/desktop/grants.py`.
- `src/backend/agentcity/policy/risk.py`.
- Tests against Notepad or a fixture window.
- `docs/runbooks/desktop-permissions.md`.

**Steps**

1. Classify the action (`read_only` to `consequential`).
2. Require a grant with scope and duration.
3. Validate the target window and take a fresh observation.
4. Execute with a timeout and a stop check between actions.
5. Take a fresh observation and verify the expected result.
6. Record the observation timestamp, target, actions, and outcome.
7. Test denial paths: no grant, expired grant, stale observation, wrong window,
   emergency stop.

## 9. Add a voice adapter

**Files**

- `src/backend/agentcity/voice/stt.py` or `tts.py`.
- `src/backend/agentcity/core/config.py`.
- `src/desktop/src/features/command/voice/*`.
- `docs/runbooks/voice.md`.

**Steps**

1. Define the interface (start, stream, cancel, error).
2. Implement the adapter with timeouts and a device-error path.
3. Keep the transcript editable; never auto-submit.
4. Add a visible mic/transmission indicator.
5. Support barge-in and stop.
6. Test missing device, denied permission, provider failure, and interruption.
7. Confirm a transcript cannot approve a consequential action.

## 10. Add a test or evaluation case

**Files**

- `src/backend/tests/<layer>/test_<name>.py` or the eval dataset.
- `docs/agentcity/test-plan.md` if it is a new scenario class.
- Evidence under `docs/agentcity/evidence/`.

**Steps**

1. State the behavior and the failure it prevents.
2. Use the smallest fixture; never the real app home or catalog.
3. Assert persisted state and events, not only return values.
4. Make it deterministic; no sleeps for synchronization.
5. Mark live tests and skip by default.
6. Run it, capture the command and result.

## 11. Change a model or provider

**Files**

- `src/backend/agentcity/core/config.py`.
- `src/backend/agentcity/agents/runner.py`.
- `docs/agentcity/model-routing.md`.
- `docs/PROJECT_MANIFEST.json` environment section.
- Health check and quota tests.

**Steps**

1. Verify the model exists in the installed SDK/provider.
2. Check capability fit (tools, structured output, vision, context).
3. Add a health check and a blocked state for missing credentials.
4. Update routing, fallbacks, and the usage label policy.
5. Run offline tests, then a paced live smoke test.
6. Record results and any quota limits observed.
7. Never silently switch providers mid-mission.

## 12. Package a release

**Files**

- `src/desktop/package.json`, electron-builder config.
- `scripts/package.ps1` (when created).
- `docs/runbooks/packaging.md`.
- `docs/agentcity/release-verification.md`.

**Steps**

1. Freeze the version and update `PROJECT_MANIFEST.json`.
2. Run the full test matrix and save evidence.
3. Build the renderer, main, and sidecar artifacts.
4. Sign the installer if a certificate is configured; otherwise label unsigned.
5. Test on a clean Windows profile: install, launch, migrate, uninstall.
6. Verify no secrets, logs, databases, or source maps leak into the package.
7. Write the release report with pass/fail/skip/blocked and known issues.
8. Tag only when critical checks pass.

## 13. Documentation-only change

1. Edit the canonical doc, not a copy.
2. Update `last_verified`.
3. Run `python scripts/check-docs.py`.
4. If status or paths changed, update the manifest and run
   `python scripts/generate-context.py`.
5. Commit with `docs(scope): ...`.

## 14. Any change: final checklist

- [ ] Tests run, evidence saved, mode labeled.
- [ ] Contracts, data model, and manifest updated.
- [ ] `check-docs.py` passes.
- [ ] No secrets, runtime data, or `src/skills` changes staged.
- [ ] Commit message explains why.
- [ ] No dead controls or fake data.
