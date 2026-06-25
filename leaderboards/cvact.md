# CVACT

Leaderboard for CVACT. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Ground→Satellite (with polar transform)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained, polar transform employed</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table IV, Section IV-D-4 | R@1=86.64 | false | R@Top1% = 98.45%; vs LPN (with polar transform): R@1 +3.77%, R@5 +2.35%, R@10 +1.85%, R@Top1% +0.68%; vs L2LTR: R@1 +1.75%, R@Top1% +0.08% |

## cross-dataset (CVUSA→CVACT) test

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Network](https://doi.org/10.1007/978-3-031-72913-3_5) | Table 4 | R@1=44.1 | false | - |

## cross-dataset (CVUSA→CVACT) val

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Network](https://doi.org/10.1007/978-3-031-72913-3_5) | Table 4 | R@1=67.79 | false | - |

## ground-to-aerial cross-view geo-localization, top-K retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>full model with image alignment (mixed mapping + dual CGAN) + Transformer</sub> | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | Table 2 | R@1=85.52 | false | R@1%: 98.96. New state-of-the-art on CVACT. |

## test

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Network](https://doi.org/10.1007/978-3-031-72913-3_5) | Table 2 | R@1=73.68 | false | - |

## top-K retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | SMDT: Cross-View Geo-Localization with Image Alignment and Transformer (ICME 2022), Table 2 | R@1=85.52 | false | - |

## validation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Network](https://doi.org/10.1007/978-3-031-72913-3_5) | Table 2 | R@1=91.9 | false | - |
