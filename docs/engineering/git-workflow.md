---
title: Git and Worktree Workflow
status: active
owner: integration
last_verified: 2026-10-23
---

# Git and Worktree Workflow

## 1. Principles

- Preserve the user's work. Never run `git clean`, `git reset --hard`, or
  force-push without explicit permission.
- Commit every production-stable update. Do not let working features sit
  uncommitted.
- One logical change per commit. Do not mix refactors with behavior changes.
- Every commit that changes behavior includes tests and docs.
- The repository is the source of truth for code and docs, not the local clone
  of a tool.

## 2. Branches

| Branch | Use |
|---|---|
| `main` | Stable, tested integration |
| `feat/<scope>` | New capability |
| `fix/<scope>` | Defect repair |
| `docs/<scope>` | Documentation only |
| `test/<scope>` | Test infrastructure or coverage |
| `chore/<scope>` | Tooling, dependencies, maintenance |

Scope is short and kebab-case: `feat/mission-engine`, `fix/sse-replay`.

## 3. Commits

Format:

```text
<type>(<scope>): <imperative summary>

Why:
<the problem or need>

What:
- <change>
- <change>

Verification:
- <command> (<result>)
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`,
`chore`, `security`.

Rules:

- Subject line under 72 characters, no trailing period.
- Explain **why** in the body; the diff explains what.
- Reference evidence paths for behavior claims.
- Do not commit generated runtime data, databases, logs, or `.env`.
- Do not commit `src/skills/**`; record the pinned SHAs instead.

## 4. Session-end publication

Every work session ends by publishing finalized, production-ready work to the
configured `origin` remote. This is a deliberate gate, not a background sync.

Before pushing:

1. Run the nearest tests and `python scripts/check-docs.py`.
2. Confirm `git status` is clean and that no secrets, runtime data, databases,
   `.env` files, or `src/skills/**` clones are staged.
3. Commit the verified work with a Conventional Commit message.
4. Confirm the branch is `main` or the intended feature branch.

Publish and verify:

```powershell
git push origin main
git fetch origin
git rev-parse main
git rev-parse origin/main
```

The two SHAs must match. If the session made a release or acceptance claim,
record the branch, local SHA, remote SHA, and push result as evidence.

Rules:

- Never force-push `main` or any shared branch.
- If the push is rejected, fetch and integrate, rerun the tests, then push.
- If authentication or network blocks the push, report the exact command and
  error. Do not claim the session is published.
- Incomplete, failing, or secret-bearing work stays local and is named as
  blocked; it is not pushed to look finished.

## 5. Worktrees

When parallel work is separable:

```powershell
git worktree add worktrees/agentcity-backend -b feat/backend-core
git worktree add worktrees/agentcity-ui -b feat/desktop-ui
git worktree add worktrees/agentcity-qa -b test/qa
```

Each worker must verify:

```powershell
git rev-parse --show-toplevel
git branch --show-current
```

Record the output. Do not claim isolation unless both commands point at the
assigned worktree and branch.

If worktrees are unavailable:

- use exclusive file ownership;
- serialize integration;
- state clearly in the handoff that isolation was not achieved.

Only the integrator merges. Merges happen after:

- the worker reports files, commands, tests, risks, branch, and SHA;
- the diff is reviewed for scope and unexpected generated files;
- a secret scan passes;
- the documented tests pass;
- docs and contracts are updated.

## 6. Shared files

Single owner at a time:

- `package.json`, `package-lock.json`, workspace manifests;
- Python `pyproject.toml` and lockfiles;
- SQL migrations and shared schemas;
- `docs/PROJECT_MANIFEST.json` and generated context files;
- release and packaging configuration.

Other workers request changes through the integrator rather than editing these
concurrently.

## 7. Review checklist

- [ ] The change matches its description; no drive-by edits.
- [ ] Boundary types and validation are present.
- [ ] Failure, cancellation, and timeout paths are handled.
- [ ] Policy and permissions are enforced in code.
- [ ] Secrets and paths are redacted.
- [ ] Tests are meaningful and deterministic.
- [ ] Docs, manifest, and contracts are updated.
- [ ] No fake data or dead controls in real mode.
- [ ] Resource budget respected.

## 8. Release tags

- `v0.x.y` while the product is incomplete.
- A tag requires `docs/agentcity/release-verification.md` with real results.
- Never tag a build with failed critical tests.
- Annotated tags with a summary of scope and known limitations.

## 9. Recovery

- A bad local change: inspect with `git diff`, ask before discarding.
- A bad commit not pushed: prefer `git revert` over rewriting history.
- A bad commit pushed: revert, never force-push shared branches.
- A merge conflict: resolve in the owning worktree, rerun tests, then merge.
- A lost worktree: `git worktree repair` or re-add from the branch; do not
  delete the directory until the branch is verified.
