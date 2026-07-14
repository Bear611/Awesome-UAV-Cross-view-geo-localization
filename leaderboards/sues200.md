# SUES-200

Cross-view geo-localization benchmark (Zhu et al. 2022, IEEE TCSVT). Drone-to-Satellite and Satellite-to-Drone retrieval are reported separately at 150m, 200m, 250m, and 300m.

## Drone-to-Satellite (150m)

Rows: **18** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| BGG | 99.30 | 99.46 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| (MGS)2-Net | 98.45 | 98.78 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| CGSI (Ours) | 95.95 | 96.80 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| MEAN | 95.50 | 96.46 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| Sample4Geo-DPHR | 94.55 | 95.60 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| SDPL | 93.37 | 95.03 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| SCOF (Ours) | 90.75 | 92.32 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| MADA-SSA | 88.12 | 90.44 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| MFFN-AAE | 88.07 | 90.82 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 85.30 | 87.58 | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III |
| AFMS-Net | 85.25 | 88.24 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| ConvNeXt-based Multi-level Representation Learning | 83.05 | 86.00 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| P2FCN (proposed, ConvNeXt-B) | 78.64 | 82.44 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) |
| AdaptGeo (DINOv2-Base) | 78.53 | - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 77.57 | 81.30 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 61.58 | 67.23 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 59.32 | 64.93 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (SUES-200 baseline row), p.11 |
| LCM (Ding et al. 2019, migrated) | 43.42 | 49.65 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Drone-to-Satellite (200m)

Rows: **16** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| (MGS)2-Net | 99.62 | 99.69 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| BGG | 99.45 | 99.55 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| MEAN | 98.38 | 98.72 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| CGSI (Ours) | 97.72 | 98.15 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| SDPL | 95.67 | 97.36 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| Sample4Geo-DPHR | 95.43 | 96.36 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| SCOF (Ours) | 94.25 | 95.35 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| MADA-SSA | 94.17 | 95.31 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| MFFN-AAE | 93.75 | 94.81 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 93.23 | 94.66 | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III |
| AFMS-Net | 90.53 | 92.24 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| ConvNeXt-based Multi-level Representation Learning | 89.65 | 91.81 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 89.50 | 91.40 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 70.85 | 75.96 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 62.3 | 67.24 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 49.42 | 55.91 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Drone-to-Satellite (250m)

Rows: **16** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| (MGS)2-Net | 99.78 | 99.80 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| BGG | 99.53 | 99.63 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| MEAN | 98.95 | 99.17 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| Sample4Geo-DPHR | 98.95 | 99.14 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| CGSI (Ours) | 97.60 | 98.03 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| SCOF (Ours) | 96.88 | 97.42 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| MADA-SSA | 96.65 | 97.38 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| SDPL | 96.50 | 97.78 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 96.48 | 97.28 | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III |
| MFFN-AAE | 95.07 | 95.98 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| ConvNeXt-based Multi-level Representation Learning | 94.05 | 95.62 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| AFMS-Net | 93.03 | 94.32 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 92.58 | 94.21 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 80.38 | 83.8 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 71.35 | 75.49 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 54.47 | 60.31 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Drone-to-Satellite (300m)

Rows: **17** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| (MGS)2-Net | 100.00 | 100.00 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| Sample4Geo-DPHR | 99.80 | 99.85 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| MEAN | 99.52 | 99.63 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| BGG | 99.25 | 99.38 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| SCOF (Ours) | 97.85 | 98.10 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| CGSI (Ours) | 97.83 | 98.23 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| MADA-SSA | 97.72 | 98.25 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| SDPL | 97.52 | 98.52 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 97.50 | 98.09 | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.40 | 97.92 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| MFFN-AAE | 96.15 | 96.83 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| ConvNeXt-based Multi-level Representation Learning | 95.75 | 96.30 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| AFMS-Net | 94.05 | 95.25 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| AdaptGeo (DINOv2-Base) | 93.28 | - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 81.47 | 84.53 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 77.17 | 80.67 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 60.43 | 65.78 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Satellite-to-Drone (150m)

Rows: **17** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| BGG | 98.75 | 98.22 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| (MGS)2-Net | 98.75 | 96.50 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| MEAN | 97.50 | 94.75 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| CGSI (Ours) | 97.50 | 96.22 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| AFMS-Net | 96.50 | 82.83 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| MADA-SSA | 96.25 | 87.33 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| MFFN-AAE | 95.00 | 88.23 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| ConvNeXt-based Multi-level Representation Learning | 95.00 | 91.82 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| Sample4Geo-DPHR | 95.00 | 90.73 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| SCOF (Ours) | 95.00 | 89.92 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 93.75 | 79.49 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| AdaptGeo (DINOv2-Base) | 92.50 | - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| MobileGeo | 92.5 | 83.81 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table II |
| P2FCN (proposed, ConvNeXt-B) | 91.50 | 82.49 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) |
| LPN (block=4) (Wang et al. 2019, migrated) | 83.75 | 66.78 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 82.5 | 58.95 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 57.5 | 38.11 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Satellite-to-Drone (200m)

Rows: **15** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| MEAN | 100.00 | 97.09 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| (MGS)2-Net | 100.00 | 98.51 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| AFMS-Net | 98.75 | 92.01 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| BGG | 98.75 | 98.24 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| MADA-SSA | 98.75 | 96.12 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| CGSI (Ours) | 98.75 | 97.62 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.50 | 90.52 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| MobileGeo | 97.5 | 91.75 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table II |
| Sample4Geo-DPHR | 97.50 | 94.41 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| SCOF (Ours) | 97.50 | 93.13 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| MFFN-AAE | 96.26 | 93.60 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| ConvNeXt-based Multi-level Representation Learning | 96.25 | 93.43 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| LPN (block=4) (Wang et al. 2019, migrated) | 88.75 | 75.01 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 85.0 | 62.56 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 68.75 | 49.19 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Satellite-to-Drone (250m)

Rows: **15** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| MEAN | 100.00 | 98.28 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| (MGS)2-Net | 100.00 | 98.73 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| MobileGeo | 98.75 | 94.59 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table II |
| AFMS-Net | 98.75 | 93.55 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| BGG | 98.75 | 98.73 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| MADA-SSA | 98.75 | 97.64 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| Sample4Geo-DPHR | 98.75 | 97.70 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| CGSI (Ours) | 98.75 | 98.01 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| SCOF (Ours) | 98.75 | 96.33 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.50 | 96.03 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| ConvNeXt-based Multi-level Representation Learning | 97.50 | 96.40 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| MFFN-AAE | 96.25 | 94.75 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| LPN (block=4) (Wang et al. 2019, migrated) | 92.5 | 81.34 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 88.75 | 69.96 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 72.5 | 47.94 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

## Satellite-to-Drone (300m)

Rows: **16** (one result row per method/configuration).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 100.00 | 97.66 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| MEAN | 100.00 | 99.21 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| (MGS)2-Net | 100.00 | 98.95 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| Sample4Geo-DPHR | 99.88 | 99.90 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| ConvNeXt-based Multi-level Representation Learning | 98.80 | 97.06 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| BGG | 98.75 | 98.68 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| CGSI (Ours) | 98.75 | 97.92 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| AdaptGeo (DINOv2-Base) | 97.50 | - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| MobileGeo | 97.5 | 96.04 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table II |
| MFFN-AAE | 97.50 | 96.05 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| AFMS-Net | 97.50 | 94.23 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| MADA-SSA | 97.50 | 97.71 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| SCOF (Ours) | 97.50 | 96.62 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 96.25 | 84.16 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LPN (block=4) (Wang et al. 2019, migrated) | 92.5 | 85.72 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| LCM (Ding et al. 2019, migrated) | 75.0 | 59.36 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
