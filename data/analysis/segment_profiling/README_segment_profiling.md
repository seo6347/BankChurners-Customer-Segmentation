# Step 5. Segment Profiling & Strategy

## 목적

Step 4에서 선택한 최종 clustering 결과를 기반으로 각 고객 세그먼트의 행동 특성, 이탈률, 고위험 신호, 고객 속성 분포를 해석하고 카드사 관점의 유지·재활성화 전략을 제안한다.

## 선택 모델

- Selected key: `axis_6_without_capacity_KMeans_k6`
- Number of clusters: `6`
- Overall attrition rate: `0.1607`

## 입력 파일

- `data/analysis/clustering_results/09_selected_model.json`
- `data/analysis/clustering_results/10_selected_cluster_labels.csv`
- `data/analysis/clustering_results/11_df_cluster_input_used.csv`
- `data/analysis/clustering_results/12_df_profile_table_used.csv`

## 주요 출력 파일

| 파일 | 설명 |
|---|---|
| `cluster_axis_profile_mean.csv` | segment별 행동 축 평균 |
| `final_segment_profiling_table.csv` | segment별 고객 수, 이탈률, 주요 행동 변수, 위험 수준 요약 |
| `segment_strategy_table.csv` | segment별 해석과 유지·재활성화 전략 |
| `01_cluster_profile_heatmap.png` | 행동 축 기반 segment profile heatmap |
| `02_attrition_rate_by_segment.png` | segment별 이탈률 비교 그래프 |
| `03_segment_size_vs_attrition_bubble.html` | segment 규모와 이탈률 bubble chart |
| `04_high_risk_signal_by_segment.png` | segment별 high-risk signal 평균 |
| `categorical_distribution_long.csv` | segment별 범주형 변수 분포 long table |
| `profile_table_with_segment.csv` | 고객 단위 profile table에 cluster/segment label을 붙인 최종 테이블 |

## 해석 주의사항

- `Attrition_Flag`는 clustering input에 사용하지 않았고, segment별 이탈률을 사후적으로 비교하기 위해서만 사용하였다.
- 성별, 소득, 카드 등급, 교육 수준 등 범주형 label은 clustering input에 사용하지 않았고, segment profiling 단계에서만 사용하였다.
- 2D/3D 투영 시각화에서 군집이 완전히 분리되지 않더라도, 본 분석의 핵심 해석은 cluster profile heatmap, segment별 이탈률, high-risk signal 차이를 중심으로 수행한다.
