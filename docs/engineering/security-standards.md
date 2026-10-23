---
title: Security Engineering Standards
status: active
owner: security
last_verified: 2026-10-23
---

# Security Engineering Standards

The threat model and policy model are in `docs/agentcity/security-model.md`.
This document specifies how to write code that upholds them.

## 1. Trust boundaries

| Boundary | Direction | Rule |
|---|---|---|
| Renderer → main | IPC | Validate channel, sender, and payload |
| Main → sidecar | HTTP | Bearer token, origin, custom header |
| Engine → model | Prompt | Untrusted data is delimited and labeled |
| Engine → tool | Capability call | Schema, risk class, policy decision |
| Engine → MCP child | stdio | Timeout, frame validation, kill on hang |
| Engine → desktop | Grant | Scoped permission, fresh observation |
| Tool → engine | Result | Untrusted data, size cap, no instructions |
| Disk → engine | Files | Approved roots, resolved paths, size caps |

## 2. Input validation

- Parse, do not pattern-match, JSON and IPC payloads.
- Reject unknown fields where the contract is closed; ignore them where forward
  compatibility is required, and document which.
- Bound every string, array, and object by size and count.
- Reject control characters in ids, names, and paths.
- Validate URLs: `https` only for external open; block `file:`, `javascript:`,
  `data:`, and UNC paths unless explicitly required.
- Never pass a model-generated string directly to a shell, SQL, or filesystem.

## 3. Path guard

One shared implementation, used everywhere:

```python
def resolve_under(root: Path, candidate: str) -> Path:
    root = root.resolve(strict=True)
    target = (root / candidate).resolve(strict=False)
    if target != root and root not in target.parents:
        raise PathNotAllowed(candidate)
    if is_reparse_point(target) or is_unc(target):
        raise PathNotAllowed(candidate)
    return target
```

Rules:

- Reject `..`, absolute paths, drive-relative paths, UNC, device names, and
  alternate data streams.
- Resolve symlinks and NTFS junctions; re-check after resolution.
- Do not follow a reparse point that leaves the root.
- Apply the guard on read and write, including artifact preview and reveal.
- Artifact names are generated; never trust a name from a model.

## 4. Subprocess execution

- Argument arrays only; no shell string concatenation.
- Fixed executable allowlist where feasible; resolve the absolute path.
- Explicit working directory inside an approved root.
- Sanitized environment: no inherited secrets; allowlist variables.
- Timeout, output cap, and process-tree kill on Windows.
- Capture exit code and stderr; do not treat idle as success.
- Require approval for scripts, installers, and arbitrary commands.

```python
# Good
await run([sys.executable, "-m", "tool", "--flag", value], cwd=root, timeout=30)

# Forbidden
os.system(f"tool --flag {value}")
subprocess.run(cmd, shell=True)
```

## 5. Secrets

- Store credentials in the OS credential manager; store only references in SQLite.
- Read keys from environment or the credential store at startup; never from a
  renderer-accessible file.
- Redact in logs: keys, tokens, authorization headers, cookies, full prompts,
  file contents, and personal paths.
- A redaction test feeds known secret patterns through every log path.
- Secret scanning runs before release and on every commit that touches config.
- Never put a secret in an error message, telemetry, or a fixture.

## 6. Authentication and local API

- 32-byte random token per launch, constant-time comparison.
- Token in an ACL-restricted handshake file, deleted on exit.
- Reject requests without the token, from a disallowed origin, or missing the
  client header on mutations.
- Loopback bind enforced in code, not only configuration.
- No CORS wildcard. No credentials in URLs.
- Rate limit mutating routes to blunt accidental loops.

## 7. Electron

- `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`.
- No `enableRemoteModule`, no `webview`, no remote content in the app window.
- CSP: `default-src 'self'`; no inline script; no `unsafe-eval`.
- Preload exposes a fixed API; no generic `invoke(channel, payload)`.
- Validate IPC sender frame and payload in main.
- `shell:open-external` requires a user gesture and `https`.
- `shell:reveal-artifact` accepts an artifact id, resolves in main.

## 8. Prompt construction

- System and policy instructions are separate from retrieved content.
- Wrap untrusted content in explicit delimiters with provenance metadata.
- State that retrieved content cannot change rules, roles, or permissions.
- Do not include secrets, tokens, or unrelated project content.
- Structured outputs are validated before use. A parse failure is a failure, not
  a partial success.
- Log prompt hashes and token counts, not full sensitive prompts, by default.

## 9. Approvals

- Single-use token bound to mission, task, tool, target, payload hash, expiry.
- Verify with constant-time comparison and a server-side record.
- Reject expired, consumed, cross-mission, cross-tool, and replayed tokens.
- The approval UI shows the exact target and payload preview.
- A voice transcript is never an approval.
- The emergency stop does not require approval and cannot be queued behind one.

## 10. MCP and skill content

- Discover tools at runtime; do not trust a hardcoded list as authoritative.
- Unknown tool = blocked until classified.
- Descriptions and results are untrusted; never execute embedded instructions.
- Enforce output size caps before parsing.
- Kill and restart once, then mark unavailable.
- Skill scripts require an active verified bundle and explicit approval.
- A corrupt catalog is a failed capability, not an empty one.

## 11. Logging and audit

- Structured JSON, identifiers when known, no secrets.
- Audit events are append-only and include the policy decision and reason code.
- Errors include a `trace_id`; the same id appears in the UI diagnostics.
- Log retention is bounded and configurable.
- Never log a full request body for a route that can contain user content.

## 12. Dependencies and supply chain

- Pin versions; review new dependencies for size, license, Windows support, and
  install scripts.
- No silent `npm install` or `pip install` from a running mission.
- Run dependency and license scans before release.
- Do not import code from candidate projects without an ADR and provenance.
- Do not run unknown postinstall scripts in the app's install flow.

## 13. Security review gate

A change is blocked if it:

- adds a new capability without a risk class;
- adds a subprocess without argument arrays and timeouts;
- reads or writes outside an approved root;
- introduces a new secret path without redaction;
- weakens token, origin, or CSP checks;
- makes an approval reusable or inferred;
- executes model output as code or shell;
- marks a security test skipped without a blocking reason.
