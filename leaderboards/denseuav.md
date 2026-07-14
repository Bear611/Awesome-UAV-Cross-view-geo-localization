# DenseUAV

UAV self-positioning benchmark (Dai et al. 2023, IEEE TIP). The canonical task retrieves satellite-view gallery images for a drone-view query.

## UAV Self-Positioning

Rows: **12** (one result row per method/configuration).

| Method | R@1 | R@5 | AP | SDM@1 | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| DINO-GFSA | 97.17 | 99.57 | - | - | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 2 (DINO-GFSA / DINOv3-ViT-L row) |
| MFAF (EVA02-L) | 95.22 | 99.93 | - | 95.23 | [MFAF: An EVA02-Based Multi-scale Frequency Attention Fusion Method for Cross-View Geo-Localization](http://arxiv.org/abs/2509.12673v1) | Table 4, rendered PDF p.11 |
| G2CL | 94.51 | - | - | 95.77 | [A Deep Learning Framework with Geographic Information Adaptive Loss for Remote Sensing Images based UAV Self-Positioning](http://arxiv.org/abs/2502.16164v1) | Table 1, setting (5), G2CL row |
| SHAA | 93.69 | 98.76 | - | 94.91 | SHAA: Spatial Hybrid Attention Network With Adaptive Cross-Entropy Loss Function for UAV-View Geo-Localization | Table VI, rendered PDF p.11 |
| SkyPart | 91.85 | 97.81 | - | - | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(b) |
| SCOF | 90.56 | 98.03 | - | - | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table X |
| MFFT (proposed) | 88.5 | - | - | 90.51 | [Visual Self-Positioning of Low-Altitude Urban UAV Based on Improved Transformer Architecture](https://doi.org/10.1109/jiot.2025.3599506) | Table II; text Section IV-C |
| DINOv2 + GLFA + CESP (Proposed) | 86.27 | 96.83 | - | 88.87 | [DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=DINOv2-Based%20UAV%20Visual%20Self-Localization%20in%20Low-Altitude%20Urban%20Environments) | Table I, p.2084 (PDF p.5) |
| DenseUAV Baseline (ViT-S + SW Triplet + KL) | 83.01 | 95.58 | - | - | [Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments](https://www.semanticscholar.org/search?q=Vision-Based%20UAV%20Self-Positioning%20in%20Low-Altitude%20Urban%20Environments) | Table VII (last row) of the paper: CE Loss + Soft-Weighted Triplet Loss + KL Loss. Abstract also reports R@1=83.05% and SDM@1=86.24% which corresponds to the same configuration (minor discrepancy in decimal precision between abstract and table; using table value as it is the primary detailed report). |
| DenseUAV Baseline (ViT-S, full pipeline) | 83.01 | - | - | 86.24 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Dai et al. 2023 — DenseUAV paper) | Abstract; Section I |
| DenseUAV Baseline (ViT-S, no random-erase) | 80.18 | - | - | 84.39 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Dai et al. 2023 — DenseUAV paper) | Table VII (ViT-S row, last row), p.10 |
| Safe-Net | 52.43 | - | 58.39 | - | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 3 (Mean) |
