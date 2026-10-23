---
title: Glossary
status: active
owner: product
last_verified: 2026-10-23
---

# Glossary

| Term | Meaning in AgentCity |
|---|---|
| **Mission** | A user objective with a persisted plan, tasks, budget, approvals, and evidence |
| **Task** | One node in a mission DAG, owned by an agent, with a contract and acceptance criteria |
| **Run** | One execution attempt of a task by an agent |
| **Agent** | An ADK-defined reasoning role with instructions, tools, and limits |
| **Team template** | A reusable roster and policy for a class of missions |
| **Capability** | A registered tool or action with a schema, risk class, and scope |
| **Policy broker** | Deterministic code that allows or denies an action |
| **Approval** | A single-use, expiring, bound token that authorizes one action |
| **Event** | An immutable, sequenced record of a state change |
| **Ledger** | The ordered event store in SQLite |
| **Artifact** | A produced file or output with provenance and a hash |
| **Verifier** | Independent agent that checks acceptance evidence before completion |
| **City Overview** | The operational home view of live missions, agents, and health |
| **Command** | The chat and voice workspace |
| **Mode** | Ask, Plan, Execute with approval, Autopilot bounded, Desktop watch |
| **Offline Mode** | Deterministic execution with no model provider calls |
| **Live Mode** | Execution with a configured, health-checked model provider |
| **SkillBridge** | The local skill catalog and stdio MCP broker |
| **Broker tool** | One of SkillBridge's 19 MCP operations |
| **MCP** | Model Context Protocol used to expose tools and data |
| **ADK** | Google Agent Development Kit, the agent runtime |
| **Agent Builder** | The build-time CLI that generates and validates ADK projects |
| **Worktree** | An isolated Git working directory for a coding worker |
| **Handshake** | The per-launch port and token file used by the shell to reach the sidecar |
| **Sidecar** | The Python FastAPI process managed by Electron |
| **UI Automation** | Windows accessibility API used for native control before vision fallback |
| **Emergency stop** | A hotkey and button path that halts desktop actions without the model |
| **Evidence** | A command output or report that proves a claim |
| **Blocked** | A state where a required credential, permission, or dependency is absent |
| **Quarantine** | Isolation of a failed or unsafe skill or catalog |
| **Schema version** | The compatibility version of an event or contract payload |
| **FTS5** | SQLite full-text search used for local retrieval |
| **WAL** | SQLite write-ahead logging mode used for concurrent reads |
