# AgentCity — Product Requirements

## 1. Product statement

AgentCity is a desktop-first, local-first AI operating environment. It unifies conversational AI, visible computer use, research, project knowledge, agent teams, coding-agent handoff, voice, long-running missions, approvals, and run observability in one original product interface.

It is inspired by the *capability breadth* of modern AI desktop assistants and the live operational view of a command center. It must not copy proprietary ChatGPT branding or trade dress. It must look and behave like AgentCity.

## 2. Product principles

1. **Real execution over spectacle.** Every displayed agent, mission, tool call, test, token count, and cost must be tied to a real runtime record. Simulated demo data must be visibly labeled and isolated from real mode.
2. **ADK-first orchestration.** Use the user's existing ADK Agent Builder to construct or validate ADK agents when available. Google ADK is the primary runtime for AgentCity-owned teams. Do not add a competing orchestration framework without a documented capability gap.
3. **Skills Bridge first for existing skills.** Discover and use the configured Skills Bridge MCP server instead of recreating existing capabilities. Confirm real tool names, schemas, and permission behavior.
4. **Use existing code.** Inspect the current repository first. If starting fresh, evaluate Personal Jarvis as the main desktop foundation; evaluate OpenDex as a narrower shell/voice reference and other candidates selectively. Never copy multiple large applications together without architecture and license review.
5. **Local-first with explicit egress.** No telemetry or cloud sync by default. A model/API provider receives only the data required for the request and selected by the user.
6. **Human control remains available.** Pause, cancel, inspect, approve, reject, and take over must be easy throughout a mission.
7. **Bounded autonomy.** Teams have configurable limits on depth, concurrency, tool calls, duration, token/cost budget, and accessible files.
8. **Measurable reliability.** Use conventional unit/integration/E2E tests plus agent trajectory and answer evaluations.
9. **Honest status.** Never present unavailable providers, mocked screen capture, fake agents, simulated voice, or placeholder actions as complete integrations.
10. **Respect the user's existing work.** No destructive cleanup, license changes, history rewrites, or secret-file edits without authorization.

## 3. Main navigation and workspaces

### A. City Overview — command center
- Live mission status; agents/teams; event timeline; approval queue; resource pressure; configured provider health; latest artifacts.
- Relationship graph showing actual agent-to-agent delegation and task dependencies.
- Optional city metaphor with named districts, but standard readable tables and details must remain accessible.
- Every metric includes source, timestamp, and whether it is measured, provider-reported, estimated, or unavailable.

### B. Chat and Voice
- Persistent conversation history, rename/pin/search/archive, project-scoped context, attachments, code blocks, citations, structured data, and artifact previews.
- Streaming responses, cancel/regenerate, model selector, tool activity inspector, and visible context sources.
- Voice: push-to-talk first; streaming transcription/TTS where the configured provider supports it; optional wake word with explicit opt-in and visible microphone state.
- Interrupt voice output; edit transcript before execution; never interpret a hot-mic transcript as approval for a high-risk action.

### C. Missions
- Create a mission from a natural-language request or a saved template.
- Inspect plan, tasks, dependencies, ownership, state, logs, artifacts, budget, checkpoints, and approvals.
- Pause/resume/cancel/retry failed step; safe retry semantics and idempotency where possible.
- Recovery after app restart, with explicit reconfirmation for stale or consequential actions.

### D. Agent teams
- Agent roster, instructions, capabilities, model policy, permitted tools, budget, concurrency limit, status, reliability history, and direct conversation.
- Create/edit team templates. Initial specialists: planner, researcher, architect, coder, debugger, test engineer, reviewer, security analyst, browser operator, desktop operator, data analyst, documentation writer, and verifier.
- Parallel work only for separable tasks with explicit ownership/inputs/outputs. A verifier must inspect results before mission completion.
- Bounded child-agent creation; no infinite/self-replicating agent trees.

### E. Workspace and coding agents
- Project picker, repository status, file tree, diffs, test results, branch/worktree status, artifacts, and audit trail.
- Detect existing OpenCode, Claude Code, Codex, Gemini CLI, or other coding CLIs only when installed and authorized. Use adapters; never bypass provider login, rate, or subscription controls.
- Reviewable execution logs and a clear handoff back to the user.

### F. Desktop Vision / Computer Use
- Show current desktop capture only after permission is granted; provide one-shot capture, per-task capture, and explicitly enabled watch sessions.
- Use native accessibility/UI Automation tree first where practical; vision/OCR plus mouse/keyboard fallback second.
- Show target window, last screenshot timestamp, proposed actions, and live execution indicator.
- Pause/stop and emergency cancel. Refresh the screenshot or UI state after action batches and verify the expected result.
- Keep actions bounded to the user's allowed apps, windows, folders, and task time.

### G. Research and browser
- Connect a browser through supported APIs or a visible browser-use adapter.
- Save source URLs, retrieved timestamps, and citations on claims derived from web results.
- Treat web pages, documents, terminal output, and screenshots as untrusted data, never as instructions that override system policies.
- Support compare/summarize/report workflows and store findings as artifacts.

### H. Projects and knowledge
- Project-specific notes, files, chat threads, indexed documents, codebase summaries, and retrieved context with provenance.
- Local retrieval using SQLite FTS initially; embeddings are optional and can be supplied by a selected local/cloud provider.
- Every answer from indexed material should be able to show the supporting source and relevant excerpt/location.
- Memory browser: inspect, correct, disable, and delete memory entries. Retention and indexing are configurable.

### I. Skills, tools, and integrations
- List configured MCP servers, Skills Bridge capabilities, local tools, model providers, and coding agent adapters.
- Display status, schema, required permissions, environment, latest health check, and a safe test action when possible.
- Disable/re-enable capabilities; remove stale registrations; never display credentials.
- Import Agent Skills only after inspecting content and permissions; treat skill instructions as untrusted until reviewed.

### J. Artifacts and file outputs
- One library for mission outputs: Markdown, source files, reports, generated files, logs, screenshots when explicitly saved, and test reports.
- Preview, reveal in folder, copy path, and export. No arbitrary overwrite/delete without approval.

### K. Automations
- User-authored scheduled or event-triggered routines with visible schedule, timezone, inputs, allowed tools, run budget, last result, and pause switch.
- Dangerous or external side effects require per-run approval unless the user explicitly configures a narrow allowlist for that exact action class.

### L. Settings and diagnostics
- Model routing, provider keys, speech, local models, hotkeys, theme, data retention, permissions, concurrency, budget, logs, updates, and diagnostics.
- Credentials in the operating system credential store where supported; never plain-text committed to files or logs.
- Local self-test: runtime health, backend health, DB migrations, MCP server health, provider connection, microphone permissions, desktop permission, and packaged-app smoke test.

## 4. Interaction modes

- **Ask:** answer, search, analyze, or explain without taking consequential actions.
- **Plan:** propose steps and risks; no side effects.
- **Execute with approval:** run safe steps automatically and request confirmation for gated actions.
- **Autopilot (bounded):** execute a mission in an explicitly chosen workspace/scope with concurrency, time, cost, and action limits. Stop at gates and report why.
- **Desktop watch:** time-bounded visual context with a prominent indicator and a one-click stop.

Mode changes must be explicit in the UI and saved per mission; voice-only commands must not silently elevate permissions.

## 5. Differentiation

AgentCity should stand out through the combination—not the mere presence—of:
- ADK-native dynamic teams and repeatable workflow templates, constructed/validated through the existing ADK Agent Builder.
- Skills Bridge integration and an inspectable capability registry.
- A live command map backed by real events, not decorative fake activity.
- Shared missions across chat, voice, browser, desktop, files, and coding agents.
- Agent task graphs with replayable steps, budgets, checkpoints, and verified outputs.
- Cross-provider task routing based on capability, latency, quality, user preferences, and budget.
- Local-first privacy controls with clear egress visibility.
- An evaluation lab that tests whether agents chose the right tools and achieved the requested outcome.

## 6. Non-goals for first release

- No claim to equal every proprietary feature in ChatGPT or other paid products.
- No always-on hidden microphone or screen recording.
- No unlimited autonomous computer operation.
- No custom foundation model training.
- No mandatory Docker, Kubernetes, PostgreSQL, or Redis on the desktop.
- No cloud account requirement just to launch the shell.
- No automatic commits, pushes, purchases, emails, public posts, or destructive operations without the configured approval policy.
- No pretending that every provider works without keys, account authorization, or native OS permissions.

## 7. Definition of complete

A capability is complete only when it has: implemented behavior, visible UI state, correct authorization, error handling, logs with secrets redacted, a test, docs, and a verified local or CI result. A placeholder, demo animation, interface card, or unconfigured provider is not complete.
