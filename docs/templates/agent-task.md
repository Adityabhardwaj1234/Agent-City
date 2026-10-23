# Agent Task Handoff: <task>

## Identity

- Worker:
- Branch:
- Worktree (absolute path):
- Base commit:
- Contract version:

## Isolation check

Paste the exact output of:

```powershell
git rev-parse --show-toplevel
git branch --show-current
```

If this does not match the assignment, stop and report.

## Objective

One paragraph. What outcome is required, not what code to write.

## Scope

**Allowed to modify**

- `path/…`

**Read only**

- `path/…`

**Forbidden**

- Shared manifests, migrations, lockfiles unless explicitly assigned
- `src/skills/**`

## Contracts

| Boundary | Version | Notes |
|---|---|---|
| API | | |
| Event | | |
| IPC | | |
| DB | | |

## Inputs

- Relevant docs:
- Artifacts:
- Existing code:
- Fixtures:

## Acceptance criteria

- [ ] Behavior:
- [ ] Tests:
- [ ] Docs:
- [ ] Evidence:

## Budget and limits

- Max wall clock:
- Max tool calls:
- Max concurrent workers:
- Provider mode: offline | mocked | live

## Report back

- Files changed:
- Commands run and results:
- Tests (pass/fail/skip/mocked/blocked):
- Deviations from the task:
- Unresolved risks:
- Branch and commit SHA:
- Evidence paths:

## Rules

Follow `AGENTS.md`. Do not claim success from a compile, a screenshot, or an idle
process. Do not touch user data or the real SkillBridge catalog. Stop and ask if
a security control must be weakened.
