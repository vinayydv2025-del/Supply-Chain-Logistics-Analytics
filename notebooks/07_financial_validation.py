
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("FINANCIAL METRIC VALIDATION")
print("=" * 60)

# 1. Check whether order profit repeats across items
profit_consistency = (
    df.groupby("order_id")["order_profit_per_order"]
    .nunique()
)

print("\n1. ORDER PROFIT CONSISTENCY")
print(
    "Orders with multiple profit values:",
    (profit_consistency > 1).sum()
)
print(
    "Orders with one consistent profit value:",
    (profit_consistency == 1).sum()
)

# 2. Compare sales and order item totals
print("\n2. SALES VS ORDER ITEM TOTAL")
print(f"Total Sales: {df['sales'].sum():,.2f}")
print(f"Total Order Item Total: {df['order_item_total'].sum():,.2f}")
print(
    "Difference:",
    f"{df['sales'].sum() - df['order_item_total'].sum():,.2f}"
)

# 3. Check whether delivery risk matches actual delivery status
actual_late = (df["delivery_status"] == "Late delivery").astype(int)

print("\n3. DELIVERY RISK VALIDATION")
print(
    "Rows where risk flag matches actual late status:",
    (df["late_delivery_risk"] == actual_late).sum()
)
print(
    "Rows where they differ:",
    (df["late_delivery_risk"] != actual_late).sum()
)

# 4. Check order status consistency
status_consistency = (
    df.groupby("order_id")["order_status"]
    .nunique()
)

print("\n4. ORDER STATUS CONSISTENCY")
print(
    "Orders with multiple statuses:",
    (status_consistency > 1).sum()
)
print(
    "Orders with one consistent status:",
    (status_consistency == 1).sum()
)

print("\n" + "=" * 60)
print("FINANCIAL VALIDATION COMPLETED")
print("=" * 60)
