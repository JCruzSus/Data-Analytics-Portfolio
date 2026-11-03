"""Run the IT repair SQL analysis and export charts."""
from pathlib import Path
import subprocess, sys, sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
def main():
    subprocess.run([sys.executable,str(ROOT/"src"/"run_analysis.py")],check=True)
    out=ROOT/"outputs"; img=ROOT/"visualizations"; img.mkdir(exist_ok=True)
    with sqlite3.connect(ROOT/"data"/"repair_operations.db") as con:
        device=pd.read_sql_query("""SELECT d.device_type,COUNT(*) orders,
            SUM(CASE WHEN w.status='Completed' THEN 1 ELSE 0 END) completed,
            ROUND(100.0*AVG(CASE WHEN w.status='Completed' THEN 1.0 ELSE 0.0 END),1) completion_pct
            FROM work_orders w JOIN devices d USING(device_id)
            GROUP BY d.device_type ORDER BY orders DESC""",con)
        issue=pd.read_sql_query("SELECT * FROM vw_issue_performance ORDER BY work_orders DESC",con)
        monthly=pd.read_sql_query("SELECT * FROM vw_monthly_operations ORDER BY intake_month",con)
    device.to_csv(out/"device_type_performance.csv",index=False)
    plt.figure(figsize=(9,4)); plt.bar(issue.issue_category,issue.work_orders)
    plt.xticks(rotation=35,ha="right"); plt.title("Work Orders by Issue Category")
    plt.tight_layout(); plt.savefig(img/"orders_by_issue.png",dpi=150); plt.close()
    plt.figure(figsize=(8,4)); plt.bar(device.device_type,device.completion_pct)
    plt.ylabel("Completion rate (%)"); plt.title("Completion Rate by Device Type")
    plt.tight_layout(); plt.savefig(img/"completion_by_device.png",dpi=150); plt.close()
    plt.figure(figsize=(10,4)); plt.plot(pd.to_datetime(monthly.intake_month),monthly.orders_received,marker="o",label="Received")
    plt.plot(pd.to_datetime(monthly.intake_month),monthly.orders_completed,marker="o",label="Completed")
    plt.legend(); plt.title("Monthly Repair Work Orders"); plt.tight_layout()
    plt.savefig(img/"monthly_work_orders.png",dpi=150); plt.close()
    print("IT repair analysis and charts exported.")
if __name__=="__main__": main()
