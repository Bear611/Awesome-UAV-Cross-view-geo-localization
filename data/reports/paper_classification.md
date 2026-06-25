# Paper Classification

Generated: 2026-06-22 01:25:23 Asia/Shanghai

This report classifies all 228 candidate papers into 4 groups based on whether they appear in the published GitHub leaderboard (the committed `leaderboards.csv` and `not_included.md`) and whether they have a fulltext cache record.

## TL;DR — Big Picture

| Group | Count | On GitHub? | Has fulltext? |
|---|---:|:---:|:---:|
| **A. In `leaderboards.csv`** (the official leaderboard) | **27** | ✓ | mostly yes |
| **B. In `not_included.md`** (reviewed, decision = exclude) | **58** | ✓ | varies |
| **C. Have cache, NOT on GitHub** (need review) | **103** | ✗ | yes (cache exists) |
| **D. In papers.yml, NO cache** (never probed) | **72** | ✗ | no |
| **Total candidates** | **228** | | |

**Already on GitHub**: 85 papers (Group A + B)
**Not yet on GitHub**: 175 papers (Group C + D)

The user's intuition '130-160 not yet read' roughly matches Group C (103) + Group D (72) = 175 papers that need attention.

---

## Group A — On the official leaderboard (27 papers)

These have at least one row in `data/leaderboards.csv` and are the 'public face' of the project. Their review was finalized and pushed to GitHub.

| Paper ID | Title | Quality |
|---|---|---|
| `18a3adb9c3c3` | A Deep Learning Framework with Geographic Information Adaptive Loss for Remote S | 真 PDF 全文 |
| `631f58d43805` | A Highly Robust Image Matching and Localization Method Based on Heatmap Guidance | 无 cache 记录 |
| `db7a7aafdad6` | Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust C | 真 PDF 全文 |
| `b51dab3341da` | BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation M | 无 cache 记录 |
| `5f27c86a30e9` | DINO-GFSA: Geo-Localization via Semantic Gated Fusion and Mamba-based Sequential | 真 PDF 全文 |
| `d04c0e428697` | DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Environments | 无 cache 记录 |
| `88b1c713820a` | DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Localization | 无 cache 记录 |
| `12a111049558` | Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localizatio | 真 PDF 全文 |
| `3d8550f1d24c` | Enhancing cross view geo localization through global local quadrant interaction  | 真 PDF 全文 |
| `e30ee7b6b636` | Improving the Localization Accuracy in Internet of Drones Networks | 无 cache 记录 |
| `ca78db4b5731` | JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-vie | 无 cache 记录 |
| `e72f3ee1cd16` | MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for  | 真 PDF 全文 |
| `7e27b2c01efa` | MFRGN: Multi-scale Feature Representation Generalization Network for Ground-to-A | HTML 太短 |
| `f5df981b2073` | Multi-Level Embedding and Alignment Network with Consistency and Invariance Lear | 真 PDF 全文 |
| `6f916702b8e5` | Multi-level representation learning via ConvNeXt-based network for unaligned cro | 无 cache 记录 |
| `d7e7b56c7172` | Multibranch Joint Representation Learning Based on Information Fusion Strategy f | 无 cache 记录 |
| `0cd8ae8fffca` | Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area | 真 PDF 全文 |
| `e3ae8d127381` | OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization | 无 cache 记录 |
| `86e493397deb` | Robust Drone-View Geo-Localization via Content-Viewpoint Disentanglement | 真 PDF 全文 |
| `69139de02b5a` | SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization | 真 PDF 全文 |
| `3ed9b45869b5` | Satellite-Free Training for Drone-View Geo-Localization | 真 PDF 全文 |
| `ed7cb3a291e1` | SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Localization | 无 cache 记录 |
| `ec71977b0f14` | Style Alignment-Based Dynamic Observation Method for UAV-View Geo-Localization | 真 PDF 全文 |
| `841f72f1d3b0` | UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervi | 真 PDF 全文 |
| `07189011a83b` | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception | 真 PDF 全文 |
| `295bb428fa52` | Vision-Based UAV Self-Positioning in Low-Altitude Urban Environments | 真 PDF 全文 |
| `e0ec8018f9b7` | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Dis | 真 PDF 全文 |

---

## Group B — Reviewed, on `not_included.md` (58 papers)

These were reviewed and the decision is 'do not include in the official leaderboard' (e.g. ablation, transfer-only, no metrics). They are listed in `leaderboards/not_included.md` on GitHub with reasons.

| Paper ID | Title | Quality |
|---|---|---|
| `c1aaaaa8337e` | A 2D Georeferenced Map Aided Visual-Inertial System for Precise UAV Localization | 真 PDF 全文 |
| `f6467fd49ebf` | A Self-Adaptive Feature Extraction Method for Aerial-View Geo-Localization | HTML 太短 |
| `5b4e2f9b1ab3` | A Spatial Consistency-Guided Sampling Algorithm for UAV Remote Sensing Heterogen | 真 PDF 全文 |
| `b75d8544f9c8` | AGEN: Adaptive Error Control-Driven Cross-View Geo-Localization Under Extreme We | 仅 OpenAlex 摘要 |
| `8ead117ff9eb` | AST: An Attention-Guided Segment Transformer for Drone-Based Cross-View Geo-Loca | 真 HTML 全文 |
| `5ab5e7a879a1` | AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation  | 真 PDF 全文 |
| `e0771ab75a1f` | Aerial-view geo-localization based on multi-layer local pattern cross-attention  | 真 HTML 全文 |
| `dac7dd98048d` | An AI-Based RGBD Framework for Cross-View Geo-Localization | 仅 OpenAlex 摘要 |
| `a5706073745b` | An Optimal Viewpoint-Guided Visual Indexing Method for UAV Autonomous Localizati | 真 PDF 全文 |
| `82930fdbcd52` | Attention-Driven Object Encoding and Multiscale Contextual Perception for Improv | 真 PDF 全文 |
| `1e2fd9322454` | Beyond Spatial Domain: Multi-View Geo-Localization with Frequency-Based Positive | 真 PDF 全文 |
| `aeb153b400f8` | BiCrossNet: resource-efficient cross-view geolocalization with binary neural net | 仅 OpenAlex 摘要 |
| `fd3d1f59b342` | CCR: A Counterfactual Causal Reasoning-Based Method for Cross-View Geo-Localizat | HTML 太短 |
| `18b0e7c247aa` | CLIP-UG: CLIP-Driven Vision-Language Model for UAV-View Geo-Localization | 真 PDF 全文 |
| `bd375063449b` | Cross-view UAV Geo-localization via Wavelet-based Local Feature Enhancement | 无 cache 记录 |
| `41f846965028` | DOA: Advancing Cross-View Geo-Localization via Domain and Objective Alignment | 真 PDF 全文 |
| `f87199e21f78` | ENSEMBLE IMAGE SUPER-RESOLUTION FOR UAV GEO-LOCALIZATION | 真 PDF 全文 |
| `77433b3d1d50` | Each Part Matters: Local Patterns Facilitate Cross-View Geo-Localization | 真 PDF 全文 |
| `7de7b7bb2240` | Efficient cross-view matching of images captured by UAV cameras | 真 PDF 全文 |
| `5e28d5dd52cf` | Enhancing Cross-View Geo-Localization Generalization via Global-Local Consistenc | 真 PDF 全文 |
| `94b049377ff5` | Enhancing Cross-View UAV Geolocalization via LVLM-Driven Relational Modeling | 真 PDF 全文 |
| `3061511b2df3` | Frequency-Enhanced Network for cross-view geolocalization | 真 PDF 全文 |
| `bdda3d75d3e3` | GNSS-denied geolocalization of UAVs using terrain-weighted constraint optimizati | HTML 太短 |
| `3bd445c4a1b7` | GeoLink: A 3D-Aware Framework Towards Better Generalization in Cross-View Geo-Lo | 真 PDF 全文 |
| `2ad1078935a8` | HCCM: Hierarchical Cross-Granularity Contrastive and Matching Learning for Natur | 真 PDF 全文 |
| `59e9d9e50cbc` | HE-VPR: Height Estimation Enabled Aerial Visual Place Recognition Against Scale  | 真 PDF 全文 |
| `440785eadbb8` | Hierarchical Image Matching for UAV Absolute Visual Localization via Semantic an | 真 PDF 全文 |
| `f11512cc1a97` | Learnable Query Aggregation with KV Routing for Cross-view Geo-localisation | 无 cache 记录 |
| `987a2921bafc` | Learning Better UAV-Based Cross-View Object Geo-Localization from Multi-Modal Pr | 真 PDF 全文 |
| `fe6b94f294fd` | Leveraging edge detection and neural networks for better UAV localization | 真 PDF 全文 |
| `c0c1545f82ef` | MCFA: Multi-Scale Cascade and Feature Adaptive Alignment Network for Cross-View  | 真 PDF 全文 |
| `fc7381acc7dd` | MFAF: An EVA02-Based Multi-scale Frequency Attention Fusion Method for Cross-Vie | 真 PDF 全文 |
| `bd2d89d0fc4e` | MM-Geo Multi-Scale and Multi-Positive UAV-View Geo-Localization | 仅 OpenAlex 摘要 |
| `5ad26fdff1b2` | Meridian: Metric-Semantic Primitive Matching for Cross-View Geo-Localization Bey | 真 PDF 全文 |
| `362f69fb5838` | Multiple-environment Self-adaptive Network for aerial-view geo-localization | 真 PDF 全文 |
| `f174fa72aafb` | NGC-GeoLoc: Neural GeoCoordinate Regression for GPS-Denied UAV Geo-Localization | 仅 OpenAlex 摘要 |
| `2baab5dbc766` | NavBEV: Empowering Self-Supervised UAV-Based Visual Navigation Through 3D BEV Re | 仅 OpenAlex 摘要 |
| `4db932860019` | One-to-Many Fine-Grained Matching Between UAV Images and Satellite Images for UA | 仅 OpenAlex 摘要 |
| `cf21e7c90485` | PHIM: heterologous remote sensing image matching method based on PC-Harris for U | 仅 OpenAlex 摘要 |
| `6dfb68d70043` | PLGeo: A Patch-level Framework to Overcome Orientation Discrepancies in Cross-vi | HTML 太短 |
| `3b8954612817` | Proxy-UAV: Bridging the Missing Drone View for Cross-View Geo-Localization | 真 PDF 全文 |
| `b208ec7913db` | Research on UAV geolocation methods based on deep learning | 仅 OpenAlex 摘要 |
| `f4eecdd88528` | Road Maps as Free Geometric Priors: Weather-Invariant Drone Geo-Localization wit | 真 PDF 全文 |
| `bd2c55fa8480` | Robust GNSS-denied localization for UAV using particle filter and visual odometr | HTML 太短 |
| `ddc52e8f3603` | Scale-Aware UAV-to-Satellite Cross-View Geo-Localization: A Semantic Geometric A | 真 PDF 全文 |
| `68640bc5fef4` | Season-Invariant GNSS-Denied Visual Localization for UAVs | 真 PDF 全文 |
| `82dbe06751f7` | Self-Supervised Cross-View Graph Search Framework for Ground-to-Satellite Geo-Lo | 真 PDF 全文 |
| `831e2bdf4b40` | SkyLink: Unifying Street-Satellite Geo-Localization via UAV-Mediated 3D Scene Al | 真 PDF 全文 |
| `2f5b6ccdd8ce` | Towards GNSS-Denied Geo-Positioning Using Search Area Refinement | 真 HTML 全文 |
| `111d1c1df219` | Towards Natural Language-Guided Drones: GeoText-1652 Benchmark with Spatial Rela | HTML 太短 |
| `100a2201256c` | Towards UAV Localization in GNSS-Denied Environments: The SatLoc Dataset and a H | 真 PDF 全文 |
| `c3321ed351c8` | UAV Visual Localization via Multimodal Fusion and Multi-Scale Attention Enhancem | 仅 OpenAlex 摘要 |
| `b8cd2823e728` | UAV-Satellite Cross-View Image Matching Based on Adaptive Threshold-Guided Ring  | 真 PDF 全文 |
| `8ad80ad4e6be` | UAV-VisLoc: A Large-scale UAV Dataset with Continuous Trajectories for Visual Ge | HTML 太短 |
| `1a5c98340843` | Understanding Global Structure Relation via Reversible Visual State Space Model  | 仅 OpenAlex 摘要 |
| `ab9dab27b058` | Unsupervised Multi-view UAV Image Geo-localization via Iterative Rendering | 无 cache 记录 |
| `171ae597721c` | Visual Orientation Posterior for Post-Retrieval UAV Geo-Localization | 仅 OpenAlex 摘要 |
| `4a524e209bfe` | Združevanje vizualnega prepoznavanja lokacij in metode SLAM s histogramskim filt | HTML 太短 |

---

## Group C — Have cache, NOT on GitHub (103 papers)

These have a fulltext cache record (from your downloads + my OpenAlex/arXiv/Unpaywall rescue) but have not been added to the leaderboard or `not_included.md` yet. They need a review pass to determine `include` / `partial` / `exclude`.

### Sub-group C.1: 真 PDF 全文 (48 papers)

| Paper ID | Title |
|---|---|
| `2040e36dc653` | ? |
| `2aea7cfc1827` | ? |
| `637455989bdd` | ? |
| `5ed8b876c844` | ? |
| `5cc3577dca98` | ? |
| `168d02a9b466` | ? |
| `b42052239952` | ? |
| `66232e8eb1c9` | ? |
| `230799676ea4` | ? |
| `22345c806236` | ? |
| `6a3fbed60c1e` | ? |
| `82e359246ac2` | ? |
| `6d1f5a988afb` | ? |
| `1e2d1a605d5d` | (MGS)$^2$-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for  |
| `707a1fe2d540` | A Comparative Study of Error-Correcting Codes for Multi-Cell Upsets in Memories: |
| `7ac44ed43a07` | A Novel EAGLe Framework for Robust UAV-View Geo-Localization |
| `b21b549fe000` | A UAV scene matching method based on triplet relationship and sliding mode contr |
| `d09a2df47fda` | Altitude-Adaptive Vision-Only Geo-Localization for UAVs in GPS-Denied Environmen |
| `c1c77403e0a3` | Attentive Multi-Kernel Feature Aggregation Network for Cross-View Geo-Localizati |
| `aa95c2daa1b2` | CGSI: Context-Guided and UAV’s Status Informed Multimodal Framework for Generali |
| `d38847a4bbbe` | CPFL: Resilient Continuous UAV Localization via Cross-View Perception and Partic |
| `1c2fac0f661d` | CVD-SfM: A Cross-View Deep Front-end Structure-from-Motion System for Sparse Loc |
| `774e09788340` | City-level aerial geo-localization based on map matching network |
| `2964565623c8` | Contrastive Ground-Level Image and Remote Sensing Pre-training Improves Represen |
| `27b14397c21c` | Exploring the best way for UAV visual localization under Low-altitude Multi-view |
| `5b733102f40e` | FALL: Fine-Grained Alignment and Local Information Aggregation Learning for Dron |
| `01a3b5e8b396` | Fine-Grained Cross-View Geo-Localization Using a Correlation-Aware Homography Es |
| `07f34415191b` | FoundLoc Vision-based Onboard Aerial Localization in the Wild |
| `b28d98811c7b` | Game4Loc A UAV Geo-Localization Benchmark from Game Data |
| `648e21111b87` | GeoMatch: Multi-View Contrastive Learning for Limited CVGL with Semantic Uncerta |
| `ea96da563d00` | HMCF-Net: Hierarchical Multi-scale Fusion for UAV-Satellite Cross-view Geo-local |
| `573972da87de` | Modern Backbone for Efficient Geo-localization |
| `d3cdc2d6ff0a` | Navigating the Metaverse: UAV-Based Cross-View Geo-Localization in Virtual World |
| `c8be0750a5a1` | One-to-Many Retrieval Between UAV Images and Satellite Images for UAV Self-Local |
| `8c187c7f35f0` | P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co |
| `4125cdc9d2ec` | Progressive High-Confidence Pseudo-Labeling for Unsupervised Cross-View Image Ge |
| `daf790654cfb` | Rethinking Pooling for Multi-Granularity Features in Aerial-View Geo-Localizatio |
| `d677dd26cb3e` | SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalizat |
| `d5de60b2f94e` | SemGeoFrame: A Visual Matching Framework for Aircraft Based on Surface Semantic  |
| `11c3f6572110` | Simple, Effective and General A New Backbone for Cross-view Image Geo-localizati |
| `2f34c094b799` | SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-Vie |
| `b5ab5786cd9c` | UAV Cross-View Geo-Localization Based on Multi-Scale Partitioning and Attention- |
| `189d681f636e` | UAV-GeoLoc A Large-Vocabulary Dataset and Geometry-Transformed Method for UAV Ge |
| `1d9504fbc049` | UAV-VisLoc A Large-scale Dataset for UAV Visual Localization |
| `e134010b5d6e` | University-1652 A Multi-view Multi-source Benchmark for Drone-based Geo-localiza |
| `a7fcf3489f1b` | VLF-SPS: a visual localization framework based on salient position selection and |
| `e8b9b13f251d` | Visual Localization system for GPS-Blind Environments in Unmanned Aerial Vehicle |
| `b8bbbd941cc5` | Visual Self-Positioning of Low-Altitude Urban UAV Based on Improved Transformer  |

### Sub-group C.2: 真 HTML 全文 (4 papers)

| Paper ID | Title |
|---|---|
| `459fe2fdc478` | Rotation and seasonal invariant UAV-satellite image matching via polar coordinat |
| `4c64f499c803` | Structural Perception Enhancement for Cross-View Geo-Localization |
| `09b55cdd62e2` | Toward Drone-View Building Localization in the Wild: A Benchmark |
| `c055725bd7ca` | UAV’s Status Is Worth Considering: A Fusion Representations Matching Method for  |

### Sub-group C.3: HTML 太短 (12 papers)

| Paper ID | Title |
|---|---|
| `068c6b4353b8` | ? |
| `a6652a1876d6` | ? |
| `fcdd313bd34f` | ? |
| `87142a4c97b6` | ? |
| `54ac76030e88` | ? |
| `bbb42bc68cd8` | ? |
| `5692c9145e2b` | CAMP A Cross-View Geo-Localization Method Using Contrastive Attributes Mining an |
| `a88eadab59a7` | CDM-Net A Framework for Cross-View Geo-Localization With Multimodal Data |
| `ffa7a7877031` | Enhancing Cross-View Geo-Localization With Domain Alignment and Scene Consistenc |
| `36136642f061` | MCCG A ConvNeXt-Based Multiple-Classifier Method for Cross-View Geo-Localization |
| `87370b99b651` | Query-Driven Feature Learning for Cross-View Geo-Localization |
| `83972fc6c838` | SUES-200 A Multi-height Multi-scene Cross-view Image Benchmark Across Drone and  |

### Sub-group C.4: 仅 OpenAlex 摘要 (38 papers)

| Paper ID | Title |
|---|---|
| `f2ec31f26fba` | &amp;Segloc: Dual-Decoder-Based Semantic-Enhanced Remote Sensing Localization Me |
| `fe0cb98827ae` | 3D Positioning of Drones through Images |
| `7bcacdaff17e` | A Cross-View Geo-Localization Algorithm Using UAV Image and Satellite Image |
| `0dffafd487e0` | A Hierarchical Absolute Visual Localization System for Low-Altitude Drones in GN |
| `6c9b3d941fa4` | A Novel Template Matching Method Incorporating a Multi‐Candidate Region Optimiza |
| `54e4a5a123a2` | A Review on Deep Learning for UAV Absolute Visual Localization |
| `2ea8b3ff6fab` | Accurate Vision-Enabled UAV Location Using Feature-Enhanced Transformer-Driven I |
| `27f25fe3a849` | AirLock <sup>+</sup> : Scaling UAV-to-Satellite Image Registration for Target Ge |
| `6cdb7194b925` | An Efficient Pyramid Transformer Network for Cross-View Geo-Localization in Comp |
| `2e894c4fd94c` | Contrastive Learning Based Visual Place Recognition Pre-Training Framework for U |
| `80cc13347437` | Cross-View Image Retrieval Guided by Spatially Aware Attention for Robust Geo-Lo |
| `cba3f199a0d3` | DOCB: A Dynamic Online Cross-Batch Hard Exemplar Recall for Cross-View Geo-Local |
| `08ba2c64262c` | Direction-Guided Multiscale Feature Fusion Network for Geo-Localization |
| `e07dffc3e9f4` | Enhancing Semantic Information Representation in Multi‐View Geo‐Localization thr |
| `565450d576ea` | FANet: Fovea Attention Network for Robust Aerial Geo-Localization Across Diverse |
| `3e61d038d390` | GRiM-Net: A Two-Stage Cross-View Visual Localization Framework for UAVs |
| `14483b52c250` | GeoRVLF: A Robust Drone-Satellite Visual Geo-Localization Framework for Small Un |
| `6f2a302b59e6` | Geolocalization of Unmanned Aerial Vehicle Images and Mapping onto Satellite Ima |
| `039cb769dc1b` | Learning Robust Feature Representation for Cross-View Image Geo-Localization |
| `f63504919148` | Leveraging Multi-View Images to Learn Domain-Invariant Discriminative Embeddings |
| `2327946336e4` | MGAW: An Effective Method for Geo-localization in Adverse Weather |
| `4cc17aecc3c0` | MMHCA: Multi-feature representations based on multi-scale hierarchical contextua |
| `50abb7ac99ee` | MTA-Dataset: Multiple-Tilt-Angle Dataset for UAV–Satellite Image Matching |
| `42bbd39ca43d` | MuRDE-FPN: Precise UAV Localization Using Enhanced Feature Pyramid Network |
| `36294fc859ec` | NaviLoc: Trajectory-Level Visual Localization for GNSS-Denied UAV Navigation |
| `58df9b4d22e8` | OBTPN: A Vision-Based Network for UAV Geo-Localization in Multi-Altitude Environ |
| `0fde36fb877f` | Robust UAV Localization in GNSS-Denied Environments via Efficient Visual Scene M |
| `ccd22757308c` | SAVL Scene-Adaptive UAV Visual Localization Using Sparse Feature Extraction and  |
| `2b493532d767` | SHAA Spatial Hybrid Attention Network With Adaptive Cross-Entropy Loss Function  |
| `caf3e6394cf6` | SIGN: Saliency-Aware Integrated Global-Local Network for Cross-View Geo-Localiza |
| `03a071c292ff` | SURFNet A Surface-Aware UAVSatellite Geolocation Framework via Feature Aggregati |
| `120e933e12d6` | Semantic Concept Perception Network With Interactive Prompting for Cross-View Im |
| `a9e46f1941ab` | Swin transformer for feature extraction: a cross-view geo-localization method fo |
| `2b03e42096de` | Tightly Coupled Multifactor Optimization-Based Hybrid Visual Localization for UA |
| `828f0287f3a3` | TirSA: A Three Stage Approach for UAV-Satellite Cross-View Geo-Localization Base |
| `f492b9c680a8` | UAV Geo-Localization Dataset and Method Based on Cross-View Matching |
| `1fa9c5986534` | VAGeo: View-specific Attention for Cross-View Object Geo-Localization |
| `2ca080213d22` | Visual State Space Model Enhanced Features for UAV Geo-localization |

### Sub-group C.5: NBS（未拿到） (1 papers)

| Paper ID | Title |
|---|---|
| `ab6f62cc19e4` | Focal Hanning Loss: Revisiting the Heatmap Classification for UAV Self-localizat |

---

## Group D — Never probed, no cache (72 papers)

These are in `papers.yml` but have NO cache record at all. They've never been run through the fulltext discovery pipeline. They likely need to be probed next (OpenAlex API, arXiv search, Unpaywall) to add them to the leaderboard pipeline.

| Paper ID | Title | DOI | arXiv |
|---|---|---|---|
| `631f58d43805` | A Highly Robust Image Matching and Localization Method Based on Heatma | [10.1109/crc67523.2025.112…](https://doi.org/10.1109/crc67523.2025.11288246) | — |
| `de5c1acf58ab` | A Transformer-Based Feature Segmentation and Region Alignment Method f | — | — |
| `e55a3076ffe2` | ACCL: A Plug-and-play Adaptive Confusion-aware Contrastive Loss for UA | [10.1109/icme59968.2025.11…](https://doi.org/10.1109/icme59968.2025.11209371) | — |
| `5f4142a58af4` | APA-BI Adaptive Partition Aggregation and Bidirectional Integration fo | [10.1109/icra55743.2025.11…](https://doi.org/10.1109/icra55743.2025.11128402) | — |
| `9880ae23b323` | Adaptive Multi-Backbone Fusion for UAV-Centric Cross-View Geo-Localiza | [10.1145/3728482.3757381](https://doi.org/10.1145/3728482.3757381) | — |
| `757be77ae202` | AerialVL: A Dataset, Baseline and Algorithm Framework for Aerial-Based | [10.1109/lra.2024.3441491](https://doi.org/10.1109/lra.2024.3441491) | — |
| `b51dab3341da` | BGG: Bridging the Geometric Gap between Cross-View images by Vision Fo | — | [2605.10345v1](https://arxiv.org/abs/2605.10345v1) |
| `9ba16a43537d` | Beyond Matching to Tiles Bridging Unaligned Aerial and Satellite Views | — | — |
| `44ce5ac96986` | Bridging the appearance gap Multi-experience localization for long-ter | — | — |
| `ca16920bb2da` | CFIRE: Cross-View Feature Interaction for Fine-Grained Regression-Base | [10.1109/icassp55912.2026.…](https://doi.org/10.1109/icassp55912.2026.11464992) | — |
| `d490bde886ee` | Comparative Studies of Descriptor-Based Image Matching Techniques for  | [10.1109/access.2025.35669…](https://doi.org/10.1109/access.2025.3566953) | — |
| `b38399c5c0d2` | Comparison of Visual Place Recognition Methods for UAV Imagery | [10.1109/dsp65409.2025.110…](https://doi.org/10.1109/dsp65409.2025.11075213) | — |
| `f21c9cfe29c0` | Cross-Attention Between Satellite and Ground Views for Enhanced Fine-G | — | — |
| `8c7585ccb202` | Cross-View Image Geo-Localization with Panorama-BEV Co-retrieval Netwo | [10.1007/978-3-031-72913-3…](https://doi.org/10.1007/978-3-031-72913-3_5) | — |
| `468b748ff556` | Cross-View Object Geo-Localization in a Local Region With Satellite Im | [10.1109/tgrs.2023.3307508](https://doi.org/10.1109/tgrs.2023.3307508) | — |
| `933a07cca9fd` | Cross-View UAV Geo-Localization with Precision-Focused Efficient Desig | — | — |
| `72d3a84cd035` | Cross-domain adaptive Siamese framework with benchmark for UAV self-po | [10.1016/j.cja.2026.104182](https://doi.org/10.1016/j.cja.2026.104182) | — |
| `bd375063449b` | Cross-view UAV Geo-localization via Wavelet-based Local Feature Enhanc | [10.1109/cnml68938.2026.11…](https://doi.org/10.1109/cnml68938.2026.11452264) | — |
| `8ac25db258bb` | DINO-MSRA: A Novel Network Architecture for UAV-Satellite Cross-View I | — | — |
| `d04c0e428697` | DINOv2-Based UAV Visual Self-Localization in Low-Altitude Urban Enviro | [10.1109/lra.2025.3527762](https://doi.org/10.1109/lra.2025.3527762) | — |
| `88b1c713820a` | DiffusionUavLoc: Visually Prompted Diffusion for Cross-View UAV Locali | — | [2511.06422v1](https://arxiv.org/abs/2511.06422v1) |
| `a49bd8bbea92` | Do Keypoints Contain Crucial Information Mining Keypoint Information t | — | — |
| `9f22c3d5e493` | Drone battlefield localization via multi-task learning and domain adap | [10.1016/j.dt.2026.04.002](https://doi.org/10.1016/j.dt.2026.04.002) | — |
| `a04107479203` | Exploring Deep Learning-Based Visual Localization Techniques for UAVs  | [10.1109/ACCESS.2024.34400…](https://doi.org/10.1109/ACCESS.2024.3440064) | — |
| `cd047607b9a7` | Exploring the Image Registration Method for UAV Visual Localization | [10.1109/csrswtc67757.2025…](https://doi.org/10.1109/csrswtc67757.2025.11384018) | — |
| `60de40de4030` | From GPS to AI: A comprehensive review of Unmanned Aerial Vehicle (UAV | [10.1016/j.isprsjprs.2025.…](https://doi.org/10.1016/j.isprsjprs.2025.09.014) | — |
| `a5449d507d08` | GNSS-denied geolocalization of UAVs by visual matching of onboard came | — | [2103.14381v2](https://arxiv.org/abs/2103.14381v2) |
| `ddca752302da` | GeoFormer: Boosting Object Distinguishing and Prompt Understanding for | [10.1109/tgrs.2025.3638946](https://doi.org/10.1109/tgrs.2025.3638946) | — |
| `e30ee7b6b636` | Improving the Localization Accuracy in Internet of Drones Networks | [10.1109/icicis66182.2025.…](https://doi.org/10.1109/icicis66182.2025.11313133) | — |
| `ca78db4b5731` | JRN-Geo: A Joint Perception Network based on RGB and Normal images for | [10.1109/icra55743.2025.11…](https://doi.org/10.1109/icra55743.2025.11127591) | [2509.05696v1](https://arxiv.org/abs/2509.05696v1) |
| `f4ed1572461e` | Joint Representation Learning Based on Feature Center Region Diffusion | [10.1109/tgrs.2024.3515484](https://doi.org/10.1109/tgrs.2024.3515484) | — |
| `f11512cc1a97` | Learnable Query Aggregation with KV Routing for Cross-view Geo-localis | [10.48550/arXiv.2512.23938](https://doi.org/10.48550/arXiv.2512.23938) | [2512.23938v1](https://arxiv.org/abs/2512.23938v1) |
| `cd3dc92a8286` | Leveraging Map Retrieval and Alignment for Robust UAV Visual Geo-Local | — | — |
| `39ff99cf43f4` | Lightweight Cross-View Localization via Quantized Knowledge Distillati | [10.1109/lsp.2026.3670737](https://doi.org/10.1109/lsp.2026.3670737) | — |
| `c84291931b02` | Long-range UAV Thermal Geo-localization with Satellite Imagery | — | — |
| `3b653d54791c` | MCL-Geo: Multi-branch Contrastive Learning for Cross-view Geo-localiza | [10.1145/3652628.3652743](https://doi.org/10.1145/3652628.3652743) | — |
| `f688dd8cddb0` | MMGeo Multimodal Compositional Geo-Localization for UAVs | [10.1109/iccv51701.2025.02…](https://doi.org/10.1109/iccv51701.2025.02334) | — |
| `c7e57d895be7` | MORE'25 Multimedia Object Re-ID: Advancements, Challenges, and Opportu | [10.1145/3701716.3717657](https://doi.org/10.1145/3701716.3717657) | — |
| `c5cb9de649a1` | Matching 2D Images in 3D Metric Relative Pose from Metric | — | — |
| `c9358f702d10` | MixFP:A Transformer-Based Method for UAV Cross-View Geolocation | [10.1007/978-3-032-16823-8…](https://doi.org/10.1007/978-3-032-16823-8_11) | — |
| `cd3a222e27f8` | MobileGeo Exploring Hierarchical Knowledge Distillation for Resource-E | — | — |
| `6f916702b8e5` | Multi-level representation learning via ConvNeXt-based network for una | [10.1080/10095020.2024.243…](https://doi.org/10.1080/10095020.2024.2439385) | — |
| `d92f0e26bb84` | Multi-weather Cross-view Geo-localization Using Denoising Diffusion Mo | [10.1145/3689095.3689103](https://doi.org/10.1145/3689095.3689103) | [2408.02408](https://arxiv.org/abs/2408.02408) |
| `372e8ffef5dd` | MultiLoc Multi-view Guided Relative Pose Regression for Fast and Robus | — | — |
| `d7e7b56c7172` | Multibranch Joint Representation Learning Based on Information Fusion  | [10.1109/TGRS.2024.3378453](https://doi.org/10.1109/TGRS.2024.3378453) | — |
| `e762d8c49f13` | Notes on Kalman Filter | — | — |
| `67f7a7aa8d61` | Object-level Cross-view Geo-localization with Location Enhancement and | [10.1109/jstars.2025.36035…](https://doi.org/10.1109/jstars.2025.3603506) | — |
| `e3ae8d127381` | OriLoc: Unlimited-FoV and Orientation-Free Cross-View Geolocalization | [10.1109/jstars.2025.35797…](https://doi.org/10.1109/jstars.2025.3579740) | — |
| `9c8f4e023278` | Particle Filter-Based Localization Using Visual Feature Synchronizatio | [10.1109/ICNS65417.2025.10…](https://doi.org/10.1109/ICNS65417.2025.10976891) | — |
| `ca98b2efc271` | PnP-UGCSuperGlue: deep learning drone image matching algorithm for vis | [10.1007/s11227-024-06128-…](https://doi.org/10.1007/s11227-024-06128-3) | — |
| `c4c5ea82da24` | Precise GPS-Denied UAV Self-positioning via Context-Enhanced Cross-Vie | [10.1007/978-981-95-5628-1…](https://doi.org/10.1007/978-981-95-5628-1_26) | [2502.11408v1](https://arxiv.org/abs/2502.11408v1) |
| `5f3026c15e82` | R2PLoc A Region-to-Point UAV Visual Geo-Localization Framework Leverag | [10.1109/tgrs.2025.3611657](https://doi.org/10.1109/tgrs.2025.3611657) | — |
| `9a41c34577e0` | Rethinking Cross-view Object Geo-Localization Towards Many-to-Many Rea | — | — |
| `c58d8d343927` | SMDT Cross-View Geo-Localization with Image Alignment and Transformer | — | — |
| `54ed1af6a9b3` | ST-D3QN Advancing UAV Path Planning With an Enhanced Deep Reinforcemen | — | — |
| `b5caac31809c` | STHN Deep Homography Estimation for UAV Thermal Geo-localization with  | — | — |
| `ed7cb3a291e1` | SeGCN: A Semantic-Aware Graph Convolutional Network for UAV Geo-Locali | [10.1109/jstars.2024.33706…](https://doi.org/10.1109/jstars.2024.3370612) | — |
| `cdfcc0ec1b73` | SliceMatch Geometry-Guided Aggregation for Cross-View Pose Estimation | — | — |
| `d13004a0f023` | Tightly Coupled GNSS-Visual-Inertial Smoothly Consistent State Estimat | — | — |
| `f6975dbe0dea` | Toward Integrating Semantic-aware Path Planning and Reliable Localizat | — | — |
| `950172f7f8c8` | UASTHN Uncertainty-Aware Deep Homography Estimation for UAV Satellite- | — | — |
| `63d35fe5fe2d` | UAV Positioning Method Based on Heterogeneous Image Matching Under GPS | [10.1007/978-981-96-2268-9…](https://doi.org/10.1007/978-981-96-2268-9_10) | — |
| `835f3f1ac3bf` | UAV Visual Localization System Empowered by Zero-Shot Deep Feature Mat | [10.1109/rusautocon65989.2…](https://doi.org/10.1109/rusautocon65989.2025.11177299) | — |
| `996bc136e153` | UAV coarse visual localization in large-scale continuous scenes | [10.1016/j.isprsjprs.2026.…](https://doi.org/10.1016/j.isprsjprs.2026.04.054) | — |
| `b508c0afaa2f` | UltraVPR: Unsupervised Lightweight Rotation- Invariant Aerial Visual P | [10.1109/lra.2025.3592075](https://doi.org/10.1109/lra.2025.3592075) | — |
| `ab9dab27b058` | Unsupervised Multi-view UAV Image Geo-localization via Iterative Rende | [10.1109/tgrs.2025.3572710](https://doi.org/10.1109/tgrs.2025.3572710) | [2411.14816v1](https://arxiv.org/abs/2411.14816v1) |
| `e93df3813f7c` | VLGeo: Bridging Viewpoints in UAV-View Geo-Localization Using a Large  | [10.1109/tgrs.2026.3680280](https://doi.org/10.1109/tgrs.2026.3680280) | — |
| `f265bcce8a8b` | View Consistent Purification for Accurate Cross-View Localization | — | — |
| `6cf6dbcaed80` | Visible-to-Infrared Image Translation for Matching Tasks | — | — |
| `d2714d8c0bdf` | Vision-Based UAV Localization by Aerial and Satellite Image Matching | [10.1109/ACCESS.2026.36846…](https://doi.org/10.1109/ACCESS.2026.3684630) | — |
| `ce14891059e1` | Visual Localization with Google Earth Images for Robust Global Pose Es | — | — |
| `ab2b9558e629` | Visual place recognition for aerial imagery: A survey | [10.1016/j.robot.2024.1048…](https://doi.org/10.1016/j.robot.2024.104837) | — |

---

## Recommended Next Steps

1. **Group A & B (85 papers)**: ALREADY on GitHub. Do not touch.
2. **Group C sub-group 真 PDF 全文 (48 papers)**: Re-review with the new full text. Several may flip from `exclude` to `include`, similar to the earlier `86e493397deb` (CVD) and `69139de02b5a` (SDPL) recoveries.
3. **Group C sub-group 真 HTML 全文 (4 papers)**: Same — re-review.
4. **Group C sub-group HTML 太短 / 仅摘要 (50 papers)**: Re-review. Most will stay excluded; some may flip to `partial` if the abstract names a dataset clearly.
5. **Group D (72 papers)**: Run fulltext discovery on these. Use the same 6-route strategy that rescued 8 from the abstract pool. Estimated runtime: ~2-3 minutes for the 6 routes × 72 papers.
6. After 1-5, run `rebuild_leaderboards.py build` then `validate`. Expect `included_rows` to grow beyond 78 and `excluded_rows` to grow beyond 247.
