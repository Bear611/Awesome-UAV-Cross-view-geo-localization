# SUES-200

Cross-view geo-localization benchmark (Zhu et al. 2022, IEEE TCSVT). Two retrieval tasks evaluated at four flight heights: Drone→Satellite and Satellite→Drone. Each row reports the original paper's metrics for one method at one altitude. Rows sorted by R@1 descending within each canonical protocol.

## Drone-to-Satellite (150m)

Rows: **18** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| VISION-LANGUAGE | 93.37 | 95.03 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 1 |
| SCOF (Ours) | 90.75 | 92.32 | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 85.30 | 87.58 | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table III |
| ENVIRONMENT-INDEPENDENT | 78.64 | 82.44 | P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement | Table IV summary (text) |
| PARAMETER-EFFICIENT | 78.53 | - | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table IV / Section IV-C2 |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 77.57 | 81.30 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 61.58 | 67.23 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 59.32 | 64.93 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (SUES-200 baseline row), p.11 |
| LCM (Ding et al. 2019, migrated) | 43.42 | 49.65 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| (MGS)2-Net | - | - | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2 |
| AFMS-Net | - | - | Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization | Table 2 |
| BGG | - | - | BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization | Tables II and III |
| Sample4Geo-DPHR | - | - | Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization | Table 2 |
| MADA-SSA | - | - | MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization | Table 2 (Drone→Satellite and Satellite→Drone blocks), mean computed across 150m/200m/250m/300m |
| ConvNeXt-based Multi-level Representation Learning | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
| MFFN-AAE | - | - | Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization | Table III |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
| CGSI (Ours) | - | - | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization | Table IV and Section IV-C-2 text |

## Drone-to-Satellite (200m)

Rows: **9** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| VISION-LANGUAGE | 95.67 | 97.36 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 93.23 | 94.66 | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table III |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 89.50 | 91.40 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 70.85 | 75.96 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 62.30 | 67.24 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 49.42 | 55.91 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| MEAN | - | - | Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization | Tables III and IV (SUES-200 comparisons, Drone→Satellite and Satellite→Drone across 150m/200m/250m/300m) |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
| SCOF (Ours) | - | - | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |

## Drone-to-Satellite (250m)

Rows: **9** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| VISION-LANGUAGE | 96.50 | 97.78 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 96.48 | 97.28 | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table III |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 92.58 | 94.21 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 80.38 | 83.80 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 71.35 | 75.49 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 54.47 | 60.31 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
| CGSI (Ours) | - | - | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization | Table IV and Section IV-C-2 text |
| SCOF (Ours) | - | - | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |

## Drone-to-Satellite (300m)

Rows: **9** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| SCOF (Ours) | 97.85 | 98.10 | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |
| VISION-LANGUAGE | 97.52 | 98.52 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 97.50 | 98.09 | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table III |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.40 | 97.92 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| PARAMETER-EFFICIENT | 93.28 | - | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table IV / Section IV-C2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 81.47 | 84.53 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 77.17 | 80.67 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 60.43 | 65.78 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |

## Satellite-to-Drone (150m)

Rows: **10** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| SCOF (Ours) | 95.00 | - | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 93.75 | 79.49 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| PARAMETER-EFFICIENT | 92.50 | - | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table IV / Section IV-C2 |
| RESOURCE-EFFICIENT | 92.50 | 83.81 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table II |
| ENVIRONMENT-INDEPENDENT | 91.50 | 82.49 | P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement | Table IV summary (text) |
| LPN (block=4) (Wang et al. 2019, migrated) | 83.75 | 66.78 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 82.50 | 58.95 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 57.50 | 38.11 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
| CGSI (Ours) | - | - | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization | Table IV and Section IV-C-2 text |

## Satellite-to-Drone (200m)

Rows: **6** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.50 | 90.52 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| RESOURCE-EFFICIENT | 97.50 | 91.75 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table II |
| LPN (block=4) (Wang et al. 2019, migrated) | 88.75 | 75.01 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 85.00 | 62.56 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 68.75 | 49.19 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |

## Satellite-to-Drone (250m)

Rows: **6** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| RESOURCE-EFFICIENT | 98.75 | 94.59 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table II |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 97.50 | 96.03 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| LPN (block=4) (Wang et al. 2019, migrated) | 92.50 | 81.34 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| SUES-200 Baseline (ResNet-50, no chunking) | 88.75 | 69.96 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LCM (Ding et al. 2019, migrated) | 72.50 | 47.94 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |

## Satellite-to-Drone (300m)

Rows: **8** (one per paper).

| Method | R@1 | AP | Paper | Source |
| --- | ---: | ---: | --- | --- |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 100.00 | 97.66 | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table III, Section IV-D-2 |
| PARAMETER-EFFICIENT | 97.50 | - | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table IV / Section IV-C2 |
| SCOF (Ours) | 97.50 | - | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table IX |
| RESOURCE-EFFICIENT | 97.50 | 96.04 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table II |
| SUES-200 Baseline (ResNet-50, no chunking) | 96.25 | 84.16 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| LPN (block=4) (Wang et al. 2019, migrated) | 92.50 | 85.72 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| LCM (Ding et al. 2019, migrated) | 75.00 | 59.36 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |
| CONVNEXT-BASED | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 3 |
