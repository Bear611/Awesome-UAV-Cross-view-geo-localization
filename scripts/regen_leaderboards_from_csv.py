#!/usr/bin/env python3
"""Regenerate leaderboard markdown pages from data/leaderboards.csv with paper hyperlinks."""
import csv, re
from pathlib import Path
import yaml

ROOT = Path(r"D:/download/awesome-uav-cvgl-v0.1/awesome-uav-cvgl-v0.1")
CSV = ROOT / "data/leaderboards.csv"
OUT = ROOT / "leaderboards"
PAPERS_YML = ROOT / "data" / "papers.yml"

# Load paper URL lookup
papers = yaml.safe_load(open(PAPERS_YML, encoding="utf-8")) or []
def paper_url(p):
    urls = p.get("urls") or {}
    source = p.get("source") or {}
    return (urls.get("paper") or urls.get("pdf") or urls.get("project")
        or (f"https://doi.org/{source.get('doi')}" if source.get("doi") else "")
        or (f"https://arxiv.org/abs/{source.get('arxiv_id')}" if source.get("arxiv_id") else "")
        or source.get("openalex_id") or "")
url_by_title = {}
for p in papers:
    t = p.get("title","")
    if t:
        u = paper_url(p)
        if u: url_by_title.setdefault(t, u)

def md_escape(v):
    if v is None: return ""
    return str(v).replace("|","\\|")
def md_link(label, url):
    label = md_escape(label)
    if url: return f"[{label}]({url})"
    return label

# Load CSV
with open(CSV, encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
print(f"loaded {len(rows)} rows")

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

# Group by dataset + protocol
from collections import defaultdict
groups = defaultdict(list)
for r in rows:
    groups[(r["dataset"], r["protocol"])].append(r)

# Write per-dataset pages
for ds in sorted(set(r["dataset"] for r in rows)):
    if not ds: continue
    slug = SLUG.get(ds, re.sub(r"[^a-z0-9]+","_",ds.lower()).strip("_"))
    path = OUT / f"{slug}.md"
    # Get protocols for this dataset
    protocols = sorted(set(r["protocol"] for r in rows if r["dataset"] == ds))
    lines = [f"# {ds}", "", f"Leaderboard for {ds}. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.", "", ""]
    for proto in protocols:
        group = [r for r in rows if r["dataset"] == ds and r["protocol"] == proto]
        # Sort by sort_value desc
        def sv(r):
            try: return float(r.get("sort_value","0") or 0)
            except: return 0
        group.sort(key=sv, reverse=True)
        lines += [f"## {proto}", "", f"Rows: **{len(group)}**.", "",
                  "| Method / Training Setting | Paper | Source | Sort | Verified | Notes |",
                  "|---|---|---|---:|---|---|"]
        for r in group:
            method = md_escape(r.get("method",""))
            ts = r.get("training_setting","")
            if ts: method += f"<br><sub>{md_escape(ts)}</sub>"
            paper_link = md_link(r.get("paper",""), url_by_title.get(r.get("paper",""),""))
            # Show all metrics from metrics_json
            import json as J
            try: metrics = J.loads(r.get("metrics_json","{}"))
            except: metrics = {}
            metric_strs = []
            for k in ["R@1","R@5","R@10","AP","Recall@1","Recall@1%","mAP","Mean Drone→Satellite R@1","Mean Satellite→Drone R@1"]:
                if k in metrics: metric_strs.append(f"{md_escape(k)}={md_escape(metrics[k])}")
            # Use sort_value as the primary sort display
            sm = r.get("sort_metric","")
            sv_val = r.get("sort_value","")
            sort_disp = f"{md_escape(sm)}={md_escape(sv_val)}" if sm else ""
            cells = [method, paper_link, md_escape(r.get("source","")), sort_disp, md_escape(r.get("verified","")), md_escape(r.get("notes","") or "-")]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {path.name} ({len([r for r in rows if r['dataset']==ds])} rows)")

# Summary
by_ds = defaultdict(int)
for r in rows: by_ds[r["dataset"]] += 1
summary = ["# Leaderboards", "",
    f"Per-dataset leaderboard pages regenerated from `data/leaderboards.csv` ({len(rows)} rows). Each paper name links to its external page (arXiv, DOI, or OpenAlex).",
    "", "| Dataset | Page | Rows |", "|---|---|---:|"]
for ds in sorted(by_ds.keys()):
    if not ds: continue
    slug = SLUG.get(ds, re.sub(r"[^a-z0-9]+","_",ds.lower()).strip("_"))
    summary.append(f"| {md_escape(ds)} | [{slug}.md]({slug}.md) | {by_ds[ds]} |")
summary.append("")
(OUT / "leaderboard_summary.md").write_text("\n".join(summary), encoding="utf-8")
print(f"  wrote leaderboard_summary.md")
