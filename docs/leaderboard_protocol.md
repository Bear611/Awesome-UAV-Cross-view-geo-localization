# Leaderboard Protocol

This repository does not maintain a single global ranking across all UAV-CVGL datasets. Results are organized by:

**Dataset × Task × Metric × Split**

A result can be added to a leaderboard only when the following information is available:

- Dataset and split
- Task definition
- Metric and value
- Paper or official benchmark source
- Whether the result is official or reproduced
- Code availability, if known
- Notes on re-ranking, TTA, external training data, or post-processing

By default, automatically parsed results should be marked as `unverified`. They can be moved into the official leaderboard only after manual checking.

