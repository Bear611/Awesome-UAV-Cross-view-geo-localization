# DenseUAV

UAV self-positioning benchmark (Dai et al. 2023, IEEE TIP). Single retrieval task: drone-view image → satellite-view gallery retrieval. Metrics include R@K and SDM@K (Spatial Distance Metric, K=1 in main results). Rows sorted by R@1 descending.

## UAV Self-Positioning

Rows: **11** (one per paper).

| Method | R@1 | R@5 | AP | SDM@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| CROSS-VIEW | 90.56 | 98.03 | - | - | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table X |
| DenseUAV Baseline (ViT-S, full pipeline) | 83.01 | - | - | 86.24 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Dai et al. 2023 — DenseUAV paper) | Abstract; Section I |
| DenseUAV Baseline (ViT-S, no random-erase) | 80.18 | - | - | 84.39 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Dai et al. 2023 — DenseUAV paper) | Table VII (ViT-S row, last row), p.10 |
| WEATHER-INVARIANT | 52.43 | - | 58.39 | - | Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse | Table 3 (Mean) |
| SELF-LOCALIZATION | 14.24 | - | - | - | DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments | Table I and text |
| G2CL | - | - | - | - | A Deep Learning Framework with Geographic Information Adaptive Loss for Remote Sensing Images based UAV Self-Positioning | Table 1, setting (5), G2CL row |
| DINO-GFSA | - | - | - | - | DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation | Table 2 (DINO-GFSA / DINOv3-ViT-L row) |
| DINOv2-GLFA-CESP | - | - | - | - | DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments | Abstract (paper text): 'the proposed method achieves impressive scores of 86.27% in R@1 and 88.87% in SDM@1 on the DenseUAV public benchmark dataset' |
| DenseUAV Baseline (ViT-S + SW Triplet + KL) | - | - | - | - | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments | Table VII (last row) of the paper: CE Loss + Soft-Weighted Triplet Loss + KL Loss. Abstract also reports R@1=83.05% and SDM@1=86.24% which corresponds to the same configuration (minor discrepancy in decimal precision between abstract and table; using table value as it is the primary detailed report). |
| SkyPart | - | - | - | - | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery | Table 2(b) |
| DINOv2 + GLFA + CESP (Proposed) | - | - | - | - | DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments | Table I and Section IV-B |
