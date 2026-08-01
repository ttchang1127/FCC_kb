#!/usr/bin/env python3
"""Build public, machine-readable FCC submarine-cable source data.

The script uses only official eCFR and FederalRegister.gov APIs. It downloads
the current text of monitored CFR sections, compares source hashes with a
manually accepted review baseline, and writes data/regulatory-status.json.

It intentionally never rewrites curated Chinese legal summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "regulatory-status.json"
BASELINE_PATH = ROOT / "data" / "review-baseline.json"
USER_AGENT = "FCC-kb-regulatory-monitor/1.0 (+https://ttchang1127.github.io/FCC_kb/)"

SUBPART_FF_SECTIONS = [f"1.700{i:02d}" for i in range(30)]
OTHER_SECTIONS = ["4.15", "43.82", "63.18", "1.40001", "1.50002"]
MONITORED_SECTIONS = SUBPART_FF_SECTIONS + OTHER_SECTIONS
REQUIRED_SECTIONS = set([f"1.700{i:02d}" for i in range(25)] + ["4.15", "43.82"])

ECFR_TITLES_URL = "https://www.ecfr.gov/api/versioner/v1/titles.json"
ECFR_WEB_ROOT = "https://www.ecfr.gov/current/title-47"
FR_API_ROOT = "https://www.federalregister.gov/api/v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fetch_bytes(url: str, attempts: int = 2) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/xml, text/xml"},
    )
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    assert last_error is not None
    raise last_error


def fetch_json(url: str) -> dict:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def compact_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def section_api_url(as_of: str, section: str) -> str:
    return (
        "https://www.ecfr.gov/api/versioner/v1/full/"
        f"{as_of}/title-47.xml?section={urllib.parse.quote(section)}"
    )


def subpart_ff_api_url(as_of: str) -> str:
    return (
        "https://www.ecfr.gov/api/versioner/v1/full/"
        f"{as_of}/title-47.xml?part=1&subpart=FF"
    )


def section_web_url(section: str) -> str:
    return f"{ECFR_WEB_ROOT}/section-{urllib.parse.quote(section)}"


def parse_section_element(section: str, root: ET.Element, as_of: str, api_url: str) -> dict:
    raw = ET.tostring(root, encoding="utf-8")
    head = root.find("HEAD")
    title = compact_text("".join(head.itertext())) if head is not None else f"§ {section}"
    paragraphs: list[str] = []
    for element in root.findall(".//P"):
        text = compact_text("".join(element.itertext()))
        if text:
            paragraphs.append(text)
    citations = [
        compact_text("".join(element.itertext()))
        for element in root.findall(".//CITA")
        if compact_text("".join(element.itertext()))
    ]
    if "[Reserved]" in title:
        content_status = "reserved"
    elif title.lower().endswith("xxx") or not paragraphs:
        content_status = "future_placeholder"
    else:
        content_status = "current_text"
    return {
        "section": section,
        "title": title,
        "available": True,
        "content_status": content_status,
        "as_of": as_of,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "paragraphs": paragraphs,
        "citations": citations,
        "official_url": section_web_url(section),
        "api_url": api_url,
    }


def parse_section(section: str, raw: bytes, as_of: str, api_url: str) -> dict:
    return parse_section_element(section, ET.fromstring(raw), as_of, api_url)


def fetch_sections(as_of: str) -> tuple[list[dict], list[str]]:
    sections_by_id: dict[str, dict] = {}
    errors: list[str] = []

    # Fetch Subpart FF in one official API request. This is substantially more
    # reliable than dozens of section-level requests and reduces API load.
    subpart_url = subpart_ff_api_url(as_of)
    try:
        subpart_root = ET.fromstring(fetch_bytes(subpart_url))
        for element in subpart_root.iter():
            section = element.attrib.get("N")
            if element.attrib.get("TYPE") != "SECTION" or section not in SUBPART_FF_SECTIONS:
                continue
            sections_by_id[section] = parse_section_element(
                section, element, as_of, subpart_url
            )
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
        errors.append(f"eCFR Subpart FF: {exc}")

    for section in OTHER_SECTIONS:
        url = section_api_url(as_of, section)
        try:
            raw = fetch_bytes(url)
            sections_by_id[section] = parse_section(section, raw, as_of, url)
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and section not in REQUIRED_SECTIONS:
                sections_by_id[section] = {
                    "section": section,
                    "title": f"§ {section}",
                    "available": False,
                    "as_of": as_of,
                    "official_url": section_web_url(section),
                }
                continue
            errors.append(f"eCFR §{section}: HTTP {exc.code}")
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
            errors.append(f"eCFR §{section}: {exc}")

    sections = [
        sections_by_id.get(
            section,
            {
                "section": section,
                "title": f"§ {section}",
                "available": False,
                "as_of": as_of,
                "official_url": section_web_url(section),
            },
        )
        for section in MONITORED_SECTIONS
    ]
    return sections, errors


def relevant_fr_document(document: dict) -> bool:
    title = str(document.get("title", "")).lower()
    dockets = " ".join(document.get("docket_ids") or []).lower()
    return "submarine cable" in title or "24-523" in dockets


def fetch_federal_register_documents() -> tuple[str, list[dict]]:
    parameters = [
        ("per_page", "100"),
        ("order", "newest"),
        ("conditions[agencies][]", "federal-communications-commission"),
        ("conditions[term]", "submarine cable"),
    ]
    query_url = f"{FR_API_ROOT}/documents.json?{urllib.parse.urlencode(parameters)}"
    response = fetch_json(query_url)
    documents = []
    for item in response.get("results", []):
        if not relevant_fr_document(item):
            continue
        documents.append(
            {
                "document_number": item.get("document_number"),
                "publication_date": item.get("publication_date"),
                "type": item.get("type"),
                "title": item.get("title"),
                "citation": item.get("citation"),
                "docket_ids": item.get("docket_ids") or [],
                "effective_on": item.get("effective_on"),
                "comments_close_on": item.get("comments_close_on"),
                "html_url": item.get("html_url"),
                "pdf_url": item.get("pdf_url"),
            }
        )
    return query_url, documents


def read_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {"sections": {}, "federal_register_documents": []}
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    path.write_text(payload, encoding="utf-8")


def markdown_cell(value: object) -> str:
    """Escape untrusted official-source text for a Markdown table cell."""
    if value is None or value == "":
        return "—"
    return compact_text(str(value)).replace("|", "\\|")


def build_change_alert_body(result: dict) -> str:
    """Build the fixed GitHub Issue body used for human legal review."""
    review = result["review"]
    lines = [
        "<!-- fcc-kb-regulatory-review -->",
        "# FCC 官方來源變動待人工複核",
        "",
        "> 自動偵測只代表官方來源內容或文件清單有變動，不代表法律狀態已完成判讀。",
        "",
        f"- 發現時間（UTC）：`{markdown_cell(result.get('generated_at'))}`",
        f"- eCFR 資料截至：`{markdown_cell(result.get('ecfr', {}).get('up_to_date_as_of'))}`",
        f"- 人工基準截至：`{markdown_cell(review.get('ecfr_reviewed_as_of'))}`",
        f"- 自動狀態：`{markdown_cell(review.get('status'))}`",
        "",
        "## eCFR section changes",
        "",
    ]
    section_changes = review.get("section_changes") or []
    if section_changes:
        lines.extend(
            [
                "| Section | Change | Reviewed SHA-256 | Current SHA-256 | Official source |",
                "|---|---|---|---|---|",
            ]
        )
        for item in section_changes:
            lines.append(
                "| §{section} | {change} | `{old}` | `{new}` | [eCFR]({url}) |".format(
                    section=markdown_cell(item.get("section")),
                    change=markdown_cell(item.get("change")),
                    old=markdown_cell(item.get("reviewed_sha256")),
                    new=markdown_cell(item.get("current_sha256")),
                    url=markdown_cell(item.get("official_url")),
                )
            )
    else:
        lines.append("無 section hash 變動。")

    lines.extend(["", "## New Federal Register documents", ""])
    documents = review.get("new_federal_register_documents") or []
    if documents:
        lines.extend(
            [
                "| Document | Publication date | Type | Citation | Official URL |",
                "|---|---|---|---|---|",
            ]
        )
        for item in documents:
            url = item.get("html_url") or item.get("pdf_url") or ""
            lines.append(
                "| {number} — {title} | {date} | {type} | {citation} | [Federal Register]({url}) |".format(
                    number=markdown_cell(item.get("document_number")),
                    title=markdown_cell(item.get("title")),
                    date=markdown_cell(item.get("publication_date")),
                    type=markdown_cell(item.get("type")),
                    citation=markdown_cell(item.get("citation")),
                    url=markdown_cell(url),
                )
            )
    else:
        lines.append("無新 Federal Register 文件。")

    lines.extend(
        [
            "",
            "## 人工處理規則",
            "",
            "1. 依 Federal Register、eCFR 與 FCC 命令判斷法律狀態。",
            "2. 不得因 hash 改變或 future amendment 標記自動接受新基準。",
            "3. 完成中文卡、矩陣與網站複核後，才可執行 `--accept-current`。",
            "4. 完成並提交人工基準後，由人員關閉本 Issue。自動流程不會自行關閉。",
            "",
            "[查看自動更新 workflow](https://github.com/ttchang1127/FCC_kb/actions/workflows/update-regulations.yml)",
        ]
    )
    return "\n".join(lines) + "\n"


def accepted_baseline(sections: list[dict], documents: list[dict], as_of: str) -> dict:
    return {
        "schema_version": 1,
        "curated_reviewed_at": utc_now(),
        "ecfr_reviewed_as_of": as_of,
        "sections": {
            item["section"]: item["sha256"]
            for item in sections
            if item.get("available") and item.get("sha256")
        },
        "federal_register_documents": [
            item["document_number"] for item in documents if item.get("document_number")
        ],
        "note": "This baseline is changed only after human review of curated legal summaries.",
    }


def compare_with_baseline(
    sections: list[dict], documents: list[dict], baseline: dict
) -> tuple[list[dict], list[dict]]:
    reviewed_sections = baseline.get("sections", {})
    section_changes = []
    for item in sections:
        section = item["section"]
        reviewed_hash = reviewed_sections.get(section)
        current_hash = item.get("sha256")
        if item.get("available") and reviewed_hash != current_hash:
            section_changes.append(
                {
                    "section": section,
                    "change": "new" if reviewed_hash is None else "modified",
                    "reviewed_sha256": reviewed_hash,
                    "current_sha256": current_hash,
                    "official_url": item["official_url"],
                }
            )
        elif not item.get("available") and reviewed_hash:
            section_changes.append(
                {
                    "section": section,
                    "change": "unavailable_or_removed",
                    "reviewed_sha256": reviewed_hash,
                    "current_sha256": None,
                    "official_url": item["official_url"],
                }
            )

    reviewed_documents = set(baseline.get("federal_register_documents", []))
    new_documents = [
        item for item in documents if item.get("document_number") not in reviewed_documents
    ]
    return section_changes, new_documents


def build(accept_current: bool = False) -> dict:
    titles = fetch_json(ECFR_TITLES_URL)
    title47 = next(item for item in titles["titles"] if item["number"] == 47)
    as_of = title47["up_to_date_as_of"]
    sections, errors = fetch_sections(as_of)
    missing_required = sorted(
        REQUIRED_SECTIONS
        - {item["section"] for item in sections if item.get("available")}
    )
    if missing_required:
        raise RuntimeError("Required eCFR sections unavailable: " + ", ".join(missing_required))

    fr_query_url, documents = fetch_federal_register_documents()
    if accept_current:
        baseline = accepted_baseline(sections, documents, as_of)
        write_json(BASELINE_PATH, baseline)
    else:
        baseline = read_baseline()

    section_changes, new_documents = compare_with_baseline(sections, documents, baseline)
    review_required = bool(section_changes or new_documents)
    result = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "automation": {
            "schedule": "daily",
            "source": "GitHub Actions",
            "workflow_url": "https://github.com/ttchang1127/FCC_kb/actions/workflows/update-regulations.yml",
        },
        "review": {
            "status": "review_required" if review_required else "current",
            "curated_reviewed_at": baseline.get("curated_reviewed_at"),
            "ecfr_reviewed_as_of": baseline.get("ecfr_reviewed_as_of"),
            "section_changes": section_changes,
            "new_federal_register_documents": new_documents,
            "policy": "Official source data updates automatically; curated legal summaries require human review.",
        },
        "ecfr": {
            "title": 47,
            "up_to_date_as_of": as_of,
            "latest_amended_on": title47.get("latest_amended_on"),
            "latest_issue_date": title47.get("latest_issue_date"),
            "official_url": f"{ECFR_WEB_ROOT}/chapter-I/subchapter-A/part-1/subpart-FF",
            "api_metadata_url": ECFR_TITLES_URL,
            "available_section_count": sum(1 for item in sections if item.get("available")),
            "current_text_section_count": sum(
                1 for item in sections if item.get("content_status") == "current_text"
            ),
            "monitored_section_count": len(sections),
            "sections": sections,
        },
        "federal_register": {
            "query_url": fr_query_url,
            "document_count": len(documents),
            "latest_publication_date": documents[0].get("publication_date") if documents else None,
            "documents": documents,
        },
        "errors": errors,
    }
    write_json(OUTPUT_PATH, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--accept-current",
        action="store_true",
        help="Replace the human-review baseline with current official source hashes.",
    )
    parser.add_argument(
        "--issue-body-output",
        type=Path,
        help="Write a deterministic regulatory-review GitHub Issue body to this path.",
    )
    args = parser.parse_args()
    try:
        result = build(accept_current=args.accept_current)
    except (RuntimeError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"Regulatory update failed: {exc}")
        return 1
    if args.issue_body_output:
        args.issue_body_output.parent.mkdir(parents=True, exist_ok=True)
        args.issue_body_output.write_text(build_change_alert_body(result), encoding="utf-8")
    print(f"eCFR Title 47 as of: {result['ecfr']['up_to_date_as_of']}")
    print(
        "Sections: "
        f"{result['ecfr']['available_section_count']}/"
        f"{result['ecfr']['monitored_section_count']} available"
    )
    print(f"Federal Register documents: {result['federal_register']['document_count']}")
    print(f"Review status: {result['review']['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
