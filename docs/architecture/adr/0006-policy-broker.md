---
title: "ADR-0006: Deterministic policy broker and approval model"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0006: Deterministic policy broker and approval model

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** security

## Context

AgentCity can read the screen, click, type, run commands, edit files, and call
network services. Model output, web pages, documents, skill instructions, and
tool results can all contain adversarial text. Allowing the model to decide its
own permissions would make prompt injection equivalent to privilege escalation.

## Decision

A deterministic, code-level **policy broker** evaluates every action. The model
proposes; the broker decides. Decisions are based on:

- the registered capability and its schema;
- the risk class;
- the mission mode, scope, and budget;
- the project and path allowlist;
- the current desktop observation and target window;
- an approval token, when required, bound to the exact action.

Approvals are single-use, expiring, and bound to mission, task, tool, target,
and payload hash. They cannot be reused, transferred, or inferred from a voice
transcript.

## Risk classes

`read_only`, `reversible_local`, `state_change`, `consequential`, `blocked`.

Defaults: read-only auto within scope; reversible local auto with audit; state
change requires approval unless a narrow project policy allows that exact class;
consequential requires explicit per-action confirmation; blocked is always
denied.

## Consequences

**Positive**

- Prompt injection cannot grant permission.
- Decisions are testable and auditable.
- The UI can explain exactly why an action is waiting or denied.

**Negative**

- More approval friction for legitimate work.
- Policy must be maintained as capabilities grow.
- A misconfigured allowlist can still be dangerous; fail closed by default.

## Guardrails

- Policy evaluation errors deny the action.
- The emergency stop path does not consult the model or the approval queue.
- Every decision writes an `audit_events` row with a reason code.
- Tests cover forged, stale, replayed, and cross-mission approval tokens.
