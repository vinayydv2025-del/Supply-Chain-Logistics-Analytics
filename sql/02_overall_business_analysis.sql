USE supply_chain_analytics;

-- ==========================================
-- 1. OVERALL BUSINESS OVERVIEW
-- ==========================================

-- Total number of order items
SELECT COUNT(*) AS total_order_items
FROM supply_chain_orders;

-- Total unique orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM supply_chain_orders;

-- Total unique customers
SELECT COUNT(DISTINCT customer_id) AS total_customers
FROM supply_chain_orders;

-- Total unique products
SELECT COUNT(DISTINCT product_card_id) AS total_products
FROM supply_chain_orders;

-- Total gross sales
SELECT ROUND(SUM(sales), 2) AS total_gross_sales
FROM supply_chain_orders;

-- Total quantity sold
SELECT SUM(order_item_quantity) AS total_quantity_sold
FROM supply_chain_orders;

-- ==========================================
-- 2. SALES PERFORMANCE ANALYSIS
-- ==========================================

-- 1. Total sales by market
SELECT
    market,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY market
ORDER BY total_sales DESC;


-- 2. Sales by customer segment
SELECT
    customer_segment,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY customer_segment
ORDER BY total_sales DESC;


-- 3. Top 10 product categories by sales
SELECT
    category_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY category_name
ORDER BY total_sales DESC
LIMIT 10;


-- 4. Top 10 products by sales
SELECT
    product_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;


-- 5. Average order-item sales value
SELECT
    ROUND(AVG(sales), 2) AS average_item_sales
FROM supply_chain_orders;


-- 6. Monthly sales trend
SELECT
    DATE_FORMAT(
        STR_TO_DATE(order_date_dateorders, '%Y-%m-%d %H:%i:%s'),
        '%Y-%m'
    ) AS sales_month,
    ROUND(SUM(sales), 2) AS monthly_sales
FROM supply_chain_orders
GROUP BY sales_month
ORDER BY sales_month;

-- ==========================================
-- 3. DELIVERY AND LOGISTICS PERFORMANCE
-- ==========================================

-- 1. Overall delivery status distribution
SELECT
    delivery_status,
    COUNT(*) AS total_order_items,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM supply_chain_orders),
        2
    ) AS percentage
FROM supply_chain_orders
GROUP BY delivery_status
ORDER BY total_order_items DESC;


-- 2. Late delivery percentage by shipping mode
SELECT
    shipping_mode,
    COUNT(*) AS total_order_items,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_deliveries,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage
FROM supply_chain_orders
GROUP BY shipping_mode
ORDER BY late_delivery_percentage DESC;


-- 3. Average actual shipping days by shipping mode
SELECT
    shipping_mode,
    ROUND(AVG(days_for_shipping_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days
FROM supply_chain_orders
GROUP BY shipping_mode
ORDER BY avg_actual_shipping_days DESC;

-- ==========================================
-- 4. PRODUCT AND CATEGORY ANALYSIS
-- ==========================================

-- 1. Top 10 categories by gross sales
SELECT
    category_name,
    ROUND(SUM(sales), 2) AS total_sales,
    SUM(order_item_quantity) AS total_quantity
FROM supply_chain_orders
GROUP BY category_name
ORDER BY total_sales DESC
LIMIT 10;


-- 2. Top 10 products by gross sales
SELECT
    product_name,
    ROUND(SUM(sales), 2) AS total_sales,
    SUM(order_item_quantity) AS total_quantity
FROM supply_chain_orders
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;


-- 3. Product category performance
SELECT
    category_name,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(sales), 2) AS avg_item_sales,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY category_name
ORDER BY total_sales DESC;

-- ==========================================
-- 5. CUSTOMER SEGMENT ANALYSIS
-- ==========================================

-- 1. Gross sales by customer segment

SELECT
    customer_segment,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY customer_segment
ORDER BY total_sales DESC;

-- 2. Average gross sales per customer by segment

SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(
        SUM(sales) / COUNT(DISTINCT customer_id), 2
    ) AS average_sales_per_customer
FROM supply_chain_orders
GROUP BY customer_segment
ORDER BY average_sales_per_customer DESC;

-- 3. Top 10 customers by gross sales

SELECT
    customer_id,
    customer_segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales
FROM supply_chain_orders
GROUP BY customer_id, customer_segment
ORDER BY total_sales DESC
LIMIT 10;

-- 4. Repeat customer analysis

SELECT
    CASE
        WHEN customer_orders = 1 THEN 'One-time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS total_customers
FROM (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS customer_orders
    FROM supply_chain_orders
    GROUP BY customer_id
) AS customer_summary
GROUP BY customer_type;

-- 5. Average orders per customer

SELECT
    ROUND(AVG(customer_orders), 2) AS avg_orders_per_customer,
    MAX(customer_orders) AS max_orders_by_customer,
    MIN(customer_orders) AS min_orders_by_customer
FROM (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS customer_orders
    FROM supply_chain_orders
    GROUP BY customer_id
) AS customer_summary;

-- ==========================================
-- 6. ORDER STATUS ANALYSIS
-- ==========================================

-- 1. Order status distribution

SELECT
    order_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        COUNT(DISTINCT order_id) * 100.0 /
        (SELECT COUNT(DISTINCT order_id) FROM supply_chain_orders),
        2
    ) AS percentage
FROM supply_chain_orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 2. Order status by market

SELECT
    market,
    order_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM supply_chain_orders
GROUP BY market, order_status
ORDER BY market, total_orders DESC;

-- 3. Canceled orders by market

SELECT
    market,
    COUNT(DISTINCT order_id) AS canceled_orders
FROM supply_chain_orders
WHERE order_status = 'CANCELED'
GROUP BY market
ORDER BY canceled_orders DESC;

-- 4. Suspected fraud orders by market

SELECT
    market,
    COUNT(DISTINCT order_id) AS suspected_fraud_orders
FROM supply_chain_orders
WHERE order_status = 'SUSPECTED_FRAUD'
GROUP BY market
ORDER BY suspected_fraud_orders DESC;

-- 5. Overall order status summary

SELECT
    order_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS gross_sales
FROM supply_chain_orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- 6. Order status by customer segment

SELECT
    customer_segment,
    order_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM supply_chain_orders
GROUP BY customer_segment, order_status
ORDER BY customer_segment, total_orders DESC;

-- ===============================================
-- 7. SHIPPING DELAY AND DELIVERY TIME ANALYSIS
-- ===============================================

-- 1. Average actual vs scheduled shipping days

SELECT
    shipping_mode,
    ROUND(AVG(days_for_shipping_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days,
    ROUND(
        AVG(days_for_shipping_real - days_for_shipment_scheduled), 2
    ) AS avg_shipping_delay
FROM supply_chain_orders
GROUP BY shipping_mode
ORDER BY avg_shipping_delay DESC;

-- 2. Late delivery percentage by market

SELECT
    market,
    COUNT(*) AS total_order_items,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_order_items,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*), 2
    ) AS late_delivery_percentage
FROM supply_chain_orders
GROUP BY market
ORDER BY late_delivery_percentage DESC;

-- 3. Late delivery percentage by region

SELECT
    order_region,
    COUNT(*) AS total_order_items,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_order_items,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*), 2
    ) AS late_delivery_percentage
FROM supply_chain_orders
GROUP BY order_region
ORDER BY late_delivery_percentage DESC;

-- 4. Late delivery percentage by customer segment

SELECT
    customer_segment,
    COUNT(*) AS total_order_items,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_order_items,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*), 2
    ) AS late_delivery_percentage
FROM supply_chain_orders
GROUP BY customer_segment
ORDER BY late_delivery_percentage DESC;

-- 5. Average delivery time by market

SELECT
    market,
    ROUND(AVG(days_for_shipping_real), 2) AS avg_actual_shipping_days,
    ROUND(AVG(days_for_shipment_scheduled), 2) AS avg_scheduled_shipping_days
FROM supply_chain_orders
GROUP BY market
ORDER BY avg_actual_shipping_days DESC;

-- 6. Shipping delay distribution

SELECT
    CASE
        WHEN days_for_shipping_real < days_for_shipment_scheduled
            THEN 'Early Delivery'
        WHEN days_for_shipping_real = days_for_shipment_scheduled
            THEN 'On Schedule'
        ELSE 'Delayed Delivery'
    END AS shipping_performance,
    COUNT(*) AS total_order_items,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM supply_chain_orders), 2
    ) AS percentage
FROM supply_chain_orders
GROUP BY shipping_performance
ORDER BY total_order_items DESC;

-- 7. Top 10 regions by late delivery volume

SELECT
    order_region,
    COUNT(*) AS late_order_items
FROM supply_chain_orders
WHERE delivery_status = 'Late delivery'
GROUP BY order_region
ORDER BY late_order_items DESC
LIMIT 10;

-- 8. Late deliveries by shipping mode

SELECT
    shipping_mode,
    COUNT(*) AS total_order_items,
    SUM(CASE
        WHEN delivery_status = 'Late delivery' THEN 1
        ELSE 0
    END) AS late_order_items,
    ROUND(
        SUM(CASE
            WHEN delivery_status = 'Late delivery' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*), 2
    ) AS late_delivery_percentage
FROM supply_chain_orders
GROUP BY shipping_mode
ORDER BY late_delivery_percentage DESC;

-- ===============================================
-- 8. PROFITABILITY ANALYSIS
-- ===============================================

-- 1. Average profit ratio by market

SELECT
    market,
    ROUND(AVG(order_item_profit_ratio), 4) AS avg_profit_ratio,
    ROUND(AVG(benefit_per_order), 2) AS avg_recorded_benefit
FROM supply_chain_orders
GROUP BY market
ORDER BY avg_profit_ratio DESC;

-- 2. Average profit ratio by product category

SELECT
    category_name,
    ROUND(AVG(order_item_profit_ratio), 4) AS avg_profit_ratio,
    ROUND(AVG(benefit_per_order), 2) AS avg_recorded_benefit
FROM supply_chain_orders
GROUP BY category_name
ORDER BY avg_profit_ratio DESC
LIMIT 15;

-- 3. Average profit ratio by customer segment

SELECT
    customer_segment,
    ROUND(AVG(order_item_profit_ratio), 4) AS avg_profit_ratio,
    ROUND(AVG(benefit_per_order), 2) AS avg_recorded_benefit
FROM supply_chain_orders
GROUP BY customer_segment
ORDER BY avg_profit_ratio DESC;


