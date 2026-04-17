"""
Step 1 & 2: Data Pipeline — Load, Validate, Clean
Handles: missing values, outliers, type corrections, deduplication.
Tools: pandas, numpy
"""

import os
import re
import numpy as np
import pandas as pd

# ─── Paths ────────────────────────────────────────────────────────────────────
RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'car_details.csv')
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'car_cleaned.csv')


def load_data(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """Step 1 — Download / Load raw data."""
    df = pd.read_csv(path)
    print(f"[LOAD] Loaded {df.shape[0]} rows, {df.shape[1]} columns from {path}")
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Step 1 — Validate schema, row counts, column integrity."""
    required_cols = ['name', 'year', 'selling_price', 'km_driven', 'fuel',
                     'seller_type', 'transmission', 'owner', 'mileage',
                     'engine', 'max_power', 'torque', 'seats']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    print(f"[VALIDATE] Schema OK — {len(df.columns)} columns present")
    print(f"[VALIDATE] Row count: {len(df)}")
    return df


# ─── Step 2.3: Data Type Corrections ─────────────────────────────────────────
def _extract_numeric(value):
    """Extract first numeric value from a string like '23.4 kmpl' → 23.4"""
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r'[\d.]+', str(value))
    return float(match.group()) if match else np.nan


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2.3 — Strip units from mileage, engine, max_power columns."""
    df['mileage'] = df['mileage'].apply(_extract_numeric)
    df['engine'] = df['engine'].apply(_extract_numeric).astype('Int64')
    df['max_power'] = df['max_power'].apply(_extract_numeric)
    df['seats'] = pd.to_numeric(df['seats'], errors='coerce').astype('Int64')
    print("[TYPES] Converted mileage, engine, max_power, seats to numeric")
    return df


# ─── Step 2.1: Missing Value Treatment ───────────────────────────────────────
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2.1 — Impute missing values: median for numeric, mode for categorical."""
    # Report missing
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        print(f"[MISSING] Found missing values:\n{missing}")
    else:
        print("[MISSING] No missing values found")
        return df

    # Drop columns with > 30% missing
    threshold = 0.30 * len(df)
    high_missing = [c for c in df.columns if df[c].isnull().sum() > threshold]
    if high_missing:
        print(f"[MISSING] Dropping columns with >30% missing: {high_missing}")
        df = df.drop(columns=high_missing)

    # Numerical: impute with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    # Categorical: impute with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    print(f"[MISSING] After imputation — remaining nulls: {df.isnull().sum().sum()}")
    return df


# ─── Step 2.2: Outlier Detection and Removal ─────────────────────────────────
def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2.2 — Remove outliers using IQR + domain rules."""
    initial = len(df)

    # Domain-based filters
    df = df[df['selling_price'] >= 10000]
    df = df[df['selling_price'] <= 10000000]
    df = df[df['km_driven'] <= 500000]
    df = df[(df['year'] >= 1990) & (df['year'] <= 2025)]

    # IQR method for numerical columns
    for col in ['selling_price', 'km_driven']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    removed = initial - len(df)
    print(f"[OUTLIERS] Removed {removed} rows ({removed/initial*100:.1f}%)")
    return df


# ─── Step 2.4: Deduplication ─────────────────────────────────────────────────
def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2.4 — Drop exact duplicate rows."""
    initial = len(df)
    df = df.drop_duplicates()
    removed = initial - len(df)
    print(f"[DEDUP] Removed {removed} duplicate rows")
    return df


# ─── Main Pipeline ───────────────────────────────────────────────────────────
def run_pipeline():
    """Execute the full data pipeline: load → validate → clean → save."""
    print("=" * 60)
    print("  DATA PIPELINE — Used Car Price Prediction")
    print("=" * 60)

    df = load_data()
    df = validate_data(df)
    df = fix_data_types(df)
    df = handle_missing_values(df)
    df = remove_outliers(df)
    df = deduplicate(df)

    # Drop torque (complex parsing, not in final feature list)
    if 'torque' in df.columns:
        df = df.drop(columns=['torque'])

    # Save processed data
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"\n[SAVE] Cleaned data saved to {PROCESSED_DATA_PATH}")
    print(f"[SAVE] Final shape: {df.shape}")
    return df


if __name__ == '__main__':
    run_pipeline()
