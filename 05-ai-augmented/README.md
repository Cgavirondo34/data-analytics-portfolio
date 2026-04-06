# 🤖 AI-Augmented Development

## Overview

This section documents how I integrate **GitHub Copilot** and **Google Gemini** into my data analytics workflow. The goal is not to replace analytical thinking — it's to eliminate repetitive low-value work and deliver faster, higher-quality outputs.

> *"AI doesn't replace the analyst. It removes the parts that don't require an analyst."*

---

## Tools Used

| Tool | Primary Use Case |
|---|---|
| **GitHub Copilot** | In-editor code completion, SQL generation, docstring writing |
| **Google Gemini** | Documentation drafting, data exploration assistance, DAX formula generation |
| **ChatGPT** | Explaining complex concepts, peer review of logic |

---

## Use Cases in Practice

---

### 1. 🐍 Python Code Generation

**Scenario:** Need to write a pandas data cleansing function with null handling, type coercion, and logging.

**Prompt given to Copilot:**
```python
# Clean a sales DataFrame:
# - drop rows with null order_id or customer_id
# - convert order_date to datetime
# - clip quantity to be >= 0
# - standardise category column to title case
# - log how many rows were removed
def cleanse_data(df):
```

**Copilot output:** Generated ~90% of the function body correctly on first suggestion.

**My contribution:** Reviewed logic, added edge case handling for empty DataFrames, adjusted the logging format to match the project's standard.

**Time saved:** ~20 minutes of boilerplate writing reduced to ~3 minutes of review and refinement.

---

### 2. 🗄️ SQL Query Assistance

**Scenario:** Need to write a window function query to rank salespeople by revenue within each region.

**Prompt given to Copilot (as a SQL comment):**
```sql
-- Rank each salesperson by total revenue within their region,
-- joining orders, order_items and salespeople tables
```

**Copilot output:** Produced a `RANK() OVER (PARTITION BY region ORDER BY SUM(...))` query with the correct JOIN structure.

**My contribution:** Validated the join keys, confirmed the aggregation logic matched business requirements, adjusted column aliases for the reporting tool.

---

### 3. 📝 Documentation Generation

**Scenario:** Need to write a README explaining a Power BI dashboard to non-technical stakeholders.

**Prompt given to Gemini:**
> *"Write a README section that explains a Power BI sales dashboard to a non-technical Sales Director. Include: objective, KPIs tracked, how to use filters, and what actions to take based on the data. Professional tone, concise."*

**Output used:** ~70% directly, with adjustments for company-specific context and tone.

**Time saved:** First draft in 2 minutes vs. 30+ minutes writing from scratch.

---

### 4. 📊 DAX Formula Generation

**Scenario:** Need a DAX measure for revenue year-over-year percentage change.

**Prompt given to Gemini:**
> *"Write a DAX measure for revenue YoY % change using SAMEPERIODLASTYEAR. Handle the case where prior year revenue is zero."*

**Output:**
```dax
Revenue YoY % =
VAR CurrentRevenue = [Total Revenue]
VAR PriorRevenue   = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('dim_date'[Date]))
RETURN
    IF(
        ISBLANK(PriorRevenue) || PriorRevenue = 0,
        BLANK(),
        DIVIDE(CurrentRevenue - PriorRevenue, PriorRevenue)
    )
```

**My contribution:** Tested against actual data, verified BLANK() handling in visuals, added a FORMAT wrapper for display.

---

### 5. 🔍 Data Exploration Assistance

**Scenario:** Investigating an unexpected spike in returns during Q3.

**Prompt given to Gemini:**
> *"I have a sales dataset with columns: order_date, category, status, quantity, unit_price, region. Suggest 5 SQL queries that would help me investigate why returns spiked in Q3."*

**Output:** 5 targeted queries covering return rate by category, region, price range, and product age — all directly actionable.

**Value:** Accelerated root cause analysis from "where do I start?" to running queries in under 5 minutes.

---

## My Workflow

```
Business Question
      │
      ▼
Define what I need analytically (my thinking)
      │
      ▼
Use AI to generate the first draft (code / SQL / doc)
      │
      ▼
Review, validate, and refine (my expertise)
      │
      ▼
Test against real data / requirements
      │
      ▼
Deliver clean, documented output
```

---

## Principles I Follow

1. **I always review AI output** — never ship AI-generated code without understanding it.
2. **AI handles the "how"** — I define the "what" and "why".
3. **Document AI usage** — I note when AI assisted in code comments or READMEs.
4. **Keep prompts precise** — vague prompts produce generic output. Good prompts produce useful output.
5. **Use AI for speed, not shortcuts** — the goal is to deliver better work faster, not to skip thinking.

---

## Impact on Productivity

| Task | Manual Time | AI-Assisted Time | Saving |
|---|---|---|---|
| Write a boilerplate Python ETL function | 30 min | 5 min | ~83% |
| Write a complex SQL window function | 20 min | 5 min | ~75% |
| Draft a technical README | 40 min | 10 min | ~75% |
| Generate 5 analytical SQL queries for investigation | 25 min | 5 min | ~80% |
| Write a DAX measure with edge cases | 15 min | 3 min | ~80% |

---

## Skills Demonstrated

- ✅ Effective prompt engineering for technical tasks
- ✅ Critical evaluation of AI-generated code and documentation
- ✅ AI-assisted Python, SQL, and DAX development
- ✅ Responsible AI usage with human oversight
- ✅ Productivity acceleration without quality loss
