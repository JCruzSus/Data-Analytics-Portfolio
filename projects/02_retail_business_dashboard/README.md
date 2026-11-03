# 02 — Retail Business Performance Dashboard

## Business question
Which regions, product categories, and customer segments drive revenue and gross profit, and how do discounts relate to transaction profitability?

**Data disclosure:** 4,000 seeded synthetic retail transactions from 2024–2025; not sales from a real retailer.

## Run results

| KPI | Result |
|---|---:|
| Transactions | 4,000 |
| Revenue | $3,275,491.68 |
| Gross profit | $1,009,375.49 |
| Gross margin | 30.82% |
| Units sold | 16,178 |
| Average order value | $818.87 |
| Average discount | 8.65% |

## Findings in this generated sample
- Central is the highest-profit region ($263,523.29).
- Technology is the highest-profit category ($605,661.34).
- Discount and profit are explored descriptively; this synthetic data does not establish a causal discount effect.

## Interactive dashboard
The Streamlit app is in `app.py`. Run it locally:

```bash
pip install -r ../../requirements.txt
python src/generate_data.py
streamlit run app.py
```

The KPI and chart analysis was executed and the summary tables are committed. Streamlit itself was not launched in the build environment because Streamlit was not installed there.

## Re-run analysis

```bash
python src/analyze_and_visualize.py
```

## Results
- [Monthly performance](outputs/monthly_performance.csv)
- [Regional performance](outputs/regional_performance.csv)
- [Category performance](outputs/category_performance.csv)
- [Customer segment performance](outputs/segment_performance.csv)
- [Top products](outputs/top_products.csv)
- [Run results](outputs/RESULTS.md)

## Limitations
No returns, shipping, taxes, inventory constraints, marketing spend, or acquisition costs. Profit uses generated product cost and revenue only. Not suitable for real business decisions.
