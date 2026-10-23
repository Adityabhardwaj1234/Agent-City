---
title: Product Requirements
status: active
owner: product
last_verified: 2026-10-23
---

# Product Requirements

## 1. Product statement

AgentCity is a desktop-first, local-first AI operating environment. It unifies
conversation, visible computer use, research, project knowledge, agent teams,
coding-agent handoff, voice, long-running missions, approvals, and run
observability in one original interface.

It is inspired by the capability breadth of modern AI desktop assistants and the
operational clarity of a command center. It does not copy ChatGPT branding,
assets, or trade dress. It must look and behave like AgentCity.

## 2. Principles

1. **Real execution over spectacle.** Every agent, mission, tool call, test,
   token count, and cost is tied to a runtime record. Demo data is opt-in,
   labeled, and isolated.
2. **ADK-first orchestration.** Google ADK is the primary reasoning runtime.
   The deterministic mission engine owns durable state; no competing
   orchestration framework is added without a documented gap.
3. **SkillBridge first.** Existing skills and MCP capabilities are discovered
   and used rather than recreated.
4. **Original code.** Candidate projects are references, not forks (ADR-0001).
5. **Local-first with explicit egress.** No telemetry or cloud sync by default.
   The UI states what data a provider will receive before sending it.
6. **Human control.** Pause, cancel, inspect, approve, reject, and take over are
   always available.
7. **Bounded autonomy.** Hard limits on depth, concurrency, tool calls, time,
   tokens, cost, and file scope.
8. **Measurable reliability.** Unit, integration, E2E, security, and agent
   trajectory evaluations are part of done.
9. **Honest status.** Working, mocked, and blocked are never blurred.
10. **Respect existing work.** No destructive cleanup, history rewrite, secret
    edit, or unrelated reformatting.

## 3. Users and jobs

**Primary user: the builder/operator.** Works across several repositories,
wants agents to plan and execute multi-step work, and wants to see and approve
what happens.

Jobs:

- “Turn this request into a plan I can inspect before anything runs.”
- “Assemble a team for this task and show me who is doing what.”
- “Watch my screen and help me with this application, without hidden control.”
- “Research this topic and keep the citations attached.”
- “Hand this coding task to a worker in an isolated worktree and show me the
  diff and tests.”
- “Stop everything now.”

**Secondary user: the reviewer/auditor.** Needs a truthful history of what
happened, what was approved, what failed, and what evidence exists.

## 4. Workspaces

### A. City Overview

Live mission status, agent map, event timeline, approval queue, resource
pressure, provider health, latest artifacts. Every metric shows source,
timestamp, and whether it is measured, reported, estimated, or unavailable. The
metaphor is optional; readable tables and details are always available.

### B. Command

Streaming chat with history, projects, attachments, citations, code blocks,
artifact previews, model selection, tool activity, cancel/regenerate. Voice
push-to-talk with an editable transcript before execution.

### C. Missions

Mission queue, plan, task DAG, dependencies, ownership, state, logs, artifacts,
budget, checkpoints, and approvals. Pause, resume, cancel, retry failed steps,
and recover after restart. Safe retry semantics; no silent replay of
non-idempotent work.

### D. Agent Teams

Roster, instructions, capabilities, model policy, permitted tools, budgets,
concurrency, status, reliability history, and direct conversation. Team
templates. A verifier must inspect results before mission completion. Bounded
child creation; no self-replication.

### E. Workspace

Project picker, repository status, file tree, diffs, test results, worktrees,
artifacts, and audit trail. Coding CLI adapters only for installed and
authorized tools; never bypass login, rate, or subscription controls.

### F. Desktop Vision

Consent-based capture, one-shot by default, time-bounded watch only after
explicit opt-in. Target window, capture timestamp, proposed actions, live
indicator, pause/stop, emergency cancel. UI Automation first; vision and
mouse/keyboard fallback. Fresh observation after each action batch.

### G. Research

Browser and web research with source URLs, retrieval timestamps, and citations.
Compare, summarize, and report workflows saved as artifacts. Web content is
untrusted data, never instructions.

### H. Projects and Memory

Project notes, files, threads, indexed documents, codebase summaries, retrieved
context with provenance. SQLite FTS for retrieval. Memory browser with inspect,
correct, disable, and delete controls.

### I. Skills and Tools

Configured MCP servers, SkillBridge capabilities, local tools, providers, and
coding adapters. Status, schema, permissions, health check, and safe test
action. Disable/re-enable. No credentials displayed. Imported skills are
inspected and treated as untrusted until reviewed.

### J. Artifacts

One library for mission outputs: Markdown, source, reports, logs, explicitly
saved screenshots, test reports. Preview, reveal, copy path, export. No
arbitrary overwrite or delete without approval.

### K. Automations

User-authored scheduled or event-triggered routines with visible schedule,
timezone, inputs, allowed tools, run budget, last result, and pause switch.
External side effects require per-run approval unless a narrow allowlist is
explicitly configured.

### L. Settings and Diagnostics

Model routing, provider keys, speech, local models, hotkeys, theme, retention,
permissions, concurrency, budget, logs, updates, diagnostics. Credentials in
the OS credential store. A self-test covers runtime, backend, migrations, MCP,
provider, microphone, desktop permission, and packaged smoke test.

## 5. Interaction modes

| Mode | Side effects | Use |
|---|---|---|
| Ask | None | Answer, search, analyze, explain |
| Plan | None | Steps, risks, and estimates for review |
| Execute with approval | Safe steps auto; gated steps wait | Normal work |
| Autopilot (bounded) | Inside explicit scope and hard limits | Repetitive, low-risk work |
| Desktop watch | Time-bounded visual context | Supervised computer help |

Mode is explicit in the UI and saved per mission. Voice or content cannot
silently elevate permissions.

## 6. Differentiation

- ADK-native teams, validated by the user's Agent Builder during development.
- SkillBridge integration with an inspectable capability registry.
- A command map backed by persisted events, never decorative activity.
- Shared missions across chat, voice, browser, desktop, files, and coding CLIs.
- Replayable task graphs with budgets, checkpoints, and verified outputs.
- Cross-provider routing by capability, latency, quality, and budget.
- Local-first privacy with visible egress.
- An evaluation lab that scores tool trajectories as well as answers.

## 7. Non-goals for the first release

- Parity with every proprietary feature of paid assistants.
- Always-on hidden microphone or screen recording.
- Unlimited autonomous computer operation.
- Foundation-model training.
- Mandatory Docker, Kubernetes, PostgreSQL, or Redis.
- A cloud account requirement to launch the shell.
- Automatic commits, pushes, purchases, emails, or public posts without policy.
- Pretending a provider works without keys, authorization, or OS permissions.
- Running on macOS/Linux in the first release; the design avoids needless
  Windows coupling but Windows is the supported target.

## 8. Definition of complete

A capability is complete only when it has implemented behavior, visible UI
states, authorization checks, error handling, redacted logs, a test, docs, and a
verified result recorded with evidence. A placeholder, animation, card, or
unconfigured provider is not complete.
