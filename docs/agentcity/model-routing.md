---
title: Model Routing and Provider Policy
status: active
owner: architecture
last_verified: 2026-10-23
---

# Model Routing and Provider Policy

## 1. Current availability

| Provider | Configured | Notes |
|---|---|---|
| Gemini (AI Studio key) | **No** | Required for live ADK reasoning |
| Vertex AI | No | No Google Cloud credentials |
| OpenAI / Anthropic | No | No keys; adapters not implemented |
| Local models | No | Hardware budget forbids automatic local inference |
| Offline Mode | **Yes** | Deterministic planner and local tools; no model calls |

The app must launch, plan, and complete Offline Mode missions with no key. Live
Mode is enabled only after a provider health check succeeds.

## 2. Selection policy

Route per task using, in order:

1. **Capability fit** — text, vision, audio, tool calling, structured output.
2. **Context requirement** — estimated input plus output must fit the model.
3. **Policy** — data classification and provider egress rules.
4. **Quality record** — evaluation results for that task class.
5. **Latency and budget** — user preference and remaining mission budget.
6. **Availability** — health, rate limit, and quota state.

A manual override always wins. The chosen model, provider, reason, fallback, and
usage label are recorded on the `agent_run`.

## 3. Default routing table

| Task class | Primary | Fallback | Why |
|---|---|---|---|
| Planning and decomposition | Gemini 2.5 Pro | 2.5 Flash | Multi-step structure quality |
| Review and verification | Gemini 2.5 Pro | 2.5 Flash | Independent judgment |
| Coding and debugging | Gemini 2.5 Pro | 2.5 Flash | Code reasoning |
| Research and summarization | Gemini 2.5 Flash | 2.5 Pro | Volume and cost |
| Desktop observation | Gemini 2.5 Flash | 2.5 Pro | Short, schema-bound calls |
| Security review | Gemini 2.5 Pro | Flash | Conservative judgment |
| Embeddings (optional) | Provider embedding model | None | Only if retrieval needs it |

Model identifiers must be verified against the installed ADK and provider at
implementation time. Do not hardcode a model string that the environment cannot
resolve; read it from `provider_profiles` with a validated default.

## 4. Quota reality

The Gemini free tier is documented in the Agent Builder references as roughly
**5 requests per minute** and **20 requests per day per model**, with 429 errors
sometimes surfacing as HTTP 500. Therefore:

- Offline tests run first and must pass with zero API calls.
- Live tests use a minimum interval of **13 seconds** and a daily budget guard.
- Retries use exponential backoff with jitter; no tight retry loops.
- A quota exhaustion marks the mission `blocked` with a reset time, not
  `failed`, and never silently falls back to another provider.
- Evaluation runs are split into a small live slice and a larger offline suite.

These numbers are provider policy, not a guarantee. Re-check them at runtime and
record the observed limit in diagnostics.

## 5. Usage and cost labeling

Every usage record has a `source` field:

| Source | Meaning |
|---|---|
| `provider_reported` | Exact values returned by the provider |
| `estimated` | Computed from token counts and a pinned price table |
| `unavailable` | No measurement; the UI shows “unavailable” |

Never fabricate a cost. If pricing is unknown, show tokens and label cost
unavailable. Display the currency, price date, and model in the tooltip.

## 6. Egress rules

Before sending data to a provider, the UI states which provider receives which
context. The default policy:

- No screen images to a cloud provider unless the user enabled vision egress.
- No file content outside the approved project roots.
- No secrets, environment dumps, or credential material ever.
- Redact local paths when they are not needed for the task.
- A mission records the provider and data classes it sent.

## 7. Coding-agent routing

Coding CLIs use their own authentication and quota. AgentCity:

- detects installed CLIs, never installs them silently;
- hands each worker a worktree, branch, file scope, and completion contract;
- captures exit code, changed files, diff, test output, and commit SHA;
- verifies the actual directory and branch rather than trusting self-report;
- never bypasses login, subscription, or rate limits.

## 8. Health checks

| Check | Frequency | Failure behavior |
|---|---|---|
| Provider credential present | On launch and settings save | Live Mode disabled, Offline Mode offered |
| Minimal model call | On explicit “Test connection” only | Show exact error code |
| Rate limit state | After each 429 | Backoff and surface reset time |
| SkillBridge broker | On launch and capability refresh | Mark unavailable with reason |
| Coding CLI | On workspace open | Show missing/unauthorized state |

Health checks must be cheap. Do not burn quota on every launch; use a cached
result with a timestamp and an explicit refresh action.

## 9. Routing record template

When M2 lands, fill `docs/agentcity/evidence/model-routing-record.md` with:

```text
Role:
Selected model/provider:
Reason:
Fallback:
Context/usage limits:
Known limitations:
Observed usage (source: provider_reported | estimated | unavailable):
Evaluation result:
Date and commit:
```
