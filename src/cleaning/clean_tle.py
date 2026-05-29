import pandas as pd
import json
import os
import glob
from datetime import datetime, timezone

REQUIRED_FIELDS = [
    "OBJECT_NAME", "NORAD_CAT_ID", "EPOCH",
    "INCLINATION", "ECCENTRICITY", "MEAN_MOTION",
    "BSTAR", "RA_OF_ASC_NODE", "ARG_OF_PERICENTER"
]

TEXT_FIELDS = [
    "OBJECT_NAME", "EPOCH"
]

NUMERIC_FIELDS = [
    "INCLINATION", "ECCENTRICITY", "MEAN_MOTION",
    "BSTAR", "RA_OF_ASC_NODE", "ARG_OF_PERICENTER",
    "MEAN_ANOMALY", "MEAN_MOTION_DOT", "MEAN_MOTION_DDOT"
]


def load_latest_raw(group_key: str = "active") -> list:
    pattern = f"data/raw/tle_{group_key}_*.json"
    files = sorted(glob.glob(pattern))

    if not files:
        raise FileNotFoundError(f"No raw files found for group '{group_key}'")

    latest = files[-1]
    print(f"[clean] Loading → {latest}")

    with open(latest, "r") as f:
        return json.load(f)


def clean(group_key: str = "active", save: bool = True) -> pd.DataFrame:
    raw = load_latest_raw(group_key)
    df = pd.DataFrame(raw)

    print(f"[clean] Raw records      : {len(df)}")

    # Keep only rows with required fields present
    df = df.dropna(subset=REQUIRED_FIELDS)

    # Remove blank text values
    for col in TEXT_FIELDS:
        df = df[df[col].astype(str).str.strip() != ""]

    print(f"[clean] After null drop  : {len(df)}")

    # Convert numeric fields
    for col in NUMERIC_FIELDS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where numeric conversion failed
    numeric_existing = [c for c in NUMERIC_FIELDS if c in df.columns]
    df = df.dropna(subset=numeric_existing)

    print(f"[clean] After type check : {len(df)}")

    # Parse epoch to datetime
    df["EPOCH"] = pd.to_datetime(df["EPOCH"], errors="coerce", utc=True)
    df = df.dropna(subset=["EPOCH"])

    print(f"[clean] After epoch check: {len(df)}")

    # Basic physical/orbital range validation
    df = df[(df["INCLINATION"] >= 0) & (df["INCLINATION"] <= 180)]
    df = df[(df["ECCENTRICITY"] >= 0) & (df["ECCENTRICITY"] < 1)]
    df = df[df["MEAN_MOTION"] > 0]

    print(f"[clean] After range check: {len(df)}")

    df = df.reset_index(drop=True)

    if save:
        os.makedirs("data/processed", exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        path = f"data/processed/clean_{group_key}_{ts}.csv"

        df.to_csv(path, index=False)

        print(f"[clean] Saved → {path}")

    return df


if __name__ == "__main__":
    df = clean("active")

    print(f"\nShape       : {df.shape}")
    print(f"Columns     : {list(df.columns)}")
    print("\nSample rows :")
    print(df[["OBJECT_NAME", "INCLINATION", "ECCENTRICITY", "MEAN_MOTION"]].head(3))