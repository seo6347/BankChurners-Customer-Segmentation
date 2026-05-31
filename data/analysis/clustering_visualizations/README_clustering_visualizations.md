# Step 4.5 Clustering Visualization Diagnostics

이 폴더는 Step 4 review shortlist 후보의 clustering 진단 시각화 결과를 보관한다.

## 최종 선택 모델

- `core_7_KMeans_k5`

보고서와 발표 준비에 바로 참고할 수 있는 최종 모델 시각화 사본은 아래 폴더에 저장된다.

```text
_final_selected_model_core7_kmeans_k5/
```

## 검토 후보

- core_7_KMeans_k4
- core_7_KMeans_k5
- core_7_KMeans_k6

## 주요 출력 파일

각 후보별로 노트북은 다음 파일을 저장한다.

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

## 해석 주의사항

이 시각화는 후보 cluster 구조를 비교하기 위한 진단 자료이다.
Scatter plot에서 군집이 완전히 분리되어 보이는지만으로 모델을 선택하지 않는다.
최종 segment 해석과 전략 설계는 Step 5의 profile heatmap, 이탈률, high-risk signal, strategy table을 중심으로 수행한다.
이 프로젝트의 최종 segment model은 `core_7_KMeans_k5`로 고정한다.
