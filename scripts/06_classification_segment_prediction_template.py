"""
06_classification_segment_prediction_template.py

최종 K-Means k=5 세그먼트 label을 core_7 행동 feature로 재현하는
Step 6/7 classification 실행 템플릿이다.

주의:
이 스크립트는 churn prediction이 아니다.
Target은 `Attrition_Flag`가 아니라 최종 clustering segment label인 `Cluster`이다.

권장 입력:
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv

권장 출력:
data/analysis/segment_classification/core_7_KMeans_k5/
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42

INPUT_CANDIDATES = [
    Path("data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv"),
    Path("data/analysis/clustering_results/13_final_customer_segments_core7_kmeans_k5.csv"),
]

OUTPUT_DIR = Path("data/analysis/segment_classification/core_7_KMeans_k5")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_COLUMNS = [
    "Activity_Score",
    "Count_Decline_Risk_Score",
    "Amount_Decline_Risk_Score",
    "Inactivity_Score",
    "Product_Relationship_Score",
    "Contact_Burden_Score",
    "Credit_Utilization_Score",
]

TARGET_COL = "Cluster"
SEGMENT_NAME_COL = "Segment_Name"

SEGMENT_NAME_MAP = {
    0: "상품 관계 중심 저위험 안정군",
    1: "신용 활용 중심 저위험 금융활용군",
    2: "고활동·저관계 잠재 전환군",
    3: "거래 감소·저활동·접촉 부담형 초고위험 이탈군",
    4: "저활동·비감소형 초저위험 안정군",
}


def safe_model_name(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_")


def find_input_file() -> Path:
    for path in INPUT_CANDIDATES:
        if path.exists():
            return path
    msg = "Step5 최종 segment table을 찾지 못했습니다. 확인한 경로:\n"
    msg += "\n".join(str(p) for p in INPUT_CANDIDATES)
    raise FileNotFoundError(msg)


def load_data() -> pd.DataFrame:
    input_path = find_input_file()
    df = pd.read_csv(input_path)

    missing_features = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing_features:
        raise ValueError(f"누락된 feature 컬럼: {missing_features}")

    if TARGET_COL not in df.columns:
        raise ValueError(f"누락된 target 컬럼: {TARGET_COL}")

    df = df.copy()
    df[TARGET_COL] = df[TARGET_COL].astype(int)

    if SEGMENT_NAME_COL not in df.columns:
        df[SEGMENT_NAME_COL] = df[TARGET_COL].map(SEGMENT_NAME_MAP)

    input_check = {
        "input_path": str(input_path),
        "n_rows": int(len(df)),
        "feature_columns": FEATURE_COLUMNS,
        "target_col": TARGET_COL,
        "target_distribution": df[TARGET_COL].value_counts().sort_index().to_dict(),
        "note": (
            "Target은 최종 k=5 cluster label입니다. "
            "Attrition_Flag는 입력 feature로 사용하지 않습니다."
        ),
    }
    (OUTPUT_DIR / "00_input_check.json").write_text(
        json.dumps(input_check, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return df


def build_models() -> dict:
    models = {
        "dummy_most_frequent": DummyClassifier(strategy="most_frequent"),
        "logistic_regression": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                        multi_class="auto",
                    ),
                ),
            ]
        ),
        "decision_tree": DecisionTreeClassifier(
            max_depth=4,
            min_samples_leaf=50,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=500,
            min_samples_leaf=20,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "xgboost": xgb.XGBClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
            eval_metric="mlogloss",
            verbosity=0,
        ),
        "lightgbm": lgb.LGBMClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
            verbose=-1,
        ),
    }
    return models


def evaluate_models(X_train, X_test, y_train, y_test) -> tuple[pd.DataFrame, dict]:
    models = build_models()
    metric_rows = []
    fitted_models = {}

    for model_name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        metric_rows.append(
            {
                "model": model_name,
                "accuracy": accuracy_score(y_test, pred),
                "macro_f1": f1_score(y_test, pred, average="macro"),
                "weighted_f1": f1_score(y_test, pred, average="weighted"),
            }
        )
        fitted_models[model_name] = model

        report_dict = classification_report(
            y_test,
            pred,
            labels=sorted(np.unique(y_test)),
            output_dict=True,
            zero_division=0,
        )
        report_df = pd.DataFrame(report_dict).T
        model_slug = safe_model_name(model_name)
        report_df.to_csv(OUTPUT_DIR / f"02_classification_report_{model_slug}.csv", encoding="utf-8-sig")

        cm = confusion_matrix(y_test, pred, labels=sorted(np.unique(y_test)))
        cm_df = pd.DataFrame(
            cm,
            index=[f"true_C{i}" for i in sorted(np.unique(y_test))],
            columns=[f"pred_C{i}" for i in sorted(np.unique(y_test))],
        )
        cm_df.to_csv(OUTPUT_DIR / f"03_confusion_matrix_{model_slug}.csv", encoding="utf-8-sig")

    metrics_df = pd.DataFrame(metric_rows).sort_values("macro_f1", ascending=False)
    metrics_df.to_csv(OUTPUT_DIR / "01_classification_metrics_summary.csv", index=False, encoding="utf-8-sig")

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_df = metrics_df.sort_values("macro_f1")
    ax.barh(plot_df["model"], plot_df["macro_f1"])
    ax.set_title("모델 비교 - Macro F1")
    ax.set_xlabel("Macro F1")
    ax.set_ylabel("Model")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "06_model_comparison.png", dpi=200)
    plt.close(fig)

    return metrics_df, fitted_models


def save_best_model_outputs(df, X_train, X_test, y_train, y_test, metrics_df, fitted_models) -> None:
    best_model_name = metrics_df.iloc[0]["model"]
    best_model = fitted_models[best_model_name]
    pred = best_model.predict(X_test)

    labels = sorted(np.unique(y_test))
    cm = confusion_matrix(y_test, pred, labels=labels)

    # 최종 선택 모델의 segment label 재현 패턴을 확인한다.
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm)
    ax.set_title(f"혼동행렬 - {best_model_name}")
    ax.set_xlabel("예측 segment")
    ax.set_ylabel("실제 segment")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels([f"C{i}" for i in labels])
    ax.set_yticklabels([f"C{i}" for i in labels])

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "07_confusion_matrices.png", dpi=200)
    plt.close(fig)

    # Random Forest 기준으로 segment 구분에 기여한 행동 축을 확인한다.
    if "random_forest" in fitted_models:
        rf = fitted_models["random_forest"]
        importance_df = pd.DataFrame(
            {
                "feature": FEATURE_COLUMNS,
                "importance": rf.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        importance_df.to_csv(
            OUTPUT_DIR / "09_feature_importance_random_forest.csv",
            index=False,
            encoding="utf-8-sig",
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(importance_df["feature"][::-1], importance_df["importance"][::-1])
        ax.set_title("Random Forest 변수 중요도")
        ax.set_xlabel("중요도")
        ax.set_ylabel("행동 feature")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / "10_feature_importance_random_forest.png", dpi=200)
        plt.close(fig)

    # Logistic Regression 계수로 segment별 방향성을 확인한다.
    if "logistic_regression" in fitted_models:
        lr_pipe = fitted_models["logistic_regression"]
        lr = lr_pipe.named_steps["model"]
        coef_df = pd.DataFrame(
            lr.coef_,
            columns=FEATURE_COLUMNS,
            index=[f"class_C{i}" for i in lr.classes_],
        )
        coef_df.to_csv(
            OUTPUT_DIR / "11_logistic_regression_coefficients.csv",
            encoding="utf-8-sig",
        )

    # 테스트 고객별 실제/예측 segment를 저장한다.
    pred_table = X_test.copy()
    pred_table["true_cluster"] = y_test.values
    pred_table["pred_cluster"] = pred
    pred_table["true_segment_name"] = pred_table["true_cluster"].map(SEGMENT_NAME_MAP)
    pred_table["pred_segment_name"] = pred_table["pred_cluster"].map(SEGMENT_NAME_MAP)
    pred_table.to_csv(
        OUTPUT_DIR / "08_predicted_segment_table_test.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # 결과 해석 요약을 한국어 Markdown으로 저장한다.
    summary = f"""# Step6 Classification 요약

## 목적

이 classification model은 고객 행동 feature를 사용해 최종 k=5 segment label을 재현한다.

이 단계는 **churn prediction이 아니다**.<br>
Target은 `Attrition_Flag`가 아니라 `Cluster`이다.

## 입력 Feature

{chr(10).join(f"- `{c}`" for c in FEATURE_COLUMNS)}

## Target

- `Cluster`: 최종 `core_7_KMeans_k5` segment label

## 최종 성능 기준 최고 모델

```text
{best_model_name}
```

## 성능 지표

{metrics_df.to_markdown(index=False)}

## 해석 주의사항

이 label은 최종 clustering model에서 생성된 pseudo-label이다.<br>
따라서 classification metric은 **세그먼트 label 재현 성능**으로 해석해야 한다.

이 값을 이탈 예측 성능으로 해석하면 안 된다.

## 활용 방향

- Confusion matrix로 서로 헷갈리는 segment 조합을 확인한다.
- Feature importance로 segment 구분에 중요한 행동 축을 설명한다.
- C3는 고위험 segment이므로 C3 recall을 별도로 확인한다.
"""
    (OUTPUT_DIR / "14_step6_7_classification_summary.md").write_text(summary, encoding="utf-8")


def main():
    df = load_data()

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COL].astype(int).copy()

    # Stratified split으로 train/test의 C0~C4 비율을 비슷하게 유지한다.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    metrics_df, fitted_models = evaluate_models(X_train, X_test, y_train, y_test)
    save_best_model_outputs(df, X_train, X_test, y_train, y_test, metrics_df, fitted_models)

    print("Step6 classification 완료")
    print(f"출력 저장 위치: {OUTPUT_DIR}")
    print(metrics_df)


if __name__ == "__main__":
    main()
