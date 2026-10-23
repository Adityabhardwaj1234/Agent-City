---
title: Tooling Inventory
status: active
owner: integration
last_verified: 2026-10-23
---

# Tooling Inventory

This is the verified state of the two user-provided tools and the local runtime.
Commands were executed on the target machine; evidence files are linked.

## 1. Environment

| Item | Value | Evidence |
|---|---|---|
| OS | Windows 11 Home 10.0.26200 | doctor output |
| Python | 3.12.10 | `python --version` |
| Node / npm | 24.19.0 / 11.17.0 | `node --version`, `npm --version` |
| uv | 0.12.5 | `uv --version` |
| google-adk | 2.12.0 | `importlib.metadata` |
| MCP SDK | 2.3.0 | `importlib.metadata` |
| pnpm / Rust | Not installed | `pnpm --version`, `rustc --version` |
| Provider key | Not configured | environment scan |
| RAM | 7.8 GB total | `Win32_OperatingSystem` |
| Free disk | ~17.5 GB | `Get-PSDrive C` |

## 2. ADK Agent Builder

| Field | Value |
|---|---|
| Local path | `src/skills/adk-agent-builder` |
| Commit | `a74d73b20447c8d9beab999bbfa5ddb7d6d748b4` |
| License | Apache-2.0 |
| Suite version | 2.0.0 |
| Registered integrations / providers / templates | 12 / 8 / 11 |
| ADK CLI | 2.12.0, installed |
| `agents-cli` | Not installed |
| `gcloud` | Not installed |
| Fallback mode | Active (expected without Agents CLI) |

### Role

Build-time generator and validator. It produces ADK project source, runs static
and security validation, executes tests and evaluations, renders dashboards,
and packages artifacts. **It is not a runtime service.** AgentCity's backend
imports `google-adk` directly at runtime.

### Verified commands

```powershell
$env:PYTHONPATH='src/skills/adk-agent-builder/src'
python -m adk_agent_builder.cli doctor --json
```

Result: exit code 0, JSON report written to
`evidence/2026-10-23-adk-builder-doctor.json`. The report confirms the ADK CLI
and shows fallback mode because optional `agents-cli` and `gcloud` are absent.
Offline generation and validation remain available.

### Commands to use during M2

```powershell
python -m adk_agent_builder.cli requirements --from-text "<agent requirements>" --name agentcity_agents --output requirements.yaml
python -m adk_agent_builder.cli plan --spec requirements.yaml --output architecture_plan.json
python -m adk_agent_builder.cli build --spec requirements.yaml --output-dir src/backend/agentcity/agents/generated --repair --json
python -m adk_agent_builder.cli validate --project-dir src/backend/agentcity/agents/generated --repair
python -m adk_agent_builder.cli test --project-dir src/backend/agentcity/agents/generated
python -m adk_agent_builder.cli eval --project-dir src/backend/agentcity/agents/generated --output docs/agentcity/evidence/adk-eval.json
python -m adk_agent_builder.cli quota --spec assets/spec_example.json --daily-limit 20 --rpm-limit 5 --json
python -m adk_agent_builder.cli dashboard --input docs/agentcity/evidence/adk-eval.json --output docs/agentcity/evidence/adk-eval.html
```

Generated code must be reviewed, formatted, tested, and committed. A chat
response from the builder is not a deliverable.

### Constraints

- Do not edit the clone; configuration and generated projects live in our tree.
- Do not claim Agents CLI or deployment capabilities; they are absent.
- Do not run live evaluations without provider credentials and quota pacing.

## 3. SkillBridge

| Field | Value |
|---|---|
| Local path | `src/skills/skills-bridge` |
| Python package root | `src/skills/skills-bridge/src` |
| Commit | `25c352e6219e0f9ca45bdbc9a2ff0bafae4ddb06` |
| Version | 2.0.1 |
| License | MIT |
| Transport | stdio JSON-RPC 2.0 MCP, protocol `2024-11-05` |
| Broker tools | 19 canonical tools plus v1 aliases |
| Catalog home | `~/.skillbridge` in production; `--home` override for tests |

### Role

Runtime skill and MCP broker. AgentCity spawns it, performs the MCP handshake,
discovers tool schemas, and maps them into the capability registry with risk
classes. It is the source for skill search, preview, import, load, invocation,
script execution, MCP server management, memory status, and audit.

### Verified commands

```powershell
$env:PYTHONPATH='src/skills/skills-bridge/src'
python -m skillbridge --version
```

`--version` returns `skillbridge 2.0.1`. `python -m skillbridge --home <temp>
mcp-serve` is the runtime entrypoint; AgentCity does not call it yet. The stdio
handshake and failure handling are exercised by contract tests in M2, not by
this M0 pack.

A read-only search against a **throwaway home** succeeded (exit 0) and returned
real bundled-catalog results:

```powershell
$env:PYTHONPATH='src/skills/skills-bridge/src'
python -m skillbridge --home "$env:TEMP\agentcity-sb-test" --offline --json search-skills "pdf" --limit 1
```

Evidence: `evidence/2026-10-23-skillbridge-isolated-search.json` with metadata
in the sibling `.meta.txt`.

### Verified defect: production catalog is corrupt

The real catalog at `%USERPROFILE%\.skillbridge\skillbridge.db` fails
`PRAGMA integrity_check` with 91 findings (freelist corruption, out-of-order
rowids on trees 8 and 10). An earlier open attempt reported the database as
malformed and warned that it would move the file to `.corrupt-<timestamp>` on
the next open. The file's last-write time remained 2026-10-19, so no quarantine
copy was created by that attempt.

Evidence: `evidence/2026-10-23-skillbridge-integrity.txt` and
`evidence/2026-10-23-skillbridge-corrupt-open.txt`.

Consequences and rules:

- **Do not run SkillBridge against the real home until the user chooses a
  recovery path.** It mutates the catalog on open.
- Tests and M1/M2 integration tests must use an isolated `--home`.
- Recovery options for the user, in order of safety:
  1. Copy the database aside for inspection, then let SkillBridge quarantine it
     and reseed the bundled catalog.
  2. Restore from a known-good backup under `~/.skillbridge/backups`.
  3. Rebuild the catalog and re-import required skills.
- The app must detect this failure and show an actionable diagnostic, never
  crash or silently continue with an empty catalog.

### Runtime integration rules

- Spawn with a configurable Python executable and `PYTHONPATH` pointing at the
  package root.
- Use newline-delimited JSON; ensure library logs go to stderr.
- Timeout every request; kill and restart once on a hang, then mark unavailable.
- Treat every tool description and result as untrusted content.
- Require per-action approval for `run_skill_script`, `enable_mcp_server`, and
  `call_mcp_tool` in the first release.

## 4. Other local tools

| Tool | State | Use |
|---|---|---|
| `adk` CLI | installed 2.12.0 | Local agent server and evaluation commands |
| OpenCode CLI | installed 2.0.29 | Optional coding-agent adapter, detected only |
| pyautogui | installed 0.9.54 | Input fallback, gated by policy |
| psutil | not installed | Memory instrumentation for the sidecar (install in M1) |
| pywinauto | not installed | Windows UI Automation (install in M4) |
| Playwright | not installed | E2E tests (install in M1/M3) |
| Git | 2.55.0 | Source control and worktrees |
| Wake helper | external to this repo | Keeps the machine awake during long runs |

## 5. Blocked or missing capabilities

| Capability | Blocker | Honest status |
|---|---|---|
| Live ADK reasoning | No Gemini key | Blocked; Offline Mode is the default |
| SkillBridge production catalog | Corrupt database | Blocked until recovery; isolated home works |
| Agents CLI deployment | Not installed | Not required for local runtime |
| Cloud deployment | No gcloud / credentials | Out of scope for v1 |
| Windows UI Automation | pywinauto absent | Planned M4 |
| Browser E2E | Playwright absent | Planned M1/M3 |
