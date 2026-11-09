
import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "DataCoSupplyChainDataset.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"

print("=" * 60)
print("SUPPLY CHAIN DATA CLEANING")
print("=" * 60)

# Load original dataset
df = pd.read_csv(DATA_PATH, encoding="latin1")

print(f"\nOriginal rows: {df.shape[0]:,}")
print(f"Original columns: {df.shape[1]}")

# 1. Remove unnecessary and personal information
columns_to_drop = [
    "Product Description",
    "Order Zipcode",
    "Customer Fname",
    "Customer Lname",
    "Customer Email",
    "Customer Password",
    "Customer Street",
    "Customer Zipcode",
    "Product Status",
    "Product Image"
]

df.drop(
    columns=columns_to_drop,
    errors="ignore",
    inplace=True
)

print("\nUnnecessary and personal columns removed.")

# 2. Convert date columns into proper datetime format
date_columns = [
    "order date (DateOrders)",
    "shipping date (DateOrders)"
]

for column in date_columns:
    df[column] = pd.to_datetime(
        df[column],
        format="%m/%d/%Y %H:%M",
        errors="coerce"
    )

print("\nDate columns converted.")

# 3. Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-zA-Z0-9]+", "_", regex=True)
    .str.strip("_")
)

# 4. Remove duplicate rows if any
duplicates = df.duplicated().sum()
df.drop_duplicates(inplace=True)

# 5. Check missing values after cleaning
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]

# 6. Save cleaned dataset
df.to_csv(OUTPUT_PATH, index=False)

# 7. Display cleaning summary
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)

print(f"Final rows: {df.shape[0]:,}")
print(f"Final columns: {df.shape[1]}")
print(f"Duplicate rows removed: {duplicates}")

print("\nRemaining missing values:")
if missing_values.empty:
    print("No missing values found.")
else:
    print(missing_values.to_string())

print(f"\nCleaned dataset saved at:\n{OUTPUT_PATH}")
print("\nDATA CLEANING COMPLETED SUCCESSFULLY.")
