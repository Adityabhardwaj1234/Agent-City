---
title: "ADR-0005: Offline-first baseline with explicit provider setup"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0005: Offline-first baseline with explicit provider setup

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** architecture

## Context

No model provider key is configured on the target machine, and the free Gemini
tier is limited (roughly 5 requests per minute and about 20 requests per day per
model). A desktop app that cannot launch, plan, or demonstrate its state machine
without a key is fragile and hard to test. A fake "live" mode would violate the
product's honesty rule.

## Decision

AgentCity has two explicit execution modes:

1. **Offline Mode (default when no provider is configured).** A deterministic
   scripted planner produces plans from templates and local rules. Local tools,
   approvals, events, artifacts, verifier logic, cancellation, and recovery all
   work. The UI labels the mode clearly and never claims model reasoning.
2. **Live Mode.** Enabled only when a provider credential passes a health check.
   ADK agents perform real reasoning. Usage is measured or labeled as estimated.

The same contracts are used in both modes. Tests run against Offline Mode by
default; live tests are opt-in and quota-paced.

## Consequences

**Positive**

- The full product is testable and demoable without spending quota.
- New contributors can run the app immediately.
- Provider failures degrade into a clear state instead of a broken screen.
- No accidental data egress when no provider is configured.

**Negative**

- Two planner implementations must satisfy the same schema.
- Offline plans are less flexible than model-generated plans.
- Some user value is unavailable until a key is configured.

## Guardrails

- The mode is visible in the status bar and in every mission record.
- The app never silently falls back from Live to Offline mid-mission; the user
  is asked and the transition is recorded as an event.
- Live evaluation results are never merged with Offline results in reports.
- Quota pacing: default minimum interval of 13 seconds between live calls and a
  daily budget guard; 429 is retried with backoff, never in a tight loop.
