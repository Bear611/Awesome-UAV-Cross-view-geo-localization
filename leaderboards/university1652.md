# University-1652

Leaderboard for University-1652. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## D2S (drone-to-satellite)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 2(a) | R@1=95.28 | false | Ablation: full SkyLink with soft labels and similarity threshold |

## Drone Localization (Drone → Satellite)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| MBF<br><sub>not specified in text (Siamese two-branch, Hybrid ViT backbone, multimodal + HBP)</sub> | [UAV’s Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization](https://doi.org/10.3390/s23020720) | Paper abstract and results discussion (text truncated before full table) | R@1=89.05 | false | Headline number stated in abstract: 'recall@1 accuracy achieves 89.05% in drone localization task' |

## Drone Navigation (Satellite → Drone)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| MBF<br><sub>not specified in text (Siamese two-branch, Hybrid ViT backbone, multimodal + HBP)</sub> | [UAV’s Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization](https://doi.org/10.3390/s23020720) | Paper abstract and results discussion (text truncated before full table) | R@1=93.15 | false | Headline number stated in abstract: '93.15% in drone navigation task in University-1652' |

## Drone-to-Satellite

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| FCE + MLFM dual-branch Siamese network<br><sub>supervised metric learning (Siamese, not explicitly specified)</sub> | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract | AP=82.38 | false | Abstract states 'improvements are observed in R@1, R@5 and R@10 metrics' but does not provide specific numerical values; only AP value reported. |

## Drone→Satellite

Rows: **6**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| RESOURCE-EFFICIENT | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table I | R@1=97.15 | false | - |
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table II | R@1=92.79 | false | Drone target localization task; improvement of 0.14% R@1 and 0.1% AP over Sample4Geo |
| UAV-SATELLITE<br><sub>trained on University-1652 train split</sub> | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) | R@1=83.88 | false | Full model: DiNAT-S + MSCM + Attention-Guided Module |
| WEATHER-INVARIANT<br><sub>X-VLM</sub> | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 1 (Mean) | R@1=80.60 | false | +3.46% R@1 and +3.15% AP over baseline |
| OA+transformer (ablation, proposed method)<br><sub>ablation study (with orientation alignment, transformer backbone)</sub> | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) | R@1=65.66 | false | Recall@1 and AP reported in %; OA = orientation alignment strategy |
| GEO-LOCALIZATION<br><sub>Trained on University-1652 (DinoV2 backbone, BERT text encoder, 392x392 input)</sub> | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table I and Section IV-C-1 text | R@1= | false | Text states Recall@1 exceeds second-best SRLN by 3.2%, but absolute value not given in text. |

## Drone→Satellite (D2S)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Large + adapter, InfoNCE loss, increased batch size, optimized optimizer/learning rate</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table XX / Appendix C | R@1=94.36 | false | Surpasses Sample4Geo (92.65%) with advanced training strategy; no architecture changes |

## Drone→Satellite (Drone Localization)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (Heatmap-guided Swin-Transformer + LightGCN)<br><sub>Trained on University-1652 train set, input 256×256, 200 epochs, SGD lr=1e-2 momentum=0.9 wd=5e-4, NVIDIA 4060 GPU, test-time augmentation</sub> | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Table I / Table III | R@1=88.38 | false | Published 2025, input 256×256; 38.7M params, ~37ms latency; 3-layer LightGCN |

## Drone→Satellite (drone-view target localization)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table II, Section IV-D-1 | R@1=86.06 | false | Compared with LPN: R@1 improved by 10.13% and AP by 8.94%; vs Swin-B: +1.91% R@1, +1.46% AP; vs FSRA: +1.55% R@1, +1.37% AP |

## Drone→Satellite (mean across 10 environmental styles)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table III summary (text) | R@1=91.05 | false | Mean over 10 environmental styles; pop. variance R@1=2.90, AP=2.28 |

## Drone→Satellite (mean across 10 environmental styles, Swin-B backbone)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, Swin-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IX (text) | R@1=85.47 | false | Baseline Swin-B mean R@1=77.34; +8.13 improvement |

## Drone→Satellite (mean across 10 environmental styles, ViT-B backbone)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ViT-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IX (text) | R@1=81.91 | false | Baseline ViT-B mean R@1=75.76; +6.15 improvement |

## Drone→Satellite (mean across 10 environmental styles, ablation: +MCFGM)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B, MCFGM module only</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table VI (text, deltas only) | R@1= | false | Delta over baseline: +1.33 R@1, +1.19 AP (D→S). Absolute values not reported in text. |

## Drone→Satellite (mean across 10 environmental styles, ablation: +SNDS)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B, SNDS module only</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table VI (text, deltas only) | R@1= | false | Delta over baseline: +1.05 R@1, +0.93 AP (D→S); +1.22 R@1, +2.77 AP (S→D). Absolute values not reported in text. |

## Drone→Satellite (mean across 10 environmental styles, ablation: n=8 parts)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, n=8 parts</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table X (text) | R@1=91.05 | false | Best part count; pop. variance R@1=2.90, AP=2.28 |

## Drone→Satellite (unseen weather: fog+rain+snow mixed)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, trained on seen environments</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table V | R@1=88.10 | false | Unseen combined weather condition |

## Drone→Satellite Retrieval

Rows: **26**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| (MGS)2-Net<br><sub>Trained on University-1652 official train split (701 buildings)</sub> | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 | R@1=97.6 | false | Test image size 336x336. R@5 and R@10 not reported in the paper table. |
| SkyPart<br><sub>Trained on University-1652 standard 701/951 split, no re-ranking, no TTA, single-pass</sub> | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(a) | R@1=96.47 | false | Main deployed checkpoint, 26.95M params, 448x448 single-scale crop, cosine similarity, no post-processing. R@5/R@10 not reported in main table; only R@1 and AP are available. |
| BGG<br><sub>Supervised, DINOv3 ViT-B/16 backbone (frozen) with MFEA + FASA adapters trained on University-1652 train split (701 buildings). Input 384x384, InfoNCE loss.</sub> | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Table I | R@1=96.24 | false | Table I reports R@1 and AP directly. R@5 and R@10 are not explicitly listed in the paper text; values shown are best-effort from the table's reported entries. Verified final flagship row. |
| DINO-GFSA<br><sub>Trained on official University-1652 train split (701 buildings), input 224x224, LoRA-adapted DINOv3 ViT-L backbone, InfoNCE loss, 80 epochs, single-pass retrieval, no TTA/re-ranking.</sub> | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) | R@1=95.68 | false | R@5 and R@10 are not reported in the paper table for DINO-GFSA on this protocol; only R@1 and AP are available. |
| JRN-Geo (k=4)<br><sub>Official 701/951 split, ConvNeXt-Base backbone, RGB+Normal inputs with 3D geographic augmentation factor k=4</sub> | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I | R@1=95.13 | false | JRN-Geo (k=4) row from Table I; R@5 and R@10 not reported in the paper |
| MFRGN<br><sub>Standard 701/951 split (same-area evaluation)</sub> | [MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization](https://doi.org/10.1145/3664647.3681431) | Table comparing Sample4Geo and MFRGN on Drone2Sat (University-1652) | R@1=94.33 | false | R@5 and R@10 not reported in the table; only R@1 and AP are available. |
| DiffusionUavLoc<br><sub>supervised (drone + satellite only, official 701/951 split)</sub> | [DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization](http://arxiv.org/abs/2511.06422v1) | Table I | R@1=94.1 | false | R@5 and R@10 are not reported in the paper for this direction. |
| UniABG<br><sub>unsupervised</sub> | [UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization](http://arxiv.org/abs/2511.12054v1) | Table 2 (PDF p7.1) | R@1=93.62 | false | Unsupervised cross-view retrieval on the standard 701/951 split. R@5 and R@10 not reported by the paper. |
| MEAN<br><sub>Supervised, standard 701/951 split, drone + satellite images, ConvNeXt-Tiny backbone</sub> | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Table I (University-1652 comparisons) | R@1=93.55 | false | Paper does not report R@5/R@10 in Table I for University-1652. |
| MADA-SSA<br><sub>supervised, standard 701/951 split, weight-sharing ConvNeXt-Base backbone, drone+satellite only, 384x384 input</sub> | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 1, Drone→Satellite column | R@1=93.26 | false | Flagship result on standard protocol. R@5 and R@10 not reported in the paper. |
| Sample4Geo-DPHR<br><sub>Sample4Geo backbone with DPHR reweighting strategy, standard 701/951 split</sub> | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 | R@1=92.32 | false | DPHR applied to Sample4Geo baseline; R@5/R@10 not reported in paper. |
| GLQINet (ConvNeXt-Tiny)<br><sub>Supervised, ConvNeXt-Tiny backbone pre-trained on ImageNet, standard 701/951 split, drone and satellite only</sub> | [Enhancing cross view geo localization through global local quadrant interaction network](https://doi.org/10.1038/s41598-025-18935-6) | Table 1 | R@1=91.66 | false | R@5 and R@10 not reported in main text for this paper. |
| CEUSP<br><sub>ConvNeXt-T backbone; trained on the official University-1652 701/951 split using only drone and satellite imagery; 256×256 inputs; single-pass retrieval.</sub> | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III | R@1=90.14 | false | R@5 and R@10 are not reported in the paper for this protocol and are therefore omitted. |
| ConvNeXt-based Multi-level Representation Learning<br><sub>Supervised, ConvNeXt-Tiny backbone, input size 256x256, standard 701/951 split, drone+satellite only</sub> | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 2 | R@1=89.79 | false | Flagship 256x256 result reported in the paper. R@5 and R@10 not reported by the authors. |
| AFMS-Net<br><sub>ViT-S backbone pretrained on ImageNet; 120 epochs, SGD, batch size 8, standard 701/951 split</sub> | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 1 | R@1=89.63 | false | R@5 and R@10 are not reported in the paper; only R@1 and AP are available. |
| MFFN-AAE<br><sub>Swin-B backbone, standard 701/951 split, drone+satellite only, single-pass retrieval</sub> | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II | R@1=89.59 | false | R@5 and R@10 values read from Table VI (single-query, query=1 row) since the main table only reports R@1 and AP for the proposed method. |
| SeGCN<br><sub>SwinV2-T backbone, shared-weight siamese, trained with instance loss + triplet loss on standard 701/951 split, 256x256 input</sub> | [SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization](https://doi.org/10.1109/jstars.2024.3370612) | Table I | R@1=89.18 | false | Flagship result from Table I on the standard University-1652 Drone→Satellite protocol. R@5 and R@10 not reported in the paper. |
| MBF<br><sub>Standard 701/951 train/test split, drone and satellite only, Hybrid ViT backbone pretrained on ImageNet, 384x384 input, SGD optimizer, single-pass retrieval with cosine distance.</sub> | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper (and Table 11 row for query=1 which mirrors Table 4). | R@1=89.05 | false | Table 4 reports R@1, AP, R@1, AP for D→S and S→D. R@5 and R@10 are taken from the multiple-query table (Table 11) at query=1, which corresponds to the single-query setting and is consistent with the paper's reported R@1=89.05 and AP=90.61. |
| Heatmap-Guided Swin-Transformer + LightGCN<br><sub>Official 701/951 split; drone and satellite images only</sub> | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Abstract | R@1=88.38 | false | Abstract-reported headline result; R@5 and R@10 not reported in supplied text, so they are unavailable. |
| SDPL (ResNet-50)<br><sub>ResNet-50 backbone, 512x512, standard 701/951 split, single-pass retrieval</sub> | [SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization](https://doi.org/10.1109/tcsvt.2024.3424196) | Table IV | R@1=85.19 | false | Primary SDPL flagship result on University-1652 with ResNet-50 backbone. |
| SA-DOM<br><sub>Trained on University-1652 standard 701/951 split, ResNet-50 backbone, 256x256 input, SAS preprocessing, HAB attention, Deconstruction+Center+CE loss</sub> | [Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization](https://doi.org/10.1109/tgrs.2023.3337383) | Table I, University-1652 Drone->Satellite | R@1=84.08 | false | Paper's flagship result on the standard test split. |
| OriLoc<br><sub>Standard 701/951 train/test split; drone and satellite views only (no ground-view training); Swin-T backbone, 384-d embeddings</sub> | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI 'PERFORMANCE OF CURRENT METHOD ON UNIVERSITY-1652', referenced in text: 'OriLoc achieves competitive results (80.03% R@1 for drone-to-satellite and 92.73% R@1 for satellite-to-drone)'. | R@1=80.03 | false | R@5, R@10, and AP values for OriLoc on University-1652 are not extractable from the provided full-text/table evidence (Table VI content not included in the extracted text). Only R@1 is clearly stated in the prose. |
| UCVGL-3D (Refined BEV)<br><sub>Zero-shot (DINOv2 + VGGT foundation models, no fine-tuning on University-1652)</sub> | [Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception](http://arxiv.org/abs/2604.01747v1) | Table 1, p.10 | R@1=79.0 | false | Multi-view UAV query (12 frames) used rather than single-image query; reported as Drone→Satellite direction. Satellite→Drone direction not reported. RIoU metrics are non-standard and excluded. |
| ResNet-101 + cosine similarity<br><sub>Trained on University-1652 standard split (701/951), ResNet-101 backbone, cosine similarity</sub> | [Improving the Localization Accuracy in Internet of Drones Networks](https://doi.org/10.1109/icicis66182.2025.11313133) | Abstract | R@1=78.23 | false | The paper does not explicitly state whether these numbers correspond to Drone→Satellite or Satellite→Drone retrieval. The task is described as UAV-to-satellite matching, and the numbers are reported only in the abstract, not in a detailed table. The standard 701/951 split is implied but not confirmed. Inclusion is based on the most likely interpretation (Drone→Satellite). |
| SFT<br><sub>Satellite-free training; multi-view UAV sequences reconstructed via 3DGS into pseudo-orthophotos, DINOv3 + Fisher vector aggregation learned from drone data only</sub> | [Satellite-Free Training for Drone-View Geo-Localization](http://arxiv.org/abs/2604.01581v2) | Table 1, p5 | R@1=62.05 | false | Uses multi-view UAV sequence reconstruction into a single pseudo-orthophoto as the location-level query, which deviates from the standard single oblique drone image query protocol. Standard 701/951 split is used. |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss)<br><sub>Satellite+Drone+Ground, shared weights, 256x256 input, instance loss</sub> | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) | R@1=58.49 | false | Flagship single-query single-pass retrieval. R@5 not reported in the paper's tables. |

## Ground → Satellite (cross-view retrieval)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| STREET-SATELLITE<br><sub>DINOv2-L backbone (full model with GREM, PAFA, SSL, MSBM)</sub> | [SkyLink: Unifying Street-Satellite Geo-Localization via UAV-Mediated 3D Scene Alignment](http://arxiv.org/abs/2509.24783v1) | Table 1 | R@1=27.06 | false | Proposed SkyLink full method, state-of-the-art on University-1652; also achieves 25.75% Recall@1 in UAVM2025 Challenge |

## Ground-to-Satellite Retrieval (drone-absent)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>Transformer-based proxy generator + uncertainty-aware adapter; PLCD cross-diffusion backend; drone images unavailable at inference</sub> | [Proxy-UAV: Bridging the Missing Drone View for Cross-View Geo-Localization](https://doi.org/10.1145/3728482.3757389) | Table 2 | R@1=2.17 | false | Proposed method; reported as percentages; mAP is the AP column. |

## S2D (satellite-to-drone)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 | R@1=93.58 | false | SkyLink re-ranking with Qwen2-VL-7B-Instruct backbone |

## Satellite-to-Drone

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| FCE + MLFM dual-branch Siamese network<br><sub>supervised metric learning (Siamese, not explicitly specified)</sub> | [Enhancing Semantic Information Representation in Multi‐View Geo‐Localization through Dual‐Branch Network with Feature Consistency Enhancement and Multi‐Level Feature Mining](https://doi.org/10.1049/ipr2.70071) | OpenAlex abstract | AP=77.36 | false | Abstract states 'improvements are observed in R@1, R@5 and R@10 metrics' but does not provide specific numerical values; only AP value reported. |

## Satellite→Drone

Rows: **6**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>Trained on University-1652 (DinoV2 backbone, BERT text encoder, 392x392 input)</sub> | [CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generalizable Cross-View Geo-Localization](https://doi.org/10.1109/TCSVT.2025.3604002) | Table I (University-1652 comparison) and Section IV-C-1 text | AP=96.44 | false | Reported in text as CGSI AP=96.44%, surpassing SRLN by 4.47%; with re-ranking post-processing AP further improves by 1.06% (to ~97.50%). Other Rank@K values not explicitly stated in text. |
| RESOURCE-EFFICIENT | [MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-Efficient Cross-view Drone Geo-Localization](https://www.semanticscholar.org/search?q=MobileGeo%20Exploring%20Hierarchical%20Knowledge%20Distillation%20for%20Resource-Efficient%20Cross-view%20Drone%20Geo-Localization) | MobileGeo (Sun et al., 2025), Table I | R@1=95.72 | false | - |
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table II | R@1=95.58 | false | Drone navigation task; improvement of 0.44% R@1 and 0.78% AP over Sample4Geo |
| WEATHER-INVARIANT<br><sub>X-VLM</sub> | [Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization with GeoFuse](https://openalex.org/W7161451916) | Table 2 (Mean) | R@1=90.39 | false | +2.67% R@1 and +4.20% AP over baseline |
| UAV-SATELLITE<br><sub>trained on University-1652 train split</sub> | [HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-localization](https://doi.org/10.1109/cac67268.2025.11487588) | Table II (Ablation) | R@1=88.16 | false | Full model: DiNAT-S + MSCM + Attention-Guided Module |
| OA+transformer (ablation, proposed method)<br><sub>ablation study (with orientation alignment, transformer backbone)</sub> | [MixFP:A Transformer-Based Method for UAV Cross-View Geolocation](https://doi.org/10.1007/978-3-032-16823-8_11) | Table 1 (Ablation study) | R@1=85.16 | false | Recall@1 and AP reported in %; OA = orientation alignment strategy |

## Satellite→Drone (Drone Navigation)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| Ours (Heatmap-guided Swin-Transformer + LightGCN)<br><sub>Trained on University-1652 train set, input 256×256, 200 epochs, SGD lr=1e-2 momentum=0.9 wd=5e-4, NVIDIA 4060 GPU, test-time augmentation</sub> | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Table I / Table III | R@1=93.76 | false | Published 2025, input 256×256; 38.7M params, ~37ms latency; 3-layer LightGCN |

## Satellite→Drone (S2D)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Large + adapter, SGD, 200 epochs, batch 8, triplet+KL+CE loss</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table III / Section IV-C1 | R@1=93.87 | false | Primary model, trains 11M parameters |

## Satellite→Drone (drone navigation)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table II, Section IV-D-1 | R@1=91.44 | false | Compared with LPN: R@1 improved by 4.99% and AP by 11.24%; vs Swin-B: +1.14% R@1, +2.18% AP; vs FSRA: +2.99% R@1, +2.26% AP |

## Satellite→Drone (population variance across 10 environmental styles)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table III summary (text) | R@1= | false | Variance values only: R@1 var=0.15, AP var=3.64; mean R@1 reported as similar to DAC |

## Satellite→Drone (unseen weather: fog+rain+snow mixed)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, trained on seen environments</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table V | R@1=95.44 | false | Unseen combined weather condition |

## Satellite→Drone Retrieval

Rows: **26**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| (MGS)2-Net<br><sub>Trained on University-1652 official train split (701 buildings)</sub> | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 1 | R@1=98.86 | false | Test image size 336x336. R@5 and R@10 not reported in the paper table. |
| SkyPart<br><sub>Trained on University-1652 standard 701/951 split, no re-ranking, no TTA, single-pass</sub> | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 2(a) | R@1=98.43 | false | Main deployed checkpoint. R@5/R@10 not reported in main table; only R@1 and AP are available. |
| DiffusionUavLoc<br><sub>supervised (drone + satellite only, official 701/951 split)</sub> | [DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization](http://arxiv.org/abs/2511.06422v1) | Table I | R@1=98.14 | false | R@5 and R@10 are not reported in the paper for this direction. |
| BGG<br><sub>Supervised, DINOv3 ViT-B/16 backbone (frozen) with MFEA + FASA adapters trained on University-1652 train split (701 buildings). Input 384x384, symmetric InfoNCE loss.</sub> | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Table I | R@1=97.57 | false | R@5 and R@10 are not explicitly listed in the paper text; values shown are best-effort from the table's reported entries. |
| JRN-Geo (k=4)<br><sub>Official 701/951 split, ConvNeXt-Base backbone, RGB+Normal inputs with 3D geographic augmentation factor k=4</sub> | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table I | R@1=96.72 | false | JRN-Geo (k=4) row from Table I; R@5 and R@10 not reported in the paper |
| DINO-GFSA<br><sub>Trained on official University-1652 train split (701 buildings), input 224x224, LoRA-adapted DINOv3 ViT-L backbone, InfoNCE loss, 80 epochs, single-pass retrieval, no TTA/re-ranking.</sub> | [DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential Aggregation](http://arxiv.org/abs/2606.00784v1) | Table 1 (DINO-GFSA / DINOv3-ViT-L row) | R@1=96.29 | false | R@5 and R@10 are not reported in the paper table for DINO-GFSA on this protocol; only R@1 and AP are available. |
| MFRGN<br><sub>Standard 701/951 split (same-area evaluation)</sub> | [MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-Aerial Geo-localization](https://doi.org/10.1145/3664647.3681431) | Table comparing Sample4Geo and MFRGN on Sat2Drone (University-1652) | R@1=96.15 | false | R@5 and R@10 not reported in the table; only R@1 and AP are available. |
| MADA-SSA<br><sub>supervised, standard 701/951 split, weight-sharing ConvNeXt-Base backbone, drone+satellite only, 384x384 input</sub> | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 1, Satellite→Drone column | R@1=96.01 | false | Flagship result on standard protocol. R@5 and R@10 not reported in the paper. |
| MEAN<br><sub>Supervised, standard 701/951 split, drone + satellite images, ConvNeXt-Tiny backbone</sub> | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Table I (University-1652 comparisons) | R@1=96.01 | false | Paper does not report R@5/R@10 in Table I for University-1652. |
| UniABG<br><sub>unsupervised</sub> | [UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization](http://arxiv.org/abs/2511.12054v1) | Table 2 (PDF p7.1) | R@1=95.43 | false | Unsupervised cross-view retrieval on the standard 701/951 split. R@5 and R@10 not reported by the paper. |
| CVD (plug-and-play on Sample4Geo backbone)<br><sub>Standard 701/951 train/test split, drone-satellite only, single-pass retrieval</sub> | [Robust Drone-View Geo-Localization via Content-Viewpoint Disentanglement](http://arxiv.org/abs/2505.11822v2) | Table 1, Sample4Geo† row (best backbone for CVD on University-1652) | R@1=95.26 | false | Satellite→Drone direction reported in Table 1. |
| ConvNeXt-based Multi-level Representation Learning<br><sub>Supervised, ConvNeXt-Tiny backbone, input size 256x256, standard 701/951 split, drone+satellite only</sub> | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 2 | R@1=94.87 | false | Flagship 256x256 result reported in the paper. R@5 and R@10 not reported by the authors. |
| GLQINet (ConvNeXt-Tiny)<br><sub>Supervised, ConvNeXt-Tiny backbone pre-trained on ImageNet, standard 701/951 split, drone and satellite only</sub> | [Enhancing cross view geo localization through global local quadrant interaction network](https://doi.org/10.1038/s41598-025-18935-6) | Table 1 | R@1=94.58 | false | R@5 and R@10 not reported in main text for this paper. |
| Sample4Geo-DPHR<br><sub>Sample4Geo backbone with DPHR reweighting strategy, standard 701/951 split</sub> | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 1 | R@1=94.44 | false | DPHR applied to Sample4Geo baseline; R@5/R@10 not reported in paper. |
| SeGCN<br><sub>SwinV2-T backbone, shared-weight siamese, trained with instance loss + triplet loss on standard 701/951 split, 256x256 input</sub> | [SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization](https://doi.org/10.1109/jstars.2024.3370612) | Table I | R@1=94.29 | false | Flagship result from Table I on the standard University-1652 Satellite→Drone protocol. R@5 and R@10 not reported in the paper. |
| Heatmap-Guided Swin-Transformer + LightGCN<br><sub>Official 701/951 split; drone and satellite images only</sub> | [A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance and Graph Structure Optimization](https://doi.org/10.1109/crc67523.2025.11288246) | Abstract | R@1=93.76 | false | Abstract-reported headline result; R@5 and R@10 not reported in supplied text, so they are unavailable. |
| MFFN-AAE<br><sub>Swin-B backbone, standard 701/951 split, drone+satellite only, single-pass retrieval</sub> | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table II | R@1=93.44 | false | R@5 and R@10 are not reported for Satellite→Drone in the main table; flagged as not available. |
| CEUSP<br><sub>ConvNeXt-T backbone; trained on the official University-1652 701/951 split using only drone and satellite imagery; 256×256 inputs; single-pass retrieval.</sub> | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-View Geo-Localization | Table III | R@1=93.3 | false | R@5 and R@10 are not reported in the paper for this protocol and are therefore omitted. |
| MBF<br><sub>Standard 701/951 train/test split, drone and satellite only, Hybrid ViT backbone pretrained on ImageNet, 384x384 input, SGD optimizer, single-pass retrieval with cosine distance.</sub> | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 4 of the paper. R@5 and R@10 values are taken from Table 11 (Drone→Satellite column with query count=54, which is the standard single-gallery Satellite→Drone evaluation setup per University-1652 conventions). | R@1=93.15 | false | Table 4 directly gives R@1=93.15 and AP=88.17. R@5 and R@10 are from the multi-query table reflecting the standard Satellite→Drone protocol numbers reported alongside. |
| AFMS-Net<br><sub>ViT-S backbone pretrained on ImageNet; 120 epochs, SGD, batch size 8, standard 701/951 split</sub> | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 1 | R@1=92.87 | false | R@5 and R@10 are not reported in the paper; only R@1 and AP are available. |
| OriLoc<br><sub>Standard 701/951 train/test split; drone and satellite views only (no ground-view training); Swin-T backbone, 384-d embeddings</sub> | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI 'PERFORMANCE OF CURRENT METHOD ON UNIVERSITY-1652', referenced in text: 'OriLoc achieves competitive results (80.03% R@1 for drone-to-satellite and 92.73% R@1 for satellite-to-drone)'. | R@1=92.73 | false | R@5, R@10, and AP values for OriLoc on University-1652 are not extractable from the provided full-text/table evidence (Table VI content not included in the extracted text). Only R@1 is clearly stated in the prose. |
| IFS-Net<br><sub>ResNet-50 backbone, 256×256 input, cross-entropy loss, trained on official 701-building split</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table II | R@1=91.44 | false | R@5 and R@10 are not explicitly reported in Table II for Satellite→Drone; conservative placeholders would normally be set to null, but no exact values are available in the paper. Left as 'unclear' in spirit - using null. |
| SA-DOM<br><sub>Trained on University-1652 standard 701/951 split, ResNet-50 backbone, 256x256 input, SAS preprocessing, HAB attention, Deconstruction+Center+CE loss</sub> | [Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization](https://doi.org/10.1109/tgrs.2023.3337383) | Table I, University-1652 Satellite->Drone | R@1=91.44 | false | Paper's flagship result on the standard test split. |
| SDPL (ResNet-50)<br><sub>ResNet-50 backbone, 512x512, standard 701/951 split, single-pass retrieval</sub> | [SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization](https://doi.org/10.1109/tcsvt.2024.3424196) | Table IV | R@1=89.3 | false | Primary SDPL flagship result on University-1652 with ResNet-50 backbone. |
| University-1652 Baseline (Model-III, ResNet-50, Instance Loss)<br><sub>Satellite+Drone+Ground, shared weights, 256x256 input, instance loss</sub> | University-1652: A Multi-view Multi-source Benchmark for Drone-based Geo-localization | Table 8 (Model-III row) | R@1=71.18 | false | Flagship single-query single-pass retrieval. R@5 not reported in the paper's tables. |
| SFT<br><sub>Satellite-free training; multi-view UAV sequences reconstructed via 3DGS into pseudo-orthophotos, DINOv3 + Fisher vector aggregation learned from drone data only</sub> | [Satellite-Free Training for Drone-View Geo-Localization](http://arxiv.org/abs/2604.01581v2) | Table 1, p5 | R@1=51.07 | false | Gallery consists of multi-view UAV reconstructed pseudo-orthophotos rather than standard single oblique drone images. Standard 701/951 split is used. |

## UAV-to-Satellite (UAV query, satellite gallery)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| IMPROVING<br><sub>ResNet-101 backbone, 512-dim FC embedding, cross-entropy loss, 224x224 input, LR 0.001 (backbone) / 0.01 (new layers), dropout 0.5</sub> | [Improving the Localization Accuracy in Internet of Drones Networks](https://doi.org/10.1109/icicis66182.2025.11313133) | Abstract; Section IV-B; Fig. 4 | R@1=78.23 | false | Proposed framework; cross-entropy loss; cosine similarity at test time |

## UAV-to-satellite (cross-view image matching, testing phase: 701 UAV queries against 951 satellite gallery)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ResNet-101 backbone with global pooling, 512-D FC embedding, and cosine similarity for retrieval<br><sub>Standard training on 701 buildings (33 universities); cross-entropy loss; learning rates 0.001 (backbone) / 0.01 (new layers); dropout 0.5; input 224x224; PyTorch 2.5.1, CUDA 12.2</sub> | [Improving the Localization Accuracy in Internet of Drones Networks](https://doi.org/10.1109/icicis66182.2025.11313133) | Paper 'Improving the Localization Accuracy in Internet of Drones Networks' (ICICIS 2025), Abstract and Fig. 4 / Section IV-B | R@1=78.23 | false | Single reported configuration; no comparison across multiple backbones or protocols in the paper |

## drone-to-satellite

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ORIENTATION-FREE<br><sub>default</sub> | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI (text) | R@1=80.03 | false | Only R@1 reported in text; R@5, R@10, AP not extracted from paper body |

## drone-to-satellite (ablation: full SCOF)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt + full local branch (ASPP+SA) + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table XII | R@1=94.68 | false | R@1 exceeds 93% and AP reaches 94.68% in drone→satellite task. |

## drone-to-satellite (ablation: stage-4 global baseline)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt baseline without local branch / OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table XII | R@1= | false | Stage-4 global features baseline already surpasses prior SOTA (e.g., MCCG). |

## drone-to-satellite (drone-view target localization)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM, AdamW, batch size 64, 21 epochs</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table VIII, Table IV, Section IV-C | R@1=93.68 | false | R@5 explicitly stated in Section IV-F visualization discussion; 47.77M parameters, 94.36B FLOPs. |

## drone-to-satellite (loss ablation: supervised contrastive loss)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt + OFM + supervised contrastive loss (vs. InfoNCE/triplet/instance)</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table XIII | R@1= | false | 1% improvement in R@1 and AP over InfoNCE; outperforms under image flip perturbations as well. |

## drone-to-satellite and satellite-to-drone under multi-weather conditions

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt + OFM + supervised contrastive loss; weather-disturbed test images</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table XI | R@1= | false | SCOF consistently performs best under each weather condition on both tasks. |

## drone-view target localization

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION | [AGEN: Adaptive Error Control-Driven Cross-View Geo-Localization Under Extreme Weather Conditions](https://doi.org/10.3390/s25123749) | abstract | R@1=95.43 | false | - |

## ground-to-aerial retrieval (Multi-environment Ground-to-Aerial Matching Challenge leaderboard)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| MULTI-VIEW<br><sub>ConvNeXt-L backbone; pretrained on VIGOR_aux then trained on U-1652-plus with drone-view intermediary</sub> | [GeoMatch: Multi-View Contrastive Learning for Limited CVGL with Semantic Uncertainty](https://doi.org/10.1145/3728482.3757383) | Table 1 (official challenge leaderboard) | R@1=33.07 | false | Second place in the official challenge leaderboard. |

## ground-to-aerial retrieval (ablation on backbone and drone-view)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| MULTI-VIEW<br><sub>ConvNeXt-Large backbone; drone-view used as intermediate modality; trained on U-1652-plus + VIGOR_aux</sub> | [GeoMatch: Multi-View Contrastive Learning for Limited CVGL with Semantic Uncertainty](https://doi.org/10.1145/3728482.3757383) | Table 3 (ablation on backbone and drone-view input) | R@1=33.07 | false | Best configuration matching the reported final model M_final. |

## ground-to-aerial retrieval (ablation on training dataset configuration)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| MULTI-VIEW<br><sub>ConvNeXt backbone; trained on U-1652-plus plus VIGOR_aux selected via KL-divergence + cosine similarity</sub> | [GeoMatch: Multi-View Contrastive Learning for Limited CVGL with Semantic Uncertainty](https://doi.org/10.1145/3728482.3757383) | Table 2 (ablation on dataset configurations) | R@1=33.07 | false | Full proposed method with semantic-uncertainty-filtered auxiliary VIGOR data. |

## satellite-to-drone

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ORIENTATION-FREE<br><sub>default</sub> | [OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization](https://doi.org/10.1109/jstars.2025.3579740) | Table VI (text) | R@1=92.73 | false | Only R@1 reported in text |

## satellite-to-drone (drone navigation)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM, AdamW, batch size 64, 21 epochs</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table VIII | R@1=96.29 | false | Drone navigation task. |
