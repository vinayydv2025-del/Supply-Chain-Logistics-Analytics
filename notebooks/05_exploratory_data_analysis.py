
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "supply_chain_cleaned.csv"
FIGURES_PATH = PROJECT_ROOT / "reports" / "figures"

FIGURES_PATH.mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(DATA_PATH)

# Convert dates back to datetime
df["order_date_dateorders"] = pd.to_datetime(
    df["order_date_dateorders"],
    errors="coerce"
)

df["shipping_date_dateorders"] = pd.to_datetime(
    df["shipping_date_dateorders"],
    errors="coerce"
)

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# 1. Basic information
print("\n1. DATASET OVERVIEW")
print(f"Total records: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print(f"Order date range: {df['order_date_dateorders'].min()} to {df['order_date_dateorders'].max()}")

# 2. Overall sales performance
print("\n2. OVERALL SALES PERFORMANCE")
print(f"Total sales: {df['sales'].sum():,.2f}")
print(f"Average sales per order item: {df['sales'].mean():,.2f}")
print(f"Total quantity sold: {df['order_item_quantity'].sum():,}")
print(f"Unique orders: {df['order_id'].nunique():,}")
print(f"Unique products: {df['product_name'].nunique():,}")

# 3. Sales by market
market_sales = (
    df.groupby("market")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n3. SALES BY MARKET")
print(market_sales.to_string())

market_sales.to_csv(
    PROJECT_ROOT / "reports" / "sales_by_market.csv"
)

# 4. Sales by product category
category_sales = (
    df.groupby("category_name")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n4. TOP 10 PRODUCT CATEGORIES BY SALES")
print(category_sales.head(10).to_string())

category_sales.to_csv(
    PROJECT_ROOT / "reports" / "sales_by_category.csv"
)

# 5. Shipping performance
shipping_performance = (
    df.groupby("shipping_mode")
    .agg(
        total_order_items=("order_item_id", "count"),
        average_shipping_days=("days_for_shipping_real", "mean"),
        late_delivery_rate=("late_delivery_risk", "mean")
    )
    .sort_values("late_delivery_rate", ascending=False)
)

shipping_performance["late_delivery_rate"] *= 100

print("\n5. SHIPPING PERFORMANCE")
print(shipping_performance.round(2).to_string())

shipping_performance.to_csv(
    PROJECT_ROOT / "reports" / "shipping_performance.csv"
)

# 6. Delivery status distribution
delivery_distribution = (
    df["delivery_status"]
    .value_counts()
)

print("\n6. DELIVERY STATUS DISTRIBUTION")
print(delivery_distribution.to_string())

delivery_distribution.to_csv(
    PROJECT_ROOT / "reports" / "delivery_status_distribution.csv"
)

# 7. Monthly sales trend
df["order_month"] = (
    df["order_date_dateorders"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    df.groupby("order_month")["sales"]
    .sum()
    .sort_index()
)

print("\n7. MONTHLY SALES TREND")
print(monthly_sales.to_string())

monthly_sales.to_csv(
    PROJECT_ROOT / "reports" / "monthly_sales.csv"
)

# 8. Generate charts

# Chart 1: Monthly sales trend
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURES_PATH / "monthly_sales_trend.png", dpi=300)
plt.close()

# Chart 2: Sales by market
plt.figure(figsize=(10, 6))
market_sales.plot(kind="bar")
plt.title("Sales by Market")
plt.xlabel("Market")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIGURES_PATH / "sales_by_market.png", dpi=300)
plt.close()

# Chart 3: Top 10 product categories
plt.figure(figsize=(12, 6))
category_sales.head(10).sort_values().plot(kind="barh")
plt.title("Top 10 Product Categories by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig(FIGURES_PATH / "top_categories_by_sales.png", dpi=300)
plt.close()

# Chart 4: Delivery status distribution
plt.figure(figsize=(9, 6))
delivery_distribution.plot(kind="bar")
plt.title("Delivery Status Distribution")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Order Items")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(FIGURES_PATH / "delivery_status_distribution.png", dpi=300)
plt.close()

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print(f"Charts saved in: {FIGURES_PATH}")
print("=" * 60)
