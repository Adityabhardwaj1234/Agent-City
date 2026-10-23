---
title: Desktop Permissions Runbook
status: active
owner: security
last_verified: 2026-10-23
---

# Desktop Permissions Runbook

Desktop control is the highest-risk capability in AgentCity. It is off until the
user grants a scoped permission.

## 1. Permission model

A grant specifies:

- capability: `capture_once`, `capture_watch`, `uia_read`, `input_control`;
- allowed applications/windows (by title and process);
- allowed monitor;
- duration (minutes) and expiry;
- whether screenshots may be saved;
- whether pixels may be sent to a provider.

Grants are persisted, visible, revocable, and audited. Expired or revoked grants
fail closed.

## 2. First use

1. The user opens Desktop Vision and sees an explanation of what will be
   captured and why.
2. The user selects a scope and duration.
3. The app requests OS permission if required.
4. A persistent indicator appears immediately.
5. Capture starts only after the grant is stored.

No hidden capture. No default watch session. No capture at launch.

## 3. Observation flow

```text
grant check → target window check → fresh capture → UIA tree if available
→ timestamp and monitor recorded → model proposes actions → policy check
→ user approves if required → actions execute → fresh observation
→ expected-result check → audit event
```

Rules:

- Stale observations are rejected; refresh after every batch.
- Coordinates are physical pixels; DPI awareness is set before capture.
- Downscale large screenshots; cap at 8 MB.
- Never send pixels to a cloud provider without explicit vision egress consent.
- Save a screenshot only when the user asks or a mission policy requires it.

## 4. UI Automation first

- Prefer UIA elements (name, control type, automation id) over pixels.
- Fail closed when the tree is unavailable; fall back to vision only if the
  grant allows it.
- Elevated windows are not controllable from a non-elevated process. Show a
  clear message; do not auto-elevate.
- Some apps expose poor UIA. Record that limitation; do not silently click.

## 5. Action safety

| Action | Class | Approval |
|---|---|---|
| Read window title / UIA tree | read_only | Grant |
| One screenshot | read_only | Grant |
| Click/type in an allowlisted window | consequential | Explicit per batch |
| Launch an application | state_change | Policy |
| Delete/move files via UI | consequential | Explicit per action |
| Interact with a sensitive window | blocked | Always denied |

Sensitive windows include password managers, banking, email composition, and
security settings. The policy list is conservative and user-visible.

## 6. Emergency stop

- A global hotkey and a visible button.
- Implemented in Electron main, not queued behind the model or approval flow.
- Cancels the desktop queue, aborts the in-flight action, releases input, hides
  the indicator.
- Records an audit event with the source (`hotkey` or `button`).
- Works even if the sidecar is unresponsive (main kills the desktop worker).

## 7. Testing

- Use Notepad or a dedicated fixture window only.
- Never test against banking, email, password managers, or personal accounts.
- Cases: no grant, expired grant, wrong window, stale observation, revoked
  mid-batch, emergency stop, UIA unavailable, DPI 125%, multi-monitor.
- Verify the indicator appears and disappears with the grant.

## 8. Cleanup

- Revoking a grant stops capture and deletes temporary frames.
- Mission screenshots follow retention (default 7 days) and are user-deletable.
- On exit, stop capture, release input, remove temp files, and log the shutdown.
- Never leave a background capture process running.

## 9. Troubleshooting

| Symptom | Check |
|---|---|
| Black screenshot | Secure desktop, DRM window, or capture permission |
| Wrong coordinates | DPI awareness and monitor origin |
| UIA empty | Elevated target or unsupported app |
| Actions ignored | Focus not on target; re-observe and retry once |
| Stop not working | Main-process hotkey registration; check for conflicts |
| Indicator missing | Grant state and renderer status bar |

## 10. Evidence

Record the grant scope, target window, observation timestamp, actions, and
result. Do not store screenshots of personal content in evidence.
