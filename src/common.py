from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager


CSV_ENCODING_CANDIDATES = ("utf-8-sig", "utf-8", "cp949", "euc-kr")

KOREAN_FONT_CANDIDATES = (
    "Malgun Gothic",      # Windows
    "AppleGothic",       # macOS
    "NanumGothic",       # Linux / Colab
    "Noto Sans CJK KR",
    "Noto Sans KR",
)


def get_project_root() -> Path:
    """
    현재 작업 위치가 project root이든 notebooks 폴더이든,
    data 폴더와 src 폴더를 기준으로 project root를 찾는다.
    """
    current = Path.cwd().resolve()
    candidates = [current] + list(current.parents)

    for path in candidates:
        if (path / "data").exists() and (path / "src").exists():
            return path

    return current


def read_csv_safely(path, **kwargs) -> pd.DataFrame:
    """
    UTF-8/CP949/EUC-KR 인코딩 이슈를 피하기 위한 CSV 로더.
    """
    path = Path(path)
    last_error = None

    for encoding in CSV_ENCODING_CANDIDATES:
        try:
            return pd.read_csv(path, encoding=encoding, **kwargs)
        except UnicodeDecodeError as exc:
            last_error = exc

    raise last_error


def configure_korean_font(verbose: bool = True):
    """
    Matplotlib에서 한글이 깨지지 않도록 사용 가능한 한글 폰트를 설정한다.
    Windows에서는 보통 Malgun Gothic이 사용된다.
    """
    installed_fonts = {font.name for font in font_manager.fontManager.ttflist}

    selected_font = next(
        (font for font in KOREAN_FONT_CANDIDATES if font in installed_fonts),
        None
    )

    if selected_font is None:
        if verbose:
            print("[warning] 설치된 한글 폰트를 찾지 못했습니다.")
            print("Windows: Malgun Gothic, macOS: AppleGothic, Linux: NanumGothic 설치를 확인하세요.")
        plt.rcParams["axes.unicode_minus"] = False
        return None

    plt.rcParams["font.family"] = selected_font
    plt.rcParams["axes.unicode_minus"] = False

    if verbose:
        print(f"[font] Matplotlib Korean font: {selected_font}")

    return selected_font


def get_plotly_layout(title: str | None = None) -> dict:
    """
    Plotly 그래프에서 한글 폰트가 깨지지 않도록 공통 layout 값을 반환한다.
    """
    layout = {
        "font": {"family": "Malgun Gothic, AppleGothic, NanumGothic, Arial"},
        "width": 950,
        "height": 700,
    }
    if title is not None:
        layout["title"] = title
    return layout


def save_json(data: dict, path) -> None:
    """
    dict 객체를 UTF-8 JSON으로 저장한다.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_csv(df: pd.DataFrame, path, index: bool = False) -> None:
    """
    CSV 저장 시 한글 호환성을 위해 utf-8-sig를 기본 사용한다.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index, encoding="utf-8-sig")
