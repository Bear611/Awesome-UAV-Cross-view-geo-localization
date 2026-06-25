# LasVegasFly

Leaderboard for LasVegasFly. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## UAV-to-Satellite image retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (ACCL)<br><sub>ConvNeXt-B backbone, siamese network, SGD optimizer, batch size 16, cosine LR scheduler, initial LR 0.005, RTX 4090</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table I | R@1=84.87 | false | LDE = 6.67m; mAP reported as 92.17%; new dataset introduced in this paper |

## test set cross-view retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on LasVegasFly (ConvNeXt-B backbone, SGD, batch 16, cosine LR 0.005)</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table I | R@1=84.87 | false | LDE = 6.67 m; +2.97% R@1 over Sample4Geo; newly collected dataset |

## test set cross-view retrieval (ablation)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| UAV-TO-SATELLITE<br><sub>trained on LasVegasFly with ACCL using only d1</sub> | [ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UAV-to-Satellite Geolocalization](https://doi.org/10.1109/icme59968.2025.11209371) | Table IV | R@1=83.85 | false | Confusion matrix ablation row 'Distance' |
