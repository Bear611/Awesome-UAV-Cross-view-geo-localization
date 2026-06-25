# University-1652

Cross-view geo-localization benchmark (Zheng et al. 2020, ACM MM'20). Two canonical retrieval protocols: **Drone-to-Satellite** (drone-view target localization) and **Satellite-to-Drone** (drone navigation). Metrics: R@1 / R@5 / R@10 / AP. Rows sorted by R@1 descending within each protocol. Multi-weather, ablation, and cross-dataset variants are excluded.

## Drone-to-Satellite

Rows: **43** (one per paper).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| SkyPart | 98.43 | - | - | 98.24 | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery | Table 2(a) |
| RESOURCE-EFFICIENT | 97.15 | - | - | 97.50 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table I |
| MADA-SSA | 96.01 | - | - | 92.84 | MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization | Table 1, Drone→Satellite column |
| DINO-GFSA | 95.68 | - | - | 96.34 | DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| GEO-LOCALIZATION | 95.43 | - | - | - | AGEN: Adaptive Error Control-Driven Cross-View Geo-Localization Under Extreme Weather Conditions | abstract |
| JRN-Geo (k=4) | 95.13 | - | - | 95.85 | JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization | Table I |
| AdaptGeo (DINOv2-Base) | 94.36 | - | - | - | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table XX / Appendix C |
| SDPL | 93.87 | 96.57 | - | 95.13 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 2(a) |
| SCOF | 93.68 | 97.94 | - | 94.68 | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table VIII, Table IV, Section IV-C |
| MEAN | 93.55 | - | - | 94.53 | Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization | Table I (University-1652 comparisons) |
| MFFN-AAE | 92.21 | 97.86 | 98.77 | 90.39 | Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization | Table II |
| P2FCN (proposed, ConvNeXt-B) | 91.05 | - | - | 92.34 | P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement | Table III summary (text) |
| MBF | 89.05 | - | - | 90.61 | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper (and Table 11 row for query=1 which mirrors Table 4). |
| MBF | 89.05 | - | - | 90.61 | UAV’s Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Paper abstract and results discussion (text truncated before full table) |
| Heatmap-Guided Swin-Transformer + LightGCN | 88.38 | - | - | 89.37 | A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization | Abstract |
| Ours (Heatmap-guided Swin-Transformer + LightGCN) | 88.38 | - | - | 89.37 | A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization | Table I / Table III |
| Baseline (DiNAT-S only) | 83.88 | - | - | 86.54 | HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization | Table II (Ablation) |
| LRFR | 80.60 | - | - | 83.35 | Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse | Table 1 (Mean) |
| OriLoc | 80.03 | - | - | - | OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization | Table VI 'PERFORMANCE OF CURRENT METHOD ON UNIVERSITY-1652', referenced in text: 'OriLoc achieves competitive results (80.03% R@1 for drone-to-satellite and 92.73% R@1 for satellite-to-drone)'. |
| ResNet-101 + cosine similarity | 78.23 | 86.35 | 92.11 | 83.65 | Improving the Localization Accuracy in Internet of Drones Networks | Abstract |
| Sample4Geo-DPHR | 74.62 | - | - | 77.87 | Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization | Table 1 |
| OA+transformer (ablation, proposed method) | 65.66 | - | - | 70.33 | MixFP:A Transformer-Based Method for UAV Cross-View Geolocation | Table 1 (Ablation study) |
| ResNet-101 backbone with global pooling, 512-D FC embedding, and cosine similarity for retrieval | 58.76 | - | - | 63.29 | Improving the Localization Accuracy in Internet of Drones Networks | Paper 'Improving the Localization Accuracy in Internet of Drones Networks' (ICICIS 2025), Abstract and Fig. 4 / Section IV-B |
| UCVGL-3D (Refined BEV) | 0.23 | - | - | 0.41 | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception | Table 1, p.10 |
| (MGS)2-Net | - | - | - | - | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 |
| AFMS-Net | - | - | - | - | Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization | Table 1 |
| BGG | - | - | - | - | BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization | Table I |
| DiffusionUavLoc | - | - | - | - | DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization | Table I |
| GLQINet (ConvNeXt-Tiny) | - | - | - | - | Enhancing cross view geo localization through global local quadrant interaction network | Table 1 |
| MFRGN | - | - | - | - | MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization | Table comparing Sample4Geo and MFRGN on Drone2Sat (University-1652) |
| ConvNeXt-based Multi-level Representation Learning | - | - | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 2 |
| CEUSP | - | - | - | - | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III |
| SDPL (ResNet-50) | - | - | - | - | SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization | Table IV |
| SFT | - | - | - | - | Satellite-Free Training for Drone-View Geo-Localization | Table 1, p5 |
| SeGCN | - | - | - | - | SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization | Table I |
| SA-DOM | - | - | - | - | Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization | Table I, University-1652 Drone->Satellite |
| UniABG | - | - | - | - | UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization | Table 2 (PDF p7.1) |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss) | - | - | - | - | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) |
| FCE + MLFM dual-branch Siamese network | - | - | - | - | Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining | OpenAlex abstract |
| Proposed (Multibranch Joint Representation Learning with IFSs) | - | - | - | - | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table II, Section IV-D-1 |
| IMPROVING | - | - | - | - | Improving the Localization Accuracy in Internet of Drones Networks | Abstract; Section IV-B; Fig. 4 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | - | - | - | - | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table II |
| CGSI | - | - | - | - | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization | Table I and Section IV-C-1 text |

## Satellite-to-Drone

Rows: **40** (one per paper).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| SkyPart | 98.43 | - | - | 98.24 | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery | Table 2(a) |
| JRN-Geo (k=4) | 96.72 | - | - | 94.93 | JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization | Table I |
| DINO-GFSA | 96.29 | - | - | 95.56 | DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| SCOF | 96.29 | - | - | 92.68 | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization | Table VIII |
| RESOURCE-EFFICIENT | 95.72 | - | - | 92.57 | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization | MobileGeo (Sun et al., 2025), Table I |
| P2FCN (proposed, ConvNeXt-B) | 95.44 | - | - | 87.78 | P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement | Table III summary (text) |
| MFFN-AAE | 95.06 | 98.74 | 99.20 | 92.85 | Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization | Table II |
| AdaptGeo (DINOv2-Base) | 93.87 | - | - | 89.12 | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter | Table III / Section IV-C1 |
| Heatmap-Guided Swin-Transformer + LightGCN | 93.76 | - | - | 89.35 | A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization | Abstract |
| Ours (Heatmap-guided Swin-Transformer + LightGCN) | 93.76 | - | - | 89.35 | A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization | Table I / Table III |
| MEAN | 93.55 | - | - | 94.53 | Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization | Table I (University-1652 comparisons) |
| OriLoc | 92.73 | - | - | - | OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization | Table VI 'PERFORMANCE OF CURRENT METHOD ON UNIVERSITY-1652', referenced in text: 'OriLoc achieves competitive results (80.03% R@1 for drone-to-satellite and 92.73% R@1 for satellite-to-drone)'. |
| SDPL | 91.87 | 93.44 | - | 91.57 | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization | Table 1 |
| LRFR | 90.39 | - | - | 80.59 | Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse | Table 2 (Mean) |
| MBF | 89.05 | - | - | 90.61 | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper. R@5 and R@10 values are taken from Table 11 (Drone→Satellite column with query count=54, which is the standard single-gallery Satellite→Drone evaluation setup per University-1652 conventions). |
| Baseline (DiNAT-S only) | 88.16 | - | - | 82.45 | HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization | Table II (Ablation) |
| Sample4Geo-DPHR | 86.73 | - | - | 74.93 | Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization | Table 1 |
| OA+transformer (ablation, proposed method) | 85.16 | - | - | 69.94 | MixFP:A Transformer-Based Method for UAV Cross-View Geolocation | Table 1 (Ablation study) |
| PLCD | 2.17 | 5.06 | 8.24 | 4.73 | Proxy-UAV: Bridging the Missing Drone View for Cross-View Geo-Localization | Table 2 |
| CVD (plug-and-play on Sample4Geo backbone) | 0.89 | 3.61 | 5.43 | 1.87 | Robust Drone-View Geo-Localization via Content-Viewpoint Disentanglement | Table 1, Sample4Geo† row (best backbone for CVD on University-1652) |
| (MGS)2-Net | - | - | - | - | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 |
| AFMS-Net | - | - | - | - | Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization | Table 1 |
| BGG | - | - | - | - | BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization | Table I |
| DiffusionUavLoc | - | - | - | - | DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization | Table I |
| GLQINet (ConvNeXt-Tiny) | - | - | - | - | Enhancing cross view geo localization through global local quadrant interaction network | Table 1 |
| MADA-SSA | - | - | - | - | MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization | Table 1, Satellite→Drone column |
| MFRGN | - | - | - | - | MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization | Table comparing Sample4Geo and MFRGN on Sat2Drone (University-1652) |
| ConvNeXt-based Multi-level Representation Learning | - | - | - | - | Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching | Table 2 |
| IFS-Net | - | - | - | - | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table II |
| CEUSP | - | - | - | - | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III |
| SDPL (ResNet-50) | - | - | - | - | SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization | Table IV |
| SFT | - | - | - | - | Satellite-Free Training for Drone-View Geo-Localization | Table 1, p5 |
| SeGCN | - | - | - | - | SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization | Table I |
| SA-DOM | - | - | - | - | Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization | Table I, University-1652 Satellite->Drone |
| UniABG | - | - | - | - | UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization | Table 2 (PDF p7.1) |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss) | - | - | - | - | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) |
| FCE + MLFM dual-branch Siamese network | - | - | - | - | Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining | OpenAlex abstract |
| Proposed (Multibranch Joint Representation Learning with IFSs) | - | - | - | - | Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization | Table II, Section IV-D-1 |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | - | - | - | - | Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization | Table II |
| CGSI | - | - | - | 96.44 | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization | Table I (University-1652 comparison) and Section IV-C-1 text |
