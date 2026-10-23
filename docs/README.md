---
title: Documentation Index
status: active
owner: integration
last_verified: 2026-10-23
---

# Documentation Index

AgentCity's documentation is organized so that a new human or AI can stop
reading as soon as they have enough context for their task.

In the reading orders below, paths are relative to the repository root. In the
tables, paths are relative to `docs/` unless they start with `docs/`.

## Reading orders

### Onboarding a new agent (about 10 minutes)

1. `docs/AI_CONTEXT.md`
2. `docs/PROJECT_MANIFEST.json`
3. `docs/agentcity/state-of-build.md`
4. `docs/engineering/coding-standards.md`
5. `docs/engineering/change-recipes.md`

### Fixing a bug

1. `docs/AI_CONTEXT.md` § invariants
2. `docs/engineering/debugging-playbook.md`
3. `docs/architecture/contracts.md` for the affected boundary
4. `docs/engineering/testing-strategy.md`

### Adding a feature

1. `docs/agentcity/PRD.md` for scope
2. `docs/architecture/overview.md` and `docs/architecture/contracts.md`
3. `docs/engineering/change-recipes.md` for the exact file list
4. `docs/agentcity/test-plan.md` for the required tests
5. `docs/agentcity/deliverables-and-acceptance.md` for the done criteria

### Security review

1. `docs/agentcity/security-model.md`
2. `docs/engineering/security-standards.md`
3. `docs/architecture/diagrams.md` § trust boundaries
4. `docs/agentcity/test-plan.md` § security tests

### Release

1. `docs/runbooks/release-verification.md`
2. `docs/runbooks/packaging.md`
3. `docs/agentcity/deliverables-and-acceptance.md`
4. `docs/templates/release-verification.md`

## Context (read first)

| Document | Purpose |
|---|---|
| `AI_CONTEXT.md` | One-page compressed context and next task |
| `PROJECT_MANIFEST.json` | Machine-readable versions, paths, commands, status |
| `agentcity/state-of-build.md` | Generated feature status matrix |
| `repo-map.md` | Generated shallow repository map |
| `agentcity/glossary.md` | Shared vocabulary |
| `agentcity/decision-log.md` | Chronological decisions and links to ADRs |

## Product and governance

| Document | Purpose |
|---|---|
| `agentcity/PRD.md` | Product scope, principles, workspaces, non-goals |
| `agentcity/implementation-plan.md` | Milestones, dependencies, agent/worktree protocol |
| `agentcity/deliverables-and-acceptance.md` | Per-capability completion checklist |
| `agentcity/reuse-audit.md` | Candidate repositories, licenses, decisions |
| `agentcity/tooling-inventory.md` | Exact tool interfaces, commands, and evidence |
| `agentcity/agent-roster.md` | Runtime agents and development workers |
| `agentcity/model-routing.md` | Model policy, fallbacks, limits, quota reality |
| `agentcity/test-plan.md` | Test layers, scenarios, and gates |
| `agentcity/security-model.md` | Threat model, permissions, approvals, egress |

## Architecture

| Document | Purpose |
|---|---|
| `architecture/overview.md` | System context, containers, components, lifecycle |
| `architecture/diagrams.md` | All Mermaid diagrams |
| `architecture/contracts.md` | API, IPC, event, error, and risk contracts |
| `architecture/data-model.md` | Tables, relationships, retention |
| `architecture/adr/` | One-way-door decisions and rationale |

## Engineering

| Document | Purpose |
|---|---|
| `engineering/coding-standards.md` | Language, typing, errors, logging, review rules |
| `engineering/backend-guidelines.md` | FastAPI, SQLite, async, cancellation patterns |
| `engineering/frontend-guidelines.md` | Electron security, React, state, accessibility |
| `engineering/testing-strategy.md` | Unit, integration, E2E, and agent evaluation |
| `engineering/debugging-playbook.md` | Symptom-to-fix procedures and Windows traps |
| `engineering/git-workflow.md` | Branches, worktrees, commits, review, releases |
| `engineering/documentation-standards.md` | Frontmatter, structure, update triggers |
| `engineering/security-standards.md` | Secure coding and secret handling |
| `engineering/performance-budget.md` | RAM, CPU, latency, and concurrency limits |
| `engineering/change-recipes.md` | Exact file checklists for common changes |

## Operations

| Document | Purpose |
|---|---|
| `runbooks/dev-setup.md` | Toolchain, clones, environment, first run |
| `runbooks/provider-setup.md` | Gemini and fallback provider configuration |
| `runbooks/mcp-and-skills.md` | SkillBridge startup, health, and isolation |
| `runbooks/desktop-permissions.md` | Consent, capture, UIA, emergency stop |
| `runbooks/voice.md` | Microphone, STT, TTS, interruption |
| `runbooks/packaging.md` | Windows packaging and clean-install checks |
| `runbooks/release-verification.md` | Evidence collection and release gate |
| `runbooks/troubleshooting.md` | Common failures and recovery |

## Templates

`templates/` contains ADR, feature spec, incident, release verification, agent
task, and AI onboarding prompt forms. Copy a template; do not edit it in place.

## Historical source brief

`agentcity/source-brief/` preserves the original build pack for provenance.
It contains assumptions that were later corrected (RAM, tool roles, foundation
choice). The corrected documents in this repository are authoritative.

## Documentation gates

```powershell
python scripts/check-docs.py
```

`check-docs.py` is the gate. It enforces required documents, frontmatter, link
resolution, Mermaid fence starters, and manifest consistency.

`scripts/generate-context.py` is not a check: it rewrites
`docs/agentcity/state-of-build.md` and `docs/repo-map.md` from the manifest. Run
it only when you intend to update those files, and commit the result.
