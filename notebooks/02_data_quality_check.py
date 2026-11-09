
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "DataCoSupplyChainDataset.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "data_quality_report.csv"

# Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Build data quality report
quality_report = pd.DataFrame({
    "Column": df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Missing_Values": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().mean().values * 100
    ).round(2),
    "Unique_Values": df.nunique(dropna=True).values
})

# Sort by missing percentage
quality_report = quality_report.sort_values(
    by="Missing_Percentage",
    ascending=False
)

# Save report
quality_report.to_csv(REPORT_PATH, index=False)

print("DATA QUALITY REPORT GENERATED")
print("-" * 50)
print(quality_report.to_string(index=False))
print(f"\nReport saved at: {REPORT_PATH}")
