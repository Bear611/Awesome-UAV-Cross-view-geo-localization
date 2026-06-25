# NewYorkFly

Leaderboard for NewYorkFly. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## UAV-to-Satellite image retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (ACCL)<br><sub>ConvNeXt-B backbone, siamese network, SGD optimizer, batch size 16, cosine LR scheduler, initial LR 0.005, RTX 4090</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table I | R@1=92.80 | false | LDE = 1.20m; mAP reported as 96.39% |

## UAV-to-Satellite image retrieval (R+M: retrieval + local feature matching)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| NetVLAD+LoFTR<br><sub>As reported in original papers, combined by Wang et al.</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table II | R@1=77.55 | false | Retrieval + matching pipeline; LDE not reported |

## test set R@1 by confusion distance (1-2 m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on NewYorkFly</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table III | R@1=99.50 | false | N=999 samples with confusion distance 1-2 m |

## test set R@1 by confusion distance (<=1 m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on NewYorkFly</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table III | R@1=100.00 | false | N=500 samples with confusion distance <=1 m |

## test set R@1 by confusion distance (>2 m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on NewYorkFly</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table III | R@1=72.26 | false | N=501 samples with confusion distance >2 m; high-confusion subset; +144.58% relative gain over Sample4Geo |

## test set cross-view retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on NewYorkFly (ConvNeXt-B backbone, SGD, batch 16, cosine LR 0.005)</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table I | R@1=92.80 | false | LDE = 1.20 m; +13.95% R@1 over Sample4Geo |

## test set cross-view retrieval (ablation)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on NewYorkFly with ACCL using only d1</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table IV | R@1=88.70 | false | Confusion matrix ablation row 'Distance' |
