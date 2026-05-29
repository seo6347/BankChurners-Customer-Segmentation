# Step6 Classification 초보자용 상세 가이드

이 문서는 데이터분석 경험이 많지 않은 담당자가 그대로 따라갈 수 있도록 작성한 가이드이다.

---

## 1. Step6이 하는 일 한 문장 설명

Step6은 고객을 다음 5개 세그먼트 중 하나로 분류하는 모델을 만든다.

| Cluster | Segment name |
|---|---|
| C0 | 상품 관계 중심 저위험 안정군 |
| C1 | 신용 활용 중심 저위험 금융활용군 |
| C2 | 고활동·저관계 잠재 전환군 |
| C3 | 거래 감소·저활동·접촉 부담형 초고위험 이탈군 |
| C4 | 저활동·비감소형 초저위험 안정군 |

중요한 점:

> 이탈/비이탈을 맞히는 모델이 아니다.  
> 고객이 어떤 세그먼트에 속하는지 맞히는 모델이다.

---

## 2. Classification이란?

Classification은 정답 label이 있는 데이터를 학습해서, 새로운 데이터가 어떤 class에 속하는지 예측하는 방법이다.

예를 들어 개와 고양이를 구분하는 모델은 다음과 같다.

```text
입력: 귀 길이, 몸무게, 털 색깔
정답: 개 / 고양이
```

이 프로젝트에서는 다음과 같다.

```text
입력: 고객 행동 feature 7개
정답: 최종 세그먼트 C0~C4
```

즉, Step6 classification은 다음 구조이다.

```text
고객 행동 feature → classification model → 예측 segment
```

---

## 3. Target과 Feature 구분

데이터분석에서 가장 중요한 구분은 `X`와 `y`이다.

| 기호 | 의미 | 이 프로젝트 예시 |
|---|---|---|
| X | 모델 입력 feature | Activity_Score 등 7개 행동 feature |
| y | 모델이 맞혀야 하는 정답 | Cluster |

이 프로젝트에서는 다음처럼 잡는다.

```python
X = df[
    [
        "Activity_Score",
        "Count_Decline_Risk_Score",
        "Amount_Decline_Risk_Score",
        "Inactivity_Score",
        "Product_Relationship_Score",
        "Contact_Burden_Score",
        "Credit_Utilization_Score",
    ]
]

y = df["Cluster"]
```

---

## 4. 왜 Attrition_Flag를 쓰면 안 되는가?

`Attrition_Flag`는 고객이 실제로 이탈했는지 여부이다.

하지만 Step6의 목표는 이탈 여부를 맞히는 것이 아니다.  
Step6의 목표는 고객을 세그먼트에 배정하는 것이다.

따라서 `Attrition_Flag`를 X에 넣으면 다음과 같은 문제가 생긴다.

```text
신규 고객을 분류할 때는 그 고객이 미래에 이탈할지 미리 알 수 없다.
그런데 모델 학습 때 Attrition_Flag를 사용하면,
현실에서는 사용할 수 없는 정보를 모델에 준 것이 된다.
```

그러므로 `Attrition_Flag`는 feature로 쓰지 않는다.  
다만 segment별 이탈률을 해석할 때 참고하는 것은 가능하다.

---

## 5. Train/Test Split이란?

모델을 평가하려면 데이터를 두 부분으로 나눈다.

| 데이터 | 역할 |
|---|---|
| Train set | 모델 학습용 |
| Test set | 모델 평가용 |

예를 들어 전체 고객이 10,000명이라면:

```text
Train: 7,000명
Test: 3,000명
```

모델은 train 데이터만 보고 학습한다.  
그 후 test 데이터의 feature만 보고 segment를 예측한다.  
그리고 test 데이터의 실제 segment와 비교해 성능을 계산한다.

추천 코드:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)
```

여기서 `stratify=y`는 train/test에 C0~C4 비율이 비슷하게 유지되도록 해준다.

---

## 6. 평가 지표 이해하기

### Accuracy

전체 중 맞힌 비율이다.

```text
100명 중 90명을 맞히면 accuracy = 0.90
```

단점은 큰 segment를 잘 맞히면 좋아 보일 수 있다는 것이다.

### Precision

모델이 어떤 segment라고 예측한 고객 중 실제로 그 segment인 비율이다.

예를 들어 모델이 C3라고 예측한 고객 100명 중 실제 C3가 80명이면:

```text
C3 precision = 0.80
```

### Recall

실제 어떤 segment인 고객 중 모델이 그 segment라고 잘 찾아낸 비율이다.

예를 들어 실제 C3 고객 100명 중 모델이 70명을 C3로 맞혔다면:

```text
C3 recall = 0.70
```

C3는 초고위험 이탈군이므로 recall이 중요하다.  
C3 recall이 낮으면 실제 고위험군을 놓친다는 뜻이다.

### F1-score

Precision과 Recall의 균형을 보는 지표이다.

```text
F1-score가 높다 = precision과 recall이 모두 어느 정도 좋다
```

### Macro F1-score

각 segment의 F1-score를 똑같은 비중으로 평균낸 값이다.  
C0, C1, C2, C3, C4가 모두 중요할 때 사용한다.

이 프로젝트에서는 Macro F1-score를 중요하게 본다.

---

## 7. Confusion Matrix 이해하기

Confusion Matrix는 모델이 어떤 segment를 어떤 segment로 헷갈렸는지 보여준다.

예를 들어 C3 고객을 C0로 많이 예측한다면, 모델이 초고위험군을 안정군으로 착각하는 문제가 있다.

Confusion Matrix를 볼 때 중요한 질문은 다음이다.

```text
C3를 다른 segment로 많이 놓치고 있지는 않은가?
C0와 C4처럼 안정군끼리 헷갈리는가?
C2와 C0처럼 전략이 다른 segment를 헷갈리는가?
```

C3를 놓치는 것은 가장 큰 문제이다.  
반면 저위험군끼리 일부 헷갈리는 것은 상대적으로 덜 치명적일 수 있다.

---

## 8. Feature Importance 이해하기

Feature Importance는 모델이 어떤 feature를 중요하게 사용했는지 보여준다.

예를 들어 Random Forest에서 다음 결과가 나왔다고 하자.

| Feature | Importance |
|---|---:|
| Count_Decline_Risk_Score | 0.30 |
| Activity_Score | 0.25 |
| Contact_Burden_Score | 0.18 |

이 경우 다음처럼 해석할 수 있다.

```text
세그먼트를 구분하는 데 거래 횟수 감소 위험, 활동성, 접촉 부담이 중요하게 작용했다.
```

주의할 점:

> Feature importance는 "이탈의 원인"이 아니다.  
> Feature importance는 "세그먼트 구분에 사용된 기준"이다.

이 프로젝트에서는 다음처럼 말해야 한다.

맞는 표현:

```text
거래 횟수 감소 위험은 세그먼트 배정에 중요한 feature로 나타났다.
```

틀린 표현:

```text
거래 횟수 감소 위험이 고객 이탈의 원인이다.
```

---

## 9. Step6 결과를 작성하는 방법

결과 보고서에는 최소한 다음을 포함한다.

1. 사용 데이터
2. Target 정의
3. Feature 정의
4. 사용 모델
5. 평가 지표
6. Confusion Matrix 해석
7. Feature Importance 해석
8. 주의점: 이탈 예측이 아니라 segment 분류임

예시 문장:

```text
본 단계에서는 Step5에서 도출한 최종 k=5 세그먼트 label을 target으로 설정하고, 고객 행동을 요약한 core_7 feature를 입력 변수로 사용하여 multi-class classification을 수행하였다. Logistic Regression, Decision Tree, Random Forest를 비교하였으며, 전체 정확도뿐 아니라 segment별 성능을 확인하기 위해 Macro F1-score와 confusion matrix를 함께 검토하였다.
```

---

## 10. Step6 담당자가 최종적으로 제출할 파일

Step6 담당자는 다음 파일을 만들어 제출하면 된다.

```text
data/analysis/classification/core_7_KMeans_k5/01_classification_metrics_summary.csv
data/analysis/classification/core_7_KMeans_k5/02_classification_report_by_segment.csv
data/analysis/classification/core_7_KMeans_k5/03_confusion_matrix.csv
data/analysis/classification/core_7_KMeans_k5/04_confusion_matrix.png
data/analysis/classification/core_7_KMeans_k5/05_feature_importance_random_forest.csv
data/analysis/classification/core_7_KMeans_k5/06_feature_importance_random_forest.png
data/analysis/classification/core_7_KMeans_k5/09_step6_classification_summary.md
```

위 파일들이 있으면 후속 단계에서 결과를 해석하고 발표 자료에 반영할 수 있다.
