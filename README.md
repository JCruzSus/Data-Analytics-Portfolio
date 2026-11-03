# Data Analytics Portfolio

A collection of end-to-end analytics projects demonstrating SQL, Python, data visualization, and machine learning.

**Author:** Jonathan Cruz-Sustaita  
**Focus:** Entry-level Data Analyst / Business Analyst roles

## Projects

| Project | Business question | Tools |
|---|---|---|
| [01 — IT Asset & Repair Operations](projects/01_it_asset_management/README.md) | How can a repair operation track inventory, turnaround, cost, and technician workload? | SQL, SQLite, Python, Pandas |
| [02 — Retail Business Performance](projects/02_retail_business_dashboard/README.md) | Which products, regions, and customer segments drive sales and profit? | Python, Pandas, Plotly, Streamlit |
| [03 — Employee Attrition Modeling](projects/03_employee_attrition/README.md) | Which employee characteristics are associated with attrition, and how well can a model identify elevated risk? | Python, Pandas, scikit-learn, Matplotlib |

## Repository structure

```
projects/
  01_it_asset_management/
    data/
    sql/
    src/
    README.md
  02_retail_business_dashboard/
    data/
    src/
    app.py
    README.md
  03_employee_attrition/
    data/
    notebooks/
    src/
    README.md
```

## Getting started

Use Python 3.10+ and create a virtual environment.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Each project contains its own instructions and generates demonstration data or downloads its documented public dataset. The IT repair and retail datasets in this repository are explicitly **synthetic**, designed to demonstrate analytical workflows; they do not represent an actual employer's records. The attrition project uses the IBM HR Analytics Employee Attrition & Performance sample dataset, which must be obtained separately from its source.

## Project status and responsible use

These projects are portfolio demonstrations. Model outputs are exploratory, not causal conclusions or decisions about real employees. Attrition prediction can encode historical bias and should not be used to make employment decisions. Results should be validated against business context before operational use.

## Skills demonstrated

- Relational data modeling, SQL joins, aggregations, views, and quality checks
- Data cleaning, exploratory analysis, KPI design, and business storytelling
- Interactive dashboard development
- Classification, train/test separation, cross-validation, model comparison, and threshold-aware evaluation

---
