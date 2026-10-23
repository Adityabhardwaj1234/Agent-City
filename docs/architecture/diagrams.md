---
title: System Diagrams
status: active
owner: architecture
last_verified: 2026-10-23
---

# System Diagrams

All diagrams are Mermaid and render on GitHub. They describe the target design;
areas marked planned are not implemented until the status matrix says so. Keep
node names stable when updating: they are referenced by ADRs and tests.

## 1. System context

```mermaid
flowchart LR
  User["User"] --> App["AgentCity"]
  App --> Providers["Model providers"]
  App --> Skills["SkillBridge broker"]
  App --> OtherMCP["Other MCP servers"]
  App --> CLIs["Coding CLIs"]
  App --> OS["Windows OS"]
  App --> Files["Approved files and projects"]
  Providers --> Cloud["Cloud inference"]
  Skills --> Catalog["Local skill catalog"]
  OtherMCP --> Remote["Remote services"]
  CLIs --> Repos["Repositories and worktrees"]
```

## 2. Containers

```mermaid
flowchart TD
  subgraph Desktop["Electron desktop"]
    Main["Main process"]
    Preload["Preload bridge"]
    Renderer["React renderer"]
  end
  subgraph Sidecar["Python sidecar"]
    API["FastAPI gateway"]
    Engine["Mission Engine"]
    Policy["Policy broker"]
    ADK["ADK runtime"]
    MCP["MCP client"]
    DesktopSvc["Desktop service"]
    Voice["Voice adapters"]
    Events["Event ledger"]
    Store["Artifact store"]
  end
  DB[("SQLite WAL")]
  Main -->|"spawn and monitor"| API
  Renderer --> Preload
  Preload --> Main
  Main -->|"typed IPC"| API
  API --> Engine
  Engine --> Policy
  Engine --> ADK
  Engine --> MCP
  Engine --> DesktopSvc
  Engine --> Voice
  Engine --> Events
  Engine --> Store
  Events --> DB
  Store --> DB
  ADK --> Providers["Model providers"]
  MCP --> SkillBridge["SkillBridge stdio"]
  DesktopSvc --> OS["Windows APIs"]
```

## 3. Backend components

```mermaid
flowchart TD
  API["api/ routes and SSE"] --> Auth["auth middleware"]
  API --> Missions["missions service"]
  Missions --> Lifecycle["lifecycle state machine"]
  Missions --> Scheduler["task scheduler"]
  Scheduler --> Runner["ADK step runner"]
  Scheduler --> Tools["tool gateway"]
  Tools --> Policy["policy broker"]
  Policy --> Approvals["approval queue"]
  Tools --> Registry["capability registry"]
  Registry --> SkillBridge["SkillBridge adapter"]
  Registry --> LocalTools["local tools"]
  Registry --> Coding["coding CLI adapter"]
  Lifecycle --> Ledger["event ledger"]
  Runner --> Ledger
  Tools --> Ledger
  Approvals --> Ledger
  Ledger --> DB[("SQLite")]
  Runner --> Artifacts["artifact service"]
  Missions --> Budget["budget service"]
  Budget --> Ledger
```

## 4. Mission lifecycle

```mermaid
stateDiagram-v2
  [*] --> draft
  draft --> planned: plan persisted
  planned --> waiting_for_approval: gated action
  planned --> queued: no gate
  waiting_for_approval --> queued: user approves
  waiting_for_approval --> cancelled: user rejects or expires
  queued --> running: worker starts
  running --> verifying: tasks complete
  running --> failed: unrecoverable error
  running --> cancelled: user cancels
  running --> blocked: policy or dependency blocks
  verifying --> completed: verifier passes
  verifying --> failed: verifier rejects
  verifying --> blocked: evidence missing
  failed --> queued: explicit retry
  blocked --> queued: blocker resolved
  completed --> [*]
  failed --> [*]
  cancelled --> [*]
  blocked --> [*]
```

## 5. Mission execution sequence

```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant UI as Renderer
  participant API as FastAPI
  participant E as Mission Engine
  participant A as ADK Runtime
  participant P as Policy Broker
  participant T as Tool Adapter
  participant V as Verifier
  U->>UI: Submit request and mode
  UI->>API: POST /missions
  API->>E: create mission
  E->>A: plan request with budget and scope
  A-->>E: typed MissionPlan
  E->>P: classify plan actions
  P-->>E: approval requirements
  E-->>API: persist plan and events
  API-->>UI: SSE mission.created and mission.planned
  U->>UI: Approve gated action
  UI->>API: POST /approvals/{id}/approve
  API->>E: resume mission
  E->>A: execute task
  A->>T: tool request
  T->>P: authorize invocation
  P-->>T: allow with scope
  T-->>A: tool result
  A-->>E: task result
  E->>V: verify acceptance criteria
  V-->>E: pass with artifact references
  E-->>API: mission.completed
  API-->>UI: SSE completion and artifact link
```

## 6. Approval and risk flow

```mermaid
flowchart TD
  Request["Tool or action request"] --> Schema{"Schema valid?"}
  Schema -->|"no"| DenySchema["Deny: invalid_request"]
  Schema -->|"yes"| Classify["Classify risk and scope"]
  Classify --> Blocked{"Blocked class?"}
  Blocked -->|"yes"| DenyBlocked["Deny: policy_blocked"]
  Blocked -->|"no"| Policy{"Mission policy allows?"}
  Policy -->|"no"| DenyPolicy["Deny: not_permitted"]
  Policy -->|"yes"| Gated{"Approval required?"}
  Gated -->|"no"| Execute["Execute with timeout and caps"]
  Gated -->|"yes"| Queue["Persist approval request"]
  Queue --> Wait["Wait for user decision"]
  Wait -->|"approve"| Execute
  Wait -->|"reject"| DenyUser["Deny: user_rejected"]
  Wait -->|"expire"| DenyExpire["Deny: approval_expired"]
  Execute --> Audit["Persist tool_invocation and audit event"]
```

## 7. Data model

```mermaid
erDiagram
  PROJECTS ||--o{ CONVERSATIONS : contains
  PROJECTS ||--o{ MISSIONS : owns
  PROJECTS ||--o{ MEMORY_ENTRIES : scopes
  CONVERSATIONS ||--o{ MESSAGES : contains
  MISSIONS ||--o{ MISSION_TASKS : plans
  MISSIONS ||--o{ AGENT_RUNS : executes
  MISSIONS ||--o{ EVENTS : records
  MISSIONS ||--o{ ARTIFACTS : produces
  MISSIONS ||--o{ BUDGET_EVENTS : tracks
  MISSIONS ||--o{ APPROVAL_REQUESTS : gates
  MISSIONS ||--o{ VERIFICATIONS : checks
  MISSION_TASKS ||--o{ AGENT_RUNS : assigned
  MISSION_TASKS ||--o{ TOOL_INVOCATIONS : invokes
  AGENT_RUNS ||--o{ TOOL_INVOCATIONS : performs
  AGENTS ||--o{ AGENT_RUNS : identity
  TEAM_TEMPLATES ||--o{ MISSIONS : instantiates
  TOOL_INVOCATIONS ||--o{ APPROVAL_REQUESTS : may_require
  ARTIFACTS ||--o{ VERIFICATIONS : evidence
  ROUTINES ||--o{ MISSIONS : triggers
  EVALUATION_RUNS ||--o{ EVALUATION_CASES : contains
```

## 8. Trust boundaries and egress

```mermaid
flowchart LR
  subgraph Trusted["Trusted deterministic core"]
    Policy["Policy broker"]
    Engine["Mission engine"]
    Ledger["Event ledger"]
    DB[("SQLite")]
  end
  subgraph Semi["Semi-trusted adapters"]
    ADK["ADK runtime"]
    MCP["MCP client"]
    Desktop["Desktop service"]
    Tools["Tool adapters"]
  end
  subgraph Untrusted["Untrusted input"]
    Web["Web and documents"]
    SkillText["Skill instructions"]
    ToolOut["Tool output"]
    Screen["OCR and screenshots"]
  end
  Untrusted --> Semi
  Semi --> Policy
  Policy --> Engine
  Engine --> Ledger
  Ledger --> DB
  Engine -->|"explicit egress only"| Cloud["Model provider"]
  Engine -->|"local only"| Local["Local tools"]
```

## 9. Startup and sidecar handshake

```mermaid
sequenceDiagram
  autonumber
  participant Main as Electron main
  participant Side as Python sidecar
  participant FS as Handshake file
  participant UI as Renderer
  Main->>Side: spawn with random token and data dir
  Side->>Side: open SQLite, run migrations
  Side->>Side: bind 127.0.0.1 ephemeral port
  Side->>FS: write port and token with restricted ACL
  Side-->>Main: ready line with pid and version
  Main->>FS: read handshake
  Main->>Side: GET /health with bearer token
  Side-->>Main: health, version, migration, provider status
  Main->>UI: load renderer with scoped config
  UI->>Side: GET /missions with bearer token
  Main->>Side: kill on quit
  Side->>FS: delete handshake
```

## 10. Event streaming and replay

```mermaid
sequenceDiagram
  autonumber
  participant UI as Renderer
  participant API as FastAPI
  participant DB as Event ledger
  UI->>API: GET /events?after=0
  API->>DB: select ordered events
  DB-->>API: page of events
  API-->>UI: replay page and cursor
  UI->>API: GET /events/stream?after=42
  loop every state change
    API->>DB: append event in transaction
    API-->>UI: SSE event with sequence
  end
  Note over UI: Connection lost
  UI->>API: reconnect with last sequence
  API-->>UI: replay only missed events
```

## 11. SkillBridge MCP integration

```mermaid
sequenceDiagram
  autonumber
  participant E as Mission Engine
  participant C as MCP client
  participant SB as SkillBridge broker
  participant DB as SkillBridge catalog
  E->>C: health check and list tools
  C->>SB: initialize and tools/list
  SB-->>C: 19 broker tools with schemas
  C-->>E: capability registry entries
  E->>C: call search_skills with query
  C->>SB: tools/call search_skills
  SB->>DB: FTS query
  DB-->>SB: matches
  SB-->>C: compact results
  C-->>E: typed results and latency
  Note over C,SB: Timeout, malformed output, and crash are tested paths
```

## 12. Desktop control

```mermaid
sequenceDiagram
  autonumber
  participant U as User
  participant UI as Renderer
  participant D as Desktop service
  participant P as Policy broker
  participant OS as Windows
  U->>UI: Grant capture scope and duration
  UI->>D: create permission grant
  D->>D: start visible capture indicator
  U->>UI: Run desktop task
  UI->>D: request minutes
  D->>P: authorize target window and app
  P-->>D: allow narrow scope
  D->>OS: capture frame and UIA tree
  OS-->>D: observation with timestamp
  D-->>UI: display observation and proposed actions
  U->>UI: Approve action batch
  D->>OS: execute actions
  D->>OS: fresh observation
  D->>P: verify expected result
  P-->>D: pass or fail closed
  U->>UI: Emergency stop
  UI->>D: cancel queue and in-flight action
```

## 13. Voice pipeline

```mermaid
flowchart LR
  Mic["Microphone"] --> VAD["Voice activity and push-to-talk"]
  VAD --> Cap["Renderer audio capture"]
  Cap --> STT["STT adapter"]
  STT --> Transcript["Editable transcript"]
  Transcript --> Intent["Mission intent"]
  Intent --> Engine["Mission engine"]
  Engine --> TTS["TTS adapter"]
  TTS --> Speaker["Speaker"]
  Stop["Stop and barge-in"] --> Cap
  Stop --> TTS
```

## 14. ADK agent topology

```mermaid
flowchart TD
  Root["agentcity_root"] --> Planner["planner"]
  Root --> Research["researcher"]
  Root --> Architect["architect"]
  Root --> Coder["coder"]
  Root --> Debug["debugger"]
  Root --> Test["test_engineer"]
  Root --> Review["reviewer"]
  Root --> Security["security_guard"]
  Root --> Desktop["desktop_operator"]
  Root --> Verifier["verifier"]
  Planner --> Plan["Typed MissionPlan"]
  Plan --> Engine["Mission Engine"]
  Coder --> Worktree["Assigned worktree"]
  Desktop --> DesktopSvc["Governed desktop service"]
  Verifier --> Evidence["Acceptance evidence"]
```

## 15. Packaging topology

```mermaid
flowchart TD
  Source["Source tree"] --> Build["Build pipeline"]
  Build --> Renderer["Renderer bundle"]
  Build --> Main["Electron main bundle"]
  Build --> Sidecar["Python sidecar or frozen binary"]
  Renderer --> Installer["Signed NSIS installer"]
  Main --> Installer
  Sidecar --> Installer
  Installer --> Install["Clean Windows install"]
  Install --> Smoke["Launch, health, migration, uninstall check"]
```

## 16. Development worktrees

```mermaid
flowchart LR
  Main["main"] --> Int["integration branch"]
  Int --> WT1["worktree: backend"]
  Int --> WT2["worktree: desktop"]
  Int --> WT3["worktree: qa"]
  WT1 --> Merge["Reviewed merges"]
  WT2 --> Merge
  WT3 --> Merge
  Merge --> Main
```
