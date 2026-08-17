-- ============================================
-- RetailPulse Analytics
-- ============================================


-- 1. Total Revenue

SELECT
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders;


-- 2. Revenue by Product

SELECT
    product_name,
    category,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY
    product_name,
    category
ORDER BY total_revenue DESC;


-- 3. Revenue by Category

SELECT
    category,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY category
ORDER BY total_revenue DESC;


-- 4. Revenue by City

SELECT
    city,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY city
ORDER BY total_revenue DESC;


-- 5. Top Customers

SELECT
    customer_id,
    customer_name,
    SUM(quantity * unit_price) AS total_spend
FROM silver_orders
GROUP BY
    customer_id,
    customer_name
ORDER BY total_spend DESC;