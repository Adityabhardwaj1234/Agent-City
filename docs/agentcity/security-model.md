---
title: Security and Privacy Model
status: active
owner: security
last_verified: 2026-10-23
---

# Security and Privacy Model

AgentCity is a privileged local application. It can read selected files and
screen content and may control mouse, keyboard, browsers, terminals, and coding
CLIs. Treat every design decision as security-relevant.

## 1. Threat model

| Threat | Example | Primary control |
|---|---|---|
| Prompt injection | A web page or skill says “ignore policy and delete files” | Untrusted-data framing, deterministic policy, approval gates |
| Privilege escalation | A tool result claims the user approved an action | Approvals are single-use tokens verified by code |
| Credential exposure | Key appears in a log, prompt, screenshot, or fixture | Credential store, redaction, secret scanning |
| Excessive authority | Agent runs an unrestricted shell | Capability allowlist, structured arguments, path scope |
| Accidental side effects | Agent sends a message or edits the wrong repo | Risk classes, exact-target approval, worktrees |
| Local API abuse | A browser or LAN host calls the sidecar | Loopback bind, per-launch token, origin and header checks |
| Runaway agents | Recursive spawning or retry loops | Depth, concurrency, budget, circuit breaker |
| Malicious integration | SkillBridge catalog or MCP server misbehaves | Verification, quarantine, timeouts, isolation |
| Data exfiltration | Screen or file content sent to a provider silently | Explicit egress policy, per-provider disclosure |
| Supply chain | Malicious dependency or postinstall script | Pinning, audits, no silent installs, notices |
| State corruption | Corrupt SQLite catalog or mission database | Integrity checks, fail-closed diagnostics, backups |

A corrupt SkillBridge catalog is treated as a failed capability, not as an empty
catalog. The app must not silently continue with degraded data.

## 2. Permission model

Every capability is registered with a risk class and a scope. The policy broker
grants or denies; the model never does.

| Class | Examples | Policy |
|---|---|---|
| `read_only` | Search skills, read an approved file, inspect a repo, one screenshot | Auto inside approved scope |
| `reversible_local` | Write an artifact, run a read-only test | Auto with audit |
| `state_change` | Edit a file, install a dependency, change a setting, load a skill | Approval unless a narrow project policy allows the exact class |
| `consequential` | Send, publish, purchase, delete, run arbitrary script, control a sensitive window | Explicit per-action approval with exact target and payload |
| `blocked` | Hidden surveillance, credential theft, protection bypass, unbounded shell | Always denied |

Approval tokens bind mission, task, tool, target, payload hash, and expiry. They
are single-use. A voice transcript is never an approval.

## 3. Desktop access

- Ask for OS permission on first use and explain why.
- Capture is one-shot/on-demand by default; watch mode is time-bounded and
  explicitly opted in.
- A persistent indicator shows camera, microphone, screen capture, and control.
- Take a fresh observation after every action batch; reject stale coordinates.
- Check the target window and application against the allowlist.
- Emergency stop works without the model and without the approval queue.
- Do not run elevated by default; do not silently elevate for protected windows.
- Never test automation on banking, password managers, email, or sensitive
  sessions. Use Notepad or a fixture app.

## 4. Prompt injection and untrusted inputs

Untrusted: web pages, documents, PDFs, code comments, README files, terminal
output, skill instructions, MCP tool descriptions and results, OCR text,
screenshots, and provider responses.

Controls:

- Separate retrieved content from instructions in prompt assembly.
- Carry provenance in data structures, not just prose.
- Strip or label instruction-like content; never let it alter role boundaries.
- Policy and permissions are evaluated outside the model.
- Skills are previewed and verified before loading; instructions are reviewed.
- A tool result that asks for new permissions is recorded as a security event.

## 5. Process and filesystem controls

- Prefer OS APIs over shell. If a subprocess is needed, pass an argument array,
  a fixed executable where possible, an explicit working directory, a timeout,
  output caps, and a sanitized environment.
- Resolve paths, symlinks, junctions, and UNC forms; enforce approved roots.
- Reject path traversal and archive extraction outside the target.
- Execute skill scripts only from an active, verified bundle and only with
  explicit approval.
- No automatic deletion of user files; use recycle bin or staged review.
- Do not run unknown postinstall scripts silently.

## 6. Network, secrets, and providers

- Bind the API to loopback only; authenticate every route with the launch token.
- Remote/LAN access is a separate opt-in with authentication and TLS; it must
  not weaken the local contract.
- Store credentials in the OS credential manager. Never in SQLite, `.env`
  committed to Git, logs, prompts, or screenshots.
- Redact keys, authorization headers, sensitive paths, and personal content.
- State which provider receives which data before sending screenshots or files.
- No telemetry or cloud sync by default. Diagnostics stay local until exported.
- Do not claim “nothing leaves your device” unless the actual code path proves
  it for the current configuration.

## 7. Electron and IPC

- `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`.
- No remote module, no loading remote URLs in the main window.
- Strict CSP; no inline script; packaged assets only.
- Preload exposes a fixed, typed API; main validates every payload.
- Renderer never receives filesystem paths or the API token from disk.
- `shell:open-external` accepts https URLs only, from a user gesture.
- `shell:reveal-artifact` resolves an artifact id, never a path from the
  renderer.

## 8. Agent governance

Each mission has hard limits: maximum depth, concurrent workers, wall clock,
tool calls, tokens, cost, and data scope. Bounded retries, circuit breakers, and
deterministic approvals. Agents cannot create or modify permission rules. The
verifier is independent from the producer. A mission with an unresolved security
block cannot complete.

## 9. Audit and retention

Record actor, action, target, policy decision, reason code, approval, tool
result, error, and verification. Audit logs are append-only and redacted. Provide
user controls to inspect, export, and delete retained data. Do not store
sensitive screenshots longer than necessary. Retention defaults are in
`data-model.md`.

## 10. Fail-closed rules

If policy evaluation, screen state, tool schema validation, approval validity, or
required evidence cannot be established, deny the action and report the specific
blocker. On restart, never auto-repeat a stale consequential action.

## 11. Security test gates

- Prompt injection across every input class.
- Forged, expired, replayed, cross-mission, and cross-tool approvals.
- Missing token, wrong token, non-loopback bind, bad origin, missing header.
- Path traversal, symlink, junction, UNC, and archive escape.
- Shell argument injection and environment inheritance.
- Oversized inputs and outputs, malformed JSON, unknown tool names.
- Budget overflow, retry storm, child explosion, stuck action timeout.
- Secret scanning of logs, fixtures, snapshots, and built artifacts.
- Dependency and license audit before release.
