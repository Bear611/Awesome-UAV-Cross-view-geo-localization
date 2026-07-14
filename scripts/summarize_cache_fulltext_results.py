#!/usr/bin/env python3
"""Create the final readable/unreadable cache audit and result disposition tables."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READABLE = ROOT / "data" / "reports" / "cache_pdf_readable.csv"
UNREADABLE = ROOT / "data" / "reports" / "cache_pdf_unreadable.csv"
LEADERBOARD = ROOT / "data" / "leaderboards.csv"
OUTPUT = ROOT / "data" / "reports" / "cache_fulltext_results.csv"
REPORT = ROOT / "data" / "reports" / "cache_fulltext_results.md"

ADDED = {
    "5f4142a58af4": ("APA-BI", "University-1652; SUES-200"),
    "573972da87de": ("MBEG-L1", "University-1652"),
    "f11512cc1a97": ("LQ-KV", "University-1652; SUES-200"),
    "bd375063449b": ("Wavelet Local Feature Enhancement", "University-1652"),
    "b5ab5786cd9c": ("MSLA", "University-1652"),
    "41f846965028": ("DOA", "University-1652; SUES-200"),
    "2aea7cfc1827": ("SHAA", "University-1652; SUES-200; DenseUAV"),
    "fc7381acc7dd": ("MFAF", "University-1652; SUES-200; DenseUAV"),
    "3b653d54791c": ("MCL-Geo", "University-1652; SUES-200"),
    "daf790654cfb": ("D²-GeM", "University-1652"),
    "a49bd8bbea92": ("UDPA-Net", "University-1652"),
    "168d02a9b466": ("SURFNet", "University-1652; SUES-200"),
    "de5c1acf58ab": ("FSRA", "University-1652"),
}

ALREADY_PRESENT_ALIAS = {
    "933a07cca9fd": "MobileGeo core rows already exist under the shorter MobileGeo paper title; multi-view refinement is noncanonical.",
    "189d681f636e": "World-UAV/UAVPlace and Nardo-Air tables are already present on their dedicated manually curated pages.",
    "757be77ae202": "AerialVL benchmark results are already present on the dedicated AerialVL page.",
    "83972fc6c838": "SUES-200 baseline rows are already present under the original benchmark-paper alias.",
    "d92f0e26bb84": "University160k-WX result is already represented on its separate protocol page.",
}

SPECIAL_EXCLUSIONS = {
    "2040e36dc653": "Tables use constructed GTA-UAV-MM and UAV-VisLoc-MM multimodal variants, not the canonical datasets.",
    "7ac44ed43a07": "Evaluates multi-environment and unseen-environment benchmark variants; not the canonical clean splits.",
    "c3321ed351c8": "GTA-UAV results use RGBD/depth priors plus EMA; canonical GTA-UAV policy is RGB-only.",
    "ab9dab27b058": "Unsupervised multi-view query protocol (Nv=30/50); not the official single-image protocol.",
    "7bcacdaff17e": "Reports UL14 heatmap localization (RDS/MA), not a canonical retrieval leaderboard protocol.",
    "6cdb7194b925": "Introduces and evaluates the separate Multi-UAV dataset and meter-level protocol.",
    "50abb7ac99ee": "Introduces the separate MTA tilt-angle dataset.",
    "f492b9c680a8": "Uses the separate VDUAV dataset and RDS/meter-level accuracy protocol.",
    "a7fcf3489f1b": "DenseUAV is evaluated as 3D position RMSE after feature matching, not canonical retrieval R@K/SDM.",
    "d2714d8c0bdf": "Uses private/controlled aerial-to-satellite routes and pose metrics, not a listed canonical split.",
    "d3cdc2d6ff0a": "Uses virtual-world day/rain/evening/night datasets rather than canonical UAV retrieval splits.",
    "82930fdbcd52": "Cross-view object bounding-box localization uses acc@IoU, not place-retrieval metrics.",
    "468b748ff556": "Local-region object geo-localization uses acc@0.25/0.5, not University-1652 retrieval.",
    "d92f0e26bb84": "Uses the University160k-WX multi-weather competition protocol, kept separate from University-1652.",
    "c7e57d895be7": "Survey/challenge overview; no new primary benchmark result.",
    "54e4a5a123a2": "Review article; contains secondary comparisons, not a new method result.",
    "ab2b9558e629": "Survey article; contains secondary comparisons, not a new method result.",
    "e762d8c49f13": "Kalman-filter notes; no UAV-CVGL benchmark experiment.",
    "54ed1af6a9b3": "Path-planning paper; no canonical cross-view retrieval experiment.",
}


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: str) -> str:
    return " ".join((value or "").replace("|", "/").split())


def main() -> int:
    readable = load(READABLE)
    unreadable = load(UNREADABLE)
    leaderboard = load(LEADERBOARD)
    leaderboard_by_paper = Counter(row["paper"] for row in leaderboard)
    output: list[dict[str, str]] = []

    for item in readable:
        ident = item["paper_id"].split(";", 1)[0]
        if ident in ADDED:
            method, datasets = ADDED[ident]
            matching = [r for r in leaderboard if r["paper"] == item["title"] and method.split()[0] in r["method"]]
            disposition = "added_to_canonical_leaderboards"
            summary = f"{method}: visually verified canonical results on {datasets}."
            action = f"added {len(matching)} verified protocol rows"
        elif item["currently_on_leaderboard"] == "true":
            disposition = "already_represented"
            count = leaderboard_by_paper[item["title"]]
            summary = "Full text extracted; result/comparison pages indexed; existing leaderboard representation retained."
            action = f"kept existing rows ({count} exact-title rows)"
        elif ident in ALREADY_PRESENT_ALIAS:
            disposition = "already_represented_under_alias_or_manual_page"
            summary = ALREADY_PRESENT_ALIAS[ident]
            action = "no duplicate row added"
        else:
            disposition = "readable_but_not_canonical_addition"
            summary = SPECIAL_EXCLUSIONS.get(
                ident,
                "Full text and candidate result pages were read, but the reported experiment is a different dataset, task, metric, transfer setting, survey, or navigation/local-matching protocol.",
            )
            action = "kept in audit only"
        output.append({
            "paper_id": item["paper_id"],
            "title": item["title"],
            "cache_category": "readable",
            "full_text_status": "complete",
            "benchmark_disposition": disposition,
            "datasets_keyword_scan": item["datasets_mentioned"],
            "result_pages": item["result_pages"],
            "comparison_pages": item["comparison_pages"],
            "result_summary": summary,
            "leaderboard_action": action,
            "pdf_file": item["pdf_file"],
        })

    fields = list(output[0])
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)

    counts = Counter(row["benchmark_disposition"] for row in output)
    added_rows = sum(1 for row in leaderboard if row["verified"].lower() == "true" and row["paper"] in {r["title"] for r in readable if r["paper_id"].split(";", 1)[0] in ADDED})
    lines = [
        "# Cached Full-Text Result Audit", "",
        "The cache was validated by PDF signature and title/content matching, then fully text-extracted. "
        "Candidate result pages were indexed and canonical additions were checked against rendered original PDF pages.", "",
        "## Totals", "",
        "| Category | Papers/files | Outcome |", "|---|---:|---|",
        f"| Readable unique papers | {len(output)} | Full text extracted and disposition recorded |",
        f"| Unreadable or wrong cached files | {len(unreadable)} | Kept separate; intended paper cannot be trusted from this cache file |",
        f"| Newly added canonical method papers | {counts['added_to_canonical_leaderboards']} | {added_rows} verified protocol rows |",
        f"| Already represented | {counts['already_represented'] + counts['already_represented_under_alias_or_manual_page']} | Existing/alias/manual rows retained |",
        f"| Readable, no canonical addition | {counts['readable_but_not_canonical_addition']} | Different protocol/task/dataset or no primary result |",
        "", "## Newly added canonical results", "",
        "| Paper ID | Method | Canonical datasets |", "|---|---|---|",
    ]
    for ident, (method, datasets) in ADDED.items():
        lines.append(f"| {ident} | {method} | {datasets} |")

    lines += ["", "## Readable papers: complete disposition table", "",
              "`datasets_keyword_scan` is a discovery aid and may include datasets mentioned only in related work.", "",
              "| ID | Title | Disposition | Result/action summary | Candidate pages |", "|---|---|---|---|---|"]
    for item in output:
        pages = item["comparison_pages"] or item["result_pages"] or "-"
        lines.append(
            f"| {clean(item['paper_id'])} | {clean(item['title'])} | {item['benchmark_disposition']} | "
            f"{clean(item['result_summary'])} {clean(item['leaderboard_action'])} | {pages} |"
        )

    lines += ["", "## Unreadable or mismatched cached files", "",
              "| Intended paper ID | Intended title | Cached file | Failure |", "|---|---|---|---|"]
    for item in unreadable:
        reason = (
            item.get("reason") or item.get("read_status") or item.get("failure_reason")
            or item.get("notes") or "unreadable/mismatched"
        )
        lines.append(
            f"| {clean(item.get('paper_id', ''))} | {clean(item.get('title', ''))} | "
            f"{clean(item.get('pdf_file', ''))} | {clean(reason)} |"
        )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print({"readable": len(output), "unreadable": len(unreadable), "dispositions": dict(counts), "verified_rows": added_rows})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
