"""
Step 3: Feature Engineering
Handles: derived features, encoding, scaling, feature selection.
Tools: pandas, scikit-learn (StandardScaler, LabelEncoder, OneHotEncoder)
"""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'car_cleaned.csv')
ENGINEERED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'car_engineered.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')


def load_cleaned_data() -> pd.DataFrame:
    df = pd.read_csv(CLEANED_DATA_PATH)
    print(f"[FE] Loaded cleaned data: {df.shape}")
    return df


# ─── Step 3.1: Derive New Features ───────────────────────────────────────────
def derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3.1 — Create car_age, brand, model_name, price_per_km, is_first_owner."""
    current_year = 2025
    df['car_age'] = current_year - df['year']
    df['brand'] = df['name'].apply(lambda x: str(x).split()[0])
    df['model_name'] = df['name'].apply(lambda x: str(x).split()[1] if len(str(x).split()) > 1 else 'Unknown')
    df['price_per_km'] = df['selling_price'] / (df['km_driven'] + 1)
    df['is_first_owner'] = (df['owner'] == 'First Owner').astype(int)
    print(f"[FE] Derived features: car_age, brand, model_name, price_per_km, is_first_owner")
    return df


# ─── Step 3.2: Encoding Categorical Variables ────────────────────────────────
def encode_features(df: pd.DataFrame):
    """Step 3.2 — Label, One-Hot, and Target encoding."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    encoders = {}

    # Label Encoding for ordinal columns
    for col in ['owner', 'seller_type']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        print(f"[ENCODE] Label encoded: {col} → {le.classes_.tolist()}")

    # One-Hot Encoding for nominal columns
    df = pd.get_dummies(df, columns=['fuel', 'transmission'], drop_first=True, dtype=int)
    print("[ENCODE] One-hot encoded: fuel, transmission")

    # Target Encoding for high-cardinality columns (brand)
    brand_means = df.groupby('brand')['selling_price'].mean()
    df['brand_encoded'] = df['brand'].map(brand_means)
    encoders['brand_target'] = brand_means.to_dict()
    print(f"[ENCODE] Target encoded: brand ({len(brand_means)} unique values)")

    # Save encoders
    encoder_path = os.path.join(MODELS_DIR, 'encoder.pkl')
    joblib.dump(encoders, encoder_path)
    print(f"[ENCODE] Encoders saved to {encoder_path}")

    return df, encoders


# ─── Step 3.3: Feature Scaling ───────────────────────────────────────────────
def scale_features(df: pd.DataFrame):
    """Step 3.3 — StandardScaler for numerical features."""
    scale_cols = ['km_driven', 'engine', 'max_power', 'mileage']
    # Filter to only existing columns
    scale_cols = [c for c in scale_cols if c in df.columns]

    scaler = StandardScaler()
    df[scale_cols] = scaler.fit_transform(df[scale_cols])

    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    joblib.dump({'scaler': scaler, 'columns': scale_cols}, scaler_path)
    print(f"[SCALE] StandardScaler applied to: {scale_cols}")
    print(f"[SCALE] Scaler saved to {scaler_path}")

    return df, scaler


# ─── Step 3.4: Feature Selection ─────────────────────────────────────────────
def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3.4 — Remove highly correlated features + select final columns."""
    # Drop non-feature columns
    drop_cols = ['name', 'model_name', 'brand', 'year', 'price_per_km']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

    # Remove highly correlated numeric features (threshold > 0.90)
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > 0.90)]
    if to_drop:
        print(f"[SELECT] Dropping highly correlated features: {to_drop}")
        df = df.drop(columns=to_drop, errors='ignore')

    print(f"[SELECT] Final features: {df.columns.tolist()}")
    print(f"[SELECT] Final shape: {df.shape}")
    return df


# ─── Main Pipeline ───────────────────────────────────────────────────────────
def run_feature_engineering():
    """Execute the full feature engineering pipeline."""
    print("=" * 60)
    print("  FEATURE ENGINEERING — Used Car Price Prediction")
    print("=" * 60)

    df = load_cleaned_data()
    df = derive_features(df)
    df, encoders = encode_features(df)
    df, scaler = scale_features(df)
    df = select_features(df)

    # Save engineered data
    os.makedirs(os.path.dirname(ENGINEERED_DATA_PATH), exist_ok=True)
    df.to_csv(ENGINEERED_DATA_PATH, index=False)
    print(f"\n[SAVE] Engineered data saved to {ENGINEERED_DATA_PATH}")
    return df


if __name__ == '__main__':
    run_feature_engineering()
