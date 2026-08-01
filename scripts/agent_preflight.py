#!/usr/bin/env python3
"""Print an unambiguous handoff state before an agent edits anything."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import taskctl


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PUBLIC_FILES = [
    "AGENTS.md",
    "GEMINI.md",
    "TODO.md",
    "docs/AI_RUNBOOK.md",
    "docs/LEGAL_STATUS_DECISION_TABLE.md",
    "tasks/queue.json",
    "data/regulatory-status.json",
    "data/review-baseline.json",
    "scripts/taskctl.py",
    "scripts/verify_project.py",
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()

    mode = taskctl.detect_mode()
    missing = [item for item in REQUIRED_PUBLIC_FILES if not (ROOT / item).exists()]
    git_status = run(["git", "status", "--porcelain"])
    dirty_lines = [line for line in git_status.stdout.splitlines() if line.strip()]
    branch = run(["git", "branch", "--show-current"]).stdout.strip()
    head = run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
    remote = run(["git", "remote", "get-url", "origin"]).stdout.strip()

    queue_errors: list[str] = []
    next_task = None
    try:
        queue = taskctl.load_queue()
        queue_errors = taskctl.validate_queue(queue)
        if not queue_errors:
            eligible = taskctl.eligible_tasks(queue, mode)
            next_task = taskctl.task_payload(eligible[0], mode) if eligible else None
    except Exception as exc:
        queue_errors = [str(exc)]

    feed_error = None
    feed = None
    try:
        feed = json.loads((ROOT / "data" / "regulatory-status.json").read_text(encoding="utf-8"))
    except Exception as exc:
        feed_error = str(exc)

    blockers: list[str] = []
    if missing:
        blockers.append("missing required files: " + ", ".join(missing))
    if git_status.returncode != 0:
        blockers.append("git status failed")
    elif dirty_lines and not args.allow_dirty:
        blockers.append("git worktree is dirty; identify existing changes before editing")
    if queue_errors:
        blockers.append("task queue invalid")
    if feed_error:
        blockers.append("regulatory feed unreadable: " + feed_error)
    elif feed:
        if feed.get("errors"):
            blockers.append("regulatory feed contains source errors")
        if feed.get("review", {}).get("status") == "review_required":
            blockers.append("official source changed; perform human legal review before normal tasks")
    if not next_task:
        blockers.append("no eligible task for current environment mode")

    result = {
        "ready": not blockers,
        "mode": mode,
        "repository": {
            "branch": branch,
            "head": head,
            "remote": remote,
            "dirty": bool(dirty_lines),
            "dirty_entries": dirty_lines,
        },
        "regulatory_feed": None
        if not feed
        else {
            "generated_at": feed.get("generated_at"),
            "ecfr_up_to_date_as_of": feed.get("ecfr", {}).get("up_to_date_as_of"),
            "review_status": feed.get("review", {}).get("status"),
            "source_errors": feed.get("errors", []),
        },
        "queue": {
            "valid": not queue_errors,
            "errors": queue_errors,
            "next_task": next_task,
        },
        "blockers": blockers,
        "mandatory_read_order": [
            "AGENTS.md",
            "TODO.md",
            "docs/AI_RUNBOOK.md",
            "docs/LEGAL_STATUS_DECISION_TABLE.md",
        ],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("READY" if result["ready"] else "BLOCKED")
        print(f"MODE: {mode}")
        print(f"GIT: branch={branch} head={head} dirty={str(bool(dirty_lines)).lower()}")
        if result["regulatory_feed"]:
            item = result["regulatory_feed"]
            print(
                "SOURCE: "
                f"eCFR={item['ecfr_up_to_date_as_of']} "
                f"review={item['review_status']} generated={item['generated_at']}"
            )
        if blockers:
            print("BLOCKERS:")
            for blocker in blockers:
                print(f"- {blocker}")
        if next_task:
            print("NEXT TASK:")
            print(f"- {next_task['id']}: {next_task['title']}")
            print(f"- recipe={next_task['recipe']} required_mode={next_task['required_mode']}")
            print(f"- python3 scripts/taskctl.py show {next_task['id']}")
        print("READ IN ORDER:")
        for item in result["mandatory_read_order"]:
            print(f"- {item}")

    return 0 if result["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
