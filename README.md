# BankChurners Customer Segmentation

신용카드 고객의 이용 행동 데이터를 기반으로 고객 세그먼트를 도출하고, 각 세그먼트의 이탈 위험과 유지 전략을 분석하는 머신러닝 팀 프로젝트입니다.

본 프로젝트의 핵심은 단순히 `Attrition_Flag`를 예측하는 것이 아니라, 고객의 거래 활동성, 거래 감소 신호, 비활성 상태, 관계 강도, 접촉 부담, 한도 사용률 등을 바탕으로 **행동 기반 고객 세그먼트**를 만들고, 각 세그먼트별 이탈률과 전략적 의미를 해석하는 것입니다.

---

## 1. 프로젝트 목표

본 분석은 다음 질문에 답하는 것을 목표로 합니다.

> 카드 고객은 어떤 이용 행동 패턴에 따라 세그먼트화되며, 각 세그먼트에는 어떤 유지·재활성화 전략이 필요한가?

세부 목표는 다음과 같습니다.

1. 신용카드 고객의 이용 행동과 관계 강도에 따라 고객군을 도출한다.
2. 각 고객군의 이탈률, 거래 행동, 비활성 수준, 접촉 빈도, 관계 상품 수를 비교한다.
3. 고객 세그먼트를 해석 가능한 전략 단위로 명명한다.
4. 세그먼트별 유지, 재활성화, 리스크 관리 전략을 제안한다.

---

## 2. 프로젝트 폴더 구조

```text
project_root/
├── data/
│   ├── raw/
│   │   └── 머신러닝 데이터 자료(은행카드).csv
│   ├── interim/
│   │   └── BankChurners_Final_Preprocessed.csv
│   ├── processed/
│   │   ├── BankChurners_cluster_input.csv
│   │   ├── BankChurners_profile_table.csv
│   │   ├── BankChurners_axis_features.csv
│   │   ├── BankChurners_component_features.csv
│   │   ├── cluster_feature_info.json
│   │   ├── preprocessing_thresholds.json
│   │   └── preprocessing_validation_summary.csv
│   └── analysis/
│       ├── clustering_results/
│       ├── clustering_visualizations/
│       └── segment_profiling/
├── notebooks/
│   ├── 03_5_further_preprocessing.ipynb
│   ├── 04_clustering_model_selection.ipynb
│   ├── 04_5_clustering_visualization.ipynb
│   └── 05_segment_profiling.ipynb
├── src/
│   └── common.py
├── config/
│   └── project_config.json
├── docs/
├── reports/
├── outputs/
├── requirements.txt
└── README.md
```

---

## 3. 데이터 파일 배치

분석을 실행하기 전에 아래 파일을 배치해야 합니다.

| 파일 | 경로 | 필수 여부 | 설명 |
|---|---|---:|---|
| 팀원이 생성한 최종 전처리 CSV | `data/interim/BankChurners_Final_Preprocessed.csv` | 필수 | Step 3까지 완료된 중간 데이터 |
| 원본 CSV | `data/raw/머신러닝 데이터 자료(은행카드).csv` | 권장 | 원본 추적성과 재현성을 위한 보관 파일 |
| 프로젝트 계획서 | `docs/프로젝트 계획서.pdf` | 권장 | 프로젝트 배경과 분석 계획 참고 문서 |

Step 3.5 이후부터는 `data/interim/BankChurners_Final_Preprocessed.csv`를 입력으로 사용합니다.

---

## 4. 실행 환경

Python 3.10 이상을 권장합니다.

필요 패키지는 다음 명령으로 설치할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

VS Code에서 노트북을 실행할 경우, 패키지를 설치한 Python 환경과 노트북 커널이 동일한지 확인해야 합니다.

---

## 5. 실행 순서

분석은 아래 순서로 실행합니다.

```text
Step 3.5  Further Preprocessing
Step 4    Clustering Model Selection
Step 4.5  Clustering Visualization / Diagnostics
Step 5    Segment Profiling & Strategy
```

### Step 3.5. Further Preprocessing

노트북:

```text
notebooks/03_5_further_preprocessing.ipynb
```

목적:

- 팀원이 만든 Step 3 결과 파일을 Step 4/5에 맞게 재구성한다.
- clustering input과 profiling table을 분리한다.
- 해석 가능한 고객 행동 축을 생성한다.

주요 출력:

```text
data/processed/BankChurners_cluster_input.csv
data/processed/BankChurners_profile_table.csv
data/processed/BankChurners_axis_features.csv
data/processed/cluster_feature_info.json
```

### Step 4. Clustering Model Selection

노트북:

```text
notebooks/04_clustering_model_selection.ipynb
```

목적:

- 여러 clustering 알고리즘과 cluster 수를 비교한다.
- 내부 군집 지표와 사후 해석 지표를 함께 평가한다.
- 최종 clustering model을 선택한다.

비교 대상:

- K-Means
- Gaussian Mixture Model
- Agglomerative Clustering
- k = 4, 5, 6
- feature set: `axis_7`, `axis_6_without_capacity`, `weighted_axis_7`

주요 출력:

```text
data/analysis/clustering_results/09_selected_model.json
data/analysis/clustering_results/10_selected_cluster_labels.csv
data/analysis/clustering_results/11_df_cluster_input_used.csv
data/analysis/clustering_results/12_df_profile_table_used.csv
```

### Step 4.5. Clustering Visualization / Diagnostics

노트북:

```text
notebooks/04_5_clustering_visualization.ipynb
```

목적:

- Step 4에서 선택된 cluster label을 기반으로 cluster 구조를 시각적으로 점검한다.
- 이 단계는 최종 segment 해석이 아니라, clustering 결과의 보조 진단을 담당한다.

주요 시각화:

- cluster size summary
- 2D PCA scatter
- 3D PCA scatter
- 3D direct risk view: `Activity × Decline Risk × Inactivity`
- 3D direct behavior view: `Activity × Contact Burden × Credit Utilization`
- 3D LDA projection

주요 출력:

```text
data/analysis/clustering_visualizations/
```

### Step 5. Segment Profiling & Strategy

노트북:

```text
notebooks/05_segment_profiling.ipynb
```

목적:

- 최종 cluster label을 바탕으로 segment별 특성을 해석한다.
- cluster별 이탈률, 위험 신호, 고객 규모, 범주형 분포를 비교한다.
- segment 이름과 유지 전략을 제안한다.

주요 출력:

```text
data/analysis/segment_profiling/final_segment_profiling_table.csv
data/analysis/segment_profiling/segment_strategy_table.csv
data/analysis/segment_profiling/01_cluster_profile_heatmap.png
data/analysis/segment_profiling/02_attrition_rate_by_segment.png
data/analysis/segment_profiling/03_segment_size_vs_attrition_bubble.html
```

---

## 6. Feature 설계 원칙

본 프로젝트에서는 clustering input과 profiling feature를 명확히 분리합니다.

### Clustering input

고객을 나누는 데 사용하는 변수입니다. 이탈 여부와 인구통계 변수는 포함하지 않습니다.

```text
Activity_Score
Decline_Risk_Score
Inactivity_Score
Relationship_Strength_Score
Contact_Burden_Score
Credit_Capacity_Score
Credit_Utilization_Score
```

최종 선택 모델에서는 `Credit_Capacity_Score`를 제외한 6개 행동 축을 사용합니다.

### Profiling table

cluster 생성 후 해석을 위해 사용하는 변수입니다.

예시:

```text
Attrition_Flag
Attrition_Label
Gender_Label
Income_Label
Card_Label
Total_Trans_Ct
Total_Trans_Amt
Months_Inactive_12_mon
Contacts_Count_12_mon
High_Risk_Signal_Count
```

`Attrition_Flag`는 clustering input에는 넣지 않고, cluster 생성 후 이탈률 비교에만 사용합니다.

---

## 7. 최종 모델 선택 기준

최종 모델은 단순히 silhouette score만으로 선택하지 않습니다.

함께 고려한 기준은 다음과 같습니다.

1. Silhouette score
2. Davies-Bouldin index
3. Calinski-Harabasz score
4. cluster size balance
5. segment별 이탈률 차이
6. segment별 high-risk signal 차이
7. segment profile 해석 가능성
8. 카드사 유지 전략과의 연결 가능성

현재 분석에서는 다음 모델을 기본 최종 모델로 사용합니다.

```text
axis_6_without_capacity_KMeans_k6
```

이 모델은 신용한도 규모보다 실제 고객 이용 행동에 집중하여 segment를 도출하므로, 이후 segment profiling과 전략 제안에 적합합니다.

---

## 8. Git 관리 원칙

본 프로젝트에서는 main branch를 관리자가 직접 관리합니다.

권장 원칙:

- 팀원이 공유한 파일은 관리자가 검토 후 repo에 반영한다.
- `data/processed/`, `data/analysis/`, `outputs/`는 재생성 가능한 산출물이므로 기본적으로 commit하지 않는다.
- 노트북, README, 설정 파일, 공통 함수는 commit한다.
- 데이터 CSV를 repo에 포함할지는 제출 방식과 용량을 고려해 결정한다.

기본 commit 예시:

```bash
git add notebooks/03_5_further_preprocessing.ipynb
git commit -m "Add step 3.5 further preprocessing notebook"
git push
```

---

## 9. 한글 폰트 설정

Matplotlib 시각화에서 한글이 깨지지 않도록 `src/common.py`의 `configure_korean_font()`를 사용합니다.

Windows 환경에서는 일반적으로 `Malgun Gothic`이 자동으로 사용됩니다.

```python
from src.common import configure_korean_font
configure_korean_font()
```

Plotly HTML 시각화는 브라우저 렌더링 환경의 폰트를 사용하므로, `Malgun Gothic`, `Apple SD Gothic Neo`, `Noto Sans CJK KR` 계열 폰트를 layout에 지정합니다.

---

## 10. 주의사항

- UMAP은 최종 시각화에서 제외했습니다. 고객 행동 데이터가 자연적으로 둥근 blob 형태로 분리되지 않고 연속적인 스펙트럼 구조를 보였기 때문입니다.
- PCA와 LDA 시각화는 보조 진단용입니다.
- 최종 해석은 scatter plot의 시각적 분리보다 cluster profile heatmap, segment별 이탈률, high-risk signal 차이를 중심으로 수행합니다.
- LDA projection은 cluster label을 알고 있는 상태에서 차이를 강조하는 supervised visualization이므로, 자연 군집의 증거로 해석하지 않습니다.

---

## 11. 최종 산출물 요약

최종 보고서에 사용할 핵심 산출물은 다음입니다.

```text
Cluster Profile Heatmap
Segment별 이탈률 Bar Chart
Segment Size vs Attrition Rate Bubble Chart
Final Segment Profiling Table
Segment Strategy Table
```

이 산출물을 바탕으로 고객군별 유지 전략을 제안합니다.
