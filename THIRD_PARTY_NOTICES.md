# Third-Party Notices

AgentCity is MIT-licensed (see `LICENSE`). This file records third-party
components, their licenses, and how they are used. It must be updated whenever
a dependency, vendored tool, asset, or model is added.

## Development-time tools (cloned locally, not committed)

These tools live in `src/skills/` after running `scripts/bootstrap-skills.ps1`.
They are excluded from Git; the repository records name, pinned commit, and
license instead of vendoring the source.

| Tool | Pinned commit | License | Use |
|---|---|---|---|
| ADK Agent Builder Skill | `a74d73b20447c8d9beab999bbfa5ddb7d6d748b4` | Apache-2.0 | Generate, validate, test, and evaluate ADK agent packages during development |
| SkillBridge | `25c352e6219e0f9ca45bdbc9a2ff0bafae4ddb06` | MIT | Runtime MCP broker for discovering, verifying, loading, and invoking skills |

Published copies of AgentCity must not rely on these local clones being present
in the source tree. The runtime must locate SkillBridge through configuration
and fail with an actionable diagnostic when it is missing.

## Runtime dependencies

| Component | License | Notes |
|---|---|---|
| google-adk | Apache-2.0 | Agent runtime and evaluation |
| FastAPI / Uvicorn | MIT | Local HTTP API |
| Pydantic | MIT | Typed contracts |
| SQLite | Public Domain | Local state |
| Electron | MIT | Desktop shell (planned) |
| React / React DOM | MIT | Renderer UI (planned) |
| Vite / TypeScript | MIT / Apache-2.0 | Build tooling (planned) |
| mcp (Python SDK) | MIT | MCP stdio client (planned) |
| pyautogui | BSD-3-Clause | Input fallback (planned) |
| pywinauto | BSD-3-Clause | Windows UI Automation (planned) |
| Pillow | HPND | Screenshot handling (planned) |

## Explicitly rejected as bundled source

Personal Jarvis (Apache-2.0), OpenHands (MIT), OpenDex (MIT), Mission Control
(MIT), and OpenComputer (MIT) are reference projects. No source is copied.
Rationale is recorded in `docs/agentcity/reuse-audit.md` and ADR-0001.

## Assets

AgentCity uses original iconography and typography. No upstream logos, brand
art, model checkpoints, or voice models are bundled. Any future asset or model
download must record its own license here; a repository's code license does not
cover its weights or binary assets.
