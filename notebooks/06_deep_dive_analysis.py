
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"
REPORT_PATH = PROJECT_ROOT / "reports"

df = pd.read_csv(DATA_PATH)

df["order_date_dateorders"] = pd.to_datetime(
    df["order_date_dateorders"],
    errors="coerce"
)

print("=" * 60)
print("DEEP DIVE BUSINESS ANALYSIS")
print("=" * 60)

# 1. Actual late delivery rate by shipping mode
shipping_analysis = (
    df.groupby("shipping_mode")
    .agg(
        total_items=("order_item_id", "count"),
        actual_late_deliveries=(
            "delivery_status",
            lambda x: (x == "Late delivery").sum()
        ),
        risk_flagged_items=("late_delivery_risk", "sum"),
        average_actual_shipping_days=(
            "days_for_shipping_real", "mean"
        )
    )
)

shipping_analysis["actual_late_rate_pct"] = (
    shipping_analysis["actual_late_deliveries"]
    / shipping_analysis["total_items"] * 100
)

shipping_analysis["risk_flag_rate_pct"] = (
    shipping_analysis["risk_flagged_items"]
    / shipping_analysis["total_items"] * 100
)

print("\n1. ACTUAL LATE DELIVERY VS RISK FLAG")
print(shipping_analysis.round(2).to_string())

shipping_analysis.to_csv(
    REPORT_PATH / "shipping_deep_dive.csv"
)

# 2. Monthly record volume
df["order_month"] = (
    df["order_date_dateorders"]
    .dt.to_period("M")
    .astype(str)
)

monthly_analysis = (
    df.groupby("order_month")
    .agg(
        order_items=("order_item_id", "count"),
        unique_orders=("order_id", "nunique"),
        total_sales=("sales", "sum")
    )
)

print("\n2. MONTHLY DATA COVERAGE")
print(monthly_analysis.to_string())

monthly_analysis.to_csv(
    REPORT_PATH / "monthly_data_coverage.csv"
)

# 3. Order status analysis
order_status_analysis = (
    df.groupby("order_status")
    .agg(
        order_items=("order_item_id", "count"),
        unique_orders=("order_id", "nunique"),
        total_sales=("sales", "sum")
    )
    .sort_values("order_items", ascending=False)
)

print("\n3. ORDER STATUS ANALYSIS")
print(order_status_analysis.round(2).to_string())

order_status_analysis.to_csv(
    REPORT_PATH / "order_status_analysis.csv"
)

# 4. Profitability by market
market_profit = (
    df.groupby("market")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("order_profit_per_order", "sum"),
        average_profit_per_item=("order_profit_per_order", "mean")
    )
    .sort_values("total_profit", ascending=False)
)

print("\n4. PROFITABILITY BY MARKET")
print(market_profit.round(2).to_string())

market_profit.to_csv(
    REPORT_PATH / "profitability_by_market.csv"
)

print("\n" + "=" * 60)
print("DEEP DIVE ANALYSIS COMPLETED")
print("=" * 60)
