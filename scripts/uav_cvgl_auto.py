#!/usr/bin/env python3
"""
UAV-CVGL automation pipeline v0.4

Modes:
1) backfill: high-recall historical search by keywords + citation expansion.
2) weekly: high-precision recent paper search.
3) backfill now uses OpenAlex for citation expansion; arXiv is keyword-only.
3) classify: one paper at a time, DeepSeek for coarse classification, MiniMax for summary.
4) migrate-existing: convert existing paper markdown tables to the new public format.
5) merge: merge parsed candidates into data/papers.yml and rebuild paper pages.
6) build-weekly: build weekly_updates/YYYY-Wxx.md from data/weekly_candidates.yml.

Important design choices:
- Search APIs and public web evidence fetches do the searching; LLMs judge relevance and dataset openness from gathered evidence.
- Each paper is processed independently.
- Non-relevant papers call DeepSeek once only.
- Relevant papers call DeepSeek once + MiniMax once.
- Results are written after every paper, so the process is resumable.
- No API keys are stored in files. Use env vars or GitHub Secrets.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html as html_lib
import hashlib
from io import BytesIO
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
    "survey": "papers/survey.md",
}

CATEGORY_NAMES = {
    "retrieval": "Retrieval-based UAV CVGL",
    "fine_pose_localization": "Fine Pose Localization / Local Matching",
    "unified_global_to_local": "Unified Global-to-Local UAV Visual Localization",
    "navigation_aided": "Navigation-aided / Sensor-fusion UAV Geo-localization",
    "survey": "Survey Papers",
}


def log(msg: str) -> None:
    now = dt.datetime.now().strftime("%H:%M:%S")
    print(f"[uav-cvgl {now}] {msg}", flush=True)


def log_section(title: str) -> None:
    line = "=" * 78
    log(line)
    log(title)
    log(line)


def log_step(current: int, total: int, title: str) -> None:
    log(f"[{current}/{total}] {title}")


def openalex_params(extra: Optional[dict] = None) -> dict:
    params = dict(extra or {})
    mailto = os.getenv("OPENALEX_MAILTO", "").strip()
    if mailto:
        params["mailto"] = mailto
    return params


def env_value(name: str, default: str) -> str:
    """Return a stripped environment value without letting an empty Actions var erase a default."""
    return os.getenv(name, "").strip() or default


def _normalized_secret_name(name: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(name).upper())


def parse_api_bundle(raw: str) -> Dict[str, str]:
    """Extract supported API keys from one combined secret without logging its contents."""
    text = (raw or "").strip()
    if not text:
        return {}

    scalar_values: Dict[str, str] = {}
    try:
        loaded = yaml.safe_load(text)
    except yaml.YAMLError:
        loaded = None

    if isinstance(loaded, dict):
        for key, value in loaded.items():
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    if isinstance(nested_value, (str, int, float)):
                        scalar_values[f"{key}_{nested_key}"] = str(nested_value).strip()
            elif isinstance(value, (str, int, float)):
                scalar_values[str(key)] = str(value).strip()

    if not scalar_values:
        for line in re.split(r"[\r\n;]+", text):
            match = re.match(
                r"^\s*(?:export\s+)?([A-Za-z][A-Za-z0-9_-]*)\s*(?:=|:)\s*(.*?)\s*$",
                line,
            )
            if not match:
                continue
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1].strip()
            scalar_values[match.group(1)] = value

    aliases = {
        "DS": "DEEPSEEK_API_KEY",
        "DSKEY": "DEEPSEEK_API_KEY",
        "DSAPIKEY": "DEEPSEEK_API_KEY",
        "DEEPSEEK": "DEEPSEEK_API_KEY",
        "DEEPSEEKKEY": "DEEPSEEK_API_KEY",
        "DEEPSEEKTOKEN": "DEEPSEEK_API_KEY",
        "DEEPSEEKAPIKEY": "DEEPSEEK_API_KEY",
        "MINIMAX": "MINIMAX_API_KEY",
        "MINIMAXKEY": "MINIMAX_API_KEY",
        "MINIMAXTOKEN": "MINIMAX_API_KEY",
        "MINIMAXAPIKEY": "MINIMAX_API_KEY",
    }
    result: Dict[str, str] = {}
    for key, value in scalar_values.items():
        target = aliases.get(_normalized_secret_name(key))
        if target and value:
            result[target] = value

    # Also accept compact provider-labelled text on one line, including JSON-like
    # or comma/Chinese-punctuation separated forms. API tokens themselves do not
    # contain whitespace, commas, semicolons, quotes, or closing braces.
    provider_patterns = {
        "DEEPSEEK_API_KEY": (
            r"(?i)(?:^|[\s,;；{])['\"]?(?:deep\s*seek|ds)['\"]?"
            r"\s*(?:[_ -]*api)?\s*(?:[_ -]*(?:key|token))?"
            r"\s*[:=：]\s*['\"]?([^'\"\s,;；}\]]+)"
        ),
        "MINIMAX_API_KEY": (
            r"(?i)(?:^|[\s,;；{])['\"]?mini\s*max['\"]?"
            r"\s*(?:[_ -]*api)?\s*(?:[_ -]*(?:key|token))?"
            r"\s*[:=：]\s*['\"]?([^'\"\s,;；}\]]+)"
        ),
    }
    for target, pattern in provider_patterns.items():
        match = re.search(pattern, text)
        if match and match.group(1).strip():
            result[target] = match.group(1).strip()
    return result


def api_secret_value(name: str) -> str:
    """Prefer a dedicated env var, then fall back to the combined API secret."""
    direct = os.getenv(name, "").strip()
    if direct:
        return direct
    bundle = os.getenv("API_BUNDLE", "").strip() or os.getenv("API", "").strip()
    return parse_api_bundle(bundle).get(name, "")


def normalize_deepseek_api_key(api_key: str) -> str:
    key = (api_key or "").strip()
    if key.lower().startswith("ds:"):
        return key.split(":", 1)[1].strip()
    return key


def minimax_base_url_candidates(base_url: str) -> List[str]:
    primary = (base_url or "https://api.minimaxi.com/v1").rstrip("/")
    candidates = [primary]
    if "api.minimax.io" in primary:
        candidates.append("https://api.minimaxi.com/v1")
    return list(dict.fromkeys(candidates))


def minimax_chat_completion(base_url: str, headers: Dict[str, str], payload: dict) -> dict:
    data = None
    last_error: Optional[Exception] = None
    timeout = float(os.getenv("MINIMAX_REQUEST_TIMEOUT", "180"))
    retries = int(os.getenv("MINIMAX_REQUEST_RETRIES", "3"))
    for candidate_base_url in minimax_base_url_candidates(base_url):
        try:
            data = request_json(
                f"{candidate_base_url}/chat/completions",
                method="POST",
                headers=headers,
                json_body=payload,
                retries=retries,
                timeout=timeout,
            )
            break
        except requests.exceptions.HTTPError as e:
            last_error = e
            status_code = e.response.status_code if e.response is not None else None
            if status_code in {401, 403} and "api.minimax.io" in candidate_base_url:
                log("MiniMax authentication failed on api.minimax.io; retrying api.minimaxi.com")
                continue
            raise
    if data is None:
        if last_error:
            raise last_error
        raise RuntimeError("MiniMax request failed without a response")
    return data


def compact_count_table(counts: Dict[str, int]) -> str:
    if not counts:
        return "-"
    return ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))


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
    tmp = p.with_name(f"{p.name}.tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)
    os.replace(tmp, p)


def read_text(path: str | Path, default: str = "") -> str:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return default
    return p.read_text(encoding="utf-8")


def write_text(path: str | Path, text: str) -> None:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(f"{p.name}.tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


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


def parse_iso_date(value: Any) -> Optional[dt.date]:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return dt.date.fromisoformat(text[:10])
    except ValueError:
        return None


def record_publication_date(record: dict) -> Optional[dt.date]:
    value = parse_iso_date(record.get("publication_date"))
    if value:
        return value
    discovery = record.get("discovery") or {}
    return parse_iso_date(discovery.get("publication_date"))


def filter_records_by_date(
    records: List[dict],
    start_date: Optional[str],
    end_date: Optional[str],
) -> List[dict]:
    """Filter known publication dates while retaining records whose exact date is unavailable."""
    start = parse_iso_date(start_date)
    end = parse_iso_date(end_date)
    out: List[dict] = []
    for record in records:
        published = record_publication_date(record)
        if published and start and published < start:
            continue
        if published and end and published > end:
            continue
        if not published:
            try:
                year = int(record.get("year"))
            except (TypeError, ValueError):
                year = None
            if year is not None and start and year < start.year:
                continue
            if year is not None and end and year > end.year:
                continue
        out.append(record)
    return out


def request_json(url: str, *, params: Optional[dict] = None, headers: Optional[dict] = None, method: str = "GET", json_body: Any = None, retries: int = 3, timeout: Optional[float] = None) -> Any:
    request_timeout = DEFAULT_TIMEOUT if timeout is None else timeout
    for attempt in range(1, retries + 1):
        try:
            if method == "GET":
                r = requests.get(url, params=params, headers=headers, timeout=request_timeout)
            else:
                r = requests.post(url, params=params, headers=headers, json=json_body, timeout=request_timeout)
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


def is_rate_limit_error(exc: Exception) -> bool:
    status_code = getattr(getattr(exc, "response", None), "status_code", None)
    return status_code == 429 or bool(re.search(r"(?:\b429\b|rate[ -]?limit)", str(exc), flags=re.I))


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
        "publication_date": item.get("publicationDate") or "",
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


def search_semantic_keyword(
    query: str,
    limit: int,
    *,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[dict]:
    log(f"Semantic Scholar keyword search: {query}")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    fields = "title,abstract,year,venue,url,externalIds,authors,publicationDate,citationCount,isOpenAccess,openAccessPdf"
    params = {"query": query, "limit": min(limit, 100), "fields": fields}
    data = request_json(url, params=params, headers=semantic_headers())
    items = data.get("data", []) if isinstance(data, dict) else []
    records = [paper_from_semantic(x, {"source": "semantic_scholar", "keyword": query}) for x in items]
    return filter_records_by_date(records, start_date, end_date)


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
    params = openalex_params({"search": query, "per-page": min(limit, 200), "sort": "publication_date:desc"})
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
            "publication_date": item.get("publication_date") or "",
            "urls": {"paper": urlp, "pdf": "", "code": "", "project": ""},
            "source": {"semantic_scholar_id": "", "doi": doi.replace("https://doi.org/", ""), "arxiv_id": "", "openalex_id": item.get("id") or ""},
            "discovery": {"found_date": dt.date.today().isoformat(), "found_by": [{"source": "openalex", "keyword": query}]},
            "status": "raw",
            "verified": False,
        })
    return out



def openalex_short_id(openalex_id: str) -> str:
    val = (openalex_id or "").strip()
    if not val:
        return ""
    return val.rstrip("/").rsplit("/", 1)[-1]


def paper_from_openalex_item(item: dict, found_by: dict) -> dict:
    title = item.get("title") or ""
    doi = item.get("doi") or ""
    urlp = doi or item.get("id") or ""
    authors = []
    for au in item.get("authorships") or []:
        name = ((au.get("author") or {}).get("display_name"))
        if name:
            authors.append(name)
    abstract = inverted_index_to_text(item.get("abstract_inverted_index"))
    return {
        "id": stable_id(title, item.get("publication_year")),
        "title": title,
        "year": item.get("publication_year"),
        "venue": ((item.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
        "authors": authors,
        "abstract": abstract,
        "publication_date": item.get("publication_date") or "",
        "urls": {"paper": urlp, "pdf": "", "code": "", "project": ""},
        "source": {
            "semantic_scholar_id": "",
            "doi": doi.replace("https://doi.org/", ""),
            "arxiv_id": "",
            "openalex_id": item.get("id") or "",
        },
        "discovery": {"found_date": dt.date.today().isoformat(), "found_by": [found_by]},
        "status": "raw",
        "verified": False,
    }


def find_openalex_work_id_by_seed(seed: dict) -> Optional[str]:
    # OpenAlex citation expansion needs a Work ID. Prefer an explicit id, otherwise search by title.
    explicit = openalex_short_id(seed.get("openalex_id", ""))
    if explicit:
        return explicit

    title = seed.get("title", "")
    if not title:
        return None
    try:
        url = "https://api.openalex.org/works"
        params = openalex_params({"search": title, "per-page": 5})
        data = request_json(url, params=params)
        results = data.get("results", []) if isinstance(data, dict) else []
    except Exception as e:
        log(f"OpenAlex seed lookup failed for {seed.get('dataset')}: {e}")
        return None

    target = norm_title(title)
    best_id, best_score = None, 0
    for item in results:
        score = fuzz.ratio(target, norm_title(item.get("title", "")))
        if score > best_score:
            best_score = score
            best_id = openalex_short_id(item.get("id", ""))
    if best_id and best_score >= 72:
        return best_id
    return None


def search_openalex_citations(
    seed: dict,
    limit: int,
    *,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[dict]:
    dataset = seed.get("dataset") or seed.get("title") or "unknown seed"
    work_id = find_openalex_work_id_by_seed(seed)
    if not work_id:
        log(f"OpenAlex citation search skipped, no work id: {dataset}")
        return []

    log(f"OpenAlex citation search: {dataset} ({work_id})")
    out: List[dict] = []
    cursor = "*"
    per_page = min(200, max(1, limit))
    while len(out) < limit:
        filters = [f"cites:{work_id}"]
        if start_date:
            filters.append(f"from_publication_date:{start_date}")
        if end_date:
            filters.append(f"to_publication_date:{end_date}")
        params = openalex_params({
            "filter": ",".join(filters),
            "sort": "publication_date:desc",
            "per-page": min(per_page, limit - len(out)),
            "cursor": cursor,
        })
        try:
            data = request_json("https://api.openalex.org/works", params=params)
        except Exception as e:
            log(f"OpenAlex citation failed for {dataset}: {e}")
            break
        results = data.get("results", []) if isinstance(data, dict) else []
        for item in results:
            if item.get("title"):
                out.append(paper_from_openalex_item(item, {"source": "openalex", "citation_of": dataset, "seed_title": seed.get("title", "")}))
        cursor = ((data.get("meta") or {}).get("next_cursor")) if isinstance(data, dict) else None
        if not cursor or not results:
            break
        time.sleep(0.2)
    return out[:limit]

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
            "publication_date": pub_date.isoformat() if pub_date else "",
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
        old_discovery = old.setdefault("discovery", {})
        new_discovery = r.get("discovery") or {}
        old_fb = (old_discovery.get("found_by") or [])
        new_fb = ((r.get("discovery") or {}).get("found_by") or [])
        combined_found_by: List[dict] = []
        seen_found_by: set[str] = set()
        for item in old_fb + new_fb:
            marker = json.dumps(item, ensure_ascii=False, sort_keys=True)
            if marker not in seen_found_by:
                seen_found_by.add(marker)
                combined_found_by.append(item)
        old_discovery["found_by"] = combined_found_by
        if not old_discovery.get("found_date") and new_discovery.get("found_date"):
            old_discovery["found_date"] = new_discovery["found_date"]
        if new_discovery.get("found_date"):
            old_discovery["last_seen_date"] = new_discovery["found_date"]

        # Fill missing metadata.
        for field in ["abstract", "venue", "year", "publication_date"]:
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
    api_key = normalize_deepseek_api_key(api_secret_value("DEEPSEEK_API_KEY"))
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set")
    model = env_value("DEEPSEEK_MODEL", "deepseek-chat")
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
- survey
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
        "max_tokens": 2000,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = request_json("https://api.deepseek.com/chat/completions", method="POST", headers=headers, json_body=payload)
    content = data["choices"][0]["message"].get("content") or ""
    if not content.strip() and model != "deepseek-chat":
        log(f"DeepSeek returned empty content for {model}; retrying deepseek-chat")
        payload["model"] = "deepseek-chat"
        payload["max_tokens"] = 1200
        data = request_json("https://api.deepseek.com/chat/completions", method="POST", headers=headers, json_body=payload)
        content = data["choices"][0]["message"].get("content") or ""
    obj = parse_json_object(content)
    if obj.get("main_category") not in set(CATEGORY_TO_FILE) | {"unrelated"}:
        obj["main_category"] = "unrelated"
    obj["relevance_score"] = float(obj.get("relevance_score") or 0)
    return obj


def minimax_summary(paper: dict, use_pdf: bool = False) -> dict:
    api_key = api_secret_value("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError("MINIMAX_API_KEY is not set")
    model = env_value("MINIMAX_MODEL", "MiniMax-M3")
    if model != "MiniMax-M3":
        raise RuntimeError(f"MINIMAX_MODEL must be MiniMax-M3 for this pipeline, got {model!r}")
    base_url = env_value("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1").rstrip("/")
    abstract = (paper.get("abstract") or "")[:5000]
    cls = paper.get("classification") or {}
    known_benchmarks = read_yaml("configs/benchmarks.yml", {}).get("benchmarks", []) or []
    old_summary = ((paper.get("summary") or {}).get("summary_en") or (paper.get("summary") or {}).get("summary_cn") or "")[:2000]
    pdf_text = ""
    if use_pdf:
        pdf_text = fetch_pdf_text_placeholder(paper)[:120000]

    system = (
        "You write concise English summaries for an Awesome UAV Cross-View Geo-Localization repository. "
        "Read the provided abstract and available full-paper text. Confirm or refine the paper category. "
        "Process one paper only. Output JSON only. Do not include hidden thinking, Markdown, or prose outside JSON. "
        "Do not invent experimental results, datasets, or leaderboard values."
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

Existing local note, if any:
{old_summary}

Optional full-paper text and table evidence:
{pdf_text}

Confirm the category using the abstract and full-paper text when available.
Valid main_category values:
- retrieval
- fine_pose_localization
- unified_global_to_local
- navigation_aided
- survey
- unrelated

Write a 190-230 word English introduction for the table column "Research content". It should cover:
1. the research problem;
2. the main modules or technical design;
3. the datasets or benchmarks used;
4. experimental effects only when clearly stated. Do not fabricate numbers.

Also extract leaderboard-ready metrics from explicit result tables or table-like evidence only.
Return an empty leaderboard_metrics array when dataset, metric, value, or method is uncertain.
All extracted leaderboard rows must be marked unverified for later manual checking.
Known leaderboard datasets already tracked by this repository:
{', '.join(known_benchmarks)}

Leaderboard inclusion rules:
- Include only results for datasets already tracked above, or for a new dataset that the paper clearly states is public/open-source with a download/repository/project page.
- Include only the paper's flagship/main method results on the main benchmark protocol.
- Do not include ablation studies, module variants, backbone-only variants, prompt variants, weather/corruption subsets, altitude-only variants, synthetic stress tests, re-ranking/TTA variants unless that is the official main protocol, or auxiliary non-UAV datasets.
- If the table reports several splits of the same official benchmark, use only the canonical aggregate/overall row when present. If no aggregate is present, keep the official split rows only when the split is part of the dataset's standard leaderboard protocol.
- If you are not sure whether a value belongs to the flagship model on an accepted dataset/protocol, omit it and explain in table_evidence_notes.

Return JSON with exactly these keys:
{{
  "summary_en": string,
  "main_category": string,
  "category_confirmed": boolean,
  "classification_reason": string,
  "benchmarks": array of benchmark names,
  "main_modules": array of strings,
  "reported_results": array of strings,
  "leaderboard_metrics": array of objects with keys dataset, task, split, metric, method, value, source, official_or_reproduced, verified, notes,
  "table_evidence_notes": string,
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
        "max_tokens": 4096,
        "thinking": {"type": "disabled"},
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = minimax_chat_completion(base_url, headers, payload)
    content = data["choices"][0]["message"]["content"]
    try:
        obj = parse_json_object(content)
    except ValueError:
        log("MiniMax returned non-JSON content; retrying with strict JSON-only prompt")
        strict_payload = dict(payload)
        strict_payload["temperature"] = 0.0
        strict_payload["max_tokens"] = 4096
        strict_payload["messages"] = [
            {
                "role": "system",
                "content": (
                    "Return exactly one valid JSON object and nothing else. "
                    "Do not include <think>, analysis, Markdown fences, explanations, or any prose outside JSON."
                ),
            },
            {"role": "user", "content": user + "\n\nReturn only the JSON object now."},
        ]
        data = minimax_chat_completion(base_url, headers, strict_payload)
        content = data["choices"][0]["message"]["content"]
        obj = parse_json_object(content)
    obj.setdefault("summary_en", "")
    obj.setdefault("main_category", cls.get("main_category", "unrelated"))
    obj.setdefault("category_confirmed", obj.get("main_category") == cls.get("main_category"))
    obj.setdefault("classification_reason", "")
    obj.setdefault("benchmarks", cls.get("datasets", []))
    obj.setdefault("main_modules", [])
    obj.setdefault("reported_results", [])
    obj.setdefault("leaderboard_metrics", [])
    obj.setdefault("table_evidence_notes", "")
    obj["leaderboard_metrics"] = filter_leaderboard_metrics(obj.get("leaderboard_metrics") or [], known_benchmarks, paper)
    obj.setdefault("code_url", None)
    obj.setdefault("needs_review", True)
    return obj


def filter_leaderboard_metrics(metrics: List[dict], known_benchmarks: List[str], paper: Optional[dict] = None) -> List[dict]:
    known = {str(x).lower().replace("-", "").replace("_", "").replace(" ", "") for x in known_benchmarks}
    banned = [
        "ablation",
        "variant",
        "w/o",
        "without",
        "weather",
        "corruption",
        "fog",
        "snow",
        "rain",
        "dark",
        "night",
        "altitude-only",
        "prompt",
        "tta",
        "re-ranking",
        "reranking",
        "backbone",
    ]
    out: List[dict] = []
    for row in metrics:
        if not isinstance(row, dict):
            continue
        dataset = str(row.get("dataset") or "").strip()
        metric = str(row.get("metric") or "").strip()
        method = str(row.get("method") or "").strip()
        value = str(row.get("value") or "").strip()
        variant_text = " ".join(str(row.get(k) or "") for k in ["task", "split", "method", "source", "notes"]).lower()
        if not (dataset and metric and method and value):
            continue
        dataset_key = dataset.lower().replace("-", "").replace("_", "").replace(" ", "")
        is_known_dataset = dataset_key in known
        if not is_known_dataset and not verify_new_dataset_open_source(dataset, paper or {}):
            continue
        if any(term in variant_text for term in banned):
            continue
        row["verified"] = False
        row.setdefault("official_or_reproduced", "unverified")
        out.append(row)
    return out



def dataset_web_search_candidates(dataset: str, paper: dict) -> List[str]:
    """Return lightweight public search/result pages for dataset openness evidence."""
    title = str(paper.get("title") or "")[:120]
    queries = [
        f'"{dataset}" dataset download UAV',
        f'"{dataset}" benchmark dataset github',
        f'"{dataset}" "data" "download"',
    ]
    if title:
        queries.append(f'"{dataset}" "{title}" dataset')
    urls: List[str] = []
    for q in queries:
        urls.append("https://duckduckgo.com/html/?q=" + urllib.parse.quote_plus(q))
    urls.extend(
        [
            "https://github.com/search?q=" + urllib.parse.quote_plus(f'{dataset} dataset') + "&type=repositories",
            "https://huggingface.co/datasets?search=" + urllib.parse.quote_plus(dataset),
            "https://paperswithcode.com/search?q=" + urllib.parse.quote_plus(dataset),
            "https://zenodo.org/search?q=" + urllib.parse.quote_plus(dataset),
        ]
    )
    return urls


def search_result_links(html_text: str, limit: int = 5) -> List[str]:
    links: List[str] = []
    for raw in re.findall(r'href=["\']([^"\']+)["\']', html_text, flags=re.I):
        url = html_lib.unescape(raw)
        if "uddg=" in url:
            parsed = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed.query)
            if params.get("uddg"):
                url = params["uddg"][0]
        if url.startswith("/") or not re.match(r"^https?://", url, flags=re.I):
            continue
        host = urllib.parse.urlparse(url).netloc.lower()
        if any(blocked in host for blocked in ["duckduckgo.com", "google.com", "bing.com"]):
            continue
        key = url.lower().split("#", 1)[0]
        if key not in {u.lower().split("#", 1)[0] for u in links}:
            links.append(url)
        if len(links) >= limit:
            break
    return links
def collect_dataset_open_source_evidence(dataset: str, paper: dict) -> str:
    urls = paper.get("urls") or {}
    source = paper.get("source") or {}
    candidates: List[str] = []
    for key in ["project", "code", "paper", "pdf"]:
        add_url_candidate(candidates, urls.get(key) or "")
    for search_url in dataset_web_search_candidates(dataset, paper):
        add_url_candidate(candidates, search_url)
    doi = (source.get("doi") or "").strip()
    if doi:
        add_url_candidate(candidates, doi)
    evidence_parts: List[str] = []
    idx = 0
    while idx < len(candidates) and len(evidence_parts) < 10:
        url = candidates[idx]
        idx += 1
        try:
            current_url, content_type, content = fetch_limited_url(url, 500000, accept="text/html,application/json,text/plain,*/*;q=0.8")
        except Exception as e:
            evidence_parts.append(f"URL: {url}\nFetch error: {e}")
            continue
        text = ""
        if "html" in (content_type or "").lower() or b"<html" in content[:1000].lower():
            html_text = content.decode("utf-8", errors="ignore")
            text = extract_article_text_from_html(html_text, 6000)
            if not text:
                text = re.sub(r"(?is)<[^>]+>", " ", html_text)
                text = html_lib.unescape(re.sub(r"\s+", " ", text)).strip()[:6000]
        else:
            text = content.decode("utf-8", errors="ignore")[:6000]
        if text:
            evidence_parts.append(f"URL: {current_url}\n{text[:6000]}")
        if "duckduckgo.com/html" in current_url:
            html_text = content.decode("utf-8", errors="ignore")
            for result_url in search_result_links(html_text, limit=3):
                add_url_candidate(candidates, result_url)
    return "\n\n---\n\n".join(evidence_parts)[:18000]


def verify_new_dataset_open_source(dataset: str, paper: dict) -> bool:
    cache = paper.setdefault("dataset_open_source_checks", {})
    if dataset in cache:
        return bool((cache.get(dataset) or {}).get("is_open_source"))
    evidence = collect_dataset_open_source_evidence(dataset, paper)
    if not evidence:
        cache[dataset] = {"is_open_source": False, "reason": "No public evidence page was accessible from the paper metadata."}
        return False

    api_key = normalize_deepseek_api_key(api_secret_value("DEEPSEEK_API_KEY"))
    if not api_key:
        cache[dataset] = {"is_open_source": False, "reason": "DEEPSEEK_API_KEY is not set for dataset openness verification."}
        return False
    system = (
        "You verify dataset openness for a UAV-CVGL leaderboard. "
        "Use only the provided evidence snippets. Output valid JSON only."
    )
    user = f"""
Dataset name: {dataset}
Paper title: {paper.get('title', '')}

Evidence snippets from paper/project/code/DOI pages:
{evidence}

Decide whether the dataset itself is publicly available/open-source with clear download, repository, data page, or access instructions.
Do not infer openness from a paper merely saying a benchmark exists.

Return JSON:
{{
  "is_open_source": boolean,
  "evidence_url": string or null,
  "reason": string
}}
""".strip()
    payload = {
        "model": env_value("DEEPSEEK_MODEL", "deepseek-chat"),
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "max_tokens": 800,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        data = request_json("https://api.deepseek.com/chat/completions", method="POST", headers=headers, json_body=payload)
        obj = parse_json_object(data["choices"][0]["message"].get("content") or "")
    except Exception as e:
        obj = {"is_open_source": False, "reason": f"DeepSeek openness verification failed: {e}", "evidence_url": None}
    cache[dataset] = obj
    log(f"Dataset openness check: {dataset} -> {bool(obj.get('is_open_source'))} ({str(obj.get('reason') or '')[:120]})")
    return bool(obj.get("is_open_source"))

def pdf_url_for_paper(paper: dict) -> str:
    urls = paper.get("urls") or {}
    pdf_url = (urls.get("pdf") or "").strip()
    if pdf_url:
        return pdf_url
    arxiv_id = ((paper.get("source") or {}).get("arxiv_id") or "").strip()
    if arxiv_id:
        return f"https://arxiv.org/pdf/{arxiv_id}"
    paper_url = (urls.get("paper") or "").strip()
    if "arxiv.org/abs/" in paper_url:
        return paper_url.replace("/abs/", "/pdf/")
    return ""


def add_url_candidate(candidates: List[str], url: str) -> None:
    url = (url or "").strip()
    if not url:
        return
    if url.startswith("doi:"):
        url = f"https://doi.org/{url[4:]}"
    if url.startswith("10."):
        url = f"https://doi.org/{url}"
    if url.startswith("//"):
        url = f"https:{url}"
    if not re.match(r"^https?://", url, flags=re.I):
        return
    url = url.replace(" ", "%20")
    key = url.lower()
    if key not in {u.lower() for u in candidates}:
        candidates.append(url)


def openalex_pdf_candidates(openalex_id: str) -> List[str]:
    work_id = openalex_short_id(openalex_id)
    if not work_id:
        return []
    try:
        item = request_json(f"https://api.openalex.org/works/{work_id}", params=openalex_params({}), retries=1)
    except Exception as e:
        log(f"OpenAlex PDF metadata lookup skipped for {work_id}: {e}")
        return []

    candidates: List[str] = []
    for location in [item.get("primary_location") or {}] + (item.get("locations") or []):
        add_url_candidate(candidates, location.get("pdf_url") or "")
        add_url_candidate(candidates, location.get("landing_page_url") or "")
    for location in item.get("best_oa_location") and [item.get("best_oa_location")] or []:
        add_url_candidate(candidates, location.get("pdf_url") or "")
        add_url_candidate(candidates, location.get("landing_page_url") or "")
    return candidates


def openalex_pdf_candidates_by_doi(doi: str) -> List[str]:
    doi = (doi or "").strip().replace("https://doi.org/", "")
    if not doi:
        return []
    try:
        data = request_json(
            "https://api.openalex.org/works",
            params=openalex_params({"filter": f"doi:{doi}", "per-page": 1}),
            retries=1,
        )
    except Exception as e:
        log(f"OpenAlex DOI PDF metadata lookup skipped for {doi}: {e}")
        return []
    results = data.get("results") or []
    if not results:
        return []
    candidates: List[str] = []
    item = results[0]
    for location in [item.get("primary_location") or {}] + (item.get("locations") or []):
        add_url_candidate(candidates, location.get("pdf_url") or "")
        add_url_candidate(candidates, location.get("landing_page_url") or "")
    if item.get("best_oa_location"):
        add_url_candidate(candidates, item["best_oa_location"].get("pdf_url") or "")
        add_url_candidate(candidates, item["best_oa_location"].get("landing_page_url") or "")
    return candidates


def pdf_candidate_urls_for_paper(paper: dict) -> List[str]:
    candidates: List[str] = []
    urls = paper.get("urls") or {}
    source = paper.get("source") or {}

    add_url_candidate(candidates, urls.get("pdf") or "")
    add_url_candidate(candidates, pdf_url_for_paper(paper))
    add_url_candidate(candidates, urls.get("paper") or "")
    add_url_candidate(candidates, urls.get("project") or "")

    arxiv_id = (source.get("arxiv_id") or "").strip()
    if arxiv_id:
        add_url_candidate(candidates, f"https://arxiv.org/pdf/{arxiv_id}")

    doi = (source.get("doi") or paper.get("doi") or "").strip()
    if doi:
        add_url_candidate(candidates, doi)
        candidates.extend(openalex_pdf_candidates_by_doi(doi))

    candidates.extend(openalex_pdf_candidates(source.get("openalex_id") or ""))
    return list(dict.fromkeys(candidates))


def response_looks_like_pdf(url: str, content_type: str, content: bytes) -> bool:
    head = content[:1000].lower().lstrip()
    if head.startswith(b"<!doctype html") or head.startswith(b"<html") or "text/html" in (content_type or "").lower():
        return content.startswith(b"%PDF")
    return (
        content.startswith(b"%PDF")
        or "application/pdf" in (content_type or "").lower()
        or likely_pdf_url(url)
    )


def likely_pdf_url(url: str) -> bool:
    return re.search(
        r"(\.pdf(?:[?#]|$)|/pdf(?:[/?#]|$)|arxiv\.org/pdf/|stamp\.jsp|Dokument\.php)",
        url or "",
        flags=re.I,
    ) is not None


def local_pdf_candidates_for_paper(paper: dict) -> List[Path]:
    cache_dir = Path(os.getenv("UAV_CVGL_PDF_CACHE_DIR", str(ROOT / "data" / "pdf_cache")))
    source = paper.get("source") or {}
    names = [
        paper.get("id") or "",
        stable_id(paper.get("title", ""), paper.get("year")),
        norm_title(paper.get("title", ""))[:120],
        (source.get("doi") or "").replace("/", "_").replace(":", "_"),
        (source.get("arxiv_id") or "").replace("/", "_"),
        openalex_short_id(source.get("openalex_id") or "").replace("/", "_"),
    ]
    paths: List[Path] = []
    for name in names:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip("_ "))
        if safe:
            paths.append(cache_dir / f"{safe}.pdf")
    return paths


def extract_pdf_text_from_bytes(content: bytes, title: str, char_limit: int, max_pages: int, source: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(BytesIO(content))
    chunks: List[str] = []
    for page in reader.pages[:max_pages]:
        chunks.append(page.extract_text() or "")
        if sum(len(c) for c in chunks) >= char_limit:
            break
    text = "\n".join(chunks)
    text = re.sub(r"\s+", " ", text).strip()
    if text:
        log(f"PDF text extracted for MiniMax: pages={min(len(reader.pages), max_pages)}, chars={min(len(text), char_limit)}, source={source}")
    return text[:char_limit]


def format_table_rows(rows: List[List[str]], max_rows: int = 40) -> str:
    clean_rows: List[List[str]] = []
    for row in rows[:max_rows]:
        clean = [re.sub(r"\s+", " ", str(cell or "")).strip() for cell in row]
        if any(clean):
            clean_rows.append(clean)
    if len(clean_rows) < 2:
        return ""
    width = max(len(row) for row in clean_rows)
    clean_rows = [row + [""] * (width - len(row)) for row in clean_rows]
    header = clean_rows[0]
    out = [
        "| " + " | ".join(md_escape(cell) for cell in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in clean_rows[1:]:
        out.append("| " + " | ".join(md_escape(cell) for cell in row) + " |")
    return "\n".join(out)


def extract_pdf_tables_from_bytes(content: bytes, max_pages: int, char_limit: int) -> str:
    try:
        import pdfplumber
    except Exception as e:
        log(f"PDF table extraction skipped; pdfplumber unavailable: {e}")
        return ""
    parts: List[str] = []
    try:
        with pdfplumber.open(BytesIO(content)) as pdf:
            for page_idx, page in enumerate(pdf.pages[:max_pages], 1):
                for table_idx, table in enumerate(page.extract_tables() or [], 1):
                    formatted = format_table_rows(table)
                    if not formatted:
                        continue
                    parts.append(f"[PDF table p{page_idx}.{table_idx}]\n{formatted}")
                    if sum(len(p) for p in parts) >= char_limit:
                        break
                if sum(len(p) for p in parts) >= char_limit:
                    break
    except Exception as e:
        log(f"PDF table extraction skipped: {e}")
        return ""
    text = "\n\n".join(parts).strip()
    if text:
        log(f"PDF tables extracted for MiniMax: tables={len(parts)}, chars={min(len(text), char_limit)}")
    return text[:char_limit]


def fetch_limited_url(url: str, max_bytes: int, *, accept: str) -> Tuple[str, str, bytes]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        ),
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
    }
    with requests.get(url, timeout=DEFAULT_TIMEOUT, headers=headers, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        chunks: List[bytes] = []
        total = 0
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(f"response exceeds byte limit {max_bytes}")
            chunks.append(chunk)
        return r.url, r.headers.get("Content-Type", ""), b"".join(chunks)


def extract_pdf_links_from_html(html_text: str, base_url: str) -> List[str]:
    links: List[str] = []
    patterns = [
        r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']',
        r'<link[^>]+type=["\']application/pdf["\'][^>]+href=["\']([^"\']+)["\']',
        r'<a[^>]+href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
        r'["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']',
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html_text, flags=re.I | re.S):
            add_url_candidate(links, urllib.parse.urljoin(base_url, match.group(1).replace("&amp;", "&")))
    ieee_ids = set(re.findall(r"(?:arnumber=|/document/|articleNumber[\"']?\s*[:=]\s*[\"']?)(\d{6,})", html_text + " " + base_url, flags=re.I))
    for arnumber in ieee_ids:
        add_url_candidate(links, f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={arnumber}")
    mdpi_match = re.match(r"(https://www\.mdpi\.com/[^?#]+)", base_url, flags=re.I)
    if mdpi_match and not mdpi_match.group(1).lower().endswith("/pdf"):
        add_url_candidate(links, mdpi_match.group(1).rstrip("/") + "/pdf")
    return links


def extract_article_text_from_html(html_text: str, char_limit: int) -> str:
    text = re.sub(r"(?is)<(script|style|noscript|svg|header|footer|nav|aside)[^>]*>.*?</\1>", " ", html_text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</(p|div|section|article|h[1-6]|li|tr)>", "\n", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = html_lib.unescape(text)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    drop = (
        "cookie",
        "privacy policy",
        "sign in",
        "institutional access",
        "subscribe",
        "advertisement",
        "javascript",
        "accept all",
    )
    kept = [line for line in lines if len(line) >= 40 and not any(term in line.lower() for term in drop)]
    text = "\n".join(kept)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    lower = text.lower()
    paper_markers = sum(marker in lower for marker in ["abstract", "introduction", "method", "experiment", "conclusion", "references"])
    if len(text) < 3000 or paper_markers < 2:
        return ""
    return text[:char_limit]


def extract_html_tables_from_html(html_text: str, char_limit: int) -> str:
    parts: List[str] = []
    for idx, table_html in enumerate(re.findall(r"(?is)<table[^>]*>.*?</table>", html_text), 1):
        rows: List[List[str]] = []
        for row_html in re.findall(r"(?is)<tr[^>]*>.*?</tr>", table_html):
            cells = re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", row_html)
            row: List[str] = []
            for cell in cells:
                cell = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", cell)
                cell = re.sub(r"(?is)<[^>]+>", " ", cell)
                row.append(html_lib.unescape(re.sub(r"\s+", " ", cell)).strip())
            if any(row):
                rows.append(row)
        formatted = format_table_rows(rows)
        if formatted:
            parts.append(f"[HTML table {idx}]\n{formatted}")
        if sum(len(p) for p in parts) >= char_limit:
            break
    text = "\n\n".join(parts).strip()
    if text:
        log(f"HTML tables extracted for MiniMax: tables={len(parts)}, chars={min(len(text), char_limit)}")
    return text[:char_limit]


def fetch_pdf_text_placeholder(paper: dict) -> str:
    """Fetch and extract paper PDF text when an accessible PDF URL is available."""
    candidate_urls = pdf_candidate_urls_for_paper(paper)
    if not candidate_urls:
        return ""
    char_limit = int(os.getenv("MINIMAX_PDF_CHAR_LIMIT", "120000"))
    table_char_limit = int(os.getenv("MINIMAX_TABLE_CHAR_LIMIT", "30000"))
    max_pages = int(os.getenv("MINIMAX_PDF_MAX_PAGES", "80"))
    max_bytes = int(os.getenv("MINIMAX_PDF_MAX_BYTES", str(100 * 1024 * 1024)))
    landing_max_bytes = int(os.getenv("MINIMAX_PDF_LANDING_MAX_BYTES", str(3 * 1024 * 1024)))
    max_candidates = int(os.getenv("MINIMAX_PDF_MAX_CANDIDATES", "16"))
    try:
        from pypdf import PdfReader
    except Exception as e:
        log(f"PDF extraction skipped; pypdf unavailable: {e}")
        return ""

    for local_path in local_pdf_candidates_for_paper(paper):
        if not local_path.exists():
            continue
        try:
            content = local_path.read_bytes()
            if len(content) > max_bytes:
                log(f"Local PDF skipped; file too large: {local_path}")
                continue
            text = extract_pdf_text_from_bytes(content, paper.get("title", "Untitled"), char_limit, max_pages, str(local_path))
            tables = extract_pdf_tables_from_bytes(content, max_pages, table_char_limit)
            if text:
                if tables:
                    text = text + "\n\nTABLE EVIDENCE:\n" + tables
                return text
        except Exception as e:
            log(f"Local PDF extraction skipped for {local_path}: {e}")

    seen: set[str] = set()
    queue = list(candidate_urls)
    errors: List[str] = []
    while queue and len(seen) < max_candidates:
        url = queue.pop(0)
        key = url.lower()
        if key in seen:
            continue
        seen.add(key)
        try:
            current_url, content_type, content = fetch_limited_url(
                url,
                max_bytes if likely_pdf_url(url) else landing_max_bytes,
                accept="application/pdf,text/html;q=0.9,*/*;q=0.8",
            )
            if response_looks_like_pdf(current_url, content_type, content):
                if len(content) > max_bytes:
                    log(f"PDF extraction skipped; file too large: {paper.get('title', 'Untitled')[:80]}")
                    continue
                text = extract_pdf_text_from_bytes(content, paper.get("title", "Untitled"), char_limit, max_pages, current_url)
                if text:
                    tables = extract_pdf_tables_from_bytes(content, max_pages, table_char_limit)
                    if tables:
                        text = text + "\n\nTABLE EVIDENCE:\n" + tables
                    return text
            elif "html" in (content_type or "").lower() or b"<html" in content[:1000].lower():
                html_text = content.decode("utf-8", errors="ignore")
                for link in extract_pdf_links_from_html(html_text, current_url):
                    if link.lower() not in seen:
                        queue.append(link)
                article_text = extract_article_text_from_html(html_text, char_limit)
                html_tables = extract_html_tables_from_html(html_text, table_char_limit)
                if article_text:
                    if html_tables:
                        article_text = article_text + "\n\nTABLE EVIDENCE:\n" + html_tables
                    log(f"HTML article text extracted for MiniMax: chars={len(article_text)}, source={current_url}")
                    return article_text
        except Exception as e:
            errors.append(f"{url}: {e}")
            continue
    if errors:
        log(f"PDF extraction skipped for {paper.get('title', 'Untitled')[:80]} after {len(seen)} candidates: {errors[-1]}")
    return ""


def parse_json_object(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        raise ValueError("empty model response")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    text_without_think = re.sub(r"<think>.*?</think>", "", text, flags=re.S | re.I).strip()
    if text_without_think and text_without_think != text:
        try:
            return json.loads(text_without_think)
        except json.JSONDecodeError:
            pass
        text = text_without_think
    # Remove fenced block if any.
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S)
    if m:
        return json.loads(m.group(1))
    # Fallback: first {...last}.
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError(f"cannot parse JSON: {text[:200]}")



def write_search_report(report: dict, path: str) -> None:
    json_path = str(path).replace(".md", ".json")
    write_text(json_path, json.dumps(report, ensure_ascii=False, indent=2))
    md = [
        f"# UAV-CVGL {str(report.get('mode') or 'search').title()} Search Report",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Summary",
        "",
        f"- Raw records: **{report.get('raw_records', 0)}**",
        f"- Deduplicated candidates: **{report.get('deduplicated_candidates', 0)}**",
        f"- Output: `{report.get('output')}`",
        "",
        "## Source Counts",
        "",
        "| Source | Count |",
        "|---|---:|",
    ]
    for k, v in sorted((report.get("search_stats") or {}).items()):
        md.append(f"| {k} | {v} |")
    md += [
        "", "## Detailed Search Steps", "",
        "| Phase | Source | Query / Seed | Count | Error |",
        "|---|---|---|---:|---|",
    ]
    for row in report.get("details", []):
        md.append(
            f"| {md_escape(row.get('phase'))} | {md_escape(row.get('source'))} | "
            f"{md_escape(row.get('query'))} | {row.get('count', 0)} | {md_escape(row.get('error') or '-')} |"
        )
    md.append("")
    write_text(path, "\n".join(md))


def classification_summary(records: List[dict]) -> Dict[str, int]:
    summary = {"algorithm_papers": 0, "survey_papers": 0, "unrelated_papers": 0, "error_papers": 0, "raw_papers": 0}
    for r in records:
        status = r.get("status", "raw")
        cls = r.get("classification") or {}
        cat = cls.get("main_category", "")
        if status == "error":
            summary["error_papers"] += 1
        elif status == "raw":
            summary["raw_papers"] += 1
        elif cat == "survey" and status == "parsed":
            summary["survey_papers"] += 1
        elif status == "parsed" and cat in {"retrieval", "fine_pose_localization", "unified_global_to_local", "navigation_aided"}:
            summary["algorithm_papers"] += 1
        elif status == "rejected" or cat == "unrelated":
            summary["unrelated_papers"] += 1
    return summary


def write_classification_report(records: List[dict], path: str) -> None:
    counts = classification_summary(records)
    cat_counts: Dict[str, int] = {}
    status_counts: Dict[str, int] = {}
    for r in records:
        status_counts[r.get("status", "raw")] = status_counts.get(r.get("status", "raw"), 0) + 1
        cat = (r.get("classification") or {}).get("main_category", "unclassified")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    report = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "classification_summary": counts,
        "category_counts": cat_counts,
        "status_counts": status_counts,
    }
    write_text(str(path).replace(".md", ".json"), json.dumps(report, ensure_ascii=False, indent=2))
    md = [
        "# UAV-CVGL Classification Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Main Summary",
        "",
        "| Bucket | Count |",
        "|---|---:|",
    ]
    for k, v in counts.items():
        md.append(f"| {k.replace('_', ' ').title()} | {v} |")
    md += ["", "## Category Counts", "", "| Category | Count |", "|---|---:|"]
    for k, v in sorted(cat_counts.items()):
        md.append(f"| {k} | {v} |")
    md += ["", "## Status Counts", "", "| Status | Count |", "|---|---:|"]
    for k, v in sorted(status_counts.items()):
        md.append(f"| {k} | {v} |")
    md.append("")
    write_text(path, "\n".join(md))

def candidate_needs_processing(
    record: dict,
    *,
    force_classification: bool = False,
    force_summary: bool = False,
    skip_minimax: bool = False,
) -> bool:
    if force_classification or force_summary:
        return True
    status = record.get("status")
    classification = record.get("classification") or {}
    summary = record.get("summary") or {}
    if status == "rejected" and classification:
        return False
    if status == "parsed" and classification and (skip_minimax or "leaderboard_metrics" in summary):
        return False
    return True


def weekly_digest_records(records: List[dict], target_date: dt.date) -> List[dict]:
    week_start = target_date - dt.timedelta(days=target_date.weekday())
    week_end = week_start + dt.timedelta(days=6)
    out: List[dict] = []
    for record in records:
        if record.get("status") not in {"parsed", "error"}:
            continue
        found = parse_iso_date((record.get("discovery") or {}).get("found_date"))
        if found and week_start <= found <= week_end:
            out.append(record)
    return out


def cmd_preflight(args: argparse.Namespace) -> None:
    missing = []
    if args.require_llm:
        if not normalize_deepseek_api_key(api_secret_value("DEEPSEEK_API_KEY")):
            missing.append("DEEPSEEK_API_KEY")
        if not api_secret_value("MINIMAX_API_KEY"):
            missing.append("MINIMAX_API_KEY")
    if missing:
        raise RuntimeError(f"Missing required GitHub Secrets: {', '.join(missing)}")
    minimax_model = env_value("MINIMAX_MODEL", "MiniMax-M3")
    if minimax_model != "MiniMax-M3":
        raise RuntimeError(f"MINIMAX_MODEL must be MiniMax-M3, got {minimax_model!r}")
    log(
        "preflight passed: required secrets are present; "
        f"DeepSeek model={env_value('DEEPSEEK_MODEL', 'deepseek-chat')}; MiniMax model={minimax_model}"
    )
    if not os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip():
        log("warning: SEMANTIC_SCHOLAR_API_KEY is not set; search will continue with public rate limits")


def cmd_backfill(args: argparse.Namespace) -> None:
    all_records: List[dict] = []
    search_stats: Dict[str, int] = {}
    detail_rows: List[dict] = []
    keywords = load_keywords("backfill")
    start_date = f"{args.start_year}-01-01" if args.start_year else None
    end_date = f"{args.end_year}-12-31" if args.end_year else None

    log_section("BACKFILL SEARCH START")
    log(f"Time range: {start_date or 'open'} to {end_date or 'open'}")
    log(f"Keyword limit per source: {args.limit_per_query}; citation limit per seed: {args.citation_limit}")

    log_section("PHASE 1/2: KEYWORD SEARCH")
    for idx, q in enumerate(keywords, 1):
        log_step(idx, len(keywords), f"Keyword search: {q}")
        before = len(all_records)
        for source_name, fn in [
            ("semantic_scholar", lambda: search_semantic_keyword(q, args.limit_per_query)),
            ("openalex", lambda: search_openalex_keyword(q, args.limit_per_query, start_date=start_date, end_date=end_date)),
            ("arxiv", lambda: search_arxiv_keyword(q, args.limit_per_query, start_date=start_date, end_date=end_date)),
        ]:
            try:
                rows = fn()
            except Exception as e:
                log(f"{source_name} keyword search failed for {q}: {e}")
                rows = []
            all_records += rows
            search_stats[f"keyword:{source_name}"] = search_stats.get(f"keyword:{source_name}", 0) + len(rows)
            detail_rows.append({"phase": "keyword", "source": source_name, "query": q, "count": len(rows)})
            log(f"  {source_name}: {len(rows)} papers")
            time.sleep(args.sleep)
        log(f"  keyword total added: {len(all_records) - before}")

    seeds = read_yaml("configs/seed_datasets.yml", {}).get("seeds", [])
    log_section("PHASE 2/2: OPENALEX CITATION EXPANSION")
    for idx, seed in enumerate(seeds, 1):
        dataset = seed.get("dataset", "unknown")
        log_step(idx, len(seeds), f"Citation search for benchmark seed: {dataset}")
        try:
            rows = search_openalex_citations(
                seed,
                args.citation_limit,
                start_date=start_date,
                end_date=end_date,
            )
        except Exception as e:
            log(f"OpenAlex citation search failed for {dataset}: {e}")
            rows = []
        all_records += rows
        search_stats["citation:openalex"] = search_stats.get("citation:openalex", 0) + len(rows)
        detail_rows.append({"phase": "citation", "source": "openalex", "query": dataset, "count": len(rows)})
        log(f"  OpenAlex citations for {dataset}: {len(rows)} papers")
        time.sleep(args.sleep)

    raw_total = len(all_records)
    merged = merge_existing_candidates(args.output, all_records)
    write_yaml(args.output, merged)
    report = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": "backfill",
        "start_year": args.start_year,
        "end_year": args.end_year,
        "raw_records": raw_total,
        "deduplicated_candidates": len(merged),
        "search_stats": search_stats,
        "details": detail_rows,
        "output": args.output,
    }
    write_search_report(report, args.report)
    log_section("BACKFILL SEARCH SUMMARY")
    log(f"Raw records: {raw_total}")
    log(f"Deduplicated candidates: {len(merged)}")
    log(f"Source counts: {compact_count_table(search_stats)}")
    log(f"Candidate file: {args.output}")
    log(f"Search report: {args.report}")

def cmd_weekly(args: argparse.Namespace) -> None:
    end = dt.date.today()
    start = end - dt.timedelta(days=max(args.days - 1, 0))
    all_records: List[dict] = []
    search_stats: Dict[str, int] = {}
    detail_rows: List[dict] = []
    successful_calls = 0
    failed_calls = 0
    disabled_sources = set()
    keywords = load_keywords("weekly")
    log_section("WEEKLY SEARCH START")
    log(f"Publication window: {start.isoformat()} to {end.isoformat()}")
    for index, q in enumerate(keywords, 1):
        log_step(index, len(keywords), f"Keyword search: {q}")
        for source_name, fn in [
            (
                "semantic_scholar",
                lambda: search_semantic_keyword(
                    q,
                    args.limit_per_query,
                    start_date=start.isoformat(),
                    end_date=end.isoformat(),
                ),
            ),
            (
                "openalex",
                lambda: search_openalex_keyword(
                    q,
                    args.limit_per_query,
                    start_date=start.isoformat(),
                    end_date=end.isoformat(),
                ),
            ),
            (
                "arxiv",
                lambda: search_arxiv_keyword(
                    q,
                    args.limit_per_query,
                    start_date=start.isoformat(),
                    end_date=end.isoformat(),
                ),
            ),
        ]:
            if source_name in disabled_sources:
                error = "skipped after an earlier rate-limit failure in this run"
                rows = []
                search_stats.setdefault(source_name, 0)
                detail_rows.append(
                    {"phase": "weekly", "source": source_name, "query": q, "count": 0, "error": error}
                )
                continue
            error = ""
            try:
                rows = fn()
                successful_calls += 1
            except Exception as exc:
                error = str(exc)
                rows = []
                failed_calls += 1
                log(f"{source_name} keyword search failed for {q}: {exc}")
                if is_rate_limit_error(exc):
                    disabled_sources.add(source_name)
                    log(f"{source_name} disabled for remaining weekly queries after exhausted rate-limit retries")
            all_records.extend(rows)
            search_stats[source_name] = search_stats.get(source_name, 0) + len(rows)
            detail_rows.append(
                {"phase": "weekly", "source": source_name, "query": q, "count": len(rows), "error": error}
            )
        time.sleep(args.sleep)

    seeds = read_yaml("configs/seed_datasets.yml", {}).get("seeds", [])
    log_section("WEEKLY OPENALEX CITATION EXPANSION")
    for index, seed in enumerate(seeds, 1):
        dataset = seed.get("dataset", "unknown")
        log_step(index, len(seeds), f"Recent citing papers for benchmark seed: {dataset}")
        error = ""
        try:
            rows = search_openalex_citations(
                seed,
                args.citation_limit,
                start_date=start.isoformat(),
                end_date=end.isoformat(),
            )
            successful_calls += 1
        except Exception as exc:
            error = str(exc)
            rows = []
            failed_calls += 1
            log(f"OpenAlex citation search failed for {dataset}: {exc}")
        all_records.extend(rows)
        search_stats["citation:openalex"] = search_stats.get("citation:openalex", 0) + len(rows)
        detail_rows.append(
            {
                "phase": "weekly_citation",
                "source": "openalex",
                "query": dataset,
                "count": len(rows),
                "error": error,
            }
        )
        time.sleep(args.sleep)

    all_records = filter_records_by_date(all_records, start.isoformat(), end.isoformat())
    current_unique = deduplicate(all_records)
    merged = merge_existing_candidates(args.output, all_records)
    write_yaml(args.output, merged)
    report = {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": "weekly",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "raw_records": len(all_records),
        "current_unique_candidates": len(current_unique),
        "deduplicated_candidates": len(merged),
        "search_stats": search_stats,
        "successful_calls": successful_calls,
        "failed_calls": failed_calls,
        "details": detail_rows,
        "output": args.output,
    }
    write_search_report(report, args.report)
    log_section("WEEKLY SEARCH SUMMARY")
    log(f"Current-window unique candidates: {len(current_unique)}")
    log(f"Cumulative candidates: {len(merged)}")
    log(f"Source counts: {compact_count_table(search_stats)}")
    log(f"Candidate file: {args.output}")
    log(f"Search report: {args.report}")
    if successful_calls == 0:
        raise RuntimeError("All weekly search API calls failed; see the weekly search report for details")


def cmd_classify(args: argparse.Namespace) -> None:
    records = read_yaml(args.input, []) or []
    threshold = {"backfill": 0.60, "weekly": 0.75, "migrate": 0.0}[args.mode]
    total = len(records)
    eligible = sum(
        candidate_needs_processing(
            record,
            force_classification=args.force_classification,
            force_summary=args.force_summary,
            skip_minimax=args.skip_minimax,
        )
        for record in records
    )
    limit = min(args.limit, eligible) if args.limit and args.limit > 0 else eligible
    output_path = args.output or args.input

    processed = deepseek_calls = minimax_calls = parsed = rejected = errors = 0
    deepseek_attempts = deepseek_errors = minimax_attempts = minimax_errors = 0

    selected = 0
    for i, r in enumerate(records):
        title = r.get("title") or "Untitled"
        if not candidate_needs_processing(
            r,
            force_classification=args.force_classification,
            force_summary=args.force_summary,
            skip_minimax=args.skip_minimax,
        ):
            continue
        if selected >= limit:
            break
        selected += 1
        log(f"[{i + 1}/{total}] Processing: {title[:120]}")
        stage = ""
        try:
            if args.force_classification or not r.get("classification"):
                log(f"[{i + 1}/{total}] DeepSeek classify")
                stage = "deepseek"
                deepseek_attempts += 1
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
                    summary = r.get("summary") or {}
                    needs_summary = not summary or "leaderboard_metrics" not in summary
                    if args.force_summary or needs_summary:
                        log(f"[{i + 1}/{total}] MiniMax summary")
                        stage = "minimax"
                        minimax_attempts += 1
                        r["summary"] = minimax_summary(r, args.use_pdf)
                        mini_cat = (r.get("summary") or {}).get("main_category")
                        if mini_cat in set(CATEGORY_TO_FILE) | {"unrelated"}:
                            cls["minimax_main_category"] = mini_cat
                            if mini_cat != cls.get("main_category"):
                                cls["needs_review"] = True
                                (r.get("summary") or {})["category_confirmed"] = False
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
            if stage == "deepseek":
                deepseek_errors += 1
            elif stage == "minimax":
                minimax_errors += 1
            log(f"[{i + 1}/{total}] Failed: {e}")

        processed += 1
        r.setdefault("automation", {})["last_processed_date"] = dt.date.today().isoformat()
        write_yaml(output_path, records)
        log(
            f"Progress: processed={processed}/{limit}, parsed={parsed}, rejected={rejected}, "
            f"errors={errors}, deepseek_calls={deepseek_calls}, minimax_calls={minimax_calls}"
        )
        time.sleep(args.sleep)

    write_yaml(output_path, records)
    cls_counts = classification_summary(records)
    write_classification_report(records, args.report)
    log_section("CLASSIFICATION SUMMARY")
    log(
        f"Done. processed={processed}/{limit}, parsed={parsed}, rejected={rejected}, errors={errors}, "
        f"deepseek_calls={deepseek_calls}, minimax_calls={minimax_calls}"
    )
    log(
        f"Algorithm papers={cls_counts['algorithm_papers']}, "
        f"survey papers={cls_counts['survey_papers']}, "
        f"unrelated papers={cls_counts['unrelated_papers']}, "
        f"error papers={cls_counts['error_papers']}, raw papers={cls_counts['raw_papers']}"
    )
    log(f"Classification report: {args.report}")
    if deepseek_attempts and deepseek_errors == deepseek_attempts:
        raise RuntimeError("All attempted DeepSeek classifications failed; inspect candidate errors and API configuration")
    if minimax_attempts and minimax_errors == minimax_attempts:
        raise RuntimeError("All attempted MiniMax summaries failed; inspect candidate errors and API configuration")


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
        if any(("论文" in c) or (c.strip().lower() == "paper") for c in cells):
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
                "summary_en": "",
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
        md.append("| Paper | Research Content | Dataset / Benchmark | Code |")
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
                f"| {paper_cell} | {md_escape(summ.get('summary_en') or '')} | {md_escape(', '.join(benchmarks) if benchmarks else '-')} | {code_cell} |"
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
    today = parse_iso_date(args.date) or dt.date.today()
    iso = today.isocalendar()
    week_name = args.output or f"weekly_updates/{iso.year}-W{iso.week:02d}.md"
    rows = weekly_digest_records(records, today)
    md = [f"# Weekly UAV-CVGL Update: {iso.year}-W{iso.week:02d}", ""]
    md.append("This file is generated by the automated weekly search pipeline. All entries are unverified until manually reviewed.")
    md.append("")
    md.append("| Paper | Category | Dataset / Benchmark | Research Summary | Status |")
    md.append("|---|---|---|---|---|")
    if not rows:
        md.append("| No new parsed papers this week | - | - | - | - |")
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
            f"| {paper_cell} | {md_escape(cat)} | {md_escape(', '.join(benchmarks) if benchmarks else '-')} | {md_escape(summ.get('summary_en') or cls.get('reason') or '')} | {md_escape(status)} |"
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
    result = {
        "total": total,
        "status": status_counts,
        "categories": cats,
        "paper_type_summary": classification_summary(records),
        "deepseek_done": deepseek,
        "minimax_done": minimax,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UAV-CVGL automation pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("preflight", help="validate required automation configuration without calling APIs")
    p.add_argument("--require-llm", action="store_true")
    p.set_defaults(func=cmd_preflight)

    p = sub.add_parser("backfill", help="large-scale historical search")
    p.add_argument("--start-year", type=int, default=2016)
    p.add_argument("--end-year", type=int, default=dt.date.today().year)
    p.add_argument("--limit-per-query", type=int, default=30)
    p.add_argument("--citation-limit", type=int, default=300)
    p.add_argument("--output", default="data/backfill_candidates.yml")
    p.add_argument("--report", default="data/reports/backfill_search_report.md")
    p.add_argument("--sleep", type=float, default=0.5)
    p.set_defaults(func=cmd_backfill)

    p = sub.add_parser("weekly", help="weekly recent search")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--limit-per-query", type=int, default=15)
    p.add_argument("--citation-limit", type=int, default=100)
    p.add_argument("--output", default="data/weekly_candidates.yml")
    p.add_argument("--report", default="data/reports/weekly_search_report.md")
    p.add_argument("--sleep", type=float, default=0.5)
    p.set_defaults(func=cmd_weekly)

    p = sub.add_parser("classify", help="DeepSeek classify, MiniMax summarize")
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="")
    p.add_argument("--mode", choices=["backfill", "weekly", "migrate"], default="weekly")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--skip-minimax", action="store_true")
    p.add_argument("--use-pdf", action="store_true", default=True, help="fetch and extract accessible PDF text for MiniMax summaries (default)")
    p.add_argument("--no-pdf", dest="use_pdf", action="store_false", help="skip PDF text extraction")
    p.add_argument("--force-classification", action="store_true")
    p.add_argument("--force-summary", action="store_true")
    p.add_argument("--report", default="data/reports/classification_report.md")
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
    p.add_argument("--date", default="", help="target date in YYYY-MM-DD format (defaults to today)")
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





