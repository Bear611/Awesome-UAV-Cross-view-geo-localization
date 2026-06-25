# CVUSA

Leaderboard for CVUSA. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## 180° FoV, unknown orientation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ORIENTATION-FREE<br><sub>loss function ablation</sub> | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table IX (text) | R@1=61.20 | false | Loss function comparison; only R@1 mentioned |

## Ground→Satellite (with polar transform)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained, polar transform employed</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table IV, Section IV-D-3 | R@1=95.09 | false | R@Top1% = 99.77%; vs LPN (with polar transform): R@1 +1.31%; vs L2LTR: R@1 +1.04%, R@Top1% +0.10% |

## ground-to-aerial (UGV query vs. UAV nadir-view reference)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| DOCB + MSFA (Dynamic Online Cross-Batch hard exemplar mining with multi-scale feature aggregation)<br><sub>two-phase training: Phase 1 intra-batch hard exemplar mining; Phase 2 adds cross-batch DOCB mining with FIFO memory bank; weighted soft-margin triplet loss; VGG16 backbone with polar-transformed aerial images; descriptor length 512</sub> | [DOCB: A Dynamic Online Cross-Batch Hard Exemplar Recall for Cross-View Geo-Localization](https://doi.org/10.3390/ijgi14110418) | Abstract and contributions text (Section 1) | R@1=95.78 | false | Value reported in the paper abstract; full R@5/R@10/AP not present in the provided excerpt. |

## ground-to-aerial cross-view geo-localization, top-K retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>full model with image alignment (mixed mapping + dual CGAN) + Transformer</sub> | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | Table 1 | R@1=95.02 | false | R@1%: 99.87. New state-of-the-art on CVUSA. |

## ground-to-aerial retrieval (top-K)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>supervised</sub> | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | Table 1 | R@1=95.02 | false | R@1% value (99.87) used in AP field; no AP metric reported. Best results in table. |

## ground-to-aerial retrieval (top-K) - ablation

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>supervised</sub> | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | Table 3 | R@1=95.02 | false | Full SMDT model; R@1% value (99.87) used in AP field |

## standard

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Network](https://doi.org/10.1007/978-3-031-72913-3_5) | Table 2 | R@1=98.71 | false | - |

## top-K retrieval

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [SMDT Cross-View Geo-Localization with Image Alignment and Transformer](https://www.semanticscholar.org/search?q=SMDT%20Cross-View%20Geo-Localization%20with%20Image%20Alignment%20and%20Transformer) | SMDT: Cross-View Geo-Localization with Image Alignment and Transformer (ICME 2022), Table 1 | R@1=95.02 | false | - |
