# BankChurners Customer Segmentation

본 프로젝트는 BankChurners 고객 데이터를 기반으로 카드 이용 행동 중심의 고객 세그먼트를 도출하고, 각 segment의 이탈률과 행동 특성을 분석하여 유지 전략을 제안하는 머신러닝 팀 프로젝트이다.

## 분석 흐름

```text
Step 3.5 Further Preprocessing
→ Step 4 Clustering Model Selection
→ Step 4.5 Clustering Visualization / Diagnostics
→ Step 5 Segment Profiling & Strategy
```

## 폴더 구조

```text
project_root/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── analysis/
│       ├── clustering_results/
│       ├── clustering_visualizations/
│       └── segment_profiling/
├── notebooks/
├── src/
├── docs/
├── reports/
└── outputs/
```

## 수동 배치 파일

| 파일 | 배치 경로 | 설명 |
|---|---|---|
| 팀원이 생성한 최종 전처리 CSV | `data/interim/BankChurners_Final_Preprocessed.csv` | Step 3.5의 필수 입력 파일 |
| 원본 CSV | `data/raw/머신러닝 데이터 자료(은행카드).csv` | 추적성과 설명을 위해 보관 권장 |
| 프로젝트 계획서 | `docs/프로젝트 계획서.pdf` | 분석 배경과 Step 정의 보관 |

## 실행 순서

```text
1. notebooks/03_5_further_preprocessing.ipynb
2. notebooks/04_clustering_model_selection.ipynb
3. notebooks/04_5_clustering_visualization.ipynb
4. notebooks/05_segment_profiling.ipynb
```

## Step 3.5 Further Preprocessing

역할은 Step 4/Step 5에서 사용할 최종 입력 데이터를 생성하는 것이다.

주요 작업:

- 범주형 label 복원
- `Avg_Open_To_Buy` 중복성 확인
- 행동 축 설계를 위한 핵심 상관관계 확인
- 변화율 변수 이상치 확인 및 1%~99% clipping
- profiling용 파생변수 생성
- high-risk signal 생성
- 행동 축 생성 및 표준화
- clustering input과 profiling table 분리 저장

핵심 행동 축:

```text
Activity_Score
Count_Decline_Risk_Score
Amount_Decline_Risk_Score
Inactivity_Score
Product_Relationship_Score
Contact_Burden_Score
Credit_Utilization_Score
```

비교 후보 축:

```text
Credit_Capacity_Score
```

## Step 4 Clustering Model Selection

역할은 여러 feature set, 알고리즘, cluster 수를 비교하여 최종 clustering 모델을 선택하는 것이다.

비교 feature set:

```text
core_7
core_7_plus_capacity
```

비교 알고리즘:

```text
K-Means
Gaussian Mixture Model
Agglomerative Clustering
```

비교 cluster 수:

```text
k = 4, 5, 6
```

평가 기준:

- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz score
- cluster size balance
- segment별 이탈률 차이
- segment별 high-risk signal 차이

## Step 4.5 Clustering Visualization / Diagnostics

역할은 선택된 clustering 결과를 보조적으로 시각화하는 것이다. UMAP은 사용하지 않는다.

시각화:

- cluster size summary
- 2D PCA scatter
- 3D PCA scatter
- 3D direct risk view
- 3D direct behavior view
- 3D LDA projection

## Step 5 Segment Profiling & Strategy

역할은 최종 cluster label을 바탕으로 segment별 특성을 해석하고 유지 전략을 제안하는 것이다.

주요 산출물:

- cluster profile heatmap
- segment별 이탈률 bar chart
- segment size vs attrition bubble chart
- high-risk signal summary
- categorical distribution table
- segment strategy table

## Feature 설명 문서

자세한 feature 의미, 파생변수 공식, 행동 축 정의 근거는 아래 문서에 정리되어 있다.

```text
docs/FEATURE_DESCRIPTION.md
```

## Git 관리 원칙

- `main` branch는 담당자가 직접 관리한다.
- 팀원이 전달한 파일은 담당자가 검토 후 반영한다.
- `data/processed/`, `data/analysis/` 결과물은 재생성 가능하므로 기본적으로 commit하지 않는다.
- 노트북과 문서 파일은 각 Step 단위로 commit한다.