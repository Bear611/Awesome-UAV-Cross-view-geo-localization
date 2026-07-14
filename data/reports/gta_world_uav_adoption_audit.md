# GTA-UAV and World-UAV adoption audit

Last checked: 2026-07-14.

## Inclusion policy

The public leaderboard contains one complete proposed method per paper and per official protocol. Loss-function comparisons, backbone sweeps, pre-training variants, component ablations, injected-noise variants, modified datasets, and non-RGB modalities are not ranked together with the canonical RGB benchmark.

## GTA-UAV

Independent adoption was found.

| Paper/method | Dataset setting | Decision | Reason |
|---|---|---|---|
| Game4Loc | GTA-UAV, official Same-Area and Cross-Area | Included | Dataset paper's complete proposed method. |
| PAUL (CVPR 2026) | GTA-UAV, 0% injected correspondence noise, Same-Area and Cross-Area | Included | Independent proposed method with complete official metrics in Table 1. |
| UAV Visual Localization via Multimodal Fusion and Multi-Scale Attention Enhancement | GTA-UAV, RGB-D + EMA | Excluded from canonical leaderboard | Uses an additional depth modality and is not directly comparable with the RGB-only policy. |

The previous 21-row GTA-UAV page mixed the Game4Loc main method with Triplet/InfoNCE losses, Positive-only training, ImageNet pre-training, and backbone sweeps. Those rows are useful ablation evidence but are not separate algorithms; the canonical CSV now contains four rows: two methods × two protocols.

Primary sources:

- [Game4Loc paper](https://arxiv.org/abs/2409.16925) and [official GTA-UAV repository](https://github.com/Yux1angJi/GTA-UAV)
- [PAUL, CVPR 2026](https://openaccess.thecvf.com/content/CVPR2026/html/Li_PAUL_Uncertainty-Guided_Partition_and_Augmentation_for_Robust_Cross-View_Geo-Localization_under_CVPR_2026_paper.html)
- [RGB-D multimodal GTA-UAV study](https://www.mdpi.com/2071-1050/18/9/4277)

## World-UAV

No independent follow-up paper reporting a new method result on World-UAV was found in the checked public sources. The existing comparison rows all come from the UAV-GeoLoc dataset paper: UAVPlace is the proposed method, while Game4Loc-b, AnyLoc variants, DINOv2/LPN, and ResNet18/LPN are baselines or configurations evaluated by the dataset authors.

The page now keeps UAVPlace alone in the official method leaderboard and moves the other eight rows into an explicitly unranked original-paper baseline table.

Primary sources:

- [UAV-GeoLoc official project](https://ringowrw.github.io/GeoLoc-UAV/)
- [UAV-GeoLoc DOI](https://doi.org/10.1109/LRA.2025.3588061)
