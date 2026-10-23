#!/usr/bin/env python3
"""Validate the AgentCity documentation pack.

Checks, without third-party dependencies:
  - required documents exist;
  - documentation frontmatter is complete and uses valid values;
  - relative Markdown links resolve;
  - Mermaid blocks are non-empty and start with a supported diagram type;
  - PROJECT_MANIFEST.json parses and references existing paths;
  - the feature status vocabulary is respected.

Exit code 0 when clean, 1 when violations are found.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

REQUIRED_DOCS = [
    "docs/AI_CONTEXT.md",
    "docs/PROJECT_MANIFEST.json",
    "docs/README.md",
    "docs/agentcity/PRD.md",
    "docs/agentcity/architecture.md",
    "docs/agentcity/implementation-plan.md",
    "docs/agentcity/deliverables-and-acceptance.md",
    "docs/agentcity/reuse-audit.md",
    "docs/agentcity/tooling-inventory.md",
    "docs/agentcity/agent-roster.md",
    "docs/agentcity/model-routing.md",
    "docs/agentcity/test-plan.md",
    "docs/agentcity/security-model.md",
    "docs/agentcity/decision-log.md",
    "docs/agentcity/glossary.md",
    "docs/agentcity/state-of-build.md",
    "docs/architecture/overview.md",
    "docs/architecture/diagrams.md",
    "docs/architecture/contracts.md",
    "docs/architecture/data-model.md",
    "docs/engineering/coding-standards.md",
    "docs/engineering/backend-guidelines.md",
    "docs/engineering/frontend-guidelines.md",
    "docs/engineering/testing-strategy.md",
    "docs/engineering/debugging-playbook.md",
    "docs/engineering/git-workflow.md",
    "docs/engineering/documentation-standards.md",
    "docs/engineering/security-standards.md",
    "docs/engineering/performance-budget.md",
    "docs/engineering/change-recipes.md",
    "docs/runbooks/dev-setup.md",
    "docs/runbooks/provider-setup.md",
    "docs/runbooks/mcp-and-skills.md",
    "docs/runbooks/desktop-permissions.md",
    "docs/runbooks/voice.md",
    "docs/runbooks/packaging.md",
    "docs/runbooks/release-verification.md",
    "docs/runbooks/troubleshooting.md",
    "docs/templates/ai-onboarding-prompt.md",
]

FRONTMATTER_EXEMPT_PREFIXES = (
    "docs/templates/",
    "docs/agentcity/source-brief/",
    "docs/agentcity/evidence/",
)

VALID_STATUS = {"draft", "active", "planned", "superseded", "archived"}
REQUIRED_KEYS = {"title", "status", "owner", "last_verified"}

MERMAID_STARTERS = {
    "flowchart",
    "graph",
    "sequenceDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "classDiagram",
    "journey",
    "gantt",
    "pie",
    "mindmap",
    "timeline",
    "quadrantChart",
    "C4Context",
    "C4Container",
    "block-beta",
    "gitGraph",
}

FEATURE_STATUS = {"implemented", "partial", "blocked", "planned"}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(errors: list[str], path: Path, message: str) -> None:
    try:
        label = path.relative_to(ROOT).as_posix()
    except ValueError:
        label = str(path)
    errors.append(f"{label}: {message}")


def read_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_frontmatter(errors: list[str], path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(FRONTMATTER_EXEMPT_PREFIXES) or rel == "docs/AI_CONTEXT.md":
        if rel != "docs/AI_CONTEXT.md":
            return
    data = read_frontmatter(path)
    if data is None:
        fail(errors, path, "missing YAML frontmatter")
        return
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        fail(errors, path, f"frontmatter missing keys: {', '.join(sorted(missing))}")
    status = data.get("status", "")
    if status and status not in VALID_STATUS:
        fail(errors, path, f"invalid status '{status}' (allowed: {sorted(VALID_STATUS)})")
    verified = data.get("last_verified", "")
    if verified:
        if not DATE_RE.match(verified):
            fail(errors, path, f"last_verified must be YYYY-MM-DD, got '{verified}'")
        else:
            try:
                date.fromisoformat(verified)
            except ValueError:
                fail(errors, path, f"last_verified is not a valid date: '{verified}'")


def check_links(errors: list[str], path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for raw in LINK_RE.findall(text):
        target = raw.strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "<" in target or ">" in target:
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            fail(errors, path, f"broken link: {target}")


def check_mermaid(errors: list[str], path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```mermaid\n(.*?)```", text, flags=re.DOTALL)
    if text.count("```mermaid") != len(blocks):
        fail(errors, path, "unbalanced Mermaid code fence")
        return
    for index, block in enumerate(blocks, start=1):
        body = block.strip()
        if not body:
            fail(errors, path, f"Mermaid block {index} is empty")
            continue
        first = body.split(maxsplit=1)[0]
        if first not in MERMAID_STARTERS:
            fail(errors, path, f"Mermaid block {index} starts with unsupported type '{first}'")


def check_manifest(errors: list[str]) -> None:
    manifest_path = ROOT / "docs/PROJECT_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, manifest_path, f"invalid JSON: {exc}")
        return

    for key in ("schema_version", "project", "environment", "paths", "features", "tools"):
        if key not in manifest:
            fail(errors, manifest_path, f"missing top-level key '{key}'")

    features = manifest.get("features", [])
    if not isinstance(features, list) or not features:
        fail(errors, manifest_path, "features must be a non-empty list")
        return

    seen: set[str] = set()
    for feature in features:
        fid = feature.get("id")
        status = feature.get("status")
        if not fid or not isinstance(fid, str):
            fail(errors, manifest_path, "feature without a string id")
            continue
        if fid in seen:
            fail(errors, manifest_path, f"duplicate feature id '{fid}'")
        seen.add(fid)
        if status not in FEATURE_STATUS:
            fail(errors, manifest_path, f"feature '{fid}' has invalid status '{status}'")
        evidence = feature.get("evidence")
        if evidence and not (ROOT / evidence).exists():
            fail(errors, manifest_path, f"feature '{fid}' evidence path missing: {evidence}")

    docs_map = manifest.get("docs", {})
    if isinstance(docs_map, dict):
        for label, rel in docs_map.items():
            if isinstance(rel, str) and not (ROOT / rel).exists():
                fail(errors, manifest_path, f"docs['{label}'] points to missing {rel}")


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"{rel}: required document is missing")

    md_files = sorted(DOCS.rglob("*.md"))
    for path in md_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(FRONTMATTER_EXEMPT_PREFIXES) and rel != "docs/templates/ai-onboarding-prompt.md":
            continue
        check_frontmatter(errors, path)
        check_links(errors, path)
        check_mermaid(errors, path)

    for root_file in ("AGENTS.md", "README.md", "THIRD_PARTY_NOTICES.md"):
        path = ROOT / root_file
        if path.exists():
            check_links(errors, path)

    check_manifest(errors)

    if errors:
        print(f"Documentation check FAILED ({len(errors)} issue(s)):\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Documentation check OK: {len(md_files)} Markdown files validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
