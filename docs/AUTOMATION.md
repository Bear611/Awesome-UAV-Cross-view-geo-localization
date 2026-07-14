# Automation Guide

## Search Modes

### Full Backfill Search

This mode performs a full historical search. It is intended for manual runs.

Pipeline:

1. Keyword search with Semantic Scholar, OpenAlex, and arXiv.
2. Citation expansion with OpenAlex for benchmark seed papers.
3. Deduplication.
4. DeepSeek classification, one paper per API call.
5. MiniMax full-text-assisted English summary and category confirmation, one relevant paper per API call.
6. Merge parsed candidates into the official paper tables after manual review.

### Weekly Watch

This mode searches recent papers only. It can run in GitHub Actions and open a pull request.

The scheduled workflow runs every Monday and keeps the existing API chain unchanged:

1. Search Semantic Scholar, OpenAlex, and arXiv using the configured weekly keywords.
2. Filter all sources to the requested publication window and deduplicate against the cumulative candidate cache.
3. Use DeepSeek for abstract-level relevance classification.
4. For relevant candidates, resolve an accessible PDF/HTML full text and send the extracted text and table evidence to MiniMax-M3.
5. Generate a digest containing only candidates first discovered in the current ISO week.
6. Open or update the automated review pull request. Nothing is merged into the curated paper list automatically.

`SEMANTIC_SCHOLAR_API_KEY` is passed to the search step. If one search provider is temporarily unavailable, the other providers continue and the failure is recorded in `data/reports/weekly_search_report.md`. The run fails only when every search call fails or required LLM Secrets are missing.

Before searching, the workflow checks that `DEEPSEEK_API_KEY` and `MINIMAX_API_KEY` exist without printing their values. Dedicated Secrets remain the preferred configuration. For compatibility, one Repository Secret named `API` may contain both keys as a JSON/YAML mapping (for example, keys named `deepseek` and `minimax`) or as two `KEY=value` lines. Dedicated Secrets take precedence over the combined bundle. Empty optional repository variables no longer override the built-in defaults (`deepseek-chat`, `MiniMax-M3`, and `https://api.minimaxi.com/v1`).

Official benchmark splits such as SUES-200's 150m/200m/250m/300m protocols and GTA-UAV's Cross-Area protocol are allowed through the unverified result extractor. Ablations, backbone sweeps, corruption subsets, and TTA/re-ranking variants remain excluded.

### Weekly Watch Troubleshooting

- `Validate automation configuration` fails: add the missing repository Secret shown in the error.
- One provider is rate-limited: inspect the weekly search report; other providers should still complete.
- `Classify and summarize candidates` reports an item error: inspect `data/weekly_candidates.yml` and the uploaded diagnostics artifact. Successfully processed candidates are checkpointed after each paper.
- No weekly paper appears: a valid empty digest is generated when the current week has no newly parsed candidate; old candidates are not repeated.

## Why OpenAlex for Citation Expansion?

arXiv does not provide a citation graph API. OpenAlex supports citation expansion through `filter=cites:<OpenAlexWorkId>`, so it is used for benchmark citation search.

## Local Full Backfill Command

```cmd
cd /d D:\download\awesome-uav-cvgl-v0.1\awesome-uav-cvgl-v0.1

set DEEPSEEK_API_KEY=your_new_deepseek_key
set MINIMAX_API_KEY=your_new_minimax_key
set DEEPSEEK_MODEL=deepseek-chat
set MINIMAX_MODEL=MiniMax-M3
set MINIMAX_BASE_URL=https://api.minimaxi.com/v1
set MINIMAX_PDF_CHAR_LIMIT=120000
set MINIMAX_PDF_MAX_PAGES=80
set MINIMAX_PDF_MAX_BYTES=104857600
set MINIMAX_PDF_LANDING_MAX_BYTES=3145728
set MINIMAX_PDF_MAX_CANDIDATES=16
set MINIMAX_TABLE_CHAR_LIMIT=30000
MINIMAX_REQUEST_TIMEOUT=180
MINIMAX_REQUEST_RETRIES=3
set UAV_CVGL_PDF_CACHE_DIR=data\pdf_cache

python scripts\uav_cvgl_auto.py backfill --start-year 2016 --end-year 2026 --limit-per-query 15 --citation-limit 150
python scripts\uav_cvgl_auto.py stats --input data\backfill_candidates.yml
python scripts\uav_cvgl_auto.py classify --input data\backfill_candidates.yml --mode backfill
python scripts\uav_cvgl_auto.py stats --input data\backfill_candidates.yml
python scripts\uav_cvgl_auto.py merge --candidates data\backfill_candidates.yml

git add .
git commit -m "Run full UAV-CVGL backfill update"
git push
```

Notes:

- If a DeepSeek key is prefixed with `ds:`, the local script strips that provider prefix before calling the DeepSeek API.
- MiniMax summaries must use `MiniMax-M3`; the script stops if `MINIMAX_MODEL` is set to any other model.
- MiniMax keys may be endpoint-specific. The default endpoint is `https://api.minimaxi.com/v1`; when `https://api.minimax.io/v1` returns an authentication error, the script retries the China endpoint.
- MiniMax-M3 summaries use accessible PDF text by default when a PDF URL, OpenAlex open-access PDF, DOI landing-page PDF, publisher `citation_pdf_url`, or arXiv PDF can be resolved. Default local limits are 120,000 extracted characters, 80 pages, 100 MB per PDF, 3 MB per landing page, 16 candidate URLs per paper, and 30,000 table-evidence characters. Tune `MINIMAX_PDF_CHAR_LIMIT`, `MINIMAX_PDF_MAX_PAGES`, `MINIMAX_PDF_MAX_BYTES`, `MINIMAX_PDF_LANDING_MAX_BYTES`, `MINIMAX_PDF_MAX_CANDIDATES`, and `MINIMAX_TABLE_CHAR_LIMIT` if the run needs more or less full-text context.
- MiniMax-M3 receives extracted PDF/HTML table evidence and returns `leaderboard_metrics` rows for unverified leaderboard review. These rows map to `data/leaderboards.csv` columns and should not be promoted into public leaderboard files until manually checked.
- The public MiniMax OpenAI-compatible API documents MiniMax-M3 text, image, and video inputs. This pipeline therefore passes full paper text extracted from PDFs to MiniMax-M3 rather than assuming an undocumented PDF file content block.
- For papers that require institutional access, download the PDF through an authorized browser session into `data/pdf_cache` (or another path set by `UAV_CVGL_PDF_CACHE_DIR`). The classifier reads this local cache before trying network PDF discovery. Do not commit downloaded PDFs.
- MiniMax also returns a second-pass category confirmation. The script stores that confirmation in each paper summary and marks records for review when it disagrees with DeepSeek.

## Generated Reports

Full backfill generates:

```text
data/reports/backfill_search_report.md
data/reports/backfill_search_report.json
data/reports/classification_report.md
data/reports/classification_report.json
```

These reports show search steps, source counts, algorithm paper counts, survey paper counts, unrelated paper counts, and error counts.

