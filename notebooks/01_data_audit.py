
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "DataCoSupplyChainDataset.csv"

print("=" * 60)
print("SUPPLY CHAIN DATASET AUDIT")
print("=" * 60)

# Load dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

# 1. Dataset dimensions
print("\n1. DATASET DIMENSIONS")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]:,}")

# 2. Column names and data types
print("\n2. COLUMN NAMES AND DATA TYPES")
print(df.dtypes.to_string())

# 3. First five rows
print("\n3. FIRST FIVE ROWS")
print(df.head().to_string())

# 4. Missing values
print("\n4. MISSING VALUES")
missing = df.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("No missing values found.")
else:
    print(missing.to_string())

# 5. Duplicate records
print("\n5. DUPLICATE RECORDS")
print(f"Duplicate rows: {df.duplicated().sum():,}")

# 6. Numerical summary
print("\n6. NUMERICAL SUMMARY")
print(df.describe().to_string())

# 7. Categorical summary
print("\n7. CATEGORICAL SUMMARY")
print(df.describe(include="object").to_string())

# 8. Save basic audit information
audit_path = PROJECT_ROOT / "reports" / "dataset_audit_summary.txt"

with open(audit_path, "w", encoding="utf-8") as file:
    file.write("SUPPLY CHAIN DATASET AUDIT\n")
    file.write(f"Rows: {df.shape[0]}\n")
    file.write(f"Columns: {df.shape[1]}\n")
    file.write(f"Duplicate rows: {df.duplicated().sum()}\n")
    file.write("\nMissing Values:\n")
    file.write(missing.to_string())

print("\nAudit summary saved successfully.")
