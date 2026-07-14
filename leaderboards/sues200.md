# SUES-200

Cross-view geo-localization benchmark (Zhu et al. 2022, IEEE TCSVT). Drone-to-Satellite and Satellite-to-Drone retrieval are ranked separately. The ranking score is the arithmetic mean of R@1 at 150m, 200m, 250m, and 300m; entries missing any altitude are shown as unranked.

## Drone-to-Satellite

Ranked methods: **23**. Ranking = mean R@1 across all four altitudes.

| Rank | Method | Avg R@1 | 150m R@1 / AP | 200m R@1 / AP | 250m R@1 / AP | 300m R@1 / AP | Paper | Source |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | (MGS)2-Net | 99.46 | 98.45 / 98.78 | 99.62 / 99.69 | 99.78 / 99.80 | 100.00 / 100.00 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| 2 | BGG | 99.38 | 99.30 / 99.46 | 99.45 / 99.55 | 99.53 / 99.63 | 99.25 / 99.38 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| 3 | MEAN | 98.09 | 95.50 / 96.46 | 98.38 / 98.72 | 98.95 / 99.17 | 99.52 / 99.63 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| 4 | LQ-KV | 97.55 | 94.70 / 95.70 | 97.93 / 98.34 | 98.73 / 99.02 | 98.85 / 99.11 | [Learnable Query Aggregation with KV Routing for Cross-view Geo-localisation](http://arxiv.org/abs/2512.23938v1) | Table II, rendered PDF p.4 |
| 5 | CGSI (Ours) | 97.28 | 95.95 / 96.80 | 97.72 / 98.15 | 97.60 / 98.03 | 97.83 / 98.23 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| 6 | MFAF (EVA02-L) | 97.25 | 95.22 / 96.30 | 98.80 / 99.08 | 97.50 / 96.87 | 97.50 / 98.42 | [MFAF: An EVA02-Based Multi-scale Frequency Attention Fusion Method for Cross-View Geo-Localization](http://arxiv.org/abs/2509.12673v1) | Table 3, rendered PDF p.11 |
| 7 | Sample4Geo-DPHR | 97.18 | 94.55 / 95.60 | 95.43 / 96.36 | 98.95 / 99.14 | 99.80 / 99.85 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| 8 | SURFNet | 96.52 | 93.63 / 94.84 | 96.20 / 97.01 | 97.58 / 98.10 | 98.68 / 98.94 | SURFNet: A Surface-Aware UAV–Satellite Geolocation Framework via Feature Aggregation and Dual Positional Encoding | Table II, rendered PDF p.8 |
| 9 | SDPL | 95.77 | 93.37 / 95.03 | 95.67 / 97.36 | 96.50 / 97.78 | 97.52 / 98.52 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| 10 | SHAA | 95.38 | 90.32 / 92.09 | 96.50 / 97.16 | 97.30 / 97.71 | 97.40 / 97.93 | SHAA: Spatial Hybrid Attention Network With Adaptive Cross-Entropy Loss Function for UAV-View Geo-Localization | Table V, rendered PDF p.11 |
| 11 | SCOF (Ours) | 94.93 | 90.75 / 92.32 | 94.25 / 95.35 | 96.88 / 97.42 | 97.85 / 98.10 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| 12 | MADA-SSA | 94.17 | 88.12 / 90.44 | 94.17 / 95.31 | 96.65 / 97.38 | 97.72 / 98.25 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| 13 | MCL-Geo | 94.16 | 85.57 / 88.17 | 95.37 / 96.33 | 97.23 / 97.77 | 98.45 / 98.78 | [MCL-Geo: Multi-branch Contrastive Learning for Cross-view Geo-localizationA multi-branch contrastive learning framework plus uniform cross-view contrastive loss for cross-view geo-localization targets.](https://doi.org/10.1145/3652628.3652743) | Table 2, rendered PDF p.6 |
| 14 | DOA | 93.87 | 87.95 / 90.20 | 92.78 / 94.15 | 96.00 / 96.91 | 98.75 / 99.05 | [DOA: Advancing Cross-View Geo-Localization via Domain and Objective Alignment](https://doi.org/10.1109/ijcnn64981.2025.11228462) | Table III, rendered PDF p.8 |
| 15 | MFFN-AAE | 93.26 | 88.07 / 90.82 | 93.75 / 94.81 | 95.07 / 95.98 | 96.15 / 96.83 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| 16 | Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 93.13 | 85.30 / 87.58 | 93.23 / 94.66 | 96.48 / 97.28 | 97.50 / 98.09 | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III |
| 17 | APA-BI | 92.67 | 86.45 / 88.90 | 91.85 / 93.54 | 95.70 / 96.62 | 96.70 / 97.37 | [APA-BI Adaptive Partition Aggregation and Bidirectional Integration for UAV-View Geo-Localization](https://www.semanticscholar.org/search?q=APA-BI%20Adaptive%20Partition%20Aggregation%20and%20Bidirectional%20Integration%20for%20UAV-View%20Geo-Localization) | Table III, rendered PDF p.5 |
| 18 | AFMS-Net | 90.72 | 85.25 / 88.24 | 90.53 / 92.24 | 93.03 / 94.32 | 94.05 / 95.25 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| 19 | ConvNeXt-based Multi-level Representation Learning | 90.62 | 83.05 / 86.00 | 89.65 / 91.81 | 94.05 / 95.62 | 95.75 / 96.30 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| 20 | Proposed (Multibranch Joint Representation Learning with IFSs) | 89.26 | 77.57 / 81.30 | 89.50 / 91.40 | 92.58 / 94.21 | 97.40 / 97.92 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| 21 | LPN (block=4) (Wang et al. 2019, migrated) | 73.57 | 61.58 / 67.23 | 70.85 / 75.96 | 80.38 / 83.8 | 81.47 / 84.53 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| 22 | SUES-200 Baseline (ResNet-50, no chunking) | 67.53 | 59.32 / 64.93 | 62.3 / 67.24 | 71.35 / 75.49 | 77.17 / 80.67 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (SUES-200 baseline row), p.11; Table VII, p.11 |
| 23 | LCM (Ding et al. 2019, migrated) | 51.94 | 43.42 / 49.65 | 49.42 / 55.91 | 54.47 / 60.31 | 60.43 / 65.78 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

### Unranked: incomplete altitude coverage

These entries are retained for evidence, but no four-altitude average or rank is assigned.

| Method | Available altitude(s) | R@1 / AP | Paper | Source |
|---|---|---|---|---|
| AdaptGeo (DINOv2-Base) | 150m, 300m | 150m: 78.53 / -; 300m: 93.28 / - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| P2FCN (proposed, ConvNeXt-B) | 150m | 150m: 78.64 / 82.44 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) |

## Satellite-to-Drone

Ranked methods: **22**. Ranking = mean R@1 across all four altitudes.

| Rank | Method | Avg R@1 | 150m R@1 / AP | 200m R@1 / AP | 250m R@1 / AP | 300m R@1 / AP | Paper | Source |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | (MGS)2-Net | 99.69 | 98.75 / 96.50 | 100.00 / 98.51 | 100.00 / 98.73 | 100.00 / 98.95 | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2, arXiv v2 PDF p.11 |
| 2 | MEAN | 99.38 | 97.50 / 94.75 | 100.00 / 97.09 | 100.00 / 98.28 | 100.00 / 99.21 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV, PDF p.10 |
| 3 | BGG | 98.75 | 98.75 / 98.22 | 98.75 / 98.24 | 98.75 / 98.73 | 98.75 / 98.68 | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III, PDF p.8 |
| 4 | LQ-KV | 98.75 | 98.75 / 95.61 | 98.75 / 97.70 | 98.75 / 98.47 | 98.75 / 98.91 | [Learnable Query Aggregation with KV Routing for Cross-view Geo-localisation](http://arxiv.org/abs/2512.23938v1) | Table II, rendered PDF p.4 |
| 5 | APA-BI | 98.44 | 97.50 / 86.21 | 98.75 / 94.03 | 98.75 / 96.95 | 98.75 / 97.82 | [APA-BI Adaptive Partition Aggregation and Bidirectional Integration for UAV-View Geo-Localization](https://www.semanticscholar.org/search?q=APA-BI%20Adaptive%20Partition%20Aggregation%20and%20Bidirectional%20Integration%20for%20UAV-View%20Geo-Localization) | Table III, rendered PDF p.5 |
| 6 | CGSI (Ours) | 98.44 | 97.50 / 96.22 | 98.75 / 97.62 | 98.75 / 98.01 | 98.75 / 97.92 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table IV, PDF p.10 |
| 7 | DOA | 98.44 | 96.25 / 90.02 | 98.75 / 95.13 | 98.75 / 97.06 | 100.00 / 98.12 | [DOA: Advancing Cross-View Geo-Localization via Domain and Objective Alignment](https://doi.org/10.1109/ijcnn64981.2025.11228462) | Table III, rendered PDF p.8 |
| 8 | SHAA | 98.44 | 97.50 / 91.50 | 98.75 / 95.68 | 98.75 / 97.45 | 98.75 / 97.31 | SHAA: Spatial Hybrid Attention Network With Adaptive Cross-Entropy Loss Function for UAV-View Geo-Localization | Table V, rendered PDF p.11 |
| 9 | MFAF (EVA02-L) | 98.12 | 97.50 / 96.87 | 97.50 / 98.03 | 98.75 / 97.98 | 98.75 / 98.72 | [MFAF: An EVA02-Based Multi-scale Frequency Attention Fusion Method for Cross-View Geo-Localization](http://arxiv.org/abs/2509.12673v1) | Table 3, rendered PDF p.11 |
| 10 | AFMS-Net | 97.88 | 96.50 / 82.83 | 98.75 / 92.01 | 98.75 / 93.55 | 97.50 / 94.23 | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2, PDF p.18 |
| 11 | MADA-SSA | 97.81 | 96.25 / 87.33 | 98.75 / 96.12 | 98.75 / 97.64 | 97.50 / 97.71 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2, PDF p.15 |
| 12 | Sample4Geo-DPHR | 97.78 | 95.00 / 90.73 | 97.50 / 94.41 | 98.75 / 97.70 | 99.88 / 99.90 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2, arXiv v3 PDF p.4 |
| 13 | SURFNet | 97.50 | 95.00 / 90.75 | 97.50 / 94.78 | 98.75 / 96.42 | 98.75 / 97.87 | SURFNet: A Surface-Aware UAV–Satellite Geolocation Framework via Feature Aggregation and Dual Positional Encoding | Table II, rendered PDF p.8 |
| 14 | Proposed (Multibranch Joint Representation Learning with IFSs) | 97.19 | 93.75 / 79.49 | 97.50 / 90.52 | 97.50 / 96.03 | 100.00 / 97.66 | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 |
| 15 | SCOF (Ours) | 97.19 | 95.00 / 89.92 | 97.50 / 93.13 | 98.75 / 96.33 | 97.50 / 96.62 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX, PDF p.11 |
| 16 | ConvNeXt-based Multi-level Representation Learning | 96.89 | 95.00 / 91.82 | 96.25 / 93.43 | 97.50 / 96.40 | 98.80 / 97.06 | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3, PDF p.9 |
| 17 | MobileGeo | 96.56 | 92.5 / 83.81 | 97.5 / 91.75 | 98.75 / 94.59 | 97.5 / 96.04 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table II |
| 18 | MFFN-AAE | 96.25 | 95.00 / 88.23 | 96.26 / 93.60 | 96.25 / 94.75 | 97.50 / 96.05 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III |
| 19 | MCL-Geo | 95.93 | 90.00 / 84.11 | 96.75 / 93.45 | 98.23 / 97.63 | 98.75 / 97.74 | [MCL-Geo: Multi-branch Contrastive Learning for Cross-view Geo-localizationA multi-branch contrastive learning framework plus uniform cross-view contrastive loss for cross-view geo-localization targets.](https://doi.org/10.1145/3652628.3652743) | Table 2, rendered PDF p.6 |
| 20 | LPN (block=4) (Wang et al. 2019, migrated) | 89.38 | 83.75 / 66.78 | 88.75 / 75.01 | 92.5 / 81.34 | 92.5 / 85.72 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LPN row), p.11 |
| 21 | SUES-200 Baseline (ResNet-50, no chunking) | 88.12 | 82.5 / 58.95 | 85.0 / 62.56 | 88.75 / 69.96 | 96.25 / 84.16 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII, p.11 |
| 22 | LCM (Ding et al. 2019, migrated) | 68.44 | 57.5 / 38.11 | 68.75 / 49.19 | 72.5 / 47.94 | 75.0 / 59.36 | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments (Zhu et al. 2022 — SUES-200 paper) | Table VII (LCM row), p.11 |

### Unranked: incomplete altitude coverage

These entries are retained for evidence, but no four-altitude average or rank is assigned.

| Method | Available altitude(s) | R@1 / AP | Paper | Source |
|---|---|---|---|---|
| AdaptGeo (DINOv2-Base) | 150m, 300m | 150m: 92.50 / -; 300m: 97.50 / - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 |
| P2FCN (proposed, ConvNeXt-B) | 150m | 150m: 91.50 / 82.49 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) |
