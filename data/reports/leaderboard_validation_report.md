# Leaderboard Validation Report

This report validates repository structure and internal consistency. A `verified` flag is treated as a claim in the data, not as independent proof that the original paper was checked.

| Dataset | Rows | Empty metrics | Placeholder methods | Verified flag | Inferred/indirect evidence |
|---|---:|---:|---:|---:|---:|
| University-1652 | 78 | 0 | 0 | 5 | 0 |
| SUES-200 | 130 | 0 | 0 | 96 | 8 |
| DenseUAV | 10 | 0 | 0 | 4 | 0 |
| GTA-UAV | 21 | 0 | 0 | 21 | 0 |

## Evidence boundary

The repair script records rendered-original-table checks for DINOv2+GLFA+CESP, OriLoc, Improving Localization in Internet of Drones, CGSI, SCOF, (MGS)2-Net, AFMS-Net, BGG, Sample4Geo-DPHR, MADA-SSA, ConvNeXt multi-level learning, and MEAN.

Rows still carrying `verified=false`: University-1652 **73**, SUES-200 **34**, DenseUAV **6**, GTA-UAV **0**. These are not declared wrong; they have not all been independently rechecked in this repair.

MFFN-AAE contributes 8 SUES-200 rows restored from extraction evidence; direct visual access to the original table remains pending, so those rows deliberately remain unverified.

SUES-200 rows without AP: **4** (AdaptGeo reports retained R@1 values only). Missing metrics are left absent rather than guessed.

Structural errors: **0**
Warnings: **0**

## Result

All core rows have metrics and numeric sort fields; protocol sets, SUES R@1 coverage, rendered/summary row counts, numeric ranges, duplicate keys, and GTA navigation checks passed.
