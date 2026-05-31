# Step6 담당자용 실행 체크리스트

## 1. 실행 전 확인

아래 파일이 존재해야 한다.

```text
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv
```

없다면 먼저 아래 노트북을 순서대로 실행해야 한다.

```text
04_clustering_model_selection.ipynb
04_5_clustering_visualization.ipynb
05_segment_profiling.ipynb
```

---

## 2. Step6에서 할 일

Step6 담당자가 해야 할 일은 다음 5가지이다.

```text
1. Step5 최종 segment table 불러오기
2. X = core_7 feature, y = Cluster로 설정
3. train/test split 수행
4. Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM 학습 및 평가
5. metrics, confusion matrix, feature importance 저장
```

---

## 3. 제출해야 하는 결과

아래 폴더를 만들어 결과를 저장한다.

```text
data/analysis/segment_classification/core_7_KMeans_k5/
```

최소 제출 파일은 다음이다.

```text
01_classification_metrics_summary.csv
02_classification_report_random_forest.csv
03_confusion_matrix_random_forest.csv
06_model_comparison.png
07_confusion_matrices.png
09_feature_importance_random_forest.csv
10_feature_importance_random_forest.png
14_step6_7_classification_summary.md
```

---

## 4. 결과 해석 시 가장 중요한 질문

결과를 볼 때는 아래 질문에 답하면 된다.

### Q1. 어떤 모델이 가장 좋은가?

`01_classification_metrics_summary.csv`에서 `macro_f1`이 가장 높은 모델을 확인한다.

### Q2. C3를 잘 잡는가?

C3는 최종 초고위험 이탈군이다.  
따라서 `classification_report`에서 C3의 recall을 확인한다.

```text
C3 recall이 높다 = 실제 C3 고객을 잘 찾아낸다.
C3 recall이 낮다 = 초고위험군을 다른 세그먼트로 놓친다.
```

### Q3. 어떤 feature가 segment 구분에 중요한가?

`09_feature_importance_random_forest.csv`를 확인한다.

예상 상위 feature는 다음 중 일부일 가능성이 높다.

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Product_Relationship_Score
Credit_Utilization_Score
Contact_Burden_Score
```

---

## 5. 보고서에 쓰면 좋은 문장

```text
Step6에서는 Step5에서 확정한 최종 k=5 세그먼트 label을 target으로 하여 multi-class classification을 수행하였다. 입력 feature로는 clustering에 사용된 core_7 고객 행동 feature를 사용하였고, Attrition_Flag는 입력 변수에서 제외하였다. 이는 이탈 여부 예측이 아니라 신규 고객을 기존 유지 전략 세그먼트에 배정하기 위한 보조 모델이다.
```

```text
모델 평가는 accuracy뿐 아니라 macro F1-score, confusion matrix, segment별 precision/recall을 함께 사용하였다. 특히 C3는 거래 감소·저활동·접촉 부담형 초고위험 이탈군이므로, C3 recall을 중요하게 확인하였다.
```

---

## 6. 하지 말아야 할 것

```text
Attrition_Flag를 feature로 넣지 말 것
Cluster_Label 또는 Segment_Name을 feature로 넣지 말 것
High_Risk_Signal_Count를 기본 feature로 넣지 말 것
성능을 이탈 예측 성능이라고 해석하지 말 것
k=4 또는 k=6 label로 다시 classification하지 말 것
mock data로 최종 성능을 계산하지 말 것
```

---

## 7. 완료 기준

Step6은 아래 조건을 만족하면 완료로 본다.

```text
classification metrics summary가 저장됨
confusion matrix가 저장됨
random forest feature importance가 저장됨
Step6/7 summary markdown이 저장됨
보고서에서 사용할 핵심 해석 문장이 정리됨
```
