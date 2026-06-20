# Leaderboards

Leaderboard pages use wide tables following each dataset's official protocol. Rows are generated from DeepSeek dataset specifications and MiniMax-M3 per-paper reviews.

Only final flagship method results are included. Ablations, variants, transfer-only results, weather/corruption subsets, TTA, re-ranking, and rows named only `Ours` are excluded.

GitHub Markdown does not support interactive table sorting. The generator sorts each table by the configured primary metric, and can be rerun with `--sort-metric <metric>`.

| Dataset | Page | Included Rows | Default Sort |
|---|---|---:|---|
| University-1652 | [university1652.md](university1652.md) | 51 | R@1 |
| SUES-200 | [sues200.md](sues200.md) | 15 | Mean Drone→Satellite R@1 |
| DenseUAV | [denseuav.md](denseuav.md) | 5 | Recall@1 |
| UAV-VisLoc | [uav_visloc.md](uav_visloc.md) | 0 | Recall@1% |
| GTA-UAV | [gta_uav.md](gta_uav.md) | 2 | Recall@1 |
| Game4Loc | [gta_uav.md](gta_uav.md) | 0 | R@1 |
| Not included | [not_included.md](not_included.md) | 226 | Manual review |
| Sources | [sources.md](sources.md) | - | - |
