# Dataset Availability Rules

A dataset is included in the public leaderboard only when it has a public or otherwise clearly accessible benchmark release and a reproducible protocol. Paper-private datasets, unverified new datasets, auxiliary transfer settings, and robustness-only variants are not mixed into the official tables.

| Dataset / Benchmark | Status | Leaderboard Handling | Notes |
|---|---|---|---|
| University-1652 | Public benchmark | Included | Standard UAV/satellite retrieval protocols. |
| SUES-200 | Public academic benchmark | Included | Altitude-specific protocol; transfer-only rows stay separate or excluded. |
| DenseUAV | Public benchmark | Included | Original self-positioning metrics only; augmented/scale-only variants are excluded. |
| GTA-UAV / Game4Loc | Public benchmark | Included when official Cross/Same protocol results are available | Ablations from the dataset paper are not used as algorithm leaderboard rows. |
| UAV-VisLoc | Public benchmark | Included with protocol labels | Different map/split protocols are not mixed. |
| World-UAV / UAV-GeoLoc | Public benchmark | Included when official results are available | No reviewed rows may appear if the run found no main-protocol values. |
| Nardo-Air | Public related benchmark | Included when protocol-compatible results are available | Aerial localization related; keep source/protocol explicit. |
| Other new datasets | Pending | Not included by default | Requires public release evidence and a clear benchmark protocol. |
