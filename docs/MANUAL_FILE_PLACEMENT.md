# Manual File Placement Guide

이 프로젝트는 폴더 구조를 자동으로 생성하지만, 원본/중간 데이터 파일은 사용자가 직접 배치해야 합니다. 공식 재현 흐름은 Step 1~3에서 원본 CSV를 읽어 `data/interim/BankChurners_Final_Preprocessed.csv`를 생성한 뒤 Step 3.5 이후 분석으로 이어집니다.

## 반드시 배치해야 하는 파일

| 파일 | 배치 경로 | 필수 여부 | 설명 |
|---|---|---:|---|
| 원본 CSV | `data/raw/머신러닝 데이터 자료(은행카드).csv` 또는 `data/raw/BankChurners.csv` | 필수 | Step 1~3의 입력 파일 |
| 팀원이 만든 최종 전처리 CSV | `data/interim/BankChurners_Final_Preprocessed.csv` | 선택 | Step 1~3을 생략하고 Step 3.5부터 실행할 때 필요한 입력 파일 |
| 프로젝트 계획서 | `docs/프로젝트 계획서.pdf` | 권장 | 제출/설명용 참고 문서 |

## 실행 순서

1. `python folder_setup.py` 실행
2. 원본 CSV를 `data/raw/`에 넣기
3. `notebooks/01_EDA_and_02_feature_engineering_and_03_preproessing.ipynb`부터 순서대로 실행
4. Step 1~3을 생략할 경우에만 `BankChurners_Final_Preprocessed.csv`를 `data/interim/`에 넣고 Step 3.5부터 실행

## 주의

- 후속 노트북은 절대경로를 사용하지 않고, 프로젝트 루트를 기준으로 상대경로를 사용합니다.
- CSV 저장은 한글 호환성을 위해 `utf-8-sig`를 사용합니다.
- Matplotlib 한글 깨짐 방지는 `src/common.py`의 `configure_korean_font()`를 사용합니다.
