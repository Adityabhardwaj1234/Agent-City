# AgentCity — Open-Source Reuse and License Audit

Research snapshot prepared 23 October 2026. The agent must re-check current repository metadata, commit, dependencies, licensing, activity, and security before cloning or importing code. Search results and READMEs are not substitutes for a code audit.

## Candidate matrix

| Candidate | Potential use | Research finding | Main caution | Decision rule |
|---|---|---|---|---|
| [Personal Jarvis](https://github.com/Robee99/PersonalJarvis) | Primary foundation candidate for desktop shell, voice, missions, agents, tool gating, local API, worktrees, artifact workspace | Closest end-to-end functional match; docs describe chat/voice, browser/desktop control, coding CLIs, MCP, routines, approvals, and a visual team map | Current releases v2+ use Apache-2.0; releases through 1.6.0 remain MIT. Preserve NOTICE, third-party license notices, trademark guidance, and source attribution. Inspect architecture and whether its native orchestrator can be adapted to ADK without duplicating runtimes. | Prefer as the first base to evaluate if there is no viable local codebase. Do not assume latest code is MIT. Record exact commit/tag and compatibility findings. |
| [Google ADK Python](https://github.com/google/adk-python) | Primary AgentCity-owned agent runtime and evaluation framework | Official open-source code-first toolkit; Apache-2.0. Official docs describe team delegation, session state, guardrail callbacks, workflows, MCP tools, voice/live agents, observability and evaluations. | Check exact current supported API/version. Do not generate code against guessed or stale examples. | Use as orchestration backbone and integrate with the user's ADK Agent Builder. |
| [OpenHands](https://github.com/OpenHands/OpenHands) | Coding-agent server/SDK/API and agent operations patterns | Separates frontend/control plane, agent server/SDK, client, and automation | Large system and separate components; integrating the whole platform may add unnecessary runtime/dependency weight. Check license and security policy at chosen commit. | Integrate only if a real coding-agent feature gap justifies the extra process; otherwise use as an adapter/reference. |
| [OpenDex](https://github.com/wassgha/opendex) | Electron/React voice-first shell concepts and provider adapters | README describes Electron, electron-vite, React, Tailwind, Vercel AI SDK, pluggable voice; MIT | Appears much narrower/early compared with the full product; native input dependency and cross-platform packaging need checking. | Fallback foundation if Personal Jarvis fails technical/architecture audit, or cherry-pick only well-isolated MIT-compatible utilities with notices. |
| [Mission Control](https://github.com/mjsorribas/mission-control-dashboard) | Dashboard, event stream, task/agent panels, logs, budgets, quality gates | README describes self-hosted agent fleet dashboard, SQLite, WebSocket/SSE, many panels, MIT | Maintainers label it alpha and warn APIs/schemas may change. It is an orchestration dashboard, not automatically a secure desktop control app. | Reuse small independent components only after integration/security review; treat as a UI/API reference if schemas conflict. |
| [OpenComputer](https://github.com/andykr1k/OpenComputer) | Screen capture, keyboard/mouse control, local-first computer-use approach | README describes cross-platform Electron shell and OpenAI-compatible model boundary; MIT | Current README calls Windows/macOS experimental and lists missing features; avoid inheriting permission gaps or model hardware assumptions. | Use as reference or isolated driver candidate after Windows-specific tests; prefer native Windows UI Automation when appropriate. |
| [Model Context Protocol](https://modelcontextprotocol.io/introduction) | Standard protocol for tool/server integrations including Skills Bridge if registered as MCP | Official docs describe a standard interface to tools, data sources and workflows | An MCP schema does not guarantee that a server or tool is safe. Apply capability restrictions and human approval. | Use as the integration seam; inspect exact Skills Bridge registration and schemas first. |

## Recommended reuse strategy

1. Inspect existing local workspace first. Do not assume new project means empty project.
2. If blank, audit Personal Jarvis at current main/stable tag as first option. The goal is to **extend/adapt**, not simply rebrand or blindly merge.
3. Preserve healthy existing voice, desktop controls, CLI integrations, artifact handling, and permission broker where code quality allows.
4. Route AgentCity-owned missions through Google ADK. Use a thin integration adapter to the existing base rather than starting two uncoordinated orchestrators.
5. Use the user's ADK Agent Builder and Skills Bridge tools through their real installed interfaces. Store generated agent config/definitions, not only transient generated text.
6. Examine code licenses, assets/model weights, dependency licenses, NOTICE, trademark policy, and third-party notices before copying source or assets. Record source path/URL and pinned commit for every imported component.
7. Only add OpenHands, Mission Control, OpenDex or OpenComputer after describing the uncovered need and proving the extra component doesn't duplicate the base.
8. Every upstream repository must be pinned to a tag/commit or vendored subset, with a written upstream-update strategy.

## License and provenance gate

Before reuse, inventory `LICENSE`, `NOTICE`, package dependencies, model/speech assets, UI images/fonts, and license metadata. For Apache-2.0 components, preserve license, required notices, patent/license terms, and mark modified files where required. For MIT components, preserve copyright and permission notices. Model checkpoints and downloadable voice assets keep their own terms; a repository's code license does not automatically license model weights or every binary.

Do not misrepresent a derivative product as entirely authored from scratch. Choose MIT for newly authored AgentCity code unless the audited combination or chosen base requires another strategy; get a clearly reviewed root license and third-party attribution plan before release.

## Reuse acceptance checklist

- [ ] Base decision has a documented rationale.
- [ ] Exact commit/tag and license checked.
- [ ] Existing build/tests reproduced before changes or baseline limitations documented.
- [ ] No upstream brand/logo/assets copied without permission/terms review.
- [ ] Third-party notices/attributions maintained.
- [ ] Duplicate frameworks eliminated or justified.
- [ ] New user-facing functionality works end-to-end with the actual ADK runtime and Skills Bridge integration.
- [ ] Dependency footprint and resource usage measured on the target Windows machine.
