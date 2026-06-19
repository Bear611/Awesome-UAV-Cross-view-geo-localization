# SUES-200

These entries are automatically extracted from the v0.4 historical backfill. They are marked unverified and should be manually checked before being treated as an official ranking. Rows are grouped by dataset-specific protocol; metrics with different tasks, splits, or units are not mixed.

Auto-extracted rows: **3**.

| Dataset | Task | Split | Metric | Method | Value | Paper | Source | Verified | Notes |
|---|---|---|---|---|---:|---|---|---|---|
| SUES-200 | cross-view retrieval | test, 150 m altitude | AP | Ours (Refined BEV) | 74.5 | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception (2026); Table 1 | false | Table 1 (PDF p10); only paper-reported value; needs manual verification |
| SUES-200 | cross-view retrieval | test, 150 m altitude | R@1 | Ours (Refined BEV) | 68.0 | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception | Unifying UAV Cross-View Geo-Localization via 3D Geometric Perception (2026); Table 1 | false | Table 1 (PDF p10); only paper-reported value; needs manual verification |
| SUES-200 | Heterogeneous feature matching / robust estimation | UAV–satellite matching (Table 4) | F-score (%) | Spatial Consistency-Guided Sampling (proposed) | 92.65 | A Spatial Consistency-Guided Sampling Algorithm for UAV Remote Sensing Heterogeneous Image Matching | A Spatial Consistency-Guided Sampling Algorithm for UAV Remote Sensing Heterogeneous Image Matching (2025); Table 4 in paper | false | Precision 94.63%, Recall 91.75%, MPE 0.0463 px. Matching F-score, not SUES-200 cross-view retrieval accuracy. Marked unverified. |
