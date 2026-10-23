---
title: AI Onboarding Prompt
status: active
owner: integration
last_verified: 2026-10-23
---

# AI Onboarding Prompt

Paste the block below into a fresh coding agent before asking it to work on
AgentCity. It points to the canonical context instead of duplicating it.

```text
You are working on AgentCity, a Windows-first local-first desktop AI command
center built around Google ADK, SkillBridge, Electron/React, and a Python
sidecar. Read these files in order before changing anything:

1. AGENTS.md
2. docs/AI_CONTEXT.md
3. docs/PROJECT_MANIFEST.json
4. docs/agentcity/state-of-build.md
5. The document relevant to your task (docs/README.md has reading orders)

Non-negotiables:
- Real execution only. No fake agents, metrics, costs, or dead controls.
- The LLM proposes; deterministic code decides permissions.
- Secrets never enter Git, logs, prompts, fixtures, or screenshots.
- Docs, tests, and the status matrix update in the same change.
- Every success claim has a command and evidence under docs/agentcity/evidence/.
- Do not edit src/skills/**; those are pinned read-only clones.
- Do not touch the real SkillBridge catalog at ~/.skillbridge; it is currently
  corrupt and must be recovered by the user. Use a temp --home for tests.
- The target machine has 7.8 GB RAM and no provider key. Offline Mode is the
  default; live tests are blocked unless a key is configured.
- Use real worktrees for parallel work and verify the path and branch from
  inside each worker.
- Run `python scripts/check-docs.py` before committing docs. Regenerate context
  with `python scripts/generate-context.py` after manifest changes.

Before starting:
1. State what you will change and which contracts are affected.
2. Name the tests you will run and the evidence you will capture.
3. If a requirement is ambiguous, inspect the repo first; ask only if the answer
   is not discoverable.

When done, report: files changed, commands and results, pass/fail/skip/blocked,
known risks, and the commit SHA. Do not claim completion from a compile or a
screenshot alone.
```

## Why this prompt exists

New agents otherwise re-derive the project from the file tree, repeat corrected
mistakes from the original build pack, or claim unverified success. The prompt
anchors them to the current truth and the evidence rules.

## Maintenance

Update this prompt when the read order, non-negotiables, or environment facts
change. Keep it short; link rather than duplicate.
