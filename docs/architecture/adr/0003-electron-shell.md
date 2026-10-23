---
title: "ADR-0003: Electron and React for the desktop shell"
status: active
owner: architecture
last_verified: 2026-10-23
---

# ADR-0003: Electron and React for the desktop shell

- **Status:** Accepted
- **Date:** 2026-10-23
- **Decision owner:** architecture

## Context

The shell must host a dense, live operational UI, audio capture and playback,
screen capture, Windows automation, global hotkeys, and a Python sidecar. The
machine is Windows 11 with 7.8 GB RAM, Intel UHD graphics, Node 24, and no Rust
toolchain.

Candidates:

| Option | Assessment |
|---|---|
| Electron + React | Mature on Windows, predictable Chromium, strong audio and automation ecosystem, large but workable memory footprint, no extra toolchain |
| Tauri 2 + React | Lighter runtime, but requires Rust and a compile toolchain that is absent, and native audio/automation integration is more bespoke |
| PySide6 | Native and already used by Personal Jarvis, but would discard the React design system and require a different UI skill set |
| Browser-only | Cannot provide trusted desktop automation, global stop, or a native installer |

## Decision

Use Electron with a context-isolated preload bridge and a React + TypeScript +
Vite renderer. Keep `nodeIntegration` off, sandbox on, and validate every IPC
payload. Target an idle footprint under 600 MB for the whole app.

## Consequences

**Positive**

- One Chromium version and consistent rendering, accessibility, and media APIs.
- Mature packaging and installer tooling on Windows.
- The renderer can reuse standard React tooling and tests.
- The global emergency-stop hotkey lives in a trusted process.

**Negative**

- Higher memory than a native shell; must be measured and bounded.
- Electron security requires discipline (CSP, no remote content, no raw IPC).
- Native modules require rebuilds when Electron changes.

## Guardrails

- No `nodeIntegration`, no `enableRemoteModule`, no loading remote URLs in the
  main window.
- CSP restricts scripts to the bundled origin; no inline script.
- Renderer never receives filesystem paths or the API token from disk directly.
- Measure idle and active memory at each milestone; regress above budget gets a
  fix or a documented exception.
