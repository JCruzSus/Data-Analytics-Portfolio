"""Build repair database and export portfolio KPI tables."""
from pathlib import Path
import sqlite3
import pandas as pd
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
DB = DATA / "repair_operations.db"

def main():
    subprocess.run([sys.executable, str(ROOT / "src" / "generate_data.py")], check=True)
    OUT.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as con:
        for name, query in {
            "monthly_operations": "SELECT * FROM vw_monthly_operations ORDER BY intake_month",
            "issue_performance": "SELECT * FROM vw_issue_performance ORDER BY work_orders DESC",
            "technician_performance": """SELECT t.technician_name, COUNT(*) assigned_orders,
                SUM(CASE WHEN w.status='Completed' THEN 1 ELSE 0 END) completed_orders,
                ROUND(100.0*AVG(w.repeat_repair),1) repeat_repair_pct
                FROM work_orders w JOIN technicians t USING(technician_id)
                GROUP BY t.technician_name"""
        }.items():
            pd.read_sql_query(query, con).to_csv(OUT / f"{name}.csv", index=False)
    print(f"Analysis exports saved in {OUT}")

if __name__ == "__main__":
    main()
