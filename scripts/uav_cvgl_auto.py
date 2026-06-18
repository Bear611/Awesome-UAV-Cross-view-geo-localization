#!/usr/bin/env python3
"""
UAV-CVGL automation pipeline v0.3

Modes:
1) backfill: high-recall historical search by keywords + citation expansion.
2) weekly: high-precision recent paper search.
3) classify: one paper at a time, DeepSeek for coarse classification, MiniMax for summary.
4) migrate-existing: convert existing paper markdown tables to the new public format.
5) merge: merge parsed candidates into data/papers.yml and rebuild paper pages.
6) build-weekly: build weekly_updates/YYYY-Wxx.md from data/weekly_candidates.yml.

Important design choices:
- Search APIs do the searching; LLMs do not search the web.
- Each paper is processed independently.
- Non-relevant papers call DeepSeek once only.
- Relevant papers call DeepSeek once + MiniMax once.
- Results are written after every paper, so the process is resumable.
- No API keys are stored in files. Use env vars or GitHub Secrets.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
import yaml
from rapidfuzz import fuzz

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TIMEOUT = 40

CATEGORY_TO_FILE = {
    "retrieval": "papers/retrieval.md",
    "fine_pose_localization": "papers/fine_pose_localization.md",
    "unified_global_to_local": "papers/unified_global_to_local.md",
    "navigation_aided": "papers/navigation_aided.md",
}

CATEGORY_NAMES = {
    "retrieval": "Retrieval-based UAV CVGL",
    "fine_pose_localization": "Fine Pose Localization / Local Matching",
    "unified_global_to_local": "Unified Global-to-Local UAV Visual Localization",
    "navigation_aided": "Navigation-aided / Sensor-fusion UAV Geo-localization",
}


def log(msg: str) -> None:
    now = dt.datetime.now().strftime("%H:%M:%S")
    print(f"[uav-cvgl {now}] {msg}", flush=True)


def read_yaml(path: str | Path, default: Any = None) -> Any:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return default if data is None else data


def write_yaml(path: str | Path, data: Any) -> None:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)


def read_text(path: str | Path, default: str = "") -> str:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return default
    return p.read_text(encoding="utf-8")


def write_text(path: str | Path, text: str) -> None:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def norm_title(title: str) -> str:
    t = (title or "").lower().strip()
    t = re.sub(r"\[[^\]]+\]", " ", t)
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def stable_id(title: str, year: Optional[int] = None) -> str:
    raw = f"{norm_title(title)}::{year or ''}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def md_escape(text: Any) -> str:
    s = "" if text is None else str(text)
    return s.replace("|", "\\|").replace("\n", "<br>")


def md_link(title: str, url: Optional[str]) -> str:
    title = md_escape(title)
    if url:
        return f"[{title}]({url})"
    return title


def strip_md_link(text: str) -> Tuple[str, Optional[str]]:
    m = re.match(r"\s*\[([^\]]+)\]\(([^)]+)\)\s*", text or "")
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return (text or "").strip(), None


def split_md_row(line: str) -> List[str]:
    """Basic Markdown table row split. Assumes no unescaped pipes inside cells."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_sep_row(cells: List[str]) -> bool:
    return all(re.match(r"^:?-{3,}:?$", c.strip()) for c in cells)


def load_keywords(mode: str) -> List[str]:
    cfg = read_yaml("configs/keywords.yml", {})
    key = "weekly_keywords" if mode == "weekly" else "backfill_keywords"
    return list(cfg.get(key, []))


def semantic_headers() -> Dict[str, str]:
    key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    return {"x-api-key": key} if key else {}


def request_json(url: str, *, params: Optional[dict] = None, headers: Optional[dict] = None, method: str = "GET", json_body: Any = None, retries: int = 3) -> Any:
    for attempt in range(1, retries + 1):
        try:
            if method == "GET":
                r = requests.get(url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT)
            else:
                r = requests.post(url, params=params, headers=headers, json=json_body, timeout=DEFAULT_TIMEOUT)
            if r.status_code == 429 and attempt < retries:
                wait = 5 * attempt
                log(f"rate limited: sleeping {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt >= retries:
                raise
            wait = 3 * attempt
            log(f"request failed ({e}); retry in {wait}s")
            time.sleep(wait)
    return None


def paper_from_semantic(item: dict, found_by: dict) -> dict:
    external = item.get("externalIds") or {}
    url = item.get("url") or None
    if external.get("ArXiv"):
        url = f"https://arxiv.org/abs/{external['ArXiv']}"
    elif external.get("DOI"):
        url = f"https://doi.org/{external['DOI']}"
    authors = [a.get("name") for a in (item.get("authors") or []) if a.get("name")]
    return {
        "id": stable_id(item.get("title", ""), item.get("year")),
        "title": item.get("title") or "",
        "year": item.get("year"),
        "venue": item.get("venue") or "",
        "authors": authors,
        "abstract": item.get("abstract") or "",
        "urls": {
            "paper": url,
            "pdf": ((item.get("openAccessPdf") or {}).get("url")) or "",
            "code": "",
            "project": "",
        },
        "source": {
            "semantic_scholar_id": item.get("paperId") or "",
            "doi": external.get("DOI") or "",
            "arxiv_id": external.get("ArXiv") or "",
            "openalex_id": "",
        },
        "discovery": {
            "found_date": dt.date.today().isoformat(),
            "found_by": [found_by],
        },
        "status": "raw",
        "verified": False,
    }


def search_semantic_keyword(query: str, limit: int) -> List[dict]:
    log(f"Semantic Scholar keyword search: {query}")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    fields = "title,abstract,year,venue,url,externalIds,authors,publicationDate,citationCount,isOpenAccess,openAccessPdf"
    params = {"query": query, "limit": min(limit, 100), "fields": fields}
    data = request_json(url, params=params, headers=semantic_headers())
    items = data.get("data", []) if isinstance(data, dict) else []
    return [paper_from_semantic(x, {"source": "semantic_scholar", "keyword": query}) for x in items]


def find_semantic_paper_id_by_title(title: str) -> Optional[str]:
    try:
        res = search_semantic_keyword(title, 5)
    except Exception:
        return None
    target = norm_title(title)
    best_id, best_score = None, 0
    for r in res:
        score = fuzz.ratio(target, norm_title(r.get("title", "")))
        if score > best_score:
            best_score = score
            best_id = (r.get("source") or {}).get("semantic_scholar_id")
    return best_id if best_score >= 75 else None


def search_semantic_citations(seed: dict, limit: int) -> List[dict]:
    paper_id = (seed.get("semantic_scholar_id") or "").strip()
    if not paper_id:
        paper_id = find_semantic_paper_id_by_title(seed.get("title", "")) or ""
    if not paper_id:
        log(f"citation search skipped, no paper id: {seed.get('dataset')}")
        return []

    log(f"Semantic Scholar citation search: {seed.get('dataset')} ({paper_id})")
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    fields = "citingPaper.title,citingPaper.abstract,citingPaper.year,citingPaper.venue,citingPaper.url,citingPaper.externalIds,citingPaper.authors,citingPaper.openAccessPdf"
    params = {"limit": min(limit, 1000), "fields": fields}
    data = request_json(url, params=params, headers=semantic_headers())
    rows = data.get("data", []) if isinstance(data, dict) else []
    out = []
    for row in rows:
        p = row.get("citingPaper") or {}
        if not p.get("title"):
            continue
        out.append(paper_from_semantic(p, {"source": "semantic_scholar", "citation_of": seed.get("dataset"), "seed_title": seed.get("title")}))
    return out


def search_openalex_keyword(query: str, limit: int, *, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    log(f"OpenAlex keyword search: {query}")
    url = "https://api.openalex.org/works"
    filters = []
    if start_date:
        filters.append(f"from_publication_date:{start_date}")
    if end_date:
        filters.append(f"to_publication_date:{end_date}")
    params = {"search": query, "per-page": min(limit, 200), "sort": "publication_date:desc"}
    if filters:
        params["filter"] = ",".join(filters)
    try:
        data = request_json(url, params=params)
    except Exception as e:
        log(f"OpenAlex failed: {e}")
        return []
    out = []
    for item in data.get("results", []) if isinstance(data, dict) else []:
        title = item.get("title") or ""
        if not title:
            continue
        doi = item.get("doi") or ""
        urlp = doi or item.get("id") or ""
        authors = []
        for au in item.get("authorships") or []:
            name = ((au.get("author") or {}).get("display_name"))
            if name:
                authors.append(name)
        abstract = inverted_index_to_text(item.get("abstract_inverted_index"))
        out.append({
            "id": stable_id(title, item.get("publication_year")),
            "title": title,
            "year": item.get("publication_year"),
            "venue": ((item.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
            "authors": authors,
            "abstract": abstract,
            "urls": {"paper": urlp, "pdf": "", "code": "", "project": ""},
            "source": {"semantic_scholar_id": "", "doi": doi.replace("https://doi.org/", ""), "arxiv_id": "", "openalex_id": item.get("id") or ""},
            "discovery": {"found_date": dt.date.today().isoformat(), "found_by": [{"source": "openalex", "keyword": query}]},
            "status": "raw",
            "verified": False,
        })
    return out


def inverted_index_to_text(idx: Optional[dict]) -> str:
    if not idx:
        return ""
    pairs = []
    for word, positions in idx.items():
        for pos in positions:
            pairs.append((pos, word))
    return " ".join(w for _, w in sorted(pairs))


def search_arxiv_keyword(query: str, limit: int, *, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    log(f"arXiv keyword search: {query}")
    # arXiv API query syntax is limited; use all:query and filter locally by date when available.
    base = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": min(limit, 100),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        r = requests.get(base, params=params, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
    except Exception as e:
        log(f"arXiv failed: {e}")
        return []
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    try:
        root = ET.fromstring(r.text)
    except Exception:
        return []
    out = []
    start_d = dt.date.fromisoformat(start_date) if start_date else None
    end_d = dt.date.fromisoformat(end_date) if end_date else None
    for entry in root.findall("atom:entry", ns):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())
        published = entry.findtext("atom:published", default="", namespaces=ns) or ""
        pub_date = None
        if published[:10]:
            try:
                pub_date = dt.date.fromisoformat(published[:10])
            except ValueError:
                pass
        if start_d and pub_date and pub_date < start_d:
            continue
        if end_d and pub_date and pub_date > end_d:
            continue
        arxiv_url = entry.findtext("atom:id", default="", namespaces=ns) or ""
        arxiv_id = arxiv_url.rsplit("/", 1)[-1]
        authors = [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)]
        out.append({
            "id": stable_id(title, pub_date.year if pub_date else None),
            "title": title,
            "year": pub_date.year if pub_date else None,
            "venue": "arXiv",
            "authors": [a for a in authors if a],
            "abstract": summary,
            "urls": {"paper": arxiv_url, "pdf": arxiv_url.replace("/abs/", "/pdf/") if "/abs/" in arxiv_url else "", "code": "", "project": ""},
            "source": {"semantic_scholar_id": "", "doi": "", "arxiv_id": arxiv_id, "openalex_id": ""},
            "discovery": {"found_date": dt.date.today().isoformat(), "found_by": [{"source": "arxiv", "keyword": query}]},
            "status": "raw",
            "verified": False,
        })
    return out


def deduplicate(records: List[dict]) -> List[dict]:
    by_key: Dict[str, dict] = {}
    titles: List[Tuple[str, str]] = []  # normalized title, key

    def get_keys(r: dict) -> List[str]:
        source = r.get("source") or {}
        keys = []
        for name in ["doi", "arxiv_id", "semantic_scholar_id", "openalex_id"]:
            val = str(source.get(name) or "").strip().lower()
            if val:
                keys.append(f"{name}:{val}")
        return keys

    for r in records:
        title_norm = norm_title(r.get("title", ""))
        if not title_norm:
            continue
        keys = get_keys(r)
        chosen = None
        for k in keys:
            if k in by_key:
                chosen = k
                break
        if not chosen:
            # Fuzzy title dedup.
            for t, k in titles:
                if fuzz.ratio(title_norm, t) >= 96:
                    chosen = k
                    break
        if not chosen:
            chosen = keys[0] if keys else f"title:{title_norm}"
            by_key[chosen] = r
            titles.append((title_norm, chosen))
            continue

        old = by_key[chosen]
        old_fb = ((old.get("discovery") or {}).get("found_by") or [])
        new_fb = ((r.get("discovery") or {}).get("found_by") or [])
        old.setdefault("discovery", {})["found_by"] = old_fb + new_fb

        # Fill missing metadata.
        for field in ["abstract", "venue", "year"]:
            if not old.get(field) and r.get(field):
                old[field] = r[field]
        for group in ["urls", "source"]:
            old.setdefault(group, {})
            for k, v in (r.get(group) or {}).items():
                if not old[group].get(k) and v:
                    old[group][k] = v

    out = list(by_key.values())
    out.sort(key=lambda x: (x.get("year") or 0, x.get("title") or ""), reverse=True)
    return out


def merge_existing_candidates(path: str, new_records: List[dict]) -> List[dict]:
    existing = read_yaml(path, []) or []
    return deduplicate(existing + new_records)


def deepseek_classify(paper: dict) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    abstract = (paper.get("abstract") or "")[:6000]
    benchmarks = read_yaml("configs/benchmarks.yml", {}).get("benchmarks", [])
    system = (
        "You are a strict curator for an Awesome UAV Cross-View Geo-Localization repository. "
        "Classify one paper at a time. Output valid JSON only. "
        "Do not guess datasets or metrics. If unsure, use empty lists and set needs_review=true."
    )
    user = f"""
Paper title: {paper.get('title', '')}
Year: {paper.get('year', '')}
Venue: {paper.get('venue', '')}
Known benchmark names: {', '.join(benchmarks)}

Abstract:
{abstract}

Decide whether this is a UAV cross-view geo-localization paper.
Valid main_category values:
- retrieval
- fine_pose_localization
- unified_global_to_local
- navigation_aided
- unrelated

Return JSON with exactly these keys:
{{
  "is_cvgl": boolean,
  "is_uav_related": boolean,
  "main_category": string,
  "relevance_score": number between 0 and 1,
  "tags": array of short strings,
  "datasets": array of benchmark names,
  "possible_leaderboard": boolean,
  "reason": string,
  "needs_review": boolean
}}
""".strip()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "max_tokens": 900,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = request_json("https://api.deepseek.com/chat/completions", method="POST", headers=headers, json_body=payload)
    content = data["choices"][0]["message"]["content"]
    obj = parse_json_object(content)
    if obj.get("main_category") not in set(CATEGORY_TO_FILE) | {"unrelated"}:
        obj["main_category"] = "unrelated"
    obj["relevance_score"] = float(obj.get("relevance_score") or 0)
    return obj


def minimax_summary(paper: dict, use_pdf: bool = False) -> dict:
    api_key = os.getenv("MINIMAX_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY is not set")
    model = os.getenv("MINIMAX_MODEL", "MiniMax-M3")
    base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1").rstrip("/")
    abstract = (paper.get("abstract") or "")[:5000]
    cls = paper.get("classification") or {}
    pdf_text = ""
    if use_pdf:
        pdf_text = fetch_pdf_text_placeholder(paper)[:9000]

    system = (
        "You write concise Chinese summaries for an Awesome UAV Cross-View Geo-Localization repository. "
        "Process one paper only. Output JSON only. Do not invent experimental results."
    )
    user = f"""
Paper title: {paper.get('title', '')}
Year: {paper.get('year', '')}
Venue: {paper.get('venue', '')}
Category from DeepSeek: {cls.get('main_category', '')}
Datasets from DeepSeek: {cls.get('datasets', [])}
Tags from DeepSeek: {cls.get('tags', [])}

Abstract:
{abstract}

Optional PDF text:
{pdf_text}

Write a 200-280 Chinese character summary for the column "研究内容". It should cover:
1. 论文研究的问题；
2. 提出的主要模块/方法；
3. 使用的数据集或 benchmark；
4. 实验效果, but only if the text clearly states it. Do not fabricate numbers.

Return JSON with exactly these keys:
{{
  "summary_cn": string,
  "benchmarks": array of benchmark names,
  "main_modules": array of strings,
  "reported_results": array of strings,
  "code_url": string or null,
  "needs_review": boolean
}}
""".strip()
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "max_tokens": 1200,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = request_json(f"{base_url}/chat/completions", method="POST", headers=headers, json_body=payload)
    content = data["choices"][0]["message"]["content"]
    obj = parse_json_object(content)
    obj.setdefault("summary_cn", "")
    obj.setdefault("benchmarks", cls.get("datasets", []))
    obj.setdefault("main_modules", [])
    obj.setdefault("reported_results", [])
    obj.setdefault("code_url", None)
    obj.setdefault("needs_review", True)
    return obj


def fetch_pdf_text_placeholder(paper: dict) -> str:
    """Placeholder for future PDF extraction.

    Keeping this empty by default prevents accidental large-context calls.
    Add PyMuPDF/Marker/GROBID later if you need PDF-level extraction.
    """
    return ""


def parse_json_object(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        raise ValueError("empty model response")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Remove fenced block if any.
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S)
    if m:
        return json.loads(m.group(1))
    # Fallback: first {...last}.
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError(f"cannot parse JSON: {text[:200]}")


def cmd_backfill(args: argparse.Namespace) -> None:
    all_records: List[dict] = []
    keywords = load_keywords("backfill")
    start_date = f"{args.start_year}-01-01" if args.start_year else None
    end_date = f"{args.end_year}-12-31" if args.end_year else None

    for q in keywords:
        all_records += search_semantic_keyword(q, args.limit_per_query)
        all_records += search_openalex_keyword(q, args.limit_per_query, start_date=start_date, end_date=end_date)
        all_records += search_arxiv_keyword(q, args.limit_per_query, start_date=start_date, end_date=end_date)
        time.sleep(args.sleep)

    seeds = read_yaml("configs/seed_datasets.yml", {}).get("seeds", [])
    for seed in seeds:
        all_records += search_semantic_citations(seed, args.citation_limit)
        time.sleep(args.sleep)

    merged = merge_existing_candidates(args.output, all_records)
    write_yaml(args.output, merged)
    log(f"backfill wrote {len(merged)} candidates to {args.output}")


def cmd_weekly(args: argparse.Namespace) -> None:
    end = dt.date.today()
    start = end - dt.timedelta(days=args.days)
    all_records: List[dict] = []
    for q in load_keywords("weekly"):
        all_records += search_semantic_keyword(q, args.limit_per_query)
        all_records += search_openalex_keyword(q, args.limit_per_query, start_date=start.isoformat(), end_date=end.isoformat())
        all_records += search_arxiv_keyword(q, args.limit_per_query, start_date=start.isoformat(), end_date=end.isoformat())
        time.sleep(args.sleep)

    # Keep only recent where a date is known; if date unknown, keep but let DeepSeek decide.
    merged = merge_existing_candidates(args.output, all_records)
    write_yaml(args.output, merged)
    log(f"weekly wrote {len(merged)} candidates to {args.output}")


def cmd_classify(args: argparse.Namespace) -> None:
    records = read_yaml(args.input, []) or []
    threshold = {"backfill": 0.60, "weekly": 0.75, "migrate": 0.0}[args.mode]
    total = len(records)
    limit = args.limit if args.limit and args.limit > 0 else total
    output_path = args.output or args.input

    processed = deepseek_calls = minimax_calls = parsed = rejected = errors = 0

    for i, r in enumerate(records):
        if i >= limit:
            break
        title = r.get("title") or "Untitled"
        log(f"[{i + 1}/{total}] Processing: {title[:120]}")
        try:
            if args.force_classification or not r.get("classification"):
                log(f"[{i + 1}/{total}] DeepSeek classify")
                r["classification"] = deepseek_classify(r)
                deepseek_calls += 1
            else:
                log(f"[{i + 1}/{total}] DeepSeek skipped: cached classification exists")

            cls = r.get("classification") or {}
            score = float(cls.get("relevance_score") or 0)
            ok = bool(cls.get("is_cvgl")) and bool(cls.get("is_uav_related")) and score >= threshold
            if ok:
                r["status"] = "parsed"
                parsed += 1
                if not args.skip_minimax:
                    if args.force_summary or not r.get("summary"):
                        log(f"[{i + 1}/{total}] MiniMax summary")
                        r["summary"] = minimax_summary(r, args.use_pdf)
                        minimax_calls += 1
                    else:
                        log(f"[{i + 1}/{total}] MiniMax skipped: cached summary exists")
            else:
                r["status"] = "rejected"
                rejected += 1
                log(f"[{i + 1}/{total}] Rejected by DeepSeek, score={score:.2f}")

            r["verified"] = False
            r.pop("error", None)
        except Exception as e:
            r["status"] = "error"
            r["error"] = str(e)
            errors += 1
            log(f"[{i + 1}/{total}] Failed: {e}")

        processed += 1
        write_yaml(output_path, records)
        log(
            f"Progress: processed={processed}/{min(limit, total)}, parsed={parsed}, rejected={rejected}, "
            f"errors={errors}, deepseek_calls={deepseek_calls}, minimax_calls={minimax_calls}"
        )
        time.sleep(args.sleep)

    write_yaml(output_path, records)
    log(
        f"Done. processed={processed}, parsed={parsed}, rejected={rejected}, errors={errors}, "
        f"deepseek_calls={deepseek_calls}, minimax_calls={minimax_calls}"
    )


def cmd_migrate_existing(args: argparse.Namespace) -> None:
    paper_files = list(CATEGORY_TO_FILE.values())
    all_records: List[dict] = []
    internal_reasons: List[dict] = []

    for rel in paper_files:
        p = ROOT / rel
        if not p.exists():
            continue
        category = file_to_category(rel)
        log(f"migrating {rel}")
        text = p.read_text(encoding="utf-8")
        records, reasons = parse_existing_paper_markdown(text, category, resolve_links=args.resolve_links)
        all_records.extend(records)
        internal_reasons.extend(reasons)

    all_records = deduplicate(all_records)
    write_yaml("data/papers.yml", all_records)
    write_yaml("data/internal/classification_reasons.yml", internal_reasons)
    build_paper_pages(all_records)
    log(f"migrated {len(all_records)} papers into data/papers.yml and rebuilt paper pages")


def file_to_category(rel: str) -> str:
    for cat, path in CATEGORY_TO_FILE.items():
        if path == rel:
            return cat
    return "retrieval"


def parse_existing_paper_markdown(text: str, category: str, *, resolve_links: bool = False) -> Tuple[List[dict], List[dict]]:
    rows: List[dict] = []
    reasons: List[dict] = []
    lines = text.splitlines()
    in_table = False
    header: List[str] = []
    for line in lines:
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = split_md_row(line)
        if not cells:
            continue
        if any("论文" in c for c in cells):
            header = cells
            in_table = True
            continue
        if in_table and is_sep_row(cells):
            continue
        if not in_table:
            continue
        # Expected old format:
        # 论文 | 分类原因 | 基于 abstract 优化的研究内容 | 数据/benchmark 介绍
        if len(cells) < 3:
            continue
        title_cell = cells[0]
        title, existing_url = strip_md_link(title_cell)
        if not title or title in {"论文", "Paper"}:
            continue
        reason = cells[1] if len(cells) >= 4 else ""
        content = cells[2] if len(cells) >= 4 else (cells[1] if len(cells) >= 2 else "")
        benchmark = cells[3] if len(cells) >= 4 else ""
        url = existing_url
        if resolve_links and not url:
            url = resolve_paper_link(title)
        record = {
            "id": stable_id(title),
            "title": title,
            "year": None,
            "venue": "",
            "authors": [],
            "abstract": "",
            "urls": {"paper": url or "", "pdf": "", "code": "", "project": ""},
            "source": {"semantic_scholar_id": "", "doi": "", "arxiv_id": "", "openalex_id": ""},
            "classification": {
                "is_cvgl": True,
                "is_uav_related": True,
                "main_category": category,
                "relevance_score": 1.0,
                "tags": [],
                "datasets": extract_benchmarks_from_text(benchmark),
                "possible_leaderboard": False,
                "reason": "migrated from existing local markdown",
                "needs_review": True,
            },
            "summary": {
                "summary_cn": clean_cell(content),
                "benchmarks": extract_benchmarks_from_text(benchmark),
                "main_modules": [],
                "reported_results": [],
                "code_url": None,
                "needs_review": True,
            },
            "status": "parsed",
            "verified": False,
        }
        rows.append(record)
        reasons.append({"title": title, "category": category, "reason": clean_cell(reason)})
    return rows, reasons


def clean_cell(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "；", s or "", flags=re.I)
    s = s.replace("\\|", "|").strip()
    return s


def extract_benchmarks_from_text(text: str) -> List[str]:
    cfg = read_yaml("configs/benchmarks.yml", {})
    names = cfg.get("benchmarks", []) or []
    aliases = cfg.get("aliases", {}) or {}
    found = []
    hay = text or ""
    for name in names:
        candidates = [name] + list((aliases.get(name) or []))
        if any(c.lower() in hay.lower() for c in candidates):
            found.append(name)
    return sorted(set(found))


def resolve_paper_link(title: str) -> Optional[str]:
    try:
        items = search_semantic_keyword(title, 3)
    except Exception:
        return f"https://www.semanticscholar.org/search?q={urllib.parse.quote(title)}"
    target = norm_title(title)
    best_url, best_score = None, 0
    for item in items:
        score = fuzz.ratio(target, norm_title(item.get("title", "")))
        if score > best_score:
            best_score = score
            best_url = (item.get("urls") or {}).get("paper")
    if best_url and best_score >= 75:
        return best_url
    return f"https://www.semanticscholar.org/search?q={urllib.parse.quote(title)}"


def build_paper_pages(records: List[dict]) -> None:
    grouped: Dict[str, List[dict]] = {k: [] for k in CATEGORY_TO_FILE}
    for r in records:
        cat = ((r.get("classification") or {}).get("main_category")) or "retrieval"
        if cat not in grouped:
            cat = "retrieval"
        grouped[cat].append(r)

    for cat, rows in grouped.items():
        rows.sort(key=lambda x: ((x.get("year") or 0), x.get("title") or ""), reverse=True)
        title = CATEGORY_NAMES[cat]
        md = [f"# {title}", ""]
        if cat == "navigation_aided":
            md.append("> This is a related category. General UAV navigation/SLAM papers are included only when they are directly connected to visual geo-localization or cross-view map association.")
            md.append("")
        md.append("| 论文 | 研究内容 | 数据/benchmark | Code |")
        md.append("|---|---|---|---|")
        for r in rows:
            summ = r.get("summary") or {}
            cls = r.get("classification") or {}
            benchmarks = summ.get("benchmarks") or cls.get("datasets") or []
            if isinstance(benchmarks, str):
                benchmarks = [benchmarks]
            code = summ.get("code_url") or (r.get("urls") or {}).get("code") or ""
            code_cell = f"[Code]({code})" if code else "-"
            paper_cell = md_link(r.get("title", "Untitled"), (r.get("urls") or {}).get("paper"))
            md.append(
                f"| {paper_cell} | {md_escape(summ.get('summary_cn') or '')} | {md_escape(', '.join(benchmarks) if benchmarks else '-')} | {code_cell} |"
            )
        md.append("")
        write_text(CATEGORY_TO_FILE[cat], "\n".join(md))


def cmd_merge(args: argparse.Namespace) -> None:
    candidates = read_yaml(args.candidates, []) or []
    existing = read_yaml("data/papers.yml", []) or []
    to_merge = []
    for r in candidates:
        if r.get("status") != "parsed":
            continue
        if args.require_verified and not r.get("verified"):
            continue
        to_merge.append(r)
    merged = deduplicate(existing + to_merge)
    write_yaml("data/papers.yml", merged)
    build_paper_pages(merged)
    log(f"merged {len(to_merge)} parsed candidates; data/papers.yml now has {len(merged)} papers")


def cmd_build_weekly(args: argparse.Namespace) -> None:
    records = read_yaml(args.input, []) or []
    today = dt.date.today()
    iso = today.isocalendar()
    week_name = args.output or f"weekly_updates/{iso.year}-W{iso.week:02d}.md"
    rows = [r for r in records if r.get("status") in {"parsed", "error"}]
    md = [f"# Weekly UAV-CVGL Update: {iso.year}-W{iso.week:02d}", ""]
    md.append("This file is generated by the automated weekly search pipeline. All entries are unverified until manually reviewed.")
    md.append("")
    md.append("| Paper | Category | Dataset / Benchmark | Research Summary | Status |")
    md.append("|---|---|---|---|---|")
    for r in rows:
        cls = r.get("classification") or {}
        summ = r.get("summary") or {}
        cat = cls.get("main_category") or "unclassified"
        benchmarks = summ.get("benchmarks") or cls.get("datasets") or []
        if isinstance(benchmarks, str):
            benchmarks = [benchmarks]
        status = r.get("status") or "raw"
        paper_cell = md_link(r.get("title", "Untitled"), (r.get("urls") or {}).get("paper"))
        md.append(
            f"| {paper_cell} | {md_escape(cat)} | {md_escape(', '.join(benchmarks) if benchmarks else '-')} | {md_escape(summ.get('summary_cn') or cls.get('reason') or '')} | {md_escape(status)} |"
        )
    md.append("")
    write_text(week_name, "\n".join(md))
    log(f"wrote weekly update to {week_name}")


def cmd_stats(args: argparse.Namespace) -> None:
    records = read_yaml(args.input, []) or []
    total = len(records)
    status_counts: Dict[str, int] = {}
    cats: Dict[str, int] = {}
    deepseek = 0
    minimax = 0
    for r in records:
        status_counts[r.get("status", "raw")] = status_counts.get(r.get("status", "raw"), 0) + 1
        if r.get("classification"):
            deepseek += 1
            cat = (r.get("classification") or {}).get("main_category", "unknown")
            cats[cat] = cats.get(cat, 0) + 1
        if r.get("summary"):
            minimax += 1
    print(json.dumps({"total": total, "status": status_counts, "categories": cats, "deepseek_done": deepseek, "minimax_done": minimax}, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UAV-CVGL automation pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("backfill", help="large-scale historical search")
    p.add_argument("--start-year", type=int, default=2016)
    p.add_argument("--end-year", type=int, default=dt.date.today().year)
    p.add_argument("--limit-per-query", type=int, default=30)
    p.add_argument("--citation-limit", type=int, default=300)
    p.add_argument("--output", default="data/backfill_candidates.yml")
    p.add_argument("--sleep", type=float, default=0.5)
    p.set_defaults(func=cmd_backfill)

    p = sub.add_parser("weekly", help="weekly recent search")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--limit-per-query", type=int, default=15)
    p.add_argument("--output", default="data/weekly_candidates.yml")
    p.add_argument("--sleep", type=float, default=0.5)
    p.set_defaults(func=cmd_weekly)

    p = sub.add_parser("classify", help="DeepSeek classify, MiniMax summarize")
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="")
    p.add_argument("--mode", choices=["backfill", "weekly", "migrate"], default="weekly")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--skip-minimax", action="store_true")
    p.add_argument("--use-pdf", action="store_true")
    p.add_argument("--force-classification", action="store_true")
    p.add_argument("--force-summary", action="store_true")
    p.add_argument("--sleep", type=float, default=0.2)
    p.set_defaults(func=cmd_classify)

    p = sub.add_parser("migrate-existing", help="convert existing paper md tables to new format")
    p.add_argument("--resolve-links", action="store_true")
    p.set_defaults(func=cmd_migrate_existing)

    p = sub.add_parser("merge", help="merge parsed candidates into data/papers.yml and rebuild paper pages")
    p.add_argument("--candidates", required=True)
    p.add_argument("--require-verified", action="store_true")
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("build-weekly", help="build weekly markdown from weekly candidates")
    p.add_argument("--input", default="data/weekly_candidates.yml")
    p.add_argument("--output", default="")
    p.set_defaults(func=cmd_build_weekly)

    p = sub.add_parser("stats", help="show candidate processing stats")
    p.add_argument("--input", required=True)
    p.set_defaults(func=cmd_stats)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    os.chdir(ROOT)
    args.func(args)


if __name__ == "__main__":
    main()
