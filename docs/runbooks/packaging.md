---
title: Packaging Runbook
status: active
owner: release
last_verified: 2026-10-23
---

# Packaging Runbook

Packaging does not exist yet. This runbook defines the target so M6 does not
invent it under pressure.

## 1. Target

- Windows 11 x64 NSIS installer, per-user install by default.
- Signed when a certificate is available; otherwise the release is labeled
  **unsigned** and SmartScreen behavior is documented.
- Bundled renderer, Electron main, and a Python runtime or frozen sidecar.
- No Docker, no external database, no admin requirement to run.
- App data under `%LOCALAPPDATA%\AgentCity`; uninstall keeps user data unless
  the user chooses to remove it.

## 2. Sidecar packaging options

| Option | Pros | Cons |
|---|---|---|
| Frozen sidecar (PyInstaller/Nuitka) | No Python prerequisite | Large, slow build, antivirus false positives possible |
| Bundle a Python runtime + wheels | Predictable, easier debugging | Larger installer, more moving parts |
| Require system Python + `uv sync` | Small installer | Bad first-run experience; version drift |

Decision: evaluate the frozen sidecar first in M6; fall back to a bundled
runtime if freezing breaks ADK, MCP subprocesses, or native modules. Record the
measured size, startup time, and failure modes.

## 3. Build steps (target)

```powershell
# planned
npm ci --workspace src/desktop
npm run build --workspace src/desktop
uv sync --project src/backend
uv run pytest --project src/backend
python scripts/check-docs.py
npm run dist --workspace src/desktop
```

The Electron builder config must exclude:

- `.env`, keys, tokens, handshake files;
- `src/skills/**` source (unless a bundled sidecar requires it);
- test output, coverage, databases, logs;
- source maps unless explicitly needed.

## 4. Clean-install smoke test

On a clean Windows profile or a fresh VM snapshot:

1. Install with the produced installer.
2. Launch with no provider configured.
3. Confirm Offline Mode, health, and a completed test mission.
4. Confirm the sidecar port is loopback and the token file is removed on exit.
5. Confirm no Python/Node development prerequisites are needed.
6. Confirm SQLite is created under `%LOCALAPPDATA%`.
7. Upgrade over the previous version; confirm migrations and data retention.
8. Uninstall; confirm the app is removed and the data retention prompt works.

Record every step and result in the release report.

## 5. Signing

- Obtain a code-signing certificate or use a trusted signing service.
- Sign the installer and the executables.
- Verify with `Get-AuthenticodeSignature`.
- Document the certificate subject and timestamp authority.
- Never commit a certificate or password.

## 6. Updates

- v1: manual download and install. No silent auto-update.
- A future updater must verify signatures, support rollback, and never update
  during an active mission.
- Database migrations must be forward-compatible with the previous release.

## 7. Uninstall and data

- Uninstall removes program files.
- User data is retained by default; the uninstaller offers removal.
- Logs and screenshots follow retention, not the installer.
- Secrets in the OS credential store are removed explicitly.

## 8. Release checklist

- [ ] Version bumped in the manifest and package metadata.
- [ ] Full test matrix and evidence complete.
- [ ] Security and license scans pass.
- [ ] No secrets or runtime data in the installer.
- [ ] Clean-install and upgrade tests pass.
- [ ] Release verification report written.
- [ ] Tag created only after all critical checks pass.

## 9. Known risks

- Antivirus false positives on frozen Python executables.
- Long paths in OneDrive during build.
- Native module ABI mismatch after an Electron upgrade.
- Installer size and first-run extraction time on a slow disk.
- Unsigned builds triggering SmartScreen warnings.

Each risk gets a measured result before release, not an assumption.
