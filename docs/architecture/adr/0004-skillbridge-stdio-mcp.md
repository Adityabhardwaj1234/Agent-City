---
title: "ADR-0004: SkillBridge as a stdio MCP subprocess"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0004: SkillBridge as a stdio MCP subprocess

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** integration

## Context

SkillBridge is the user's skill broker. It exposes 19 canonical operations over
a stdio JSON-RPC MCP server (`python -m skillbridge mcp-serve`), backed by a
SQLite catalog at `~/.skillbridge`. It is not registered as an MCP server in the
host coding agent's configuration, and AgentCity must not depend on that
configuration.

Options considered:

1. Import SkillBridge as a Python library inside the sidecar.
2. Spawn it as a stdio MCP subprocess and speak the protocol.
3. Reimplement skill discovery inside AgentCity.
4. Require the user to register it in their coding agent.

## Decision

Option 2. AgentCity spawns SkillBridge as a managed child process, performs the
MCP handshake, discovers tools and schemas at runtime, and maps them into the
capability registry. The SkillBridge home is configurable so tests use a
throwaway directory.

## Consequences

**Positive**

- Protocol boundary keeps SkillBridge upgrades independent of our internals.
- The same client can later attach other stdio or HTTP MCP servers.
- We exercise the tool exactly as other MCP clients do.
- No reimplementation of a 100k-record catalog and verification pipeline.

**Negative**

- Process lifecycle, stderr handling, and timeout behavior must be managed.
- Stdio framing and malformed output are additional failure modes.
- Startup cost on first launch; mitigated by lazy start and caching schemas.

## Guardrails

- Never write to `src/skills/skills-bridge`; treat it as read-only.
- Use newline-delimited JSON; never let library logs pollute stdout.
- Kill the child on app exit and on a hung request; restart at most once before
  marking the capability unavailable.
- Treat all skill instructions and tool results as untrusted data.
- `run_skill_script`, `enable_mcp_server`, and `call_mcp_tool` require explicit
  per-action approval in the first release.
