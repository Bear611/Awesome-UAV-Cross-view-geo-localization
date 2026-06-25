# UAV-VLL (U-1652)

Leaderboard for UAV-VLL (U-1652). Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Satellite->UAV

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>CLIP ViT-B + BERT frozen, bidirectional-guided alignment + contrastive learning</sub> | [VLGeo: Bridging Viewpoints in UAV-View Geo-Localization Using a Large Vision–Language Model](https://doi.org/10.1109/tgrs.2026.3680280) | Table II / Section V-C-1 | R@1= | false | Reported improvement of 6.13% in R@1 over image-only and 3.73% over image–text; full numeric values not legible in extracted text |

## UAV->Satellite

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>CLIP ViT-B + BERT frozen, bidirectional-guided alignment + contrastive learning</sub> | [VLGeo: Bridging Viewpoints in UAV-View Geo-Localization Using a Large Vision–Language Model](https://doi.org/10.1109/tgrs.2026.3680280) | Table V | R@1=98.57 | false | Qwen2-VL used as text-generation pipeline; reported as optimal for target localization task |

## UAV->Satellite (weather robustness)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>Robustness evaluation against weather disturbances</sub> | [VLGeo: Bridging Viewpoints in UAV-View Geo-Localization Using a Large Vision–Language Model](https://doi.org/10.1109/tgrs.2026.3680280) | Table VII / Section V-D-6 | R@1= | false | Qualitative claim that VLGeo shows smaller performance drops than FSRA under rain/fog/rain+fog; specific numeric values not legible |
