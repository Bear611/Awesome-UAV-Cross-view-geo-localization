# UAV-CVGL Automation v0.3

This automation has two modes.

## Mode 1: Backfill

Backfill is a high-recall historical search mode. It searches by high-frequency UAV-CVGL keywords and by papers that cite seed dataset papers such as University-1652, SUES-200, DenseUAV, UAV-VisLoc, GTA-UAV, and UAV-GeoLoc.

Backfill is not scheduled. Run it manually because it can generate many candidates and consume API credits.

## Mode 2: Weekly Watch

Weekly Watch is a high-precision update mode. It searches recent papers, runs DeepSeek classification, uses MiniMax to summarize relevant papers, generates `data/weekly_candidates.yml`, and creates a weekly markdown update.

It is scheduled by GitHub Actions every Monday 02:00 UTC.

## LLM Responsibilities

DeepSeek is used for coarse paper classification:

- whether the paper belongs to UAV-CVGL;
- whether it is UAV-related;
- which of the four categories it belongs to;
- which benchmarks are mentioned;
- whether it may contain leaderboard results.

MiniMax is used for paper summary:

- 200-280 Chinese character research summary;
- proposed modules / methods;
- benchmark names;
- reported results if explicitly available;
- code link if explicitly available.

## Context Control

The pipeline never sends multiple papers in one prompt.

For each paper:

- unrelated paper: one DeepSeek call only;
- relevant paper: one DeepSeek call + one MiniMax call.

The default DeepSeek prompt uses title, year, venue, and abstract only. The default MiniMax prompt also uses title, abstract, and DeepSeek classification only. PDF extraction is disabled by default.

## Observable Progress

During local or GitHub Actions execution, logs show:

- searched keyword;
- number of candidates written;
- `[current/total]` processing status;
- whether DeepSeek or MiniMax was called;
- parsed / rejected / error counts;
- DeepSeek call count;
- MiniMax call count.

Every paper is written back to YAML immediately after processing. If the run is interrupted, rerun the command and cached classifications/summaries will be skipped.

## Public Paper Table Format

Generated paper pages use:

```markdown
| 论文 | 研究内容 | 数据/benchmark | Code |
```

The old visible `分类原因` column is removed from public pages. It is stored internally in:

```text
data/internal/classification_reasons.yml
```

## Security

Never write API keys into code, README, issues, pull requests, or logs. Use GitHub Actions Secrets:

- `DEEPSEEK_API_KEY`
- `MINIMAX_API_KEY`
- optional: `SEMANTIC_SCHOLAR_API_KEY`

If an API key is accidentally exposed, revoke it immediately and create a new one.
