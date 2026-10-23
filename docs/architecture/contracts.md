---
title: Interface Contracts
status: active
owner: architecture
last_verified: 2026-10-23
---

# Interface Contracts

This document is normative. Code and tests must match it. Change the contract
and its tests in the same commit; never let a client and server drift.

## 1. Local API conventions

| Item | Contract |
|---|---|
| Bind | `127.0.0.1` only; ephemeral port selected at launch |
| Base path | `/api/v1` |
| Auth | `Authorization: Bearer <per-launch-token>` on every route except `/health/live` |
| Token lifetime | One process lifetime; rotated every launch; deleted on exit |
| Content type | `application/json; charset=utf-8` |
| Origin | Only the packaged renderer origin or `null` for IPC-mediated calls |
| CSRF | Custom header `X-AgentCity-Client` required on mutating routes |
| Timeouts | Server enforces per-route timeouts; clients use 30 s default, 5 s health |
| Errors | Problem+JSON shape defined in § 9 |
| Versioning | Path version plus `schema_version` inside event payloads |

No route may be reachable from the LAN. Remote access, if ever added, is a
separate opt-in server with authentication and TLS and must not weaken this
contract.

## 2. Core resources

### Mission

```json
{
  "id": "mis_01J...",
  "project_id": "prj_01J...",
  "title": "Audit the repository for unsafe shell usage",
  "mode": "execute_with_approval",
  "status": "running",
  "plan": {
    "objective": "string",
    "assumptions": ["string"],
    "acceptance_criteria": ["string"],
    "risk_summary": "string",
    "tasks": [
      {
        "id": "tsk_01J...",
        "title": "string",
        "agent": "security_guard",
        "depends_on": ["tsk_...", "tsk_..."],
        "risk": "read_only",
        "timeout_seconds": 300,
        "budget": { "max_tool_calls": 20, "max_tokens": 40000 }
      }
    ]
  },
  "budget": {
    "max_wall_clock_seconds": 1800,
    "max_tool_calls": 80,
    "max_tokens": 200000,
    "max_cost_usd": 2.0,
    "max_concurrent_tasks": 2
  },
  "created_at": "2026-10-23T12:00:00Z",
  "updated_at": "2026-10-23T12:04:11Z"
}
```

### Approval request

```json
{
  "id": "apr_01J...",
  "mission_id": "mis_01J...",
  "task_id": "tsk_01J...",
  "tool_invocation_id": "tin_01J...",
  "risk": "consequential",
  "summary": "Send the generated report to the address on screen",
  "target": { "kind": "external_send", "detail": "mailto:..." },
  "payload_preview": "redacted preview",
  "expires_at": "2026-10-23T12:10:00Z",
  "status": "pending",
  "decision": null
}
```

### Event envelope

```json
{
  "id": "evt_01J...",
  "mission_id": "mis_01J...",
  "run_id": "run_01J...",
  "agent_id": "agt_verifier",
  "task_id": "tsk_01J...",
  "sequence": 42,
  "type": "tool.succeeded",
  "schema_version": 1,
  "visibility": "user",
  "risk": "read_only",
  "created_at": "2026-10-23T12:04:11.123Z",
  "payload": {}
}
```

Sequence is strictly increasing per mission. Duplicate delivery is allowed;
clients deduplicate by `id` and order by `sequence`.

## 3. REST surface

| Method | Path | Purpose | Notes |
|---|---|---|---|
| GET | `/health/live` | Process liveness | No auth, no detail |
| GET | `/health/ready` | DB, migrations, sidecar, provider, MCP status | Auth |
| GET | `/api/v1/missions` | List missions with filters | Cursor pagination |
| POST | `/api/v1/missions` | Create a mission and request a plan | Returns 202 with mission id |
| GET | `/api/v1/missions/{id}` | Mission with plan, tasks, budget | |
| POST | `/api/v1/missions/{id}/pause` | Request pause | Idempotent |
| POST | `/api/v1/missions/{id}/resume` | Resume paused mission | |
| POST | `/api/v1/missions/{id}/cancel` | Cancel mission and descendants | Bounded propagation |
| POST | `/api/v1/missions/{id}/retry` | Retry a failed task | Body requires `task_id` |
| GET | `/api/v1/missions/{id}/events` | Replay events after a sequence | `after`, `limit` |
| GET | `/api/v1/events/stream` | SSE stream | `after` cursor, `mission_id` filter |
| GET | `/api/v1/approvals` | Pending approvals | |
| POST | `/api/v1/approvals/{id}/approve` | Approve with single-use token | Rejects stale or replayed |
| POST | `/api/v1/approvals/{id}/reject` | Reject with reason | |
| GET | `/api/v1/artifacts` | List artifacts with provenance | |
| GET | `/api/v1/artifacts/{id}` | Metadata | |
| GET | `/api/v1/artifacts/{id}/content` | Stream content | Size capped |
| GET | `/api/v1/agents` | Roster and availability | |
| GET | `/api/v1/capabilities` | Tools, MCP servers, Skills Bridge status | No secrets |
| POST | `/api/v1/capabilities/{id}/test` | Safe read-only connectivity test | Approval rules apply |
| GET | `/api/v1/projects` | Projects and workspace roots | |
| GET | `/api/v1/settings` | Redacted settings | |
| PATCH | `/api/v1/settings` | Update allowlisted settings | Audit event |
| POST | `/api/v1/desktop/grants` | Create scoped capture/control grant | Explicit consent |
| POST | `/api/v1/desktop/observe` | One-shot observation | Grant required |
| POST | `/api/v1/desktop/actions` | Proposed action batch | Policy checked |
| POST | `/api/v1/desktop/stop` | Emergency stop | Never queued behind the model |
| POST | `/api/v1/voice/transcribe` | Audio to editable transcript | Size and duration caps |
| GET | `/api/v1/diagnostics` | Self-test report | Redacted |

Payload schemas are defined as Pydantic models under `src/backend` in M1 and
exported to `docs/architecture/schemas/` when the first implementation lands.
Until then this table is the contract.

## 4. SSE format

```text
event: mission
id: 42
data: {"id":"evt_...","sequence":42,"type":"mission.planned",...}

: keepalive
```

- `id` is the sequence number, usable as the reconnect cursor.
- Keepalive comments every 15 seconds.
- The server buffers at most 5,000 events in memory; older events are read from
  SQLite.
- On reconnect, the server replays from the requested cursor and then streams.
- A gap is impossible within one mission; if detected, the client refetches
  `/missions/{id}/events?after=` and reconciles.

## 5. IPC channels

Electron main exposes only these channels through preload:

| Channel | Direction | Payload | Validation |
|---|---|---|---|
| `app:info` | renderer → main | none | returns version, platform, data dir |
| `sidecar:status` | renderer → main | none | ready, port, version, error |
| `sidecar:restart` | renderer → main | reason | rate limited |
| `window:minimize` | renderer → main | none | |
| `window:close` | renderer → main | none | |
| `desktop:stop` | renderer → main | none | bypasses API queue |
| `shell:reveal-artifact` | renderer → main | artifact id | main resolves path, rejects traversal |
| `shell:open-external` | renderer → main | allowlisted URL | https only, user gesture |

Rules: no raw `ipcRenderer`, no `nodeIntegration`, no remote module, context
isolation on, sandbox on, every payload validated in both preload and main, and
no channel accepts a filesystem path from the renderer.

## 6. Event types

| Family | Types |
|---|---|
| Mission | `mission.created`, `mission.planned`, `mission.approved`, `mission.started`, `mission.paused`, `mission.resumed`, `mission.cancelled`, `mission.completed`, `mission.failed`, `mission.blocked`, `mission.interrupted` |
| Task | `task.queued`, `task.started`, `task.progress`, `task.blocked`, `task.completed`, `task.failed`, `task.retried` |
| Agent | `agent.spawned`, `agent.assigned`, `agent.heartbeat`, `agent.completed`, `agent.failed`, `agent.stopped` |
| Tool | `tool.requested`, `tool.approval_required`, `tool.approved`, `tool.rejected`, `tool.started`, `tool.succeeded`, `tool.failed`, `tool.timed_out` |
| Artifact | `artifact.created`, `artifact.updated` |
| Budget | `budget.warning`, `budget.exceeded` |
| Provider | `provider.connected`, `provider.disconnected`, `provider.rate_limited`, `provider.error` |
| Verification | `verification.started`, `verification.passed`, `verification.failed` |
| System | `system.diagnostic`, `system.recovery`, `system.capability_changed` |

## 7. Risk classes

| Class | Examples | Default policy |
|---|---|---|
| `read_only` | search skills, read file in approved root, inspect repo, one screenshot | Auto within scope |
| `reversible_local` | write artifact, run allowlisted read-only test | Auto with audit |
| `state_change` | edit file, install package, change setting, load skill | Approval unless project policy allows the exact class |
| `consequential` | send message, publish, purchase, delete, run arbitrary script, control sensitive window | Explicit per-action approval with exact target |
| `blocked` | hidden capture, credential theft, bypassing protections, unbounded shell | Always denied |

## 8. Mission modes

| Mode | Behavior |
|---|---|
| `ask` | Answer only; no side effects |
| `plan` | Produce a plan; no execution |
| `execute_with_approval` | Safe steps auto; gated steps wait for approval |
| `autopilot_bounded` | Execute inside explicit scope and hard budgets; stop at gates |
| `desktop_watch` | Time-bounded visual context with a visible indicator |

Mode is chosen explicitly, stored per mission, and never elevated by a voice
command or a tool result.

## 9. Error contract

```json
{
  "error": {
    "code": "approval_expired",
    "message": "The approval request expired before a decision was recorded.",
    "retryable": false,
    "details": { "approval_id": "apr_...", "expired_at": "..." },
    "trace_id": "trc_..."
  }
}
```

Stable codes include: `invalid_request`, `unauthorized`, `forbidden_origin`,
`not_found`, `conflict`, `rate_limited`, `provider_unavailable`,
`provider_auth_failed`, `provider_quota_exceeded`, `mcp_unavailable`,
`mcp_timeout`, `mcp_invalid_response`, `policy_blocked`, `not_permitted`,
`approval_required`, `approval_expired`, `user_rejected`, `budget_exceeded`,
`timeout`, `cancelled`, `capability_missing`, `path_not_allowed`,
`schema_version_unsupported`, `internal_error`.

Every error carries a `trace_id` that appears in the structured log.

## 10. Compatibility rules

- Additive fields are allowed within a schema version.
- Removing or renaming a field requires a version bump and a migration note.
- Event payloads carry `schema_version`; the reader tolerates unknown fields and
  rejects unsupported major versions.
- Clients must not infer success from a connection closing; they read the event
  ledger or the resource status.
