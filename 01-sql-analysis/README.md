# 🗄️ SQL Business Analysis

## Business Context

This project simulates a **retail / e-commerce** analytics scenario. The data model includes:

- `customers` — customer master data (id, name, email, city, segment)
- `orders` — transaction header (id, date, status, salesperson)
- `order_items` — line items (product, quantity, unit price)
- `products` — product catalog (id, name, category)
- `salespeople` — sales rep data (id, name, region)

The goal is to answer real business questions that a Data Analyst would face in a commercial team:

> *"Which products are driving the most revenue?"*
> *"Who are our highest-value customers?"*
> *"Are we growing month-over-month?"*
> *"Which customers churned this year?"*

---

## Queries Overview

| # | Query | Technique |
|---|---|---|
| 1 | Orders by status | Basic aggregation |
| 2 | Top 10 products by units sold | GROUP BY + ORDER BY |
| 3 | Revenue by category | JOIN + aggregation |
| 4 | Full order detail with customer info | Multi-table JOIN |
| 5 | Customers with no orders | LEFT JOIN anti-pattern |
| 6 | Month-over-month revenue growth | CTE + LAG window function |
| 7 | Customer LTV segmentation | CTE + CASE WHEN |
| 8 | Salespeople ranked by region | RANK() OVER PARTITION |
| 9 | Cumulative revenue over time | SUM() OVER running total |
| 10 | Top 3 products per category | ROW_NUMBER() + CTE |
| 11 | Annual KPI summary | Compound aggregation |
| 12 | Churned customer detection | Multi-CTE + anti-join |

---

## Key Skills Demonstrated

- ✅ CTEs for modular, readable query design
- ✅ Window functions: `RANK()`, `ROW_NUMBER()`, `LAG()`, running totals
- ✅ Multi-table JOINs with business context
- ✅ KPI design: revenue, LTV, AOV, churn
- ✅ Anti-join pattern for gap analysis
- ✅ Date-based filtering for period comparisons

---

## How to Run

These queries are written in **standard SQL** compatible with PostgreSQL and SQL Server (minor syntax adjustments may be needed for MySQL).

You can test them by:
1. Creating the tables in your local PostgreSQL instance
2. Loading sample data (see `../data/raw/` folder)
3. Running `queries.sql` in pgAdmin, DBeaver, or any SQL client
