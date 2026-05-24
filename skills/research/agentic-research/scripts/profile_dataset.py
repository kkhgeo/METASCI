#!/usr/bin/env python3
"""
Automated dataset profiling for agentic research.
Analyzes dataset structure, quality, and basic statistics.

Usage:
    python profile_dataset.py --dataset /path/to/data.csv --session /path/to/session/
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def load_dataset(path: str):
    """Load dataset from various formats."""
    import pandas as pd

    ext = os.path.splitext(path)[1].lower()
    loaders = {
        ".csv": pd.read_csv,
        ".tsv": lambda p: pd.read_csv(p, sep="\t"),
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
        ".parquet": pd.read_parquet,
        ".json": pd.read_json,
        ".feather": pd.read_feather,
    }

    if ext not in loaders:
        raise ValueError(f"Unsupported format: {ext}. Supported: {list(loaders.keys())}")

    return loaders[ext](path)


def profile_column(series) -> dict:
    """Profile a single column."""
    import numpy as np

    profile = {
        "name": series.name,
        "dtype": str(series.dtype),
        "missing_count": int(series.isna().sum()),
        "missing_pct": round(float(series.isna().mean()), 4),
        "unique_values": int(series.nunique()),
        "unique_pct": round(float(series.nunique() / max(len(series), 1)), 4),
    }

    if series.dtype in ["float64", "float32", "int64", "int32"]:
        desc = series.describe()
        profile["stats"] = {
            "mean": round(float(desc.get("mean", 0)), 4),
            "std": round(float(desc.get("std", 0)), 4),
            "min": round(float(desc.get("min", 0)), 4),
            "q25": round(float(desc.get("25%", 0)), 4),
            "median": round(float(desc.get("50%", 0)), 4),
            "q75": round(float(desc.get("75%", 0)), 4),
            "max": round(float(desc.get("max", 0)), 4),
        }
        # Detect skewness
        skew = float(series.skew()) if len(series.dropna()) > 2 else 0
        profile["skewness"] = round(skew, 4)
        if abs(skew) > 2:
            profile["note"] = "Highly skewed — consider log transform"
        # Detect outliers (IQR method)
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        outlier_mask = (series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)
        profile["outlier_count"] = int(outlier_mask.sum())
        profile["outlier_pct"] = round(float(outlier_mask.mean()), 4)

    elif series.dtype == "object" or series.dtype.name == "category":
        top_values = series.value_counts().head(10)
        profile["top_values"] = {str(k): int(v) for k, v in top_values.items()}
        if series.nunique() < 20:
            profile["note"] = "Low cardinality — possible categorical variable"

    elif "datetime" in str(series.dtype):
        profile["date_range"] = {
            "min": str(series.min()),
            "max": str(series.max()),
        }

    return profile


def detect_quality_issues(df) -> list:
    """Detect common data quality issues."""
    import numpy as np

    issues = []

    # High missing values
    for col in df.columns:
        miss_pct = df[col].isna().mean()
        if miss_pct > 0.3:
            issues.append(f"Column '{col}' has {miss_pct:.1%} missing values — consider dropping or imputing")
        elif miss_pct > 0.05:
            issues.append(f"Column '{col}' has {miss_pct:.1%} missing values — imputation recommended")

    # Duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        issues.append(f"{dup_count} duplicate rows detected ({dup_count/len(df):.1%})")

    # Constant columns
    for col in df.columns:
        if df[col].nunique() <= 1:
            issues.append(f"Column '{col}' is constant — consider removing")

    # High correlation detection for numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 1 and len(numeric_cols) < 100:
        corr = df[numeric_cols].corr()
        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):
                r = abs(corr.iloc[i, j])
                if r > 0.95:
                    issues.append(
                        f"Very high correlation (|r|={r:.3f}) between "
                        f"'{corr.columns[i]}' and '{corr.columns[j]}'"
                    )

    return issues


def suggest_initial_analyses(df, objective_keywords: list) -> list:
    """Suggest initial analysis tasks based on dataset structure."""
    suggestions = []
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Basic EDA
    suggestions.append({
        "task_type": "data_analysis",
        "priority": "high",
        "question": "What are the overall distributions and relationships in the dataset?",
        "approach": "Comprehensive EDA: distributions, correlations, PCA if high-dimensional",
    })

    # Group comparisons if categorical variables exist
    if categorical_cols and numeric_cols:
        suggestions.append({
            "task_type": "data_analysis",
            "priority": "high",
            "question": f"How do numeric features differ across groups defined by {categorical_cols[:3]}?",
            "approach": "Group-wise comparisons with appropriate statistical tests",
        })

    # Dimensionality reduction for high-dimensional data
    if len(numeric_cols) > 20:
        suggestions.append({
            "task_type": "data_analysis",
            "priority": "medium",
            "question": "What latent structure exists in the high-dimensional data?",
            "approach": "PCA, t-SNE, or UMAP for dimensionality reduction",
        })

    # Literature grounding
    if objective_keywords:
        suggestions.append({
            "task_type": "literature_search",
            "priority": "high",
            "question": f"What is the current state of knowledge regarding {', '.join(objective_keywords[:5])}?",
            "approach": "Targeted web search for recent papers and reviews",
        })

    return suggestions


def profile_dataset(dataset_path: str, session_dir: str):
    """Run full dataset profiling and update world model."""
    import pandas as pd

    # Load dataset
    print(f"Loading dataset: {dataset_path}")
    df = load_dataset(dataset_path)
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # Profile columns
    print("Profiling columns...")
    column_profiles = [profile_column(df[col]) for col in df.columns]

    # Detect quality issues
    print("Detecting quality issues...")
    quality_issues = detect_quality_issues(df)

    # Build profile
    profile = {
        "filename": os.path.basename(dataset_path),
        "format": os.path.splitext(dataset_path)[1].lstrip("."),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "size_mb": round(os.path.getsize(dataset_path) / 1024 / 1024, 2),
        "column_schema": column_profiles,
        "numeric_columns": df.select_dtypes(include=["number"]).columns.tolist(),
        "categorical_columns": df.select_dtypes(include=["object", "category"]).columns.tolist(),
        "datetime_columns": df.select_dtypes(include=["datetime"]).columns.tolist(),
        "quality_notes": quality_issues,
        "preprocessing_applied": [],
    }

    # Update world model
    wm_path = os.path.join(session_dir, "world_model.json")
    if os.path.exists(wm_path):
        with open(wm_path) as f:
            wm = json.load(f)

        wm["dataset_profile"] = profile
        wm["metadata"]["updated_at"] = datetime.now(timezone.utc).isoformat()
        wm["metadata"]["status"] = "ready"

        # Generate initial task queue
        keywords = wm["metadata"].get("objective_keywords", [])
        initial_tasks = suggest_initial_analyses(df, keywords)
        wm["task_queue"] = [
            {
                "task_id": f"c1_{t['task_type'][:2]}_{i+1:02d}",
                "type": t["task_type"],
                "priority": t["priority"],
                "question": t["question"],
                "approach": t["approach"],
                "depends_on": [],
            }
            for i, t in enumerate(initial_tasks)
        ]

        with open(wm_path, "w") as f:
            json.dump(wm, f, indent=2, ensure_ascii=False)
        print(f"\n✓ World model updated: {wm_path}")
    else:
        # Save standalone profile
        profile_path = os.path.join(session_dir, "dataset_profile.json")
        with open(profile_path, "w") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Profile saved: {profile_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"DATASET PROFILE SUMMARY")
    print(f"{'='*60}")
    print(f"  File: {profile['filename']} ({profile['size_mb']} MB)")
    print(f"  Shape: {profile['rows']:,} rows × {profile['columns']} columns")
    print(f"  Numeric: {len(profile['numeric_columns'])} | Categorical: {len(profile['categorical_columns'])}")
    if quality_issues:
        print(f"\n  ⚠ Quality Issues ({len(quality_issues)}):")
        for issue in quality_issues[:5]:
            print(f"    - {issue}")
    print(f"{'='*60}")

    return profile


def main():
    parser = argparse.ArgumentParser(description="Profile dataset for agentic research")
    parser.add_argument("--dataset", required=True, help="Path to dataset file")
    parser.add_argument("--session", required=True, help="Session directory")
    args = parser.parse_args()

    profile_dataset(args.dataset, args.session)


if __name__ == "__main__":
    main()
