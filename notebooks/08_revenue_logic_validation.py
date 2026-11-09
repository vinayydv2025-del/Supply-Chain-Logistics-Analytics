
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("REVENUE AND DISCOUNT VALIDATION")
print("=" * 60)

# Candidate calculations
gross_candidate = (
    df["order_item_product_price"] *
    df["order_item_quantity"]
)

net_candidate = (
    gross_candidate - df["order_item_discount"]
)

discount_candidate = df["sales"] - df["order_item_total"]

def show_comparison(label, actual, calculated):
    difference = (actual - calculated).abs()

    print(f"\n{label}")
    print(f"Exact matches: {(difference < 0.01).sum():,}")
    print(f"Non-matches: {(difference >= 0.01).sum():,}")
    print(f"Average absolute difference: {difference.mean():.4f}")

show_comparison(
    "1. SALES VS PRODUCT PRICE",
    df["sales"],
    df["order_item_product_price"]
)

show_comparison(
    "2. SALES VS PRICE MULTIPLIED BY QUANTITY",
    df["sales"],
    gross_candidate
)

show_comparison(
    "3. ORDER ITEM TOTAL VS GROSS SALES MINUS DISCOUNT",
    df["order_item_total"],
    net_candidate
)

print("\n4. DISCOUNT SUMMARY")
print(f"Total recorded discount: {df['order_item_discount'].sum():,.2f}")
print(f"Sales minus order item total: {discount_candidate.sum():,.2f}")

show_comparison(
    "5. ORDER PROFIT VS BENEFIT PER ORDER",
    df["order_profit_per_order"],
    df["benefit_per_order"]
)

print("\n" + "=" * 60)
print("REVENUE VALIDATION COMPLETED")
print("=" * 60)
