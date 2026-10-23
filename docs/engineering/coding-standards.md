---
title: Coding Standards
status: active
owner: engineering
last_verified: 2026-10-23
---

# Coding Standards

These rules apply to all AgentCity code. They exist so multiple agents and
humans can work in the same tree without producing an unreviewable mess.

## 1. Baseline

| Area | Rule |
|---|---|
| Python | 3.12+, `src`-layout, 4-space indent, 100-column lines |
| Python tooling | `ruff` (lint + format), `mypy` (types), `pytest` (tests) — added in M1 |
| TypeScript | `strict: true`, `noUncheckedIndexedAccess`, 2-space indent |
| TypeScript tooling | `tsc --noEmit`, ESLint, Vitest — added in M1 |
| Encoding | UTF-8, LF, final newline |
| Dependency policy | Pin exact versions in lockfiles; no floating tags |
| Commit policy | Conventional Commits, one logical change |

Do not claim a tool is configured before it exists in the repository. Until M1
adds `pyproject.toml` and `package.json`, the documentation describes the
target, not a working setup.

## 2. Python conventions

### Structure

- Public functions and methods have full type hints. No `Any` at a module
  boundary; use a precise model or `object` with a validator.
- Pydantic v2 models at every external boundary: API, events, tool inputs and
  outputs, LLM structured output.
- Internal data may use dataclasses when validation is not needed.
- Use `enum.StrEnum` for closed sets; reject unknown values explicitly.
- Modules stay under ~400 lines. Split by responsibility, not by layer names
  like `utils.py`.
- No mutable module-level state except an explicit, documented registry.

### Naming

| Thing | Convention | Example |
|---|---|---|
| Module | snake_case | `mission_engine.py` |
| Class | PascalCase | `MissionEngine` |
| Function | snake_case, verb first | `create_mission` |
| Constant | UPPER_SNAKE | `MAX_DEPTH` |
| ID | prefix + ULID | `mis_01J...` |
| Event type | dotted lower | `tool.succeeded` |
| Risk class | lower snake | `state_change` |

### Errors

- Define a small exception hierarchy with a stable `code`.
- Never `except Exception: pass`. Catch the narrowest type, log context, and
  either recover or convert to a typed error.
- API errors use the problem shape in `docs/architecture/contracts.md`.
- Do not leak stack traces, paths, or provider payloads to the UI.
- A blocked dependency is not an exception to swallow; it is a product state.

### Logging

Structured JSON, one event per line:

```json
{"ts":"2026-10-23T12:00:00.123Z","level":"info","event":"tool.succeeded","mission_id":"mis_01J...","run_id":"run_01J...","task_id":"tsk_01J...","capability":"skillbridge.search_skills","duration_ms":412,"trace_id":"trc_01J..."}
```

- Include identifiers when known.
- Redact secrets, tokens, full prompts, and sensitive paths.
- Never log request bodies wholesale.
- Use `trace_id` to correlate API request, engine step, and tool call.

### Async and concurrency

- Every external call has an explicit timeout.
- Every long operation accepts a cancellation signal.
- No unbounded `asyncio.create_task`; use a task registry with done callbacks.
- No blocking calls in the event loop; use `asyncio.to_thread` or a process.
- Prefer bounded queues and worker pools with a documented size.
- Cancellation must propagate; a cancelled task never writes a success event.

### Data and SQL

- Parameterized queries only. No string interpolation into SQL.
- State transition and event append share one transaction.
- Write transactions use `BEGIN IMMEDIATE`; reads use a separate connection.
- Timestamps are UTC ISO-8601 with milliseconds.
- Never store secrets in the database; store a credential reference.
- Validate paths with a single shared guard, not ad hoc checks.

### Tests

- Every bug fix starts with a failing test.
- Use fixtures for temp homes, clocks, fake providers, and fake MCP servers.
- No test may touch the real app home or the real SkillBridge catalog.
- Tests are deterministic; no sleeps for synchronization, use events.
- Mark live/provider tests explicitly and skip them by default.

## 3. TypeScript and React conventions

- `strict` on; no `any`; no non-null assertions without a comment explaining
  the invariant.
- Validate every external payload (HTTP, SSE, IPC) at the boundary with a schema
  parser. Do not trust `as`.
- Discriminated unions for state: `{status:"loading"} | {status:"ready",data} |
  {status:"error",error}`.
- Components are small and named by what they render. No 500-line route files.
- Side effects live in hooks or a store, not in render bodies.
- No `useEffect` for derived state; compute it.
- Keys must be stable IDs, never array indices for reorderable lists.
- Accessibility is part of the component, not a later pass: labels, roles,
  focus management, keyboard paths.
- Never render a button whose handler is a TODO. Disable it with a reason or do
  not render it.

### State and data

- Server state comes from the API; do not duplicate it in a second store.
- The event stream updates one normalized mission store; components subscribe
  with selectors.
- Optimistic updates are allowed only for reversible local UI state, never for
  mission status or approvals.
- Errors are typed and displayed with a retry path where meaningful.

## 4. Visual and UX rules

- Dark graphite/ink base with restrained cyan/teal for active systems, amber
  for approvals, green for verified success, red for faults.
- Never encode state with color alone; pair with text, icon, and shape.
- Motion communicates a real event. No perpetual decorative animation.
- Respect `prefers-reduced-motion`.
- Every view has loading, empty, error, and blocked states.
- Tables and lists are first-class; the map is an additional view, not the only
  way to read the system.
- Minimum supported window: 1100 × 700; test at 100% and 125% scaling.

## 5. Comments and documentation

- Comments explain **why**, not what the code does.
- Public modules have a short docstring stating responsibility and boundaries.
- `TODO` must include an owner and an issue reference; otherwise it is noise.
- A behavior change updates the relevant doc in the same commit.
- Every new event type, error code, risk class, and endpoint is added to
  `docs/architecture/contracts.md`.

## 6. Prohibited patterns

- Bare `except`, swallowed promise rejections, empty catch blocks.
- `eval`, `exec`, dynamic import of user input, or shell string concatenation.
- `shell=True` with interpolated values.
- Sleeping to wait for a process; use exit events and timeouts.
- Silent fallback from Live to Offline mode.
- Fake latency, fake progress, fake agent activity, or fabricated costs.
- Global mutable singletons for mission state.
- Reading the API token from a renderer-accessible file.
- Storing secrets in SQLite, localStorage, or fixtures.
- Editing `src/skills/**` to make our code work.

## 7. Review checklist

- [ ] Does it solve the stated problem without unrelated changes?
- [ ] Are boundaries typed and validated?
- [ ] Are failure, cancellation, and timeout paths handled?
- [ ] Is policy enforced in code, not in a prompt?
- [ ] Are secrets and paths redacted?
- [ ] Are tests meaningful and deterministic?
- [ ] Are docs and contracts updated?
- [ ] Is every visible control real?
- [ ] Does it respect the memory and concurrency budget?
