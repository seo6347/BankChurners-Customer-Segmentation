# Notebook Markdown Blocks

아래 내용은 각 노트북 맨 앞 또는 주요 코드 셀 앞에 Markdown 셀로 삽입하기 위한 설명문입니다.

---

## 03_5_further_preprocessing.ipynb

```markdown
# Step 3.5. Further Preprocessing

이 노트북은 팀원이 Step 3까지 수행한 전처리 결과물인 `BankChurners_Final_Preprocessed.csv`를 기반으로, 이후 Step 4 Clustering과 Step 5 Segment Profiling에 사용할 최종 분석용 데이터를 생성한다.

본 단계의 핵심은 다음 두 데이터를 명확히 분리하는 것이다.

1. `BankChurners_cluster_input.csv`  
   - clustering 알고리즘에 직접 입력되는 행동 축 기반 feature matrix
   - `Attrition_Flag`, 인구통계 변수, label-encoded 범주형 변수는 포함하지 않음

2. `BankChurners_profile_table.csv`  
   - clustering 이후 segment 해석에 사용하는 profiling table
   - 이탈 여부, 범주형 label, 원본 행동 변수, high-risk signal 등을 포함

이렇게 분리하는 이유는 고객군을 이탈 여부나 인구통계 정보가 아니라 실제 카드 이용 행동 중심으로 나누기 위함이다.
```

```markdown
## 1. Data Loading and Validation

팀원이 생성한 Step 3 결과 파일을 불러오고, 이후 분석에 필요한 필수 컬럼이 존재하는지 확인한다. 결측치와 중복 row도 함께 점검하여 Step 4/5에서 발생할 수 있는 오류를 사전에 방지한다.
```

```markdown
## 2. Label Restoration for Profiling

팀원 전처리 과정에서 범주형 변수는 숫자로 인코딩되었다. 그러나 segment profiling 단계에서는 사람이 해석 가능한 범주명이 필요하므로, `Gender_Label`, `Income_Label`, `Card_Label` 등의 label 컬럼을 복원한다.

이 label 컬럼들은 clustering input에는 사용하지 않고, cluster 생성 후 segment 특성을 해석하는 데만 사용한다.
```

```markdown
## 3. Clipping for Change-rate Variables

거래 횟수 변화율과 거래 금액 변화율은 일부 극단값이 존재할 수 있다. 거리 기반 clustering에서는 극단값이 cluster 중심을 과도하게 움직일 수 있으므로, 1%~99% 범위로 clipping하여 영향력을 완화한다.

이는 고객을 삭제하는 처리가 아니라, 극단적인 변화율 값의 영향만 줄이는 winsorization 방식이다.
```

```markdown
## 4. Profiling Features and High-risk Signals

이 단계에서는 segment 해석을 위한 파생변수와 high-risk signal을 생성한다. 예를 들어 평균 결제 금액, 비활성 비율, 접촉 비율, 회전잔액 없음 여부, 관계 상품 수 부족 여부 등을 생성한다.

`High_Risk_Signal_Count`는 cluster 생성 기준이 아니라, cluster 생성 후 해당 segment가 실제 고위험 행동 신호를 많이 포함하는지 검증하기 위한 사후 해석 변수이다.
```

```markdown
## 5. Behavior Axis Construction

원본 변수들을 그대로 clustering에 넣지 않고, 해석 가능한 고객 행동 축으로 통합한다.

사용한 행동 축은 다음과 같다.

- `Activity_Score`: 거래 횟수와 거래 금액을 통합한 카드 사용 활성도
- `Decline_Risk_Score`: 최근 거래 횟수 및 금액 감소 위험
- `Inactivity_Score`: 최근 12개월 중 비활성 개월 수 기반 비활성 신호
- `Relationship_Strength_Score`: 카드 이용 기간과 관계 상품 수 기반 관계 강도
- `Contact_Burden_Score`: 고객 접촉 횟수 기반 접촉 부담 또는 불만 가능성
- `Credit_Capacity_Score`: 신용한도 규모
- `Credit_Utilization_Score`: 평균 한도 사용률

서로 단위가 다른 원변수를 하나의 축으로 합치기 위해 component-level standardization을 먼저 수행하고, 생성된 행동 축들이 clustering에서 동일한 영향력을 갖도록 axis-level standardization을 추가로 수행한다.
```

```markdown
## 6. Save Processed Data

최종적으로 Step 4에서 사용할 clustering input과 Step 5에서 사용할 profiling table을 별도 파일로 저장한다. 두 파일은 동일한 `Row_ID`를 공유하므로, 이후 cluster label을 안정적으로 연결할 수 있다.
```

---

## 04_clustering_model_selection.ipynb

```markdown
# Step 4. Clustering Model Selection

이 노트북은 Step 3.5에서 생성한 행동 축 기반 clustering input을 사용하여 여러 clustering 후보를 비교하고, 최종 segment model을 선택한다.

본 프로젝트의 clustering은 이탈 여부를 직접 예측하는 것이 아니라, 고객의 이용 행동 패턴을 기준으로 전략적으로 해석 가능한 고객군을 도출하는 것이 목적이다. 따라서 `Attrition_Flag`는 clustering input에 포함하지 않고, cluster 생성 후 segment별 이탈률을 비교하는 사후 검증 지표로만 사용한다.
```

```markdown
## 1. Feature Sets

세 가지 feature set을 비교한다.

1. `axis_7`: Step 3.5에서 생성한 7개 행동 축 전체 사용
2. `axis_6_without_capacity`: 신용한도 규모를 제외하고 실제 이용 행동 중심 6개 축 사용
3. `weighted_axis_7`: 거래 감소, 활동성, 비활성 신호 등 유지 전략과 직접 연결되는 축에 약한 가중치 부여

최종 모델은 내부 군집 지표뿐 아니라 segment 해석 가능성과 전략 연결성을 함께 고려하여 선택한다.
```

```markdown
## 2. Candidate Algorithms

다음 clustering 알고리즘을 비교한다.

- K-Means: 단순하고 해석이 쉬운 baseline clustering
- Gaussian Mixture Model: cluster 소속 확률을 제공하는 soft clustering
- Agglomerative Clustering: 계층적 구조를 확인할 수 있는 clustering

cluster 수는 계획서에 맞추어 k=4, 5, 6 범위에서 비교한다.
```

```markdown
## 3. Evaluation Criteria

clustering 결과는 silhouette score만으로 선택하지 않는다. 본 분석에서는 다음 기준을 종합적으로 고려한다.

- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz score
- cluster size balance
- segment별 이탈률 차이
- segment별 high-risk signal 차이
- segment profile 해석 가능성
- 카드사 유지 전략과의 연결 가능성

고객 데이터는 자연스럽게 둥근 군집으로 분리되기보다 연속적인 행동 스펙트럼을 가질 수 있으므로, 내부 지표와 비즈니스 해석 가능성을 함께 평가한다.
```

```markdown
## 4. Selected Model

최종 선택 모델은 `axis_6_without_capacity_KMeans_k6`이다.

이 모델은 신용한도 규모보다 실제 이용 행동에 집중하여 고객군을 나누며, cluster size balance, segment별 이탈률 차이, high-risk signal 차이, 해석 가능성 측면에서 가장 균형적인 결과를 보였다.
```

---

## 04_5_clustering_visualization.ipynb

```markdown
# Step 4.5. Clustering Visualization / Diagnostics

이 노트북은 Step 4에서 선택한 최종 clustering 결과를 시각적으로 점검하는 단계이다. 이 단계의 목적은 최종 segment 해석이 아니라, 선택된 cluster label이 feature space에서 어떤 구조를 보이는지 확인하는 것이다.

최종 segment 이름, 이탈률 해석, 유지 전략 제안은 Step 5 Segment Profiling에서 수행한다.
```

```markdown
## 1. Visualization Scope

본 노트북에서는 UMAP을 제외하고 다음 시각화만 사용한다.

- Cluster size summary
- 2D PCA scatter
- 3D PCA scatter
- 3D Direct Risk View
- 3D Direct Behavior View
- 3D LDA Projection

UMAP은 고객 행동 데이터가 뚜렷한 blob 구조로 나타나지 않고 연속적 분포를 보여 최종 발표용 시각화에서 제외하였다.
```

```markdown
## 2. PCA Visualization

PCA는 고차원 행동 축을 선형 결합하여 2D 또는 3D 공간에 투영하는 방법이다. PCA scatter는 cluster가 전체 feature space에서 어떤 방향으로 배치되는지 확인하는 보조 시각화이다.

단, PCA 축 자체는 `Activity_Score`나 `Decline_Risk_Score`처럼 직접 해석 가능한 변수가 아니므로, 최종 segment 해석의 핵심 근거로 사용하지 않는다.
```

```markdown
## 3. Direct 3D Feature View

직접 해석 가능한 행동 축을 사용해 3D 시각화를 수행한다.

- Risk View: `Activity_Score × Decline_Risk_Score × Inactivity_Score`
- Behavior View: `Activity_Score × Contact_Burden_Score × Credit_Utilization_Score`

이 시각화는 각 segment가 어떤 행동 축에서 차이를 보이는지 직관적으로 설명하는 데 사용한다.
```

```markdown
## 4. LDA Projection

LDA projection은 이미 도출된 cluster label을 기준으로 segment 간 차이가 잘 보이도록 투영하는 supervised visualization이다.

따라서 LDA 결과는 자연 군집이 완벽하게 분리되어 있다는 증거가 아니라, K-Means로 도출된 segment 간 차이를 강조해서 보여주는 보조 시각화로 해석해야 한다.
```

---

## 05_segment_profiling.ipynb

```markdown
# Step 5. Segment Profiling & Strategy

이 노트북은 Step 4에서 선택한 최종 cluster label을 바탕으로 segment별 행동 특성, 이탈률, 위험 신호, 고객 특성을 해석하고, 각 segment에 적합한 유지·재활성화 전략을 제안한다.

이 단계에서는 clustering을 다시 수행하지 않는다. 이미 선택된 cluster label을 profile table에 결합한 뒤, 각 cluster를 전략적으로 해석 가능한 segment로 명명한다.
```

```markdown
## 1. Segment Profiling Summary

각 segment별로 고객 수, 고객 비율, 이탈률, 평균 거래 횟수, 평균 거래 금액, 비활성 개월 수, 접촉 횟수, 관계 상품 수, 한도 사용률, high-risk signal 평균을 계산한다.

이 표는 최종 segment 해석과 전략 제안의 기본 자료로 사용된다.
```

```markdown
## 2. Cluster Profile Heatmap

Cluster profile heatmap은 segment별 행동 축 평균을 시각화한다. 각 segment가 활동성, 거래 감소 위험, 비활성 신호, 관계 강도, 접촉 부담, 한도 사용률 중 어떤 축에서 높은지 또는 낮은지를 한눈에 보여준다.

본 프로젝트에서는 scatter plot의 시각적 분리보다 이 heatmap을 segment 해석의 핵심 근거로 사용한다.
```

```markdown
## 3. Attrition Rate and High-risk Signal

`Attrition_Flag`는 clustering input으로 사용하지 않았기 때문에, segment별 이탈률은 사후 검증 지표로 의미가 있다.

행동 기반으로 만든 segment가 실제 이탈률과 high-risk signal에서 차이를 보인다면, 해당 segment는 카드사 유지 전략 수립에 활용 가능한 고객군으로 해석할 수 있다.
```

```markdown
## 4. Segment Naming and Strategy

각 cluster의 행동 특성과 이탈률을 바탕으로 segment 이름을 부여한다. 예를 들어 활동성이 높고 이탈률이 낮은 cluster는 고활성 핵심 고객으로, 거래 감소 위험과 접촉 부담이 높은 cluster는 거래감소 고위험 고객으로 해석할 수 있다.

최종적으로 각 segment별 위험 수준과 전략 우선순위를 부여하고, 카드사 관점의 유지·재활성화 전략을 제안한다.
```
