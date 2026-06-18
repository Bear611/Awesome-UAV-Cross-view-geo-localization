# University-1652

原始任务是 Drone→Satellite target localization 和 Satellite→Drone navigation。原始指标为 R@1 与 AP。

| Rank | 方法 / 论文 | Drone→Satellite R@1 | Drone→Satellite AP | Satellite→Drone R@1 | Satellite→Drone AP | 结果来源 |
|---:|---|---:|---:|---:|---:|---|
| 1 | PFED / MobileGeo, w/ post-process | 97.15 | 97.50 | 95.58 | 96.27 | PFED/MobileGeo 表格 |
| 2 | CGSI | 95.45 | 96.10 | 96.58 | 95.38 | University-1652 official SOTA |
| 3 | DINO-MSRA | 95.14 | 95.92 | 97.29 | 93.81 | DINO-MSRA 表格 |
| 4 | CDM-Net | 95.13 | 96.04 | 96.68 | 94.05 | CDM-Net 表格 |
| 5 | QDFL | 95.00 | 95.83 | 97.15 | 94.57 | University-1652 official SOTA |
| 6 | DAC | 94.67 | 95.50 | 96.43 | 93.79 | DAC 表格 |
| 7 | CAMP | 94.46 | 95.38 | 96.15 | 92.72 | CAMP 表格 |
| 8 | SHAA | 93.69 | 94.68 | 96.15 | 93.49 | University-1652 official SOTA / SHAA 表格 |
| 9 | APA-BI | 93.57 | 94.55 | 95.86 | 92.88 | University-1652 official SOTA |
| 10 | MEAN | 93.55 | 94.53 | 96.01 | 92.08 | MEAN 表格 |
| 11 | MobileGeo / PFED, no post-process | 93.87 | 94.83 | 95.72 | 92.57 | PFED/MobileGeo 表格 |
| 12 | Sample4Geo | 92.65 | 93.81 | 95.14 | 91.39 | University-1652 official SOTA / 多篇对比表 |
| 13 | MCCG | 89.64 | 91.32 | 94.30 | 89.39 | MCCG 表格 |
| 14 | FSRA, k=3 | 84.51 | 86.71 | 88.45 | 83.37 | FSRA 表格 |
| 15 | FSRA, k=1 | 82.25 | 84.82 | 87.87 | 81.53 | FSRA 表格 |
| 16 | LPN | 75.93 | 79.14 | 86.45 | 74.79 | University-1652 official SOTA |
| 17 | Instance Loss + Verification Loss | 61.30 | 65.68 | 75.04 | 62.87 | University-1652 原始 baseline |
