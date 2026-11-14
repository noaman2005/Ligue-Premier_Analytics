
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "epl_2024_25.csv"
OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" /
    "epl_2024_25_cleaned.csv"
)

# --------------------------------------------------
# COLUMNS REQUIRED FOR FOOTBALL ANALYSIS
# --------------------------------------------------

KEEP_COLUMNS = [
    "Div",
    "Date",
    "Time",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HTHG",
    "HTAG",
    "HTR",
    "Referee",
    "HS",
    "AS",
    "HST",
    "AST",
    "HF",
    "AF",
    "HC",
    "AC",
    "HY",
    "AY",
    "HR",
    "AR"
]

REQUIRED_COLUMNS = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR"
]


def clean_dataset():

    print("=" * 55)
    print("PREMIER LEAGUE DATA CLEANING")
    print("=" * 55)

    # 1. Load original dataset
    df = pd.read_csv(RAW_PATH)

    print(f"\nOriginal shape: {df.shape}")

    # 2. Verify required columns exist
    missing_columns = [
        col for col in KEEP_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}"
        )

    # 3. Retain football-related columns only
    df = df[KEEP_COLUMNS].copy()

    # 4. Convert dates
    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True,
        errors="coerce"
    )

    # 5. Convert numerical match statistics
    numeric_columns = [
        "FTHG", "FTAG", "HTHG", "HTAG",
        "HS", "AS", "HST", "AST",
        "HF", "AF", "HC", "AC",
        "HY", "AY", "HR", "AR"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 6. Standardise text fields
    text_columns = [
        "Div", "Time", "HomeTeam",
        "AwayTeam", "FTR", "HTR", "Referee"
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # 7. Validate essential match information
    if df[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError(
            "Essential match information contains missing values."
        )

    # 8. Validate scores
    score_columns = ["FTHG", "FTAG", "HTHG", "HTAG"]

    if (df[score_columns] < 0).any().any():
        raise ValueError("Negative goal values detected.")

    if (df["HTHG"] > df["FTHG"]).any():
        raise ValueError("Half-time home goals exceed full-time goals.")

    if (df["HTAG"] > df["FTAG"]).any():
        raise ValueError("Half-time away goals exceed full-time goals.")

    # 9. Validate full-time result labels
    valid_results = {"H", "D", "A"}

    if not set(df["FTR"].dropna().unique()).issubset(valid_results):
        raise ValueError("Unexpected full-time result values.")

    # 10. Check duplicate fixtures
    duplicate_count = df.duplicated(
        subset=["Date", "HomeTeam", "AwayTeam"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate fixtures."
        )

    # 11. Sort chronologically
    df = df.sort_values(
        by=["Date", "Time"],
        na_position="last"
    ).reset_index(drop=True)

    # 12. Export cleaned dataset
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_PATH, index=False)

    # 13. Summary
    print("\nCLEANING COMPLETED")
    print("-" * 55)
    print(f"Original columns: 120")
    print(f"Retained columns: {len(df.columns)}")
    print(f"Matches retained: {len(df)}")
    print(f"Duplicate fixtures: {duplicate_count}")
    print(f"Missing essential values: 0")
    print(f"Output: {OUTPUT_PATH}")

    print("\nDate range:")
    print(df["Date"].min(), "to", df["Date"].max())

    print("\nResult distribution:")
    print(df["FTR"].value_counts())

    print("\nMissing values in cleaned dataset:")
    print(df.isna().sum()[df.isna().sum() > 0])


if __name__ == "__main__":
    clean_dataset()
