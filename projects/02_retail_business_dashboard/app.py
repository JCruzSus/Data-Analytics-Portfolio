"""Interactive Streamlit dashboard for synthetic retail transactions."""
from pathlib import Path
import subprocess, sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "retail_transactions.csv"

st.set_page_config(page_title="Retail Performance", page_icon="📊", layout="wide")
st.title("Retail Business Performance")
st.caption("Portfolio demo • Synthetic transaction data • 2024–2025")

if not DATA.exists():
    subprocess.run([sys.executable, str(ROOT / "src" / "generate_data.py")], check=True)

df = pd.read_csv(DATA, parse_dates=["order_date"])
with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df.region.unique()), default=sorted(df.region.unique()))
    categories = st.multiselect("Category", sorted(df.category.unique()), default=sorted(df.category.unique()))
    segments = st.multiselect("Customer segment", sorted(df.segment.unique()), default=sorted(df.segment.unique()))
    min_date, max_date = df.order_date.min().date(), df.order_date.max().date()
    date_range = st.date_input("Order date range", value=(min_date,max_date), min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start, end = date_range
else:
    start, end = min_date, max_date
f = df[df.region.isin(regions) & df.category.isin(categories) & df.segment.isin(segments) &
       df.order_date.dt.date.between(start,end)].copy()

if f.empty:
    st.warning("No transactions match these filters.")
    st.stop()

revenue, profit, orders = f.sales.sum(), f.profit.sum(), f.order_id.nunique()
margin = profit / revenue if revenue else 0
a,b,c,d = st.columns(4)
a.metric("Revenue", f"${revenue:,.0f}")
b.metric("Gross profit", f"${profit:,.0f}")
c.metric("Orders", f"{orders:,}")
d.metric("Gross margin", f"{margin:.1%}")

monthly = f.set_index("order_date").resample("MS").agg(sales=("sales","sum"),profit=("profit","sum")).reset_index()
left,right = st.columns(2)
left.plotly_chart(px.line(monthly,x="order_date",y="sales",title="Monthly revenue",markers=True),use_container_width=True)
right.plotly_chart(px.bar(f.groupby("region",as_index=False).agg(profit=("profit","sum")).sort_values("profit",ascending=False),
                          x="region",y="profit",title="Gross profit by region"),use_container_width=True)

left,right = st.columns(2)
left.plotly_chart(px.bar(f.groupby("category",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum")),
                         x="category",y=["sales","profit"],barmode="group",title="Sales and profit by category"),use_container_width=True)
right.plotly_chart(px.scatter(f,x="discount",y="profit",color="category",opacity=.55,
                              title="Discount vs. transaction profit",labels={"discount":"Discount rate"}),use_container_width=True)

st.subheader("Top products by profit")
top = f.groupby("product",as_index=False).agg(units=("units","sum"),sales=("sales","sum"),profit=("profit","sum"))
st.dataframe(top.sort_values("profit",ascending=False).head(10).style.format({"sales":"${:,.2f}","profit":"${:,.2f}"}),use_container_width=True)
st.download_button("Download filtered transactions",f.to_csv(index=False).encode("utf-8"),"filtered_retail_transactions.csv","text/csv")
st.caption("Interpretation: Explore the filters and compare trends. Correlation between discount and profit is not evidence that discounting alone causes profit changes.")
