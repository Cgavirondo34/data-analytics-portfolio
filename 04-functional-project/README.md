# 📋 Functional Project — CRM Data Integration

## Business Problem

A mid-size retail company manages customer interactions across three isolated systems:
- A legacy **ERP** (SAP B1) that tracks orders and invoices
- A **CRM tool** (HubSpot) used by the sales team to log calls, meetings, and deals
- A **support ticketing system** (Freshdesk) for post-sale issues

**The problem:** Customer data lives in three silos. There is no unified customer view. Sales reps don't know if a customer has open support tickets. Management cannot measure customer satisfaction alongside revenue. Reports are built manually every week by copying data between Excel files.

---

## Proposed Solution

Design and implement a **Customer 360 Data Integration** layer that:

1. **Extracts** data nightly from ERP, CRM, and ticketing systems via APIs and database connectors
2. **Transforms** and harmonises customer records into a single canonical format
3. **Loads** into a centralised data warehouse (Azure SQL)
4. **Exposes** the unified view via a Power BI dashboard and an internal web portal

---

## System Scope

### In scope
- Customer master data unification (deduplication, golden record)
- Order and revenue history per customer
- Sales activity log (calls, meetings, deal stages)
- Support ticket history and CSAT scores
- Daily automated refresh
- Power BI Customer 360 dashboard

### Out of scope
- Real-time streaming (Phase 2)
- Direct write-back to source systems
- Mobile app

---

## Process Flows

### P1 — Nightly ETL Process

```
[ERP API]     ──►
[CRM API]     ──►  [ETL Orchestrator]  ──►  [Staging Layer]  ──►  [Data Warehouse]
[Tickets API] ──►
```

Steps:
1. Scheduler triggers ETL at 02:00 AM
2. Connectors extract delta changes from each source
3. Raw data lands in staging tables
4. Transformation rules apply: deduplication, normalisation, matching
5. Golden records are upserted into the `customers` dimension
6. Fact tables (orders, activities, tickets) are refreshed
7. Power BI dataset is refreshed at 06:00 AM

---

### P2 — Customer Deduplication Logic

| Rule | Action |
|---|---|
| Same email address | Auto-merge |
| Same phone + company name | Auto-merge |
| Similar name + same city | Flag for manual review |
| Conflicting data | Source priority: ERP > CRM > Tickets |

---

## User Roles

| Role | Access | Use Case |
|---|---|---|
| **Sales Rep** | Own customers only | View customer 360 before a call |
| **Sales Manager** | Full team | Monitor pipeline and customer health |
| **Support Agent** | Ticket-related data | Check order history for a case |
| **Data Analyst** | Read-only full access | Build reports and ad-hoc queries |
| **IT Admin** | Full system | Manage connectors and schedules |

---

## Data Requirements

### Canonical Customer Record

| Field | Source | Notes |
|---|---|---|
| `customer_id` | Generated (UUID) | Unique across all systems |
| `full_name` | ERP (primary) | Normalised |
| `email` | CRM | Validated format |
| `phone` | ERP / CRM | E.164 format |
| `company` | ERP | |
| `segment` | Calculated | Based on LTV tier |
| `ltv` | Calculated | 12-month rolling revenue |
| `open_tickets` | Freshdesk | Count of unresolved tickets |
| `last_order_date` | ERP | |
| `nps_score` | Freshdesk | Last CSAT survey score |

---

## KPIs to Track (Post-Implementation)

| KPI | Target |
|---|---|
| Data freshness | < 6 hours lag |
| Deduplication rate | > 98% auto-resolved |
| Dashboard adoption | > 80% of sales team weekly active |
| Manual report time saved | > 8 hours/week per analyst |
| Customer match rate across systems | > 95% |

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| API rate limits on CRM | Medium | Implement exponential backoff + batching |
| Duplicate golden records | High | Human review queue for ambiguous matches |
| Schema changes in source systems | Medium | Schema validation step in ETL with alerting |
| Data privacy (GDPR) | High | PII masking in non-prod; access controls on prod |

---

## Skills Demonstrated

- ✅ Functional analysis: translating a business problem into a technical solution
- ✅ Process documentation and flow design
- ✅ Data modelling and integration architecture
- ✅ User story thinking (roles and access)
- ✅ KPI definition and success measurement
- ✅ Risk identification and mitigation planning
