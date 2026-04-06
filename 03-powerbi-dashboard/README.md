# 📊 Power BI Sales Dashboard

## Project Overview

This dashboard was designed to give **commercial leaders** a single source of truth for sales performance. It replaces a fragmented set of weekly Excel reports and provides real-time visibility into revenue, customer behaviour, and product performance.

---

## Business Objective

> *"We need to understand where we are versus target, which products are growing, and which customers are at risk — all in one place, updated daily."*

**Primary audience:** Sales Director, Regional Managers, Commercial Analysts

---

## Data Sources

| Source | Connection |
|---|---|
| Sales transactions | SQL Server (DirectQuery) |
| Customer master data | Excel flat file (import) |
| Budget / target data | Excel flat file (import) |
| Product catalog | SQL Server (import) |

---

## Data Model

The report uses a **star schema** with:

- **Fact table:** `fact_sales` — one row per order line
- **Dimension tables:** `dim_customer`, `dim_product`, `dim_date`, `dim_salesperson`, `dim_region`

Relationships are all one-to-many, single-direction filters.

---

## DAX Measures

| Measure | Formula Logic |
|---|---|
| `Total Revenue` | SUM of net revenue on completed orders |
| `Revenue YoY %` | Comparison vs same period prior year using `SAMEPERIODLASTYEAR` |
| `% vs Target` | Actual revenue divided by budget target |
| `Avg Order Value` | Total Revenue / Count of distinct orders |
| `Customer Count` | DISTINCTCOUNT of customer IDs |
| `Churn Rate` | Customers active LY but not TY / Total LY customers |
| `Top N Products` | RANKX over product revenue with dynamic N filter |

---

## Report Pages

### Page 1 — Executive Summary
- KPI cards: Revenue, Orders, AOV, Customers, % vs Target
- Revenue trend line (monthly, with budget overlay)
- Revenue by region (map visual)
- Top 5 products (bar chart)

### Page 2 — Sales Detail
- Matrix: Salesperson × Month with conditional formatting
- Drill-through to individual order list
- Slicer: Region, Category, Date range

### Page 3 — Customer Analysis
- Customer count over time
- LTV distribution (histogram)
- New vs returning customer trend
- Churn flag table

### Page 4 — Product Performance
- Revenue and units sold by category (stacked bar)
- Product scatter: Revenue vs Margin
- Top / Bottom 10 products toggle

---

## Key Insights Delivered

1. **Electronics** drives 42% of revenue but has the highest return rate — margin risk to investigate.
2. **West region** consistently underperforms vs target by 15%+ — flagged for action plan.
3. **Top 100 customers** represent 68% of total revenue — concentration risk identified.
4. Month-over-month growth slowed in Q3 — correlated with a price increase on key SKUs.

---

## Screenshots

> *(Dashboard screenshots are stored in the `screenshots/` folder)*

| File | Description |
|---|---|
| `executive_summary.png` | Executive KPI page |
| `sales_detail.png` | Salesperson performance matrix |
| `customer_analysis.png` | Customer segmentation view |
| `product_performance.png` | Product scatter and rankings |

---

## Skills Demonstrated

- ✅ Star schema data modelling in Power BI
- ✅ DAX: time intelligence, RANKX, dynamic measures
- ✅ Report design: layout, UX, conditional formatting
- ✅ Multi-source data integration (SQL + Excel)
- ✅ Business storytelling through data visualisation
