# UAV-VisLoc

UAV-VisLoc 原始论文定义的是在大幅卫星地图上确定 UAV 真实坐标。以下两个榜单来自后续论文对 UAV-VisLoc 的实际改造实验，因此不与原论文任务混排。

### Game4Loc Transfer Protocol

| 设置 | Pre-training dataset | R@1 | R@5 | AP | SDM@3 | Dis@1 |
|---|---|---:|---:|---:|---:|---:|
| fine-tune | GTA-UAV | 80.20 | 96.53 | 87.83 | 85.46 | 122.87m |
| fine-tune | DenseUAV | 77.09 | 92.61 | 83.82 | 82.05 | 139.34m |
| fine-tune | SUES-200 | 74.44 | 92.61 | 81.95 | 82.10 | 150.22m |
| fine-tune | ImageNet | 74.41 | 92.36 | 83.29 | 80.94 | 166.63m |
| fine-tune | University-1652 | 73.91 | 93.10 | 82.05 | 82.01 | 170.23m |
| zero-shot | GTA-UAV | 24.94 | 42.59 | 33.15 | 41.40 | 1689.24m |
| zero-shot | DenseUAV | 18.79 | 27.09 | 23.65 | 32.95 | 2051.58m |
| zero-shot | SUES-200 | 16.71 | 27.84 | 22.93 | 34.07 | 1959.02m |
| zero-shot | University-1652 | 9.61 | 19.70 | 14.73 | 31.67 | 2285.08m |
| zero-shot | ImageNet | 8.35 | 16.47 | 13.16 | 26.53 | 2615.08m |

### MM-Geo UAV-VisLoc Protocol

MM-Geo 将 UAV-VisLoc 裁切为 sequence-level retrieval 任务，原表指标为 R@1/R@5/R@10。

| 方法 / 论文 | Seq.04 R@1/R@5/R@10 | Seq.09 R@1/R@5/R@10 |
|---|---:|---:|
| MM-Geo, with rerank | 85.1 / 98.0 / 98.9 | 59.9 / 82.0 / 87.1 |
| MM-Geo, no rerank | 75.5 / 96.1 / 98.0 | 55.1 / 78.3 / 85.9 |
| SALAD | 55.7 / 82.3 / 90.4 | 42.7 / 66.5 / 75.2 |
| AnyLoc | 58.0 / 86.2 / 92.6 | 33.4 / 64.5 / 73.2 |
| DenseUAV* | 51.6 / 79.5 / 88.8 | 38.5 / 67.0 / 76.6 |
| SelaVPR | 44.3 / 72.8 / 81.8 | 29.4 / 55.6 / 66.7 |
| DenseUAV | 42.0 / 70.5 / 79.7 | 25.1 / 47.4 / 60.2 |
