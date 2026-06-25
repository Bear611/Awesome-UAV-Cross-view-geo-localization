# AerialVL

Leaderboard for AerialVL. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view aerial VPR (Recall@N, 100m geographic distance threshold)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR<br><sub>Unsupervised fine-tuning on AerialVL (11k satellite-aerial pairs), RTX 4090, 320x320, triplet loss with hard negative mining</sub> | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II, Section IV.A.2 | R@1=63.05 | false | Recall values obtained on NVIDIA RTX 3060; 256-dim descriptor |

## R@N retrieval (100m threshold)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed (TeTRA-VPR + UAV adapter + KD)<br><sub>cross-domain transfer learning from ground-level VPR pretraining</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Section III.B (text), Table I (caption only in provided text) | R@1=62.5 | false | Explicitly stated in text; R@5 and R@10 not provided in paper text. Compared to UltraVPR. |

## R@N retrieval (100m threshold) - ablation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed w/o UAV adapter (ablation)<br><sub>ablation removing UAV adapter</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Table IV (caption only in provided text), Section III.D | R@1= | false | Table IV contents not included in text; only stated that removing UAV adapter causes 3.3-5.3% R@1 drops. Exact values not extractable. |

## R@N retrieval - semantic conditioning ablation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed w/o semantic conditioning (ablation)<br><sub>ablation removing semantic conditioning</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Fig. 4 (caption only in provided text), Section III.D | R@1= | false | Fig. 4 contents not included in text; described as showing significant performance degradation without specific numbers. |

## Recall@N (R@N), radius threshold 100m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching)<br><sub>Trained on AerialVL vpr-training-data; frozen TeTRA-VPR backbone with UAV adapter; UAV-specific augmentation (random affine, perspective, ColorJitter, RandomErasing); knowledge distillation + triplet loss</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Table I; text: 'our method achieves 62.5% and 56.7% R@1 on AerialVL and UAV-VisLoc respectively' | R@1=62.5 | false | 256-dim global descriptor, 3.2 GFLOPs, 5.8M parameters, 323 FPS on UAV-VisLoc (cj-20); compared against UltraVPR and other SOTA VPR methods (Table I not fully rendered in text) |

## Recall@N, 100m geographic distance threshold

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II | R@1=63.05 | false | - |

## geographic distance threshold 100m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR<br><sub>unsupervised, fine-tuned on AerialVL with 11k image pairs, ResNet50 backbone, N=8 rotation angles, m=5 clustering</sub> | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II | R@1=63.05 | false | Comprehensive performance comparison, feature dim 256 |
