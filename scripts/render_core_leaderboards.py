#!/usr/bin/env python3
"""Render the four canonical leaderboard pages from data/leaderboards.csv."""

from __future__ import annotations

import csv
import json
import re
from statistics import mean
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml


CONFIG = {
    "University-1652": {
        "file": "university1652.md",
        "title": "University-1652",
        "intro": (
            "Cross-view geo-localization benchmark (Zheng et al. 2020, ACM MM'20). "
            "Two canonical retrieval protocols: **Drone-to-Satellite** (drone-view target "
            "localization) and **Satellite-to-Drone** (drone navigation). Metrics: "
            "R@1 / R@5 / R@10 / AP. Multi-weather, ablation, and cross-dataset variants "
            "are excluded."
        ),
        "protocols": ["Drone-to-Satellite", "Satellite-to-Drone"],
        "metrics": ["R@1", "R@5", "R@10", "AP"],
    },
    "SUES-200": {
        "file": "sues200.md",
        "title": "SUES-200",
        "intro": (
            "Cross-view geo-localization benchmark (Zhu et al. 2022, IEEE TCSVT). "
            "Drone-to-Satellite and Satellite-to-Drone retrieval are ranked separately. "
            "The ranking score is the arithmetic mean of R@1 at 150m, 200m, 250m, and "
            "300m; entries missing any altitude are shown as unranked."
        ),
        "protocols": [
            "Drone-to-Satellite (150m)", "Drone-to-Satellite (200m)",
            "Drone-to-Satellite (250m)", "Drone-to-Satellite (300m)",
            "Satellite-to-Drone (150m)", "Satellite-to-Drone (200m)",
            "Satellite-to-Drone (250m)", "Satellite-to-Drone (300m)",
        ],
        "metrics": ["R@1", "AP"],
    },
    "DenseUAV": {
        "file": "denseuav.md",
        "title": "DenseUAV",
        "intro": (
            "UAV self-positioning benchmark (Dai et al. 2023, IEEE TIP). The canonical "
            "task retrieves satellite-view gallery images for a drone-view query."
        ),
        "protocols": ["UAV Self-Positioning"],
        "metrics": ["R@1", "R@5", "AP", "SDM@1"],
    },
    "GTA-UAV": {
        "file": "gta_uav.md",
        "title": "GTA-UAV (Game4Loc)",
        "intro": (
            "UAV geo-localization benchmark from game data (Dai et al. 2024, Game4Loc). "
            "Cross-Area is the canonical leaderboard protocol; Same-Area is retained as a "
            "clearly separated supplementary comparison. Only each paper's complete "
            "proposed method is ranked; loss, backbone, pre-training, and component ablations "
            "are excluded."
        ),
        "protocols": ["Cross-Area", "Same-Area"],
        "metrics": ["R@1", "R@5", "AP", "SDM@3", "Dis@1"],
    },
}

SLUG = {
    "University-1652": "university1652",
    "SUES-200": "sues200",
    "DenseUAV": "denseuav",
    "UAV-VisLoc": "uav_visloc",
    "GTA-UAV": "gta_uav",
    "Game4Loc": "gta_uav",
    "World-UAV": "world_uav",
    "UAV-GeoLoc": "world_uav",
    "Nardo-Air": "nardo_air",
}


def md_escape(value: Any) -> str:
    if value in (None, ""):
        return "-"
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def paper_urls(root: Path) -> dict[str, str]:
    papers = yaml.safe_load((root / "data" / "papers.yml").read_text(encoding="utf-8")) or []
    result: dict[str, str] = {}
    for paper in papers:
        if not isinstance(paper, dict):
            continue
        urls = paper.get("urls") or {}
        source = paper.get("source") or {}
        url = (
            urls.get("paper") or urls.get("pdf") or urls.get("project")
            or (f"https://doi.org/{source['doi']}" if source.get("doi") else "")
            or (f"https://arxiv.org/abs/{source['arxiv_id']}" if source.get("arxiv_id") else "")
            or source.get("openalex_id") or ""
        )
        title = str(paper.get("title") or "").strip()
        if title and url:
            result.setdefault(title, url)
    return result


def parse_metrics(row: dict[str, str]) -> dict[str, Any]:
    try:
        metrics = json.loads(row.get("metrics_json") or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return metrics if isinstance(metrics, dict) else {}


def sort_value(row: dict[str, str]) -> float:
    metrics = parse_metrics(row)
    raw = metrics.get("R@1", row.get("sort_value"))
    try:
        return float(str(raw).replace("%", ""))
    except (TypeError, ValueError):
        return float("-inf")


def paper_cell(title: str, urls: dict[str, str]) -> str:
    label = md_escape(title)
    url = urls.get(title, "")
    return f"[{label}]({url})" if url else label


def dataset_slug(dataset: str) -> str:
    return SLUG.get(dataset, re.sub(r"[^a-z0-9]+", "_", dataset.lower()).strip("_"))


def render_sues200(
    lines: list[str],
    rows: list[dict[str, str]],
    urls: dict[str, str],
) -> int:
    """Render one method per row and rank complete records by four-altitude mean R@1."""
    heights = ("150", "200", "250", "300")
    directions = ("Drone-to-Satellite", "Satellite-to-Drone")
    rendered = 0

    for direction in directions:
        method_rows: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
        for row in rows:
            protocol = row.get("protocol", "")
            if not protocol.startswith(direction):
                continue
            match = re.search(r"(150|200|250|300)m", protocol)
            if not match:
                continue
            method_rows[(row.get("paper", ""), row.get("method", ""))][match.group(1)] = row

        complete: list[tuple[float, tuple[str, str], dict[str, dict[str, str]]]] = []
        incomplete: list[tuple[tuple[str, str], dict[str, dict[str, str]]]] = []
        for key, altitude_rows in method_rows.items():
            if all(height in altitude_rows for height in heights):
                average = mean(sort_value(altitude_rows[height]) for height in heights)
                complete.append((average, key, altitude_rows))
            else:
                incomplete.append((key, altitude_rows))
        complete.sort(key=lambda item: (-item[0], item[1][1].lower()))
        incomplete.sort(key=lambda item: item[0][1].lower())

        lines.extend([
            f"## {direction}", "",
            f"Ranked methods: **{len(complete)}**. Ranking = mean R@1 across all four altitudes.", "",
            "| Rank | Method | Avg R@1 | 150m R@1 / AP | 200m R@1 / AP | 250m R@1 / AP | 300m R@1 / AP | Paper | Source |",
            "|---:|---|---:|---:|---:|---:|---:|---|---|",
        ])
        for rank, (average, (paper, method), altitude_rows) in enumerate(complete, start=1):
            altitude_cells = []
            sources = []
            for height in heights:
                row = altitude_rows[height]
                metrics = parse_metrics(row)
                altitude_cells.append(
                    f"{md_escape(metrics.get('R@1'))} / {md_escape(metrics.get('AP'))}"
                )
                if row.get("source") and row["source"] not in sources:
                    sources.append(row["source"])
            cells = [
                str(rank), md_escape(method), f"{average:.2f}", *altitude_cells,
                paper_cell(paper, urls), md_escape("; ".join(sources)),
            ]
            lines.append("| " + " | ".join(cells) + " |")
            rendered += 1
        lines.append("")

        if incomplete:
            lines.extend([
                "### Unranked: incomplete altitude coverage", "",
                "These entries are retained for evidence, but no four-altitude average or rank is assigned.", "",
                "| Method | Available altitude(s) | R@1 / AP | Paper | Source |",
                "|---|---|---|---|---|",
            ])
            for (paper, method), altitude_rows in incomplete:
                available = sorted(altitude_rows, key=int)
                metric_cells = []
                sources = []
                for height in available:
                    row = altitude_rows[height]
                    metrics = parse_metrics(row)
                    metric_cells.append(
                        f"{height}m: {md_escape(metrics.get('R@1'))} / {md_escape(metrics.get('AP'))}"
                    )
                    if row.get("source") and row["source"] not in sources:
                        sources.append(row["source"])
                cells = [
                    md_escape(method), ", ".join(f"{height}m" for height in available),
                    "; ".join(metric_cells), paper_cell(paper, urls),
                    md_escape("; ".join(sources)),
                ]
                lines.append("| " + " | ".join(cells) + " |")
                rendered += 1
            lines.append("")
    return rendered


def render_summary(root: Path, rows: list[dict[str, str]]) -> None:
    counts = Counter(row.get("dataset", "") for row in rows)
    lines = [
        "# Leaderboards", "",
        f"Per-dataset leaderboard pages regenerated from `data/leaderboards.csv` ({len(rows)} rows). "
        "Each paper name links to its external page (arXiv, DOI, or OpenAlex).",
        "", "| Dataset | Page | Rows |", "|---|---|---:|",
    ]
    for dataset in sorted(item for item in counts if item):
        slug = dataset_slug(dataset)
        lines.append(
            f"| {md_escape(dataset)} | [{slug}.md]({slug}.md) | {counts[dataset]} |"
        )
    lines.append("")
    (root / "leaderboards" / "leaderboard_summary.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print("  wrote leaderboard_summary.md")


def render_core_leaderboards(root: Path | None = None) -> None:
    root = root or Path(__file__).resolve().parents[1]
    csv_path = root / "data" / "leaderboards.csv"
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    urls = paper_urls(root)
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row.get("dataset", ""), row.get("protocol", ""))].append(row)

    for dataset, cfg in CONFIG.items():
        lines = [f"# {cfg['title']}", "", str(cfg["intro"]), ""]
        if dataset == "SUES-200":
            dataset_rows = [row for row in rows if row.get("dataset") == dataset]
            rendered = render_sues200(lines, dataset_rows, urls)
            output = root / "leaderboards" / str(cfg["file"])
            output.write_text("\n".join(lines), encoding="utf-8")
            print(f"  wrote {output.name} ({rendered} method rows from {len(dataset_rows)} altitude rows)")
            continue
        for protocol in cfg["protocols"]:
            protocol_rows = sorted(grouped.get((dataset, protocol), []), key=sort_value, reverse=True)
            heading = protocol
            if dataset == "GTA-UAV":
                heading = (
                    "Cross-Area (official leaderboard)"
                    if protocol == "Cross-Area"
                    else "Same-Area (supplementary)"
                )
            lines.extend([
                f"## {heading}", "",
                f"Rows: **{len(protocol_rows)}** (one result row per method/configuration).", "",
            ])
            metrics = list(cfg["metrics"])
            header = ["Method", *metrics, "Paper", "Source"]
            separator = ["---", *(["---:"] * len(metrics)), "---", "---"]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(separator) + " |")
            for row in protocol_rows:
                values = parse_metrics(row)
                cells = [md_escape(row.get("method"))]
                cells.extend(md_escape(values.get(metric)) for metric in metrics)
                cells.extend([
                    paper_cell(row.get("paper", ""), urls),
                    md_escape(row.get("source")),
                ])
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")

        output = root / "leaderboards" / str(cfg["file"])
        output.write_text("\n".join(lines), encoding="utf-8")
        print(f"  wrote {output.name} ({sum(len(grouped.get((dataset, p), [])) for p in cfg['protocols'])} rows)")
    render_summary(root, rows)


if __name__ == "__main__":
    render_core_leaderboards()
