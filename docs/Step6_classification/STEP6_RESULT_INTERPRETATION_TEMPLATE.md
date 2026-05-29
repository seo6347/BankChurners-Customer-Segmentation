# Step6 결과 해석 템플릿

이 파일은 Step6 실행 후 `09_step6_classification_summary.md`를 보완할 때 사용할 수 있는 템플릿이다.

---

## 1. 실험 목적

본 단계에서는 Step5에서 도출한 최종 고객 세그먼트 label을 target으로 하여 classification을 수행하였다.  
이 모델은 이탈 여부를 예측하는 것이 아니라, 고객 행동 feature를 기반으로 신규 고객을 기존 세그먼트에 배정하는 보조 모델이다.

---

## 2. 사용 데이터

입력 파일:

```text
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv
```

Target:

```text
Cluster
```

Input features:

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Inactivity_Score
Product_Relationship_Score
Contact_Burden_Score
Credit_Utilization_Score
```

제외한 컬럼:

```text
Attrition_Flag
Cluster_Label
Segment_Name
High_Risk_Signal_Count
```

---

## 3. 모델 비교 결과

아래 표는 Step6 실행 후 `01_classification_metrics_summary.csv`를 보고 채운다.

| Model | Accuracy | Macro F1 | Weighted F1 | 해석 |
|---|---:|---:|---:|---|
| Logistic Regression | TODO | TODO | TODO | TODO |
| Decision Tree | TODO | TODO | TODO | TODO |
| Random Forest | TODO | TODO | TODO | TODO |

최종 선택 모델:

```text
TODO
```

선택 이유:

```text
TODO
```

---

## 4. Confusion Matrix 해석

확인할 질문:

```text
C3를 C3로 잘 맞히는가?
C3를 C0, C1, C4 같은 저위험군으로 잘못 분류하지 않는가?
어떤 segment끼리 가장 자주 헷갈리는가?
```

해석 작성:

```text
TODO
```

---

## 5. Feature Importance 해석

Random Forest feature importance 상위 feature:

| Rank | Feature | Importance | 해석 |
|---:|---|---:|---|
| 1 | TODO | TODO | TODO |
| 2 | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO |

해석 작성:

```text
TODO
```

주의:

```text
Feature importance는 세그먼트 구분 기준을 의미하며, 이탈의 인과적 원인을 의미하지 않는다.
```

---

## 6. 최종 결론 문장

```text
Step6 classification 결과, 고객 행동 feature만으로도 최종 k=5 세그먼트 label을 일정 수준 이상 재현할 수 있었다. 이는 Step4와 Step5에서 도출한 세그먼트가 고객 행동 feature에 기반한 구조적 차이를 가진다는 점을 보조적으로 보여준다. 다만 본 모델은 이탈 여부를 직접 예측하는 모델이 아니며, 성능은 final segmentation에 대한 surrogate fidelity로 해석해야 한다.
```
