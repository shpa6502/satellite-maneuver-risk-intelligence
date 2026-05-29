## May 29, 2026 Session 1

### Work completed
- Created the initial project directory structure for the Satellite Maneuver Detection & Conjunction Risk Intelligence Platform.
- Added folders for raw data, processed data, external data, notebooks, source code modules, app files, and report figures.
- Added `.gitkeep` files so Git can track empty project directories.
- Committed the initialized project structure to Git.
- Pushed the commit to the GitHub repository.

### Concept applied
**Separation of Concerns**

The project was divided into separate folders based on responsibility:

- `data/raw/` stores original downloaded API data.
- `data/processed/` stores cleaned and transformed data.
- `data/external/` stores outside reference data if needed later.
- `notebooks/` stores exploratory analysis.
- `src/ingestion/` handles data collection.
- `src/cleaning/` handles validation and cleaning.
- `src/features/` handles feature engineering.
- `src/models/` handles anomaly detection models.
- `src/risk/` handles risk scoring logic.
- `src/visualization/` handles plots and visual summaries.
- `app/` will contain the Streamlit dashboard.
- `reports/figures/` stores generated figures for the final report.

### Why this matters
This structure makes the project easier to grow without becoming messy. Since the project includes ingestion, cleaning, feature engineering, anomaly detection, risk scoring, visualization, and dashboard deployment, each part needs its own clear location.

This also supports modular development. Each stage of the pipeline can be built, tested, and improved separately.

### Problem faced
The first commit showed `nothing to commit` because Git does not track empty folders by default.

### Fix / decision
Added `.gitkeep` files inside each empty folder. This allowed Git to track the intended directory structure before actual code or data files were added.

### Git evidence
- Commit message: `chore: initialize pipeline project structure`
- Commit hash: `44830e8`
- Branch: `main`
- Push result: successfully pushed to GitHub

### Files changed
- `app/.gitkeep`
- `data/external/.gitkeep`
- `data/processed/.gitkeep`
- `data/raw/.gitkeep`
- `notebooks/.gitkeep`
- `reports/figures/.gitkeep`
- `src/cleaning/.gitkeep`
- `src/features/.gitkeep`
- `src/ingestion/.gitkeep`
- `src/models/.gitkeep`
- `src/risk/.gitkeep`
- `src/visualization/.gitkeep`

## May 29, 2026 — Session 2

### Work Completed
- Created the first data ingestion script: `src/ingestion/fetch_tle.py`
- Connected the project to the CelesTrak GP JSON API
- Downloaded live satellite data for the `active` group
- Saved the raw API response into `data/raw/`
- Printed a sample satellite record to verify the API response structure
- Committed and pushed the ingestion script to GitHub

### Data Retrieved
| Field | Value |
|---|---|
| Source | CelesTrak GP JSON API |
| Group | `active` |
| Objects received | `15507` |
| Saved file | `data/raw/tle_active_20260529_165859.json` |
| Sample object | `CALSPHERE 1` |
| NORAD ID | `900` |
| Epoch | `2026-05-29T11:36:33.828768` |
| Inclination | `90.2238` |
| Eccentricity | `0.002647` |

### Concept Applied: Data Ingestion

This session implemented the first stage of the data pipeline: collecting raw data from an external API.

The script separates data collection from later cleaning and modeling steps. It only fetches and stores the original API response. No transformation is applied at this stage.

### Why This Matters

Saving raw data first creates a reproducible starting point. If cleaning, feature engineering, or model outputs later look wrong, the original downloaded data can be checked again.

This also follows good pipeline design: ingestion should collect data, cleaning should validate data, and modeling should use processed data.

### Problem Encountered

An SSL certificate error appeared earlier:

```text
certificate has expired (_ssl.c:1032)
```
### Fix / Decision

The script was rerun inside the project virtual environment using:

```powershell
& ".venv\Scripts\python.exe" src/ingestion/fetch_tle.py
```

The request succeeded, confirming that the earlier issue was environment-related rather than a logic error in the ingestion script.

### Git Record

| Field | Value |
|---|---|
| Commit | `feat: add TLE ingestion script for CelesTrak GP JSON API` |
| Hash | `c9eb3d7` |
| Branch | `main` |
| Status | Pushed successfully |

### Files Changed
- `src/ingestion/fetch_tle.py`

### Output Generated
- `data/raw/tle_active_20260529_165859.json`

### Next Step
Build `src/cleaning/clean_tle.py` to load the raw JSON file, validate required orbital fields, convert it into a clean pandas DataFrame, and save the cleaned output into `data/processed/`.

### Git Ignore Decision

Generated data files should not be committed to Git because they can become large and can be recreated by rerunning the pipeline.

To keep the repository clean, a `.gitignore` rule was added for generated data outputs:

```text
data/raw/*.json
data/processed/*.csv
data/processed/*.parquet
```

The raw JSON file was checked with git rm --cached, but Git returned:

fatal: pathspec 'data/raw/tle_active_20260529_165859.json' did not match any files

This confirmed that the raw data file had not been committed. No cleanup was needed.