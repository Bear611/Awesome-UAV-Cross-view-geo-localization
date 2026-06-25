# DenseUAV

Leaderboard for DenseUAV. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Drone-to-Satellite

Rows: **5**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| DINO-GFSA<br><sub>Trained on official DenseUAV training set, input 224x224, LoRA-adapted DINOv3 ViT-L backbone, InfoNCE loss, 80 epochs, single-pass retrieval, no TTA/re-ranking.</sub> | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 2 (DINO-GFSA / DINOv3-ViT-L row) | Recall@1=97.17 | false | AP is not reported; the paper reports R@5 (99.57%) and SDM@1 (97.68%), where SDM@1 is a positioning-distance metric (not AP). Only R@1 is directly mappable to the leaderboard spec; AP is unavailable in the paper and left null. Paper trained on official DenseUAV training set and evaluated on the official test set, so no exclusion based on training data. Needs manual review because AP is missing. |
| G2CL<br><sub>ConvNeXt-Tiny backbone, InfoNCE + Geographic Information Adaptive Contrastive Loss, trained on official DenseUAV training set, evaluated on official test set with all satellite scales (Small/Middle/Big) and both timeframes (2020/2022) — setting (5)</sub> | [A Deep Learning Framework with Geographic Information Adaptive Loss for Remote Sensing Images based UAV Self-Positioning](http://arxiv.org/abs/2502.16164v1) | Table 1, setting (5), G2CL row | Recall@1=94.51 | false | The leaderboard spec lists 'AP' as the second column; the paper reports SDM@1 (95.77) in this position. SDM is a DenseUAV-specific metric. AP value is reported as SDM@1=95.77 per paper convention. |
| SkyPart<br><sub>Trained on DenseUAV official train split with rotation augmentation, single-pass, no re-ranking, no TTA</sub> | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(b) | Recall@1=91.85 | false | 256x256 input, 26.95M params. Detailed comparison (Table 10) adds R@top1=99.61, AP=92.52, SDM@3=92.40, SDM@5=79.33; main table only reports R@1/R@5/SDM@1. Leaderboard column 'AP' is not reported in the main Table 2(b); Table 10 reports mean average precision=92.52 (additional metric, not requested). |
| DINOv2-GLFA-CESP<br><sub>Trained on official DenseUAV training set (no external training data, no TTA/re-ranking stated)</sub> | [DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=DINOv2-Based%20UAV%20Visual%20Self-Localization%20in%20Low-Altitude%20Urban%20Environments) | Abstract (paper text): 'the proposed method achieves impressive scores of 86.27% in R@1 and 88.87% in SDM@1 on the DenseUAV public benchmark dataset' | Recall@1=86.27 | false | Abstract does not report the 'AP' metric required by the leaderboard; it reports R@1 and SDM@1. Full text/tables were not available to confirm an AP value. |
| DenseUAV Baseline (ViT-S + SW Triplet + KL)<br><sub>Trained on official DenseUAV training set (10 universities, 6768 UAV-view / 13536 satellite-view images). ViT-S backbone pre-trained on ImageNet (timm). Input 224x224. SGD optimizer, lr=0.003, batch=8, 120 epochs. Standard cosine similarity retrieval at test time.</sub> | [Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=Vision-Based%20UAV%20Self-Positioning%20in%20Low-Altitude%20Urban%20Environments) | Table VII (last row) of the paper: CE Loss + Soft-Weighted Triplet Loss + KL Loss. Abstract also reports R@1=83.05% and SDM@1=86.24% which corresponds to the same configuration (minor discrepancy in decimal precision between abstract and table; using table value as it is the primary detailed report). | Recall@1=83.01 | false | The paper does not report Average Precision (AP) on DenseUAV. The closest reported metric is SDM@1 (Spatial Distance Metric), which is a continuous retrieval+localization metric introduced by the paper. The abstract reports R@1=83.05% / SDM@1=86.24%, while Table VII reports 83.01% / 86.50% for the same configuration. Small discrepancies likely due to different runs. We use Table VII values as they are the more detailed report. |

## Drone→Satellite

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| WEATHER-INVARIANT<br><sub>X-VLM</sub> | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 3 (Mean) | R@1=52.43 | false | +23.18% R@1 and +23.20% AP over baseline |

## Satellite→Drone

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| WEATHER-INVARIANT<br><sub>X-VLM</sub> | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 4 (Mean) | R@1=49.03 | false | +21.25% R@1 and +21.05% AP over baseline |

## UAV-to-satellite cross-view matching

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| DINOv2 + GLFA + CESP (Proposed)<br><sub>224x224 input, SGD optimizer, lr=0.03 with 0.9 decay at epochs 70 and 110, batch size 80, 120 epochs, single GTX 4090 GPU</sub> | [DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=DINOv2-Based%20UAV%20Visual%20Self-Localization%20in%20Low-Altitude%20Urban%20Environments) | Table I and Section IV-B | R@1=86.27 | false | SDM@1 = 88.87%; improvements of 3.26% (R@1) and 2.37% (SDM@1) over the DenseUAV baseline. R@5, R@10, and AP not reported in the visible text. |

## cross-view UAV-satellite retrieval, R@K and SDM@K metrics

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| SELF-LOCALIZATION<br><sub>DINOv2-B backbone, batch size 80, lr 0.03, SGD, 120 epochs, GTX 4090</sub> | [DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=DINOv2-Based%20UAV%20Visual%20Self-Localization%20in%20Low-Altitude%20Urban%20Environments) | Table I and text | R@1=86.27 | false | SDM@1 = 88.87%. Improvements over baseline: +3.26% R@1, +2.37% SDM@1. |

## cross-view UAV-satellite retrieval, R@K metric

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| SELF-LOCALIZATION<br><sub>From Keetha et al. 2024, no fine-tuning on DenseUAV</sub> | [DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=DINOv2-Based%20UAV%20Visual%20Self-Localization%20in%20Low-Altitude%20Urban%20Environments) | Table I and text | R@1=14.24 | false | Used DINOv2 model directly without proposed adaptations. |

## drone-to-satellite

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table X | R@1=90.56 | false | Improves R@1 by 1.84 percentage points over second-best method (CAMP). |
