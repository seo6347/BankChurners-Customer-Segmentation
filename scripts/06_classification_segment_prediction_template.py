"""
06_classification_segment_prediction_template.py

Purpose
-------
Train classification models to reproduce the final k=5 segment labels.

Important
---------
This is NOT churn prediction.
Target is the final clustering segment label, not Attrition_Flag.

Recommended input:
data/analysis/segment_profiling/core_7_KMeans_k5/11_profile_table_with_segment_k5.csv

Recommended output:
data/analysis/classification/core_7_KMeans_k5/
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

OUTPUT_DIR = Path("data/analysis/classification/core_7_KMeans_k5")
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


def find_input_file() -> Path:
    for path in INPUT_CANDIDATES:
        if path.exists():
            return path
    msg = "No Step5 final segment table found. Checked:\n"
    msg += "\n".join(str(p) for p in INPUT_CANDIDATES)
    raise FileNotFoundError(msg)


def load_data() -> pd.DataFrame:
    input_path = find_input_file()
    df = pd.read_csv(input_path)

    missing_features = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing_features:
        raise ValueError(f"Missing feature columns: {missing_features}")

    if TARGET_COL not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COL}")

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
            "Target is final k=5 cluster label. "
            "Attrition_Flag must not be used as an input feature."
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
        report_df.to_csv(OUTPUT_DIR / f"02_classification_report_{model_name}.csv", encoding="utf-8-sig")

        cm = confusion_matrix(y_test, pred, labels=sorted(np.unique(y_test)))
        cm_df = pd.DataFrame(
            cm,
            index=[f"true_C{i}" for i in sorted(np.unique(y_test))],
            columns=[f"pred_C{i}" for i in sorted(np.unique(y_test))],
        )
        cm_df.to_csv(OUTPUT_DIR / f"03_confusion_matrix_{model_name}.csv", encoding="utf-8-sig")

    metrics_df = pd.DataFrame(metric_rows).sort_values("macro_f1", ascending=False)
    metrics_df.to_csv(OUTPUT_DIR / "01_classification_metrics_summary.csv", index=False, encoding="utf-8-sig")

    return metrics_df, fitted_models


def save_best_model_outputs(df, X_train, X_test, y_train, y_test, metrics_df, fitted_models) -> None:
    best_model_name = metrics_df.iloc[0]["model"]
    best_model = fitted_models[best_model_name]
    pred = best_model.predict(X_test)

    labels = sorted(np.unique(y_test))
    cm = confusion_matrix(y_test, pred, labels=labels)

    # Confusion matrix plot
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm)
    ax.set_title(f"Confusion Matrix - {best_model_name}")
    ax.set_xlabel("Predicted segment")
    ax.set_ylabel("True segment")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels([f"C{i}" for i in labels])
    ax.set_yticklabels([f"C{i}" for i in labels])

    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center")

    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04_confusion_matrix_best_model.png", dpi=200)
    plt.close(fig)

    # Feature importance for random forest
    if "random_forest" in fitted_models:
        rf = fitted_models["random_forest"]
        importance_df = pd.DataFrame(
            {
                "feature": FEATURE_COLUMNS,
                "importance": rf.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        importance_df.to_csv(
            OUTPUT_DIR / "05_feature_importance_random_forest.csv",
            index=False,
            encoding="utf-8-sig",
        )

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(importance_df["feature"][::-1], importance_df["importance"][::-1])
        ax.set_title("Random Forest Feature Importance")
        ax.set_xlabel("Importance")
        ax.set_ylabel("Feature")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / "06_feature_importance_random_forest.png", dpi=200)
        plt.close(fig)

    # Logistic regression coefficients
    if "logistic_regression" in fitted_models:
        lr_pipe = fitted_models["logistic_regression"]
        lr = lr_pipe.named_steps["model"]
        coef_df = pd.DataFrame(
            lr.coef_,
            columns=FEATURE_COLUMNS,
            index=[f"class_C{i}" for i in lr.classes_],
        )
        coef_df.to_csv(
            OUTPUT_DIR / "07_logistic_regression_coefficients.csv",
            encoding="utf-8-sig",
        )

    # Predicted segment table for test set
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

    # Summary markdown
    summary = f"""# Step6 Classification Summary

## Purpose

This classification model predicts final k=5 segment labels from customer behavior features.

This is **not churn prediction**.  
Target is `Cluster`, not `Attrition_Flag`.

## Input Features

{chr(10).join(f"- `{c}`" for c in FEATURE_COLUMNS)}

## Target

- `Cluster`: final `core_7_KMeans_k5` segment label

## Best Model

```text
{best_model_name}
```

## Metrics

{metrics_df.to_markdown(index=False)}

## Interpretation Caution

The labels were produced by the final clustering model.  
Therefore, classification metrics should be interpreted as **surrogate fidelity**:
how well the classification model reproduces the final segmentation structure.

Do not interpret these metrics as churn prediction performance.

## Recommended Next Use

- Use confusion matrix to see which segments are similar.
- Use feature importance to explain which behavior axes separate segments.
- Pay special attention to C3 recall because C3 is the high-risk attrition segment.
"""
    (OUTPUT_DIR / "09_step6_classification_summary.md").write_text(summary, encoding="utf-8")


def main():
    df = load_data()

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COL].astype(int).copy()

    # Stratified split keeps the C0~C4 ratio similar in train/test.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    metrics_df, fitted_models = evaluate_models(X_train, X_test, y_train, y_test)
    save_best_model_outputs(df, X_train, X_test, y_train, y_test, metrics_df, fitted_models)

    print("Step6 classification completed.")
    print(f"Outputs saved to: {OUTPUT_DIR}")
    print(metrics_df)


if __name__ == "__main__":
    main()
