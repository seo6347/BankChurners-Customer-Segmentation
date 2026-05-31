# Step 6/7 Segment Classification 요약

## 목적
최종 `core_7_KMeans_k5` segment label을 core_7 행동 feature로 재현하는 classification model을 비교하였다.

## 해석 주의
이 결과는 churn prediction 성능이 아니다. Target은 `Attrition_Flag`가 아니라 최종 K-Means k=5 label인 `Cluster`이다. 높은 Logistic Regression 성능은 segment label reproduction / assignment 성능으로 해석한다.

## 주요 출력
- `01_classification_metrics_summary.csv`
- `07_confusion_matrices.png`
- `09_feature_importance_random_forest.csv`
- `11_logistic_regression_coefficients.csv`
- `13_final_logistic_regression_classification_report.csv`
