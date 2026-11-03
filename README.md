# Data Analytics Portfolio

End-to-end portfolio case studies demonstrating SQL, Python, data visualization, and machine learning.

**Author:** Jonathan Cruz-Sustaita  
**Career focus:** Entry-level Data Analyst / Business Analyst

## Projects

| Project | Business question | Tools |
|---|---|---|
| [01 — IT Asset & Repair Operations](projects/01_it_asset_management/README.md) | How can a repair operation monitor intake, turnaround, cost, and technician workload? | SQL, SQLite, Python, Pandas, Matplotlib |
| [02 — Retail Business Performance](projects/02_retail_business_dashboard/README.md) | Which regions, products, and segments drive sales and profit? | Python, Pandas, Plotly, Streamlit, Matplotlib |
| [03 — Employee Attrition Analysis & Prediction](projects/03_employee_attrition/README.md) | What patterns are associated with attrition, and how do classifiers perform? | Python, Pandas, scikit-learn, Matplotlib |

## Reproduce
Use Python 3.10+ and install `requirements.txt`. Each project includes a seeded data generator, analysis script, outputs, visualizations, notebook, and project-specific README. IT repair, retail, and employee datasets are synthetic demonstrations, not employer data.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Run each project's script as described in its README. The retail interactive app requires Streamlit.

## Skills demonstrated
- Relational data modeling, SQL joins, aggregations, views, and constraints
- KPI design, exploratory analysis, and data storytelling
- Reproducible Python pipelines and visualizations
- Classification pipelines, leakage-aware preprocessing, imbalanced-class metrics, and permutation importance

## Caveat
Results are generated-data demonstrations, not measured business outcomes. The attrition model is educational only and must not be used for employment decisions.
