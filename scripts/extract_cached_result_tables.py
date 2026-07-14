#!/usr/bin/env python3
"""Extract and render candidate result pages from readable cached papers."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import fitz


ROOT = Path(__file__).resolve().parents[1]
READABLE_CSV = ROOT / "data" / "reports" / "cache_pdf_readable.csv"
INDEX_CSV = ROOT / "data" / "reports" / "cache_result_table_index.csv"
TABLE_DIR = ROOT / "tmp" / "pdfs" / "cache_result_tables"
IMAGE_DIR = ROOT / "tmp" / "pdfs" / "cache_result_pages"


def page_numbers(raw: str) -> list[int]:
    return sorted({int(value.strip()) for value in raw.split(";") if value.strip()})


def safe_id(raw: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", raw).strip("_")


def find_pdftoppm(explicit: str | None) -> str:
    candidates = [
        explicit,
        r"C:\texlive\2025\bin\windows\pdftoppm.exe",
        shutil.which("pdftoppm"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise FileNotFoundError("pdftoppm was not found")


def choose_pdf(cache_dir: Path, raw: str) -> Path:
    for name in (item.strip() for item in raw.split(";") if item.strip()):
        path = cache_dir / name
        if path.exists():
            return path
    raise FileNotFoundError(raw)


def extract_tables(path: Path, pages: list[int]) -> dict[str, Any]:
    result: dict[str, Any] = {"pdf_file": path.name, "pages": {}}
    document = fitz.open(path)
    try:
        for page_no in pages:
            if not 1 <= page_no <= len(document):
                result["pages"][str(page_no)] = {"error": "page_out_of_range", "tables": []}
                continue
            page = document[page_no - 1]
            tables: list[list[list[str | None]]] = []
            try:
                for table in page.find_tables().tables:
                    tables.append(table.extract())
            except Exception as exc:  # PyMuPDF table detection can fail on malformed vectors.
                result["pages"][str(page_no)] = {"error": repr(exc), "tables": []}
                continue
            result["pages"][str(page_no)] = {"error": "", "tables": tables}
    finally:
        document.close()
    return result


def render_page(
    executable: str, path: Path, page_no: int, output: Path, dpi: int
) -> tuple[Path, str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = output.with_suffix("")
    completed = subprocess.run(
        [
            executable, "-f", str(page_no), "-l", str(page_no),
            "-r", str(dpi), "-png", "-singlefile", str(path), str(prefix),
        ],
        capture_output=True,
        timeout=180,
        check=False,
    )
    if completed.returncode != 0:
        return output, completed.stderr.decode("utf-8", errors="replace").strip()
    return output, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--pdftoppm")
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument("--all-readable", action="store_true")
    parser.add_argument("--reuse-existing", action="store_true")
    parser.add_argument("--skip-existing-renders", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    executable = find_pdftoppm(args.pdftoppm)
    with READABLE_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not args.all_readable:
        rows = [row for row in rows if row["currently_on_leaderboard"] == "false"]

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    index: list[dict[str, Any]] = []
    render_jobs: list[tuple[str, Path, int, Path]] = []

    for position, row in enumerate(rows, start=1):
        pages = page_numbers(row["comparison_pages"] or row["result_pages"])
        if not pages:
            index.append({
                "paper_id": row["paper_id"], "title": row["title"],
                "pages_checked": "", "tables_found": 0, "rendered_pages": 0,
                "extraction_errors": "", "status": "no_candidate_pages",
            })
            continue
        ident = safe_id(row["paper_id"].split(";", 1)[0])
        path = choose_pdf(args.cache_dir, row["pdf_file"])
        with fitz.open(path) as document:
            pages = [page for page in pages if 1 <= page <= len(document)]
        table_path = TABLE_DIR / f"{ident}.json"
        if args.reuse_existing and table_path.exists():
            result = json.loads(table_path.read_text(encoding="utf-8"))
        else:
            result = extract_tables(path, pages)
        result["pages"] = {
            page: value for page, value in result.get("pages", {}).items()
            if int(page) in pages
        }
        result.update({"paper_id": row["paper_id"], "title": row["title"]})
        table_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        table_count = sum(
            len(page.get("tables", [])) for page in result["pages"].values()
        )
        errors = [
            f"p{page}: {value['error']}" for page, value in result["pages"].items()
            if value.get("error")
        ]
        for page_no in pages:
            output = IMAGE_DIR / f"{ident}_p{page_no:03d}.png"
            if not (args.skip_existing_renders and output.exists()):
                render_jobs.append((ident, path, page_no, output))
        index.append({
            "paper_id": row["paper_id"],
            "title": row["title"],
            "pages_checked": "; ".join(map(str, pages)),
            "tables_found": table_count,
            "rendered_pages": len(pages),
            "extraction_errors": " | ".join(errors),
            "status": "tables_extracted" if table_count else "visual_review_required",
        })
        print(
            f"[{position}/{len(rows)}] {ident}: pages={pages}, tables={table_count}",
            flush=True,
        )

    render_errors: dict[tuple[str, int], str] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {
            executor.submit(render_page, executable, path, page, output, args.dpi):
            (ident, page)
            for ident, path, page, output in render_jobs
        }
        for future in as_completed(futures):
            ident, page = futures[future]
            _, error = future.result()
            if error:
                render_errors[(ident, page)] = error

    for row in index:
        ident = safe_id(str(row["paper_id"]).split(";", 1)[0])
        errors = [
            f"p{page}: {error}" for (paper, page), error in render_errors.items()
            if paper == ident
        ]
        if errors:
            row["extraction_errors"] = " | ".join(
                part for part in (str(row["extraction_errors"]), *errors) if part
            )
            row["status"] = "render_failed"

    fields = [
        "paper_id", "title", "pages_checked", "tables_found", "rendered_pages",
        "extraction_errors", "status",
    ]
    with INDEX_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(index)
    print(json.dumps({
        "papers": len(rows), "rendered_pages": len(render_jobs),
        "render_errors": len(render_errors), "index": str(INDEX_CSV),
    }, ensure_ascii=False, indent=2))
    return 1 if render_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
