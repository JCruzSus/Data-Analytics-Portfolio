# 02 — Retail Business Performance Dashboard

## Business scenario

A multi-region retailer wants to understand sales, profit, discounting, product performance, and customer behavior. This project creates a reproducible dataset and an interactive Streamlit dashboard.

**Data note:** The included-data generator creates synthetic retail transactions. The dashboard is an illustrative business case, not a claim about any real retailer.

## Key questions

- How are revenue, gross profit, and order volume trending?
- Which regions and categories contribute the most profit?
- Are large discounts associated with weaker margins?
- Which products and customer segments lead performance?

## Run

```bash
pip install -r ../../requirements.txt
python src/generate_data.py
streamlit run app.py
```

Open the local Streamlit URL shown in your terminal.

## Files

- `src/generate_data.py` — reproducible synthetic transaction generator
- `app.py` — interactive dashboard with filters and Plotly charts
- `data/` — generated CSV is created locally (not committed)

## Metrics

Revenue is the sum of sales. Profit is revenue less product cost. Margin is profit divided by revenue. Returns and tax/shipping are not modeled in this simplified example.

## Limitations

Data is synthetic and intentionally simplified. It does not include seasonality calibration, returns, inventory availability, or customer acquisition costs.
