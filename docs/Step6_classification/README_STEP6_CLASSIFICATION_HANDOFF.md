# Step6 Classification 인수인계 README

## 0. 현재 프로젝트 위치

현재 프로젝트는 Step5까지 완료된 상태이다.

- Step3.5: 고객 행동 기반 clustering feature set 생성
- Step4: 여러 clustering 후보 비교 후 최종 모델 선택
- Step4.5: k=4, k=5, k=6 시각화 진단
- Step5: 최종 k=5 세그먼트 프로파일링 및 세그먼트명 부여
- Step6: 최종 세그먼트 label을 target으로 하는 classification 수행 예정

최종 선택된 세그먼트 모델은 다음이다.

```text
core_7_KMeans_k5
```

Step6의 목적은 **이탈 여부를 예측하는 것**이 아니다.  
Step6의 목적은 **새로운 고객의 최근 이용 행동 feature가 주어졌을 때, 해당 고객을 어떤 유지 전략 세그먼트에 배정할 수 있는지 확인하는 것**이다.

---

## 1. Step6의 핵심 목적

Step6은 다음 질문에 답해야 한다.

> 고객의 행동 feature만 보고, Step5에서 정의한 최종 세그먼트를 예측할 수 있는가?

여기서 target은 `Attrition_Flag`가 아니라 `Cluster` 또는 `Segment_Name`이다.

즉, 일반적인 이탈 예측 모델과 다르다.

| 구분 | 이 프로젝트 Step6 |
|---|---|
| 일반 churn classification | 이탈 여부 `Attrition_Flag` 예측 |
| 본 프로젝트 Step6 | 세그먼트 label `Cluster` 예측 |
| 목적 | 신규 고객을 적절한 유지 전략 그룹에 배정 |
| 핵심 평가 | segment label을 얼마나 잘 재현하는가 |
| 해석 방향 | 어떤 feature가 세그먼트 배정에 중요한가 |

---

## 2. 반드시 사용할 입력 파일

Step6은 Step5 결과물을 입력으로 사용한다.

### 1순위 입력 파일

```text
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv
```

이 파일은 고객 단위 최종 테이블이다. 고객마다 최종 cluster 번호와 segment name이 붙어 있다.

주요 컬럼 예시는 다음과 같다.

| 컬럼 | 의미 |
|---|---|
| `Cluster` | k=5 최종 cluster 번호 |
| `Cluster_Label` | C0, C1, C2, C3, C4 형태 label |
| `Segment_Name` | 사람이 읽을 수 있는 세그먼트명 |
| `Attrition_Flag` | 이탈 여부. Step6 feature로 사용 금지 |
| `High_Risk_Signal_Count` | 위험 신호 개수. 기본 feature로 사용하지 않는 것을 권장 |
| `Activity_Score` 등 core_7 feature | classification 입력 feature 후보 |

### 보조 참고 파일

```text
data/analysis/segment_profiling/core_7_KMeans_k5/12_segment_final_summary_k5.csv
data/analysis/segment_profiling/core_7_KMeans_k5/10_segment_strategy_table_k5.csv
data/analysis/segment_profiling/core_7_KMeans_k5/01_segment_profile_standardized.csv
data/analysis/segment_profiling/core_7_KMeans_k5/02_segment_profile_raw_mean_median.csv
```

이 파일들은 모델 학습용이라기보다, 결과 해석과 보고서 작성용이다.

---

## 3. Step6에서 사용할 feature

가장 안전하고 설명하기 쉬운 기본 feature는 Step4/Step5에서 사용한 core_7 축이다.

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Inactivity_Score
Product_Relationship_Score
Contact_Burden_Score
Credit_Utilization_Score
```

이 7개 feature는 고객 행동을 다음 관점으로 요약한다.

| Feature | 의미 |
|---|---|
| `Activity_Score` | 카드 이용 활성도 |
| `Count_Decline_Risk_Score` | 거래 횟수 감소 위험 |
| `Amount_Decline_Risk_Score` | 거래 금액 감소 위험 |
| `Inactivity_Score` | 비활성 수준 |
| `Product_Relationship_Score` | 카드사와의 관계 강도 |
| `Contact_Burden_Score` | 고객 접촉/문의 부담 |
| `Credit_Utilization_Score` | 신용 한도 활용도 |

처음에는 이 7개 feature만 사용해서 classification을 수행하는 것을 권장한다.  
이유는 Step4의 clustering 자체가 이 feature set을 기준으로 만들어졌기 때문에, Step6 classification의 목적과 가장 잘 맞기 때문이다.

---

## 4. 절대 feature로 넣으면 안 되는 컬럼

아래 컬럼은 classification 입력 feature로 사용하면 안 된다.

| 컬럼 | 사용 금지 이유 |
|---|---|
| `Cluster` | target 자체 |
| `Cluster_Label` | target을 문자로 바꾼 것 |
| `Segment_Name` | target을 사람이 읽기 쉽게 바꾼 것 |
| `Attrition_Flag` | 세그먼트 배정 모델의 목적은 이탈 예측이 아니므로 사용 금지 |
| `High_Risk_Signal_Count` | 보조 검증 지표에 가까움. 기본 모델에서는 제외 권장 |

특히 `Attrition_Flag`를 넣으면 안 된다.  
Step6은 이탈 여부 예측 모델이 아니라, 행동 feature 기반의 세그먼트 배정 모델이다.

---

## 5. 추천 모델 순서

아래 순서대로 수행하면 된다.

### 1단계. Logistic Regression

가장 기본적인 baseline이다.  
해석이 쉽고, 모델이 과하게 복잡하지 않다.

추천 설정:

```python
LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)
```

### 2단계. Decision Tree

세그먼트 분류 규칙을 직관적으로 설명하기 좋다.  
다만 너무 깊게 자라면 과적합될 수 있으므로 `max_depth`를 제한한다.

추천 설정:

```python
DecisionTreeClassifier(
    max_depth=4,
    min_samples_leaf=50,
    class_weight="balanced",
    random_state=42
)
```

### 3단계. Random Forest

성능과 안정성이 좋은 모델이다.  
최종 성능 표에서는 Random Forest를 가장 중요한 후보로 보면 된다.

추천 설정:

```python
RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_leaf=20,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)
```

### 선택. XGBoost / LightGBM

설치되어 있고 담당자가 다룰 수 있다면 추가해도 된다.  
하지만 필수는 아니다. 이 프로젝트에서는 Logistic Regression, Decision Tree, Random Forest만으로도 충분히 Step6 목적을 달성할 수 있다.

---

## 6. 평가 지표

Step6은 5개 segment를 예측하는 multi-class classification이다.

반드시 아래 지표를 확인한다.

| 지표 | 의미 |
|---|---|
| Accuracy | 전체 고객 중 segment를 맞춘 비율 |
| Macro F1-score | segment별 F1을 동일 가중 평균한 값 |
| Weighted F1-score | segment 크기를 반영한 F1 평균 |
| Confusion Matrix | 어떤 segment끼리 자주 헷갈리는지 확인 |
| Segment별 precision/recall | 각 segment별 예측 품질 확인 |

가장 중요하게 볼 지표는 `Macro F1-score`이다.

이유는 segment 크기가 완전히 같지 않기 때문이다.  
Accuracy만 보면 큰 segment를 잘 맞히는 모델이 좋아 보일 수 있다.  
하지만 우리는 C3 같은 초고위험군도 중요하게 봐야 하므로, segment별 성능을 균형 있게 보는 Macro F1-score가 중요하다.

---

## 7. 결과 해석에서 반드시 지켜야 할 표현

Step6 결과는 다음처럼 표현한다.

적절한 표현:

```text
Random Forest 모델은 고객 행동 feature를 바탕으로 최종 k=5 세그먼트 label을 비교적 잘 재현하였다.
이는 Step5에서 정의한 세그먼트 구조가 고객 행동 feature에 의해 설명 가능하다는 것을 보여준다.
```

부적절한 표현:

```text
Random Forest 모델이 이탈 고객을 잘 예측하였다.
```

Step6의 target은 `Attrition_Flag`가 아니므로, 이탈 예측이라고 쓰면 안 된다.

---

## 8. Step6 산출물 저장 위치

Step6 결과는 아래 폴더에 저장하는 것을 권장한다.

```text
data/analysis/classification/core_7_KMeans_k5/
```

권장 출력 파일은 다음과 같다.

```text
00_input_check.json
01_classification_metrics_summary.csv
02_classification_report_by_segment.csv
03_confusion_matrix.csv
04_confusion_matrix.png
05_feature_importance_random_forest.csv
06_feature_importance_random_forest.png
07_logistic_regression_coefficients.csv
08_predicted_segment_table.csv
09_step6_classification_summary.md
```

---

## 9. Step6 이후 다음 단계에서 활용하는 방법

Step6 이후에는 다음과 같이 활용한다.

| Step6 결과 | 후속 활용 |
|---|---|
| Classification metrics | 세그먼트 구조가 feature로 재현 가능한지 검증 |
| Confusion matrix | 어떤 세그먼트가 비슷한지 확인 |
| Feature importance | 세그먼트 구분의 핵심 행동 축 설명 |
| Predicted segment table | 신규 고객 배정 시나리오 설명 |
| Segment별 precision/recall | 고위험군 C3가 잘 잡히는지 확인 |

특히 C3는 최종 초고위험군이므로, C3의 recall이 너무 낮으면 주의해야 한다.  
C3 recall이 낮다는 것은 실제 C3 고객을 다른 segment로 잘못 배정하는 경우가 많다는 뜻이다.

---

## 10. 한 줄 요약

Step6은 **이탈 예측 모델이 아니라, Step5에서 정의한 최종 고객 세그먼트를 신규 고객에게 배정하기 위한 보조 classification 모델**이다.  
따라서 `Attrition_Flag`를 feature로 사용하지 않고, `core_7` 행동 feature만으로 `Cluster`를 예측하는 방식으로 진행한다.
