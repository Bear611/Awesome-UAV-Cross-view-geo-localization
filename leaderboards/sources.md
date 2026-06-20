# Leaderboard Sources

The rebuilt leaderboards are generated from:

| Artifact | Role |
|---|---|
| `data/internal/leaderboard_dataset_specs.yml` | DeepSeek-generated dataset protocol and metric specifications. |
| `data/internal/leaderboard_reviews.yml` | MiniMax-M3 one-paper-at-a-time review cache. |
| `data/leaderboards.csv` | Machine-readable wide-row leaderboard export. |
| `data/backfill_candidates.yml` | Original candidate records and prior extraction evidence. |

## Included Row Counts

| Dataset | Rows |
|---|---:|
| DenseUAV | 5 |
| GTA-UAV | 2 |
| SUES-200 | 15 |
| University-1652 | 51 |

## Excluded Row Counts

| Dataset | Rows |
|---|---:|
| DenseUAV | 26 |
| GTA-UAV | 11 |
| SUES-200 | 50 |
| UAV-VisLoc | 23 |
| University-1652 | 116 |
