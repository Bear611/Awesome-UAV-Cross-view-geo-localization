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
| SUES-200 | 17 |
| University-1652 | 54 |

## Excluded Row Counts

| Dataset | Rows |
|---|---:|
| DenseUAV | 29 |
| GTA-UAV | 13 |
| Nardo-Air | 5 |
| SUES-200 | 49 |
| UAV-GeoLoc | 5 |
| UAV-VisLoc | 25 |
| University-1652 | 116 |
| World-UAV | 5 |
