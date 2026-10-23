---
title: Decision Log
status: active
owner: integration
last_verified: 2026-10-23
---

# Decision Log

Chronological record of decisions that shape the project. One-way doors get an
ADR; reversible choices are recorded here with enough context to revisit them.

| ID | Date | Decision | Rationale | Status |
|---|---|---|---|---|
| D-001 | 2026-10-23 | Use an original lean app instead of forking Personal Jarvis | PySide6, 1.2 GB, heavy extras, competing orchestrator, 7.8 GB RAM | Accepted (ADR-0001) |
| D-002 | 2026-10-23 | Deterministic mission engine owns durable state | Restart, approvals, cancellation, and budgets cannot rely on a model loop | Accepted (ADR-0002) |
| D-003 | 2026-10-23 | Electron + React + TypeScript shell | No Rust toolchain; mature Windows audio, capture, packaging | Accepted (ADR-0003) |
| D-004 | 2026-10-23 | SkillBridge as stdio MCP subprocess | Real protocol boundary; no reimplementation; host config independent | Accepted (ADR-0004) |
| D-005 | 2026-10-23 | Offline-first default, live mode explicit | No key on this machine; deterministic tests; honest UI | Accepted (ADR-0005) |
| D-006 | 2026-10-23 | Deterministic policy broker with single-use approvals | Prompt injection must not equal privilege escalation | Accepted (ADR-0006) |
| D-007 | 2026-10-23 | Docs and context are build artifacts with checks | AI maintainers need reliable, current context | Accepted (ADR-0007) |
| D-008 | 2026-10-23 | Pin ADK Agent Builder at `a74d73b` | Reproducible generation and validation | Accepted |
| D-009 | 2026-10-23 | Pin SkillBridge at `25c352e` | Reproducible MCP behavior and security fixes | Accepted |
| D-010 | 2026-10-23 | Do not vendor tool source in Git | Keep the repo small; licenses and upgrades stay explicit | Accepted |
| D-011 | 2026-10-23 | Use npm, not pnpm | pnpm is not installed; avoid global tooling changes | Revisit if the workspace standardizes on pnpm |
| D-012 | 2026-10-23 | Correct the build pack: 7.8 GB RAM, not 16 GB | Measured on the target machine | Accepted |
| D-013 | 2026-10-23 | Correct the build pack: ADK Agent Builder is build-time, not a runtime tool | Its interface is a CLI/skill, not a service | Accepted |
| D-014 | 2026-10-23 | Quarantine the corrupt SkillBridge catalog; use isolated homes for tests | `PRAGMA integrity_check` reports 91 findings; opening it mutates user data | Accepted; user recovery decision pending |
| D-015 | 2026-10-23 | Target concurrency of 2 workers | 7.8 GB RAM with ~0.8 GB free during planning | Revisit after memory measurements |
| D-016 | 2026-10-23 | Keep project in OneDrive for now | User's chosen location; exclude build output from sync where possible | Revisit if sync causes SQLite or node_modules issues |

## Open questions

| ID | Question | Default if unresolved |
|---|---|---|
| Q-001 | Which provider key will be used for live mode? | Offline Mode only |
| Q-002 | Recover or rebuild the SkillBridge catalog? | Use isolated home; ask before touching real data |
| Q-003 | Move the working copy out of OneDrive? | Stay, with `.gitignore` and artifact locations outside the tree |
| Q-004 | Is a pnpm workspace required? | Use npm |
| Q-005 | Should desktop capture be enabled by default for the first demo? | Off; require explicit consent |

## Decision process

1. State the problem and the constraints that are actually measured.
2. List viable options and their costs on this machine.
3. Choose the option that preserves safety, testability, and honesty.
4. Record the consequences, including what gets harder.
5. For one-way doors, write an ADR before implementation.
6. Revisit when a trigger in the ADR or this log is met; do not silently drift.
