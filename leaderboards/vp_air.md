# VP-Air

Leaderboard for VP-Air. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view aerial VPR (Recall@N, consecutive frame threshold ±1)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR<br><sub>Unsupervised fine-tuning on AerialVL (11k satellite-aerial pairs), RTX 4090, 320x320, triplet loss with hard negative mining</sub> | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II, Section IV.A.2 | R@1=76.98 | false | Recall values obtained on NVIDIA RTX 3060; 256-dim descriptor; 139 FPS; 488 MB memory |

## Recall@N, ±1 consecutive frame threshold

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II | R@1=76.98 | false | - |

## consecutive frame threshold ±1

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ULTRAVPR<br><sub>unsupervised, fine-tuned on AerialVL with 11k image pairs, ResNet50 backbone, N=8 rotation angles, m=5 clustering</sub> | [UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual Place Recognition](https://doi.org/10.1109/lra.2025.3592075) | Table II | R@1=76.98 | false | Comprehensive performance comparison, feature dim 256, 139 FPS on RTX 3060 |
