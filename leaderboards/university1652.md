# University-1652

Cross-view geo-localization benchmark (Zheng et al. 2020, ACM MM'20). Two canonical retrieval protocols: **Drone-to-Satellite** (drone-view target localization) and **Satellite-to-Drone** (drone navigation). Metrics: R@1 / R@5 / R@10 / AP. Multi-weather, ablation, and cross-dataset variants are excluded.

## Drone-to-Satellite

Rows: **40** (one result row per method/configuration).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| SkyPart | 98.43 | - | - | 98.24 | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(a) |
| (MGS)2-Net | 97.6 | - | - | - | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 |
| MobileGeo | 97.15 | - | - | 97.5 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table I |
| BGG | 96.24 | - | - | - | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Table I |
| MADA-SSA | 96.01 | - | - | 92.84 | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 1, Drone→Satellite column |
| CGSI (Ours + Post-process) | 95.90 | - | - | 96.48 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table I, PDF p.9 |
| DINO-GFSA | 95.68 | - | - | 96.34 | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| AGEN | 95.43 | - | - | - | [AGEN: Adaptive Error Control-Driven Cross-View Geo-Localization Under Extreme Weather Conditions](https://doi.org/10.3390/s25123749) | abstract |
| JRN-Geo (k=4) | 95.13 | - | - | 95.85 | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I |
| AdaptGeo (DINOv2-Base) | 94.36 | - | - | - | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table XX / Appendix C |
| MFRGN | 94.33 | - | - | - | [MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization](https://doi.org/10.1145/3664647.3681431) | Table comparing Sample4Geo and MFRGN on Drone2Sat (University-1652) |
| DiffusionUavLoc | 94.1 | - | - | - | [DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization](http://arxiv.org/abs/2511.06422v1) | Table I |
| SDPL | 93.87 | 96.57 | - | 95.13 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 2(a) |
| SCOF | 93.68 | 97.94 | - | 94.68 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table VIII, Table IV, Section IV-C |
| UniABG | 93.62 | - | - | - | [UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization](http://arxiv.org/abs/2511.12054v1) | Table 2 (PDF p7.1) |
| MEAN | 93.55 | - | - | 94.53 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Table I (University-1652 comparisons) |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 92.79 | - | - | - | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table II |
| MFFN-AAE | 92.21 | 97.86 | 98.77 | 90.39 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II |
| GLQINet (ConvNeXt-Tiny) | 91.66 | - | - | - | [Enhancing cross view geo localization through global local quadrant interaction network](https://doi.org/10.1038/s41598-025-18935-6) | Table 1 |
| P2FCN (proposed, ConvNeXt-B) | 91.05 | - | - | 92.34 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table III summary (text) |
| CEUSP | 90.14 | - | - | - | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III |
| ConvNeXt-based Multi-level Representation Learning | 89.79 | - | - | - | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 2 |
| AFMS-Net | 89.63 | - | - | - | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 1 |
| SeGCN | 89.18 | - | - | - | [SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization](https://doi.org/10.1109/jstars.2024.3370612) | Table I |
| MBF | 89.05 | - | - | 90.61 | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper (and Table 11 row for query=1 which mirrors Table 4). |
| MBF | 89.05 | - | - | 90.61 | [UAV’s Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization](https://doi.org/10.3390/s23020720) | Paper abstract and results discussion (text truncated before full table) |
| Heatmap-Guided Swin-Transformer + LightGCN | 88.38 | - | - | 89.37 | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Abstract |
| Proposed (Multibranch Joint Representation Learning with IFSs) | 86.06 | - | - | - | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table II, Section IV-D-1 |
| SDPL (ResNet-50) | 85.19 | - | - | - | [SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization](https://doi.org/10.1109/tcsvt.2024.3424196) | Table IV |
| SA-DOM | 84.08 | - | - | - | [Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization](https://doi.org/10.1109/tgrs.2023.3337383) | Table I, University-1652 Drone->Satellite |
| Baseline (DiNAT-S only) | 83.88 | - | - | 86.54 | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) |
| FCE + MLFM dual-branch Siamese network | - | - | - | 82.38 | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract |
| LRFR | 80.60 | - | - | 83.35 | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 1 (Mean) |
| OriLoc | 80.03 | - | - | 83.95 | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI, p.15518 (PDF p.11) |
| ResNet-101 + cosine similarity | 78.23 | 86.35 | 92.11 | 83.65 | [Improving the Localization Accuracy in Internet of Drones Networks](https://doi.org/10.1109/icicis66182.2025.11313133) | Figure 4 and Table III, PDF p.5 |
| Sample4Geo-DPHR | 74.62 | - | - | 77.87 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 |
| OA+transformer (ablation, proposed method) | 65.66 | - | - | 70.33 | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) |
| SFT | 62.05 | - | - | - | [Satellite-Free Training for Drone-View Geo-Localization](http://arxiv.org/abs/2604.01581v2) | Table 1, p5 |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss) | 58.49 | - | - | - | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) |
| UCVGL-3D (Refined BEV) | 0.23 | - | - | 0.41 | [Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception](http://arxiv.org/abs/2604.01747v1) | Table 1, p.10 |

## Satellite-to-Drone

Rows: **38** (one result row per method/configuration).

| Method | R@1 | R@5 | R@10 | AP | Paper | Source |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| (MGS)2-Net | 98.86 | - | - | - | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 |
| SkyPart | 98.43 | - | - | 98.24 | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(a) |
| DiffusionUavLoc | 98.14 | - | - | - | [DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization](http://arxiv.org/abs/2511.06422v1) | Table I |
| BGG | 97.57 | - | - | - | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Table I |
| JRN-Geo (k=4) | 96.72 | - | - | 94.93 | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I |
| CGSI (Ours + Post-process) | 96.72 | - | - | 96.44 | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table I, PDF p.9 |
| DINO-GFSA | 96.29 | - | - | 95.56 | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) |
| SCOF | 96.29 | - | - | 92.68 | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table VIII |
| MFRGN | 96.15 | - | - | - | [MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization](https://doi.org/10.1145/3664647.3681431) | Table comparing Sample4Geo and MFRGN on Sat2Drone (University-1652) |
| MADA-SSA | 96.01 | - | - | - | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 1, Satellite→Drone column |
| MobileGeo | 95.72 | - | - | 92.57 | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table I |
| Proposed (Joint Representation Learning with Feature Center Region Diffusion and Edge Radiation) | 95.58 | - | - | - | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table II |
| P2FCN (proposed, ConvNeXt-B) | 95.44 | - | - | 87.78 | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table III summary (text) |
| UniABG | 95.43 | - | - | - | [UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization](http://arxiv.org/abs/2511.12054v1) | Table 2 (PDF p7.1) |
| MFFN-AAE | 95.06 | 98.74 | 99.20 | 92.85 | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II |
| ConvNeXt-based Multi-level Representation Learning | 94.87 | - | - | - | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 2 |
| GLQINet (ConvNeXt-Tiny) | 94.58 | - | - | - | [Enhancing cross view geo localization through global local quadrant interaction network](https://doi.org/10.1038/s41598-025-18935-6) | Table 1 |
| SeGCN | 94.29 | - | - | - | [SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization](https://doi.org/10.1109/jstars.2024.3370612) | Table I |
| AdaptGeo (DINOv2-Base) | 93.87 | - | - | 89.12 | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table III / Section IV-C1 |
| Heatmap-Guided Swin-Transformer + LightGCN | 93.76 | - | - | 89.35 | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Abstract |
| MEAN | 93.55 | - | - | 94.53 | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Table I (University-1652 comparisons) |
| CEUSP | 93.3 | - | - | - | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III |
| AFMS-Net | 92.87 | - | - | - | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 1 |
| OriLoc | 92.73 | - | - | 80.75 | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI, p.15518 (PDF p.11) |
| SDPL | 91.87 | 93.44 | - | 91.57 | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 |
| IFS-Net | 91.44 | - | - | - | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table II |
| SA-DOM | 91.44 | - | - | - | [Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization](https://doi.org/10.1109/tgrs.2023.3337383) | Table I, University-1652 Satellite->Drone |
| LRFR | 90.39 | - | - | 80.59 | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 2 (Mean) |
| SDPL (ResNet-50) | 89.3 | - | - | - | [SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization](https://doi.org/10.1109/tcsvt.2024.3424196) | Table IV |
| MBF | 89.05 | - | - | 90.61 | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper. R@5 and R@10 values are taken from Table 11 (Drone→Satellite column with query count=54, which is the standard single-gallery Satellite→Drone evaluation setup per University-1652 conventions). |
| Baseline (DiNAT-S only) | 88.16 | - | - | 82.45 | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) |
| Sample4Geo-DPHR | 86.73 | - | - | 74.93 | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 |
| OA+transformer (ablation, proposed method) | 85.16 | - | - | 69.94 | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) |
| FCE + MLFM dual-branch Siamese network | - | - | - | 77.36 | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss) | 71.18 | - | - | - | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) |
| SFT | 51.07 | - | - | - | [Satellite-Free Training for Drone-View Geo-Localization](http://arxiv.org/abs/2604.01581v2) | Table 1, p5 |
| PLCD | 2.17 | 5.06 | 8.24 | 4.73 | [Proxy-UAV: Bridging the Missing Drone View for Cross-View Geo-Localization](https://doi.org/10.1145/3728482.3757389) | Table 2 |
| CVD (plug-and-play on Sample4Geo backbone) | 0.89 | 3.61 | 5.43 | 1.87 | [Robust Drone-View Geo-Localization via Content-Viewpoint Disentanglement](http://arxiv.org/abs/2505.11822v2) | Table 1, Sample4Geo† row (best backbone for CVD on University-1652) |
