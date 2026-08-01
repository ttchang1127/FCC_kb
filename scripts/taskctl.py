#!/usr/bin/env python3
"""Deterministic task queue control for humans and low-capability agents."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "tasks" / "queue.json"
REQUIRED_TASK_FIELDS = {
    "id",
    "priority",
    "order",
    "status",
    "mode",
    "recipe",
    "title",
    "depends_on",
    "sources",
    "targets",
    "acceptance",
    "human_review_required",
    "evidence",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_queue() -> dict:
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(queue: dict) -> None:
    queue["last_updated"] = datetime.now(timezone.utc).date().isoformat()
    QUEUE_PATH.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def detect_mode() -> str:
    full_vault_markers = [ROOT / "00_首頁", ROOT / "99_資料治理"]
    return "full_vault" if all(path.is_dir() for path in full_vault_markers) else "public"


def validate_queue(queue: dict) -> list[str]:
    errors: list[str] = []
    if queue.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    statuses = set(queue.get("status_values", []))
    modes = set(queue.get("mode_values", []))
    recipes = set(queue.get("recipe_values", []))
    tasks = queue.get("tasks")
    if not isinstance(tasks, list):
        return errors + ["tasks must be a list"]

    ids: list[str] = []
    by_id: dict[str, dict] = {}
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"task[{index}] must be an object")
            continue
        missing = sorted(REQUIRED_TASK_FIELDS - set(task))
        if missing:
            errors.append(f"task[{index}] missing: {', '.join(missing)}")
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"task[{index}] has invalid id")
            continue
        ids.append(task_id)
        by_id[task_id] = task
        if task.get("status") not in statuses:
            errors.append(f"{task_id}: invalid status {task.get('status')}")
        if task.get("mode") not in modes:
            errors.append(f"{task_id}: invalid mode {task.get('mode')}")
        if task.get("recipe") not in recipes:
            errors.append(f"{task_id}: invalid recipe {task.get('recipe')}")
        if not isinstance(task.get("priority"), int) or not isinstance(task.get("order"), int):
            errors.append(f"{task_id}: priority and order must be integers")
        for field in ("depends_on", "sources", "targets", "acceptance", "evidence"):
            if not isinstance(task.get(field), list):
                errors.append(f"{task_id}: {field} must be a list")

    duplicate_ids = sorted({task_id for task_id in ids if ids.count(task_id) > 1})
    if duplicate_ids:
        errors.append("duplicate task ids: " + ", ".join(duplicate_ids))

    for task_id, task in by_id.items():
        for dependency in task.get("depends_on", []):
            if dependency not in by_id:
                errors.append(f"{task_id}: unknown dependency {dependency}")
            elif dependency == task_id:
                errors.append(f"{task_id}: cannot depend on itself")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, chain: list[str]) -> None:
        if task_id in visiting:
            errors.append("dependency cycle: " + " -> ".join(chain + [task_id]))
            return
        if task_id in visited or task_id not in by_id:
            return
        visiting.add(task_id)
        for dependency in by_id[task_id].get("depends_on", []):
            visit(dependency, chain + [task_id])
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        visit(task_id, [])
    in_progress = [task_id for task_id, task in by_id.items() if task.get("status") == "in_progress"]
    if len(in_progress) > 1:
        errors.append("more than one task is in_progress: " + ", ".join(in_progress))
    return errors


def resolve_mode(requested: str) -> str:
    detected = detect_mode()
    if requested == "auto":
        return detected
    if requested == "full_vault" and detected != "full_vault":
        raise RuntimeError("full_vault requested but vault markers are missing")
    return requested


def dependencies_done(task: dict, by_id: dict[str, dict]) -> bool:
    return all(by_id[item]["status"] == "done" for item in task["depends_on"])


def eligible_tasks(queue: dict, mode: str) -> list[dict]:
    by_id = {task["id"]: task for task in queue["tasks"]}
    active = sorted(
        [
            task
            for task in queue["tasks"]
            if task["status"] == "in_progress"
            and (task["mode"] == "public" or mode == "full_vault")
        ],
        key=lambda task: (task["priority"], task["order"], task["id"]),
    )
    if active:
        return active
    return sorted(
        [
            task
            for task in queue["tasks"]
            if task["status"] == "ready"
            and (task["mode"] == "public" or mode == "full_vault")
            and dependencies_done(task, by_id)
        ],
        key=lambda task: (task["priority"], task["order"], task["id"]),
    )


def find_task(queue: dict, task_id: str) -> dict:
    for task in queue["tasks"]:
        if task["id"] == task_id:
            return task
    raise RuntimeError(f"unknown task id: {task_id}")


def task_payload(task: dict, mode: str) -> dict:
    if task["status"] == "in_progress":
        next_commands = [
            f"python3 scripts/taskctl.py show {task['id']}",
            "Read docs/AI_RUNBOOK.md recipe " + task["recipe"],
            "Resume only this in_progress task; do not start another task",
        ]
    else:
        next_commands = [
            f"python3 scripts/taskctl.py show {task['id']}",
            "Read docs/AI_RUNBOOK.md recipe " + task["recipe"],
            f"python3 scripts/taskctl.py start {task['id']}",
        ]
    return {
        "environment_mode": mode,
        "id": task["id"],
        "priority": task["priority"],
        "status": task["status"],
        "required_mode": task["mode"],
        "recipe": task["recipe"],
        "title": task["title"],
        "depends_on": task["depends_on"],
        "sources": task["sources"],
        "targets": task["targets"],
        "acceptance": task["acceptance"],
        "human_review_required": task["human_review_required"],
        "next_commands": next_commands,
    }


def print_task(task: dict, mode: str, as_json: bool) -> None:
    payload = task_payload(task, mode)
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"TASK: {payload['id']}")
    print(f"TITLE: {payload['title']}")
    print(f"MODE: {payload['required_mode']} (current: {mode})")
    print(f"RECIPE: {payload['recipe']}")
    print("SOURCES:")
    for item in payload["sources"]:
        print(f"- {item}")
    print("TARGETS:")
    for item in payload["targets"]:
        print(f"- {item}")
    print("ACCEPTANCE:")
    for item in payload["acceptance"]:
        print(f"- [ ] {item}")
    print("NEXT:")
    for item in payload["next_commands"]:
        print(f"- {item}")


def git_is_clean() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0 and not result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate")

    next_parser = subparsers.add_parser("next")
    next_parser.add_argument("--mode", choices=["auto", "public", "full_vault"], default="auto")
    next_parser.add_argument("--json", action="store_true")

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("task_id")
    show_parser.add_argument("--json", action="store_true")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status", choices=["ready", "in_progress", "blocked", "done"])
    list_parser.add_argument("--mode", choices=["auto", "public", "full_vault"], default="auto")

    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("task_id")

    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("task_id")
    complete_parser.add_argument("--evidence", required=True)

    block_parser = subparsers.add_parser("block")
    block_parser.add_argument("task_id")
    block_parser.add_argument("--reason", required=True)

    args = parser.parse_args()
    queue = load_queue()
    errors = validate_queue(queue)
    if errors:
        print("INVALID TASK QUEUE", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    if args.command == "validate":
        print(f"Task queue valid: {len(queue['tasks'])} tasks")
        return 0

    mode = resolve_mode(getattr(args, "mode", "auto"))

    if args.command == "next":
        tasks = eligible_tasks(queue, mode)
        if not tasks:
            print("NO ELIGIBLE TASK")
            return 3
        print_task(tasks[0], mode, args.json)
        return 0

    if args.command == "show":
        task = find_task(queue, args.task_id)
        if task["mode"] == "full_vault" and mode != "full_vault":
            print("BLOCKED: task requires full_vault", file=sys.stderr)
            return 4
        print_task(task, mode, args.json)
        return 0

    if args.command == "list":
        for task in sorted(queue["tasks"], key=lambda item: (item["priority"], item["order"])):
            if args.status and task["status"] != args.status:
                continue
            compatible = task["mode"] == "public" or mode == "full_vault"
            print(f"{task['id']}\t{task['status']}\t{task['mode']}\tcompatible={str(compatible).lower()}\t{task['title']}")
        return 0

    task = find_task(queue, args.task_id)
    by_id = {item["id"]: item for item in queue["tasks"]}

    if args.command == "start":
        if task["status"] != "ready":
            print(f"BLOCKED: status is {task['status']}, expected ready", file=sys.stderr)
            return 5
        if task["mode"] == "full_vault" and mode != "full_vault":
            print("BLOCKED: task requires full_vault", file=sys.stderr)
            return 4
        if not dependencies_done(task, by_id):
            pending = [item for item in task["depends_on"] if by_id[item]["status"] != "done"]
            print("BLOCKED dependencies: " + ", ".join(pending), file=sys.stderr)
            return 6
        if not git_is_clean():
            print("BLOCKED: git worktree is not clean", file=sys.stderr)
            return 7
        task["status"] = "in_progress"
        task["started_at"] = now_utc()
        save_queue(queue)
        print(f"STARTED {task['id']}")
        return 0

    if args.command == "complete":
        if task["status"] != "in_progress":
            print(f"BLOCKED: status is {task['status']}, expected in_progress", file=sys.stderr)
            return 5
        task["status"] = "done"
        task["completed_at"] = now_utc()
        task["evidence"].append({"recorded_at": now_utc(), "summary": args.evidence})
        save_queue(queue)
        print(f"COMPLETED {task['id']}")
        return 0

    if args.command == "block":
        if task["status"] not in {"ready", "in_progress"}:
            print(f"BLOCKED: cannot block task in status {task['status']}", file=sys.stderr)
            return 5
        task["status"] = "blocked"
        task["blocked_at"] = now_utc()
        task["blocked_reason"] = args.reason
        save_queue(queue)
        print(f"BLOCKED {task['id']}: {args.reason}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
