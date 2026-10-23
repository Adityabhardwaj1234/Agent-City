---
title: Performance Budget
status: active
owner: engineering
last_verified: 2026-10-23
---

# Performance Budget

The target machine is modest: **7.8 GB RAM**, Intel UHD graphics, and roughly
0.8 GB free while the planning session ran. Performance is a correctness issue,
not a polish task.

## 1. Hard limits

| Resource | Budget | Enforcement |
|---|---:|---|
| Total app idle memory | ≤ 600 MB | Measured at each milestone |
| Sidecar idle | ≤ 250 MB | Process RSS after startup |
| Electron main + renderer idle | ≤ 350 MB | Main + renderer processes |
| Active mission memory growth | ≤ 150 MB above idle | Bounded queues, event paging |
| Concurrent agent workers | 2 default, 3 maximum | Engine semaphore |
| Concurrent missions | 1 default | Scheduler |
| In-memory event buffer | 5,000 events | Ring buffer + DB paging |
| Screenshot size | 8 MB per image | Encoder cap + downscale |
| Tool output | 1 MB parsed, 8 MB stored | Adapter cap |
| Log file | 20 MB per file, 5 files | Rotation |
| Startup to usable window | ≤ 5 seconds | Measured cold start |
| Sidecar ready | ≤ 3 seconds | Health handshake |
| SSE update latency | ≤ 250 ms p95 local | Event timestamp to render |
| Approval interaction | ≤ 100 ms p95 | Local API |

Numbers are targets until measured. Once measured, record the real values in the
release report and either meet the budget or document an approved exception.

## 2. CPU and GPU

- No continuous animation when idle.
- No polling when SSE is available.
- The City Overview map updates on events, not on a 60 fps loop.
- GPU: no WebGL or 3D requirement; optional only after measurement.
- Background indexing runs at low priority and pauses during an active mission
  if CPU exceeds 70% for 30 seconds.

## 3. Startup sequence budget

| Step | Target |
|---|---:|
| Electron window visible | 1.5 s |
| Sidecar process spawned | 0.3 s |
| Migrations (no-op) | 0.2 s |
| Health ready | 3.0 s |
| First meaningful UI | 5.0 s cold |
| SkillBridge schemas cached | No blocking startup; lazy with cache |

SkillBridge and coding CLI discovery are lazy. Startup must not wait for them.
The UI shows “checking” and updates when the capability supervisor reports.

## 4. Concurrency policy

- One mission at a time by default; a second requires explicit user action.
- Two task workers per mission by default; a third only if the user raises the
  limit and free memory is above 2 GB.
- Provider calls are paced; no burst of parallel calls on a free tier.
- MCP requests are serialized per server unless the server documents otherwise.
- Desktop actions are serialized; no parallel input.

## 5. Memory instrumentation

- Sidecar: `psutil` process RSS plus child process tree (SkillBridge, coding CLI).
- Electron: `process.getProcessMemoryInfo()` for main and renderer.
- Display a resource panel in Settings → Diagnostics with timestamped samples.
- Log a warning at 80% of budget and a `budget.warning` event at 100%.
- On sustained pressure, stop starting new work; do not kill a running approval
  wait silently.

## 6. Degradation rules

| Pressure | Behavior |
|---|---|
| Memory above budget | Refuse new missions with an explanation; suggest closing a mission |
| Provider quota low | Warn before a live run; prefer Offline Mode |
| Disk below 2 GB | Stop artifact writes; keep state consistent |
| CPU above 80% for 60 s | Pause indexing and non-essential UI animation |
| Event buffer full | Page older events from SQLite; never drop silently |
| MCP unresponsive | Restart once, then mark unavailable |

## 7. Measurement procedure

1. Start from a clean app home and no provider.
2. Measure cold start to first meaningful UI (three runs, report median).
3. Idle for 60 seconds; sample memory and CPU every 5 seconds.
4. Run one deterministic mission with two workers; sample peak memory.
5. Run a live mission only if quota allows; label the result.
6. Record commands, build SHA, and environment in evidence.
7. Compare against the budget table; file a regression if above.

## 8. Profiling tools

- Python: `py-spy` (optional), `tracemalloc`, `asyncio` debug mode in tests.
- Electron: DevTools performance panel, `process.getProcessMemoryInfo()`.
- Windows: Task Manager / `Get-Process` for RSS and handle counts.
- Playwright traces for E2E timing.
- Do not ship profiling overhead in production builds.

## 9. Anti-patterns

- Loading all mission events or artifacts into memory.
- Keeping a full screenshot history for a watch session.
- Starting a local model or embedding server by default.
- Running Playwright, the app, and a coding agent simultaneously on 8 GB.
- Unbounded retries that multiply memory and quota use.
- Rendering the entire DAG at high frequency instead of diffing state.
