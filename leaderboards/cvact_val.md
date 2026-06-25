# CVACT_val

Leaderboard for CVACT_val. Rows are generated from data/leaderboards.csv with paper-name hyperlinks.


## ground-to-aerial (UGV query vs. UAV nadir-view reference)

Rows: **1**.

| Method / Training Setting | Paper | Source | Sort | Verified | Notes |
|---|---|---|---:|---|---|
| DOCB + MSFA (Dynamic Online Cross-Batch hard exemplar mining with multi-scale feature aggregation)<br><sub>two-phase training: Phase 1 intra-batch hard exemplar mining; Phase 2 adds cross-batch DOCB mining with FIFO memory bank; weighted soft-margin triplet loss; VGG16 backbone with polar-transformed aerial images; descriptor length 512</sub> | [DOCB: A Dynamic Online Cross-Batch Hard Exemplar Recall for Cross-View Geo-Localization](https://doi.org/10.3390/ijgi14110418) | Abstract and contributions text (Section 1) | R@1=86.34 | false | Value reported in the paper abstract; full R@5/R@10/AP not present in the provided excerpt. |
