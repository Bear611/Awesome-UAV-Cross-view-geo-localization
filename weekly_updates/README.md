# Weekly Updates

This folder will track newly found UAV-CVGL papers. The intended workflow is:

1. The scheduled weekly search finds recent candidate papers from three public scholarly indexes and recent OpenAlex citations of the configured benchmark seed papers.
2. Candidate papers are parsed into structured summaries.
3. A weekly digest is generated from papers first discovered in the current ISO week, so prior entries are not repeated.
4. Parsed papers are proposed in the automated PR for `data/papers.yml` and the matching classification/introduction page.
5. Human verification decides whether extracted experimental results are eligible for a public leaderboard; the automation never promotes them directly.

Status labels:

- `newly found`
- `parsed`
- `verified`
- `leaderboard added`
- `needs review`

