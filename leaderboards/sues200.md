# SUES-200

Leaderboard for SUES-200. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## D2S 150m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 | R@1=93.37 | false | SkyLink re-ranking with Qwen2-VL-7B-Instruct backbone |

## D2S 200m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 | R@1=95.67 | false | SkyLink re-ranking with Qwen2-VL-7B-Instruct backbone |

## D2S 250m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 | R@1=96.50 | false | SkyLink re-ranking with Qwen2-VL-7B-Instruct backbone |

## D2S 300m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| VISION-LANGUAGE<br><sub>re-ranking</sub> | [SkyLink: A Large Vision-Language Model Driven Re-ranking Framework for Cross-View UAV geolocalization](http://arxiv.org/abs/2603.08063v3) | Table 1 | R@1=97.52 | false | SkyLink re-ranking with Qwen2-VL-7B-Instruct backbone |

## Drone (150m)→Satellite (mean across 10 environmental styles)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) | R@1=78.64 | false | Mean over 10 environmental styles; hardest height (150m) group |

## Drone→Satellite (150m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=83.05 | false | - |

## Drone→Satellite (200m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=89.65 | false | - |

## Drone→Satellite (250m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=94.05 | false | - |

## Drone→Satellite (300m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=95.75 | false | - |

## Drone→Satellite (height 150m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=85.30 | false | Drone target localization at 150m flight height |

## Drone→Satellite (height 200m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=93.23 | false | Drone target localization at 200m flight height |

## Drone→Satellite (height 250m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=96.48 | false | Drone target localization at 250m flight height |

## Drone→Satellite (height 300m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=97.50 | false | Drone target localization at 300m flight height |

## Drone→Satellite @ 150m (D2S)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Base + adapter, U1652-pretrained then fine-tuned</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 | R@1=78.53 | false | +23.63% over U1652-pretrained ViT-Base baseline (54.90%) |

## Drone→Satellite @ 300m (D2S)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Large + adapter</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 | R@1=93.28 | false | Performance increases with altitude |

## Drone→Satellite @ height 150m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=77.57 | false | Compared with LPN: R@1 +15.99%, AP +14.07% on Drone→Satellite task |

## Drone→Satellite @ height 200m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=89.50 | false | Compared with LPN: R@1 +18.92%, AP +15.44% on Drone→Satellite task |

## Drone→Satellite @ height 250m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=92.58 | false | Compared with LPN: R@1 +12.20%, AP +10.41% on Drone→Satellite task |

## Drone→Satellite @ height 300m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=97.40 | false | Compared with LPN: R@1 +15.93%, AP +13.39% on Drone→Satellite task |

## Satellite→Drone (150m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=95.0 | false | - |

## Satellite→Drone (150m, mean across 10 environmental styles)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| ENVIRONMENT-INDEPENDENT<br><sub>supervised, ConvNeXt-B backbone, multi-environment style augmentation</sub> | [P2FCN: Environment-Independent UAV-View Geo-Localization via Pixel-to-Feature Co-Enhancement](https://doi.org/10.1109/tgrs.2025.3643917) | Table IV summary (text) | R@1=91.50 | false | Mean over 10 environmental styles; hardest height (150m) group |

## Satellite→Drone (200m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=96.25 | false | - |

## Satellite→Drone (250m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=97.5 | false | - |

## Satellite→Drone (300m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CONVNEXT-BASED | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | R@1=98.8 | false | - |

## Satellite→Drone (height 150m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=93.75 | false | Drone navigation task at 150m flight height |

## Satellite→Drone (height 200m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=97.75 | false | Drone navigation task at 200m flight height |

## Satellite→Drone (height 250m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=98.75 | false | Drone navigation task at 250m flight height |

## Satellite→Drone (height 300m)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ConvNeXt-base backbone, 384x384, 130 epochs, cross-entropy + adaptive triple InfoNCE loss</sub> | [Joint Representation Learning Based on Feature Center Region Diffusion and Edge Radiation for Cross-View Geo-Localization](https://doi.org/10.1109/tgrs.2024.3515484) | Table III | R@1=98.75 | false | Drone navigation task at 300m flight height |

## Satellite→Drone @ 150m (S2D)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Large + adapter</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 | R@1=92.50 | false | +8.75% over FSRA at 150m |

## Satellite→Drone @ 300m (S2D)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| PARAMETER-EFFICIENT<br><sub>frozen DINOv2-Large + adapter</sub> | [AdaptGeo: Parameter-Efficient Cross-View Geo-Localization via Frozen Foundation Model and Transformer Adapter](https://doi.org/10.1109/TGRS.2025.3635418) | Table IV / Section IV-C2 | R@1=97.50 | false | Exceeds SDPL (96.25%) at 300m |

## Satellite→Drone @ height 150m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=93.75 | false | Compared with LPN: R@1 +10.00%, AP +12.71% on Satellite→Drone task |

## Satellite→Drone @ height 200m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=97.50 | false | Compared with LPN: R@1 +8.75%, AP +15.51% on Satellite→Drone task |

## Satellite→Drone @ height 250m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=97.50 | false | Compared with LPN: R@1 +5.00%, AP +14.69% on Satellite→Drone task |

## Satellite→Drone @ height 300m

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GEO-LOCALIZATION<br><sub>ResNet50 backbone, 256x256 input, 120 epochs, SGD optimizer, ImageNet pretrained</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III, Section IV-D-2 | R@1=100.00 | false | Compared with LPN: R@1 +7.50%, AP +11.94% on Satellite→Drone task |

## Standard Supervised Cross-View Retrieval

Rows: **16**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| (MGS)2-Net<br><sub>Trained on SUES-200 official training set across four altitudes (150m, 200m, 250m, 300m)</sub> | (MGS)2-Net: Unifying Micro-Geometric Scale and Macro-Geometric Structure for Cross-View Geo-Localization | Table 2 | Mean Drone→Satellite R@1=99.46 | false | Values computed as mean across four altitudes (150m, 200m, 250m, 300m). Drone→Sat: R@1 = (98.45+99.62+99.78+100.00)/4, AP = (98.78+99.69+99.80+100.00)/4. Satellite→Drone: R@1 = (98.75+100.00+100.00+100.00)/4, AP = (96.50+98.51+98.73+98.95)/4. Test image size 336x336. |
| BGG<br><sub>Supervised, DINOv3 ViT-B/16 backbone (frozen) with MFEA + FASA adapters trained on SUES-200 per-altitude training splits. Input 384x384, InfoNCE loss. Per-altitude test results (150m/200m/250m/300m) averaged.</sub> | [BGG: Bridging the Geometric Gap between Cross-View images by Vision Foundation Model Adaptation for Geo-Localization](http://arxiv.org/abs/2605.10345v1) | Tables II and III | Mean Drone→Satellite R@1=99.3825 | false | Mean values computed as average across the four altitudes (150m, 200m, 250m, 300m) of the paper's per-altitude R@1/AP entries for BGG. Drone→Satellite per-altitude: R@1/AP = 99.30/99.46 (150m), 99.45/99.55 (200m), 99.53/99.63 (250m), 99.25/99.38 (300m). Satellite→Drone per-altitude: R@1/AP = 98.75/98.22 (150m), 98.75/98.24 (200m), 98.75/98.73 (250m), 98.75/98.68 (300m). |
| SkyPart<br><sub>Trained on SUES-200 official train split (all four altitudes), single-pass, no re-ranking, no TTA, 448x448 single-scale crop, full 200-satellite confusion gallery</sub> | [Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery](http://arxiv.org/abs/2605.11654v2) | Table 1 (mean columns) and main text SOTA summary | Mean Drone→Satellite R@1=98.74 | false | Mean across four altitudes (150/200/250/300m). Per-altitude D→S R@1: 97.25/98.75/99.30/99.64; AP: 97.90/99.33/99.60/99.64. Per-altitude S→D R@1: 100.00/97.95/99.95/100.00; AP: 97.36/100.00/99.95/99.81. |
| JRN-Geo (k=4)<br><sub>Official SUES-200 splits per altitude, ConvNeXt-Base backbone, RGB+Normal inputs with 3D geographic augmentation factor k=4; metrics averaged across 150m, 200m, 250m, 300m</sub> | [JRN-Geo: A Joint Perception Network based on RGB and Normal images for Cross-view Geo-localization](http://arxiv.org/abs/2509.05696v1) | Table II | Mean Drone→Satellite R@1=98.36 | false | Computed mean across four altitudes from Table II: D→S R@1 = (96.47+98.60+99.28+99.10)/4 = 98.36; D→S AP = (97.26+98.92+99.45+99.33)/4 = 98.74; S→D R@1 = (98.75+98.75+98.75+98.75)/4 = 98.75; S→D AP = (96.05+98.02+99.06+98.97)/4 = 98.03 |
| MEAN<br><sub>Supervised on official SUES-200 training splits (per altitude), ConvNeXt-Tiny backbone</sub> | [Multi-Level Embedding and Alignment Network with Consistency and Invariance Learning for Cross-View Geo-Localization](https://www.semanticscholar.org/search?q=Multi-Level%20Embedding%20and%20Alignment%20Network%20with%20Consistency%20and%20Invariance%20Learning%20for%20Cross-View%20Geo-Localization) | Tables III and IV (SUES-200 comparisons, Drone→Satellite and Satellite→Drone across 150m/200m/250m/300m) | Mean Drone→Satellite R@1=98.0875 | false | Values computed as the mean across the four altitudes (150m, 200m, 250m, 300m) from Tables III and IV. Drone→Satellite: R@1 = mean(95.50, 98.38, 98.95, 99.52) = 98.0875; AP = mean(96.46, 98.72, 99.17, 99.63) = 98.495. Satellite→Drone: R@1 = mean(97.50, 100.00, 100.00, 100.00) = 99.375; AP = mean(94.75, 97.09, 98.28, 99.21) = 97.3325. |
| Sample4Geo-DPHR<br><sub>Sample4Geo backbone with DPHR reweighting strategy, per-altitude training and testing</sub> | [Dual-level Progressive Hardness-Aware Reweighting for Cross-View Geo-Localization](http://arxiv.org/abs/2510.27181v3) | Table 2 | Mean Drone→Satellite R@1=97.18 | false | Values computed as mean across 150m, 200m, 250m, 300m. Drone→Satellite R@1: (94.55+95.43+98.95+99.80)/4=97.18. Drone→Satellite AP: (95.60+96.36+99.14+99.85)/4=97.74. Satellite→Drone R@1: (95.00+97.50+98.75+99.88)/4=97.78. Satellite→Drone AP: (90.73+94.41+97.70+99.90)/4=95.69. |
| CVD (plug-and-play on Sample4Geo backbone)<br><sub>Official SUES-200 120/80 train/test split, trained and evaluated per altitude, mean across 150m/200m/250m/300m</sub> | [Robust Drone-View Geo-Localization via Content-Viewpoint Disentanglement](http://arxiv.org/abs/2505.11822v2) | Table 2, Sample4Geo† row; per-altitude values: D→S AP {97.12, 98.05, 98.63, 98.99}, D→S R@1 {94.97, 97.19, 98.00, 98.34}; S→D AP {96.24, 96.90, 96.98, 97.11}, S→D R@1 {96.87, 97.22, 98.01, 97.82}. Means computed as arithmetic averages across the four altitudes. | Mean Drone→Satellite R@1=97.13 | false | SUES-200 metrics in the paper are reported per altitude. The leaderboard requires the mean across the four altitudes, computed here from Table 2. |
| MADA-SSA<br><sub>supervised, per-altitude training, weight-sharing ConvNeXt-Base backbone, drone+satellite only, 384x384 input</sub> | [MADA-SSA: Multi-Axis Directional Attention and Spatial-Semantic Aggregation for Robust Drone-to-Satellite Geo-Localization](https://doi.org/10.21203/rs.3.rs-9512906/v1) | Table 2 (Drone→Satellite and Satellite→Drone blocks), mean computed across 150m/200m/250m/300m | Mean Drone→Satellite R@1=94.165 | false | Per-altitude values: D→S R@1 88.12/94.17/96.65/97.72; D→S AP 90.44/95.31/97.38/98.25; S→D R@1 96.25/98.75/98.75/97.50; S→D AP 87.33/96.12/97.64/97.71. Means computed by auditor. |
| MFFN-AAE<br><sub>Swin-B backbone, official SUES-200 training and test splits across all four altitudes (150/200/250/300m), single-image retrieval</sub> | [Multilevel Feedback Joint Representation Learning Network Based on Adaptive Area Elimination for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3396330) | Table III | Mean Drone→Satellite R@1=93.26 | false | Per-altitude values from Table III averaged across 150/200/250/300m. Drone→Satellite R@1 mean = (88.07+93.75+95.07+96.15)/4 = 93.26; AP mean = (90.82+94.81+95.98+96.83)/4 = 94.61. Satellite→Drone R@1 mean = (95.00+96.26+96.25+97.50)/4 = 96.25; AP mean = (88.23+93.60+94.75+96.05)/4 = 93.16. |
| SDPL<br><sub>ResNet-50 backbone, 256x256, official per-altitude train/test split, single-pass retrieval; mean computed across 150/200/250/300m</sub> | [SDPL: Shifting-Dense Partition Learning for UAV-View Geo-Localization](https://doi.org/10.1109/tcsvt.2024.3424196) | Table V | Mean Drone→Satellite R@1=92.39 | false | Mean across four altitudes (150/200/250/300m). Per-altitude values: D->S R@1 = 82.95/92.73/96.05/97.83, D->S AP = 85.82/94.07/96.69/98.05; S->D R@1 = 93.75/96.25/97.50/96.25, S->D AP = 83.75/92.42/95.65/96.17. |
| GLQINet (ConvNeXt-Tiny)<br><sub>Supervised, ConvNeXt-Tiny backbone pre-trained on ImageNet, official per-altitude SUES-200 train/test splits, drone and satellite only</sub> | [Enhancing cross view geo localization through global local quadrant interaction network](https://doi.org/10.1038/s41598-025-18935-6) | Table 2 (per-altitude values averaged across 150m/200m/250m/300m: D→S R@1 = (82.07+91.50+96.72+96.82)/4; D→S AP = (85.55+93.33+97.49+97.42)/4; S→D R@1 = (95.00+98.75+98.75+98.75)/4; S→D AP = (85.44+95.26+97.14+97.98)/4) | Mean Drone→Satellite R@1=91.7775 | false | Per-altitude values from Table 2. Means computed as the unweighted average across the four official flight altitudes (150m, 200m, 250m, 300m) for each retrieval direction. |
| AFMS-Net<br><sub>ViT-S backbone pretrained on ImageNet; 120 epochs, SGD, batch size 8; per-altitude training as in official SUES-200 protocol</sub> | [Adaptive Frequency Enhancement and Multi-Scale Semantic Interaction for Robust Cross-View Geo-Localization](https://doi.org/10.21203/rs.3.rs-9537179/v1) | Table 2 | Mean Drone→Satellite R@1=90.715 | false | Mean values computed from the four altitudes (150m, 200m, 250m, 300m). Drone→Satellite R@1: (85.25+90.53+93.03+94.05)/4 = 90.715. Drone→Satellite AP: (88.24+92.24+94.32+95.25)/4 = 92.5125. Satellite→Drone R@1: (97.50+98.75+98.75+97.50)/4 = 98.125. Satellite→Drone AP: (96.50+92.01+93.55+94.23)/4 = 94.0725 (using AP values 96.50, 92.01, 93.55, 94.23 as listed in Table 2 for 150m/200m/250m/300m respectively). |
| ConvNeXt-based Multi-level Representation Learning<br><sub>Supervised, ConvNeXt-Tiny backbone, input size 256x256, standard per-altitude train/test splits</sub> | [Multi-level representation learning via ConvNeXt-based network for unaligned cross-view matching](https://doi.org/10.1080/10095020.2024.2439385) | Table 3 | Mean Drone→Satellite R@1=90.625 | false | Per-altitude values from Table 3: Drone→Satellite R@1 = {83.05, 89.65, 94.05, 95.75}, AP = {86.00, 91.81, 95.62, 96.30}; Satellite→Drone R@1 = {95.00, 96.25, 97.50, 98.80}, AP = {91.82, 93.43, 96.40, 97.06}. Means computed by averaging across the four altitudes (150m, 200m, 250m, 300m). |
| MBF<br><sub>Official SUES-200 training/test splits (120 train / 80 query + 200 gallery locations), all four altitudes (150m, 200m, 250m, 300m), drone and satellite only, Hybrid ViT backbone, 384x384 input, single-pass retrieval with cosine distance.</sub> | UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization | Table 5 of the paper (MBF row across four altitudes), averaged over the four heights. | Mean Drone→Satellite R@1=88.955 | false | Per-altitude values: D→S R@1: 85.62, 87.43, 90.65, 92.12 (mean ≈ 88.96). D→S AP: 88.21, 90.02, 92.53, 93.63 (mean ≈ 91.10). S→D R@1: 88.75, 91.25, 93.75, 96.25 (mean = 92.50). S→D AP: 84.74, 89.95, 90.65, 91.60 (mean ≈ 89.24). |
| SFT<br><sub>Satellite-free training; multi-view UAV sequences reconstructed via 3DGS into pseudo-orthophotos, DINOv3 + Fisher vector aggregation learned from drone data only; results averaged over all four official altitudes (150m, 200m, 250m, 300m)</sub> | [Satellite-Free Training for Drone-View Geo-Localization](http://arxiv.org/abs/2604.01581v2) | Table 2, p5-6; computed as mean across the four altitudes (150m, 200m, 250m, 300m) | Mean Drone→Satellite R@1=85.85 | false | Per-altitude values from Table 2: D→S R@1 = 78.75/82.50/88.65/93.50, D→S AP = 81.86/85.51/90.75/94.87, S→D R@1 = 78.75/88.75/95.00/97.50, S→D AP = 63.03/80.77/88.81/92.34. Query/gallery is a multi-view reconstructed pseudo-orthophoto rather than a single drone image, which deviates from the standard single-image protocol. The four-altitude mean is included to match the leaderboard's official averaged metric. |
| UniABG<br><sub>unsupervised</sub> | [UniABG: Unified Adversarial View Bridging and Graph Correspondence for Unsupervised Cross-View Geo-Localization](http://arxiv.org/abs/2511.12054v1) | Table 3 (PDF p7.2 and p7.3) | Mean Drone→Satellite R@1= | false | Unsupervised method. Paper reports per-altitude numbers only; the mean across altitudes is not explicitly reported. Per-altitude R@1 and AP are provided for all four altitudes (150m, 200m, 250m, 300m) in both directions. |

## Standard Supervised Cross-View Retrieval (Drone→Satellite)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| IFS-Net<br><sub>ResNet-50 backbone, 256×256 input, cross-entropy loss, trained on official SUES-200 training split</sub> | [Multibranch Joint Representation Learning Based on Information Fusion Strategy for Cross-View Geo-Localization](https://doi.org/10.1109/TGRS.2024.3378453) | Table III | Mean Drone→Satellite R@1=89.2625 | false | Means computed from per-altitude results: D→S R@1: (77.57+89.50+92.58+97.40)/4=89.26; D→S AP: (81.30+91.40+94.21+97.92)/4=91.21; S→D R@1: (93.75+97.50+97.50+100.00)/4=97.19; S→D AP: (79.49+90.52+96.03+97.66)/4=90.93. |

## drone-to-satellite @ 150m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1=90.75 | false | Lowest altitude in SUES-200 evaluation. |

## drone-to-satellite @ 200m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1= | false | Exact value not extracted from visible table cell; AP reported to gradually increase from 92.32 to 98.10 across altitudes. |

## drone-to-satellite @ 250m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1= | false | Exact value not extracted from visible table cell. |

## drone-to-satellite @ 300m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1=97.85 | false | Highest altitude in SUES-200 evaluation. |

## satellite-to-drone @ 150m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1=95.00 | false | Lowest altitude, satellite-to-drone task. |

## satellite-to-drone @ 300m altitude

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| CROSS-VIEW<br><sub>ConvNeXt backbone, shared weights, input 384x384, supervised contrastive loss + OFM</sub> | [SCOF Supervised Contrastive Orthogonal Fusion for Robust Cross-View Geolocalization](https://www.semanticscholar.org/search?q=SCOF%20Supervised%20Contrastive%20Orthogonal%20Fusion%20for%20Robust%20Cross-View%20Geolocalization) | Table IX | R@1=97.50 | false | SCOF performance at 300m is slightly inferior to MCCG but surpasses MCCG at first three elevations. |
