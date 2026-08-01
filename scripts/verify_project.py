#!/usr/bin/env python3
"""Offline verification for public files and optional full Obsidian vault."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import taskctl


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TRACKED_PREFIXES = (
    "00_首頁/",
    "01_規範總覽/",
    "02_法源與原文索引/",
    "03_主題整合/",
    "04_合規流程映射/",
    "05_跨版本與法律狀態比較/",
    "06_案例命令與許可/",
    "07_申報通報與期限/",
    "08_設備與系統卡/",
    "99_資料治理/",
)
FORBIDDEN_EXTENSIONS = {".pdf", ".xml", ".pem", ".key", ".p12", ".pfx"}
REQUIRED_HTML_IDS = {
    "regulation-grid",
    "deadline-body",
    "automation-panel",
    "sync-badge",
    "detail-dialog",
}


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "id" and value:
                self.ids.add(value)


def git_candidate_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return sorted(set(line for line in result.stdout.splitlines() if line))


def verify(full_vault: bool = False) -> dict:
    passed: list[str] = []
    errors: list[str] = []

    required = [
        "AGENTS.md",
        "GEMINI.md",
        "TODO.md",
        "docs/AI_RUNBOOK.md",
        "docs/LEGAL_STATUS_DECISION_TABLE.md",
        "tasks/queue.json",
        "index.html",
        "assets/app.js",
        "assets/site.css",
        "data/regulatory-status.json",
        "data/review-baseline.json",
        "scripts/update_regulatory_data.py",
        "scripts/taskctl.py",
        "scripts/agent_preflight.py",
    ]
    missing = [item for item in required if not (ROOT / item).exists()]
    if missing:
        errors.append("missing files: " + ", ".join(missing))
    else:
        passed.append("required files")

    candidates = git_candidate_files()
    boundary_violations = [
        item
        for item in candidates
        if item.startswith(FORBIDDEN_TRACKED_PREFIXES)
        or Path(item).suffix.lower() in FORBIDDEN_EXTENSIONS
    ]
    if boundary_violations:
        errors.append("public boundary violations: " + ", ".join(boundary_violations))
    else:
        passed.append("public file boundary")

    for relative in ["tasks/queue.json", "data/regulatory-status.json", "data/review-baseline.json"]:
        try:
            json.loads((ROOT / relative).read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON {relative}: {exc}")
    if not any(item.startswith("invalid JSON") for item in errors):
        passed.append("JSON syntax")

    try:
        queue = taskctl.load_queue()
        queue_errors = taskctl.validate_queue(queue)
        if queue_errors:
            errors.extend("task queue: " + item for item in queue_errors)
        elif len(queue["tasks"]) < 30:
            errors.append("task queue unexpectedly has fewer than 30 tasks")
        else:
            passed.append(f"task queue ({len(queue['tasks'])} tasks)")
    except Exception as exc:
        errors.append("task queue unreadable: " + str(exc))

    try:
        feed = json.loads((ROOT / "data" / "regulatory-status.json").read_text(encoding="utf-8"))
        sections = feed["ecfr"]["sections"]
        if len(sections) != 35:
            errors.append(f"regulatory feed section count is {len(sections)}, expected 35")
        if feed.get("errors"):
            errors.append("regulatory feed contains source errors")
        if feed.get("review", {}).get("status") not in {"current", "review_required"}:
            errors.append("regulatory feed has invalid review status")
        if not any(item.startswith("regulatory feed") for item in errors):
            passed.append("regulatory feed schema")
    except Exception as exc:
        errors.append("regulatory feed unreadable: " + str(exc))

    try:
        parser = IdParser()
        parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        missing_ids = sorted(REQUIRED_HTML_IDS - parser.ids)
        if missing_ids:
            errors.append("index.html missing ids: " + ", ".join(missing_ids))
        else:
            passed.append("HTML structure")
    except Exception as exc:
        errors.append("HTML parse failed: " + str(exc))

    for relative in [
        "scripts/update_regulatory_data.py",
        "scripts/taskctl.py",
        "scripts/agent_preflight.py",
        "scripts/verify_project.py",
    ]:
        try:
            source = (ROOT / relative).read_text(encoding="utf-8")
            compile(source, str(ROOT / relative), "exec")
        except Exception as exc:
            errors.append(f"Python syntax {relative}: {exc}")
    if not any(item.startswith("Python syntax") for item in errors):
        passed.append("Python syntax")

    node = shutil.which("node")
    if node:
        result = subprocess.run(
            [node, "--check", "assets/app.js"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append("JavaScript syntax: " + (result.stderr.strip() or result.stdout.strip()))
        else:
            passed.append("JavaScript syntax")
    else:
        passed.append("JavaScript syntax skipped: node unavailable")

    whitespace_files = [
        ROOT / "AGENTS.md",
        ROOT / "GEMINI.md",
        ROOT / "TODO.md",
        ROOT / "docs" / "AI_RUNBOOK.md",
        ROOT / "docs" / "LEGAL_STATUS_DECISION_TABLE.md",
    ]
    whitespace_errors = []
    for path in whitespace_files:
        if not path.exists():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.endswith(" ") or line.endswith("\t"):
                whitespace_errors.append(f"{path.relative_to(ROOT)}:{line_number}")
    if whitespace_errors:
        errors.append("trailing whitespace: " + ", ".join(whitespace_errors))
    else:
        passed.append("handoff document whitespace")

    if full_vault:
        health = ROOT / "99_資料治理" / "fcc_kb_health.py"
        if not health.exists():
            errors.append("full vault health script missing")
        else:
            result = subprocess.run(
                [sys.executable, str(health), "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode:
                errors.append("full vault health failed: " + result.stdout.strip())
            else:
                passed.append("full vault health")

    return {"ok": not errors, "mode": "full_vault" if full_vault else "public", "passed": passed, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-vault", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(full_vault=args.full_vault)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PASS" if result["ok"] else "FAIL")
        for item in result["passed"]:
            print(f"[PASS] {item}")
        for item in result["errors"]:
            print(f"[FAIL] {item}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
