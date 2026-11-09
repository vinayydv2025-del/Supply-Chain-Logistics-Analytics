
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "supply_chain_cleaned.csv"
)

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("CLEANED DATASET VERIFICATION")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDate Column Data Types:")
print(df[[
    "order_date_dateorders",
    "shipping_date_dateorders"
]].dtypes)

print("\nFirst Five Records:")
print(df.head().to_string())

print("\nVERIFICATION COMPLETED.")
