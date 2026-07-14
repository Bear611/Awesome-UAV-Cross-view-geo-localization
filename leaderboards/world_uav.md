# World-UAV

World-UAV was introduced by [UAV-GeoLoc](https://doi.org/10.1109/LRA.2025.3588061). The paper reports retrieval results for Terrain, City, and Mix scenes. This page separates independently proposed methods from baselines re-evaluated by the dataset authors.

## Official method leaderboard

Only a paper's complete proposed method is eligible here. As of 2026-07-14, no independent follow-up paper with a new World-UAV result was found.

| Method | Training dataset | Time | Terrain R@1/R@5/R@10 | City R@1/R@5/R@10 | Mix R@1/R@5/R@10 | Paper |
|---|---|---:|---:|---:|---:|---|
| UAVPlace | UAV-World | 111.11 ms | 69.22 / 83.57 / 88.15 | 65.50 / 82.25 / 87.41 | 65.38 / 82.62 / 87.79 | [UAV-GeoLoc](https://ringowrw.github.io/GeoLoc-UAV/) |

## Original-paper benchmark baselines (not ranked)

These values remain useful as reference evidence, but they are not independent World-UAV submissions. They were trained, adapted, or evaluated inside the UAV-GeoLoc paper; backbone and LPN variants must not be interpreted as separate papers or leaderboard entries.

| Baseline/configuration | Training dataset | Time | Terrain R@1/R@5/R@10 | City R@1/R@5/R@10 | Mix R@1/R@5/R@10 |
|---|---|---:|---:|---:|---:|
| Game4Loc-b | GTA-UAV | 15.97 ms | 56.13 / 77.24 / 83.75 | 35.63 / 54.04 / 62.51 | 43.83 / 63.32 / 71.01 |
| AnyLoc-g | - | 36.77 ms | 51.28 / 73.66 / 81.56 | 39.26 / 59.04 / 66.77 | 44.07 / 64.89 / 72.68 |
| DINOv2-s + LPN | UAV-World | 12.58 ms | 46.53 / 71.14 / 79.96 | 49.00 / 70.90 / 78.66 | 58.26 / 79.49 / 85.64 |
| DINOv2-s, fine-tuned | UAV-World | 12.45 ms | 45.45 / 70.25 / 79.39 | 32.22 / 54.82 / 65.28 | 48.24 / 71.28 / 79.56 |
| AnyLoc-l | - | 14.80 ms | 43.98 / 66.93 / 75.63 | 37.40 / 56.57 / 65.00 | 40.03 / 60.71 / 69.25 |
| AnyLoc-s | - | 8.22 ms | 35.69 / 57.89 / 67.09 | 24.89 / 42.94 / 52.24 | 29.21 / 48.92 / 58.18 |
| ResNet18 + LPN | UAV-World | 7.20 ms | 38.33 / 64.42 / 74.81 | 43.03 / 64.41 / 72.08 | 40.86 / 64.45 / 73.50 |
| ResNet18, fine-tuned | UAV-World | 6.77 ms | 31.73 / 59.53 / 71.12 | 22.90 / 43.82 / 54.20 | 26.07 / 50.31 / 62.31 |

Source: UAV-GeoLoc comparative evaluation on World-UAV. The official project page provides the paper, code, and dataset links.
