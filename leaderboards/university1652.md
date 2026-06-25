# University-1652

University-1652 is a multi-view multi-source benchmark for drone-based cross-view geo-localization (Zheng et al. MM'20). The canonical protocols defined by the original paper are **Drone-to-Satellite** (drone-view target localization) and **Satellite-to-Drone** (drone navigation). Multi-weather variants are robustness benchmarks from follow-up papers (e.g., DiffLoc 2024).

Each row shows the original paper's reported R@1 / R@5 / R@10 / AP values. Rows are sorted by R@1 descending within each protocol. Ablations, baselines, and sensitivity studies are excluded — only each paper's flagship result on the canonical protocol is shown.

## Drone-to-Satellite

Rows: **11** (one per paper).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
|---|---:|---:|---:|---:|---|---|
| MADA-SSA | 96.01 | - | - | 92.84 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 1, Drone→Satellite column |
| DINO-GFSA | 95.68 | - | - | 96.34 | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| JRN-Geo (k=4) | 95.13 | - | - | 95.85 | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I |
| VISION-LANGUAGE | 93.87 | 96.57 | - | 95.13 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 2(a) |
| MFFN-AAE | 92.21 | 97.86 | 98.77 | 90.39 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II |
| Ours (Heatmap-guided Swin-Transformer + LightGCN) | 88.38 | - | - | 89.37 | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Table I / Table III |
| UAV-SATELLITE | 83.88 | - | - | 86.54 | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) |
| ResNet-101 + cosine similarity | 78.23 | 86.35 | 92.11 | 83.65 | [Improving the Localization Accuracy in Internet of Drones Networks](https://doi.org/10.1109/icicis66182.2025.11313133) | Abstract |
| Sample4Geo-DPHR | 74.62 | - | - | 77.87 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 |
| OA+transformer (ablation, proposed method) | 65.66 | - | - | 70.33 | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) |
| FCE + MLFM dual-branch Siamese network | - | - | - | - | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract |

## Satellite-to-Drone

Rows: **9** (one per paper).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
|---|---:|---:|---:|---:|---|---|
| JRN-Geo (k=4) | 96.72 | - | - | 94.93 | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I |
| DINO-GFSA | 96.29 | - | - | 95.56 | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| MFFN-AAE | 95.06 | 98.74 | 99.20 | 92.85 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II |
| Ours (Heatmap-guided Swin-Transformer + LightGCN) | 93.76 | - | - | 89.35 | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Table I / Table III |
| VISION-LANGUAGE | 91.87 | 93.44 | - | 91.57 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| UAV-SATELLITE | 88.16 | - | - | 82.45 | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) |
| Sample4Geo-DPHR | 86.73 | - | - | 74.93 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 |
| OA+transformer (ablation, proposed method) | 85.16 | - | - | 69.94 | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) |
| FCE + MLFM dual-branch Siamese network | - | - | - | - | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract |
