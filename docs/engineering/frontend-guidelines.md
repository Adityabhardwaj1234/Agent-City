---
title: Frontend Guidelines
status: active
owner: frontend
last_verified: 2026-10-23
---

# Frontend Guidelines

The renderer is a dense operational interface, not a marketing page. It must be
fast, accessible, honest, and readable under pressure.

## 1. Stack (M1 target)

| Concern | Choice | Reason |
|---|---|---|
| Shell | Electron with context isolation and sandbox | Trusted desktop APIs |
| UI | React 19 + TypeScript + Vite | Mature, fast, testable |
| Routing | React Router | Simple route-level code splitting |
| Styling | CSS variables + utility classes (Tailwind if adopted) | Consistent tokens, small runtime |
| Icons | Lucide (bundled) | Legible vector icons, no emoji as primary icons |
| Primitive dialogs/menus | Radix or custom accessible primitives | Focus and keyboard correctness |
| Server state | Typed fetch client + normalized event store | One source of truth |
| Tests | Vitest + Testing Library, Playwright | Component and end-to-end |

Do not add a state library, charting framework, or 3D engine until a measured
need exists. The machine has 7.8 GB RAM.

## 2. Electron security

- `nodeIntegration: false`, `contextIsolation: true`, `sandbox: true`.
- No remote module, no `webview`, no loading remote content in the app window.
- Strict CSP: bundled scripts only, no inline script, no `unsafe-eval`.
- The preload exposes a small typed object; it never exposes `ipcRenderer`.
- Main validates every IPC payload and every sender frame.
- The renderer never receives the sidecar token from disk; main hands it a
  scoped client configuration.
- External links open only via an allowlisted `https` handler from a gesture.

## 3. Application structure

```text
src/desktop/
  electron/
    main.ts          # windows, sidecar, hotkeys, menu
    preload.ts       # typed bridge
    sidecar.ts       # spawn, handshake, health, restart
    ipc.ts           # channel schemas and handlers
  src/
    app/             # providers, router, error boundary
    components/      # shared primitives
    features/
      overview/      # City Overview
      command/       # chat and voice
      missions/
      agents/
      workspace/
      desktop/
      research/
      projects/
      capabilities/
      artifacts/
      automations/
      settings/
    lib/             # api client, sse, event store, formatting
    styles/          # tokens and global styles
  tests/
```

## 4. Layout and visual language

- Three-zone shell: left navigation, center workspace, right inspector.
- A persistent status bar shows mode (Offline/Live), provider health, capture and
  microphone state, active mission count, and emergency stop.
- Dark graphite/ink background; cyan/teal for active systems; amber for
  approvals; green for verified success; red for faults. Never color alone.
- Information density over decoration. Tables and lists are always available.
- The City Overview map shows real nodes and edges from the mission DAG and
  delegation events. No idle animation pretending work is happening.
- Motion: event-driven pulses, dependency-edge travel, approval emphasis.
  Respect `prefers-reduced-motion`; provide a reduced-motion toggle.
- Every number shows its source and timestamp on hover or in the inspector.

## 5. State rules

- Server state is fetched, not invented. Loading, empty, error, and blocked are
  distinct states.
- The SSE event store is normalized by mission and task. Components select what
  they need; no prop drilling of whole mission objects.
- Reconnect uses the last sequence; deduplicate by event id.
- Optimistic updates are limited to reversible UI preferences. Never optimistically
  mark a mission complete or an approval approved.
- Demo Mode is a separate provider that injects visibly labeled fixtures; it
  must be impossible to confuse with real data.

## 6. Components

- One responsibility per component; keep route files under ~200 lines.
- Props are explicit and typed; no `any`.
- Controlled inputs for forms; validate before submit; show field errors.
- Buttons reflect real state: `idle`, `busy`, `disabled` with a reason, `error`.
- Destructive or consequential actions require a confirmation that shows the
  exact target and payload preview.
- Never use color as the only status signal.

## 7. Accessibility

- Keyboard reachable: navigation, mission list, approval actions, stop.
- Visible focus ring on every interactive element.
- Semantic landmarks and headings; no div-only buttons.
- Live regions for mission status and approval changes.
- Contrast at least 4.5:1 for body text and 3:1 for large text.
- Dialog focus trap and restore; Escape closes non-destructive dialogs.
- Test at 125% scaling and with reduced motion.

## 8. Performance

- Route-level code splitting.
- Virtualize lists over 100 items.
- Bound the in-memory event list; older events load on demand.
- Avoid layout thrash in the map; use transform/opacity for motion.
- No polling when SSE is available; one reconnect loop with backoff.
- Keep the renderer idle under ~200 MB; measure at each milestone.

## 9. Copy and honesty

- Name the actual state: “Offline Mode — no provider configured”, not “Thinking”.
- Never show a percentage that is not computed from real progress.
- Say “blocked” and give the fix; do not leave a spinner.
- Costs show currency, model, and source (reported/estimated/unavailable).
- Errors are actionable: what failed, what to do, where the log is.

## 10. Testing

- Component tests for loading/empty/error/blocked and keyboard paths.
- Store tests for event ordering, deduplication, and reconnect.
- Playwright journeys: launch, create mission, approve, reject, cancel, restart,
  open artifact, stop desktop session.
- No snapshot-only tests for critical status rendering.

## 11. Frontend anti-patterns

- Dead buttons, placeholder handlers, or “coming soon” in a shipped route.
- Fake activity animation or fabricated metrics.
- Direct `fetch` from components without the typed client.
- Storing the API token in `localStorage` or `sessionStorage`.
- Using `dangerouslySetInnerHTML` for model or tool output.
- Blocking the UI thread with parsing large payloads.
- Adding heavy UI dependencies without a measured reason.
