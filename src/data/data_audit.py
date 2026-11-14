
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "epl_2024_25.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "data_quality_report.txt"

def audit_dataset():
    print("=" * 55)
    print("PREMIER LEAGUE DATA QUALITY AUDIT")
    print("=" * 55)

    # Load original dataset
    df = pd.read_csv(DATA_PATH)

    # Basic information
    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    # Duplicate checks
    exact_duplicates = df.duplicated().sum()

    fixture_columns = ["Date", "HomeTeam", "AwayTeam"]
    fixture_duplicates = df.duplicated(
        subset=fixture_columns
    ).sum()

    # Data types
    data_types = df.dtypes.astype(str)

    # Core column checks
    core_columns = [
        "Date", "HomeTeam", "AwayTeam",
        "FTHG", "FTAG", "FTR"
    ]

    missing_core_columns = [
        col for col in core_columns
        if col not in df.columns
    ]

    core_missing = (
        df[core_columns].isnull().sum()
        if not missing_core_columns
        else None
    )

    # Results
    report = []

    report.append("PREMIER LEAGUE DATA QUALITY REPORT")
    report.append("=" * 45)
    report.append(f"Total rows: {len(df)}")
    report.append(f"Total columns: {len(df.columns)}")
    report.append(f"Exact duplicate rows: {exact_duplicates}")
    report.append(f"Duplicate fixtures: {fixture_duplicates}")

    report.append("\nMISSING VALUES")
    report.append("-" * 45)

    if missing.empty:
        report.append("No missing values found.")
    else:
        for column, count in missing.items():
            percentage = count / len(df) * 100
            report.append(
                f"{column}: {count} ({percentage:.2f}%)"
            )

    report.append("\nDATA TYPES")
    report.append("-" * 45)

    for column, dtype in data_types.items():
        report.append(f"{column}: {dtype}")

    report.append("\nCORE COLUMN CHECK")
    report.append("-" * 45)

    if missing_core_columns:
        report.append(
            f"Missing columns: {missing_core_columns}"
        )
    else:
        for column, count in core_missing.items():
            report.append(f"{column}: {count} missing")

    report.append("\nNUMERIC SUMMARY")
    report.append("-" * 45)
    report.append(str(df.describe().round(2)))

    # Save report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nAudit completed.")
    print(f"Report saved to: {REPORT_PATH}")

    print("\nMISSING VALUES:")
    print(missing)

    print("\nDUPLICATES:")
    print(f"Exact rows: {exact_duplicates}")
    print(f"Fixtures: {fixture_duplicates}")


if __name__ == "__main__":
    audit_dataset()
