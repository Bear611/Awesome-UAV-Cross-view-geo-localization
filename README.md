# Awesome UAV Cross-View Geo-Localization

A curated taxonomy, benchmark hub, leaderboard collection, and weekly update tracker for **UAV Cross-View Geo-Localization (UAV-CVGL)**.

This repository focuses on UAV-to-satellite, UAV-to-map, and aerial cross-view localization. General UAV navigation, SLAM, and sensor-fusion papers are included only when they are directly related to visual geo-localization, map association, or GNSS-denied relocalization.

## Scope

UAV-CVGL aims to localize UAV images by matching or aligning them with satellite maps, aerial maps, or geo-referenced reference imagery. The output can range from Top-K retrieved satellite tiles to continuous 2D position, meter-level error, heading, or 3-DoF pose.

## Taxonomy

| Category | Definition | Typical Output | Typical Metrics |
|---|---|---|---|
| Retrieval-based UAV CVGL | Given a UAV image, retrieve the most similar satellite tile, place, or region from a large gallery. | Top-K candidates | R@1, R@5, R@10, AP, mAP, SDM |
| Fine Pose Localization / Local Matching | Given a local satellite map or candidate region, estimate the precise UAV position or pose. | Heatmap, 2D coordinate, homography, 3-DoF pose | Position error, heading error, homography error, success rate |
| Unified Global-to-Local UAV Visual Localization | Connect global retrieval and local fine localization into a full wide-area-to-local chain. | Meter-level position or 3-DoF pose | Retrieval recall, PE, HE, Success@threshold, coverage |
| Navigation-aided / Sensor-fusion UAV Geo-localization | Use CVGL as an observation, relocalization, or map-matching module in a navigation system. | Corrected trajectory, relocalized state, map observation | ATE, RPE, localization error, relocalization success |

See [docs/taxonomy.md](docs/taxonomy.md) for detailed definitions.

## Datasets

Dataset inclusion is based on original task design and actual usage in UAV-CVGL papers. Public availability is also tracked because this repository only includes publicly accessible benchmarks in official leaderboards.

See [datasets/datasets.md](datasets/datasets.md) and [leaderboards/dataset_availability.md](leaderboards/dataset_availability.md).

## Leaderboards

Results are organized by **Dataset × Task × Metric × Split**. Different protocols are not mixed. Auxiliary transfer studies, robustness experiments, and non-public benchmarks are listed as notes rather than official leaderboards.

Leaderboard index: [leaderboards/leaderboard_summary.md](leaderboards/leaderboard_summary.md)

Current leaderboard pages:

- [University-1652](leaderboards/university1652.md)
- [SUES-200](leaderboards/sues200.md)
- [DenseUAV](leaderboards/denseuav.md)
- [GTA-UAV / Game4Loc](leaderboards/gta_uav.md)
- [UAV-VisLoc](leaderboards/uav_visloc.md)
- [World-UAV / UAV-GeoLoc](leaderboards/world_uav.md)
- [Nardo-Air](leaderboards/nardo_air.md)

## Paper Lists

- [Retrieval-based UAV CVGL](papers/retrieval.md)
- [Fine Pose Localization / Local Matching](papers/fine_pose_localization.md)
- [Unified Global-to-Local UAV Visual Localization](papers/unified_global_to_local.md)
- [Navigation-aided / Sensor-fusion UAV Geo-localization](papers/navigation_aided.md)

## Weekly Updates

Weekly updates will be maintained in [weekly_updates](weekly_updates/). The intended workflow is daily search, weekly digest, and human verification before formal inclusion.

## Inclusion Rules

- Do not mix different dataset protocols in one leaderboard.
- Do not convert R@1, AP, SDM, meter-level error, and pose metrics into each other.
- Do not add a benchmark to the official leaderboard unless the dataset is publicly accessible or has a clear request/download channel.
- Mark automatically parsed results as `unverified` until manually checked.
- Keep general UAV navigation, SLAM, or path planning papers out unless they directly use visual geo-localization or cross-view map association.

## Contribution

See [docs/contribution.md](docs/contribution.md).

## License

This repository is released under the MIT License unless otherwise specified. Dataset and paper links follow their original licenses.
