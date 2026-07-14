# GTA-UAV (Game4Loc)

UAV geo-localization benchmark from game data (Dai et al. 2024, Game4Loc). Cross-Area is the canonical leaderboard protocol; Same-Area is retained as a clearly separated supplementary comparison. Only each paper's complete proposed method is ranked; loss, backbone, pre-training, and component ablations are excluded.

## Cross-Area (official leaderboard)

Rows: **2** (one result row per method/configuration).

| Method | R@1 | R@5 | AP | SDM@3 | Dis@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| PAUL | 61.21 | 83.59 | 70.66 | 72.06 | 421.12 | [PAUL: Uncertainty-Guided Partition and Augmentation for Robust Cross-View Geo-Localization under Noisy Correspondence](https://openaccess.thecvf.com/content/CVPR2026/html/Li_PAUL_Uncertainty-Guided_Partition_and_Augmentation_for_Robust_Cross-View_Geo-Localization_under_CVPR_2026_paper.html) | Table 1, 0.0% noise block, p.6 of PDF |
| Game4Loc | 55.91 | 81.07 | 66.56 | 76.35 | 342.05 | [Game4Loc A UAV Geo-Localization Benchmark from Game Data](https://arxiv.org/abs/2409.16925) | Table 2, Positive+Semi-positive block, Ours row, p.5 |

## Same-Area (supplementary)

Rows: **2** (one result row per method/configuration).

| Method | R@1 | R@5 | AP | SDM@3 | Dis@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Game4Loc | 84.95 | 97.59 | 90.15 | 88.03 | 149.07 | [Game4Loc A UAV Geo-Localization Benchmark from Game Data](https://arxiv.org/abs/2409.16925) | Table 2, Positive+Semi-positive block, Ours row, p.5 |
| PAUL | 73.55 | 91.17 | 81.28 | 79.41 | 402.16 | [PAUL: Uncertainty-Guided Partition and Augmentation for Robust Cross-View Geo-Localization under Noisy Correspondence](https://openaccess.thecvf.com/content/CVPR2026/html/Li_PAUL_Uncertainty-Guided_Partition_and_Augmentation_for_Robust_Cross-View_Geo-Localization_under_CVPR_2026_paper.html) | Table 1, 0.0% noise block, p.6 of PDF |
