# MPV-TraC: Multi-Perspective Validated Trace Clustering for Judicial Event Logs

This repository contains the data, code, and results of the cross-specialization empirical study of the **MPV-TraC** (Multi-Perspective Validated Trace Clustering) methodology applied to Brazilian judicial event logs.

The study extends the initial validation reported in Araújo et al. (2025), *Artificial Intelligence and Law* (three Special Civil Courts), to **18 judicial units across six judicial specializations** (Special Civil Courts, Ordinary Civil, Criminal, Electoral, Tax, and Labor), totalling 37 representative clusters analyzed under a multi-perspective protocol.

A *judicial specialization* is the set of subject matters and procedural classes a unit is institutionally authorized to adjudicate. Specializations differ both in the matters they handle and in the procedural rite governing how a case advances from filing to closing, so their event logs describe structurally distinct populations.

## Highlights

- **18 anonymized judicial event logs** drawn from the CNJ Codex data lake, covering six specializations of the Brazilian Judiciary (stored as `.csv.gz` for compact distribution).
- **A reproducible two-phase pipeline**: Phase 1 — systematic parameter search over 6,083 configurations in aggregate; Phase 2 — application of the MPV-TraC protocol on the best configuration of each unit.
- **A multi-perspective reporting template** (one executive table + five complementary figures: boxplots, heatmap, silhouette–F1 scatter, simplicity–fitness trade-off, and specialization radar charts).
- **The complete extraction sheet of the systematic mapping** (71 studies, 2006–2025) in `docs/supplementary/`.
- **Open data and open code** under MIT (code) and CC-BY-4.0 (data) licenses.

## Repository structure

```
mpv-trac-experiment/
├── data/
│   ├── event_logs/                18 cleaned, anonymized event logs (.csv.gz)
│   ├── event_logs_original_pt/    same 18 logs with original Portuguese activity labels
│   ├── translation/               activity-name translation table (PT-BR → EN)
│   ├── anonymization/             anonymization scripts (anonym.py, renumber_ids.py)
│   └── README.md                  data documentation
├── notebooks/
│   ├── 00_data_processing.ipynb   pre-processing pipeline
│   ├── 01_params_search/          Phase 1 — parameter search per specialization (7 notebooks)
│   └── 02_mpv_trac/               Phase 2 — MPV-TraC protocol per unit (15 notebooks)
├── results/
│   ├── params_search/             18 CSVs with the parameter-search configurations per unit
│   ├── figures/                   127 PNGs (silhouettes, t-SNE, heuristic nets per cluster)
│   ├── tables/                    synthesis tables (CSV/JSON)
│   └── notebook_outputs/          original notebooks preserved with execution outputs
├── docs/
│   ├── methodology.md             MPV-TraC summary
│   ├── figures/                   5 paper figures (boxplots, heatmap, scatter, trade-off, radar)
│   └── supplementary/             extraction sheet of the systematic mapping (71 studies)
├── environment.yml                conda environment specification
├── CITATION.cff                   citation metadata
└── LICENSE                        MIT (code) + CC-BY-4.0 (data)
```

## Coverage: 18 judicial units across six specializations

| Code | Specialization | Units |
|---|---|---|
| T1 | Special Civil Courts (Juizados Especiais Cíveis) | T1U1, T1U2, T1U3 |
| T2 | Ordinary Civil | T2U1, T2U2, T2U3 |
| T3 | Criminal | T3U1, T3U2, T3U3 |
| T4 | Electoral | T4U1, T4U2, T4U3 |
| T5 | Tax (Fazenda Pública) | T5U1, T5U2, T5U3 |
| T7 | Labor | T7U1, T7U2, T7U3 |

The gap from T5 to T7 corresponds to the military specialization (T6), originally planned but not included in the final sample. Unit codes follow the `TXUY` scheme, where `X` identifies the specialization and `Y` the unit.

## Reproducing the experiment

### 1. Set up the environment

```bash
git clone https://github.com/tsa2ufpe/mpv-trac-experiment.git
cd mpv-trac-experiment
conda env create -f environment.yml
conda activate mpv-trac
```

Event logs are stored as gzip-compressed CSV (`.csv.gz`). Pandas reads them transparently with `pd.read_csv("path/to/file.csv.gz")`; no extra setup required.

### 2. Run Phase 1 — parameter search

Each notebook in `notebooks/01_params_search/` runs a systematic search over algorithm choice (K-Means, AHC, DBSCAN, HDBSCAN) and clustering hyperparameters, scoring every configuration by the silhouette restricted to the representative clusters, and producing a CSV in `results/params_search/`. Approximate runtime per unit: 2–8 hours on a workstation.

### 3. Run Phase 2 — MPV-TraC protocol per unit

Each notebook in `notebooks/02_mpv_trac/` (named `TXUY.ipynb`) loads the best Phase 1 configuration and applies the four MPV-TraC stages: (i) attribute selection and extraction, (ii) clustering algorithm design, (iii) multi-perspective validation, (iv) result interpretation. Outputs are written to `results/figures/` and `results/tables/`.


## License

- **Code** (notebooks, scripts): [MIT License](LICENSE)
- **Data and figures**: [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/)

