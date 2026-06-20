#!/usr/bin/env python3
"""
Rebuild UAV-CVGL leaderboards from dataset-level specifications and per-paper
MiniMax-M3 reviews.

The workflow is intentionally split into resumable stages:

1. specs  - DeepSeek reads dataset benchmark evidence and writes the official
            leaderboard protocol/column specification.
2. review - MiniMax-M3 reviews one paper at a time and extracts only flagship
            main-protocol results.
3. build  - Generate data/leaderboards.csv and English Markdown leaderboard
            pages in wide-table form.

No API keys are stored in files. The script checks environment-variable
presence only and never prints secret values.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import http.cookiejar
import json
import multiprocessing as mp
import os
import queue
import re
import sys
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import uav_cvgl_auto as auto  # noqa: E402

DEFAULT_DATASETS = [
    "University-1652",
    "SUES-200",
    "DenseUAV",
    "UAV-VisLoc",
    "GTA-UAV",
    "Game4Loc",
    "World-UAV",
    "UAV-GeoLoc",
    "Nardo-Air",
]

SPEC_PATH = ROOT / "data" / "internal" / "leaderboard_dataset_specs.yml"
REVIEW_PATH = ROOT / "data" / "internal" / "leaderboard_reviews.yml"
REPORT_PATH = ROOT / "data" / "reports" / "leaderboard_rebuild_report.md"
CSV_PATH = ROOT / "data" / "leaderboards.csv"
FULLTEXT_PATH = ROOT / "data" / "internal" / "leaderboard_fulltext_access.yml"

ACCESS_ATTEMPT_LIMIT = 24
COOKIE_LOAD_LOGGED: set[str] = set()


def log(msg: str) -> None:
    now = dt.datetime.now().strftime("%H:%M:%S")
    safe = str(msg).encode("ascii", errors="backslashreplace").decode("ascii")
    print(f"[leaderboard {now}] {safe}", flush=True)


def resolve_paper_timeout(value: Optional[int] = None) -> int:
    if value is not None and value > 0:
        return int(value)
    raw = os.getenv("LEADERBOARD_DISCOVERY_TIMEOUT", "300").strip()
    try:
        return max(0, int(float(raw)))
    except ValueError:
        return 300


def resolve_url_timeout() -> int:
    raw = os.getenv("LEADERBOARD_URL_TIMEOUT", "30").strip()
    try:
        return max(5, int(float(raw)))
    except ValueError:
        return 30


def strip_fulltext(record: dict) -> dict:
    return {k: v for k, v in (record or {}).items() if k != "fulltext"}


def require_env(names: Iterable[str]) -> None:
    missing = [name for name in names if not os.getenv(name, "").strip()]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(f"Missing required environment variables: {joined}")
    model = os.getenv("MINIMAX_MODEL", "MiniMax-M3")
    if "MINIMAX_API_KEY" in names and model != "MiniMax-M3":
        raise RuntimeError(f"MINIMAX_MODEL must be MiniMax-M3, got {model!r}")


def read_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return default if data is None else data


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=140)
    os.replace(tmp, path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def clean(value: Any) -> str:
    text = "" if value is None else str(value)
    replacements = {
        "鈫扴": "->",
        "鈫?": "->",
        "鈥?": "-",
        "�": "",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def md_escape(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_link(label: str, url: str) -> str:
    label = md_escape(label)
    url = clean(url)
    return f"[{label}]({url})" if url else label


def norm_key(text: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", clean(text).lower())


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    text = clean(value)
    if not text:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", text.replace(",", ""))
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def load_benchmark_aliases() -> Dict[str, str]:
    cfg = read_yaml(ROOT / "configs" / "benchmarks.yml", {}) or {}
    aliases: Dict[str, str] = {}
    for name in cfg.get("benchmarks", []) or []:
        aliases[norm_key(name)] = name
    for name, values in (cfg.get("aliases") or {}).items():
        aliases[norm_key(name)] = name
        for value in values or []:
            aliases[norm_key(value)] = name
    aliases[norm_key("UAV GeoLoc")] = "UAV-GeoLoc"
    aliases[norm_key("UAVPlace")] = "UAV-GeoLoc"
    aliases[norm_key("Game4Loc")] = "GTA-UAV"
    return aliases


def canonical_dataset(name: Any, aliases: Dict[str, str]) -> str:
    raw = clean(name)
    return aliases.get(norm_key(raw), raw)


def paper_url(paper: dict) -> str:
    urls = paper.get("urls") or {}
    source = paper.get("source") or {}
    return clean(
        urls.get("paper")
        or urls.get("pdf")
        or urls.get("project")
        or (f"https://doi.org/{source.get('doi')}" if source.get("doi") else "")
        or (f"https://arxiv.org/abs/{source.get('arxiv_id')}" if source.get("arxiv_id") else "")
        or source.get("openalex_id")
        or ""
    )


def paper_id(paper: dict) -> str:
    return clean(paper.get("id")) or auto.stable_id(paper.get("title", ""), paper.get("year"))


def dataset_mentions(paper: dict, aliases: Dict[str, str]) -> List[str]:
    found: set[str] = set()
    cls = paper.get("classification") or {}
    summary = paper.get("summary") or {}
    for value in cls.get("datasets") or []:
        ds = canonical_dataset(value, aliases)
        if ds:
            found.add(ds)
    for value in summary.get("benchmarks") or []:
        ds = canonical_dataset(value, aliases)
        if ds:
            found.add(ds)
    for row in summary.get("leaderboard_metrics") or []:
        ds = canonical_dataset(row.get("dataset"), aliases)
        if ds:
            found.add(ds)

    text = " ".join(
        [
            clean(paper.get("title")),
            clean(paper.get("abstract")),
            clean(summary.get("summary_en")),
            " ".join(map(clean, summary.get("reported_results") or [])),
            " ".join(map(clean, summary.get("table_evidence_notes") or [])) if isinstance(summary.get("table_evidence_notes"), list) else clean(summary.get("table_evidence_notes")),
        ]
    )
    lowered = text.lower()
    for key, canonical in aliases.items():
        # Use the original configured dataset names for substring matching.
        if canonical.lower() in lowered:
            found.add(canonical)
    return sorted(found)


def all_source_papers() -> List[dict]:
    merged: Dict[str, dict] = {}
    for rel in ["data/papers.yml", "data/backfill_candidates.yml"]:
        for paper in read_yaml(ROOT / rel, []) or []:
            pid = paper_id(paper)
            if not pid:
                continue
            old = merged.get(pid)
            if not old:
                merged[pid] = paper
                continue
            # Prefer the richer candidate record, but keep official merged status.
            if len(json.dumps(paper, ensure_ascii=False)) > len(json.dumps(old, ensure_ascii=False)):
                merged[pid] = paper
    return list(merged.values())


def select_papers(datasets: List[str], include_surveys: bool = False) -> List[dict]:
    aliases = load_benchmark_aliases()
    wanted = {canonical_dataset(ds, aliases) for ds in datasets}
    selected: List[dict] = []
    for paper in all_source_papers():
        status = paper.get("status")
        cls = paper.get("classification") or {}
        category = cls.get("main_category")
        if status not in {"parsed", None}:
            continue
        if category == "survey" and not include_surveys:
            continue
        mentions = set(dataset_mentions(paper, aliases))
        if mentions & wanted:
            copied = dict(paper)
            copied["_leaderboard_datasets"] = sorted(mentions & wanted)
            selected.append(copied)
    selected.sort(key=lambda p: (max(p.get("year") or 0, 0), p.get("title") or ""), reverse=True)
    return selected


def deepseek_json(system: str, user: str, max_tokens: int = 2200) -> dict:
    api_key = auto.normalize_deepseek_api_key(os.getenv("DEEPSEEK_API_KEY", ""))
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "max_tokens": max_tokens,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    timeout = float(os.getenv("DEEPSEEK_REQUEST_TIMEOUT", "180"))
    retries = int(os.getenv("DEEPSEEK_REQUEST_RETRIES", "3"))
    data = auto.request_json(
        "https://api.deepseek.com/chat/completions",
        method="POST",
        headers=headers,
        json_body=payload,
        timeout=timeout,
        retries=retries,
    )
    content = data["choices"][0]["message"].get("content") or ""
    try:
        return auto.parse_json_object(content)
    except Exception:
        payload["max_tokens"] = max(max_tokens, 6000)
        payload["messages"] = [
            {"role": "system", "content": "Return exactly one compact valid JSON object. No Markdown, no commentary, no trailing prose."},
            {"role": "user", "content": user + "\n\nReturn compact JSON only. Keep descriptions concise."},
        ]
        data = auto.request_json(
            "https://api.deepseek.com/chat/completions",
            method="POST",
            headers=headers,
            json_body=payload,
            timeout=timeout,
            retries=retries,
        )
        content = data["choices"][0]["message"].get("content") or ""
        return auto.parse_json_object(content)


def minimax_json(system: str, user: str, max_tokens: int = 6000, *, tools: Optional[List[dict]] = None) -> dict:
    api_key = os.getenv("MINIMAX_API_KEY", "").strip()
    model = os.getenv("MINIMAX_MODEL", "MiniMax-M3")
    base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1").rstrip("/")
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": max_tokens,
        "thinking": {"type": "disabled"},
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = os.getenv("MINIMAX_TOOL_CHOICE", "auto")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    content = ""
    max_tool_rounds = int(os.getenv("MINIMAX_SEARCH_TOOL_ROUNDS", "3"))
    for round_idx in range(max_tool_rounds + 1):
        payload["messages"] = messages
        data = auto.minimax_chat_completion(base_url, headers, payload)
        message = data["choices"][0].get("message") or {}
        content = message.get("content") or ""
        tool_calls = message.get("tool_calls") or []
        if not tools or not tool_calls or round_idx >= max_tool_rounds:
            break
        messages.append(message)
        for call in tool_calls:
            messages.append(execute_minimax_tool_call(call))
    if tools and not content.strip():
        final_messages = messages + [
            {
                "role": "user",
                "content": "Use the search results already provided above. Do not call more tools. Return one valid JSON object now.",
            }
        ]
        final_payload = {
            "model": model,
            "messages": final_messages,
            "temperature": 0.0,
            "max_tokens": max_tokens,
            "thinking": {"type": "disabled"},
        }
        data = auto.minimax_chat_completion(base_url, headers, final_payload)
        content = data["choices"][0]["message"].get("content") or ""
    try:
        return auto.parse_json_object(content)
    except Exception:
        retry_payload = {
            "model": model,
            "messages": [
            {"role": "system", "content": "Return one valid JSON object only. No Markdown, no commentary, no hidden thinking."},
            {"role": "user", "content": user + "\n\nReturn the JSON object now."},
            ],
            "temperature": 0.0,
            "max_tokens": max_tokens,
            "thinking": {"type": "disabled"},
        }
        data = auto.minimax_chat_completion(base_url, headers, retry_payload)
        content = data["choices"][0]["message"].get("content") or ""
        return auto.parse_json_object(content)


def minimax_search_tools() -> List[dict]:
    raw = os.getenv("MINIMAX_SEARCH_TOOLS_JSON", "").strip()
    if raw:
        tools = json.loads(raw)
        if isinstance(tools, dict):
            return [tools]
        if isinstance(tools, list):
            return tools
        raise ValueError("MINIMAX_SEARCH_TOOLS_JSON must be a JSON object or array")
    return [{"type": "web_search"}]


def minimax_search_tool_variants() -> List[List[dict]]:
    raw = os.getenv("MINIMAX_SEARCH_TOOL_VARIANTS_JSON", "").strip()
    if raw:
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("MINIMAX_SEARCH_TOOL_VARIANTS_JSON must be a JSON array")
        variants: List[List[dict]] = []
        for item in data:
            if isinstance(item, dict):
                variants.append([item])
            elif isinstance(item, list):
                variants.append(item)
            else:
                raise ValueError("Each MINIMAX_SEARCH_TOOL_VARIANTS_JSON item must be an object or array")
        return variants
    if os.getenv("MINIMAX_SEARCH_TOOLS_JSON", "").strip():
        return [minimax_search_tools()]
    return [[{"type": "web_search"}]]


def load_fulltext_cache() -> Dict[str, dict]:
    data = read_yaml(FULLTEXT_PATH, []) or []
    if isinstance(data, dict):
        return data
    return {clean(row.get("paper_id")): row for row in data if row.get("paper_id")}


def save_fulltext_cache(cache: Dict[str, dict]) -> None:
    rows = list(cache.values())
    rows.sort(key=lambda r: (r.get("paper_title") or ""))
    write_yaml(FULLTEXT_PATH, rows)


def save_fulltext_record(record: dict) -> None:
    cache = load_fulltext_cache()
    cache[clean(record.get("paper_id"))] = record
    save_fulltext_cache(cache)


def requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    cookie_file = os.getenv("UAV_CVGL_COOKIE_FILE", "").strip()
    if cookie_file:
        path = Path(cookie_file)
        if path.exists():
            try:
                jar = http.cookiejar.MozillaCookieJar(str(path))
                jar.load(ignore_discard=True, ignore_expires=True)
                session.cookies.update(jar)
                if str(path) not in COOKIE_LOAD_LOGGED:
                    log(f"loaded cookie file for requests session: {path.name}")
                    COOKIE_LOAD_LOGGED.add(str(path))
            except Exception as e:
                log(f"cookie file could not be loaded: {e}")
    return session


def ezproxy_url(url: str) -> str:
    prefix = os.getenv("UAV_CVGL_EZPROXY_PREFIX", "").strip()
    if not prefix:
        return ""
    if "{url}" in prefix:
        return prefix.replace("{url}", urllib.parse.quote(url, safe=""))
    return prefix + urllib.parse.quote(url, safe="")


def add_ezproxy_candidates(candidates: List[str]) -> None:
    if not os.getenv("UAV_CVGL_EZPROXY_PREFIX", "").strip():
        return
    originals = list(candidates)
    for url in originals:
        proxied = ezproxy_url(url)
        if proxied:
            auto.add_url_candidate(candidates, proxied)


def should_skip_candidate_url(url: str) -> Tuple[bool, str]:
    lowered = clean(url).lower()
    if not lowered:
        return True, "empty URL"
    if os.getenv("LEADERBOARD_SKIP_IEEE_STAGING", "1").strip().lower() not in {"0", "false", "no", "off"}:
        if "xplorestaging.ieee.org" in lowered:
            return True, "IEEE staging PDF endpoint is unstable for non-browser requests"
    return False, ""


def candidate_url_priority(url: str) -> int:
    lowered = clean(url).lower()
    if "arxiv.org/pdf/" in lowered:
        return 0
    if any(domain in lowered for domain in ["pmc.ncbi.nlm.nih.gov", "ncbi.nlm.nih.gov/pmc", "mdpi.com"]):
        return 1
    if auto.likely_pdf_url(url) or any(token in lowered for token in ["/pdf", "stamp.jsp", ".pdf?"]):
        return 2
    if "arxiv.org/abs/" in lowered:
        return 3
    if any(domain in lowered for domain in ["doi.org", "openalex.org", "semanticscholar.org"]):
        return 9
    return 5


def order_url_candidates(candidates: List[str]) -> List[str]:
    indexed = list(enumerate(dict.fromkeys(candidates)))
    indexed.sort(key=lambda item: (candidate_url_priority(item[1]), item[0]))
    return [url for _, url in indexed]


def decode_duckduckgo_url(raw: str) -> str:
    raw = html.unescape(raw or "")
    if raw.startswith("//"):
        raw = "https:" + raw
    parsed = urllib.parse.urlparse(raw)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = urllib.parse.parse_qs(parsed.query)
        raw = (qs.get("uddg") or [""])[0]
    return html.unescape(raw)


def search_duckduckgo_query(query: str, limit: int = 8) -> List[dict]:
    if not clean(query):
        return []
    results: List[dict] = []
    try:
        with requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            timeout=auto.DEFAULT_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html,*/*;q=0.8"},
        ) as r:
            r.raise_for_status()
            page = r.text
        pattern = re.compile(
            r'<a[^>]+class=["\'][^"\']*result__a[^"\']*["\'][^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            flags=re.I | re.S,
        )
        for match in pattern.finditer(page):
            url = decode_duckduckgo_url(match.group(1))
            title = clean(re.sub(r"<.*?>", " ", html.unescape(match.group(2))))
            if not url or any(block in url.lower() for block in ["duckduckgo.com", "javascript:", "mailto:"]):
                continue
            results.append({"title": title, "url": url})
            if len(results) >= limit:
                break
    except Exception as e:
        log(f"DuckDuckGo query search skipped: {e}")
    return results


def execute_minimax_tool_call(call: dict) -> dict:
    function = call.get("function") or {}
    name = clean(function.get("name")) or "plugin_web_search"
    args_text = function.get("arguments") or "{}"
    try:
        args = json.loads(args_text)
    except Exception:
        args = {}
    query = clean(args.get("query_key") or args.get("query") or args.get("q"))
    log(f"MiniMax requested web search: {query}")
    results = search_duckduckgo_query(query, limit=int(os.getenv("MINIMAX_TOOL_SEARCH_RESULTS", "8")))
    log(f"MiniMax web search results returned: {len(results)}")
    content = json.dumps({"query": query, "results": results}, ensure_ascii=False)
    return {
        "role": "tool",
        "tool_call_id": call.get("id"),
        "name": name,
        "content": content,
    }


def search_crossref_candidates(paper: dict) -> List[str]:
    title = clean(paper.get("title"))
    doi = clean((paper.get("source") or {}).get("doi") or paper.get("doi"))
    urls: List[str] = []
    try:
        if doi:
            data = auto.request_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}", retries=1, timeout=30)
            msg = data.get("message") or {}
        else:
            data = auto.request_json("https://api.crossref.org/works", params={"query.title": title, "rows": 3}, retries=1, timeout=30)
            items = ((data.get("message") or {}).get("items") or [])
            msg = items[0] if items else {}
        for link in msg.get("link") or []:
            auto.add_url_candidate(urls, link.get("URL") or "")
        auto.add_url_candidate(urls, msg.get("URL") or "")
        if msg.get("DOI"):
            auto.add_url_candidate(urls, f"https://doi.org/{msg.get('DOI')}")
    except Exception as e:
        log(f"Crossref candidate search skipped: {e}")
    return urls


def search_unpaywall_candidates(paper: dict) -> List[str]:
    doi = clean((paper.get("source") or {}).get("doi") or paper.get("doi")).replace("https://doi.org/", "")
    if not doi:
        return []
    email = os.getenv("UNPAYWALL_EMAIL", "").strip() or os.getenv("OPENALEX_MAILTO", "").strip() or "uav-cvgl@example.com"
    urls: List[str] = []
    try:
        data = auto.request_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi, safe='')}", params={"email": email}, retries=1, timeout=30)
        for loc in [data.get("best_oa_location") or {}] + (data.get("oa_locations") or []):
            auto.add_url_candidate(urls, loc.get("url_for_pdf") or "")
            auto.add_url_candidate(urls, loc.get("url_for_landing_page") or "")
    except Exception as e:
        log(f"Unpaywall candidate search skipped: {e}")
    return urls


def search_duckduckgo_candidates(paper: dict, limit: int = 8) -> List[str]:
    title = clean(paper.get("title"))
    if not title:
        return []
    query = f'"{title}" pdf OR html'
    return [row["url"] for row in search_duckduckgo_query(query, limit=limit)]


def base_url_candidates_for_paper(paper: dict) -> List[str]:
    urls = paper.get("urls") or {}
    source = paper.get("source") or {}
    candidates: List[str] = []
    for url in [urls.get("pdf"), urls.get("paper"), urls.get("project"), paper_url(paper)]:
        auto.add_url_candidate(candidates, url or "")
    doi = clean(source.get("doi") or paper.get("doi"))
    if doi:
        auto.add_url_candidate(candidates, doi)
    arxiv_id = clean(source.get("arxiv_id"))
    if arxiv_id:
        auto.add_url_candidate(candidates, f"https://arxiv.org/abs/{arxiv_id}")
        auto.add_url_candidate(candidates, f"https://arxiv.org/pdf/{arxiv_id}")
    openalex_id = clean(source.get("openalex_id"))
    if openalex_id:
        auto.add_url_candidate(candidates, openalex_id)
    try:
        for url in auto.pdf_candidate_urls_for_paper(paper):
            auto.add_url_candidate(candidates, url)
    except Exception as e:
        log(f"local candidate URL collection warning: {e}")
    for fn in [search_unpaywall_candidates, search_crossref_candidates]:
        for url in fn(paper):
            auto.add_url_candidate(candidates, url)
    if os.getenv("LEADERBOARD_USE_LOCAL_SEARCH", "").strip().lower() in {"1", "true", "yes", "on"}:
        for url in search_duckduckgo_candidates(paper):
            auto.add_url_candidate(candidates, url)
    add_ezproxy_candidates(candidates)
    return list(dict.fromkeys(candidates))


def minimax_fulltext_candidates(paper: dict) -> List[str]:
    require_env(["MINIMAX_API_KEY"])
    model = os.getenv("MINIMAX_MODEL", "MiniMax-M3")
    log(f"MiniMax search model: {model}")
    system = (
        "You find accessible full-text sources for academic papers using the provided built-in search/web-reading tools. "
        "Return valid JSON only. Prefer open PDFs, arXiv PDFs, publisher article pages, PubMed Central, MDPI, IEEE/ACM/Springer/Elsevier pages, "
        "repository landing pages, and author/project pages. Do not invent URLs. Only include URLs you found or verified through search/web reading."
    )
    user = f"""
Paper title: {paper.get('title', '')}
Year: {paper.get('year', '')}
Venue: {paper.get('venue', '')}
Known URLs: {json.dumps(paper.get('urls') or {}, ensure_ascii=False)}
Source IDs: {json.dumps(paper.get('source') or {}, ensure_ascii=False)}
Abstract:
{clean(paper.get('abstract'))[:2500]}

Use search/web reading to find candidate URLs for accessible full text or result tables.
Return JSON:
{{
  "pdf_urls": array of strings,
  "html_urls": array of strings,
  "evidence_urls": array of strings,
  "reason": string
}}
""".strip()
    errors: List[str] = []
    obj: Optional[dict] = None
    for tools in minimax_search_tool_variants():
        try:
            log(f"MiniMax built-in tools: {[tool.get('type') for tool in tools]}")
            obj = minimax_json(system, user, max_tokens=2600, tools=tools)
            break
        except Exception as e:
            errors.append(f"{[tool.get('type') for tool in tools]}: {str(e)[:220]}")
            log(f"MiniMax search tool attempt failed: {errors[-1]}")
    if obj is None:
        raise RuntimeError("MiniMax built-in search failed for all configured tool variants: " + " | ".join(errors))
    pdf_urls = [clean(url) for url in obj.get("pdf_urls") or [] if clean(url)]
    html_urls = [clean(url) for url in obj.get("html_urls") or [] if clean(url)]
    evidence_urls = [clean(url) for url in obj.get("evidence_urls") or [] if clean(url)]
    log(f"MiniMax candidate URLs: pdf={len(pdf_urls)}, html={len(html_urls)}, evidence={len(evidence_urls)}")
    for url in pdf_urls:
        log(f"  pdf candidate: {url}")
    for url in html_urls:
        log(f"  html candidate: {url}")
    for url in evidence_urls:
        log(f"  evidence candidate: {url}")
    out: List[str] = []
    for url in pdf_urls + html_urls + evidence_urls:
        auto.add_url_candidate(out, url)
    return out


def fetch_url_with_session(url: str, max_bytes: int, *, accept: str) -> Tuple[str, str, bytes]:
    session = requests_session()
    headers = {
        "Accept": accept,
        "Referer": url,
    }
    with session.get(url, timeout=resolve_url_timeout(), headers=headers, stream=True, allow_redirects=True) as r:
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


def log_attempt_result(meta: dict, ok: bool) -> None:
    kind = clean(meta.get("kind")) or ("accessible" if ok else "unknown")
    url = clean(meta.get("url"))
    content_type = clean(meta.get("content_type"))
    chars = meta.get("chars", 0)
    status = "accessible" if ok else kind
    log(f"  result: {status}; kind={kind}; chars={chars}; content_type={content_type}; url={url}")


def extract_text_from_url(url: str, paper: dict) -> Tuple[str, dict]:
    char_limit = int(os.getenv("MINIMAX_PDF_CHAR_LIMIT", "120000"))
    table_char_limit = int(os.getenv("MINIMAX_TABLE_CHAR_LIMIT", "30000"))
    max_pages = int(os.getenv("MINIMAX_PDF_MAX_PAGES", "80"))
    max_bytes = int(os.getenv("MINIMAX_PDF_MAX_BYTES", str(100 * 1024 * 1024)))
    landing_max_bytes = int(os.getenv("MINIMAX_PDF_LANDING_MAX_BYTES", str(5 * 1024 * 1024)))
    current_url, content_type, content = fetch_url_with_session(
        url,
        max_bytes if auto.likely_pdf_url(url) else landing_max_bytes,
        accept="text/html,application/pdf;q=0.9,*/*;q=0.8",
    )
    if auto.response_looks_like_pdf(current_url, content_type, content):
        text = auto.extract_pdf_text_from_bytes(content, paper.get("title", "Untitled"), char_limit, max_pages, current_url)
        tables = auto.extract_pdf_tables_from_bytes(content, max_pages, table_char_limit)
        if text and tables:
            text = text + "\n\nTABLE EVIDENCE:\n" + tables
        return text, {"url": current_url, "kind": "pdf", "content_type": content_type, "chars": len(text or "")}
    if "html" in (content_type or "").lower() or b"<html" in content[:1000].lower():
        html_text = content.decode("utf-8", errors="ignore")
        article_text = auto.extract_article_text_from_html(html_text, char_limit)
        html_tables = auto.extract_html_tables_from_html(html_text, table_char_limit)
        combined = article_text
        if html_tables:
            combined = (combined + "\n\nTABLE EVIDENCE:\n" if combined else "TABLE EVIDENCE:\n") + html_tables
        if combined:
            return combined[: char_limit + table_char_limit], {"url": current_url, "kind": "html", "content_type": content_type, "chars": len(combined)}
        for link in auto.extract_pdf_links_from_html(html_text, current_url)[:5]:
            try:
                text, meta = extract_text_from_url(link, paper)
                if text:
                    meta["discovered_from"] = current_url
                    return text, meta
            except Exception:
                continue
        return "", {"url": current_url, "kind": "html_no_extract", "content_type": content_type, "chars": 0}
    return "", {"url": current_url, "kind": "unknown", "content_type": content_type, "chars": 0}


def discover_accessible_fulltext(paper: dict, *, force: bool = False) -> dict:
    cache = load_fulltext_cache()
    pid = paper_id(paper)
    if pid in cache and not force:
        return cache[pid]

    candidates: List[str] = []
    for url in base_url_candidates_for_paper(paper):
        auto.add_url_candidate(candidates, url)
    try:
        for url in minimax_fulltext_candidates(paper):
            auto.add_url_candidate(candidates, url)
    except Exception as e:
        log(f"MiniMax full-text discovery failed for {paper.get('title', '')[:80]}: {e}")
    add_ezproxy_candidates(candidates)
    candidates = order_url_candidates(candidates)

    attempted: List[dict] = []
    log(f"URL candidates to validate: {min(len(candidates), ACCESS_ATTEMPT_LIMIT)}")
    attempts = 0
    for url in candidates:
        skip, reason = should_skip_candidate_url(url)
        if skip:
            log(f"  skipped candidate: {url}; reason={reason}")
            attempted.append({"url": url, "ok": False, "skipped": True, "reason": reason})
            continue
        attempts += 1
        if attempts > ACCESS_ATTEMPT_LIMIT:
            break
        log(f"  access attempt [{attempts}/{ACCESS_ATTEMPT_LIMIT}]: {url}")
        try:
            text, meta = extract_text_from_url(url, paper)
            attempted.append({**meta, "ok": bool(text)})
            log_attempt_result(meta, bool(text))
            if text:
                record = {
                    "paper_id": pid,
                    "paper_title": paper.get("title"),
                    "status": "accessible",
                    "selected_url": meta.get("url") or url,
                    "kind": meta.get("kind"),
                    "chars": len(text),
                    "attempted": attempted,
                    "fulltext": text[: int(os.getenv("LEADERBOARD_FULLTEXT_CACHE_CHARS", "160000"))],
                    "checked_at": dt.datetime.now().isoformat(timespec="seconds"),
                }
                cache[pid] = record
                save_fulltext_cache(cache)
                log(f"full text accessible: kind={record['kind']}, chars={record['chars']}, title={paper.get('title', '')[:80]}")
                return record
        except Exception as e:
            log(f"  result: error; url={url}; error={str(e)[:220]}")
            attempted.append({"url": url, "ok": False, "error": str(e)[:500]})

    needs_browser = any(
        (a.get("kind") == "html_no_extract")
        or ("403" in (a.get("error") or ""))
        or ("Forbidden" in (a.get("error") or ""))
        for a in attempted
    )
    record = {
        "paper_id": pid,
        "paper_title": paper.get("title"),
        "status": "needs_browser_session" if needs_browser else "inaccessible",
        "reason": "No accessible PDF or HTML article/table text found after MiniMax-assisted URL discovery and local URL validation.",
        "attempted": attempted,
        "fulltext": "",
        "checked_at": dt.datetime.now().isoformat(timespec="seconds"),
    }
    cache[pid] = record
    save_fulltext_cache(cache)
    log(f"full text inaccessible: {paper.get('title', '')[:100]}")
    return record


def _discover_worker(paper: dict, force: bool, result_queue: mp.Queue) -> None:
    try:
        record = discover_accessible_fulltext(paper, force=force)
        result_queue.put({"ok": True, "record": strip_fulltext(record)})
    except BaseException as e:
        result_queue.put({"ok": False, "error": str(e)[:1000]})


def discover_accessible_fulltext_with_timeout(paper: dict, *, force: bool = False, paper_timeout: Optional[int] = None) -> dict:
    pid = paper_id(paper)
    cache = load_fulltext_cache()
    if pid in cache and not force:
        return cache[pid]

    timeout = resolve_paper_timeout(paper_timeout)
    if timeout <= 0:
        return discover_accessible_fulltext(paper, force=force)

    log(f"per-paper timeout: {timeout}s")
    ctx = mp.get_context("spawn" if os.name == "nt" else "fork")
    result_queue = ctx.Queue()
    proc = ctx.Process(target=_discover_worker, args=(paper, force, result_queue), name=f"leaderboard-discover-{pid[:12]}")
    proc.start()
    proc.join(timeout)
    if proc.is_alive():
        proc.terminate()
        proc.join(10)
        if proc.is_alive() and hasattr(proc, "kill"):
            proc.kill()
            proc.join(5)
        record = {
            "paper_id": pid,
            "paper_title": paper.get("title"),
            "status": "timeout",
            "reason": f"Full-text discovery exceeded the per-paper wall-clock timeout of {timeout} seconds.",
            "current_stage": "subprocess full-text discovery",
            "attempted": [],
            "fulltext": "",
            "checked_at": dt.datetime.now().isoformat(timespec="seconds"),
        }
        save_fulltext_record(record)
        log(f"full text timeout: title={paper.get('title', '')[:100]}, timeout={timeout}s")
        return record

    result: Optional[dict] = None
    try:
        result = result_queue.get_nowait()
    except queue.Empty:
        pass
    finally:
        result_queue.close()

    cache = load_fulltext_cache()
    if pid in cache:
        return cache[pid]
    if result and result.get("ok"):
        return result.get("record") or {}

    error = (result or {}).get("error") or f"worker exited with code {proc.exitcode} without writing a cache record"
    record = {
        "paper_id": pid,
        "paper_title": paper.get("title"),
        "status": "error",
        "reason": error,
        "current_stage": "subprocess full-text discovery",
        "attempted": [],
        "fulltext": "",
        "checked_at": dt.datetime.now().isoformat(timespec="seconds"),
    }
    save_fulltext_record(record)
    log(f"full text discovery error: title={paper.get('title', '')[:100]}, error={error[:220]}")
    return record


def default_dataset_specs() -> Dict[str, dict]:
    return {
        "University-1652": {
            "dataset": "University-1652",
            "description": "UAV-to-satellite cross-view geo-localization benchmark with drone-to-satellite and satellite-to-drone retrieval protocols.",
            "official_protocols": [
                {
                    "name": "Drone-to-Satellite",
                    "columns": ["R@1", "R@5", "R@10", "AP"],
                    "primary_sort_metric": "R@1",
                    "higher_is_better": True,
                },
                {
                    "name": "Satellite-to-Drone",
                    "columns": ["R@1", "R@5", "R@10", "AP"],
                    "primary_sort_metric": "R@1",
                    "higher_is_better": True,
                },
            ],
            "inclusion_rules": "Use only the final method on the standard University-1652 protocol. Exclude ablations, re-ranking/TTA variants, weather subsets, and transfer-only settings.",
        },
        "SUES-200": {
            "dataset": "SUES-200",
            "description": "Multi-height UAV-satellite benchmark with altitude-specific retrieval results.",
            "official_protocols": [
                {
                    "name": "Drone-to-Satellite",
                    "columns": [
                        "150m R@1", "150m AP", "200m R@1", "200m AP", "250m R@1", "250m AP", "300m R@1", "300m AP",
                    ],
                    "primary_sort_metric": "300m R@1",
                    "higher_is_better": True,
                },
                {
                    "name": "Satellite-to-Drone",
                    "columns": [
                        "150m R@1", "150m AP", "200m R@1", "200m AP", "250m R@1", "250m AP", "300m R@1", "300m AP",
                    ],
                    "primary_sort_metric": "300m R@1",
                    "higher_is_better": True,
                },
            ],
            "inclusion_rules": "Use final method results on the official altitude protocol only. Exclude zero-shot transfer, weather robustness, and ablations unless a page is explicitly dedicated to that protocol.",
        },
        "DenseUAV": {
            "dataset": "DenseUAV",
            "description": "Dense urban UAV self-positioning benchmark with retrieval and spatial distance matching metrics.",
            "official_protocols": [
                {
                    "name": "Drone-to-Satellite",
                    "columns": ["R@1", "R@5", "R@top1", "AP", "SDM@1", "SDM@3", "SDM@5"],
                    "primary_sort_metric": "R@1",
                    "higher_is_better": True,
                }
            ],
            "inclusion_rules": "Use the final model on the original DenseUAV self-positioning benchmark. Exclude scale/altitude-only variants and non-original augmented versions.",
        },
        "UAV-VisLoc": {
            "dataset": "UAV-VisLoc",
            "description": "UAV visual localization benchmark; protocols differ across papers and should not be mixed unless the split and unit match.",
            "official_protocols": [
                {
                    "name": "Protocol-specific localization",
                    "columns": ["Mean Error (m)", "Median Error (m)", "Success Rate", "R@1", "AP"],
                    "primary_sort_metric": "Mean Error (m)",
                    "higher_is_better": False,
                }
            ],
            "inclusion_rules": "Include only clearly stated main protocol results and keep protocol names explicit. Do not mix incompatible map splits or units.",
        },
        "GTA-UAV": {
            "dataset": "GTA-UAV",
            "description": "Game4Loc/GTA-UAV benchmark with Cross-Area and Same-Area retrieval/localization metrics.",
            "official_protocols": [
                {
                    "name": "Cross-Area / Same-Area",
                    "columns": ["Cross R@1", "Cross R@5", "Cross AP", "Cross SDM@3", "Cross Dis@1", "Same R@1", "Same R@5", "Same AP", "Same SDM@3", "Same Dis@1"],
                    "primary_sort_metric": "Cross R@1",
                    "higher_is_better": True,
                }
            ],
            "inclusion_rules": "Use only final method results on the official Cross-Area and Same-Area settings.",
        },
    }


def cmd_specs(args: argparse.Namespace) -> None:
    require_env(["DEEPSEEK_API_KEY"])
    datasets = args.datasets or DEFAULT_DATASETS
    specs = read_yaml(SPEC_PATH, {}) or {}
    seed_cfg = read_yaml(ROOT / "configs" / "seed_datasets.yml", {}) or {}
    seeds = seed_cfg.get("seeds") or []
    candidate_papers = select_papers(datasets, include_surveys=True)

    for dataset in datasets:
        if dataset in specs and not args.force:
            log(f"DeepSeek spec skipped, cached: {dataset}")
            continue
        related_seed = [s for s in seeds if norm_key(s.get("dataset")) == norm_key(dataset)]
        related_papers = []
        for paper in candidate_papers:
            if dataset in paper.get("_leaderboard_datasets", []):
                related_papers.append(
                    {
                        "title": paper.get("title"),
                        "year": paper.get("year"),
                        "abstract": clean(paper.get("abstract"))[:1500],
                        "summary": clean((paper.get("summary") or {}).get("summary_en"))[:1200],
                        "reported_results": (paper.get("summary") or {}).get("reported_results") or [],
                    }
                )
            if len(related_papers) >= 8:
                break
        system = (
            "You are defining official leaderboard table specifications for an English UAV cross-view geo-localization repository. "
            "Output valid JSON only. Be conservative and do not create protocols from ablation, weather robustness, transfer, or auxiliary experiments."
        )
        user = f"""
Dataset: {dataset}

Seed/reference metadata:
{json.dumps(related_seed, ensure_ascii=False, indent=2)}

Representative papers that mention this dataset:
{json.dumps(related_papers, ensure_ascii=False, indent=2)}

Task:
1. Identify the official/main benchmark protocol(s) and metrics used by the dataset paper or official benchmark.
2. Propose a GitHub Markdown wide-table layout similar to: method/training-setting as the first column and metric columns across the row.
3. Choose a default sorting metric and direction.
4. State strict inclusion/exclusion rules.

Return JSON with this exact shape:
{{
  "dataset": string,
  "description": string,
  "official_protocols": [
    {{
      "name": string,
      "columns": array of metric column names,
      "primary_sort_metric": string,
      "higher_is_better": boolean
    }}
  ],
  "inclusion_rules": string,
  "exclusion_rules": array of strings,
  "dataset_paper_summary": string,
  "needs_manual_review": boolean
}}
""".strip()
        log(f"DeepSeek spec: {dataset}")
        specs[dataset] = deepseek_json(system, user, max_tokens=6000)
        write_yaml(SPEC_PATH, specs)
    log(f"wrote specs: {SPEC_PATH}")


def evidence_for_paper(paper: dict, use_pdf: bool, fulltext_record: Optional[dict] = None) -> str:
    pieces = [
        f"Title: {paper.get('title', '')}",
        f"Year: {paper.get('year', '')}",
        f"Venue: {paper.get('venue', '')}",
        "Abstract:",
        clean(paper.get("abstract"))[:5000],
        "Existing summary:",
        clean((paper.get("summary") or {}).get("summary_en"))[:3500],
        "Existing reported results:",
        json.dumps((paper.get("summary") or {}).get("reported_results") or [], ensure_ascii=False)[:3500],
        "Existing extracted metrics:",
        json.dumps((paper.get("summary") or {}).get("leaderboard_metrics") or [], ensure_ascii=False)[:6000],
    ]
    if use_pdf:
        full_text = (fulltext_record or {}).get("fulltext") or auto.fetch_pdf_text_placeholder(paper)
        pieces.extend(["Full-text and table evidence:", full_text[:120000]])
    return "\n\n".join(pieces)


def review_one_paper(paper: dict, specs: Dict[str, dict], use_pdf: bool, fulltext_record: Optional[dict] = None) -> dict:
    datasets = paper.get("_leaderboard_datasets") or []
    relevant_specs = {ds: specs.get(ds) or default_dataset_specs().get(ds) for ds in datasets}
    system = (
        "You are a strict leaderboard auditor for an English UAV cross-view geo-localization repository. "
        "Review exactly one paper. Extract only the paper's final flagship method results on official dataset protocols. "
        "Never include ablations, component variants, backbone sweeps, weather/corruption subsets, transfer-only results, TTA, re-ranking, or auxiliary protocol rows. "
        "If a paper table says 'Ours', replace it with the real method name from the paper title or method description; if the real method name is uncertain, exclude the row. "
        "Output valid JSON only."
    )
    user = f"""
Datasets to audit for this paper: {', '.join(datasets)}

Dataset leaderboard specifications:
{json.dumps(relevant_specs, ensure_ascii=False, indent=2)}

Paper evidence:
{evidence_for_paper(paper, use_pdf, fulltext_record)}

Return JSON with this exact shape:
{{
  "paper_id": "{paper_id(paper)}",
  "paper_title": string,
  "method_name": string,
  "overall_decision": "include" | "exclude" | "partial",
  "overall_reason": string,
  "dataset_results": [
    {{
      "dataset": string,
      "protocol": string,
      "include": boolean,
      "method": string,
      "training_setting": string,
      "sort_metric": string,
      "sort_value": number or null,
      "metrics": object mapping exact leaderboard column names to string values,
      "source": string,
      "notes": string,
      "exclusion_reason": string
    }}
  ],
  "dropped_rows": array of strings,
  "needs_manual_review": boolean
}}

Rules:
- `metrics` keys must match the dataset spec columns whenever possible.
- Use only one row per paper per dataset/protocol unless the official dataset protocol explicitly separates Cross/Same or altitude bands in one row.
- Do not output any method value containing only "Ours" or "Our method".
- Prefer the method acronym/name such as DINO-GFSA, SkyPart, CEUSP, etc.
- If DINO-GFSA reports DenseUAV official results, include its final DenseUAV row.
""".strip()
    obj = minimax_json(system, user, max_tokens=7000)
    obj.setdefault("paper_id", paper_id(paper))
    obj.setdefault("paper_title", paper.get("title"))
    obj.setdefault("dataset_results", [])
    obj["reviewed_at"] = dt.datetime.now().isoformat(timespec="seconds")
    obj["review_model"] = os.getenv("MINIMAX_MODEL", "MiniMax-M3")
    obj["datasets_requested"] = datasets
    return obj


def load_reviews() -> Dict[str, dict]:
    data = read_yaml(REVIEW_PATH, []) or []
    if isinstance(data, dict):
        return data
    return {clean(row.get("paper_id")): row for row in data if row.get("paper_id")}


def save_reviews(reviews: Dict[str, dict]) -> None:
    rows = list(reviews.values())
    rows.sort(key=lambda r: (r.get("paper_title") or ""))
    write_yaml(REVIEW_PATH, rows)


def cmd_review(args: argparse.Namespace) -> None:
    require_env(["MINIMAX_API_KEY"])
    if args.require_accessible_fulltext:
        require_env(["MINIMAX_API_KEY"])
    specs = read_yaml(SPEC_PATH, {}) or {}
    defaults = default_dataset_specs()
    for dataset, spec in defaults.items():
        specs.setdefault(dataset, spec)
    datasets = args.datasets or DEFAULT_DATASETS
    papers = select_papers(datasets, include_surveys=False)
    if args.title_regex:
        pattern = re.compile(args.title_regex, flags=re.I)
        papers = [p for p in papers if pattern.search(p.get("title") or "")]
    reviews = load_reviews()
    total = len(papers)
    limit = args.limit if args.limit and args.limit > 0 else total
    done = 0
    for idx, paper in enumerate(papers[:limit], 1):
        pid = paper_id(paper)
        if pid in reviews and not args.force:
            continue
        log(f"MiniMax-M3 review [{idx}/{total}]: {paper.get('title', '')[:110]}")
        try:
            fulltext_record = None
            if args.require_accessible_fulltext:
                fulltext_record = discover_accessible_fulltext_with_timeout(
                    paper,
                    force=args.force_fulltext,
                    paper_timeout=args.paper_timeout,
                )
                if fulltext_record.get("status") != "accessible":
                    reviews[pid] = {
                        "paper_id": pid,
                        "paper_title": paper.get("title"),
                        "overall_decision": "skipped_no_fulltext",
                        "overall_reason": fulltext_record.get("reason") or "No accessible full text found",
                        "dataset_results": [],
                        "dropped_rows": [],
                        "reviewed_at": dt.datetime.now().isoformat(timespec="seconds"),
                        "datasets_requested": paper.get("_leaderboard_datasets") or [],
                        "fulltext_access": {k: v for k, v in fulltext_record.items() if k != "fulltext"},
                        "needs_manual_review": True,
                    }
                    log(f"skipped MiniMax: no accessible full text for {paper.get('title', '')[:100]}")
                    save_reviews(reviews)
                    done += 1
                    if args.progress_every and done % args.progress_every == 0:
                        log(f"review progress: new_reviews={done}, cached_or_total={len(reviews)}")
                    continue
            reviews[pid] = review_one_paper(paper, specs, use_pdf=args.use_pdf, fulltext_record=fulltext_record)
        except Exception as e:
            reviews[pid] = {
                "paper_id": pid,
                "paper_title": paper.get("title"),
                "overall_decision": "error",
                "overall_reason": str(e),
                "dataset_results": [],
                "reviewed_at": dt.datetime.now().isoformat(timespec="seconds"),
                "datasets_requested": paper.get("_leaderboard_datasets") or [],
                "needs_manual_review": True,
            }
            log(f"review failed: {e}")
        save_reviews(reviews)
        done += 1
        if args.progress_every and done % args.progress_every == 0:
            log(f"review progress: new_reviews={done}, cached_or_total={len(reviews)}")
    log(f"review stage complete: new_reviews={done}, review_cache={REVIEW_PATH}")


def cmd_discover(args: argparse.Namespace) -> None:
    require_env(["MINIMAX_API_KEY"])
    datasets = args.datasets or DEFAULT_DATASETS
    papers = select_papers(datasets, include_surveys=False)
    if args.title_regex:
        pattern = re.compile(args.title_regex, flags=re.I)
        papers = [p for p in papers if pattern.search(p.get("title") or "")]
    total = len(papers)
    limit = args.limit if args.limit and args.limit > 0 else total
    done = 0
    for idx, paper in enumerate(papers[:limit], 1):
        log(f"full-text discovery [{idx}/{total}]: {paper.get('title', '')[:110]}")
        discover_accessible_fulltext_with_timeout(paper, force=args.force, paper_timeout=args.paper_timeout)
        done += 1
        if args.progress_every and done % args.progress_every == 0:
            cache = load_fulltext_cache()
            counts = Counter(row.get("status", "unknown") for row in cache.values())
            log(f"discovery progress: checked={done}, cache={len(cache)}, status={dict(counts)}")
    cache = load_fulltext_cache()
    counts = Counter(row.get("status", "unknown") for row in cache.values())
    log(f"discovery complete: checked={done}, cache={len(cache)}, status={dict(counts)}")


def cmd_test_fulltext(args: argparse.Namespace) -> None:
    require_env(["MINIMAX_API_KEY"])
    datasets = args.datasets or DEFAULT_DATASETS
    papers = select_papers(datasets, include_surveys=False)
    pattern = re.compile(args.title_regex, flags=re.I)
    matches = [p for p in papers if pattern.search(p.get("title") or "")]
    if not matches:
        raise RuntimeError(f"No paper matched --title-regex {args.title_regex!r}")
    paper = matches[0]
    log(f"MiniMax full-text smoke test: {paper.get('title', '')[:140]}")
    record = discover_accessible_fulltext_with_timeout(
        paper,
        force=args.force,
        paper_timeout=args.paper_timeout,
    )
    attempted = record.get("attempted") or []
    compact = {
        "paper_id": record.get("paper_id"),
        "paper_title": record.get("paper_title"),
        "status": record.get("status"),
        "selected_url": record.get("selected_url"),
        "kind": record.get("kind"),
        "chars": record.get("chars"),
        "reason": record.get("reason"),
        "attempt_count": len(attempted),
        "attempted": [
            {
                "url": item.get("url"),
                "kind": item.get("kind"),
                "ok": item.get("ok"),
                "chars": item.get("chars"),
                "content_type": item.get("content_type"),
                "error": item.get("error"),
            }
            for item in attempted[:12]
        ],
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


def cmd_validate(args: argparse.Namespace) -> None:
    errors: List[str] = []
    warnings: List[str] = []
    specs = read_yaml(SPEC_PATH, {}) or {}
    reviews = load_reviews()
    included, excluded = build_rows(reviews, specs)

    dense_methods = {row.get("method") for row in included if row.get("dataset") == "DenseUAV"}
    if "DINO-GFSA" not in dense_methods:
        errors.append("DINO-GFSA is missing from the DenseUAV included rows.")

    ambiguous = [
        row
        for row in included
        if re.fullmatch(r"(?i)(ours?|our method|proposed|the proposed method)(?:\s*\([^)]*\))?", clean(row.get("method")))
    ]
    if ambiguous:
        errors.append(f"Included rows still contain ambiguous method names: {len(ambiguous)}")

    non_metric_keys = {"method", "methodname", "methodtrainingsetting"}
    for dataset, spec in specs.items():
        for protocol in protocol_specs_for_dataset(spec):
            bad_columns = [c for c in protocol.get("columns") or [] if canonical_metric_key(clean(c)) in non_metric_keys]
            if bad_columns:
                warnings.append(f"{dataset} / {protocol.get('name')}: spec contains non-metric column(s) filtered during output: {bad_columns}")

    dense_page = ROOT / "leaderboards" / "denseuav.md"
    if dense_page.exists():
        dense_text = dense_page.read_text(encoding="utf-8")
        if "| Method / Training Setting | Method |" in dense_text:
            errors.append("DenseUAV page still has a duplicate Method metric column.")
        if "DINO-GFSA" not in dense_text:
            errors.append("DenseUAV page does not mention DINO-GFSA.")
        if "Rows: **0**" in dense_text:
            errors.append("DenseUAV page still reports zero rows.")
    else:
        errors.append("DenseUAV page is missing.")

    for page in (ROOT / "leaderboards").glob("*.md"):
        text = page.read_text(encoding="utf-8")
        if "| Method / Training Setting | Method / Training Setting |" in text:
            errors.append(f"{page.name} has a duplicate Method / Training Setting metric column.")

    access_cache = load_fulltext_cache()
    status_counts = Counter(row.get("status", "unknown") for row in access_cache.values())
    review_counts = Counter(row.get("overall_decision", "unknown") for row in reviews.values())
    summary = {
        "included_rows": len(included),
        "excluded_rows": len(excluded),
        "fulltext_cache": dict(status_counts),
        "review_cache": dict(review_counts),
        "warnings": warnings,
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


def sanitize_method(method: str, fallback: str) -> str:
    method = clean(method)
    if not method or re.fullmatch(r"(?i)(ours?|our method|proposed|the proposed method)(?:\s*\([^)]*\))?", method):
        return clean(fallback)
    method = re.sub(r"(?i)\bours\b", clean(fallback) or "Proposed method", method).strip()
    return method


def canonical_metric_key(text: str) -> str:
    text = clean(text).lower()
    text = text.replace("recall@", "r@")
    text = text.replace("recall @", "r@")
    text = text.replace("top-1", "r@1")
    text = text.replace("top1", "r@1")
    text = text.replace("average precision", "ap")
    return re.sub(r"[^a-z0-9@]+", "", text)


def metric_value(metrics: Dict[str, Any], column: str) -> str:
    if not metrics:
        return ""
    wanted = canonical_metric_key(column)
    for key, value in metrics.items():
        if canonical_metric_key(key) == wanted:
            return clean(value)
    # Soft matching for columns such as "150m R@1".
    wanted_parts = [p for p in re.split(r"[^a-zA-Z0-9@]+", column.lower()) if p]
    for key, value in metrics.items():
        hay = canonical_metric_key(key)
        if all(canonical_metric_key(part) in hay for part in wanted_parts):
            return clean(value)
    return ""


def metric_columns(columns: Iterable[Any]) -> List[str]:
    ignored = {
        "method",
        "methodname",
        "methodtrainingsetting",
        "paper",
        "source",
        "verified",
        "notes",
        "training",
        "trainingsetting",
        "sortmetric",
        "sortvalue",
    }
    out: List[str] = []
    seen: set[str] = set()
    for column in columns or []:
        text = clean(column)
        key = canonical_metric_key(text)
        if not text or key in ignored or key in seen:
            continue
        seen.add(key)
        out.append(text)
    return out


def protocol_tokens(text: Any) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", clean(text).lower()))
    aliases = {
        "drone": "uav",
        "uav": "uav",
        "satellite": "satellite",
        "sat": "satellite",
        "retrieval": "retrieval",
        "matching": "retrieval",
        "localization": "localization",
        "geolocalization": "localization",
        "geo": "localization",
    }
    return {aliases.get(token, token) for token in tokens if token not in {"to", "2", "view", "cross", "official", "protocol"}}


def protocol_matches(row_protocol: Any, spec_protocol: Any) -> bool:
    row_key = norm_key(row_protocol)
    spec_key = norm_key(spec_protocol)
    if row_key == spec_key:
        return True
    if row_key and spec_key and (row_key in spec_key or spec_key in row_key):
        return True
    row_tokens = protocol_tokens(row_protocol)
    spec_tokens = protocol_tokens(spec_protocol)
    if not row_tokens or not spec_tokens:
        return False
    overlap = row_tokens & spec_tokens
    return len(overlap) >= min(len(row_tokens), len(spec_tokens), 2)


def include_result(row: dict) -> bool:
    if not row.get("include"):
        return False
    method = clean(row.get("method"))
    if not method or re.fullmatch(r"(?i)(ours?|our method|proposed|the proposed method)(?:\s*\([^)]*\))?", method):
        return False
    joined = " ".join([clean(row.get("protocol")), clean(row.get("training_setting")), clean(row.get("notes")), clean(row.get("source"))]).lower()
    banned_phrases = [
        "ablation",
        "without ",
        "w/o",
        "module",
        "backbone sweep",
        "variant",
        "weather robustness",
        "corruption",
        "transfer-only",
        "zero-shot transfer",
    ]
    if any(term in joined for term in banned_phrases):
        return False
    banned_words = ["fog", "snow", "rain", "dark"]
    if any(re.search(rf"\b{re.escape(term)}\b", joined) for term in banned_words):
        return False
    for term in ["tta", "test-time augmentation", "re-ranking", "reranking"]:
        pos = joined.find(term)
        if pos < 0:
            continue
        prefix = joined[max(0, pos - 32) : pos]
        if re.search(r"(?:\bno\b|\bnot\b|\bwithout\b|\bw/o\b)[\w\s,;/+-]*$", prefix):
            continue
        return False
    return True


def build_rows(reviews: Dict[str, dict], specs: Dict[str, dict]) -> Tuple[List[dict], List[dict]]:
    included: List[dict] = []
    excluded: List[dict] = []
    for review in reviews.values():
        title = clean(review.get("paper_title"))
        fallback_method = clean(review.get("method_name")) or title
        for row in review.get("dataset_results") or []:
            dataset = clean(row.get("dataset"))
            protocol = clean(row.get("protocol")) or "Main"
            method = sanitize_method(row.get("method"), fallback_method)
            base = {
                "dataset": dataset,
                "protocol": protocol,
                "method": method,
                "training_setting": clean(row.get("training_setting")),
                "paper": title,
                "source": clean(row.get("source")),
                "notes": clean(row.get("notes")),
                "verified": "false",
                "review_status": clean(review.get("overall_decision")),
                "sort_metric": clean(row.get("sort_metric")),
                "sort_value": row.get("sort_value"),
                "metrics": row.get("metrics") or {},
                "exclusion_reason": clean(row.get("exclusion_reason") or review.get("overall_reason")),
            }
            if include_result(row) and dataset in specs:
                included.append(base)
            else:
                excluded.append(base)
    # Deduplicate by dataset/protocol/method/paper.
    seen = set()
    unique: List[dict] = []
    for row in included:
        key = (norm_key(row["dataset"]), norm_key(row["protocol"]), norm_key(row["method"]), norm_key(row["paper"]))
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique, excluded


def sort_rows(rows: List[dict], protocol_spec: dict, sort_metric: Optional[str]) -> List[dict]:
    metric = sort_metric or protocol_spec.get("primary_sort_metric") or ""
    higher = bool(protocol_spec.get("higher_is_better", True))

    def score(row: dict) -> Tuple[int, float, str]:
        value = row.get("sort_value")
        if value is None and metric:
            value = metric_value(row.get("metrics") or {}, metric)
        num = parse_float(value)
        if num is None:
            return (1, 0.0, clean(row.get("method")).lower())
        return (0, -num if higher else num, clean(row.get("method")).lower())

    return sorted(rows, key=score)


def protocol_specs_for_dataset(spec: dict) -> List[dict]:
    protocols = spec.get("official_protocols") or []
    if not protocols:
        protocols = [{"name": "Main", "columns": [], "primary_sort_metric": "", "higher_is_better": True}]
    return protocols


def rows_for_protocol(dataset_rows: List[dict], protocol: dict, all_protocols: List[dict]) -> List[dict]:
    name = clean(protocol.get("name")) or "Main"
    exact = [r for r in dataset_rows if norm_key(r["protocol"]) == norm_key(name)]
    if exact:
        return exact
    matched = [r for r in dataset_rows if protocol_matches(r["protocol"], name)]
    if matched:
        return matched
    if len(all_protocols) == 1:
        return dataset_rows
    return []


def write_dataset_page(dataset: str, spec: dict, rows: List[dict], sort_metric: Optional[str]) -> None:
    slug = {
        "University-1652": "university1652",
        "SUES-200": "sues200",
        "DenseUAV": "denseuav",
        "UAV-VisLoc": "uav_visloc",
        "GTA-UAV": "gta_uav",
        "Game4Loc": "gta_uav",
        "World-UAV": "world_uav",
        "UAV-GeoLoc": "world_uav",
        "Nardo-Air": "nardo_air",
    }.get(dataset, re.sub(r"[^a-z0-9]+", "_", dataset.lower()).strip("_"))
    path = ROOT / "leaderboards" / f"{slug}.md"
    lines = [
        f"# {dataset}",
        "",
        clean(spec.get("description")),
        "",
        "Only final flagship method results on the official dataset protocol are listed. Automatically reviewed rows are marked `verified=false` until manual checking.",
        "",
    ]
    dataset_rows = [r for r in rows if r["dataset"] == dataset]
    protocols = protocol_specs_for_dataset(spec)
    for protocol in protocols:
        name = clean(protocol.get("name")) or "Main"
        columns = metric_columns(protocol.get("columns") or [])
        group = rows_for_protocol(dataset_rows, protocol, protocols)
        group = sort_rows(group, protocol, sort_metric)
        sort_name = sort_metric or protocol.get("primary_sort_metric") or "method"
        direction = "descending" if protocol.get("higher_is_better", True) else "ascending"
        lines += [
            f"## {name}",
            "",
            f"Rows: **{len(group)}**. Default sort: **{md_escape(sort_name)}** ({direction}).",
            "",
        ]
        header = ["Method / Training Setting"] + columns + ["Paper", "Source", "Verified", "Notes"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] + ["---:"] * len(columns) + ["---", "---", "---", "---"]) + " |")
        for row in group:
            method_cell = md_escape(row["method"])
            if row.get("training_setting"):
                method_cell += f"<br><sub>{md_escape(row['training_setting'])}</sub>"
            metric_cells = [md_escape(metric_value(row.get("metrics") or {}, col) or "-") for col in columns]
            cells = [
                method_cell,
                *metric_cells,
                md_escape(row["paper"]),
                md_escape(row["source"]),
                md_escape(row["verified"]),
                md_escape(row["notes"] or "-"),
            ]
            lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    write_text(path, "\n".join(lines))


def write_outputs(included: List[dict], excluded: List[dict], specs: Dict[str, dict], sort_metric: Optional[str]) -> None:
    fieldnames = [
        "dataset",
        "protocol",
        "method",
        "training_setting",
        "paper",
        "source",
        "verified",
        "sort_metric",
        "sort_value",
        "metrics_json",
        "notes",
    ]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in included:
            writer.writerow(
                {
                    "dataset": row["dataset"],
                    "protocol": row["protocol"],
                    "method": row["method"],
                    "training_setting": row["training_setting"],
                    "paper": row["paper"],
                    "source": row["source"],
                    "verified": row["verified"],
                    "sort_metric": row["sort_metric"],
                    "sort_value": row["sort_value"],
                    "metrics_json": json.dumps(row.get("metrics") or {}, ensure_ascii=False, sort_keys=True),
                    "notes": row["notes"],
                }
            )

    by_dataset = Counter(row["dataset"] for row in included)
    for dataset, spec in specs.items():
        if dataset in DEFAULT_DATASETS or by_dataset.get(dataset):
            write_dataset_page(dataset, spec, included, sort_metric)

    summary = [
        "# Leaderboards",
        "",
        "Leaderboard pages use wide tables following each dataset's official protocol. Rows are generated from DeepSeek dataset specifications and MiniMax-M3 per-paper reviews.",
        "",
        "Only final flagship method results are included. Ablations, variants, transfer-only results, weather/corruption subsets, TTA, re-ranking, and rows named only `Ours` are excluded.",
        "",
        "GitHub Markdown does not support interactive table sorting. The generator sorts each table by the configured primary metric, and can be rerun with `--sort-metric <metric>`.",
        "",
        "| Dataset | Page | Included Rows | Default Sort |",
        "|---|---|---:|---|",
    ]
    for dataset in DEFAULT_DATASETS:
        if dataset not in specs and dataset not in by_dataset:
            continue
        slug = {
            "University-1652": "university1652.md",
            "SUES-200": "sues200.md",
            "DenseUAV": "denseuav.md",
            "UAV-VisLoc": "uav_visloc.md",
            "GTA-UAV": "gta_uav.md",
            "Game4Loc": "gta_uav.md",
            "World-UAV": "world_uav.md",
            "UAV-GeoLoc": "world_uav.md",
            "Nardo-Air": "nardo_air.md",
        }.get(dataset, f"{dataset.lower()}.md")
        spec = specs.get(dataset) or {}
        proto = (spec.get("official_protocols") or [{}])[0]
        summary.append(f"| {md_escape(dataset)} | [{slug}]({slug}) | {by_dataset.get(dataset, 0)} | {md_escape(proto.get('primary_sort_metric') or '-')} |")
    summary += [
        f"| Not included | [not_included.md](not_included.md) | {len(excluded)} | Manual review |",
        "| Sources | [sources.md](sources.md) | - | - |",
        "",
    ]
    write_text(ROOT / "leaderboards" / "leaderboard_summary.md", "\n".join(summary))

    not_lines = [
        "# Not Included",
        "",
        "Rows below were reviewed but excluded from official leaderboard tables because they are ablations, variants, transfer-only settings, ambiguous `Ours` rows, unsupported datasets, or protocol-mismatched results.",
        "",
        "| Dataset | Protocol | Method | Paper | Reason |",
        "|---|---|---|---|---|",
    ]
    for row in excluded:
        not_lines.append(
            f"| {md_escape(row.get('dataset'))} | {md_escape(row.get('protocol'))} | {md_escape(row.get('method') or '-')} | {md_escape(row.get('paper'))} | {md_escape(row.get('exclusion_reason') or row.get('notes') or 'Excluded by leaderboard rules')} |"
        )
    not_lines.append("")
    write_text(ROOT / "leaderboards" / "not_included.md", "\n".join(not_lines))

    source_lines = [
        "# Leaderboard Sources",
        "",
        "The rebuilt leaderboards are generated from:",
        "",
        "| Artifact | Role |",
        "|---|---|",
        "| `data/internal/leaderboard_dataset_specs.yml` | DeepSeek-generated dataset protocol and metric specifications. |",
        "| `data/internal/leaderboard_reviews.yml` | MiniMax-M3 one-paper-at-a-time review cache. |",
        "| `data/leaderboards.csv` | Machine-readable wide-row leaderboard export. |",
        "| `data/backfill_candidates.yml` | Original candidate records and prior extraction evidence. |",
        "",
        "## Included Row Counts",
        "",
        "| Dataset | Rows |",
        "|---|---:|",
    ]
    for dataset, count in sorted(by_dataset.items()):
        source_lines.append(f"| {md_escape(dataset)} | {count} |")
    source_lines += ["", "## Excluded Row Counts", "", "| Dataset | Rows |", "|---|---:|"]
    for dataset, count in sorted(Counter(row.get("dataset") or "Unknown" for row in excluded).items()):
        source_lines.append(f"| {md_escape(dataset)} | {count} |")
    source_lines.append("")
    write_text(ROOT / "leaderboards" / "sources.md", "\n".join(source_lines))

    availability = [
        "# Dataset Availability Rules",
        "",
        "A dataset is included in the public leaderboard only when it has a public or otherwise clearly accessible benchmark release and a reproducible protocol. Paper-private datasets, unverified new datasets, auxiliary transfer settings, and robustness-only variants are not mixed into the official tables.",
        "",
        "| Dataset / Benchmark | Status | Leaderboard Handling | Notes |",
        "|---|---|---|---|",
        "| University-1652 | Public benchmark | Included | Standard UAV/satellite retrieval protocols. |",
        "| SUES-200 | Public academic benchmark | Included | Altitude-specific protocol; transfer-only rows stay separate or excluded. |",
        "| DenseUAV | Public benchmark | Included | Original self-positioning metrics only; augmented/scale-only variants are excluded. |",
        "| GTA-UAV / Game4Loc | Public benchmark | Included when official Cross/Same protocol results are available | Ablations from the dataset paper are not used as algorithm leaderboard rows. |",
        "| UAV-VisLoc | Public benchmark | Included with protocol labels | Different map/split protocols are not mixed. |",
        "| World-UAV / UAV-GeoLoc | Public benchmark | Included when official results are available | No reviewed rows may appear if the run found no main-protocol values. |",
        "| Nardo-Air | Public related benchmark | Included when protocol-compatible results are available | Aerial localization related; keep source/protocol explicit. |",
        "| Other new datasets | Pending | Not included by default | Requires public release evidence and a clear benchmark protocol. |",
        "",
    ]
    write_text(ROOT / "leaderboards" / "dataset_availability.md", "\n".join(availability))

    report = [
        "# Leaderboard Rebuild Report",
        "",
        f"Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`",
        "",
        f"- Included rows: **{len(included)}**",
        f"- Excluded rows: **{len(excluded)}**",
        f"- Sort override: `{sort_metric or 'dataset default'}`",
        "",
        "## Included Rows by Dataset",
        "",
        "| Dataset | Rows |",
        "|---|---:|",
    ]
    for dataset, count in sorted(by_dataset.items()):
        report.append(f"| {md_escape(dataset)} | {count} |")
    report += ["", "## Excluded Rows by Dataset", "", "| Dataset | Rows |", "|---|---:|"]
    for dataset, count in sorted(Counter(row.get("dataset") or "Unknown" for row in excluded).items()):
        report.append(f"| {md_escape(dataset)} | {count} |")
    report.append("")
    write_text(REPORT_PATH, "\n".join(report))


def cmd_build(args: argparse.Namespace) -> None:
    specs = read_yaml(SPEC_PATH, {}) or {}
    defaults = default_dataset_specs()
    for dataset, spec in defaults.items():
        specs.setdefault(dataset, spec)
    reviews = load_reviews()
    included, excluded = build_rows(reviews, specs)
    write_outputs(included, excluded, specs, args.sort_metric)
    log(f"built leaderboards: included={len(included)}, excluded={len(excluded)}")


def cmd_list(args: argparse.Namespace) -> None:
    datasets = args.datasets or DEFAULT_DATASETS
    papers = select_papers(datasets, include_surveys=False)
    counts = Counter()
    for paper in papers:
        for dataset in paper.get("_leaderboard_datasets") or []:
            counts[dataset] += 1
    print(json.dumps({"paper_count": len(papers), "by_dataset": counts, "titles": [p.get("title") for p in papers]}, ensure_ascii=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rebuild wide-table UAV-CVGL leaderboards")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list papers selected for leaderboard review")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("specs", help="use DeepSeek to generate dataset leaderboard specs")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_specs)

    p = sub.add_parser("review", help="use MiniMax-M3 to review one paper at a time")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.add_argument("--use-pdf", action="store_true")
    p.add_argument("--require-accessible-fulltext", action="store_true", help="use MiniMax built-in search discovery and skip review when no PDF/HTML text is accessible")
    p.add_argument("--force-fulltext", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--title-regex", default="")
    p.add_argument("--progress-every", type=int, default=25)
    p.add_argument("--paper-timeout", type=int, default=0, help="per-paper wall-clock timeout in seconds; defaults to LEADERBOARD_DISCOVERY_TIMEOUT or 300")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("discover", help="MiniMax built-in search full-text URL discovery and access validation only")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.add_argument("--force", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--title-regex", default="")
    p.add_argument("--progress-every", type=int, default=25)
    p.add_argument("--paper-timeout", type=int, default=0, help="per-paper wall-clock timeout in seconds; defaults to LEADERBOARD_DISCOVERY_TIMEOUT or 300")
    p.set_defaults(func=cmd_discover)

    p = sub.add_parser("test-fulltext", help="smoke test MiniMax built-in search on one previously inaccessible paper")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.add_argument("--title-regex", default="Modern Backbone for Efficient Geo-localization")
    p.add_argument("--force", action="store_true")
    p.add_argument("--paper-timeout", type=int, default=120, help="per-paper wall-clock timeout in seconds")
    p.set_defaults(func=cmd_test_fulltext)

    p = sub.add_parser("validate", help="validate generated leaderboard invariants without calling external APIs")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("build", help="build CSV and Markdown leaderboards from cached reviews")
    p.add_argument("--sort-metric", default="", help="optional metric column to sort tables by instead of dataset defaults")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("all", help="run specs, review, and build")
    p.add_argument("--datasets", nargs="*", default=DEFAULT_DATASETS)
    p.add_argument("--use-pdf", action="store_true")
    p.add_argument("--require-accessible-fulltext", action="store_true")
    p.add_argument("--force-specs", action="store_true")
    p.add_argument("--force-review", action="store_true")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--sort-metric", default="")
    p.add_argument("--progress-every", type=int, default=25)
    p.add_argument("--paper-timeout", type=int, default=0, help="per-paper wall-clock timeout in seconds; defaults to LEADERBOARD_DISCOVERY_TIMEOUT or 300")

    def run_all(args: argparse.Namespace) -> None:
        spec_args = argparse.Namespace(datasets=args.datasets, force=args.force_specs)
        cmd_specs(spec_args)
        review_args = argparse.Namespace(
            datasets=args.datasets,
            use_pdf=args.use_pdf,
            require_accessible_fulltext=args.require_accessible_fulltext,
            force_fulltext=False,
            force=args.force_review,
            limit=args.limit,
            title_regex="",
            progress_every=args.progress_every,
            paper_timeout=args.paper_timeout,
        )
        cmd_review(review_args)
        build_args = argparse.Namespace(sort_metric=args.sort_metric)
        cmd_build(build_args)

    p.set_defaults(func=run_all)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
