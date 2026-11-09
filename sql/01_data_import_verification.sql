--Total Records--
SELECT COUNT(*) AS total_rows
FROM supply_chain_orders;

--Unique Orders--
SELECT COUNT(DISTINCT order_id) AS unique_orders
FROM supply_chain_orders;

--Check Sample Records--
SELECT *
FROM supply_chain_orders
LIMIT 10;