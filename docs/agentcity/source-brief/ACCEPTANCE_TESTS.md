# AgentCity — Acceptance and Verification Plan

## 1. Release gate

The project is not called production-ready or “perfect” just because it compiles. Release requires all critical tests to pass, all non-passing checks to be explicitly listed, the packaged app to launch on Windows, and the user-facing product to distinguish working features from setup-required integrations.

## 2. Core functional checks

### Launch and setup
- [ ] Clean local launch opens a usable window and health status.
- [ ] App works with no provider configured and clearly guides setup rather than crashing.
- [ ] Setup checks versions/dependencies and never silently overwrites existing Python/Node versions.
- [ ] Backend startup failure is shown with actionable logs and retry/diagnostics.

### Chat and projects
- [ ] New, rename, search, pin/archive, and reopen conversation work across restart.
- [ ] Streaming output can be cancelled.
- [ ] Project-specific sources do not leak into other projects unless explicitly enabled.
- [ ] File upload validates allowed types/size and survives malformed inputs.
- [ ] Source-backed answers show the citation/provenance, not invented references.

### ADK orchestration
- [ ] User request generates a typed plan with steps, dependencies, risk, budget, and acceptance condition.
- [ ] Agent Builder integration is actually invoked or explicitly marked unavailable; no fake successful invocation.
- [ ] ADK agent config/definitions are source controlled and tests prove the intended agents load.
- [ ] Sequential and parallel workflow paths each have tests.
- [ ] Tool call sequence matches an expected trajectory for deterministic eval cases.
- [ ] One failed worker is surfaced as failed/blocked and cannot silently make the parent mission successful.
- [ ] Bounded agent spawning, recursion depth, concurrency, duration, and tool limits are enforced.

### Skills Bridge / MCP
- [ ] Exact Skills Bridge server and tool schemas were discovered from live registration/configuration.
- [ ] A real harmless read-only tool call succeeds when the configured server is available.
- [ ] Disconnected, timeout, malformed result, invalid input, cancellation, and reconnect cases are tested.
- [ ] Tool result text that contains instructions cannot alter system permissions or policy.
- [ ] User can see which tool was invoked, the risk class, outcome, and redacted result.

### Missions and observability
- [ ] Event timeline derives from persisted backend events.
- [ ] Reconnecting UI catches up from the last sequence cursor without duplicate/out-of-order display.
- [ ] Pause/resume/cancel updates real run state and cancels downstream operations.
- [ ] Restart recovers state; interrupted non-idempotent steps are not blindly replayed.
- [ ] Every artifact links to its producing mission/run/agent.
- [ ] Agent status is based on real run lifecycle/heartbeat, not UI animation.
- [ ] Usage/cost fields are provider reported or visibly estimates; unavailable data is not fabricated.

### Desktop control
- [ ] Screen capture is off until consent and shows a persistent visible state when active.
- [ ] Default mode is one-shot/on-demand, not hidden continuous screen watching.
- [ ] Agent can identify the current target window/snapshot timestamp.
- [ ] Desktop actions are denied outside permission scope.
- [ ] An action batch triggers a fresh observation and checks expected result.
- [ ] Emergency cancel halts queued and future actions.
- [ ] Destructive file actions and sensitive external submissions require approval.
- [ ] UI Automation unavailable/permission denied is reported and safe fallback is tested.
- [ ] Tests run against a controlled test window/app, never against real sensitive apps.

### Voice
- [ ] Push-to-talk sends audio to the selected STT/live provider or selected local engine.
- [ ] Mic activity/transmission indicator is accurate; user can stop immediately.
- [ ] Voice response can be interrupted; cancelled speech is not resumed unexpectedly.
- [ ] Failure from absent microphone, denied permission, provider error, or network loss is graceful.
- [ ] A voice transcript alone is not accepted as confirmation for high-risk actions.
- [ ] Wake word is opt-in, visible, and off by default in a fresh install.

### Agents and coding adapters
- [ ] Team template creates agents with explicit scopes, tools, and budgets.
- [ ] Coding agent receives its actual branch/worktree path and reports changed files plus test outcome.
- [ ] Integration checks verify the worker's directory/branch rather than trusting its self-report.
- [ ] Missing coding CLI is labeled unavailable; no shell command silently installs one without permission.
- [ ] No provider limits/auth restrictions are bypassed.

### Privacy, settings, and artifacts
- [ ] API credentials never appear in logs, UI, test snapshots, or checked-in files.
- [ ] User can inspect, edit, disable, and delete memory records.
- [ ] Telemetry/cloud sync remain off unless expressly enabled.
- [ ] Artifact paths remain under app-owned or user-approved locations.
- [ ] Path traversal, symlink escape, and archive extraction attempts are rejected.
- [ ] Data retention and screenshot deletion are honored.

## 3. Security tests

- [ ] Prompt injection in web page, document, screenshot text, terminal output, and Skill description.
- [ ] Forged or stale approval token; approval replay; cross-mission approval confusion.
- [ ] Localhost API origin/CSRF/auth checks; non-loopback bind disabled by default.
- [ ] Shell argument injection and unsafe environment inheritance.
- [ ] Tool argument schema and output-size limits.
- [ ] Secrets redaction and error logging test.
- [ ] Unauthorized path, symlink, traversal, and directory enumeration tests.
- [ ] Mission budget overflow, repeated error loop, child-worker explosion, and stuck action timeout.
- [ ] Dependency/license scan and audit of bundled model/speech assets.

## 4. Reliability and performance checks

- [ ] Cancel during model streaming, tool invocation, subagent run, and desktop action.
- [ ] Simulate API timeout, 429/rate limit, malformed response, disconnect, and provider fallback.
- [ ] Simulate process crash mid-mission and verify safe recovery.
- [ ] Measure idle and active memory/CPU; avoid starting several local models by default.
- [ ] UI remains responsive while tool calls and agent runs execute.
- [ ] Event and log buffers are bounded; old logs can be pruned using configured retention.
- [ ] Packaged Windows app launches on a clean environment with documented prerequisites.

## 5. Automated agent-evaluation dataset

Create scenario cases for:
1. simple read-only question with no tools;
2. task that requires Skills Bridge read-only lookup;
3. research task with citation requirements;
4. a multi-step mission with sequential dependencies;
5. independent tasks that should run in parallel;
6. ambiguous task that should ask for clarification or choose Plan mode;
7. prompt injection in retrieved content;
8. attempted dangerous/unapproved desktop action;
9. worker failure that requires recovery/escalation;
10. action requiring human approval;
11. budget exhaustion;
12. cancellation/resume recovery;
13. unsupported provider/credential absence;
14. report generation with verifiable artifacts.

Store expected tool trajectories, required permissions, acceptable output rubric, and known failure reasons. Use ADK's supported evaluation tooling where possible. At minimum track tool-trajectory correctness, task-completion criteria, policy/approval correctness, citation/provenance correctness, and time/cost/resource limits.

## 6. Reporting format

At final validation, produce `docs/agentcity/release-verification.md` including:
- commit SHA and base commit;
- build commands and exit codes;
- test suite counts (pass/fail/skip), failing case names, and concise evidence;
- ADK eval score/results and scenarios not run;
- UI screenshots as optional supplemental evidence, not sole proof;
- security/license review summary;
- real integrations, unconfigured integrations, mocked paths, and blocked work;
- known issues and exact repro steps;
- installer/launch smoke-test environment and outcome.

Never claim all tests passed if some were skipped, mocked, or dependent on unavailable credentials.
