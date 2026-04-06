# Quarterly Objectives

This page tracks quarterly objectives and their related repositories across Program Increments (PIs).

## Current PI: 26.2

| # | Objective | Contributors | Repos |
|---|-----------|--------------|-------|
| [#1](https://github.com/NASA-IMPACT/science-support/issues/1) | Hub Support | wildintellect, jsignell | repo2docker-action, pangeo-docker-images, pangeo-notebook-veda-image |
| [#2](https://github.com/NASA-IMPACT/science-support/issues/2) | Cloud Optimized Workflows | wildintellect, jsignell | veda-docs, maap-documentation, cloud-optimized-geospatial-formats-guide |
| [#3](https://github.com/NASA-IMPACT/science-support/issues/3) | Open-Source Contributions | jsignell, ircwaves, tylanderson | stac-best-practices, stac-spec, dask, pystac, pystac-client, xarray |
| [#9](https://github.com/NASA-IMPACT/science-support/issues/9) | Data Retention Policy | smk0033 | - |
| [#10](https://github.com/NASA-IMPACT/science-support/issues/10) | VEDA Forum (Stretch) | smk0033 | - |
| [#11](https://github.com/NASA-IMPACT/science-support/issues/11) | AI Embedding Report (Stretch) | omshinde | - |
| [#12](https://github.com/NASA-IMPACT/science-support/issues/12) | Merge MAAP Documentation into VEDA (Stretch) |  | - |

---

---

## Visualization

The charts use color-coding to show which objective each repo contributes to. Repos that contribute to multiple objectives are shown with split bars.

![PI-26.2 Commits per Repository](images/pi-26.2-authored-commits.png)

![PI-26.2 Resolved issues/PRs](images/pi-26.2-resolved-issues-prs.png)

---

## Configuration

Objectives are configured in [`reports/config.py`](https://github.com/NASA-IMPACT/science-support/blob/main/reports/config.py).

To regenerate this page from config:

```bash
cd reports
uv run generate_docs.py
```