---
title: "ADR-0002: Deterministic mission engine owns durable state"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0002: Deterministic mission engine owns durable state

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** architecture

## Context

Google ADK provides agents, workflows, session state, guardrail callbacks, and
evaluation. It is the right reasoning framework. It is not a durable scheduler
for a desktop product that must:

- persist a plan before any side effect;
- wait minutes or hours for human approval;
- survive a crash and restart without replaying dangerous steps;
- cancel from a button while a model call is in flight;
- enforce hard budgets and concurrency limits;
- stream a monotonic event history to a UI.

Putting those responsibilities inside an LLM-driven workflow makes behavior
probabilistic and hard to test. A second general-purpose orchestrator would also
violate the "one orchestration brain" rule.

## Decision

A deterministic **Mission Engine** owns mission state, the task DAG, budgets,
approvals, retries, checkpoints, cancellation, and recovery. It invokes ADK for
reasoning steps and receives typed results. ADK remains the only agent
framework; we are not introducing a competing one.

The split is:

| Concern | Owner |
|---|---|
| Intent, planning, specialist reasoning, tool selection | ADK |
| Plan validation, schema enforcement, policy | Engine |
| Durable lifecycle, events, approvals, budgets | Engine |
| Tool execution and result capture | Tool gateway (engine-controlled) |
| Final acceptance decision | Verifier agent proposes, engine records |

## Consequences

**Positive**

- Mission behavior is testable without a model.
- Crash recovery and cancellation are deterministic.
- The UI can trust the event ledger.
- Offline Mode can exercise the full lifecycle with a scripted planner.

**Negative**

- Two layers to maintain: engine contracts and ADK agent contracts.
- The plan schema must be versioned and validated carefully.
- Agents cannot freely spawn unbounded trees; delegation is mediated.

## Guardrails

- Agents never write mission state directly. They return typed results.
- The engine rejects a plan that exceeds depth, concurrency, or budget limits.
- Only the engine can transition mission status.
- ADK workflow composition is used inside a task, not as the global scheduler.
