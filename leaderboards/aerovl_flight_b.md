# AeroVL (Flight B)

Leaderboard for AeroVL (Flight B). Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view (UAV aerial query vs. Google Maps satellite reference database) image retrieval; Recall@1 = top-1 correct retrieval; Georeference Recall = correctly localized if lat/lon error within threshold

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GPS-BLIND<br><sub>DINOv2 ViT-L pre-trained (foundation model), no task-specific fine-tuning reported; PCA dimensionality reduction applied</sub> | [Visual Localization system for GPS-Blind Environments in Unmanned Aerial Vehicles](https://doi.org/10.1109/icct62929.2024.10875019) | Table II, AeroVL Flight B | Recall@1=0.39 | false | Georeference Recall = 0.44; 3106 query images vs. 5208 database tiles (34 km²); low performance attributed to large proportion of visually homogeneous empty-field scenes |
