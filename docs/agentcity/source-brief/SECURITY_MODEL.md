# AgentCity — Security and Privacy Model

## 1. Threat model

AgentCity can read selected local files and screen content and may be granted access to mouse, keyboard, browsers, terminals, coding CLIs, and connected services. This is a privileged local application. Its main risks include malicious instructions in retrieved content, excessive tool authority, accidental side effects, credential exposure, untrusted integrations, local API misuse, and runaway agent loops.

## 2. Permission model

Every tool is classified by risk, capability scope, and approval policy. The model proposes an action; deterministic policy code grants or denies it.

- **Read-only/local:** view selected files, inspect repository status, summarize indexed docs, capture one screenshot after consent. May run automatically within allowed roots.
- **Low-risk reversible:** create an artifact in AgentCity's workspace, produce a report, run an allowlisted read-only test. May run under bounded mode.
- **Changes local state:** modify/delete files, edit code, install dependencies, run a command that changes state, alter settings or change environment. Require approval unless a narrowly scoped project policy explicitly allows it.
- **External or consequential:** send email/message, publish, make a purchase, upload data, delete cloud resources, change security settings, run a privileged command, or operate sensitive account pages. Require explicit per-action confirmation and show exact target, payload, and consequences.
- **Blocked by default:** hidden surveillance, credential theft, bypassing OS protections, broad unrestricted shell, evading provider limits, or unbounded autonomous control.

## 3. Desktop access

- Ask for the required OS permission on first use and explain why it is needed.
- Make screen capture on-demand by default; visible time-bounded watch mode only after explicit opt-in.
- Display persistent activity state for camera/microphone/screen capture and desktop control.
- Take fresh observations after action batches; do not act against stale coordinates/windows.
- Check allowed application/window/folder scope before execution.
- Implement an emergency stop/cancel path that does not depend on the LLM being responsive.
- Keep the app non-elevated by default. Do not silently elevate privileges to control protected windows.
- Never test automated mouse/keyboard operations on real banking, passwords, email, or other sensitive sessions.

## 4. Prompt injection and untrusted inputs

Treat web content, files, PDFs, code comments, README files, terminal output, skill instructions, OCR text, screenshots, and tool responses as untrusted data. They may inform answers but must not override system policies, role boundaries, user permissions, or approval requirements. Separate retrieved text from agent instructions in prompts and carry source provenance in data structures.

## 5. Process and filesystem controls

- Prefer OS APIs and structured commands over arbitrary shell.
- If a subprocess is required, use argument arrays, fixed executable allowlists where feasible, explicit working directory, timeout, output caps, and a sanitized environment.
- Resolve paths and symlinks; validate against user-approved workspace roots. Do not follow paths outside the allowed root.
- Store artifacts in an app-owned directory unless the user chooses another destination.
- No automatic deletion of user files; use trash/recycle bin or staged review when supported.
- Run repository code in the user's approved workspace or a controlled environment; don't run unknown postinstall scripts silently.

## 6. Network, secrets, and providers

- Bind local server to loopback by default and authenticate desktop IPC/API calls.
- Remote/LAN access is a distinct opt-in setting with authentication and transport security.
- Use operating system credential storage where available. If not, use an audited encrypted storage mechanism, never a plain-text committed key file.
- Redact keys, authorization headers, sensitive prompt data, local paths when appropriate, and personal content from logs.
- State which provider will receive which context before sending selected screen/file data to cloud models.
- No telemetry or cloud syncing by default; local diagnostics remain local until explicitly exported.
- Avoid claims of end-to-end encryption or “nothing leaves your device” unless the actual provider and code path prove it.

## 7. Agent governance

Each mission has hard limits: maximum nesting depth, concurrent workers, elapsed time, model/tool calls, token/cost budget when measurable, and data scope. Use bounded retries, circuit breakers, and deterministic approval checks. Agents cannot create or modify their own permission rules. Approval belongs to the user, not another language-model agent.

## 8. Auditability and retention

Record who/what requested an action, target scope, policy decision, approval, actual tool result, error, and verification result. Do not store sensitive screenshots or full contents longer than necessary. Provide a way to redact/delete retained data. Logs must remain useful without recording secrets.

## 9. Fail-closed behavior

If policy evaluation, current screen state, tool schema validation, or required approval cannot be established, do not perform the action. Report the specific blocker and provide a safe path forward. On restart, do not auto-repeat stale high-risk actions.
