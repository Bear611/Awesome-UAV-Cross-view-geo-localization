# Leaderboard Sources

The v0.4 leaderboard rows are derived from MiniMax-M3 extraction over full-text PDF/HTML/table evidence after DeepSeek relevance filtering. Rows remain `verified=false` until manual review.

| Artifact | Description |
|---|---|
| `data/leaderboards.csv` | Machine-readable extracted leaderboard rows for configured public benchmarks. |
| `data/backfill_candidates.yml` | Source candidate records, classification decisions, summaries, and extracted `leaderboard_metrics`. |
| `data/reports/backfill_search_report.md` | Search-source report confirming OpenAlex citation expansion. |
| `data/reports/classification_report.md` | Classification and summarization report. |

## Included Row Counts

| Dataset | Rows |
|---|---:|
| University-1652 | 114 |
| UAV-VisLoc | 18 |
| DenseUAV | 15 |
| SUES-200 | 3 |

## Excluded Row Counts

| Dataset | Rows |
|---|---:|
| AerialVL | 2 |
| UL14 | 1 |
