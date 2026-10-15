"""
CropWise - Model Training and Evaluation Pipeline
SDG 2: Zero Hunger | Sustainable Precision Agriculture

Trains a supervised RandomForestClassifier to predict suitable crops based on
soil nutrients (N, P, K) and environmental conditions (temperature, humidity, pH, rainfall).
Calculates and saves genuine evaluation metrics on a held-out stratified test set.
"""

import os
import json
import argparse
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

FEATURE_COLS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_COL = "label"


def load_or_generate_data(csv_path: str = os.path.join("data", "crop_data.csv")) -> pd.DataFrame:
    """Load dataset from CSV, or automatically generate if not found."""
    if not os.path.exists(csv_path):
        print(f"[!] Dataset not found at '{csv_path}'. Automatically generating synthetic dataset...")
        from generate_data import generate_dataset
        df = generate_dataset(samples_per_crop=100, random_seed=42)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        print(f"[+] Generated dataset with {len(df)} rows and saved to '{csv_path}'.")
    else:
        df = pd.read_csv(csv_path)
        print(f"[+] Loaded existing dataset from '{csv_path}' ({len(df)} rows).")

    return df


def train_and_evaluate(
    data_path: str = os.path.join("data", "crop_data.csv"),
    model_output_dir: str = "models",
    test_size: float = 0.20,
    random_seed: int = 42
) -> dict:
    """
    Train Random Forest model and compute real test set metrics.
    """
    os.makedirs(model_output_dir, exist_ok=True)

    # 1. Load data
    df = load_or_generate_data(data_path)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    classes = sorted(list(y.unique()))

    # 2. Stratified train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_seed,
        stratify=y
    )

    print(f"[*] Training samples: {len(X_train)} | Test samples: {len(X_test)}")
    print(f"[*] Number of crop classes: {len(classes)}")

    # 3. Supervised Model Training: RandomForestClassifier
    print("[*] Training RandomForestClassifier (100 estimators, max_depth=16)...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=16,
        random_state=random_seed,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    # 4. Predict on held-out test data
    y_pred = clf.predict(X_test)

    # 5. Calculate genuine evaluation metrics on test set
    accuracy = float(accuracy_score(y_test, y_pred))
    precision_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    precision_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    recall_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    recall_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    cm = confusion_matrix(y_test, y_pred, labels=classes)
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    # Feature importance
    feature_importances = {
        feat: round(float(imp), 4)
        for feat, imp in zip(FEATURE_COLS, clf.feature_importances_)
    }
    # Sort feature importances descending
    feature_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))

    metrics_payload = {
        "model_type": "RandomForestClassifier",
        "random_seed": random_seed,
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "num_classes": len(classes),
        "classes": classes,
        "features": FEATURE_COLS,
        "accuracy": round(accuracy, 4),
        "precision_macro": round(precision_macro, 4),
        "precision_weighted": round(precision_weighted, 4),
        "recall_macro": round(recall_macro, 4),
        "recall_weighted": round(recall_weighted, 4),
        "f1_macro": round(f1_macro, 4),
        "f1_weighted": round(f1_weighted, 4),
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict,
        "feature_importances": feature_importances
    }

    # 6. Save model and metrics locally
    model_path = os.path.join(model_output_dir, "crop_model.joblib")
    metrics_path = os.path.join(model_output_dir, "model_metrics.json")
    cm_plot_path = os.path.join(model_output_dir, "confusion_matrix.png")

    joblib.dump(clf, model_path)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    # 7. Generate and save confusion matrix figure
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Greens",
        xticklabels=classes,
        yticklabels=classes,
        cbar=True
    )
    plt.title(f"CropWise Test Confusion Matrix (Accuracy: {accuracy * 100:.2f}%)", fontsize=14, pad=15)
    plt.xlabel("Predicted Crop Label", fontsize=11, labelpad=10)
    plt.ylabel("Actual Crop Label", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(cm_plot_path, dpi=200)
    plt.close()

    # 8. Print evaluation summary
    print("\n" + "=" * 65)
    print("CropWise - Model Training & Evaluation Complete")
    print("=" * 65)
    print(f"Algorithm:           RandomForestClassifier")
    print(f"Test Set Accuracy:   {accuracy * 100:.2f}%")
    print(f"Test Set Precision:  {precision_weighted * 100:.2f}% (weighted) | {precision_macro * 100:.2f}% (macro)")
    print(f"Test Set Recall:     {recall_weighted * 100:.2f}% (weighted) | {recall_macro * 100:.2f}% (macro)")
    print(f"Test Set F1-Score:   {f1_weighted * 100:.2f}% (weighted) | {f1_macro * 100:.2f}% (macro)")
    print("-" * 65)
    print("Feature Importances:")
    for feat, imp in feature_importances.items():
        bar = "#" * int(imp * 40)
        print(f"  {feat:12} : {imp:.4f} {bar}")
    print("-" * 65)
    print(f"[+] Model saved to:            {os.path.abspath(model_path)}")
    print(f"[+] Metrics saved to:          {os.path.abspath(metrics_path)}")
    print(f"[+] Confusion matrix saved to: {os.path.abspath(cm_plot_path)}")
    print("=" * 65 + "\n")

    return metrics_payload


def main():
    parser = argparse.ArgumentParser(
        description="Train and evaluate CropWise Random Forest classifier"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=os.path.join("data", "crop_data.csv"),
        help="Path to input dataset CSV"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="models",
        help="Directory to save trained model and metrics"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for train/test split and RandomForest"
    )

    args = parser.parse_args()
    train_and_evaluate(
        data_path=args.data,
        model_output_dir=args.output_dir,
        random_seed=args.seed
    )


if __name__ == "__main__":
    main()
