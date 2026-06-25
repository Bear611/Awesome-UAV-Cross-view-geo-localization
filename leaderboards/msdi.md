# MSDI

Leaderboard for MSDI. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## Cross-view retrieval (Top-K candidate set within 64 pixels of ground truth)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| GRiM-Net<br><sub>VTRN (retrieval) + RSSDIVCS (matching), evaluated on MSDI</sub> | [GRiM-Net: A Two-Stage Cross-View Visual Localization Framework for UAVs](https://doi.org/10.3390/rs18101477) | Table 5 | R@5=92.2 | false | Recall@K for K=1,2,3,5,8,10: 82.3%, 86.9%, 89.7%, 92.2%, 92.8%, 93.1% |
