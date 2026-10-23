---
title: Data Model
status: active
owner: architecture
last_verified: 2026-10-23
---

# Data Model

SQLite is the source of truth for missions and configuration. The artifact
store holds bytes; the database holds provenance. Everything is local.

## 1. Storage locations

| Data | Location | Retention |
|---|---|---|
| Database | `%LOCALAPPDATA%\AgentCity\agentcity.db` | Until user deletes |
| Artifacts | `%LOCALAPPDATA%\AgentCity\artifacts\<mission-id>\` | Configurable, default 90 days |
| Logs | `%LOCALAPPDATA%\AgentCity\logs\` | Default 14 days, size-capped |
| Screenshots | Artifact store only when explicitly saved | Default 7 days |
| Handshake | `%LOCALAPPDATA%\AgentCity\handshake.json` | Deleted on exit |
| Test data | Temp home per test run | Deleted by fixture |

The repository is never used for runtime data. Tests must never touch the real
`%LOCALAPPDATA%\AgentCity` directory.

## 2. Tables

### projects

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `prj_` prefix |
| name | TEXT NOT NULL | |
| root_path | TEXT NOT NULL | Resolved absolute path |
| allowed_paths | TEXT JSON | Additional approved roots |
| created_at / updated_at | TEXT ISO-8601 UTC | |

### conversations / messages

| Table | Key columns |
|---|---|
| conversations | id, project_id, title, pinned, archived, created_at, updated_at |
| messages | id, conversation_id, role, content, content_json, citations_json, model, token_usage_json, created_at |

Messages are append-only. Edits create a new revision row; the original is
retained for audit unless the user deletes the conversation.

### agents / team_templates

| Table | Key columns |
|---|---|
| agents | id, name, role, instructions, model_policy_json, allowed_tools_json, budget_json, enabled, created_at |
| team_templates | id, name, description, roster_json, policy_json, created_at, updated_at |

### missions

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `mis_` prefix |
| project_id | TEXT FK | Nullable for quick tasks |
| title / objective | TEXT | |
| mode | TEXT | ask, plan, execute_with_approval, autopilot_bounded |
| status | TEXT | Lifecycle enum |
| plan_json | TEXT JSON | Validated `MissionPlan` |
| budget_json | TEXT JSON | Hard limits |
| policy_json | TEXT JSON | Snapshot of effective policy |
| parent_mission_id | TEXT FK | Bounded delegation |
| depth | INTEGER | Max 2 by default |
| created_at / updated_at / started_at / ended_at | TEXT | |
| cancel_requested | INTEGER | 0/1 |

Indexes: `(status, created_at)`, `(project_id, created_at)`.

### mission_tasks

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `tsk_` prefix |
| mission_id | TEXT FK | |
| title / description | TEXT | |
| agent_id | TEXT | Planned owner |
| depends_on_json | TEXT JSON | Task ids |
| status | TEXT | queued, running, blocked, completed, failed, cancelled |
| risk | TEXT | Risk class |
| attempt | INTEGER | Starts at 1 |
| input_json / output_json | TEXT JSON | Contract-shaped |
| acceptance_json | TEXT JSON | Verifiable criteria |
| started_at / ended_at | TEXT | |

Index: `(mission_id, status)`.

### agent_runs

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `run_` prefix |
| mission_id / task_id / agent_id | TEXT | |
| status | TEXT | queued, running, completed, failed, cancelled, interrupted |
| model / provider | TEXT | |
| heartbeat_at | TEXT | Liveness, not success |
| token_usage_json / cost_estimate_json | TEXT JSON | Measured vs estimated flag |
| error_code / error_message | TEXT | Redacted |
| started_at / ended_at | TEXT | |

### events

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `evt_` prefix |
| mission_id | TEXT FK | |
| run_id / agent_id / task_id | TEXT | Nullable |
| sequence | INTEGER | Unique per mission |
| type | TEXT | Dotted event type |
| schema_version | INTEGER | |
| visibility | TEXT | user, debug, audit |
| risk | TEXT | |
| payload_json | TEXT JSON | Redacted |
| created_at | TEXT | UTC with milliseconds |

Unique index `(mission_id, sequence)`. Index `(type, created_at)`.

Events are immutable. Corrections are new events, never updates.

### tool_invocations

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `tin_` prefix |
| mission_id / task_id / run_id | TEXT | |
| capability_id | TEXT | Registry id |
| risk | TEXT | |
| input_redacted_json / output_redacted_json | TEXT JSON | Caps applied |
| status | TEXT | requested, approved, denied, running, succeeded, failed, timed_out |
| approval_id | TEXT | Nullable |
| duration_ms | INTEGER | |
| error_code | TEXT | |
| created_at | TEXT | |

### approval_requests

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `apr_` prefix |
| mission_id / task_id / tool_invocation_id | TEXT | |
| risk | TEXT | |
| summary / target_json / payload_preview | TEXT | Redacted |
| token_hash | TEXT | Single-use, hashed |
| status | TEXT | pending, approved, rejected, expired, consumed |
| decided_by | TEXT | user |
| decided_at / expires_at / created_at | TEXT | |

### artifacts

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | `art_` prefix |
| mission_id / task_id / run_id | TEXT | |
| kind | TEXT | report, code, log, image, test_report |
| name | TEXT | |
| relative_path | TEXT | Under app-owned root |
| sha256 | TEXT | Integrity |
| size_bytes | INTEGER | |
| mime_type | TEXT | |
| provenance_json | TEXT JSON | Tool and inputs |
| created_at | TEXT | |

Path traversal and symlink escape are rejected on write and read.

### provider_profiles

| Column | Type | Notes |
|---|---|---|
| id | TEXT PK | |
| provider | TEXT | gemini, openai, local |
| model | TEXT | |
| capabilities_json | TEXT JSON | text, vision, audio_in, audio_out, tools |
| credential_ref | TEXT | Pointer to OS credential store, never the secret |
| enabled / last_health_at / last_error_code | | |

### skill_registry / memory_entries / routines / budget_events / evaluation_runs / audit_events

| Table | Key columns |
|---|---|
| skill_registry | id, source, name, version, digest, risk, verdict, enabled, last_checked_at |
| memory_entries | id, project_id, kind, content, source_ref, enabled, created_at, updated_at |
| routines | id, name, schedule, timezone, inputs_json, policy_json, budget_json, enabled, last_run_at |
| budget_events | id, mission_id, kind, amount, unit, source, created_at |
| evaluation_runs | id, dataset, status, metrics_json, report_path, created_at |
| audit_events | id, actor, action, target, decision, reason_code, created_at |

`schema_migrations` records applied migration ids and checksums.

## 3. Relationships

The ER diagram is in [`diagrams.md`](diagrams.md) § 7. Key invariants:

- Every artifact references exactly one producing mission.
- Every tool invocation references a mission and a run.
- Every approval references the tool invocation it gates.
- Every event belongs to exactly one mission.
- A task cannot run before all dependencies are `completed`.
- A mission cannot be `completed` without a `verifications` row with `passed=1`.

## 4. Transactions

State change and event append occur in one transaction:

```text
BEGIN IMMEDIATE
  update mission_tasks set status='completed'
  update missions set status='verifying'
  insert into events (... task.completed ...)
  insert into events (... mission status ...)
COMMIT
```

If the event insert fails, the state change rolls back. The UI can therefore
never observe a state that has no event, and a crash cannot produce an event
without state.

## 5. Migrations

- Numbered SQL files: `0001_initial.sql`, `0002_add_approvals.sql`.
- Applied in order, each in a transaction, recorded in `schema_migrations` with
  a SHA-256 checksum.
- Startup refuses to run against a database with a newer schema and shows a
  clear downgrade/install message.
- A backup copy is taken before destructive migrations.
- Tests run migrations from zero and from the previous fixture schema.

## 6. Retention and deletion

- Deleting a mission deletes events, tasks, runs, approvals, and tool records,
  then removes artifacts unless the user chose to keep them.
- Deleting a project requires an explicit confirmation and never deletes user
  files outside the artifact store.
- Logs and screenshots are pruned by configured retention, not silently.
- Memory entries are user-visible and individually deletable.
- Secrets are never stored in SQLite; only credential references.

## 7. Concurrency

- One writer at a time: SQLite WAL plus `BEGIN IMMEDIATE` for state transitions.
- Readers use a separate connection and never block the writer.
- Sequence allocation uses a per-mission counter incremented inside the write
  transaction; no gaps are created for rolled-back events.
- Background workers never hold a transaction open across an HTTP or model call.
