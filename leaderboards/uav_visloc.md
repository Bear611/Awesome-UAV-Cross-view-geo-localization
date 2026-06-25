# UAV-VisLoc

Leaderboard for UAV-VisLoc. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view aerial VPR (Recall@N, 200m geographic distance threshold, average over 10 sub-datasets)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR<br><sub>Unsupervised fine-tuning on AerialVL</sub> | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table IV, Section IV.B.3 | R@1= | false | Baseline (UltraVPR*); enhancement C(m=5) yields +2.32% R@1; absolute value not stated in text |

## R@N retrieval (150m threshold)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed (TeTRA-VPR + UAV adapter + KD)<br><sub>cross-domain transfer learning from ground-level VPR pretraining</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Section III.B (text), Table I (caption only in provided text) | R@1=56.7 | false | Explicitly stated in text; R@5 and R@10 not provided in paper text. Compared to UltraVPR. |

## R@N retrieval (150m threshold) - ablation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed w/o UAV adapter (ablation)<br><sub>ablation removing UAV adapter</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Table IV (caption only in provided text), Section III.D | R@1= | false | Table IV contents not included in text; only stated that removing UAV adapter causes 3.3-5.3% R@1 drops. Exact values not extractable. |

## R@N retrieval - semantic conditioning ablation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Proposed w/o semantic conditioning (ablation)<br><sub>ablation removing semantic conditioning</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Fig. 4 (caption only in provided text), Section III.D | R@1= | false | Fig. 4 contents not included in text; described as showing significant performance degradation without specific numbers. |

## Recall@N (R@N), radius threshold 150m; satellite images segmented into fixed-size patches centered at mapped UAV GPS coordinates

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching)<br><sub>Trained on AerialVL vpr-training-data; frozen TeTRA-VPR backbone with UAV adapter; UAV-specific augmentation; knowledge distillation + triplet loss</sub> | [Lightweight Cross-View Localization via Quantized Knowledge Distillation and Adaptive Local Feature Matching](https://doi.org/10.1109/lsp.2026.3670737) | Table I; text: 'our method achieves 62.5% and 56.7% R@1 on AerialVL and UAV-VisLoc respectively' | R@1=56.7 | false | Table I not fully rendered in provided text; only R@1 explicitly stated. Ablation shows removing UAV adapter causes 3.3-5.3% R@1 drops. Fine-matching GMD=4.0m (35.5% improvement over DeDoDe 6.2m) is a separate matching metric, not retrieval. |

## Recall@N, 200m geographic distance threshold (avg over 10 sub-datasets)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table I (numbers not visible in extracted text) |  | false | - |
