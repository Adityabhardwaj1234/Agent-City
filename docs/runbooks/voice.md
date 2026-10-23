---
title: Voice Runbook
status: active
owner: engineering
last_verified: 2026-10-23
---

# Voice Runbook

Voice is push-to-talk first. It is an accessibility and speed feature, not a
permission bypass.

## 1. Defaults

| Setting | Default |
|---|---|
| Push-to-talk hotkey | Enabled after explicit setup |
| Streaming transcription | Plumbed when a provider supports it |
| Text-to-speech | Local Windows SAPI |
| Wake word | **Off**, opt-in only |
| Mic indicator | Always visible when capturing |
| Auto-send transcript | **Off**; transcript is editable |

## 2. Pipeline

```text
key down → capture microphone → stream frames
→ STT adapter → partial transcript → key up → final transcript
→ user edits → send to mission
```

Response:

```text
assistant text → TTS adapter → speaker
stop/barge-in → cancel playback and any queued speech
```

## 3. STT options

| Option | State | Notes |
|---|---|---|
| Gemini audio input (live) | Planned | Requires a key and quota |
| OpenAI/other provider | Not implemented | Adapter required |
| Local Whisper | Not planned for v1 | Too heavy for 7.8 GB with the rest |
| Browser Web Speech | Not default | Hidden cloud dependency; label if used |

The adapter interface:

```python
class SttAdapter(Protocol):
    async def start(self, session_id: str) -> None: ...
    async def push(self, chunk: bytes) -> None: ...
    async def finish(self) -> Transcript: ...
    async def cancel(self) -> None: ...
```

Every method has a timeout; cancel must stop transmission immediately.

## 4. TTS

- Local SAPI via PowerShell or `pyttsx3` for the first release.
- No cloud TTS by default.
- Barge-in stops playback within 200 ms.
- Long responses are chunked; the first chunk starts quickly.
- A failed audio device degrades to text with a visible notice.

## 5. Permissions and privacy

- Ask for microphone permission on first use and explain why.
- The indicator shows recording and transmitting states separately.
- Audio is sent only when a provider is configured and the user starts PTT.
- Do not retain raw audio by default; keep the transcript with the message.
- A voice transcript is never an approval for a consequential action.
- Wake word requires opt-in, a visible indicator, and a local detector; it is off
  in a fresh install.

## 6. Interaction rules

- PTT key down starts; key up finalizes.
- Escape cancels capture and discards the partial transcript.
- The transcript is editable before submission.
- While TTS is speaking, a new PTT press barges in and stops playback.
- Hot-mic audio is never interpreted as intent without an explicit send.
- The mode (Ask/Plan/Execute) cannot be raised by voice alone.

## 7. Failure handling

| Failure | Behavior |
|---|---|
| No microphone | Disable PTT with an explanation |
| Permission denied | Show settings guidance; keep text input |
| Provider error | Keep audio local, show error, do not auto-retry blindly |
| Network loss | Stop streaming, mark transcript partial |
| TTS device busy | Text response remains; notify |
| Hotkey conflict | Detect registration failure and ask for another key |

## 8. Testing

- Mock audio source with a fixture waveform; no real microphone in CI.
- Test silence, noise, long speech, and immediate cancel.
- Test provider failure and device removal mid-stream.
- Test barge-in and transcript editing.
- Test that a transcript cannot approve an action.

## 9. Evidence

Record the adapter, provider, mode (offline/live/mocked), latency, and result.
Never store raw user audio in evidence.
