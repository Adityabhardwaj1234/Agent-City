---
title: Provider Setup Runbook
status: active
owner: engineering
last_verified: 2026-10-23
---

# Provider Setup Runbook

AgentCity works without a provider in Offline Mode. Live Mode requires a real
credential and an explicit health check.

## 1. Current state

No provider key is configured on this machine. Live ADK reasoning is **blocked**
until one is supplied. The app must show this clearly and offer Offline Mode.

## 2. Gemini (default)

1. Create an API key in Google AI Studio (a product subscription does not grant
   API access).
2. Store it in the OS credential store through Settings → Providers.
3. For development only, you may set `GEMINI_API_KEY` in `.env`.
4. Restart the sidecar or use “Test connection”.
5. The health check performs one minimal call and records latency and model id.

Do not paste a key into chat, a prompt, a screenshot, an issue, or a commit.

## 3. Verification (planned M2)

```powershell
# planned
uv run python -m agentcity.diagnostics provider-check --provider gemini
```

Expected: `connected`, model id, latency, and quota headers when available.
Failure states:

| Result | Meaning | Action |
|---|---|---|
| `provider_auth_failed` | Key invalid or revoked | Replace the credential |
| `provider_quota_exceeded` | Daily/minute limit hit | Wait for reset; use Offline Mode |
| `provider_unavailable` | Network or outage | Retry later; do not switch silently |
| `model_not_found` | Bad model id | Choose a model the SDK supports |

## 4. Quota discipline

The free tier is approximately 5 requests per minute and 20 requests per day per
model. Rules:

- Run offline tests first; they must pass with zero calls.
- Live smoke tests use a minimum interval of 13 seconds.
- A daily budget guard stops before exhaustion.
- 429 is retried with exponential backoff and jitter, then marked blocked with a
  reset time.
- Never loop a failed request to “warm up” a model.

## 5. Other providers

Adapters for OpenAI, Anthropic, Vertex AI, or local servers are **not
implemented**. The Agent Builder lists providers it can generate for, but that
is not proof that AgentCity is configured for them. Adding one requires:

- a typed adapter with health check;
- capability metadata (tools, structured output, vision, audio, context);
- a model routing entry and fallback;
- credential storage and redaction review;
- offline fakes and a paced live test;
- an update to `model-routing.md` and the manifest.

## 6. Egress disclosure

Before the first live run, show the user:

- which provider receives data;
- which data classes are sent (text, files, screenshots, audio);
- whether the data leaves the device;
- how to disable vision or file egress.

Defaults: no screenshots to the cloud, no file content outside approved roots,
no secrets ever.

## 7. Revocation

- Removing a key disables Live Mode immediately.
- In-flight missions are marked blocked, not failed, with a clear reason.
- No silent fallback to another provider or to Offline Mode mid-mission.
- The app never stores the key in SQLite, localStorage, or logs.

## 8. Troubleshooting

| Symptom | Check |
|---|---|
| Live Mode greyed out | Credential missing or health check failed |
| HTTP 500 from ADK | Provider 429/auth error surfaced as 500; inspect detail |
| Intermittent timeouts | Network, proxy, or quota; retry with backoff |
| Cost shows “unavailable” | No pricing data; tokens may still be shown |
| Wrong model behavior | Verify the model id and routing record |

## 9. Evidence

Record the health check command, result, model, latency, and date. Never record
the key or a full provider response containing account data.
