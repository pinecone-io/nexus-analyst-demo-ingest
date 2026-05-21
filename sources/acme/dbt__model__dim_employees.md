---
title: "dbt model — dim/dim_employees"
source_url: "internal://acme/dbt/dim/dim_employees"
license: "synthetic-demo"
attribution: "Acme Inc dbt model documentation (synthetic demo). Owner: David Kim (Sr DE)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: dbt_model
---

# `dim_employees`

> Path: `dbt/models/dimensions/dim_employees.sql`
> Materialization: `table` (rebuilt weekly Mondays @ 05:00 UTC)
> Owner: David Kim (`@david.kim`)
> Tags: `dimensions`, `hris`, `core`
>
> 🚧 `// TODO: @jorge.martinez keeps flagging that 'sales_engineer' role is a catch-all for both Solution Architects and Sales Engineers. HRIS doesn't distinguish yet. Need to manually map these in a seed file if Sales Ops needs the split for Q3 planning. -david 2026-04-10`

## Purpose

The canonical dimension for all Acme internal staff. Used for joining to `fact_opportunities` (AEs/SDRs), `fact_support_tickets` (Support/CS), and `dim_customers` (CSMs). 

This model is a point-in-time snapshot of the current employee roster. We do not currently maintain a history of role changes or team transfers in this table (SCD Type 1).

## SQL

```sql
{{
  config(
    materialized='table',
    tags=['core', 'hris']
  )
}}

WITH raw_employees AS (
  SELECT
    emp_id AS employee_id,
    first_name,
    last_name,
    email,
    role,
    department AS team,
    manager_id AS manager_employee_id,
    hire_date,
    termination_date,
    location,
    is_active
  FROM {{ ref('stg_hris__employees') }}
),

-- Logic to identify quota-carrying reps for Sales Ops dashboards.
-- Currently includes AEs and SDRs. 
-- Note: Sales Engineers are NOT marked as quota-carrying in this logic
-- per Marcus's request, even though they have a variable component.
quota_logic AS (
  SELECT
    *,
    CASE 
      WHEN team = 'Sales' AND (role LIKE '%Account Executive%' OR role LIKE '%SDR%') THEN TRUE
      ELSE FALSE
    END AS is_quota_carrying
  FROM raw_employees
)

SELECT
  employee_id,
  CONCAT(first_name, ' ', last_name) AS full_name,
  email,
  role,
  team,
  manager_employee_id,
  hire_date,
  termination_date,
  location,
  is_active,
  is_quota_carrying
FROM quota_logic;
```

## Columns

| Column | Type | Notes |
|---|---|---|
| `employee_id` | STRING | PK. `emp_xxx`. |
| `full_name` | STRING | Combined first and last name. |
| `email` | STRING | Acme corporate email. |
| `role` | STRING | Current job title. See note on `sales_engineer` conflation. |
| `team` | STRING | `Engineering`, `Sales`, `CS`, `Marketing`, `Product`, `Design`, `People`, `Finance`, `Legal`. |
| `manager_employee_id` | STRING | FK to self. NULL for `@sam.reyes`. |
| `hire_date` | DATE | |
| `termination_date` | DATE | NULL for active employees. |
| `location` | STRING | `SF`, `Amsterdam`, `Remote-NA`, `Remote-EU`. |
| `is_active` | BOOL | TRUE if currently employed. |
| `is_quota_carrying` | BOOL | TRUE for AEs and SDRs. |

## Known Issues & Nuances

- **Role Conflation**: As noted by `@jorge.martinez`, the `sales_engineer` role in our HRIS source is used for both pre-sales Sales Engineers and post-sales Solution Architects. If you are building a dashboard that requires this distinction, you will need to join against the `manual_role_overrides` seed file or filter by `manager_employee_id`.
- **Manager Chain**: The `manager_employee_id` for VPs (e.g., `@priya.anand`, `@marcus.webb`) points to `@sam.reyes`.
- **Quota Definition**: `is_quota_carrying` is a derived field in dbt. If Sales changes the definition of who carries a bag (e.g., adding CSMs for renewals), this model must be updated.

## Downstream Consumers

- `fact_opportunities`: Joins on `ae_employee_id` and `sdr_employee_id`.
- `fact_support_tickets`: Joins on `assigned_to_employee_id`.
- `dim_customers`: Joins on `csm_employee_id` and `ae_employee_id`.
- `marts/sales/bookings_attribution.sql`: Used for AE performance reporting.

## File History

- `2026-03-01` — `@david.kim`: Added `is_quota_carrying` logic to support Q1 sales retro.
- `2025-11-12` — `@david.kim`: Initial table materialization.
- `2025-10-04` — `@lina.cho`: Requested addition of `location` for tax/region reporting.
