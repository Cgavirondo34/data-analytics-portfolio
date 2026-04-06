-- =============================================================
-- SQL BUSINESS ANALYSIS — Sales & Customer KPI Queries
-- Dataset: Fictional e-commerce / retail company
-- Author: Carlos Gavirondo | Data Analytics Portfolio
-- =============================================================


-- =============================================================
-- 1. BASIC QUERIES — Overview of orders and products
-- =============================================================

-- Total number of orders per status
SELECT
    status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY status
ORDER BY total_orders DESC;


-- Top 10 best-selling products by quantity sold
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_name
ORDER BY units_sold DESC
LIMIT 10;


-- Revenue per product category
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- =============================================================
-- 2. JOINS — Customer and order enrichment
-- =============================================================

-- Full order details with customer information
SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    c.city,
    c.segment,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS order_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_date, c.customer_name, c.city, c.segment
ORDER BY o.order_date DESC;


-- Customers who have never placed an order (LEFT JOIN anti-pattern)
SELECT
    c.customer_id,
    c.customer_name,
    c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


-- =============================================================
-- 3. CTEs — Modular and readable queries
-- =============================================================

-- Monthly revenue with month-over-month comparison
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', o.order_date) AS month,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY DATE_TRUNC('month', o.order_date)
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
        2
    ) AS mom_growth_pct
FROM monthly_revenue
ORDER BY month;


-- Customer segmentation by lifetime value
WITH customer_ltv AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(DISTINCT o.order_id)          AS total_orders,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS lifetime_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT
    customer_id,
    customer_name,
    segment,
    total_orders,
    lifetime_value,
    CASE
        WHEN lifetime_value >= 10000 THEN 'VIP'
        WHEN lifetime_value >= 5000  THEN 'High Value'
        WHEN lifetime_value >= 1000  THEN 'Medium Value'
        ELSE 'Low Value'
    END AS ltv_tier
FROM customer_ltv
ORDER BY lifetime_value DESC;


-- =============================================================
-- 4. WINDOW FUNCTIONS — Rankings and running totals
-- =============================================================

-- Rank salespeople by revenue within each region
SELECT
    s.region,
    s.salesperson_name,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    RANK() OVER (
        PARTITION BY s.region
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC
    ) AS rank_in_region
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN salespeople s ON o.salesperson_id = s.salesperson_id
GROUP BY s.region, s.salesperson_name
ORDER BY s.region, rank_in_region;


-- Running cumulative revenue over time
SELECT
    DATE_TRUNC('month', o.order_date)           AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS monthly_revenue,
    ROUND(SUM(SUM(oi.quantity * oi.unit_price))
          OVER (ORDER BY DATE_TRUNC('month', o.order_date)), 2) AS cumulative_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;


-- Top 3 products per category by units sold
WITH product_sales AS (
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity) AS units_sold,
        ROW_NUMBER() OVER (
            PARTITION BY p.category
            ORDER BY SUM(oi.quantity) DESC
        ) AS rn
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT category, product_name, units_sold
FROM product_sales
WHERE rn <= 3
ORDER BY category, units_sold DESC;


-- =============================================================
-- 5. BUSINESS KPIs
-- =============================================================

-- KPI Summary: key business metrics for a given period
WITH period_data AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        oi.quantity * oi.unit_price AS line_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
      AND o.order_date BETWEEN '2024-01-01' AND '2024-12-31'
)
SELECT
    COUNT(DISTINCT order_id)                            AS total_orders,
    COUNT(DISTINCT customer_id)                         AS unique_customers,
    ROUND(SUM(line_revenue), 2)                         AS total_revenue,
    ROUND(AVG(line_revenue), 2)                         AS avg_order_value,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT customer_id), 2) AS avg_revenue_per_customer
FROM period_data;


-- Churn indicator: customers who bought in 2023 but not in 2024
WITH buyers_2023 AS (
    SELECT DISTINCT customer_id FROM orders
    WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
      AND status = 'completed'
),
buyers_2024 AS (
    SELECT DISTINCT customer_id FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
      AND status = 'completed'
)
SELECT
    b23.customer_id,
    c.customer_name,
    c.email
FROM buyers_2023 b23
LEFT JOIN buyers_2024 b24 ON b23.customer_id = b24.customer_id
JOIN customers c ON b23.customer_id = c.customer_id
WHERE b24.customer_id IS NULL
ORDER BY c.customer_name;
