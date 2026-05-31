# PPT 제작 인수인계 가이드

이 문서는 최종 발표 PPT를 만드는 팀원이 분석 흐름과 핵심 결과를 빠르게 이해하고, 어떤 결과물을 어떤 슬라이드에 써야 하는지 판단할 수 있도록 정리한 handoff 문서이다.

분석 결과의 기준 모델은 `core_7_KMeans_k5`이다. Step 6/7의 classification은 churn prediction이 아니라, 최종 K-Means k=5 segment label을 core_7 행동 feature로 재현하고 신규 고객 배정 가능성을 확인하는 보조 분석이다.

## 1. 프로젝트 한눈에 보기

이 프로젝트는 BankChurners / Credit Card Customers 데이터를 사용해 신용카드 고객의 이용 행동을 분석하고, 고객을 해석 가능한 5개 segment로 나눈 뒤 segment별 이탈률과 행동 특성을 비교하여 유지 전략을 제안한다.

핵심은 단순히 "고객이 이탈할지"를 맞히는 churn prediction이 아니다. 이탈 여부는 profiling과 전략 해석에 사용하되, clustering input에서는 제외했다. 대신 거래 활동, 거래 감소, 비활성, 상품 관계, 접촉 부담, 신용 활용 행동을 종합해 고객 행동 segment를 만든다.

PPT의 중심 메시지는 다음 문장으로 잡으면 된다.

> 고객의 신용카드 이용 행동을 기반으로 고객을 5개 segment로 나누고, 각 segment의 이탈률과 행동 특성을 비교하여 segment별 유지 전략을 제안한다. 이후 classification은 새 고객을 이 segment 체계에 배정할 수 있음을 보조적으로 확인한다.

PPT에서 가장 강조해야 할 결과는 최종 5개 segment의 행동 프로파일, C3의 높은 이탈/위험 수준, 그리고 segment별 차별화된 유지 전략이다. Step 6/7은 발표 후반부에서 "이 segment 체계를 운영에 연결할 수 있다"는 보조 근거로 짧게 다룬다.

## 2. 전체 분석 파이프라인 요약

| Step | Notebook | Input | Output | Purpose |
|---|---|---|---|---|
| Step 1 EDA | `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb` | `data/raw/머신러닝 데이터 자료(은행카드).csv` | `data/interim/BankChurners_cleaned_v2.csv` | 원본 데이터 구조, 주요 변수, 결측/분포를 확인하고 분석 가능한 형태로 정리한다. |
| Step 2 Feature Engineering | `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb` | Step 1 cleaned data | 중간 feature 포함 preprocessed table | 고객 행동을 설명할 수 있는 거래 활동, 거래 감소, 관계, 접촉, 신용 활용 관련 feature를 설계한다. |
| Step 3 Preprocessing | `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb` | engineered data | `data/interim/BankChurners_Final_Preprocessed.csv` | 모델링 전에 필요한 encoding, scaling, 정제 처리를 수행한다. |
| Step 3.5 Further Preprocessing | `notebooks/03_5_further_preprocessing.ipynb` | `data/interim/BankChurners_Final_Preprocessed.csv` | `data/processed/BankChurners_cluster_input.csv`, `data/processed/BankChurners_profile_table.csv`, `data/processed/cluster_feature_info.json` | clustering에 사용할 core_7 행동 축과 profiling용 table을 분리한다. |
| Step 4 Clustering Model Selection | `notebooks/04_clustering_model_selection.ipynb` | `data/processed/BankChurners_cluster_input.csv`, `data/processed/BankChurners_profile_table.csv` | `data/analysis/clustering_results/09_final_selected_model_core7_kmeans_k5.json`, `data/analysis/clustering_results/13_final_customer_segments_core7_kmeans_k5.csv` | 여러 clustering 후보를 비교하고 최종 모델 `core_7_KMeans_k5`를 선택한다. |
| Step 4.5 Clustering Visualization / Diagnostics | `notebooks/04_5_clustering_visualization.ipynb` | Step 4 candidate labels | `data/analysis/clustering_visualizations/00_review_shortlist_visual_diagnostics_summary.csv` 및 후보별 시각화 | k=4,5,6 후보를 시각적으로 진단하되, 산점도 분리만으로 최종 모델을 결정하지 않는다. |
| Step 5 Segment Profiling & Strategy | `notebooks/05_segment_profiling.ipynb` | `data/analysis/clustering_results/13_final_customer_segments_core7_kmeans_k5.csv` | `data/analysis/segment_profiling/core_7_KMeans_k5/` | 최종 5개 segment의 행동 특성, 이탈률, 위험 신호, 전략을 정리한다. |
| Step 6 Classification Segment Prediction | `notebooks/06_classification_segment_prediction_and_07_feature_importance.ipynb` | `data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv` | `data/analysis/segment_classification/core_7_KMeans_k5/01_classification_metrics_summary.csv` | core_7 feature만으로 최종 segment label을 얼마나 잘 재현할 수 있는지 확인한다. |
| Step 7 Feature Importance | `notebooks/06_classification_segment_prediction_and_07_feature_importance.ipynb` | Step 6 trained models | `data/analysis/segment_classification/core_7_KMeans_k5/09_feature_importance_random_forest.csv`, `11_logistic_regression_coefficients.csv` | 어떤 행동 feature가 segment 배정에 중요한지 보조적으로 해석한다. |

## 3. 데이터와 핵심 feature 요약

사용 데이터는 BankChurners / Credit Card Customers 데이터이다. 최종 segment table 기준 고객 수는 10,127명이며, `Attrition_Flag` 분포는 기존 고객 8,500명, 이탈 고객 1,627명이다.

중요한 한계는 데이터에 모바일 결제나 앱 결제 행동을 직접 나타내는 변수가 없다는 점이다. 따라서 이 프로젝트는 모바일 결제 사용 행태를 직접 관찰했다고 말하면 안 된다. 거래 횟수, 거래 금액, 변화율, 접촉 횟수, 상품 수, 신용 활용률 같은 신용카드 이용 행동 변수로 고객 segment를 해석한다.

`Attrition_Flag`는 segment별 이탈률을 비교하는 profiling 변수이다. 그러나 clustering input에는 넣지 않았다. 즉, segment는 이탈 label을 기준으로 만든 것이 아니라 고객 행동 feature를 기준으로 만든 것이다.

최종 clustering input은 core_7 행동 feature이다.

| Feature | 한 줄 의미 | Segment 구분에 도움이 되는 이유 |
|---|---|---|
| `Activity_Score` | 거래 횟수와 거래 금액을 바탕으로 한 카드 사용 활성도 | 고활동 고객과 저활동 고객을 구분한다. C2는 높고 C3, C4는 낮다. |
| `Count_Decline_Risk_Score` | 거래 횟수 감소 위험 | 거래 빈도가 줄어드는 고객을 포착한다. C3의 핵심 위험 신호이다. |
| `Amount_Decline_Risk_Score` | 거래 금액 감소 위험 | 사용 금액이 줄어드는 고객을 포착한다. C3와 C4를 구분하는 데 중요하다. |
| `Inactivity_Score` | 최근 12개월 비활성 수준 | 장기간 사용하지 않는 고객의 위험 신호를 보조적으로 설명한다. |
| `Product_Relationship_Score` | 카드사와의 상품 관계 강도 | 관계 상품 수가 많은 안정 고객과 관계가 약한 고객을 구분한다. C0는 높고 C2는 낮다. |
| `Contact_Burden_Score` | 고객 접촉 부담 또는 문의/접촉 빈도 | 접촉 피로도가 높은 고객군을 찾는 데 도움을 준다. C3에서 높다. |
| `Credit_Utilization_Score` | 신용 한도 대비 사용 비율 | 신용 활용 중심 고객을 구분한다. C1에서 매우 높다. |

보조로 `Credit_Capacity_Score`도 생성되어 있지만, 최종 `core_7_KMeans_k5` clustering input에는 포함하지 않았다.

## 4. 최종 clustering 선택 요약

최종 clustering model은 `core_7_KMeans_k5`이다.

Step 4와 Step 4.5에서는 `core_7` feature set의 K-Means k=4, k=5, k=6 후보를 비교했다. 최종 선택은 단순 내부 지표 1개로 결정한 것이 아니라, 내부 metric, segment 크기 균형, 이탈률 차이, high-risk signal 차이, 해석 가능성, 전략 활용성을 함께 고려한 결과이다.

산점도에서 cluster가 완벽하게 분리되는 것처럼 보이는지보다, segment profile heatmap에서 행동 패턴 차이가 설명 가능한지, segment별 이탈률과 위험 신호가 전략적으로 의미 있는 차이를 보이는지가 더 중요했다.

| 후보 | Silhouette | Davies-Bouldin | Calinski-Harabasz | 최소/최대 segment 비율 | 이탈률 범위 | High-risk signal 범위 | 해석 |
|---|---:|---:|---:|---:|---:|---:|---|
| `core_7_KMeans_k4` | 0.155 | 1.814 | 1545.2 | 19.1% / 31.8% | 26.7%p | 0.98 | 내부 metric은 양호하지만 segment가 상대적으로 덜 세분화된다. |
| `core_7_KMeans_k5` | 0.145 | 1.838 | 1441.4 | 9.9% / 23.4% | 41.0%p | 1.30 | 최종 선택. 이탈률 차이와 행동 profile 해석, 전략 구분의 균형이 좋다. |
| `core_7_KMeans_k6` | 0.139 | 1.725 | 1346.5 | 8.6% / 20.4% | 47.0%p | 1.47 | 더 세분화되지만 발표와 전략 설계 관점에서는 복잡도가 커진다. |

근거 파일:

- `data/analysis/clustering_results/04_final_model_comparison_core7_kmeans_k456.csv`
- `data/analysis/clustering_results/07_review_shortlist_config.json`
- `data/analysis/clustering_results/09_final_selected_model_core7_kmeans_k5.json`
- `data/analysis/clustering_visualizations/00_review_shortlist_visual_diagnostics_summary.csv`

## 5. 최종 5개 segment 요약

아래 표는 `data/analysis/segment_profiling/core_7_KMeans_k5/00_segment_summary_core7_kmeans_k5.csv`, `10_segment_strategy_table_k5.csv`, `12_segment_final_summary_k5.csv`를 기준으로 정리했다. `Segment_Name`은 산출물에 포함되어 있지만, PPT에서는 C0~C4를 기본 label로 쓰고 설명 문장으로 특성을 풀어 쓰는 편이 안전하다.

| Segment | Size / Ratio | Key behavior profile | Attrition / risk level | Suggested strategy | PPT message |
|---|---:|---|---|---|---|
| C0 | 2,373명 / 23.4% | 상품 관계가 강함. `Product_Relationship_Score`가 높고, 신용 활용률은 낮은 안정 고객군. | 이탈률 8.6%, 평균 high-risk signal 0.60, Low | 기존 상품 관계 유지, 과도한 접촉 지양, 맞춤형 부가 혜택 제안 | 관계가 이미 깊은 안정 고객이므로 공격적 프로모션보다 유지와 만족 관리가 적합하다. |
| C1 | 2,258명 / 22.3% | 신용 활용도가 매우 높음. `Credit_Utilization_Score`가 가장 높고 이탈률은 낮음. | 이탈률 8.2%, 평균 high-risk signal 0.37, Low | 신용 이용 패턴 기반 한도·금리·상환 안내, 우량 금융활용 고객 관리 | 신용 활용 중심의 우량 고객으로, 금융 활용 편의성과 리스크 관리를 함께 제공한다. |
| C2 | 2,324명 / 22.9% | 활동성은 가장 높지만 상품 관계가 약함. `Activity_Score`는 높고 `Product_Relationship_Score`는 낮음. | 이탈률 8.1%, 평균 high-risk signal 1.02, Low | 주거래화 유도, 관계 상품 확대, 활동 기반 교차판매 캠페인 | 많이 쓰지만 관계가 얕은 고객이다. 교차판매와 관계 확대의 기회가 크다. |
| C3 | 2,174명 / 21.5% | 거래 횟수·금액 감소, 저활동, 접촉 부담이 동시에 나타남. `Count_Decline_Risk_Score`, `Amount_Decline_Risk_Score`, `Contact_Burden_Score`가 높음. | 이탈률 46.0%, 평균 high-risk signal 1.67, High | 최우선 이탈 방어, 거래 감소 원인 확인, 접촉 피로도 완화, 관계 회복형 혜택 제공 | 가장 중요한 위험 segment이다. 유지 전략의 우선순위를 C3에 두는 것이 발표의 핵심이다. |
| C4 | 998명 / 9.9% | 활동성은 낮지만 거래 감소 신호도 낮음. 거래 변화율은 안정적이고 이탈률이 가장 낮음. | 이탈률 4.9%, 평균 high-risk signal 0.44, Low | 저비용 유지 관리, 불필요한 프로모션 최소화, 안정 고객 모니터링 | 조용하지만 안정적인 고객군이다. 비용 효율적인 유지 관리가 적합하다. |

추가로 발표에서 한 문장으로 요약하면 다음과 같다.

> C3는 전체 고객의 21.5%이지만 이탈률이 46.0%로 압도적으로 높아 최우선 관리 대상이며, C0/C1/C2/C4는 낮은 이탈률 안에서도 관계 강화, 금융 활용 관리, 교차판매, 저비용 유지라는 서로 다른 전략이 필요하다.

## 6. PPT에 반드시 사용할 핵심 결과물

| 우선순위 | Slide usage | File path | What it shows | How to explain | Presenter caution |
|---|---|---|---|---|---|
| 1 | Main slide | `data/analysis/segment_profiling/core_7_KMeans_k5/03_cluster_profile_heatmap_k5.png` | C0~C4의 core_7 행동 feature 평균 차이 | 각 segment가 어떤 행동 축에서 높고 낮은지 보여주는 핵심 그림이다. C3는 거래 감소/접촉 부담, C2는 활동성, C1은 신용 활용, C0는 상품 관계가 두드러진다. | 색이 진하다고 곧바로 이탈 원인이라고 말하지 않는다. 행동 profile 차이로 설명한다. |
| 2 | Main slide | `data/analysis/segment_profiling/core_7_KMeans_k5/04_attrition_rate_by_segment_k5.png` | Segment별 이탈률 | C3의 이탈률이 46.0%로 다른 segment보다 훨씬 높다는 점을 강조한다. | Segment는 이탈 label로 만든 것이 아니라 행동 feature로 만든 뒤 이탈률을 비교한 것이다. |
| 3 | Main slide | `data/analysis/segment_profiling/core_7_KMeans_k5/05_segment_size_vs_attrition_bubble_k5.html` | Segment size와 이탈률을 함께 보여주는 bubble chart | C3는 규모도 작지 않고 이탈률도 높아 우선순위가 높다. C4는 작고 이탈률이 낮다. | HTML 파일이라 PPT에는 screenshot 또는 이미지 변환이 필요할 수 있다. |
| 4 | Main slide | `data/analysis/segment_profiling/core_7_KMeans_k5/07_high_risk_signal_count_by_segment_k5.png` | Segment별 평균 high-risk signal count | C3가 평균 1.67개로 가장 높고, C2도 1.02개로 관계 취약 신호가 있다. | High-risk signal은 보조 지표이며, 이탈 확률 그 자체가 아니다. |
| 5 | Main slide | `data/analysis/segment_profiling/core_7_KMeans_k5/10_segment_strategy_table_k5.csv` | Segment별 규모, 이탈률, profile, 전략 요약 | 전략 슬라이드의 표 원본으로 사용한다. C3는 최우선 방어, C2는 관계 확대, C1은 금융 활용 관리가 핵심이다. | 표를 그대로 다 넣기보다 발표용으로 5행 요약표로 줄이는 것이 좋다. |
| 6 | Appendix or short support slide | `data/analysis/segment_classification/core_7_KMeans_k5/06_model_comparison.png` | Segment label reproduction 모델 비교 | Logistic Regression accuracy 0.990, Macro F1 0.989로 최종 segment label이 core_7 feature에서 안정적으로 재현된다. | "이탈을 99% 예측했다"라고 말하면 안 된다. |
| 7 | Appendix | `data/analysis/segment_classification/core_7_KMeans_k5/07_confusion_matrices.png` | 모델별 confusion matrix | 대부분의 segment가 잘 재현되며, C3도 Logistic Regression 기준 recall 0.989로 높다. | 모든 모델별 matrix를 본문에서 자세히 설명할 필요는 없다. |
| 8 | Appendix or support slide | `data/analysis/segment_classification/core_7_KMeans_k5/10_feature_importance_random_forest.png` | Random Forest feature importance | `Credit_Utilization_Score`, `Activity_Score`, `Product_Relationship_Score`, 거래 감소 score가 segment 구분에 중요하게 나타난다. | Random Forest 중요도는 보조 해석이다. 최종 전략은 Step 5 profiling을 중심으로 설명한다. |
| 9 | Appendix or support slide | `data/analysis/segment_classification/core_7_KMeans_k5/12_logistic_regression_coefficient_heatmap.png` | Logistic Regression coefficient 방향성 | 각 segment 배정에 어떤 feature가 양/음 방향으로 작용하는지 보조적으로 확인한다. | coefficient는 standardized feature 기반 해석이므로 절대적인 원인 효과로 말하지 않는다. |

보조 CSV:

- `data/analysis/segment_profiling/core_7_KMeans_k5/06_high_risk_signal_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/01_classification_metrics_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/08_c3_performance_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/09_feature_importance_random_forest.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/11_logistic_regression_coefficients.csv`

Random Forest tuning 결과 `data/analysis/segment_classification/core_7_KMeans_k5/04_random_forest_tuning_result.csv`는 appendix 수준으로만 사용한다. 최종 발표의 중심 스토리는 tuning이 아니라 segment profiling과 전략이다.

## 7. Step 6/7 해석 가이드

Step 6/7은 매우 조심해서 설명해야 한다.

Step 6의 target은 `Attrition_Flag`가 아니다. Target은 Step 4/5에서 확정된 최종 K-Means k=5 segment label인 `Cluster`이다. Input은 `Activity_Score`, `Count_Decline_Risk_Score`, `Amount_Decline_Risk_Score`, `Inactivity_Score`, `Product_Relationship_Score`, `Contact_Burden_Score`, `Credit_Utilization_Score`로 구성된 core_7 행동 feature이다.

따라서 Step 6은 churn prediction이 아니라 segment label reproduction / assignment 문제이다. 목적은 새 고객에게도 같은 core_7 feature를 계산하면 기존 5개 segment 체계에 배정할 수 있는지 확인하는 것이다.

실제 결과는 다음과 같다.

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| Logistic Regression | 0.990 | 0.989 |
| LightGBM | 0.958 | 0.956 |
| XGBoost | 0.957 | 0.954 |
| Random Forest | 0.942 | 0.939 |
| Decision Tree | 0.893 | 0.884 |

Logistic Regression의 성능이 높은 이유는 이탈을 잘 맞혔기 때문이 아니라, 최종 segment label이 core_7 행동 feature의 조합으로 안정적으로 재현되기 때문이다. C3 기준으로도 Logistic Regression의 precision은 0.995, recall은 0.989, F1은 0.992이다.

PPT에서 금지해야 하는 표현 예시:

```text
이 모델은 이탈을 99% 정확도로 예측했다.
```

PPT에서 써야 하는 표현:

```text
최종 segment label을 core_7 행동 feature만으로 높은 정확도로 재현했다.
```

Step 6/7은 발표에서 짧게 다루는 것이 좋다. 핵심 메시지는 다음 한 문장이다.

> 새 고객이 들어와도 동일한 행동 feature를 계산하면 기존 segment 체계에 안정적으로 배정할 수 있다.

## 8. 발표 슬라이드 구성 추천

| Slide | Title | Key message | Recommended figure/table | Speaker note |
|---:|---|---|---|---|
| 1 | 프로젝트 제목 | 신용카드 고객 행동 기반 segment 분석과 유지 전략 제안 | 없음 또는 간단한 title visual | 이 프로젝트는 churn prediction 자체보다 행동 기반 segment와 전략 제안을 목표로 한다. |
| 2 | 배경과 문제 정의 | 고객 이탈 관리는 전체 고객을 한 방식으로 보는 것보다 행동 segment별로 접근해야 한다. | 간단한 문제 정의 diagram | 이탈 여부만 예측하면 어떤 고객에게 어떤 전략을 줄지 설명하기 어렵다. |
| 3 | 데이터와 한계 | BankChurners 데이터는 카드 이용 행동을 담지만 모바일 결제 변수는 직접 없다. | dataset summary table | 분석은 카드 거래 행동 중심이며, 모바일/앱 결제 행동을 직접 관찰했다고 말하지 않는다. |
| 4 | 전체 분석 파이프라인 | EDA부터 segment profiling, classification assignment까지 이어지는 흐름 | 이 문서 2장 pipeline table | Step 5가 본론이고 Step 6/7은 운영화 가능성을 확인하는 보조 단계이다. |
| 5 | 행동 feature 설계 | core_7 feature는 활동성, 감소 위험, 비활성, 관계, 접촉, 신용 활용을 포괄한다. | core_7 feature 설명 표 | `Attrition_Flag`는 clustering input에서 제외했다는 점을 강조한다. |
| 6 | Clustering 모델 선택 | k=5는 metric, 해석 가능성, 전략 활용성의 균형으로 선택했다. | `04_final_model_comparison_core7_kmeans_k456.csv` 기반 요약표 | 산점도 분리보다 profile heatmap과 segment별 이탈/위험 차이가 더 중요했다. |
| 7 | 최종 5개 segment overview | C0~C4는 서로 다른 행동 profile과 전략 필요성을 가진다. | `00_segment_summary_core7_kmeans_k5.csv` 기반 요약표 | segment 이름은 고정 business name이라기보다 분석상 설명 label로 다룬다. |
| 8 | Segment profile heatmap | 행동 feature 차이가 segment 해석의 핵심 근거이다. | `03_cluster_profile_heatmap_k5.png` | C3, C2, C1, C0의 특징을 한눈에 보여주는 핵심 슬라이드이다. |
| 9 | Segment별 이탈률과 위험 비교 | C3는 규모도 작지 않고 이탈률과 위험 신호가 가장 높다. | `04_attrition_rate_by_segment_k5.png`, `07_high_risk_signal_count_by_segment_k5.png` | C3를 최우선 관리 대상으로 제시한다. |
| 10 | Segment별 유지 전략 | Segment별로 방어, 관계 확대, 금융 활용 관리, 저비용 유지 전략을 다르게 제안한다. | `10_segment_strategy_table_k5.csv` 요약표 | 모든 고객에게 같은 캠페인을 하는 것이 아니라 segment별 처방이 다르다는 점을 강조한다. |
| 11 | Classification을 통한 신규 고객 배정 | 기존 segment 체계를 core_7 feature로 안정적으로 재현할 수 있다. | `06_model_comparison.png` | Logistic Regression 성능은 churn prediction이 아니라 segment assignment 성능이다. |
| 12 | 한계와 주의사항 | 데이터와 방법론의 한계를 명확히 둔다. | bullet list | causal claim, 모바일 결제 직접 관찰, 99% 이탈 예측 같은 표현을 피한다. |
| 13 | 결론 | 행동 기반 segment는 이탈 방어 우선순위와 유지 전략 설계에 활용 가능하다. | 최종 message slide | C3 우선 방어와 C2/C1/C0/C4의 차별 전략으로 마무리한다. |

## 9. 발표에서 강조하지 않아도 되는 내용

아래 내용은 분석에는 존재하지만 PPT 본문에서 길게 다룰 필요는 없다. 시간이 부족하면 appendix로 이동하거나 생략한다.

- Step 6의 Random Forest hyperparameter tuning: `04_random_forest_tuning_result.csv`
- 모든 모델의 confusion matrix 세부 해석
- 모든 categorical distribution plot
- raw/interim/processed CSV 파일의 세부 생성 과정
- path handling, 재현성 설정, 폴더 구조 정리 과정
- 개별 notebook code cell의 구현 상세
- k=4, k=6 후보의 모든 시각화 결과
- LDA/PCA 산점도의 세부 해석

특히 scatter plot에서 cluster가 완벽하게 분리되지 않는 점을 방어적으로 길게 설명할 필요는 없다. 이 프로젝트의 핵심은 2D/3D 시각화에서 완벽히 분리되는 군집을 찾는 것이 아니라, 행동 profile과 이탈/위험 차이가 해석 가능하고 전략으로 연결되는 segment를 만드는 것이다.

## 10. 한계와 주의사항

- 데이터에는 모바일 결제 또는 앱 결제 사용 여부를 직접 나타내는 변수가 없다.
- 데이터는 특정 한국 카드사의 실제 내부 데이터가 아니라 BankChurners / Credit Card Customers 데이터이다.
- 이 분석은 cross-sectional 행동 데이터 기반이며, causal analysis가 아니다.
- Clustering 결과는 feature engineering, scaling, algorithm, k 선택에 영향을 받는다.
- Segment는 자연적으로 관찰된 고객 유형이 아니라 분석자가 정의한 행동 기반 pseudo-label이다.
- Step 6/7은 segment assignment / reproduction이지 churn prediction이 아니다.
- `Attrition_Flag`는 clustering input이 아니라 profiling과 segment별 이탈률 비교에 사용한 변수이다.
- Segment별 전략은 분석 결과 기반 제안이며, 실제 캠페인 적용 전에는 비용, 채널, 규제, 고객 피로도 검토가 필요하다.

## 11. PPT 담당자 작업 체크리스트

- [ ] 최종 모델이 `core_7_KMeans_k5`인지 확인한다.
- [ ] 최종 segment table은 `data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv`를 기준으로 사용한다.
- [ ] 최종 segment 요약은 `00_segment_summary_core7_kmeans_k5.csv` 또는 `12_segment_final_summary_k5.csv`를 기준으로 사용한다.
- [ ] 메인 heatmap은 `03_cluster_profile_heatmap_k5.png`를 사용한다.
- [ ] 이탈률 chart는 `04_attrition_rate_by_segment_k5.png`를 사용한다.
- [ ] 위험 신호 chart는 `07_high_risk_signal_count_by_segment_k5.png`를 사용한다.
- [ ] 전략 표는 `10_segment_strategy_table_k5.csv`를 PPT용으로 줄여 사용한다.
- [ ] Step 6 model comparison은 본문 후반 또는 appendix에서 보조 근거로만 사용한다.
- [ ] classification 결과를 이탈 예측 성능으로 설명하지 않는다.
- [ ] C0~C4 label을 기본으로 쓰고, business segment name이 필요하면 분석팀과 최종 명칭을 합의한다.
- [ ] 모바일 결제 행동을 직접 분석했다고 말하지 않는다.
- [ ] 인과관계 표현 대신 "연관된 행동 특성", "segment별 차이", "전략적 시사점"으로 표현한다.

## 참고한 주요 산출물

- `data/processed/cluster_feature_info.json`
- `data/analysis/clustering_results/04_final_model_comparison_core7_kmeans_k456.csv`
- `data/analysis/clustering_results/07_review_shortlist_config.json`
- `data/analysis/clustering_results/09_final_selected_model_core7_kmeans_k5.json`
- `data/analysis/clustering_visualizations/00_review_shortlist_visual_diagnostics_summary.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/00_segment_summary_core7_kmeans_k5.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/01_segment_profile_standardized.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/02_segment_profile_raw_mean_median.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/06_high_risk_signal_summary.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/10_segment_strategy_table_k5.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv`
- `data/analysis/segment_profiling/core_7_KMeans_k5/12_segment_final_summary_k5.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/01_classification_metrics_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/05_cross_validation_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/08_c3_performance_summary.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/09_feature_importance_random_forest.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/11_logistic_regression_coefficients.csv`
- `data/analysis/segment_classification/core_7_KMeans_k5/13_final_logistic_regression_classification_report.csv`
