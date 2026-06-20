# Leaderboard Full-Text Cookie Requirements

Generated from `data/internal/leaderboard_fulltext_access.yml`.

The leaderboard discovery pipeline can read a Netscape/Mozilla cookie export through
`UAV_CVGL_COOKIE_FILE`. Do not commit real cookie files.

## Highest-Value Cookie Domains

| Priority | Provider | Domains to export/search in browser cookies | Why it matters |
|---:|---|---|---|
| 1 | ACM Digital Library | `dl.acm.org`, `acm.org` | ACM pages and PDFs often return 403. `Modern Backbone for Efficient Geo-localization` still needs browser/session access. |
| 2 | IEEE Xplore | `ieeexplore.ieee.org`, `ieee.org` | Several skipped or inaccessible papers are IEEE pages. |
| 3 | SpringerLink | `link.springer.com`, `springer.com`, `static-content.springer.com` | Needed for Springer chapter/article pages such as Focal Hanning Loss. |
| 4 | Elsevier / ScienceDirect | `www.sciencedirect.com`, `sciencedirect.com`, `linkinghub.elsevier.com`, `elsevier.com` | Needed for ScienceDirect pages/PDFs such as MMHCA. |
| 5 | MDPI | `www.mdpi.com`, `mdpi.com` | MDPI PDF URLs can return 403, though PMC mirrors may avoid this for some papers. |
| 6 | NCBI / PubMed / PMC | `pubmed.ncbi.nlm.nih.gov`, `pmc.ncbi.nlm.nih.gov`, `ncbi.nlm.nih.gov` | Usually open, but cookies/session can reduce anti-bot 403s. |
| 7 | DOI and metadata | `doi.org`, `openalex.org`, `semanticscholar.org`, `www.semanticscholar.org`, `arxiv.org` | Mostly metadata, useful for redirects and candidate discovery. |

## Institution Access

If full text is available through a university library login, also export cookies for the institution access domains, for example:

- `sysu`
- `library`
- `cas`
- `ezproxy`
- `vpn`

When available, configure:

```cmd
set UAV_CVGL_COOKIE_FILE=C:\tmp\uav_cvgl_cookies.txt
set UAV_CVGL_EZPROXY_PREFIX=https://your-ezproxy-prefix/login?url={url}
```

The cookie file should be a Netscape/Mozilla-format export from an already logged-in browser session.

## Current Remaining Skipped Full-Text Papers

After MiniMax built-in search retries plus the exported CARSI/CAS cookie file, the remaining skipped papers all require a real browser session,
publisher PDF entitlement, or manual PDF download. They no longer fail because of the pipeline wall-clock timeout.

- `Contrastive Learning Based Visual Place Recognition Pre-Training Framework for UAV Geo-Localization`
- `Direction-Guided Multiscale Feature Fusion Network for Geo-Localization`
- `Focal Hanning Loss: Revisiting the Heatmap Classification for UAV Self-localization`
- `MMHCA: Multi-feature representations based on multi-scale hierarchical contextual aggregation for UAV-view geo-localization`
- `Modern Backbone for Efficient Geo-localization`
- `Navigating the Metaverse: UAV-Based Cross-View Geo-Localization in Virtual Worlds`

`UAV's Status Is Worth Considering: A Fusion Representations Matching Method for Geo-Localization` was recovered through MiniMax-assisted discovery and PMC full text, then reviewed and included.

After exporting or refreshing cookies, run:

```cmd
set MINIMAX_API_KEY=your_minimax_key
set UAV_CVGL_COOKIE_FILE=C:\tmp\uav_cvgl_cookies.txt
scripts\run_remaining_fulltext_after_cookies.cmd
```

If a publisher still returns 403/420 or an HTML shell without article text, open that specific page through `scripts\open_publisher_page.py`, download
the PDF manually if access is available in the visible browser, and then add a direct local/PDF cache handling step before re-running review.
