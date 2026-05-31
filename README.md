# BankChurners Customer Segmentation

BankChurners / Credit Card Customers 데이터를 사용해 카드 고객의 이용 행동 기반 세그먼트를 도출하고, 세그먼트별 이탈률과 행동 특성을 해석해 유지 전략을 제안하는 머신러닝 팀 프로젝트이다.

## 프로젝트 목적

이 프로젝트의 목적은 단순 churn prediction이 아니다. 핵심 목표는 고객의 거래 활동, 거래 감소, 비활성, 상품 관계, 접촉 부담, 신용 활용 행동을 기준으로 해석 가능한 고객 segment를 만들고, 각 segment에 맞는 retention strategy를 제안하는 것이다.

최종 clustering model은 `core_7_KMeans_k5`이다.

## 폴더 구조

```text
project_root/
├── config/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── analysis/
│       ├── clustering_results/
│       ├── clustering_visualizations/
│       ├── segment_profiling/
│       └── segment_classification/
├── docs/
├── notebooks/
├── outputs/
├── reports/
├── scripts/
└── src/
```

## 수동 파일 배치

Step 1부터 실행하려면 원본 CSV를 아래 경로 중 하나에 둔다.

```text
data/raw/머신러닝 데이터 자료(은행카드).csv
data/raw/BankChurners.csv
```

Step 1~3을 생략하고 Step 3.5부터 실행해야 할 때는 아래 파일을 직접 배치한다.

```text
data/interim/BankChurners_Final_Preprocessed.csv
```

## 공식 실행 순서

1. `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb`
2. `notebooks/03_5_further_preprocessing.ipynb`
3. `notebooks/04_clustering_model_selection.ipynb`
4. `notebooks/04_5_clustering_visualization.ipynb`
5. `notebooks/05_segment_profiling.ipynb`
6. `notebooks/06_classification_segment_prediction_and_07_feature_importance.ipynb`

## 단계별 입력과 출력

| 단계 | 역할 | 주요 입력 | 주요 출력 |
|---|---|---|---|
| Step 1 EDA | 원본 데이터 구조와 이탈 관련 행동 차이 확인 | `data/raw/*.csv` | 화면 출력 중심 |
| Step 2 Feature Engineering | 범주형 인코딩, log transform, 스케일링용 파생 변수 생성 | Step 1 데이터프레임 | 중간 전처리 데이터프레임 |
| Step 3 Preprocessing | Step 3.5가 사용할 전처리 CSV 저장 | Step 2 데이터프레임 | `data/interim/BankChurners_Final_Preprocessed.csv` |
| Step 3.5 Further Preprocessing | clustering input과 profiling table 분리, core behavior axes 생성 | `data/interim/BankChurners_Final_Preprocessed.csv` | `data/processed/BankChurners_cluster_input.csv`, `data/processed/BankChurners_profile_table.csv`, `data/processed/BankChurners_axis_features.csv` |
| Step 4 Clustering Model Selection | clustering 후보 비교와 최종 모델 선택 | `data/processed/` | `data/analysis/clustering_results/09_selected_model.json`, `13_final_customer_segments_core7_kmeans_k5.csv` |
| Step 4.5 Visualization | k=4,5,6 후보와 최종 k=5 진단 시각화 | Step 4 outputs | `data/analysis/clustering_visualizations/` |
| Step 5 Segment Profiling | segment별 행동 특성, 이탈률, 전략 해석 | Step 4 final labels, profile table | `data/analysis/segment_profiling/core_7_KMeans_k5/` |
| Step 6/7 Segment Classification | 최종 segment label 재현 모델과 feature importance 확인 | Step 5 final profile table | `data/analysis/segment_classification/core_7_KMeans_k5/` |

## core_7 행동 축

최종 모델은 아래 7개 행동 축을 사용한다.

| 행동 축 | 의미 |
|---|---|
| `Activity_Score` | 카드 이용 활성도 |
| `Count_Decline_Risk_Score` | 거래 횟수 감소 위험 |
| `Amount_Decline_Risk_Score` | 거래 금액 감소 위험 |
| `Inactivity_Score` | 최근 비활성 강도 |
| `Product_Relationship_Score` | 은행 상품 관계 수준 |
| `Contact_Burden_Score` | 고객 접촉 부담 또는 불만 가능성 |
| `Credit_Utilization_Score` | 신용한도 활용 수준 |

`Attrition_Flag`, 인구통계 변수, 카드 등급, 소득 구간 등 범주형 변수는 clustering input에 넣지 않고 segment profiling에서 사후 해석용으로 사용한다.

## Step 6/7 해석 주의

Step 6/7은 churn prediction이 아니다. Target은 `Attrition_Flag`가 아니라 최종 K-Means k=5 segment label인 `Cluster`이다.

따라서 Logistic Regression의 accuracy가 약 0.99로 높게 나와도 이는 이탈 예측 정확도가 아니다. 이 값은 core_7 행동 feature만으로 최종 `core_7_KMeans_k5` segment label을 얼마나 잘 재현하거나 신규 고객에게 배정할 수 있는지를 보여주는 surrogate fidelity로 해석한다.

Feature importance도 이탈 원인 중요도가 아니라 segment classification에서 어떤 행동 축이 세그먼트 구분에 많이 기여했는지를 의미한다.

## PPT 준비 전 주요 결과물 위치

```text
data/analysis/clustering_results/09_selected_model.json
data/analysis/clustering_visualizations/_final_selected_model_core7_kmeans_k5/
data/analysis/segment_profiling/core_7_KMeans_k5/10_segment_strategy_table_k5.csv
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv
data/analysis/segment_profiling/core_7_KMeans_k5/12_segment_final_summary_k5.csv
data/analysis/segment_classification/core_7_KMeans_k5/
```

## 생성 파일 Git 관리 원칙

`data/raw/`, `data/interim/`, `data/processed/`, `data/analysis/`, `outputs/`, `reports/`의 분석 산출물은 대부분 재생성 가능하므로 기본적으로 commit하지 않는다. 발표나 문서화에 필요한 산출물만 팀 합의 후 예외적으로 commit한다.

이미 Git에 추적된 생성 파일은 로컬 파일을 삭제하지 않고 추적만 해제한다. 아래 명령은 사용자가 직접 확인 후 실행한다.

```bash
git rm --cached -r data/raw
git rm --cached -r data/interim
git rm --cached -r data/processed
git rm --cached -r data/analysis
git rm --cached -r outputs
git rm --cached -r reports/figures
git rm --cached -r reports/tables
git add data/raw/.gitkeep data/interim/.gitkeep data/processed/.gitkeep data/analysis/.gitkeep reports/.gitkeep reports/figures/.gitkeep reports/tables/.gitkeep
```

## 문제 해결

| 문제 | 확인할 내용 |
|---|---|
| 원본 데이터 파일 없음 | `data/raw/머신러닝 데이터 자료(은행카드).csv` 또는 `data/raw/BankChurners.csv`가 있는지 확인 |
| 경로 오류 | 저장소 루트 또는 `notebooks/` 폴더에서 실행했는지 확인 |
| 패키지 오류 | `pip install -r requirements.txt` 실행, 특히 `xgboost`, `lightgbm` 설치 확인 |
| 한글 폰트 깨짐 | Windows는 `Malgun Gothic`, macOS는 `AppleGothic`, Linux는 `NanumGothic` 계열 폰트 확인 |

자세한 실행 절차는 `docs/RUNBOOK.md`를 참고한다.
