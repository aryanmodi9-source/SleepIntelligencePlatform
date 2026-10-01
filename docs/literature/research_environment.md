# Research Environment Declaration (CLAUDE.md §6.1)

- **Declared:** 2026-10-01 (Phase R, Step 1)
- **Session type:** Claude Code in a managed cloud container. Outbound network goes through an egress proxy that allows only some hosts.
- **Status:** Every capability below was **tested in this session**, not assumed. Each test, its result and its exact target are recorded so it can be repeated.

## 1. Summary — realistic read-level ceiling

| Capability | Result | Consequence |
| --- | --- | --- |
| Web search (`WebSearch`) | **Works.** Returns titles, URLs and a short model-written summary. | Good for discovery only. Search snippets are never evidence (§5.2). |
| Literature connector — **Consensus** (`mcp__Consensus__search`) | **Works (free tier).** Returns up to 10 papers per query, each with title, authors, year, venue, citation count, a consensus.app URL and the **abstract text**. No DOI field. Full-text excerpts (`include_full_text_chunks`) and pages beyond the first need a paid plan. | Gives at most **ABSTRACT_ONLY** read level. DOIs are not shown, so they cannot be checked from this source. |
| Full text — open-access paper | **FAILED.** `pmc.ncbi.nlm.nih.gov`, `europepmc.org`, `arxiv.org`, `zenodo.org`, `core.ac.uk`, `biorxiv.org` and `mdpi.com` are all blocked, both from the shell and through `WebFetch`. | **No FULL_TEXT retrieval is currently possible.** |
| Full text — paywalled paper | **FAILED.** `ieeexplore.ieee.org` and `iopscience.iop.org` are blocked. No institutional access exists either way. | Same as above. |
| DOI / metadata resolution | **FAILED.** `doi.org`, `api.crossref.org`, `api.semanticscholar.org` and `api.openalex.org` are blocked. | The §8 reference verification (resolve every DOI, verify every URL) **cannot be done** in this environment. |
| PhysioNet (`physionet.org`) | **FAILED.** Blocked (proxy returns 403 to CONNECT; `WebFetch` returns EGRESS_BLOCKED). | Dataset documentation cannot be read, and datasets cannot be downloaded or inspected. |
| NSRR (`sleepdata.org`) | **FAILED.** Blocked the same way. | Same as above. NSRR also needs an account and a DUA (to be verified once reachable). |
| Manufacturer datasheets (`analog.com`) | **FAILED.** Blocked. | The MAX30105 datasheet (§26 primary source) cannot be retrieved. |
| Standards / guideline bodies (`aasm.org`) | **FAILED.** Blocked. | Scoring-rule documents (§23) cannot be retrieved. |
| GitHub (`github.com`, `raw.githubusercontent.com`) | **Works**, from the shell and through `WebFetch`. | Can read open-source code and READMEs (e.g. toolboxes). These are §5.2 "secondary technical sources", not papers. |
| Python package index (`pypi.org`, `files.pythonhosted.org`) | **Works.** `pip download wfdb` succeeded. | Analysis tooling can be installed. |
| Cloud object storage (`storage.googleapis.com`, `s3.amazonaws.com`) | **Host reachable** (HTTP 400 / 307 from the services themselves, not a proxy denial). | A possible future route to dataset mirrors. **UNVERIFIED:** whether any dataset is mirrored there, and under what terms, could not be checked because the official documentation is unreachable. No data was requested. |
| General web (`en.wikipedia.org`, etc.) via `WebFetch` | **FAILED.** Blocked. | `WebFetch` is effectively limited to GitHub. |

### Read-level ceiling (binding until the network policy changes)

```text
FULL_TEXT           — not achievable for any paper, datasheet, standard or dataset page
ABSTRACT_ONLY       — achievable via the Consensus connector (abstract text returned)
SECONDARY_CITATION  — achievable (papers known only through another source)
```

Consequences under CLAUDE.md:

- **§7:** every quantitative claim (MAE, RMSE, sensitivity, subject counts, sampling rates, dataset sizes …) must be recorded as `UNVERIFIED_FIGURE`. None can justify a Phase-E requirement or a RESOLVED decision.
- **§9:** no evidence record can be rated `STRONG` for a quantitative or detailed methodological claim.
- **§10:** no claim can reach `ESTABLISHED`, because that requires FULL_TEXT sources.
- **§8:** DOIs and URLs cannot be resolved, so the end-of-phase reference verification cannot be done here.
- **§12–§16 (Gate R1):** dataset modalities cannot be verified from official documentation or by inspecting data. Every dataset-matrix field would stay `UNVERIFIED`. Gate R1 cannot honestly be passed in this environment.
- This limitation **must appear in every gate report** (§6.1).

### What would lift the ceiling

These are human actions: changing the cloud environment's **Network access** setting (environment menu → Edit) to a broader level, or adding hosts to its allowed domains. Minimum useful set:

| Purpose | Hosts |
| --- | --- |
| Open-access full text | `pmc.ncbi.nlm.nih.gov`, `www.ncbi.nlm.nih.gov`, `europepmc.org`, `arxiv.org`, `export.arxiv.org`, `www.biorxiv.org`, `www.medrxiv.org`, `www.mdpi.com`, `zenodo.org` |
| DOI / metadata verification (§8) | `doi.org`, `api.crossref.org`, `api.openalex.org`, `api.semanticscholar.org` |
| Datasets (§13) | `physionet.org`, `sleepdata.org` |
| Datasheets / standards | `www.analog.com`, `aasm.org` |

Paywalled full text (e.g. IEEE Xplore, IOP) would stay unavailable even when reachable, unless the owner supplies institutional access or legally obtained copies. Copies must not be committed to the repository (§6.2).

A different route that needs no network change: the human owner downloads open-access PDFs or dataset documentation and places them **outside the repository**, under the data root (Section 2 of this document). They are then read locally and recorded with `retrieval_route: owner-supplied`.

## 2. Data root

```text
SLEEP_INTEL_DATA_ROOT=/home/user/sleep_intel_data
```

- The directory was created empty, outside the repository. **No datasets have been downloaded** (as instructed for Step 1).
- Environment variables do not carry over between sessions in this container. Set the variable in each session, or in the cloud environment's variables. `.env.example` records the expected name.
- The container is temporary: anything placed under the data root is lost when the session ends unless it is put back.
- Raw data under this root is treated as read-only (§40).

## 3. Tools and versions observed

| Item | Value |
| --- | --- |
| Python | 3.11.15 |
| PyYAML | 6.0.1 (used by `scripts/check_registries.py`) |
| `wfdb` (PhysioNet reader) | 4.3.1 is downloadable from PyPI. It cannot reach PhysioNet while that host is blocked. |
| GitHub access | Git over the session proxy for this repository. The GitHub MCP tools are scoped to `aryanmodi9-source/sleepintelligenceplatform`. |

## 4. Literature connectors visible to this session

| Connector | Visible | Usable | Notes |
| --- | --- | --- | --- |
| Consensus (`mcp__Consensus__search`) | Yes | Yes, free tier | It says it covers Semantic Scholar, PubMed, Scopus and arXiv. It has filters (year, study type, open access, etc.); per the connector's own guidance, filters are applied only when the task calls for them. The connector asks for at most 3 parallel searches to avoid rate limits. Its result pages (`consensus.app/papers/...`) cannot be opened with `WebFetch`, because `consensus.app` is blocked. |
| WebSearch | Yes | Yes | Discovery only. |
| WebFetch | Yes | Only for GitHub hosts | Every academic, dataset and publisher host tested was blocked. |
| PubMed / Europe PMC / Semantic Scholar / OpenAlex APIs | No connector | Blocked over HTTP | — |
| Scopus / Web of Science / Google Scholar | No connector | — | — |

## 5. Test log (reproducible)

All tests ran on 2026-10-01.

| # | Test | Target | Result |
| --- | --- | --- | --- |
| T1 | Web search | `WebSearch("photoplethysmography respiratory rate estimation review Charlton")` | OK. 10 results, among them PMC, Cambridge repository, Zenodo and CORE links. |
| T2 | Consensus search | `mcp__Consensus__search("photoplethysmography derived respiratory rate estimation during sleep")` | OK. 10 papers with abstracts; no DOIs. |
| T3 | Open-access full text | `WebFetch https://pmc.ncbi.nlm.nih.gov/articles/PMC7612521/` (an open-access PMC article surfaced by T1) | EGRESS_BLOCKED |
| T4 | Paywalled paper | `WebFetch https://ieeexplore.ieee.org/document/8073191` | EGRESS_BLOCKED |
| T5 | PhysioNet | `WebFetch https://physionet.org/content/bidmc/1.0.0/`; `curl` of `/content/capnobase/`, `/content/bidmc/1.0.0/`, `/files/bidmc/1.0.0/RECORDS` | EGRESS_BLOCKED / proxy 403 |
| T6 | NSRR | `WebFetch https://sleepdata.org/datasets/mesa`; `curl` of `/datasets/mesa`, `/datasets/shhs` | EGRESS_BLOCKED / proxy 403 |
| T7 | DOI / metadata | `curl` of `https://doi.org/10.1088/1361-6579/aa670e`, `api.crossref.org/works/…`, `api.semanticscholar.org/…`, `api.openalex.org/…` | proxy 403 |
| T8 | Other open-access hosts | `curl` of `europepmc.org`, `arxiv.org`, `export.arxiv.org`, `zenodo.org`, `fileserver-az.core.ac.uk`, `biorxiv.org`, `mdpi.com` | proxy 403 |
| T9 | Datasheet / standards | `curl` of `analog.com/.../MAX30105.pdf`, `aasm.org` | proxy 403 |
| T10 | GitHub | `curl` and `WebFetch` of `raw.githubusercontent.com/MIT-LCP/wfdb-python/main/README.md` | OK |
| T11 | Package index | `pip download --no-deps wfdb` | OK (`wfdb-4.3.1-py3-none-any.whl`; removed afterwards) |
| T12 | Cloud storage | `curl` of `storage.googleapis.com/`, `s3.amazonaws.com/` | Reachable (400 / 307 from the services). No bucket was listed and no data was requested. |
| T13 | General web | `WebFetch https://en.wikipedia.org/wiki/Photoplethysmogram` | EGRESS_BLOCKED |

The DOI and the IEEE document number used in T4 and T7 are **test targets only**. Because they could not be resolved, they are not recorded as sources and support nothing.

## 6. Statement for gate reports

> **Access limitation (from `docs/literature/research_environment.md`):** In this environment no full text, DOI resolution, dataset documentation or dataset download is possible. Literature evidence is capped at ABSTRACT_ONLY (via Consensus). Quantitative claims are therefore `UNVERIFIED_FIGURE`, no claim can be `ESTABLISHED`, and dataset facts remain `UNVERIFIED` until the network policy is widened or the owner supplies material.
