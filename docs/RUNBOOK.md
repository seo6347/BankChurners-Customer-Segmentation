# 실행 안내서

이 문서는 프로젝트를 처음 받은 팀원이 같은 순서로 분석을 재생성하기 위한 실행 기준이다. PPT 제작자는 `docs/PPT_HANDOFF_GUIDE.md`와 Git에 포함된 PPT handoff 산출물을 함께 확인하면 된다.

## 1. 처음 받은 사람이 할 일

1. 저장소를 clone한다.
2. Python 가상환경을 만든다.
3. 패키지를 설치한다.
4. 원본 CSV를 `data/raw/`에 배치한다.
5. 노트북을 Step 1부터 Step 7까지 순서대로 실행한다.
6. 생성된 산출물이 아래 체크리스트 위치에 생겼는지 확인한다.

## 2. 필수 파일 배치

원본 BankChurners CSV는 아래 경로 중 하나에 둔다.

```text
data/raw/머신러닝 데이터 자료(은행카드).csv
data/raw/BankChurners.csv
```

Step 1~3을 생략하고 팀원이 만든 중간 전처리 파일부터 시작해야 하는 경우에는 아래 파일을 직접 배치한다.

```text
data/interim/BankChurners_Final_Preprocessed.csv
```

## 3. 패키지 설치

```bash
pip install -r requirements.txt
```

Step 6/7은 XGBoost와 LightGBM을 비교 모델에 포함하므로 `xgboost`, `lightgbm`이 필요하다.

## 4. 공식 실행 순서

1. `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb`
2. `notebooks/03_5_further_preprocessing.ipynb`
3. `notebooks/04_clustering_model_selection.ipynb`
4. `notebooks/04_5_clustering_visualization.ipynb`
5. `notebooks/05_segment_profiling.ipynb`
6. `notebooks/06_classification_segment_prediction_and_07_feature_importance.ipynb`

파일명은 Step 6/7이 하나의 노트북에 함께 들어 있어 6개지만, 분석 흐름은 Step 1부터 Step 7까지 이어진다.

## 5. 단계별 확인 파일

| 단계 | 확인할 주요 출력 |
|---|---|
| Step 1~3 | `data/interim/BankChurners_Final_Preprocessed.csv` |
| Step 3.5 | `data/processed/BankChurners_cluster_input.csv`, `data/processed/BankChurners_profile_table.csv`, `data/processed/BankChurners_axis_features.csv` |
| Step 4 | `data/analysis/clustering_results/09_selected_model.json`, `data/analysis/clustering_results/13_final_customer_segments_core7_kmeans_k5.csv` |
| Step 4.5 | `data/analysis/clustering_visualizations/_final_selected_model_core7_kmeans_k5/` |
| Step 5 | `data/analysis/segment_profiling/core_7_KMeans_k5/10_segment_strategy_table_k5.csv`, `data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv` |
| Step 6/7 | `data/analysis/segment_classification/core_7_KMeans_k5/01_classification_metrics_summary.csv` |

## 6. Git 추적 원칙

`data/raw/`, `data/interim/`, `data/processed/`, `data/analysis/`, `outputs/`, `reports/figures/`, `reports/tables/`의 생성 산출물은 대부분 재생성 가능하므로 일반적으로 commit하지 않는다. 문서화에 반드시 필요한 소수의 결과 파일만 팀 합의 후 commit한다.

현재 Git에 포함하는 예외 산출물은 PPT handoff용 결과물이다. 범위는 최종 모델 선정 요약, 최종 k=5 클러스터 시각화, Step 5 segment profiling 표/이미지/HTML, Step 6/7 segment assignment 보조 결과로 제한한다.

이미 추적된 생성 파일은 로컬 파일을 삭제하지 않고 Git 추적만 해제한다. 아래 명령은 사용자가 직접 확인 후 실행한다.

```bash
git rm --cached "data/raw/*.csv"
git rm --cached "data/interim/*.csv"
git rm --cached -r data/processed
git rm --cached -r data/analysis/clustering_results
git rm --cached "data/analysis/clustering_visualizations/*.csv"
git rm --cached -r data/analysis/clustering_visualizations/core_7_KMeans_k4
git rm --cached -r data/analysis/clustering_visualizations/core_7_KMeans_k5
git rm --cached -r data/analysis/clustering_visualizations/core_7_KMeans_k6
git rm --cached -r data/analysis/clustering_visualizations/_final_selected_model_core7_kmeans_k5
git rm --cached "data/analysis/segment_profiling/*.csv"
git rm --cached "data/analysis/segment_profiling/*.png"
git rm --cached "data/analysis/segment_profiling/*.html"
git rm --cached -r data/analysis/segment_profiling/core_7_KMeans_k5
git rm --cached -r data/analysis/segment_classification
git rm --cached -r outputs
git rm --cached -r reports/figures
git rm --cached -r reports/tables
```

폴더 자체를 남겨야 하면 `.gitkeep`은 다시 추가한다.

```bash
git add data/raw/.gitkeep data/interim/.gitkeep data/processed/.gitkeep data/analysis/.gitkeep reports/.gitkeep reports/figures/.gitkeep reports/tables/.gitkeep
```

## 7. PPT 제작 전 체크리스트

- 저장소를 받은 뒤 별도 실행 없이 아래 산출물 경로가 열리는지 확인한다.
- 최종 모델 metadata가 `core_7_KMeans_k5`인지 확인한다.
- Step 4.5 최종 시각화 폴더가 생성되었는지 확인한다.
- Step 5 segment strategy table과 profile table이 생성되었는지 확인한다.
- Step 6/7 결과가 `data/analysis/segment_classification/core_7_KMeans_k5/`에 저장되었는지 확인한다.
- Step 6/7 성능은 이탈 예측 정확도가 아니라 최종 세그먼트 label 재현 성능으로 해석한다.

## 8. 문제 해결

### 데이터 파일이 없을 때

Step 1~3은 `data/raw/머신러닝 데이터 자료(은행카드).csv` 또는 `data/raw/BankChurners.csv`를 찾는다. 파일명이 다르면 둘 중 하나로 맞추거나 노트북의 입력 후보 목록에 같은 의미의 파일명을 추가한다.

### 경로 문제가 날 때

노트북은 프로젝트 루트를 자동 탐색하도록 구성한다. 가능하면 저장소 루트 또는 `notebooks/` 폴더에서 실행한다.

### 패키지 문제가 날 때

`pip install -r requirements.txt`를 다시 실행한다. Step 6/7에서 `xgboost` 또는 `lightgbm` import 오류가 나면 해당 패키지가 설치되지 않은 것이다.

### 한글 폰트가 깨질 때

Windows는 보통 `Malgun Gothic`을 사용한다. macOS는 `AppleGothic`, Linux/Colab은 `NanumGothic` 계열 폰트를 설치하면 된다. 폰트가 없어도 분석 결과 파일 생성은 가능하지만 그래프의 한글 표시가 깨질 수 있다.
