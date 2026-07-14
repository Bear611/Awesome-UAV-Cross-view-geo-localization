#!/usr/bin/env python3
"""Validate leaderboard structure and write a reproducible audit report."""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "leaderboards.csv"
REPORT_PATH = ROOT / "data" / "reports" / "leaderboard_validation_report.md"

CORE = {
    "University-1652": {
        "file": "university1652.md",
        "protocols": {"Drone-to-Satellite", "Satellite-to-Drone"},
    },
    "SUES-200": {
        "file": "sues200.md",
        "protocols": {
            "Drone-to-Satellite (150m)", "Drone-to-Satellite (200m)",
            "Drone-to-Satellite (250m)", "Drone-to-Satellite (300m)",
            "Satellite-to-Drone (150m)", "Satellite-to-Drone (200m)",
            "Satellite-to-Drone (250m)", "Satellite-to-Drone (300m)",
        },
    },
    "DenseUAV": {"file": "denseuav.md", "protocols": {"UAV Self-Positioning"}},
    "GTA-UAV": {
        "file": "gta_uav.md",
        "protocols": {"Same-Area", "Cross-Area"},
    },
}

# MEAN is intentionally absent: it is the published acronym for the
# Multi-Level Embedding and Alignment Network, not a placeholder.
PLACEHOLDER_METHODS = {
    "GEO-LOCALIZATION", "CROSS-VIEW", "CONVNEXT-BASED", "RESOURCE-EFFICIENT",
    "ENVIRONMENT-INDEPENDENT", "WEATHER-INVARIANT", "PARAMETER-EFFICIENT",
    "PROTOTYPE-BASED", "MULTI-LEVEL", "SELF-LOCALIZATION", "VISION-LANGUAGE",
    "GEO-LOCATION", "FRAMEWORK-WITH-GEOGRAPHIC-INFO-ADAPTIVE-LOSS",
    "UAV-SATELLITE", "ORIENTATION-FREE", "IMPROVING",
}


def parse_metrics(row: dict[str, str], errors: list[str], line_no: int) -> dict[str, Any]:
    try:
        value = json.loads(row.get("metrics_json") or "{}")
    except json.JSONDecodeError as exc:
        errors.append(f"CSV line {line_no}: invalid metrics_json ({exc})")
        return {}
    if not isinstance(value, dict):
        errors.append(f"CSV line {line_no}: metrics_json is not an object")
        return {}
    return value


def number(value: Any) -> float | None:
    if value in (None, "", "-"):
        return None
    try:
        result = float(str(value).replace("%", "").strip())
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def markdown_data_rows(path: Path) -> int:
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        if line.startswith("| Method ") or line.startswith("| Rank ") or line.startswith("| ---"):
            continue
        count += 1
    return count


def sues_method_rows(rows: list[dict[str, str]]) -> int:
    """Count rendered SUES method rows after collapsing altitude rows."""
    keys: set[tuple[str, str, str]] = set()
    for row in rows:
        if row.get("dataset") != "SUES-200":
            continue
        protocol = row.get("protocol", "")
        direction = "Drone-to-Satellite" if protocol.startswith("Drone-to-Satellite") else "Satellite-to-Drone"
        keys.add((direction, row.get("paper", ""), row.get("method", "")))
    return len(keys)


def validate_sues_average_ranking(rows: list[dict[str, str]], errors: list[str]) -> None:
    """Check that the rendered SUES rank/order/average matches all four R@1 values."""
    page_text = (ROOT / "leaderboards" / "sues200.md").read_text(encoding="utf-8")
    heights = ("150", "200", "250", "300")
    for direction in ("Drone-to-Satellite", "Satellite-to-Drone"):
        groups: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
        for row in rows:
            if row.get("dataset") != "SUES-200" or not row.get("protocol", "").startswith(direction):
                continue
            match = re.search(r"(150|200|250|300)m", row.get("protocol", ""))
            metrics = json.loads(row.get("metrics_json") or "{}")
            r1 = number(metrics.get("R@1"))
            if match and r1 is not None:
                groups[(row.get("paper", ""), row.get("method", ""))][match.group(1)] = r1
        expected = []
        for (paper, method), values in groups.items():
            if all(height in values for height in heights):
                average = sum(values[height] for height in heights) / 4
                expected.append((method, average))
        expected.sort(key=lambda item: (-item[1], item[0].lower()))

        try:
            section = page_text.split(f"## {direction}", 1)[1].split("\n## ", 1)[0]
        except IndexError:
            errors.append(f"SUES-200: missing rendered section {direction}")
            continue
        actual = []
        for line in section.splitlines():
            if not re.match(r"^\| \d+ \|", line):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            actual.append((int(cells[0]), cells[1].replace("\\|", "|"), number(cells[2])))
        if len(actual) != len(expected):
            errors.append(
                f"SUES-200 {direction}: ranked rows={len(actual)}, complete four-altitude methods={len(expected)}"
            )
            continue
        for rank, ((actual_rank, actual_method, actual_average), (method, average)) in enumerate(
            zip(actual, expected), start=1
        ):
            if actual_rank != rank or actual_method != method:
                errors.append(
                    f"SUES-200 {direction}: rank {rank} mismatch; rendered={actual_method!r}, expected={method!r}"
                )
            if actual_average is None or not math.isclose(actual_average, average, rel_tol=0, abs_tol=0.005001):
                errors.append(
                    f"SUES-200 {direction}: {method} average mismatch; rendered={actual_average}, expected={average:.4f}"
                )


def validate() -> tuple[list[str], list[str], list[str]]:
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    empty_metrics: Counter[str] = Counter()
    verified: Counter[str] = Counter()
    placeholder: Counter[str] = Counter()
    inferred: Counter[str] = Counter()
    rows_by_dataset: Counter[str] = Counter()
    protocols: dict[str, set[str]] = defaultdict(set)
    keys: Counter[tuple[str, str, str, str]] = Counter()

    for index, row in enumerate(rows, start=2):
        dataset = row.get("dataset", "")
        rows_by_dataset[dataset] += 1
        protocols[dataset].add(row.get("protocol", ""))
        keys[(dataset, row.get("protocol", ""), row.get("paper", ""), row.get("method", ""))] += 1
        metrics = parse_metrics(row, errors, index)
        meaningful = {k: v for k, v in metrics.items() if v not in (None, "", "-")}
        if not meaningful:
            empty_metrics[dataset] += 1
        if str(row.get("verified", "")).strip().lower() in {"true", "yes", "1"}:
            verified[dataset] += 1
        if row.get("method") in PLACEHOLDER_METHODS:
            placeholder[dataset] += 1
        note_text = f"{row.get('notes', '')} {row.get('source', '')}".lower()
        if any(token in note_text for token in (
            "inferred", "≈", "approx", "not explicitly stated",
            "visual verification pending", "restored from the extraction evidence",
        )):
            inferred[dataset] += 1
        if not row.get("paper") or not row.get("source"):
            warnings.append(f"CSV line {index}: missing paper/source for {dataset}")

        for metric, value in meaningful.items():
            numeric = number(value)
            if numeric is None:
                warnings.append(f"CSV line {index}: non-numeric {metric}={value!r}")
                continue
            normalized = metric.lower().replace(" ", "")
            if any(token in normalized for token in ("r@", "recall", "map", "ap", "sdm")):
                if not 0 <= numeric <= 100:
                    errors.append(f"CSV line {index}: out-of-range {metric}={numeric}")

        sort_metric = row.get("sort_metric", "").strip()
        sort_numeric = number(row.get("sort_value"))
        metric_numeric = number(metrics.get(sort_metric)) if sort_metric else None
        if dataset in CORE and not meaningful:
            errors.append(f"CSV line {index}: core row has no metrics ({dataset}, {row.get('method', '')})")
        if dataset == "SUES-200" and "R@1" not in meaningful:
            errors.append(
                f"CSV line {index}: SUES-200 row lacks R@1 "
                f"({row.get('protocol', '')}, {row.get('method', '')})"
            )
        if dataset in CORE and (not sort_metric or sort_numeric is None):
            errors.append(f"CSV line {index}: core row lacks numeric sort field")
        if dataset in CORE and sort_metric not in metrics:
            errors.append(f"CSV line {index}: core sort metric {sort_metric!r} absent from metrics_json")
        if sort_metric and sort_numeric is not None and metric_numeric is not None:
            # Mean values can retain four decimals in sort_value while the
            # display metric is rounded to two decimals.
            if not math.isclose(sort_numeric, metric_numeric, rel_tol=0, abs_tol=0.005001):
                errors.append(
                    f"CSV line {index}: sort {sort_metric}={sort_numeric} conflicts with metrics_json={metric_numeric}"
                )

    for dataset, cfg in CORE.items():
        actual = protocols.get(dataset, set())
        expected = set(cfg["protocols"])
        if actual != expected:
            errors.append(
                f"{dataset}: protocol mismatch; missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}"
            )
        page = ROOT / "leaderboards" / str(cfg["file"])
        if not page.exists():
            errors.append(f"{dataset}: missing rendered page {page.name}")
        else:
            rendered = markdown_data_rows(page)
            expected_rendered = sues_method_rows(rows) if dataset == "SUES-200" else rows_by_dataset[dataset]
            if rendered != expected_rendered:
                errors.append(
                    f"{dataset}: rendered rows={rendered}, expected rendered rows={expected_rendered}"
                )

    validate_sues_average_ranking(rows, errors)

    if (ROOT / "leaderboards" / "gta-uav.md").exists():
        errors.append("stale duplicate leaderboards/gta-uav.md still exists")

    summary = (ROOT / "leaderboards" / "leaderboard_summary.md").read_text(encoding="utf-8")
    if "[gta_uav.md](gta_uav.md)" not in summary:
        errors.append("leaderboard_summary.md does not link to gta_uav.md")
    if f"`data/leaderboards.csv` ({len(rows)} rows)" not in summary:
        errors.append("leaderboard_summary.md total row count is stale")
    for dataset, cfg in CORE.items():
        expected_line = (
            f"| {dataset} | [{cfg['file']}]({cfg['file']}) | {rows_by_dataset[dataset]} |"
        )
        if expected_line not in summary:
            errors.append(f"leaderboard_summary.md count/link is stale for {dataset}")

    duplicate_keys = [(key, count) for key, count in keys.items() if count > 1]
    for key, count in duplicate_keys:
        warnings.append(f"duplicate logical key x{count}: {key}")

    lines = [
        "# Leaderboard Validation Report", "",
        "This report validates repository structure and internal consistency. A `verified` flag is treated as a claim in the data, not as independent proof that the original paper was checked.", "",
        "| Dataset | Rows | Empty metrics | Placeholder methods | Verified flag | Inferred/indirect evidence |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for dataset in CORE:
        lines.append(
            f"| {dataset} | {rows_by_dataset[dataset]} | {empty_metrics[dataset]} | "
            f"{placeholder[dataset]} | {verified[dataset]} | {inferred[dataset]} |"
        )
    sues_missing_ap = sum(
        1 for row in rows
        if row.get("dataset") == "SUES-200" and "AP" not in json.loads(row.get("metrics_json") or "{}")
    )
    lines.extend([
        "", "## Evidence boundary", "",
        "The repair script records rendered-original-table checks for DINOv2+GLFA+CESP, OriLoc, "
        "Improving Localization in Internet of Drones, CGSI, SCOF, (MGS)2-Net, AFMS-Net, BGG, "
        "Sample4Geo-DPHR, MADA-SSA, ConvNeXt multi-level learning, and MEAN.",
        "",
        f"Rows still carrying `verified=false`: University-1652 **{rows_by_dataset['University-1652'] - verified['University-1652']}**, "
        f"SUES-200 **{rows_by_dataset['SUES-200'] - verified['SUES-200']}**, "
        f"DenseUAV **{rows_by_dataset['DenseUAV'] - verified['DenseUAV']}**, "
        f"GTA-UAV **{rows_by_dataset['GTA-UAV'] - verified['GTA-UAV']}**. "
        "These are not declared wrong; they have not all been independently rechecked in this repair.",
        "",
        "MFFN-AAE contributes 8 SUES-200 rows restored from extraction evidence; direct visual access to "
        "the original table remains pending, so those rows deliberately remain unverified.",
        "",
        f"SUES-200 rows without AP: **{sues_missing_ap}** (AdaptGeo reports retained R@1 values only). "
        "Missing metrics are left absent rather than guessed.",
    ])
    lines.extend(["", f"Structural errors: **{len(errors)}**", f"Warnings: **{len(warnings)}**", ""])
    if errors:
        lines.extend(["## Errors", "", *[f"- {item}" for item in errors], ""])
    if warnings:
        lines.extend(["## Warnings", "", *[f"- {item}" for item in warnings], ""])
    if not errors:
        notes.append(
            "All core rows have metrics and numeric sort fields; protocol sets, SUES R@1 coverage and four-altitude average ranking, "
            "rendered/summary row counts, numeric ranges, duplicate keys, and GTA navigation checks passed."
        )
        lines.extend(["## Result", "", notes[-1], ""])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return errors, warnings, notes


def main() -> int:
    errors, warnings, notes = validate()
    print(f"validation: {len(errors)} errors, {len(warnings)} warnings")
    for item in errors:
        print(f"ERROR: {item}")
    for item in notes:
        print(f"OK: {item}")
    print(f"report: {REPORT_PATH}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
