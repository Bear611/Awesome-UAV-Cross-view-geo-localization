# GTA-UAV

Leaderboard for GTA-UAV. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-Area Retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Game4Loc (weighted-InfoNCE + MES, ViT-Base/16, positive+semipositive)<br><sub>Trained on GTA-UAV with weighted-InfoNCE loss (k=5) and Mutually Exclusive Sampling using positive+semi-positive pairs; ViT-Base/16 backbone, 384x384 input, 20 epochs, batch size 64.</sub> | Game4Loc: A UAV Geo-Localization Benchmark from Game Data | Table 2 (positive+semipositive, cross-area row: Lweighted-InfoNCE w/. MES) | Recall@1=55.91 | false | Flagship GTA-UAV cross-area result using the full partial-matching training set (positive + semi-positive). |

## cross-area

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| RGBD-EMA<br><sub>Shared-weight ViTAdapter backbone with MiDaS v3.1 (DPT-BEiT-Large) depth estimation for UAV inputs, Efficient Multi-scale Attention (EMA) module, IoU-weighted InfoNCE loss; train/test split ~8:2 by region</sub> | [UAV Visual Localization via Multimodal Fusion and Multi-Scale Attention Enhancement](https://doi.org/10.3390/su18094277) | Abstract | R@1=18.12 | false | Additional reported metrics: SDM@3=0.53, Dis@1=1052.73 m. Values are as reported in the abstract; AP stated as 28.01 (unit/percentage not explicitly indicated in text). |

## cross-area (8:2 region split)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| RGBD + EMA (proposed)<br><sub>AdamW, batch size 4, lr 5e-5 with cosine annealing + 0.1-epoch warmup, IoU-weighted InfoNCE loss (tau=0.07), 384x384 input, MiDaS depth + EMA module, shared-weight ViTAdapter, embedding dim 768</sub> | [UAV Visual Localization via Multimodal Fusion and Multi-Scale Attention Enhancement](https://doi.org/10.3390/su18094277) | Table 1 & Table 2 | R@1=18.1207 | false | Proposed full framework; SDM@1=0.5549, SDM@3=0.5257, SDM@5=0.5047; Dis@1=1052.73m |
