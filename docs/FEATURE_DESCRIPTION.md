# Feature Description & Preprocessing Rationale

본 문서는 BankChurners 기반 고객 세그먼트 분석에서 사용하는 feature의 의미, 전처리 판단 기준, Step 3.5 Further Preprocessing에서 생성한 파생변수와 행동 축의 계산식을 정리한다.

본 프로젝트의 핵심 원칙은 다음과 같다.

- Clustering은 고객 행동 feature만 사용한다.
- `Attrition_Flag`는 clustering input에서 제외하고, segment별 이탈률을 사후 비교하는 profiling 변수로 사용한다.
- 인구통계 변수, 소득 구간, 카드 등급, Label Encoding된 범주형 변수는 clustering input에서 제외하고 profiling에 사용한다.
- 행동 축은 변수 의미와 간단한 데이터 검증 결과를 함께 고려하여 정의한다.
- 이상치 처리는 분포 확인 후 적용한다.
- 최종 clustering input과 profiling table을 분리하여 data leakage와 해석 오류를 방지한다.

---

## 1. 최초 CSV 기준 주요 feature 설명

### 1.1 제거 또는 clustering input 제외 feature

| Feature | 의미 | 처리 이유 |
|---|---|---|
| `CLIENTNUM` | 고객 고유 ID | 단순 식별자이므로 고객 행동이나 이탈 위험을 설명하지 않는다. 거리 기반 clustering에 포함하면 ID의 숫자 차이가 의미 없는 거리로 반영될 수 있다. |
| `Naive_Bayes_Classifier_..._1`, `Naive_Bayes_Classifier_..._2` | 원 데이터셋에 포함된 기존 모델 산출값 | 실제 고객 행동 feature가 아니라 기존 예측 모델의 결과물이다. 고객 행동 기반 segment 분석 목적과 맞지 않고 data leakage 위험이 있어 제외한다. |
| `Attrition_Flag` | 이탈 여부 | clustering input에서는 제외한다. 행동 기반으로 cluster를 만든 뒤 segment별 이탈률을 사후적으로 비교하는 데 사용한다. |
| `Gender`, `Education_Level`, `Marital_Status`, `Income_Category`, `Card_Category` | 성별, 교육 수준, 결혼 상태, 소득 구간, 카드 등급 | 고객 속성 및 범주형 변수이므로 clustering input에서 제외한다. segment profiling에서 분포를 해석하는 데 사용한다. |

---

## 2. 원본 feature 의미

### 2.1 고객 기본 정보

| Feature | 의미 | 사용 방식 |
|---|---|---|
| `Customer_Age` | 고객 나이 | profiling 변수 |
| `Gender` | 성별 | label 복원 후 profiling 변수 |
| `Dependent_count` | 부양가족 수 | profiling 변수 |
| `Education_Level` | 교육 수준 | label 복원 후 profiling 변수 |
| `Marital_Status` | 결혼 상태 | label 복원 후 profiling 변수 |
| `Income_Category` | 소득 구간 | label 복원 후 profiling 변수 |
| `Card_Category` | 카드 등급 | label 복원 후 profiling 변수 |

Label Encoding된 범주형 변수는 숫자처럼 보이지만 숫자 간 거리의 의미가 없다. 예를 들어 `Income_Category = 5`가 `Income_Category = 1`보다 수치적으로 4만큼 크다는 의미는 없다. 따라서 clustering input에서 제외한다.

### 2.2 카드사 관계 정보

| Feature | 의미 | 사용 방식 |
|---|---|---|
| `Months_on_book` | 고객 등록 기간 또는 카드사와의 관계 지속 기간 | profiling 변수 |
| `Total_Relationship_Count` | 고객이 은행에서 보유한 금융 상품 수 | `Product_Relationship_Score` 및 profiling 변수 |

`Total_Relationship_Count`는 고객이 구입한 물품 수가 아니라 은행/금융기관에서 보유한 금융 상품 수를 의미한다. 구체적인 상품 종류는 데이터셋에 제공되지 않으므로 특정 금융 상품 목록으로 단정하지 않는다.

### 2.3 비활성 및 접촉 신호

| Feature | 의미 | 사용 방식 |
|---|---|---|
| `Months_Inactive_12_mon` | 최근 12개월 중 비활성 개월 수 | `Inactivity_Score`, `Inactive_Ratio_12m`, `High_Inactive_Flag` |
| `Contacts_Count_12_mon` | 최근 12개월 고객 접촉 횟수 | `Contact_Burden_Score`, `Contact_Rate_12m`, `High_Contact_Flag` |

### 2.4 신용한도 및 이용 관련 feature

| Feature | 의미 | 사용 방식 |
|---|---|---|
| `Credit_Limit` | 고객 신용한도 | `Credit_Capacity_Score` 후보 축 |
| `Total_Revolving_Bal` | 회전 잔액 | `No_Revolving_Bal_Flag` 및 profiling 변수 |
| `Avg_Open_To_Buy` | 평균 가용 한도 | clustering input 제외 |
| `Avg_Utilization_Ratio` | 평균 한도 사용률 | `Credit_Utilization_Score`, `Zero_Utilization_Flag` |

`Avg_Open_To_Buy`는 데이터 정의상 가용 한도에 해당한다. 원본 CSV에서는 다음 관계를 확인한다.

```text
Avg_Open_To_Buy = Credit_Limit - Total_Revolving_Bal
```

Step 3.5 노트북에서는 `Credit_Limit - Total_Revolving_Bal - Avg_Open_To_Buy`의 최대 절대 오차를 계산하여 중복성을 확인한다. 이 관계가 사실상 0에 가까우므로 `Avg_Open_To_Buy`를 clustering input에 직접 포함하지 않는다.

### 2.5 거래 행동 및 변화율 feature

| Feature | 의미 | 사용 방식 |
|---|---|---|
| `Total_Trans_Amt` | 최근 12개월 총 거래 금액 | `Activity_Score`, `Avg_Ticket_Size` |
| `Total_Trans_Ct` | 최근 12개월 총 거래 횟수 | `Activity_Score`, `Avg_Ticket_Size` |
| `Total_Amt_Chng_Q4_Q1` | 최근 12개월 중 첫 번째 분기 대비 네 번째 분기의 거래 금액 변화율 | clipping 후 `Amount_Decline_Risk_Score` |
| `Total_Ct_Chng_Q4_Q1` | 최근 12개월 중 첫 번째 분기 대비 네 번째 분기의 거래 횟수 변화율 | clipping 후 `Count_Decline_Risk_Score` |

Q1과 Q4는 특정 연도의 1분기/4분기라기보다, 데이터에서 관측된 최근 12개월 기간을 네 구간으로 나누었을 때의 첫 번째 분기와 네 번째 분기로 해석한다. 실제 날짜 컬럼이 없으므로 특정 수집 연도나 월을 단정하지 않는다.

---

## 3. Label 복원 feature

| 생성 feature | 계산 방식 | 사용 목적 |
|---|---|---|
| `Attrition_Label` | `Attrition_Flag`를 `{0: Existing Customer, 1: Attrited Customer}`로 매핑 | segment별 이탈 고객 비율 해석 |
| `Gender_Label` | `Gender`를 `{0: F, 1: M}`으로 매핑 | segment별 성별 분포 |
| `Education_Label` | `Education_Level` 숫자값을 원래 교육 수준으로 매핑 | segment별 교육 수준 분포 |
| `Marital_Label` | `Marital_Status` 숫자값을 원래 결혼 상태로 매핑 | segment별 결혼 상태 분포 |
| `Income_Label` | `Income_Category` 숫자값을 원래 소득 구간으로 매핑 | segment별 소득 구간 분포 |
| `Card_Label` | `Card_Category` 숫자값을 원래 카드 등급으로 매핑 | segment별 카드 등급 분포 |

---

## 4. 변화율 clipping

거래 변화율 변수는 일부 극단값이 존재할 수 있으므로, Step 3.5에서 분포를 확인한다. 확인 항목은 `min`, `q01`, `median`, `q99`, `max`, IQR fence, IQR fence 밖의 row 수이다.

Clipping 공식은 다음과 같다.

```text
x_clip = min(max(x, Q_0.01(x)), Q_0.99(x))
```

| 생성 feature | 계산식 | 사용 목적 |
|---|---|---|
| `Total_Ct_Chng_Q4_Q1_clip` | `clip(Total_Ct_Chng_Q4_Q1, Q_0.01, Q_0.99)` | 거래 횟수 변화율 극단값 완화 |
| `Total_Amt_Chng_Q4_Q1_clip` | `clip(Total_Amt_Chng_Q4_Q1, Q_0.01, Q_0.99)` | 거래 금액 변화율 극단값 완화 |

---

## 5. Profiling용 파생변수

이 변수들은 clustering input이 아니라 segment profiling에 사용한다.

### 5.1 `Avg_Ticket_Size`

```text
Avg_Ticket_Size = Total_Trans_Amt / Total_Trans_Ct, if Total_Trans_Ct > 0
Avg_Ticket_Size = 0, if Total_Trans_Ct = 0
```

거래 1건당 평균 결제 금액을 나타낸다.

### 5.2 `Avg_Ticket_Size_log`

```text
Avg_Ticket_Size_log = log(1 + Avg_Ticket_Size)
```

건당 결제 금액의 오른쪽 꼬리 영향을 줄이기 위한 log 변환 변수이다.

### 5.3 `Inactive_Ratio_12m`

```text
Inactive_Ratio_12m = Months_Inactive_12_mon / 12
```

최근 12개월 중 비활성 상태였던 비율이다.

### 5.4 `Contact_Rate_12m`

```text
Contact_Rate_12m = Contacts_Count_12_mon / 12
```

최근 12개월 기준 월평균 접촉 빈도에 가까운 해석용 변수이다.

### 5.5 `No_Revolving_Bal_Flag`

```text
No_Revolving_Bal_Flag = 1 if Total_Revolving_Bal = 0 else 0
```

회전 잔액이 없는 고객 여부를 나타낸다.

### 5.6 `Low_Bank_Product_Count_Flag`

```text
Low_Bank_Product_Count_Flag = 1 if Total_Relationship_Count <= 2 else 0
```

은행 상품 보유 수가 낮은 고객을 나타낸다. Step 3.5에서 상품 수별 이탈률을 확인하여 이 기준의 해석 가능성을 점검한다.

### 5.7 `Zero_Utilization_Flag`

```text
Zero_Utilization_Flag = 1 if Avg_Utilization_Ratio = 0 else 0
```

한도 사용률이 0인 고객을 나타낸다.

---

## 6. High-risk signal feature

High-risk signal은 segment가 실제 고위험 행동 신호를 얼마나 포함하는지 사후 검증하기 위한 변수이다. Clustering input에는 사용하지 않는다.

### 6.1 개별 flag

```text
Low_Ct_Change = Total_Ct_Chng_Q4_Q1 <= Q_0.20(Total_Ct_Chng_Q4_Q1)
Low_Amt_Change = Total_Amt_Chng_Q4_Q1 <= Q_0.20(Total_Amt_Chng_Q4_Q1)
Low_Activity_Ct = Total_Trans_Ct <= Q_0.20(Total_Trans_Ct)
```

| 생성 feature | 계산식 | 의미 |
|---|---|---|
| `Strong_Decline_Flag` | `1 if Low_Ct_Change and Low_Amt_Change else 0` | 거래 횟수와 거래 금액 변화율이 모두 낮은 고객 |
| `Decline_Low_Activity_Flag` | `1 if Low_Ct_Change and Low_Activity_Ct else 0` | 거래 횟수 변화율이 낮고 현재 거래 활동도 낮은 고객 |
| `High_Inactive_Flag` | `1 if Months_Inactive_12_mon >= 4 else 0` | 최근 12개월 중 비활성 개월 수가 높은 고객 |
| `High_Contact_Flag` | `1 if Contacts_Count_12_mon >= 4 else 0` | 최근 12개월 접촉 횟수가 높은 고객 |
| `Low_Bank_Product_Count_Flag` | `1 if Total_Relationship_Count <= 2 else 0` | 은행 상품 보유 수가 낮은 고객 |
| `Zero_Utilization_Flag` | `1 if Avg_Utilization_Ratio = 0 else 0` | 한도 사용률이 0인 고객 |

### 6.2 `High_Risk_Signal_Count`

```text
High_Risk_Signal_Count
= Strong_Decline_Flag
+ Decline_Low_Activity_Flag
+ High_Inactive_Flag
+ High_Contact_Flag
+ Low_Bank_Product_Count_Flag
+ Zero_Utilization_Flag
```

이 값은 고객별 고위험 행동 신호의 중첩 수를 나타낸다.

---

## 7. Component-level standardization

서로 단위가 다른 component를 행동 축으로 만들기 전에 표준화한다.

```text
z_j = (x_j - mean(x_j)) / std(x_j)
```

사용 component는 다음과 같다.

| Component | 계산식 또는 원천 |
|---|---|
| `Total_Trans_Ct` | 원본 거래 횟수 |
| `Total_Trans_Amt_log` | `log(1 + Total_Trans_Amt)` |
| `Total_Ct_Chng_Q4_Q1_clip` | clipping된 거래 횟수 변화율 |
| `Total_Amt_Chng_Q4_Q1_clip` | clipping된 거래 금액 변화율 |
| `Months_Inactive_12_mon` | 원본 비활성 개월 수 |
| `Total_Relationship_Count` | 원본 은행 상품 보유 수 |
| `Contacts_Count_12_mon` | 원본 접촉 횟수 |
| `Avg_Utilization_Ratio` | 원본 평균 한도 사용률 |
| `Credit_Limit_log` | `log(1 + Credit_Limit)` |

---

## 8. Clustering용 행동 축 feature

### 8.1 `Activity_Score`

```text
Activity_Score_raw = (z_Total_Trans_Ct + z_Total_Trans_Amt_log) / 2
```

거래 횟수와 거래 금액은 카드 사용 활성도를 함께 설명한다. 두 변수는 의미가 유사하고 상관관계가 높기 때문에 하나의 활동성 축으로 통합한다.

### 8.2 `Count_Decline_Risk_Score`

```text
Count_Decline_Risk_Score_raw = -z_Total_Ct_Chng_Q4_Q1_clip
```

거래 횟수 변화율이 낮을수록 최근 거래 횟수가 감소한 것으로 해석한다. 부호를 반대로 바꾸어 값이 높을수록 감소 위험이 큰 축으로 정의한다.

### 8.3 `Amount_Decline_Risk_Score`

```text
Amount_Decline_Risk_Score_raw = -z_Total_Amt_Chng_Q4_Q1_clip
```

거래 금액 변화율이 낮을수록 최근 거래 금액이 감소한 것으로 해석한다. 거래 횟수 변화율과 거래 금액 변화율은 관련성이 있지만 완전히 같은 축으로 묶을 만큼 강한 상관은 아니므로 별도 축으로 둔다.

### 8.4 `Inactivity_Score`

```text
Inactivity_Score_raw = z_Months_Inactive_12_mon
```

최근 12개월 중 비활성 개월 수가 높은 고객을 나타낸다.

### 8.5 `Product_Relationship_Score`

```text
Product_Relationship_Score_raw = z_Total_Relationship_Count
```

고객이 은행에서 보유한 금융 상품 수를 나타낸다. 은행과의 관계 폭을 설명하는 축이다.

### 8.6 `Contact_Burden_Score`

```text
Contact_Burden_Score_raw = z_Contacts_Count_12_mon
```

최근 12개월 고객 접촉 횟수 기반의 접촉 부담 또는 불만 가능성 축이다.

### 8.7 `Credit_Utilization_Score`

```text
Credit_Utilization_Score_raw = z_Avg_Utilization_Ratio
```

고객이 실제로 한도를 얼마나 사용하고 있는지를 나타낸다.

### 8.8 `Credit_Capacity_Score`

```text
Credit_Capacity_Score_raw = z_Credit_Limit_log
```

신용한도 규모를 나타내는 후보 축이다. 고객 행동 중심 clustering에서는 핵심 7축에서 제외하고, Step 4에서 비교용 feature set에 포함한다.

---

## 9. Axis-level standardization

행동 축마다 분산이 다를 수 있으므로 최종 clustering input에서는 행동 축을 다시 표준화한다.

```text
A_k = (a_k - mean(a_k)) / std(a_k)
```

---

## 10. 최종 feature set

### 10.1 `core_7`

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Inactivity_Score
Product_Relationship_Score
Contact_Burden_Score
Credit_Utilization_Score
```

### 10.2 `core_7_plus_capacity`

```text
core_7
+ Credit_Capacity_Score
```

`Credit_Capacity_Score`는 고객 신용한도 규모를 나타내지만, 카드 이용 행동 자체보다는 고객 규모 또는 잠재 가치에 가까우므로 별도 후보 feature set에서 비교한다.

---

## 11. 최종 산출 파일

| 파일 | 역할 |
|---|---|
| `data/processed/BankChurners_cluster_input.csv` | Step 4 clustering 입력 데이터 |
| `data/processed/BankChurners_profile_table.csv` | Step 5 segment profiling 해석용 데이터 |
| `data/processed/BankChurners_axis_features_raw.csv` | axis-level standardization 전 행동 축 |
| `data/processed/BankChurners_component_features.csv` | 행동 축 생성 전 component feature |
| `data/processed/feature_design_evidence.csv` | 행동 축 설계 근거 요약 |
| `data/processed/change_rate_outlier_summary.csv` | 변화율 변수 이상치 검토 요약 |
| `data/processed/relationship_count_evidence.csv` | 관계 상품 수별 이탈률 검토 요약 |
| `data/processed/risk_signal_summary.csv` | high-risk signal flag 비율 및 이탈률 요약 |
| `data/processed/cluster_feature_info.json` | feature set 및 metadata |

---

## 12. 해석상 주의점

- 본 데이터는 정확한 수집 시작일과 종료일을 제공하지 않는다. 따라서 분석은 특정 연도에 대한 시계열 분석이 아니라 최근 12개월 행동 feature 기반의 횡단면적 고객 세그먼트 분석으로 해석한다.
- `Total_Relationship_Count`는 쇼핑 물품 수가 아니라 은행 상품 보유 수이다.
- `Attrition_Flag`는 행동 축 생성과 clustering input에 사용하지 않는다.
- High-risk signal은 cluster를 만드는 기준이 아니라, 도출된 segment의 위험 특성을 사후 검증하는 기준이다.