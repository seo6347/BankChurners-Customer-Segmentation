#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BankChurners 고객 세그먼트 분석 프로젝트 폴더 구조 초기화 스크립트.

권장 실행:
    python folder_setup.py
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime


COMMON_PY_CONTENT = 'from __future__ import annotations\n\nfrom pathlib import Path\nimport json\nimport pandas as pd\nimport matplotlib.pyplot as plt\nfrom matplotlib import font_manager\n\n\nCSV_ENCODING_CANDIDATES = ("utf-8-sig", "utf-8", "cp949", "euc-kr")\n\nKOREAN_FONT_CANDIDATES = (\n    "Malgun Gothic",      # Windows\n    "AppleGothic",       # macOS\n    "NanumGothic",       # Linux / Colab\n    "Noto Sans CJK KR",\n    "Noto Sans KR",\n)\n\n\ndef get_project_root() -> Path:\n    """\n    현재 작업 위치가 project root이든 notebooks 폴더이든,\n    data 폴더와 src 폴더를 기준으로 project root를 찾는다.\n    """\n    current = Path.cwd().resolve()\n    candidates = [current] + list(current.parents)\n\n    for path in candidates:\n        if (path / "data").exists() and (path / "src").exists():\n            return path\n\n    return current\n\n\ndef read_csv_safely(path, **kwargs) -> pd.DataFrame:\n    """\n    UTF-8/CP949/EUC-KR 인코딩 이슈를 피하기 위한 CSV 로더.\n    """\n    path = Path(path)\n    last_error = None\n\n    for encoding in CSV_ENCODING_CANDIDATES:\n        try:\n            return pd.read_csv(path, encoding=encoding, **kwargs)\n        except UnicodeDecodeError as exc:\n            last_error = exc\n\n    raise last_error\n\n\ndef configure_korean_font(verbose: bool = True):\n    """\n    Matplotlib에서 한글이 깨지지 않도록 사용 가능한 한글 폰트를 설정한다.\n    Windows에서는 보통 Malgun Gothic이 사용된다.\n    """\n    installed_fonts = {font.name for font in font_manager.fontManager.ttflist}\n\n    selected_font = next(\n        (font for font in KOREAN_FONT_CANDIDATES if font in installed_fonts),\n        None\n    )\n\n    if selected_font is None:\n        if verbose:\n            print("[warning] 설치된 한글 폰트를 찾지 못했습니다.")\n            print("Windows: Malgun Gothic, macOS: AppleGothic, Linux: NanumGothic 설치를 확인하세요.")\n        plt.rcParams["axes.unicode_minus"] = False\n        return None\n\n    plt.rcParams["font.family"] = selected_font\n    plt.rcParams["axes.unicode_minus"] = False\n\n    if verbose:\n        print(f"[font] Matplotlib Korean font: {selected_font}")\n\n    return selected_font\n\n\ndef get_plotly_layout(title: str | None = None) -> dict:\n    """\n    Plotly 그래프에서 한글 폰트가 깨지지 않도록 공통 layout 값을 반환한다.\n    """\n    layout = {\n        "font": {"family": "Malgun Gothic, AppleGothic, NanumGothic, Arial"},\n        "width": 950,\n        "height": 700,\n    }\n    if title is not None:\n        layout["title"] = title\n    return layout\n\n\ndef save_json(data: dict, path) -> None:\n    """\n    dict 객체를 UTF-8 JSON으로 저장한다.\n    """\n    path = Path(path)\n    path.parent.mkdir(parents=True, exist_ok=True)\n\n    with open(path, "w", encoding="utf-8") as f:\n        json.dump(data, f, ensure_ascii=False, indent=4)\n\n\ndef save_csv(df: pd.DataFrame, path, index: bool = False) -> None:\n    """\n    CSV 저장 시 한글 호환성을 위해 utf-8-sig를 기본 사용한다.\n    """\n    path = Path(path)\n    path.parent.mkdir(parents=True, exist_ok=True)\n    df.to_csv(path, index=index, encoding="utf-8-sig")\n'
README_CONTENT = '# BankChurners Customer Segmentation Project\n\n## 프로젝트 목적\n\n신용카드 고객의 이용 행동 데이터를 기반으로 고객 세그먼트를 도출하고, 각 세그먼트의 이탈률과 행동 특성을 비교하여 카드사 관점의 유지·재활성화 전략을 제안한다.\n\n## 표준 폴더 구조\n\n```text\nproject_root/\n├── data/\n│   ├── raw/\n│   ├── interim/\n│   ├── processed/\n│   └── analysis/\n│       ├── clustering_results/\n│       ├── clustering_visualizations/\n│       └── segment_profiling/\n├── notebooks/\n├── src/\n├── config/\n├── docs/\n├── reports/\n└── outputs/\n```\n\n## 단계별 역할\n\n| 단계 | 노트북 | 목적 |\n|---|---|---|\n| Step 3.5 | `03_5_further_preprocessing.ipynb` | 팀원 Step3 결과를 clustering/profiling용 데이터로 재구성 |\n| Step 4 | `04_clustering_model_selection.ipynb` | 여러 clustering 후보 비교 및 최종 모델 선택 |\n| Step 4.5 | `04_5_clustering_visualization.ipynb` | 선택된 clustering 결과의 구조를 보조 시각화 |\n| Step 5 | `05_segment_profiling.ipynb` | 세그먼트별 행동 특성, 이탈률, 위험 신호, 전략 해석 |\n\n## 필수 입력 파일\n\n`data/interim/BankChurners_Final_Preprocessed.csv`\n\n이 파일은 팀원이 Step3 전처리까지 완료한 최종 CSV이다.\n\n## 실행 순서\n\n1. `python folder_setup.py`\n2. `data/interim/BankChurners_Final_Preprocessed.csv` 배치\n3. Step 3.5 노트북 실행\n4. Step 4 노트북 실행\n5. Step 4.5 노트북 실행\n6. Step 5 노트북 실행\n'
MANUAL_FILE_PLACEMENT_CONTENT = '# Manual File Placement Guide\n\n이 프로젝트는 폴더 구조를 자동으로 생성하지만, 원본/중간 데이터 파일은 사용자가 직접 배치해야 합니다.\n\n## 반드시 배치해야 하는 파일\n\n| 파일 | 배치 경로 | 필수 여부 | 설명 |\n|---|---|---:|---|\n| 팀원이 만든 최종 전처리 CSV | `data/interim/BankChurners_Final_Preprocessed.csv` | 필수 | Step 3.5의 입력 파일 |\n| 원본 CSV | `data/raw/머신러닝 데이터 자료(은행카드).csv` | 권장 | 추적성과 재현성을 위해 보관 |\n| 프로젝트 계획서 | `docs/프로젝트 계획서.pdf` | 권장 | 제출/설명용 참고 문서 |\n\n## 실행 순서\n\n1. `python folder_setup.py` 실행\n2. 팀원이 만든 `BankChurners_Final_Preprocessed.csv`를 `data/interim/`에 넣기\n3. 원본 CSV는 가능하면 `data/raw/`에 넣기\n4. 이후 `notebooks/03_5_further_preprocessing.ipynb`부터 순서대로 실행\n\n## 주의\n\n- 후속 노트북은 절대경로를 사용하지 않고, 프로젝트 루트를 기준으로 상대경로를 사용합니다.\n- CSV 저장은 한글 호환성을 위해 `utf-8-sig`를 사용합니다.\n- Matplotlib 한글 깨짐 방지는 `src/common.py`의 `configure_korean_font()`를 사용합니다.\n'
GITIGNORE_CONTENT = '# Python\n__pycache__/\n*.py[cod]\n.ipynb_checkpoints/\n\n# OS\n.DS_Store\nThumbs.db\n\n# Generated analysis outputs can be regenerated from notebooks.\noutputs/\nreports/figures/*.html\nreports/figures/*.png\ndata/analysis/**/*.html\ndata/analysis/**/*.png\ndata/analysis/**/*.csv\n\n# Keep data folders but avoid accidentally committing raw sensitive data if needed.\n# data/raw/*.csv\n# data/interim/*.csv\n'
REQUIREMENTS_CONTENT = 'pandas\nnumpy\nscikit-learn\nmatplotlib\nplotly\njupyter\nipykernel\n'

MANAGED_DIRS = [
    "data",
    "notebooks",
    "src",
    "config",
    "docs",
    "reports",
    "outputs",
]

GENERATED_DIRS = [
    "data/processed",
    "data/analysis",
    "reports",
    "outputs",
]

FOLDERS = [
    "data/raw",
    "data/interim",
    "data/processed",
    "data/analysis",
    "data/analysis/clustering_results",
    "data/analysis/clustering_visualizations",
    "data/analysis/segment_profiling",
    "notebooks",
    "src",
    "config",
    "docs",
    "reports",
    "reports/figures",
    "reports/tables",
    "outputs",
]

REQUIRED_MANUAL_FILES = {
    "team_step3_preprocessed": {
        "path": "data/interim/BankChurners_Final_Preprocessed.csv",
        "required": True,
        "description": "팀원이 Step3 전처리까지 완료한 최종 CSV. Step3.5의 필수 입력 파일.",
    },
    "raw_bankchurners": {
        "path": "data/raw/머신러닝 데이터 자료(은행카드).csv",
        "required": False,
        "description": "원본 BankChurners CSV. Step3.5 실행에는 필수는 아니지만 추적성과 재현성을 위해 보관 권장.",
    },
    "project_plan": {
        "path": "docs/프로젝트 계획서.pdf",
        "required": False,
        "description": "프로젝트 계획서. 분석 배경과 Step 정의를 보관하기 위한 참고 문서.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="BankChurners 고객 세그먼트 분석 프로젝트 폴더 구조 초기화"
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=".",
        help="프로젝트 루트 경로. 기본값은 현재 폴더(.)",
    )
    parser.add_argument(
        "--reset-generated",
        action="store_true",
        help="data/processed, data/analysis, reports, outputs만 삭제 후 재생성",
    )
    parser.add_argument(
        "--reset-all-managed",
        action="store_true",
        help="data, notebooks, src, config, docs, reports, outputs 전체 삭제 후 재생성",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="삭제 확인을 생략하고 실행",
    )
    return parser.parse_args()


def safe_rmtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
        print(f"[deleted] {path}")


def confirm_reset(targets: list[Path], yes: bool) -> None:
    if yes:
        return

    print("\n다음 폴더가 삭제됩니다:")
    for target in targets:
        print(f"  - {target}")

    answer = input("\n정말 삭제하고 다시 생성할까요? 계속하려면 'YES'를 입력하세요: ").strip()

    if answer != "YES":
        raise SystemExit("사용자가 삭제를 취소했습니다.")


def make_dirs(project_root: Path) -> None:
    for rel in FOLDERS:
        folder = project_root / rel
        folder.mkdir(parents=True, exist_ok=True)
        (folder / ".gitkeep").touch(exist_ok=True)

    print("[created] standard folder structure")


def write_text_file(project_root: Path, rel_path: str, content: str) -> None:
    path = project_root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[created] {path.relative_to(project_root)}")


def write_config(project_root: Path) -> None:
    config = {
        "project_name": "BankChurners Customer Segmentation",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "raw_data": "data/raw/머신러닝 데이터 자료(은행카드).csv",
            "team_step3_preprocessed": "data/interim/BankChurners_Final_Preprocessed.csv",
            "processed_dir": "data/processed",
            "clustering_results_dir": "data/analysis/clustering_results",
            "clustering_visualizations_dir": "data/analysis/clustering_visualizations",
            "segment_profiling_dir": "data/analysis/segment_profiling",
            "notebooks_dir": "notebooks",
            "src_dir": "src",
            "docs_dir": "docs",
        },
        "selected_model": {
            "candidate_key": "axis_6_without_capacity_KMeans_k6",
            "description": "Credit_Capacity_Score를 제외한 6개 행동 축 기반 K-Means k=6",
        },
        "random_state": 42,
        "encoding": "utf-8-sig",
    }
    write_text_file(
        project_root,
        "config/project_config.json",
        json.dumps(config, ensure_ascii=False, indent=4)
    )


def write_placeholder_files(project_root: Path) -> None:
    placeholders = {
        "data/raw/README.md": (
            "# data/raw\n\n"
            "원본 데이터를 보관하는 폴더입니다.\n\n"
            "권장 배치 파일:\n"
            "- `머신러닝 데이터 자료(은행카드).csv`\n"
        ),
        "data/interim/README.md": (
            "# data/interim\n\n"
            "팀원이 Step3까지 완료한 중간 전처리 데이터를 보관하는 폴더입니다.\n\n"
            "필수 배치 파일:\n"
            "- `BankChurners_Final_Preprocessed.csv`\n"
        ),
        "data/processed/README.md": (
            "# data/processed\n\n"
            "Step3.5에서 생성되는 최종 분석 입력 데이터를 보관합니다.\n"
        ),
        "data/analysis/README.md": (
            "# data/analysis\n\n"
            "Step4 이후 clustering 결과, 시각화, segment profiling 결과를 저장합니다.\n"
        ),
        "notebooks/README.md": (
            "# notebooks\n\n"
            "단계별 분석 노트북을 보관합니다.\n\n"
            "- `03_5_further_preprocessing.ipynb`\n"
            "- `04_clustering_model_selection.ipynb`\n"
            "- `04_5_clustering_visualization.ipynb`\n"
            "- `05_segment_profiling.ipynb`\n"
        ),
    }

    for rel_path, content in placeholders.items():
        write_text_file(project_root, rel_path, content)


def check_required_files(project_root: Path) -> None:
    print("\n[manual file placement check]")
    for info in REQUIRED_MANUAL_FILES.values():
        path = project_root / info["path"]
        status = "OK" if path.exists() else "MISSING"
        required = "required" if info["required"] else "optional"
        print(f"- [{status}] ({required}) {info['path']}")

    missing_required = [
        info["path"]
        for info in REQUIRED_MANUAL_FILES.values()
        if info["required"] and not (project_root / info["path"]).exists()
    ]

    if missing_required:
        print("\n다음 필수 파일을 직접 배치해야 합니다:")
        for path in missing_required:
            print(f"  - {path}")
    else:
        print("\n필수 파일 배치가 완료되어 있습니다.")


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    print(f"[project root] {project_root}")

    if args.reset_all_managed and args.reset_generated:
        raise SystemExit("--reset-all-managed와 --reset-generated는 동시에 사용할 수 없습니다.")

    if args.reset_all_managed:
        targets = [project_root / rel for rel in MANAGED_DIRS]
        confirm_reset(targets, args.yes)
        for target in targets:
            safe_rmtree(target)

    if args.reset_generated:
        targets = [project_root / rel for rel in GENERATED_DIRS]
        confirm_reset(targets, args.yes)
        for target in targets:
            safe_rmtree(target)

    make_dirs(project_root)

    write_text_file(
        project_root,
        ".project_root",
        "BankChurners Customer Segmentation Project\n"
    )
    write_text_file(project_root, "src/common.py", COMMON_PY_CONTENT)
    write_config(project_root)
    write_text_file(project_root, "docs/MANUAL_FILE_PLACEMENT.md", MANUAL_FILE_PLACEMENT_CONTENT)
    write_text_file(project_root, "README.md", README_CONTENT)
    write_text_file(project_root, ".gitignore", GITIGNORE_CONTENT)
    write_text_file(project_root, "requirements.txt", REQUIREMENTS_CONTENT)
    write_placeholder_files(project_root)
    check_required_files(project_root)

    print("\nFolder setup completed.")
    print("Next step:")
    print("1. data/interim/BankChurners_Final_Preprocessed.csv 파일을 배치하세요.")
    print("2. 이후 Step 3.5 노트북을 실행하세요.")


if __name__ == "__main__":
    main()
