"""
Python ETL Automation — Sales Report Pipeline
==============================================
Reads raw sales data from CSV, cleanses and transforms it,
calculates key business KPIs, and exports a processed report.

Author : Carlos Gavirondo | Data Analytics Portfolio
Python : 3.10+
"""

import os
import logging
from pathlib import Path

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR       = Path(__file__).resolve().parent.parent
RAW_DATA_PATH  = BASE_DIR / "data" / "raw"   / "sales_raw.csv"
OUT_DATA_PATH  = BASE_DIR / "data" / "processed" / "sales_report.csv"
KPI_OUT_PATH   = BASE_DIR / "data" / "processed" / "kpi_summary.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Step 1 — Extract: load raw data
# ---------------------------------------------------------------------------

def load_data(path: Path) -> pd.DataFrame:
    """Read CSV file and return a raw DataFrame."""
    log.info("Loading data from: %s", path)
    if not path.exists():
        log.warning("File not found — generating synthetic sample data.")
        return _generate_sample_data()
    df = pd.read_csv(path, parse_dates=["order_date"])
    log.info("Loaded %d rows, %d columns.", len(df), len(df.columns))
    return df


def _generate_sample_data() -> pd.DataFrame:
    """Create a reproducible synthetic sales dataset for demonstration."""
    np.random.seed(42)
    n = 500

    categories = ["Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Sports"]
    regions    = ["North", "South", "East", "West", "Central"]
    statuses   = ["completed", "completed", "completed", "returned", "pending"]

    return pd.DataFrame({
        "order_id"    : range(1001, 1001 + n),
        "order_date"  : pd.date_range("2024-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
        "customer_id" : np.random.randint(1, 101, n),
        "product_id"  : np.random.randint(1, 51, n),
        "category"    : np.random.choice(categories, n),
        "region"      : np.random.choice(regions, n),
        "quantity"    : np.random.randint(1, 20, n),
        "unit_price"  : np.round(np.random.uniform(5, 500, n), 2),
        "discount"    : np.round(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], n), 2),
        "status"      : np.random.choice(statuses, n, p=[0.6, 0.15, 0.1, 0.1, 0.05]),
    })


# ---------------------------------------------------------------------------
# Step 2 — Transform: cleanse and enrich
# ---------------------------------------------------------------------------

def cleanse_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates, fix types, handle nulls."""
    log.info("Cleansing data...")
    initial_rows = len(df)

    # Ensure date column is datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Drop rows with null critical fields
    critical_cols = ["order_id", "order_date", "customer_id", "quantity", "unit_price"]
    df = df.dropna(subset=critical_cols)

    # Remove duplicate order lines
    df = df.drop_duplicates(subset=["order_id"])

    # Clamp negatives to zero
    df["quantity"]   = df["quantity"].clip(lower=0)
    df["unit_price"] = df["unit_price"].clip(lower=0)
    df["discount"]   = df["discount"].fillna(0).clip(lower=0, upper=1)

    # Standardise string columns
    for col in ["category", "region", "status"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    log.info(
        "Cleansing complete: %d → %d rows (removed %d).",
        initial_rows, len(df), initial_rows - len(df),
    )
    return df.reset_index(drop=True)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns and business metrics."""
    log.info("Transforming data...")

    # Revenue calculations
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["discount_amount"] = df["gross_revenue"] * df["discount"]
    df["net_revenue"]   = df["gross_revenue"] - df["discount_amount"]

    # Date features
    df["year"]    = df["order_date"].dt.year
    df["month"]   = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter
    df["week"]    = df["order_date"].dt.isocalendar().week.astype(int)

    # Flag high-value orders (top 20% by net revenue)
    threshold = df["net_revenue"].quantile(0.80)
    df["is_high_value"] = df["net_revenue"] >= threshold

    log.info("Transformation complete. New columns: gross_revenue, net_revenue, year, month, quarter, week, is_high_value")
    return df


# ---------------------------------------------------------------------------
# Step 3 — Aggregate: compute business KPIs
# ---------------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Build a KPI summary by month and category."""
    log.info("Computing KPIs...")

    completed = df[df["status"] == "Completed"].copy()

    kpis = (
        completed
        .groupby(["year", "month", "category"])
        .agg(
            total_orders      =("order_id",    "count"),
            unique_customers  =("customer_id", "nunique"),
            units_sold        =("quantity",     "sum"),
            gross_revenue     =("gross_revenue","sum"),
            discount_total    =("discount_amount","sum"),
            net_revenue       =("net_revenue",  "sum"),
        )
        .reset_index()
    )

    # Average order value
    kpis["avg_order_value"] = np.where(
        kpis["total_orders"] > 0,
        kpis["net_revenue"] / kpis["total_orders"],
        0,
    )

    # Round monetary columns
    money_cols = ["gross_revenue", "discount_total", "net_revenue", "avg_order_value"]
    kpis[money_cols] = kpis[money_cols].round(2)

    log.info("KPI table: %d rows.", len(kpis))
    return kpis


# ---------------------------------------------------------------------------
# Step 4 — Load: export results
# ---------------------------------------------------------------------------

def export_data(df: pd.DataFrame, path: Path, label: str = "data") -> None:
    """Save DataFrame to CSV, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    log.info("Exported %s → %s  (%d rows)", label, path, len(df))


# ---------------------------------------------------------------------------
# Pipeline orchestrator
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    """Execute the full ETL pipeline end-to-end."""
    log.info("=" * 60)
    log.info("  Sales ETL Pipeline — START")
    log.info("=" * 60)

    # Extract
    raw_df = load_data(RAW_DATA_PATH)

    # Transform
    clean_df     = cleanse_data(raw_df)
    enriched_df  = transform_data(clean_df)

    # Aggregate
    kpi_df = compute_kpis(enriched_df)

    # Load
    export_data(enriched_df, OUT_DATA_PATH, label="processed sales")
    export_data(kpi_df,      KPI_OUT_PATH,  label="KPI summary")

    # Console summary
    log.info("-" * 60)
    log.info("Pipeline complete. Summary:")
    log.info("  Total rows processed : %d",   len(enriched_df))
    log.info("  Completed orders     : %d",   len(enriched_df[enriched_df["status"] == "Completed"]))
    log.info("  Total net revenue    : %.2f", enriched_df.loc[enriched_df["status"] == "Completed", "net_revenue"].sum())
    log.info("  KPI table rows       : %d",   len(kpi_df))
    log.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()
