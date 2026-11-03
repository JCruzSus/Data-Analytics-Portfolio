"""Generate reproducible synthetic IT repair operations data."""
from pathlib import Path
import random
import sqlite3
from datetime import date, timedelta
import sys

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "repair_operations.db"
SCHEMA = ROOT / "sql" / "schema.sql"
random.seed(42)

def main():
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))

    customers = [(1,"Northside ISD","School District"),(2,"Central Learning Network","School District"),
                 (3,"Small Business Co.","Business"),(4,"Walk-in Customer Group","Individual")]
    techs = [(1,"Alex Morgan","Hardware"),(2,"Jamie Lee","Hardware"),(3,"Taylor Rivera","Imaging")]
    con.executemany("INSERT INTO customers VALUES (?,?,?)", customers)
    con.executemany("INSERT INTO technicians VALUES (?,?,?)", techs)

    device_types = ["Chromebook","Windows Laptop","iPad"]
    makers = {"Chromebook":["Acer","Lenovo","Dell"],"Windows Laptop":["Dell","HP","Lenovo"],"iPad":["Apple"]}
    issues = ["Battery","Keyboard","Screen","Operating System","Charging Port","Connectivity","Other"]
    today = date(2025, 12, 31)
    for i in range(1, 501):
        dtype = random.choice(device_types)
        customer_id = random.randint(1, 4)
        con.execute("INSERT INTO devices VALUES (?,?,?,?,?,?)",
                    (i, customer_id, dtype, random.choice(makers[dtype]), "Model-" + str(random.randint(100,999)), random.choice(["Good","Fair","Damaged"])))
        intake = today - timedelta(days=random.randint(0, 364))
        status = random.choices(["Completed","Waiting for Parts","Repairing","Diagnosing","Unrepairable"],[.72,.08,.08,.08,.04])[0]
        completion = (intake + timedelta(days=random.randint(1, 12))).isoformat() if status == "Completed" else None
        category = random.choice(issues)
        labor = round(random.uniform(.25, 3.5), 2)
        parts = round(random.choice([0,0,0,12,18,25,35,60,90]), 2)
        repeat = 1 if random.random() < .07 else 0
        priority = random.choice(["Low","Normal","High","Urgent"])
        cur = con.execute("""INSERT INTO work_orders
          (device_id, technician_id, issue_category, priority, intake_date, completion_date,
           status, labor_hours, parts_cost, repeat_repair)
          VALUES (?,?,?,?,?,?,?,?,?,?)""",
          (i, random.randint(1,3), category, priority, intake.isoformat(), completion,
           status, labor, parts, repeat))
        wid = cur.lastrowid
        con.execute("INSERT INTO status_history(work_order_id,status,event_date,notes) VALUES (?,?,?,?)",
                    (wid,"Received",intake.isoformat(),"Device checked in"))
        if completion:
            con.execute("INSERT INTO status_history(work_order_id,status,event_date,notes) VALUES (?,?,?,?)",
                        (wid,"Completed",completion,"Repair completed"))
    con.commit()
    print(f"Created {DB} with 500 synthetic work orders.")
    con.close()

if __name__ == "__main__":
    main()
