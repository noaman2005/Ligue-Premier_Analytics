
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "epl_2024_25.csv"

df = pd.read_csv(DATA_PATH)

# Convert dates from DD/MM/YYYY text into datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

print("\nDATA TYPES")
print("=" * 50)
print(df.dtypes.value_counts())

print("\nCOLUMN INFORMATION")
print("=" * 50)
print(df.info())

print("\nMATCH RESULT DISTRIBUTION")
print("=" * 50)
print(df["FTR"].value_counts())

print("\nUNIQUE TEAMS")
print("=" * 50)
print("Number of teams:", pd.concat([
    df["HomeTeam"],
    df["AwayTeam"]
]).nunique())

print("\nDATE RANGE")
print("=" * 50)
print("First match:", df["Date"].min())
print("Last match:", df["Date"].max())
print("Invalid dates:", df["Date"].isna().sum())
