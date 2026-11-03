"""Create retail KPI tables and visualizations from the generated transaction CSV."""
from pathlib import Path
import subprocess,sys
import pandas as pd
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=ROOT/"data"/"retail_transactions.csv"
    if not data.exists(): subprocess.run([sys.executable,str(ROOT/"src"/"generate_data.py")],check=True)
    out=ROOT/"outputs"; img=ROOT/"visualizations"; out.mkdir(exist_ok=True); img.mkdir(exist_ok=True)
    df=pd.read_csv(data,parse_dates=["order_date"]); df["month"]=df.order_date.dt.to_period("M").astype(str)
    tables={
      "monthly_performance":df.groupby("month",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"),orders=("order_id","nunique")),
      "regional_performance":df.groupby("region",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"),orders=("order_id","nunique")),
      "category_performance":df.groupby("category",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"),units=("units","sum")),
      "segment_performance":df.groupby("segment",as_index=False).agg(revenue=("sales","sum"),profit=("profit","sum"),orders=("order_id","nunique")),
      "top_products":df.groupby("product",as_index=False).agg(units=("units","sum"),revenue=("sales","sum"),profit=("profit","sum")).sort_values("profit",ascending=False).head(15)}
    for name,table in tables.items(): table.to_csv(out/f"{name}.csv",index=False)
    kpis={"transactions":df.order_id.nunique(),"revenue":df.sales.sum(),"gross_profit":df.profit.sum(),
          "gross_margin_pct":100*df.profit.sum()/df.sales.sum(),"units_sold":df.units.sum(),
          "avg_order_value":df.sales.mean(),"avg_discount_pct":100*df.discount.mean()}
    pd.Series(kpis,name="value").to_csv(out/"kpis.csv")
    m=tables["monthly_performance"]; plt.figure(figsize=(10,4)); plt.plot(pd.to_datetime(m.month),m.revenue,label="Revenue"); plt.plot(pd.to_datetime(m.month),m.profit,label="Profit"); plt.legend(); plt.title("Monthly Revenue and Profit"); plt.tight_layout(); plt.savefig(img/"monthly_revenue_profit.png",dpi=150); plt.close()
    for name,col,title in [("regional_performance","region","Gross Profit by Region"),("category_performance","category","Gross Profit by Category")]:
        t=tables[name].sort_values("profit",ascending=False); plt.figure(figsize=(8,4)); plt.bar(t[col],t.profit); plt.xticks(rotation=25,ha="right"); plt.title(title); plt.ylabel("Profit ($)"); plt.tight_layout(); plt.savefig(img/("profit_by_region.png" if col=="region" else "profit_by_category.png"),dpi=150); plt.close()
    plt.figure(figsize=(8,4)); plt.scatter(df.discount*100,df.profit,alpha=.25); plt.xlabel("Discount (%)"); plt.ylabel("Transaction profit ($)"); plt.title("Discount vs. Transaction Profit"); plt.tight_layout(); plt.savefig(img/"discount_vs_profit.png",dpi=150); plt.close()
    print("Retail KPI tables and visualizations exported.")
if __name__=="__main__": main()
