# Step6 Data Leakage 검토 및 운영 원칙

## 1. 현재 우려 지점

현재 clustering은 전체 데이터를 사용하여 수행되었다.  
이후 Step6에서 그 clustering label을 target으로 classification을 수행하면 data leakage가 되는지 걱정할 수 있다.

결론부터 말하면 다음과 같다.

> mock data를 만들 필요는 없다.  
> 다만 Step6 결과를 어떻게 해석하고 보고할지 명확히 구분해야 한다.

---

## 2. 가장 중요한 구분: 이탈 예측 vs 세그먼트 재현

Step6은 이탈 여부 예측이 아니다.

| 구분 | target | leakage 위험 |
|---|---|---|
| 이탈 예측 | `Attrition_Flag` | 이탈 label을 feature로 넣으면 명백한 leakage |
| 세그먼트 재현 | `Cluster` | final cluster label을 target으로 사용 가능. 단, 성능 해석 주의 필요 |

Step6의 target은 `Cluster`이다.  
즉, "이 고객이 이탈했는지"를 맞히는 것이 아니라 "이 고객이 어떤 세그먼트에 속하는지"를 맞히는 것이다.

---

## 3. 전체 데이터로 clustering한 label을 target으로 써도 되는가?

### 가능하다

이 프로젝트의 Step6 목적이 다음이라면 가능하다.

```text
Step4/Step5에서 확정한 최종 세그먼트 구조를,
classification 모델이 얼마나 잘 재현할 수 있는지 확인한다.
```

이 경우 Step6은 엄밀히 말해 "진짜 미래 고객에 대한 독립 검증"이라기보다, **final segmentation을 설명하고 재현하는 surrogate model**이다.

따라서 보고서에는 다음처럼 써야 한다.

```text
본 classification은 이탈 여부 예측이 아니라, 최종 clustering 기반 세그먼트 label을 행동 feature로 재현하는 보조 모델이다.
```

---

## 4. 어떤 경우에 leakage라고 볼 수 있는가?

아래처럼 하면 문제가 된다.

### 문제 1. `Attrition_Flag`를 feature로 사용

```python
X = df[["Activity_Score", ..., "Attrition_Flag"]]
y = df["Cluster"]
```

이건 피해야 한다.  
세그먼트 배정 모델은 신규 고객의 이탈 여부를 미리 알고 있다고 가정하면 안 된다.

### 문제 2. target과 같은 정보를 feature로 사용

아래 컬럼을 feature로 넣으면 안 된다.

```text
Cluster
Cluster_Label
Segment_Name
```

### 문제 3. Step6 성능을 “이탈 예측 성능”이라고 표현

이건 해석상 오류이다.

틀린 표현:

```text
Random Forest가 이탈 고객을 잘 예측했다.
```

맞는 표현:

```text
Random Forest가 final segment label을 잘 재현했다.
```

### 문제 4. 전체 데이터 clustering label 기반 평가를 “완전한 out-of-sample 검증”이라고 주장

전체 데이터로 clustering한 label은 test row의 feature도 cluster 중심점 학습에 영향을 주었을 수 있다.  
따라서 Step6의 train/test split 결과는 **세그먼트 재현 성능**으로는 쓸 수 있지만, "완전히 독립적인 미래 데이터 검증"이라고 과장하면 안 된다.

---

## 5. 추천 운영 방식: 현실적이고 안전한 방식

현재 프로젝트 상황에서는 아래 방식을 추천한다.

### 추천 방식 A: Final Segment Surrogate Classification

1. Step5 결과 파일을 읽는다.
2. `Cluster`를 target으로 둔다.
3. core_7 feature만 입력 feature로 사용한다.
4. train/test split을 한다.
5. Logistic Regression, Decision Tree, Random Forest를 학습한다.
6. Accuracy, Macro F1, Confusion Matrix를 출력한다.
7. 결과 해석 시 "세그먼트 label 재현 모델"이라고 명시한다.

장점:

- 지금까지 만든 final k=5 세그먼트와 완전히 연결된다.
- 다음 담당자가 수행하기 쉽다.
- 보고서에서 설명하기 좋다.
- mock data가 필요 없다.

주의점:

- 성능을 “이탈 예측 성능”이라고 쓰면 안 된다.
- 성능을 “완전한 신규 데이터 일반화 성능”이라고 과장하면 안 된다.

---

## 6. Step6 보고서에 넣을 권장 문장

아래 문장을 그대로 사용해도 된다.

```text
본 단계의 classification은 이탈 여부를 직접 예측하는 모델이 아니라, Step4와 Step5에서 도출한 최종 고객 세그먼트 label을 고객 행동 feature를 통해 재현하는 보조 모델이다. 따라서 target은 Attrition_Flag가 아니라 최종 cluster label이며, Attrition_Flag는 모델 입력 feature로 사용하지 않았다. 이 모델의 목적은 새로운 고객의 행동 정보가 주어졌을 때 어느 유지 전략 세그먼트에 배정될 수 있는지 확인하는 것이다.
```

추가로 data leakage 우려를 설명할 때는 다음 문장을 사용하면 된다.

```text
최종 clustering label은 전체 데이터 기반으로 도출되었으므로, Step6의 classification 성능은 완전한 미래 데이터 예측 성능이라기보다 final segmentation을 행동 feature로 얼마나 잘 재현하는지 보여주는 surrogate fidelity로 해석한다. 단, classification 학습 및 평가에서는 train/test split을 적용하고, Attrition_Flag와 segment label 관련 컬럼은 입력 feature에서 제외하였다.
```

---

## 7. 실무적 결론

현재 프로젝트에서는 다음 방식으로 진행하면 된다.

```text
실제 Step5 결과 파일 사용
mock data 사용하지 않음
Cluster를 target으로 사용
core_7 feature를 input으로 사용
Attrition_Flag는 input에서 제외
train/test split 적용
성능은 segment reproduction 성능으로 해석
```
