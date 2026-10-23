# AgentCity Build Pack

This pack is the execution brief for building **AgentCity**, a local-first desktop AI command center built around Google's Agent Development Kit (ADK), the user's existing ADK Agent Builder, and their Skills Bridge MCP tool.

## Files

- `MASTER_BUILD_PROMPT.md` — paste this into the user's coding/orchestration environment as the main build task.
- `PRODUCT_REQUIREMENTS.md` — product scope, product principles, and prioritized capabilities.
- `ARCHITECTURE.md` — target architecture, runtime boundaries, event model, and state model.
- `IMPLEMENTATION_PLAN.md` — phases, worktree and agent delegation rules, dependencies, and delivery order.
- `ACCEPTANCE_TESTS.md` — quality gates, measurable acceptance criteria, and test scenarios.
- `REUSE_AUDIT.md` — reuse candidates, license caveats, and a repo-selection procedure.
- `SECURITY_MODEL.md` — desktop permissions, approvals, isolation, and privacy rules.

## How to use

1. Open the target AgentCity workspace in the environment that has your ADK Agent Builder and Skills Bridge MCP configured.
2. Start the main orchestrator/coding agent and paste the full contents of `MASTER_BUILD_PROMPT.md` as the task.
3. Attach the rest of this pack or copy the documents into the repository under `docs/agentcity/` before execution.
4. Require the agent to inspect local tools and MCP registrations to find the exact names and schemas of the custom ADK Agent Builder and Skills Bridge tools. The tool names are not guessed in this pack because those custom tools were not exposed in the current chat session.
5. Review the repo/license report and the proposed architecture gate before allowing invasive changes to any existing codebase.
6. Have the agent produce a runnable local app and a test report; do not treat a rendered dashboard, mocked integrations, or a successful compile as proof that every capability works.

## Important execution note

This pack is a research-backed implementation brief, not a claim that AgentCity has already been installed or tested on your PC. The local custom tools and your working repository were not available in this chat session. The master prompt tells your local agent to discover and use those tools, inspect the actual repository, implement the system, and verify it against the acceptance checklist.

## Research anchors

- Google ADK Python: https://github.com/google/adk-python (Apache 2.0)
- ADK multi-agent team tutorial: https://adk.dev/tutorials/agent-team/
- ADK workflows: https://adk.dev/workflows/
- ADK live and voice agents: https://adk.dev/live/
- ADK evaluation: https://adk.dev/evaluate/
- ADK MCP tools: https://adk.dev/tools-custom/mcp-tools/
- Model Context Protocol: https://modelcontextprotocol.io/introduction
- Personal Jarvis: https://github.com/Robee99/PersonalJarvis
- OpenHands: https://github.com/OpenHands/OpenHands
- OpenDex: https://github.com/wassgha/opendex
- Mission Control: https://github.com/mjsorribas/mission-control-dashboard
- OpenComputer: https://github.com/andykr1k/OpenComputer
