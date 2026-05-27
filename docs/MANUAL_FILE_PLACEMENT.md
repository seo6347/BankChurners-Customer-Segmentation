# Manual File Placement Guide

이 프로젝트는 폴더 구조를 자동으로 생성하지만, 원본/중간 데이터 파일은 사용자가 직접 배치해야 합니다.

## 반드시 배치해야 하는 파일

| 파일 | 배치 경로 | 필수 여부 | 설명 |
|---|---|---:|---|
| 팀원이 만든 최종 전처리 CSV | `data/interim/BankChurners_Final_Preprocessed.csv` | 필수 | Step 3.5의 입력 파일 |
| 원본 CSV | `data/raw/머신러닝 데이터 자료(은행카드).csv` | 권장 | 추적성과 재현성을 위해 보관 |
| 프로젝트 계획서 | `docs/프로젝트 계획서.pdf` | 권장 | 제출/설명용 참고 문서 |

## 실행 순서

1. `python folder_setup.py` 실행
2. 팀원이 만든 `BankChurners_Final_Preprocessed.csv`를 `data/interim/`에 넣기
3. 원본 CSV는 가능하면 `data/raw/`에 넣기
4. 이후 `notebooks/03_5_further_preprocessing.ipynb`부터 순서대로 실행

## 주의

- 후속 노트북은 절대경로를 사용하지 않고, 프로젝트 루트를 기준으로 상대경로를 사용합니다.
- CSV 저장은 한글 호환성을 위해 `utf-8-sig`를 사용합니다.
- Matplotlib 한글 깨짐 방지는 `src/common.py`의 `configure_korean_font()`를 사용합니다.
