# Step 4.5 Clustering Visualization Diagnostics

This folder contains visualization outputs for the clustering review shortlist.

## Final selected model

- `core_7_KMeans_k5`

A report-ready copy of the final selected model visualizations is saved in:

```text
_final_selected_model_core7_kmeans_k5/
```

## Review candidates

- core_7_KMeans_k4
- core_7_KMeans_k5
- core_7_KMeans_k6

## Main outputs

For each candidate, the notebook saves:

- `01_cluster_size_summary.csv`
- `01_cluster_size_ratio.png`
- `02_cluster_axis_profile_mean.csv`
- `02_cluster_profile_heatmap.png`
- `03_feature_separation_summary.csv`
- `04_attrition_and_risk_summary.csv`
- `04_attrition_rate_by_cluster.png`
- `05_high_risk_signal_summary.csv`
- `05_high_risk_signal_by_cluster.png`
- `06_2d_pca_scatter.html`
- `07_3d_pca_scatter.html`
- `08_3d_direct_risk_view.html`
- `09_3d_direct_behavior_view.html`
- `10_3d_lda_projection.html`

## Interpretation note

These visualizations are diagnostic materials for comparing candidate cluster structures.
The final segment interpretation and strategy design should be completed in Step 5.
For this project, the final segment model is fixed as `core_7_KMeans_k5`.
