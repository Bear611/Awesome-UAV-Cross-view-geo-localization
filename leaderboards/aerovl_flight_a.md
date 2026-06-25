# AeroVL (Flight A)

Leaderboard for AeroVL (Flight A). Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view (UAV aerial query vs. Google Maps satellite reference database) image retrieval; Recall@1 = top-1 correct retrieval; Georeference Recall = correctly localized if lat/lon error within threshold

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GPS-BLIND<br><sub>DINOv2 ViT-L pre-trained (foundation model), no task-specific fine-tuning reported; PCA dimensionality reduction applied</sub> | [Visual Localization system for GPS-Blind Environments in Unmanned Aerial Vehicles](https://doi.org/10.1109/icct62929.2024.10875019) | Table II, AeroVL Flight A | Recall@1=0.62 | false | Georeference Recall = 0.69; 1864 query images vs. 7482 database tiles (63 km²); with local feature similarity threshold filter system reaches ~99% true positive rate |
