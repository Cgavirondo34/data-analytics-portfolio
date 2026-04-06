# 🐍 Python ETL Automation — Sales Report Pipeline

## Overview

This project automates a common Data Analyst workflow:

> *Raw CSV data → Cleanse → Transform → Aggregate KPIs → Export clean report*

It simulates the kind of script you would schedule to run daily/weekly to refresh a sales dashboard or feed a BI tool.

---

## Pipeline Architecture

```
data/raw/sales_raw.csv
        │
        ▼
  [ 1. Extract ]   — Read CSV with pandas
        │
        ▼
  [ 2. Cleanse ]   — Drop duplicates, fix types, handle nulls
        │
        ▼
  [ 3. Transform ] — Derive revenue columns, date features, high-value flag
        │
        ▼
  [ 4. Aggregate ] — Compute monthly KPIs by category
        │
        ▼
  data/processed/sales_report.csv
  data/processed/kpi_summary.csv
```

---

## Transformations Applied

| Step | Action |
|---|---|
| Cleanse | Remove duplicate order IDs |
| Cleanse | Drop rows with null critical fields |
| Cleanse | Clip negative quantities and prices |
| Cleanse | Standardise string columns (title case) |
| Transform | Calculate `gross_revenue = quantity × unit_price` |
| Transform | Calculate `discount_amount` and `net_revenue` |
| Transform | Extract year, month, quarter, week from order date |
| Transform | Flag top 20% orders as `is_high_value` |
| Aggregate | Group by year/month/category → KPI table |

---

## KPIs Computed

| KPI | Description |
|---|---|
| `total_orders` | Number of completed orders |
| `unique_customers` | Distinct customer count |
| `units_sold` | Total quantity sold |
| `gross_revenue` | Revenue before discounts |
| `discount_total` | Total discount given |
| `net_revenue` | Revenue after discounts |
| `avg_order_value` | Net revenue per order |

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python main.py
```

If `data/raw/sales_raw.csv` does not exist, the script automatically generates a **synthetic 500-row dataset** for demonstration.

---

## Sample Output (Console)

```
2024-01-15 09:00:00  [INFO]  Loading data from: data/raw/sales_raw.csv
2024-01-15 09:00:00  [INFO]  Generated synthetic sample data.
2024-01-15 09:00:00  [INFO]  Cleansing: 500 → 497 rows (removed 3)
2024-01-15 09:00:00  [INFO]  Transformation complete.
2024-01-15 09:00:00  [INFO]  KPI table: 60 rows.
2024-01-15 09:00:00  [INFO]  Exported processed sales → data/processed/sales_report.csv
2024-01-15 09:00:00  [INFO]  Exported KPI summary   → data/processed/kpi_summary.csv
2024-01-15 09:00:00  [INFO]  Total net revenue: 312,540.87
```

---

## Skills Demonstrated

- ✅ Clean, modular Python code (functions with single responsibility)
- ✅ Defensive data cleansing (nulls, duplicates, type coercion)
- ✅ Business-driven transformations (not just technical)
- ✅ Logging with timestamps for pipeline observability
- ✅ Synthetic data generation for reproducible demos
- ✅ Path handling with `pathlib` for cross-platform compatibility
