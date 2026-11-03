"""Generate synthetic retail transaction data for a dashboard demo."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "retail_transactions.csv"

def main():
    rng = np.random.default_rng(17)
    n = 4000
    dates = pd.to_datetime(rng.choice(pd.date_range("2024-01-01","2025-12-31",freq="D"), n))
    categories = rng.choice(["Technology","Office Supplies","Furniture","Accessories"], n, p=[.28,.27,.22,.23])
    regions = rng.choice(["West","East","Central","South"], n)
    segments = rng.choice(["Consumer","Corporate","Small Business"], n, p=[.55,.3,.15])
    units = rng.integers(1, 8, n)
    unit_price = np.select(
        [categories=="Technology", categories=="Furniture", categories=="Accessories"],
        [rng.uniform(80,900,n), rng.uniform(40,500,n), rng.uniform(10,120,n)],
        default=rng.uniform(5,90,n))
    unit_cost = unit_price * rng.uniform(.45,.82,n)
    discount = rng.choice([0,.05,.10,.15,.20,.30], n, p=[.35,.14,.20,.14,.12,.05])
    sales = units * unit_price * (1-discount)
    profit = sales - units * unit_cost
    df = pd.DataFrame({
        "order_id": np.arange(10001,10001+n),
        "order_date": dates,
        "region": regions,
        "segment": segments,
        "category": categories,
        "product": [f"{c} Product {i%12+1}" for i,c in enumerate(categories)],
        "units": units,
        "unit_price": unit_price.round(2),
        "discount": discount,
        "sales": sales.round(2),
        "cost": (units*unit_cost).round(2),
        "profit": profit.round(2)
    }).sort_values("order_date")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT,index=False)
    print(f"Saved {len(df)} synthetic transactions to {OUT}")

if __name__ == "__main__":
    main()
