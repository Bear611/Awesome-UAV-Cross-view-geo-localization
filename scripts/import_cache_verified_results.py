#!/usr/bin/env python3
"""Import visually verified benchmark rows from the local full-text cache audit.

The script is intentionally idempotent.  A row is identified by dataset, protocol,
paper, and method; rerunning the script replaces that row instead of duplicating it.
Only canonical in-dataset protocols are imported here.  Cross-dataset, zero-shot,
multi-view, test-time augmentation, and constructed dataset variants remain in the
audit report rather than being mixed into the official leaderboards.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "leaderboards.csv"
FIELDS = [
    "dataset", "protocol", "method", "training_setting", "paper", "source",
    "verified", "sort_metric", "sort_value", "metrics_json", "notes",
]


def row(dataset: str, protocol: str, method: str, setting: str, paper: str,
        source: str, metrics: dict[str, str], notes: str = "") -> dict[str, str]:
    sort_value = metrics.get("R@1") or metrics.get("Recall@1") or ""
    return {
        "dataset": dataset,
        "protocol": protocol,
        "method": method,
        "training_setting": setting,
        "paper": paper,
        "source": source,
        "verified": "true",
        "sort_metric": "R@1",
        "sort_value": sort_value,
        "metrics_json": json.dumps(metrics, ensure_ascii=False),
        "notes": notes,
    }


def university(method: str, setting: str, paper: str, source: str,
               d2s: tuple[str, str], s2d: tuple[str, str], notes: str = "") -> list[dict[str, str]]:
    return [
        row("University-1652", "Drone-to-Satellite", method, setting, paper, source,
            {"R@1": d2s[0], "AP": d2s[1]}, notes),
        row("University-1652", "Satellite-to-Drone", method, setting, paper, source,
            {"R@1": s2d[0], "AP": s2d[1]}, notes),
    ]


def sues(method: str, setting: str, paper: str, source: str,
         d2s: list[tuple[str, str]], s2d: list[tuple[str, str]], notes: str = "") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for direction, values in (("Drone-to-Satellite", d2s), ("Satellite-to-Drone", s2d)):
        for altitude, metrics in zip((150, 200, 250, 300), values, strict=True):
            rows.append(row(
                "SUES-200", f"{direction} ({altitude}m)", method, setting, paper, source,
                {"R@1": metrics[0], "AP": metrics[1]}, notes,
            ))
    return rows


def dense(method: str, setting: str, paper: str, source: str,
          metrics: dict[str, str], notes: str = "") -> dict[str, str]:
    return row("DenseUAV", "UAV Self-Positioning", method, setting, paper, source, metrics, notes)


def verified_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    paper = "APA-BI Adaptive Partition Aggregation and Bidirectional Integration for UAV-View Geo-Localization"
    rows += university("APA-BI (384×384)", "Official split; 384×384 input", paper,
                       "Table II (dagger row), rendered PDF p.4", ("93.57", "94.55"), ("95.86", "92.88"))
    rows += sues("APA-BI", "Official split; four altitudes", paper,
                 "Table III, rendered PDF p.5",
                 [("86.45", "88.90"), ("91.85", "93.54"), ("95.70", "96.62"), ("96.70", "97.37")],
                 [("97.50", "86.21"), ("98.75", "94.03"), ("98.75", "96.95"), ("98.75", "97.82")])

    paper = "Modern Backbone for Efficient Geo-localization"
    rows += university("MBEG-L1", "Standard single-pass model; no Feature Rotate Encoder", paper,
                       "Table II, rendered PDF p.5", ("92.43", "93.72"), ("94.29", "91.90"),
                       "Feature Rotate Encoder rows are test-time augmentation and are deliberately excluded.")

    paper = "Learnable Query Aggregation with KV Routing for Cross-view Geo-localisation"
    rows += university("LQ-KV", "DINOv2 ViT-B/14; 322×322; official split", paper,
                       "Table III, rendered PDF p.5", ("94.41", "95.40"), ("96.72", "93.57"))
    rows += sues("LQ-KV", "DINOv2 ViT-B/14; official four-altitude split", paper,
                 "Table II, rendered PDF p.4",
                 [("94.70", "95.70"), ("97.93", "98.34"), ("98.73", "99.02"), ("98.85", "99.11")],
                 [("98.75", "95.61"), ("98.75", "97.70"), ("98.75", "98.47"), ("98.75", "98.91")])

    paper = "Cross-view UAV Geo-localization via Wavelet-based Local Feature Enhancement"
    rows += university("Wavelet Local Feature Enhancement", "Official split; single-pass retrieval", paper,
                       "Table I, rendered PDF p.4", ("81.63", "84.89"), ("90.31", "81.27"))

    paper = "UAV Cross-View Geo-Localization Based on Multi-Scale Partitioning and Attention-Enhanced Transformer"
    rows += university("MSLA", "ViT-B with multi-scale partitioning and local attention", paper,
                       "Table I, rendered PDF p.3", ("87.40", "89.32"), ("92.15", "87.55"))

    paper = "DOA: Advancing Cross-View Geo-Localization via Domain and Objective Alignment"
    rows += university("DOA", "TransNeXt-Tiny; 256×256; official split", paper,
                       "Table IV, rendered PDF p.8", ("92.00", "93.72"), ("95.15", "91.98"))
    rows += sues("DOA", "TransNeXt-Tiny; official four-altitude split", paper,
                 "Table III, rendered PDF p.8",
                 [("87.95", "90.20"), ("92.78", "94.15"), ("96.00", "96.91"), ("98.75", "99.05")],
                 [("96.25", "90.02"), ("98.75", "95.13"), ("98.75", "97.06"), ("100.00", "98.12")])

    paper = "SHAA: Spatial Hybrid Attention Network With Adaptive Cross-Entropy Loss Function for UAV-View Geo-Localization"
    rows += university("SHAA", "Official split; standard supervised retrieval", paper,
                       "Table IV, rendered PDF p.10", ("93.69", "94.68"), ("96.15", "93.49"))
    rows += sues("SHAA", "Official four-altitude split", paper,
                 "Table V, rendered PDF p.11",
                 [("90.32", "92.09"), ("96.50", "97.16"), ("97.30", "97.71"), ("97.40", "97.93")],
                 [("97.50", "91.50"), ("98.75", "95.68"), ("98.75", "97.45"), ("98.75", "97.31")])
    rows.append(dense("SHAA", "Official in-domain Drone→Satellite protocol", paper,
                      "Table VI, rendered PDF p.11", {"R@1": "93.69", "R@5": "98.76", "SDM@1": "94.91"}))

    paper = "MFAF: An EVA02-Based Multi-scale Frequency Attention Fusion Method for Cross-View Geo-Localization"
    rows += university("MFAF (EVA02-L)", "EVA02-L; 448×448; official split", paper,
                       "Table 2, rendered PDF p.10", ("95.06", "95.89"), ("96.01", "95.07"))
    rows += sues("MFAF (EVA02-L)", "EVA02-L; official four-altitude split", paper,
                 "Table 3, rendered PDF p.11",
                 [("95.22", "96.30"), ("98.80", "99.08"), ("97.50", "96.87"), ("97.50", "98.42")],
                 [("97.50", "96.87"), ("97.50", "98.03"), ("98.75", "97.98"), ("98.75", "98.72")])
    rows.append(dense("MFAF (EVA02-L)", "Official in-domain Drone→Satellite protocol", paper,
                      "Table 4, rendered PDF p.11", {"R@1": "95.22", "R@5": "99.93", "SDM@1": "95.23"}))

    paper = "MCL-Geo: Multi-branch Contrastive Learning for Cross-view Geo-localizationA multi-branch contrastive learning framework plus uniform cross-view contrastive loss for cross-view geo-localization targets."
    rows += university("MCL-Geo", "ConvNeXt-Tiny; official split", paper,
                       "Table 1, rendered PDF p.6", ("91.90", "93.20"), ("95.60", "90.64"))
    rows += sues("MCL-Geo", "ConvNeXt-Tiny; official four-altitude split", paper,
                 "Table 2, rendered PDF p.6",
                 [("85.57", "88.17"), ("95.37", "96.33"), ("97.23", "97.77"), ("98.45", "98.78")],
                 [("90.00", "84.11"), ("96.75", "93.45"), ("98.23", "97.63"), ("98.75", "97.74")])

    paper = "Rethinking Pooling for Multi-Granularity Features in Aerial-View Geo-Localization"
    rows += university("D²-GeM (LPN)", "ResNet-50; LPN with D²-GeM; 512×512", paper,
                       "Table IV, rendered PDF p.4", ("84.49", "86.81"), ("91.01", "80.97"))

    paper = "Do Keypoints Contain Crucial Information Mining Keypoint Information to Enhance Cross-View Geo-Localization"
    rows += university("UDPA-Net (LPN + UDPAM)", "No extra Google images; standard augmentation", paper,
                       "Table I, rendered PDF p.4", ("78.38", "81.31"), ("86.45", "77.06"),
                       "Rows using the extra Google image set are excluded.")

    paper = "SURFNet: A Surface-Aware UAV–Satellite Geolocation Framework via Feature Aggregation and Dual Positional Encoding"
    rows += university("SURFNet", "ConvNeXt-B; 224×224; in-domain training", paper,
                       "Table I, rendered PDF p.7", ("94.57", "95.49"), ("95.72", "93.20"))
    rows += sues("SURFNet", "ConvNeXt-B; official in-domain four-altitude split", paper,
                 "Table II, rendered PDF p.8",
                 [("93.63", "94.84"), ("96.20", "97.01"), ("97.58", "98.10"), ("98.68", "98.94")],
                 [("95.00", "90.75"), ("97.50", "94.78"), ("98.75", "96.42"), ("98.75", "97.87")],
                 "Cross-dataset Tables VI–VIII are zero-shot/transfer studies and are excluded from canonical rows.")

    paper = "A Transformer-Based Feature Segmentation and Region Alignment Method for UAV-View Geo-Localization"
    rows += university("FSRA (ViT-S, 512×512)", "ViT-S; k=1; 512×512 input", paper,
                       "Table II, rendered PDF p.8", ("85.50", "87.53"), ("89.73", "84.94"),
                       "The row is explicitly tagged with its larger input size; no external data are used.")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-ref",
        help="Read the base CSV from this git ref (useful when rebuilding an audit branch).",
    )
    args = parser.parse_args()
    if args.base_ref:
        completed = subprocess.run(
            ["git", "show", f"{args.base_ref}:data/leaderboards.csv"],
            cwd=ROOT, check=True, capture_output=True,
        )
        text = completed.stdout.decode("utf-8-sig")
        existing = list(csv.DictReader(text.splitlines()))
    else:
        with CSV_PATH.open(encoding="utf-8", newline="") as handle:
            existing = list(csv.DictReader(handle))
    additions = verified_rows()
    key = lambda r: (r["dataset"], r["protocol"], r["paper"], r["method"])
    additions_by_key = {key(item): item for item in additions}
    output: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for item in existing:
        item_key = key(item)
        if item_key in seen:
            continue
        output.append(additions_by_key.pop(item_key, item))
        seen.add(item_key)
    output.extend(additions_by_key.values())
    before = len(seen)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    print(json.dumps({
        "existing_unique_rows": before,
        "verified_cache_rows": len(additions),
        "new_or_replaced_rows": len(output) - before,
        "final_rows": len(output),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
