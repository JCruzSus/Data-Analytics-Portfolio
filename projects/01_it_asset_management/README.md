# 01 — IT Asset & Repair Operations Analytics

## Business scenario

A device-repair operation needs a reliable way to track devices from intake through diagnosis, repair, quality check, and return. This project builds a small relational database and uses SQL to answer operational questions.

**Important:** All records are synthetic demonstration data. They are not records from iTurity or any other employer.

## Questions answered

1. How many devices are received and completed each week?
2. What is the average turnaround time by device type and repair category?
3. Which issue categories account for the most labor and parts cost?
4. What is the repair completion and repeat-repair rate?
5. How does workload vary across technicians?

## Data model

- `customers`: synthetic customer organizations
- `technicians`: technician roster
- `devices`: device metadata and customer link
- `work_orders`: intake, status, technician, timestamps, labor and parts cost
- `status_history`: lifecycle event log

The SQL schema includes primary keys, foreign keys, check constraints, and analysis views.

## Run

```bash
pip install -r ../../requirements.txt
python src/generate_data.py
python src/run_analysis.py
```

The scripts create `data/repair_operations.db` and export summary tables to `outputs/`.

## Files

- `sql/schema.sql` — schema and views
- `sql/analysis_queries.sql` — reusable business queries
- `src/generate_data.py` — reproducible synthetic data generator
- `src/run_analysis.py` — database build and KPI exports

## Interpretation notes

Turnaround is measured from intake to completion for closed orders only. Open orders are not treated as completed. Repeat-repair flags are synthetic indicators and should be interpreted as an illustrative quality metric.
