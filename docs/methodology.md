# MPV-TraC Methodology

This document summarizes the **MPV-TraC** (Multi-Perspective Validated Trace Clustering) approach applied in this experiment. The complete formalization is in Araújo et al. (2025, *Artificial Intelligence and Law*) and in the doctoral thesis associated with this repository.

## Two-phase experimental design

The experiment is structured in two complementary phases that together constitute a single, replicable protocol.

### Phase 1 — Parameter search

For each of the 18 judicial units, an exhaustive grid search explores combinations of:

- **Clustering algorithm**: K-Means, Agglomerative Hierarchical Clustering (Ward linkage, Euclidean distance), DBSCAN, HDBSCAN.
- **Encoding**: activity profile (frequency-based vector representation over the activity vocabulary).
- **Algorithm-specific hyperparameters**: number of clusters (2–50) for K-Means and AHC; `eps` for DBSCAN; `min_cluster_size` adaptive for HDBSCAN (decreasing from approximately 7.5% of the log down to a statistically significant minimum).

A total of **6,083 configurations** are evaluated per unit. The best configuration is selected by the **silhouette coefficient** restricted to cases assigned to non-noise clusters. The corresponding notebook is `notebooks/01_params_search/params-search_TX.ipynb` (one per competence).

### Phase 2 — MPV-TraC protocol

The best configuration from Phase 1 is then applied to each unit through the four macro-steps of the MPV-TraC protocol, formalized in the methodology chapter of the thesis:

1. **Attribute selection and extraction** — the event log is encoded as an activity profile and normalized to the [0, 1] range.
2. **Clustering algorithm application** — the chosen algorithm and hyperparameters from Phase 1 are applied to the encoded log.
3. **Multi-perspective validation** — three complementary perspectives are integrated:
   - *Cluster quality*: silhouette coefficient on the chosen feature space.
   - *Process-model quality*: structural and behavioral metrics computed over the heuristic-net model discovered from each cluster (number of nodes, number of arcs, Control-Flow Complexity, composite simplicity, fitness, precision, F1).
   - *Substantive validation*: activity-level analysis via the **Lift Calculation in Clusters (LCC)** algorithm, supplemented by expert validation through focus groups (when applicable).
4. **Result interpretation** — clusters are interpreted in light of the research questions and validated against domain knowledge.

Each unit's Phase 2 analysis is conducted in `notebooks/02_mpv_trac/TXUY.ipynb`.

## Representativeness criterion

Only clusters covering **at least 5% of the unit's cases** are considered representative and enter the substantive interpretation. This threshold is exposed as a parameter in the implementation and may be adjusted by the analyst. Across the 18 units, the protocol identifies between 2 and 4 representative clusters per unit, totalling **37 representative clusters** across the extension.

## Multi-perspective comparative analysis

The 37 representative clusters of Phase 2 are then analyzed jointly through a six-figure comparative protocol:

- **Executive table** — synthesizes the best configuration, the number of representative clusters, and the per-unit aggregate metrics ([`results/tables/`](../results/tables/)).
- **Box plots** — intra-competence dispersion of silhouette and process-model metrics ([`docs/figures/fig2_boxplots_by_competence.png`](figures/fig2_boxplots_by_competence.png)).
- **Heatmap** — cluster-by-cluster metric values, granular view ([`fig3_heatmap_clusters.png`](figures/fig3_heatmap_clusters.png)).
- **Silhouette × F1 scatter** — correlation between geometric separability and behavioral fidelity ([`fig4_scatter_silhouette_f1.png`](figures/fig4_scatter_silhouette_f1.png)).
- **Simplicity × Fitness trade-off** — relationship between structural simplification and behavioral fidelity ([`fig5_tradeoff_simplicity_fitness.png`](figures/fig5_tradeoff_simplicity_fitness.png)).
- **Radar charts** — multi-metric signatures per competence ([`fig6_radar_competences.png`](figures/fig6_radar_competences.png)).

Each visualization addresses a distinct analytical question over the same dataset; none individually captures the full picture.

## Key empirical findings

A condensed summary of the experiment's findings, fully developed in the thesis discussion chapter:

1. **VVI heterogeneity between competences** — Variant Variability Index ranges from approximately 0.10 (Ordinary Civil) to approximately 0.95 (Treasury) across the 18 units.
2. **HDBSCAN superiority** — best-performing algorithm in 15 of 18 units (83%).
3. **Cluster parsimony** — the number of representative clusters per unit consistently falls between 2 and 4.
4. **Universal simplification gain** — average simplicity of representative clusters between 0.95 and 0.99 across all competences.
5. **Inter-competence hierarchy** — aggregate performance ranks Ordinary Civil > Criminal > Labor > Electoral > Treasury.
6. **Positive simplicity–fitness correlation** — `r = 0.386, p = 0.018` across the 37 representative clusters, tensioning the classical simplicity-vs.-fidelity trade-off.
7. **Competence-specific weak spots** — Electoral underperforms primarily in silhouette; Treasury, primarily in precision.

## References

- Araújo, T. S. et al. (2025). *Trace clustering for judicial process simplification: identifying patterns guided by business decisions*. **Artificial Intelligence and Law**.
- van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action*. Springer.
- Campello, R. J. G. B. et al. (2015). *Hierarchical Density Estimates for Data Clustering, Visualization, and Outlier Detection*. ACM TKDD.
- Zandkarimi, F.; Kwon, T. (2020). *A generic framework for trace clustering in process mining*. ICPM.
