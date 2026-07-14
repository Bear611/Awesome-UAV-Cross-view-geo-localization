# GTA-UAV (Game4Loc)

UAV geo-localization benchmark from game data (Dai et al. 2024, Game4Loc). Same-Area and Cross-Area results are kept separate; the canonical tables use Positive+Semi-positive training data.

## Same-Area (Pos+Semi)

Rows: **9** (one result row per method/configuration).

| Method | R@1 | R@5 | AP | SDM@3 | Dis@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Ours: Weighted-InfoNCE + MES (Pos+Semi) | 84.95 | 97.59 | 90.15 | 88.03 | 149.07 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, Ours row), p.5 |
| Weighted-InfoNCE + MES (Pos-only) | 75.97 | 94.53 | 83.35 | 82.8 | 325.61 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, Ours row, Same-Area column), p.5 |
| InfoNCE Loss (Pos-only) | 72.99 | 90.64 | 80.76 | 80.4 | 363.67 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, InfoNCE row, Same-Area column), p.5 |
| InfoNCE + MES (Pos-only) | 72.34 | 91.42 | 80.86 | 81.57 | 369.59 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, InfoNCE+MES row, Same-Area column), p.5 |
| Triplet Loss (Pos-only) | 68.22 | 87.99 | 76.73 | 79.17 | 438.38 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, TripletLoss row, Same-Area column), p.5 |
| InfoNCE + MES (Mutual Exclusive Sampling, Pos+Semi) | 65.89 | 93.09 | 77.84 | 86.52 | 196.59 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, InfoNCE+MES row), p.5 |
| InfoNCE Loss (Pos+Semi) | 52.67 | 90.75 | 67.74 | 85.35 | 204.08 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, InfoNCE row), p.5 |
| Triplet Loss (L_triplet, Pos+Semi) | 46.55 | 85.07 | 62.95 | 83.63 | 252.88 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, TripletLoss row), p.5 |
| Pretrain on ImageNet | 10.65 | 23.9 | 17.15 | 36.82 | 1470.5 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 3 (ImageNet row), p.6 |

## Cross-Area (Pos+Semi)

Rows: **12** (one result row per method/configuration).

| Method | R@1 | R@5 | AP | SDM@3 | Dis@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Weighted-InfoNCE + MES (Pos-only) | 57.52 | 80.1 | 67.24 | 72.33 | 444.13 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, Ours row, Cross-Area column), p.5 |
| Ours: Weighted-InfoNCE + MES (Pos+Semi) | 55.91 | 81.07 | 66.56 | 76.35 | 342.05 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, Ours row), p.5 |
| ConvNeXt-Base (backbone) | 55.36 | - | 66.14 | 74.91 | 386.35 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 5 (ConvNeXt-Base row), p.6 |
| Swinv2-B (backbone) | 53.7 | - | - | - | - | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 5 (Swinv2-B row), p.6 |
| InfoNCE + MES (Pos-only) | 52.64 | 74.63 | 62.4 | 67.64 | 552.9 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, InfoNCE+MES row, Cross-Area column), p.5 |
| InfoNCE Loss (Pos-only) | 49.57 | 72.84 | 59.68 | 65.53 | 612.22 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, InfoNCE row, Cross-Area column), p.5 |
| InfoNCE + MES (Mutual Exclusive Sampling, Pos+Semi) | 45.97 | 71.43 | 57.19 | 71.48 | 460.08 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, InfoNCE+MES row), p.5 |
| Triplet Loss (Pos-only) | 43.41 | 66.7 | 53.56 | 61.26 | 756.95 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive-only block, TripletLoss row, Cross-Area column), p.5 |
| InfoNCE Loss (Pos+Semi) | 35.83 | 63.79 | 48.08 | 68.15 | 576.41 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, InfoNCE row), p.5 |
| Triplet Loss (L_triplet, Pos+Semi) | 24.78 | 46.99 | 35.13 | 58.79 | 879.06 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 2 (Positive+Semi-positive block, TripletLoss row), p.5 |
| ResNet-101 (backbone) | 13.74 | - | 23.06 | 48.06 | 1126.52 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 5 (ResNet-101 row), p.6 |
| Pretrain on ImageNet | 9.74 | 21.73 | 15.74 | 33.58 | 1841.3 | Game4Loc: A UAV Geo-Localization Benchmark from Game Data (Dai et al. 2024 — GTA-UAV paper) | Table 3 (ImageNet row), p.6 |
