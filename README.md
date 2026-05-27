# BankChurners Customer Segmentation Project

## 프로젝트 목적

신용카드 고객의 이용 행동 데이터를 기반으로 고객 세그먼트를 도출하고, 각 세그먼트의 이탈률과 행동 특성을 비교하여 카드사 관점의 유지·재활성화 전략을 제안한다.

## 표준 폴더 구조

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
├── config/
├── docs/
├── reports/
└── outputs/
```

## 단계별 역할

| 단계 | 노트북 | 목적 |
|---|---|---|
| Step 3.5 | `03_5_further_preprocessing.ipynb` | 팀원 Step3 결과를 clustering/profiling용 데이터로 재구성 |
| Step 4 | `04_clustering_model_selection.ipynb` | 여러 clustering 후보 비교 및 최종 모델 선택 |
| Step 4.5 | `04_5_clustering_visualization.ipynb` | 선택된 clustering 결과의 구조를 보조 시각화 |
| Step 5 | `05_segment_profiling.ipynb` | 세그먼트별 행동 특성, 이탈률, 위험 신호, 전략 해석 |

## 필수 입력 파일

`data/interim/BankChurners_Final_Preprocessed.csv`

이 파일은 팀원이 Step3 전처리까지 완료한 최종 CSV이다.

## 실행 순서

1. `python folder_setup.py`
2. `data/interim/BankChurners_Final_Preprocessed.csv` 배치
3. Step 3.5 노트북 실행
4. Step 4 노트북 실행
5. Step 4.5 노트북 실행
6. Step 5 노트북 실행
