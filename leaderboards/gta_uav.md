# GTA-UAV / Game4Loc

GTA-UAV 原始论文使用 Cross-Area 与 Same-Area 两套设置。原表指标为 R@1、R@5、AP、SDM@3、Dis@1。

| 方法 / 训练设置 | Cross R@1 | Cross R@5 | Cross AP | Cross SDM@3 | Cross Dis@1 | Same R@1 | Same R@5 | Same AP | Same SDM@3 | Same Dis@1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ours, weighted-InfoNCE + MES, Positive-only | 57.52 | 80.10 | 67.24 | 72.33 | 444.13m | 75.97 | 94.53 | 83.35 | 82.80 | 325.61m |
| Ours, weighted-InfoNCE + MES, Positive + Semi-positive | 55.91 | 81.07 | 66.56 | 76.35 | 342.05m | 84.95 | 97.59 | 90.15 | 88.03 | 149.07m |
| InfoNCE + MES, Positive-only | 52.64 | 74.63 | 62.40 | 67.64 | 552.90m | 72.34 | 91.42 | 80.86 | 81.57 | 369.59m |
| InfoNCE, Positive-only | 49.57 | 72.84 | 59.68 | 65.53 | 612.22m | 72.99 | 90.64 | 80.76 | 80.40 | 363.67m |
| Triplet, Positive-only | 43.41 | 66.70 | 53.56 | 61.26 | 756.95m | 68.22 | 87.99 | 76.73 | 79.17 | 438.38m |
| InfoNCE + MES, Positive + Semi-positive | 45.97 | 71.43 | 57.19 | 71.48 | 460.08m | 65.89 | 93.09 | 77.84 | 86.52 | 196.59m |
| InfoNCE, Positive + Semi-positive | 35.83 | 63.79 | 48.08 | 68.15 | 576.41m | 52.67 | 90.75 | 67.74 | 85.35 | 204.08m |
| Triplet, Positive + Semi-positive | 24.78 | 46.99 | 35.13 | 58.79 | 879.06m | 46.55 | 85.07 | 62.95 | 83.63 | 252.88m |
