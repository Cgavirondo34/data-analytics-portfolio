# Raw Data

This folder contains raw, unprocessed input files used by the ETL pipeline.

Files placed here are read by `02-python-automation/main.py` during the Extract phase.

## Expected format: `sales_raw.csv`

| Column | Type | Description |
|---|---|---|
| `order_id` | integer | Unique order identifier |
| `order_date` | date (YYYY-MM-DD) | Date the order was placed |
| `customer_id` | integer | Customer identifier |
| `product_id` | integer | Product identifier |
| `category` | string | Product category |
| `region` | string | Sales region |
| `quantity` | integer | Units ordered |
| `unit_price` | decimal | Price per unit |
| `discount` | decimal (0–1) | Discount rate applied |
| `status` | string | Order status (completed/returned/pending) |

> If this file is absent, the pipeline generates a synthetic 500-row sample automatically.
