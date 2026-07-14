#!/usr/bin/env python3
"""Deterministically restore leaderboard fields already preserved elsewhere in each row."""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "leaderboards.csv"

# These replacements are supported directly by the paper title or by a
# non-placeholder method already used for the same paper elsewhere in the CSV.
METHOD_BY_TITLE_PREFIX = {
    "AGEN: Adaptive Error Control-Driven": "AGEN",
    "MobileGeo Exploring Hierarchical Knowledge Distillation": "MobileGeo",
    "Multi-level representation learning via ConvNeXt-based": (
        "ConvNeXt-based Multi-level Representation Learning"
    ),
}

# Values below were checked against rendered original-paper tables.  Keeping
# them here makes the correction reproducible and records the exact evidence.
VERIFIED_CORRECTIONS = {
    (
        "DenseUAV",
        "UAV Self-Positioning",
        "DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments",
        "DINOv2 + GLFA + CESP (Proposed)",
    ): {
        "metrics": {"R@1": "86.27", "R@5": "96.83", "SDM@1": "88.87"},
        "source": "Table I, p.2084 (PDF p.5)",
        "notes": "Original-paper Table I. AnyLoc, not the proposed method, has R@1=14.24.",
    },
    (
        "University-1652",
        "Drone-to-Satellite",
        "OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization",
        "OriLoc",
    ): {
        "metrics": {"R@1": "80.03", "AP": "83.95"},
        "source": "Table VI, p.15518 (PDF p.11)",
        "notes": "Original-paper Table VI, OriLoc (ours), Drone2Sat columns.",
    },
    (
        "University-1652",
        "Satellite-to-Drone",
        "OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization",
        "OriLoc",
    ): {
        "metrics": {"R@1": "92.73", "AP": "80.75"},
        "source": "Table VI, p.15518 (PDF p.11)",
        "notes": "Original-paper Table VI, OriLoc (ours), Sat2Drone columns.",
    },
    (
        "University-1652",
        "Drone-to-Satellite",
        "Improving the Localization Accuracy in Internet of Drones Networks",
        "ResNet-101 + cosine similarity",
    ): {
        "metrics": {"R@1": "78.23", "R@5": "86.35", "R@10": "92.11", "AP": "83.65"},
        "source": "Figure 4 and Table III, PDF p.5",
        "notes": "Original-paper Figure 4 and Table III; the paper describes UAV-to-satellite matching.",
    },
    (
        "University-1652",
        "Drone-to-Satellite",
        "CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization",
        "CGSI",
    ): {
        "method": "CGSI (Ours + Post-process)",
        "metrics": {"R@1": "95.90", "AP": "96.48"},
        "source": "Table I, PDF p.9",
        "notes": "Original-paper Table I, CGSI (Ours + Post-process), Drone-to-Satellite columns.",
    },
    (
        "University-1652",
        "Satellite-to-Drone",
        "CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization",
        "CGSI",
    ): {
        "method": "CGSI (Ours + Post-process)",
        "metrics": {"R@1": "96.72", "AP": "96.44"},
        "source": "Table I, PDF p.9",
        "notes": "Original-paper Table I, CGSI (Ours + Post-process), Satellite-to-Drone columns.",
    },
}

# Accept the corrected method name on later idempotent runs as well.
for _key, _value in list(VERIFIED_CORRECTIONS.items()):
    if _value.get("method"):
        VERIFIED_CORRECTIONS[(*_key[:3], str(_value["method"]))] = _value

DUPLICATE_METHOD_ROWS = {
    (
        "DenseUAV",
        "UAV Self-Positioning",
        "DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments",
        "DINOv2-GLFA-CESP",
    ),
    (
        "DenseUAV",
        "UAV Self-Positioning",
        "DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments",
        "Proposed (DINOv2 + GLFA + CESP)",
    ),
    (
        "University-1652",
        "Drone-to-Satellite",
        "Improving the Localization Accuracy in Internet of Drones Networks",
        "ResNet-101 backbone with global pooling, 512-D FC embedding, and cosine similarity for retrieval",
    ),
    (
        "University-1652",
        "Drone-to-Satellite",
        "Improving the Localization Accuracy in Internet of Drones Networks",
        "IMPROVING",
    ),
    (
        "University-1652",
        "Drone-to-Satellite",
        "A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization",
        "Ours (Heatmap-guided Swin-Transformer + LightGCN)",
    ),
    (
        "University-1652",
        "Satellite-to-Drone",
        "A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization",
        "Ours (Heatmap-guided Swin-Transformer + LightGCN)",
    ),
    (
        "University-1652",
        "Satellite-to-Drone",
        "Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization",
        "Proposed (Multibranch Joint Representation Learning with IFSs)",
    ),
}

ALTITUDES = ("150m", "200m", "250m", "300m")

# Several extraction rows preserved four per-altitude values only inside their
# notes/mean fields and were incorrectly attached to one altitude.  Expand
# those rows back to the eight canonical SUES-200 protocols.  These remain
# unverified until the corresponding original table has been visually checked.
SUES_ALTITUDE_RESULTS = {
    "CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization": {
        "method": "CGSI (Ours)", "source": "Table IV, PDF p.10", "table_verified": True,
        "d2s_r1": [95.95, 97.72, 97.60, 97.83], "d2s_ap": [96.80, 98.15, 98.03, 98.23],
        "s2d_r1": [97.50, 98.75, 98.75, 98.75], "s2d_ap": [96.22, 97.62, 98.01, 97.92],
    },
    "SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization": {
        "method": "SCOF (Ours)", "source": "Table IX, PDF p.11", "table_verified": True,
        "d2s_r1": [90.75, 94.25, 96.88, 97.85], "d2s_ap": [92.32, 95.35, 97.42, 98.10],
        "s2d_r1": [95.00, 97.50, 98.75, 97.50], "s2d_ap": [89.92, 93.13, 96.33, 96.62],
    },
    "(MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization": {
        "method": "(MGS)2-Net", "source": "Table 2, arXiv v2 PDF p.11", "table_verified": True,
        "d2s_r1": [98.45, 99.62, 99.78, 100.00], "d2s_ap": [98.78, 99.69, 99.80, 100.00],
        "s2d_r1": [98.75, 100.00, 100.00, 100.00], "s2d_ap": [96.50, 98.51, 98.73, 98.95],
    },
    "Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization": {
        "method": "AFMS-Net", "source": "Table 2, PDF p.18", "table_verified": True,
        "d2s_r1": [85.25, 90.53, 93.03, 94.05], "d2s_ap": [88.24, 92.24, 94.32, 95.25],
        "s2d_r1": [96.50, 98.75, 98.75, 97.50], "s2d_ap": [82.83, 92.01, 93.55, 94.23],
    },
    "BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization": {
        "method": "BGG", "source": "Tables II and III, PDF p.8", "table_verified": True,
        "d2s_r1": [99.30, 99.45, 99.53, 99.25], "d2s_ap": [99.46, 99.55, 99.63, 99.38],
        "s2d_r1": [98.75, 98.75, 98.75, 98.75], "s2d_ap": [98.22, 98.24, 98.73, 98.68],
    },
    "Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization": {
        "method": "Sample4Geo-DPHR", "source": "Table 2, arXiv v3 PDF p.4", "table_verified": True,
        "d2s_r1": [94.55, 95.43, 98.95, 99.80], "d2s_ap": [95.60, 96.36, 99.14, 99.85],
        "s2d_r1": [95.00, 97.50, 98.75, 99.88], "s2d_ap": [90.73, 94.41, 97.70, 99.90],
    },
    "MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization": {
        "method": "MADA-SSA", "source": "Table 2, PDF p.15", "table_verified": True,
        "d2s_r1": [88.12, 94.17, 96.65, 97.72], "d2s_ap": [90.44, 95.31, 97.38, 98.25],
        "s2d_r1": [96.25, 98.75, 98.75, 97.50], "s2d_ap": [87.33, 96.12, 97.64, 97.71],
    },
    "Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching": {
        "method": "ConvNeXt-based Multi-level Representation Learning", "source": "Table 3, PDF p.9", "table_verified": True,
        "d2s_r1": [83.05, 89.65, 94.05, 95.75], "d2s_ap": [86.00, 91.81, 95.62, 96.30],
        "s2d_r1": [95.00, 96.25, 97.50, 98.80], "s2d_ap": [91.82, 93.43, 96.40, 97.06],
    },
    "Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization": {
        "method": "MFFN-AAE", "source": "Table III",
        "d2s_r1": [88.07, 93.75, 95.07, 96.15], "d2s_ap": [90.82, 94.81, 95.98, 96.83],
        "s2d_r1": [95.00, 96.26, 96.25, 97.50], "s2d_ap": [88.23, 93.60, 94.75, 96.05],
    },
    "Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization": {
        "method": "MEAN", "source": "Tables III and IV, PDF p.10", "table_verified": True,
        "d2s_r1": [95.50, 98.38, 98.95, 99.52], "d2s_ap": [96.46, 98.72, 99.17, 99.63],
        "s2d_r1": [97.50, 100.00, 100.00, 100.00], "s2d_ap": [94.75, 97.09, 98.28, 99.21],
    },
}


def meaningful(value: object) -> bool:
    return value not in (None, "", "-")


def load_metrics(raw: str) -> dict[str, object]:
    try:
        value = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def rescue(rows: list[dict[str, str]]) -> tuple[int, int, int, int, int]:
    restored_metrics = 0
    restored_sort_values = 0
    restored_methods = 0
    verified_corrections = 0
    for row in rows:
        metrics = load_metrics(row.get("metrics_json", ""))
        sort_metric = (row.get("sort_metric") or "").strip()
        sort_value = (row.get("sort_value") or "").strip()
        if not any(meaningful(value) for value in metrics.values()) and sort_metric and sort_value:
            metrics[sort_metric] = sort_value
            row["metrics_json"] = json.dumps(metrics, ensure_ascii=False)
            restored_metrics += 1
        if sort_metric and not sort_value and meaningful(metrics.get(sort_metric)):
            row["sort_value"] = str(metrics[sort_metric])
            restored_sort_values += 1

        title = row.get("paper", "")
        for prefix, method in METHOD_BY_TITLE_PREFIX.items():
            if title.startswith(prefix) and row.get("method") != method:
                row["method"] = method
                restored_methods += 1
                break

        key = (row.get("dataset", ""), row.get("protocol", ""), title, row.get("method", ""))
        correction = VERIFIED_CORRECTIONS.get(key)
        if correction:
            desired_metrics = correction["metrics"]
            desired = {
                "method": str(correction.get("method", row.get("method", ""))),
                "metrics_json": json.dumps(desired_metrics, ensure_ascii=False),
                "sort_metric": "R@1",
                "sort_value": str(desired_metrics["R@1"]),
                "source": str(correction["source"]),
                "notes": str(correction["notes"]),
                "verified": "true",
            }
            if any(row.get(field) != value for field, value in desired.items()):
                row.update(desired)
                verified_corrections += 1
    before = len(rows)
    rows[:] = [
        row for row in rows
        if (row.get("dataset", ""), row.get("protocol", ""), row.get("paper", ""), row.get("method", ""))
        not in DUPLICATE_METHOD_ROWS
    ]
    return restored_metrics, restored_sort_values, restored_methods, verified_corrections, before - len(rows)


def write_atomic(rows: list[dict[str, str]], fields: list[str]) -> None:
    tmp = CSV_PATH.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp, CSV_PATH)


def expand_sues_altitudes(rows: list[dict[str, str]]) -> tuple[int, int]:
    replaced = 0
    generated = 0
    for paper, result in SUES_ALTITUDE_RESULTS.items():
        matches = [row for row in rows if row.get("dataset") == "SUES-200" and row.get("paper") == paper]
        if not matches:
            continue
        template = dict(matches[0])
        desired: list[dict[str, str]] = []
        for direction, r1_key, ap_key in (
            ("Drone-to-Satellite", "d2s_r1", "d2s_ap"),
            ("Satellite-to-Drone", "s2d_r1", "s2d_ap"),
        ):
            for index, altitude in enumerate(ALTITUDES):
                row = dict(template)
                r1 = result[r1_key][index]
                ap = result[ap_key][index]
                row.update({
                    "dataset": "SUES-200",
                    "protocol": f"{direction} ({altitude})",
                    "method": str(result["method"]),
                    "source": str(result["source"]),
                    "sort_metric": "R@1",
                    "sort_value": f"{r1:.2f}",
                    "metrics_json": json.dumps({"R@1": f"{r1:.2f}", "AP": f"{ap:.2f}"}, ensure_ascii=False),
                    "verified": "true" if result.get("table_verified") else "false",
                    "notes": (
                        "Per-altitude value visually checked against the rendered original-paper table."
                        if result.get("table_verified") else
                        "Per-altitude value restored from the extraction evidence; original-table visual verification pending."
                    ),
                })
                desired.append(row)

        comparable = lambda row: (
            row.get("protocol"), row.get("method"), row.get("sort_value"),
            row.get("metrics_json"), row.get("source"), row.get("verified"), row.get("notes"),
        )
        if sorted(map(comparable, matches)) != sorted(map(comparable, desired)):
            rows[:] = [
                row for row in rows
                if not (row.get("dataset") == "SUES-200" and row.get("paper") == paper)
            ]
            rows.extend(desired)
            replaced += len(matches)
            generated += len(desired)
    return replaced, generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the deterministic repairs")
    args = parser.parse_args()

    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    metrics, sort_values, methods, corrections, duplicates = rescue(rows)
    replaced, generated = expand_sues_altitudes(rows)
    action = "applied" if args.apply else "would apply"
    print(
        f"{action}: {metrics} metric restorations, {sort_values} sort-value restorations, "
        f"{methods} method-name restorations, "
        f"{corrections} original-table corrections, {duplicates} duplicate rows removed, "
        f"{replaced} misplaced SUES rows replaced by {generated} per-altitude rows"
    )
    if args.apply:
        write_atomic(rows, fields)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
