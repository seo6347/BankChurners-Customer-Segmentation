# Step6 담당자를 위한 이전 단계 요약: Step3.5 ~ Step5

이 문서는 Step6 classification을 수행하기 전에, 이전 단계에서 무엇을 했는지 이해하기 위한 요약이다.

---

## 1. 프로젝트 전체 흐름

본 프로젝트의 핵심은 카드 고객을 행동 패턴에 따라 세그먼트화하고, 각 세그먼트별 이탈 위험과 유지 전략을 해석하는 것이다.

흐름은 다음과 같다.

```text
Step3.5 Feature Engineering
→ Step4 Clustering Model Selection
→ Step4.5 Visualization Diagnostics
→ Step5 Segment Profiling
→ Step6 Classification
```

---

## 2. Step3.5: Feature Engineering

Step3.5에서는 clustering에 사용할 고객 행동 feature를 만들었다.

Raw feature를 그대로 쓰지 않고, 고객 행동을 해석 가능한 축으로 요약했다.

최종 사용 feature set은 `core_7`이다.

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Inactivity_Score
Product_Relationship_Score
Contact_Burden_Score
Credit_Utilization_Score
```

이 feature들은 대부분 표준화된 값이다.  
따라서 값이 `1.13`, `-0.85`처럼 보일 수 있다.

해석 방법:

| 값 | 의미 |
|---:|---|
| 0 | 전체 평균 수준 |
| 양수 | 전체 평균보다 높음 |
| 음수 | 전체 평균보다 낮음 |
| +1 근처 | 평균보다 꽤 높음 |
| -1 근처 | 평균보다 꽤 낮음 |

예를 들어 `Count_Decline_Risk_Score = 1.0`이면 거래 횟수 감소 위험이 전체 평균보다 높은 고객이라고 볼 수 있다.

---

## 3. Step4: Clustering Model Selection

Step4에서는 고객을 여러 그룹으로 나누는 clustering을 수행했다.

비교한 핵심 후보는 다음이다.

```text
core_7_KMeans_k4
core_7_KMeans_k5
core_7_KMeans_k6
```

최종 선택 모델은 다음이다.

```text
core_7_KMeans_k5
```

### 왜 k=5를 선택했는가?

k=4는 해석은 쉽지만 고위험군과 저위험군의 세분화가 부족했다.  
k=6은 고위험군을 더 날카롭게 분리하지만, 군집이 많아져 해석이 복잡해졌다.  
k=5는 초고위험군, 초저위험군, 신용 활용군, 상품 관계군, 고활동·저관계군을 비교적 명확하게 구분하면서도 해석 가능성을 유지했다.

따라서 k=5를 최종 모델로 선택했다.

---

## 4. Step4.5: Visualization Diagnostics

Step4.5에서는 clustering 결과를 다양한 방식으로 시각화했다.

주요 시각화는 다음이다.

| 시각화 | 목적 |
|---|---|
| Cluster Size Ratio | 군집 크기가 너무 불균형하지 않은지 확인 |
| Cluster Profile Heatmap | 각 군집의 행동 feature 특성 확인 |
| Attrition Rate by Cluster | 군집별 실제 이탈률 확인 |
| High-risk Signal by Cluster | 위험 신호가 어느 군집에 집중되는지 확인 |
| PCA 2D/3D | 고차원 군집을 2D/3D로 참고 시각화 |
| LDA Projection | cluster label 차이를 강조한 참고 시각화 |

---

## 5. PCA와 LDA 해석 주의점

### PCA란?

PCA는 여러 개의 feature를 2개 또는 3개의 축으로 압축해서 보여주는 방법이다.  
고차원 데이터를 보기 쉽게 만드는 용도이다.

주의할 점:

> PCA에서 군집이 겹쳐 보인다고 해서 clustering이 무조건 나쁜 것은 아니다.

이유는 PCA 2D/3D가 전체 정보를 모두 담지 못하기 때문이다.  
현재 PCA 2D는 약 40%, PCA 3D는 약 54% 정도의 정보만 담고 있다.  
따라서 최종 해석은 PCA plot보다 cluster profile heatmap과 이탈률 차이를 중심으로 해야 한다.

### LDA란?

LDA는 이미 만들어진 cluster label을 사용해서, cluster 간 차이가 잘 보이도록 축을 만드는 방법이다.

주의할 점:

> LDA는 cluster label을 알고 있는 상태에서 그 차이를 잘 보이게 만든 시각화이다.  
> 따라서 LDA에서 잘 분리되어 보인다고 해서 자연적으로 완벽한 군집이 존재한다는 증거는 아니다.

즉, LDA는 발표용 참고 시각화로는 유용하지만, 최종 모델 선택의 핵심 근거로 쓰면 안 된다.

---

## 6. Step5: Segment Profiling

Step5에서는 최종 k=5 cluster에 이름과 해석을 부여했다.

최종 세그먼트는 다음과 같다.

| Cluster | Segment name | 해석 |
|---|---|---|
| C0 | 상품 관계 중심 저위험 안정군 | 상품 관계가 비교적 깊고 이탈률이 낮은 안정 고객 |
| C1 | 신용 활용 중심 저위험 금융활용군 | 신용 활용도가 높지만 이탈률은 낮은 고객 |
| C2 | 고활동·저관계 잠재 전환군 | 활동성은 높지만 상품 관계가 약한 고객 |
| C3 | 거래 감소·저활동·접촉 부담형 초고위험 이탈군 | 거래 감소와 접촉 부담이 동시에 큰 핵심 위험군 |
| C4 | 저활동·비감소형 초저위험 안정군 | 활동성은 낮지만 거래 감소 신호가 거의 없는 안정 고객 |

Step6에서는 이 세그먼트를 target으로 사용한다.

---

## 7. Step6에서 이전 결과를 어떻게 사용해야 하는가?

Step6에서는 Step5 결과 파일 중 다음 파일을 읽으면 된다.

```text
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv
```

이 파일에서:

```text
X = core_7 feature 7개
y = Cluster
```

로 두고 classification을 수행한다.

---

## 8. Step6에서 하면 안 되는 것

아래는 하지 않는다.

```text
Attrition_Flag를 target으로 두고 이탈 예측 모델 만들기
Attrition_Flag를 feature로 넣기
Cluster, Cluster_Label, Segment_Name을 feature로 넣기
Step4/Step5의 최종 선택 모델을 바꾸기
k=4 또는 k=6 기준으로 다시 classification하기
```

Step6은 반드시 최종 선택 모델인 `core_7_KMeans_k5` 기준으로 진행한다.
