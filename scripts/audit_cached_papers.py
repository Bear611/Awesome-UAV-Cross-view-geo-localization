#!/usr/bin/env python3
"""Audit cached PDFs that have not been reviewed from their current file.

The script separates readable, title-matched papers from corrupt, mislabeled,
or otherwise unreadable files.  For readable papers it extracts the complete
text, records dataset mentions, and locates pages likely to contain benchmark
results or comparisons.  Page-level visual verification is a later, explicit
step; text extraction alone never sets a paper to ``visually_verified``.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
READABLE_CSV = ROOT / "data" / "reports" / "cache_pdf_readable.csv"
UNREADABLE_CSV = ROOT / "data" / "reports" / "cache_pdf_unreadable.csv"
REPORT_MD = ROOT / "data" / "reports" / "cache_fulltext_audit.md"
TEXT_CACHE_DIR = ROOT / "tmp" / "pdfs" / "cache_fulltext"

DATASET_PATTERNS = {
    "University-1652": (r"university[- ]?1652",),
    "SUES-200": (r"sues[- ]?200",),
    "DenseUAV": (r"dense[- ]?uav",),
    "GTA-UAV": (r"gta[- ]?uav", r"game4loc"),
    "World-UAV": (r"world[- ]?uav",),
    "UAV-VisLoc": (r"uav[- ]?visloc",),
    "UAV-GeoLoc": (r"uav[- ]?geoloc",),
    "UAV-VLL": (r"uav[- ]?vll",),
    "AerialVL": (r"aerial[- ]?vl",),
    "VIGOR": (r"\bvigor\b",),
    "CVUSA": (r"\bcvusa\b",),
    "CVACT": (r"\bcvact\b", r"cv[- ]?act"),
}

METRIC_RE = re.compile(
    r"(?:R@\s*(?:1|5|10)|Recall\s*@?\s*(?:1|5|10)|top[- ]?(?:1|5|10)|"
    r"mAP|\bAP\b|SDM\s*@?\s*\d|mean\s+locali[sz]ation\s+error|\bMLE\b|"
    r"distance\s+error|meter[- ]level)",
    re.IGNORECASE,
)
COMPARISON_RE = re.compile(
    r"(?:comparison\s+(?:with|to)|state[- ]of[- ]the[- ]art|\bSOTA\b|"
    r"compared\s+(?:with|to)|quantitative\s+comparison|benchmark\s+comparison)",
    re.IGNORECASE,
)
RESULT_RE = re.compile(
    r"(?:experimental\s+results?|evaluation\s+results?|quantitative\s+results?|"
    r"retrieval\s+results?|locali[sz]ation\s+results?|\bresults\b)",
    re.IGNORECASE,
)
NUMBER_RE = re.compile(r"(?:\b\d{1,3}\.\d{1,4}\b|\b\d{1,3}\s*%)")
REFERENCES_HEADING_RE = re.compile(
    r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?references\s*$"
)

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "using", "based",
    "via", "under", "toward", "towards", "through", "between", "method",
    "framework", "network", "approach", "system", "visual", "image", "images",
    "uav", "drone", "geo", "localization", "localisation", "cross", "view",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).lower()
    return " ".join(re.findall(r"[a-z0-9]+", value))


def title_tokens(value: str) -> set[str]:
    return {
        token for token in normalize(value).split()
        if len(token) > 2 and token not in STOPWORDS
    }


def paper_acronym(title: str) -> str:
    prefix = title.split(":", 1)[0].strip()
    if 2 <= len(prefix) <= 20 and re.fullmatch(r"[A-Za-z0-9()\-+² ]+", prefix):
        return normalize(prefix).replace(" ", "")
    return ""


def pdf_magic(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(5) == b"%PDF-"
    except OSError:
        return False


def find_pdftotext(explicit: str | None) -> str:
    candidates = [
        explicit,
        shutil.which("pdftotext"),
        r"C:\texlive\2025\bin\windows\pdftotext.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise FileNotFoundError("pdftotext was not found")


def extract_pages(executable: str, path: Path) -> tuple[list[str], str]:
    command = [executable, "-layout", "-enc", "UTF-8", str(path), "-"]
    completed = subprocess.run(
        command, capture_output=True, timeout=180, check=False
    )
    if completed.returncode != 0:
        error = completed.stderr.decode("utf-8", errors="replace").strip()
        return [], error or f"pdftotext exited {completed.returncode}"
    text = completed.stdout.decode("utf-8", errors="replace")
    pages = [page.strip() for page in text.split("\f")]
    while pages and not pages[-1]:
        pages.pop()
    return pages, ""


def parse_review_time(value: Any) -> float | None:
    try:
        return datetime.fromisoformat(str(value)).timestamp()
    except (TypeError, ValueError):
        return None


def row_datasets(pages: list[str]) -> list[str]:
    full_text = "\n".join(pages)
    return [
        dataset for dataset, patterns in DATASET_PATTERNS.items()
        if any(re.search(pattern, full_text, re.IGNORECASE) for pattern in patterns)
    ]


def evidence_pages(pages: list[str]) -> tuple[list[int], list[int]]:
    scored: list[tuple[int, int]] = []
    comparisons: list[tuple[int, int]] = []
    references_page = next(
        (
            page_no for page_no, text in enumerate(pages, start=1)
            if REFERENCES_HEADING_RE.search(text)
        ),
        math.inf,
    )
    for page_no, text in enumerate(pages, start=1):
        if page_no >= references_page:
            continue
        metric_hits = len(METRIC_RE.findall(text))
        numeric_hits = len(NUMBER_RE.findall(text))
        if not metric_hits or numeric_hits < 2:
            continue
        dataset_hits = sum(
            1 for patterns in DATASET_PATTERNS.values()
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)
        )
        comparison = bool(COMPARISON_RE.search(text))
        result = bool(RESULT_RE.search(text))
        table = bool(re.search(r"\btable\s+(?:[ivxlcdm]+|\d+)\b", text, re.IGNORECASE))
        score = min(metric_hits, 8) + 3 * dataset_hits + 2 * int(comparison) + int(result) + int(table)
        if dataset_hits or result or table:
            scored.append((score, page_no))
        if comparison and dataset_hits and table:
            comparisons.append((score, page_no))
    top_results = [page for _, page in sorted(scored, reverse=True)[:8]]
    top_comparisons = [page for _, page in sorted(comparisons, reverse=True)[:8]]
    return sorted(top_results), sorted(top_comparisons)


def title_match(title: str, pages: list[str]) -> tuple[float, bool]:
    full_normalized = normalize("\n".join(pages))
    front_normalized = normalize("\n".join(pages[:2]))
    wanted = title_tokens(title)
    present = set(front_normalized.split())
    coverage = len(wanted & present) / max(1, len(wanted))
    exact = bool(normalize(title)) and normalize(title) in full_normalized
    acronym = paper_acronym(title)
    acronym_match = bool(acronym and acronym in front_normalized.replace(" ", ""))
    # An acronym before a colon is a strong identity constraint: a generic UAV
    # paper can otherwise share most title tokens while still being the wrong
    # download.  Book/proceedings chapters remain supported by the exact-title
    # search across the full document.
    if acronym:
        matched = exact or (acronym_match and coverage >= 0.40)
    else:
        matched = exact or coverage >= 0.60
    return coverage, matched


def first_nonempty_text(pages: list[str]) -> str:
    text = next((page for page in pages if page.strip()), "")
    return re.sub(r"\s+", " ", text).strip()[:240]


def load_csv_titles(path: Path) -> set[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        return {normalize(row.get("paper", "")) for row in csv.DictReader(handle)}


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value or "-").replace("|", "\\|").replace("\n", " ")


def audit(cache_dir: Path, pdftotext: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    papers = yaml.safe_load((ROOT / "data" / "papers.yml").read_text(encoding="utf-8")) or []
    reviews_path = ROOT / "data" / "internal" / "leaderboard_reviews.yml"
    reviews = yaml.safe_load(reviews_path.read_text(encoding="utf-8")) or []
    paper_by_id = {str(item.get("id")): item for item in papers if item.get("id")}
    review_by_id = {
        str(item.get("paper_id")): item for item in reviews if item.get("paper_id")
    }
    leaderboard_titles = load_csv_titles(ROOT / "data" / "leaderboards.csv")

    pdfs_by_id: dict[str, list[Path]] = defaultdict(list)
    unreadable: list[dict[str, Any]] = []
    for path in sorted(cache_dir.glob("*.pdf")):
        match = re.match(r"^([0-9a-f]{12})(?:_|\.|$)", path.name, re.IGNORECASE)
        if not pdf_magic(path):
            unreadable.append({
                "paper_id": match.group(1).lower() if match else "",
                "title": "",
                "pdf_file": path.name,
                "reason": "invalid_pdf_signature",
                "match_score": "",
                "actual_content_preview": "",
            })
            continue
        if match:
            pdfs_by_id[match.group(1).lower()].append(path)

    candidate_ids: set[str] = set()
    for paper_id, paths in pdfs_by_id.items():
        review = review_by_id.get(paper_id)
        if not review:
            candidate_ids.add(paper_id)
            continue
        reviewed_at = parse_review_time(review.get("reviewed_at"))
        if reviewed_at is None or max(path.stat().st_mtime for path in paths) > reviewed_at + 2:
            candidate_ids.add(paper_id)

    extracted: list[dict[str, Any]] = []
    for position, paper_id in enumerate(sorted(candidate_ids), start=1):
        paper = paper_by_id.get(paper_id, {})
        review = review_by_id.get(paper_id, {})
        title = str(paper.get("title") or review.get("paper_title") or "").strip()
        best: dict[str, Any] | None = None
        failures: list[str] = []
        for path in pdfs_by_id[paper_id]:
            pages, error = extract_pages(pdftotext, path)
            if error:
                failures.append(f"{path.name}: {error}")
                continue
            chars = sum(len(page) for page in pages)
            coverage, matched = title_match(title, pages)
            candidate = {
                "path": path,
                "pages": pages,
                "chars": chars,
                "coverage": coverage,
                "matched": matched,
            }
            if best is None or (matched, coverage, chars) > (
                best["matched"], best["coverage"], best["chars"]
            ):
                best = candidate
        if best is None:
            unreadable.append({
                "paper_id": paper_id,
                "title": title,
                "pdf_file": "; ".join(path.name for path in pdfs_by_id[paper_id]),
                "reason": "text_extraction_failed: " + " | ".join(failures),
                "match_score": "",
                "actual_content_preview": "",
            })
            continue
        if best["chars"] < 1000:
            reason = "insufficient_extractable_text"
        elif not best["matched"]:
            reason = "pdf_content_does_not_match_paper_title"
        else:
            reason = ""
        if reason:
            unreadable.append({
                "paper_id": paper_id,
                "title": title,
                "pdf_file": best["path"].name,
                "reason": reason,
                "match_score": f"{best['coverage']:.3f}",
                "actual_content_preview": first_nonempty_text(best["pages"]),
            })
            continue

        datasets = row_datasets(best["pages"])
        result_pages, comparison_pages = evidence_pages(best["pages"])
        TEXT_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with gzip.open(TEXT_CACHE_DIR / f"{paper_id}.json.gz", "wt", encoding="utf-8") as handle:
            json.dump(
                {
                    "paper_id": paper_id,
                    "title": title,
                    "pdf_file": best["path"].name,
                    "pages": best["pages"],
                },
                handle,
                ensure_ascii=False,
            )
        review_time = review.get("reviewed_at", "")
        current_file_is_new = bool(review_time)
        if comparison_pages:
            candidate_status = "comparison_pages_found"
        elif result_pages:
            candidate_status = "result_pages_found"
        else:
            candidate_status = "no_benchmark_result_page_detected"
        extracted.append({
            "paper_id": paper_id,
            "title": title,
            "pdf_file": best["path"].name,
            "pages": len(best["pages"]),
            "text_chars": best["chars"],
            "title_match_score": f"{best['coverage']:.3f}",
            "datasets_mentioned": "; ".join(datasets),
            "result_pages": "; ".join(map(str, result_pages)),
            "comparison_pages": "; ".join(map(str, comparison_pages)),
            "currently_on_leaderboard": "true" if normalize(title) in leaderboard_titles else "false",
            "prior_review": str(review.get("overall_decision") or "none"),
            "prior_reviewed_at": str(review_time),
            "current_pdf_postdates_review": "true" if current_file_is_new else "false",
            "read_status": "full_text_extracted_pending_visual_table_review",
            "result_status": candidate_status,
            "notes": "",
        })
        print(
            f"[{position}/{len(candidate_ids)}] readable {paper_id}: "
            f"{len(best['pages'])} pages, {best['chars']} chars",
            flush=True,
        )

    # Collapse duplicate catalog IDs representing the same paper title.  Keep
    # the row with the most complete text and retain all IDs/files in notes.
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in extracted:
        grouped[normalize(str(row["title"]))].append(row)
    readable: list[dict[str, Any]] = []
    for rows in grouped.values():
        best = max(rows, key=lambda row: (int(row["text_chars"]), int(row["pages"])))
        if len(rows) > 1:
            best = dict(best)
            best["paper_id"] = "; ".join(sorted(str(row["paper_id"]) for row in rows))
            best["pdf_file"] = "; ".join(sorted(str(row["pdf_file"]) for row in rows))
            best["notes"] = "duplicate catalog IDs collapsed"
        readable.append(best)
    readable.sort(key=lambda row: str(row["title"]).casefold())
    unreadable.sort(key=lambda row: (str(row["title"]).casefold(), str(row["pdf_file"])))
    return readable, unreadable


def render_report(readable: list[dict[str, Any]], unreadable: list[dict[str, Any]]) -> None:
    comparison_count = sum(row["result_status"] == "comparison_pages_found" for row in readable)
    result_count = sum(row["result_status"] == "result_pages_found" for row in readable)
    lines = [
        "# Cached PDF Full-Text Audit", "",
        "This report separates the current unread cached-paper backlog into readable/title-matched PDFs and unreadable, corrupt, or mislabeled files. Full text has been extracted for every readable row. Candidate result pages still require visual table verification before leaderboard values are accepted.",
        "",
        f"- Readable unique papers: **{len(readable)}**",
        f"- Unreadable or mismatched cached files: **{len(unreadable)}**",
        f"- Papers with comparison-page candidates: **{comparison_count}**",
        f"- Papers with other result-page candidates: **{result_count}**",
        "", "## Readable papers", "",
        "| Paper ID | Title | Pages | Datasets | Result pages | Comparison pages | On leaderboard | Status |",
        "|---|---|---:|---|---|---|---|---|",
    ]
    for row in readable:
        lines.append(
            "| " + " | ".join(md_escape(row[key]) for key in (
                "paper_id", "title", "pages", "datasets_mentioned", "result_pages",
                "comparison_pages", "currently_on_leaderboard", "result_status",
            )) + " |"
        )
    lines.extend([
        "", "## Unreadable or mismatched files", "",
        "| Paper ID | Intended title | Cached file | Reason | Match score | Actual-content preview |",
        "|---|---|---|---|---:|---|",
    ])
    for row in unreadable:
        lines.append(
            "| " + " | ".join(md_escape(row[key]) for key in (
                "paper_id", "title", "pdf_file", "reason", "match_score",
                "actual_content_preview",
            )) + " |"
        )
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--pdftotext")
    args = parser.parse_args()
    executable = find_pdftotext(args.pdftotext)
    readable, unreadable = audit(args.cache_dir.resolve(), executable)

    readable_fields = [
        "paper_id", "title", "pdf_file", "pages", "text_chars", "title_match_score",
        "datasets_mentioned", "result_pages", "comparison_pages",
        "currently_on_leaderboard", "prior_review", "prior_reviewed_at",
        "current_pdf_postdates_review", "read_status", "result_status", "notes",
    ]
    unreadable_fields = [
        "paper_id", "title", "pdf_file", "reason", "match_score",
        "actual_content_preview",
    ]
    write_csv(READABLE_CSV, readable, readable_fields)
    write_csv(UNREADABLE_CSV, unreadable, unreadable_fields)
    render_report(readable, unreadable)
    print(json.dumps({
        "readable_unique_papers": len(readable),
        "unreadable_or_mismatched_files": len(unreadable),
        "readable_csv": str(READABLE_CSV),
        "unreadable_csv": str(UNREADABLE_CSV),
        "report": str(REPORT_MD),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
