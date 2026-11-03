"""Generate reproducible synthetic IT repair operations data."""
from pathlib import Path
import random
import sqlite3
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "repair_operations.db"
SCHEMA = ROOT / "sql" / "schema.sql"

def main():
    random.seed(42)
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    con.executemany("INSERT INTO customers VALUES (?,?,?)", [
        (1, "Northside ISD", "School District"),
        (2, "Central Learning Network", "School District"),
        (3, "Small Business Co.", "Business"),
        (4, "Walk-in Customer Group", "Individual")
    ])
    con.executemany("INSERT INTO technicians VALUES (?,?,?)", [
        (1, "Alex Morgan", "Hardware"),
        (2, "Jamie Lee", "Hardware"),
        (3, "Taylor Rivera", "Imaging")
    ])
    device_types = ["Chromebook", "Windows Laptop", "iPad"]
    makers = {"Chromebook": ["Acer", "Lenovo", "Dell"],
              "Windows Laptop": ["Dell", "HP", "Lenovo"], "iPad": ["Apple"]}
    issues = ["Battery", "Keyboard", "Screen", "Operating System",
              "Charging Port", "Connectivity", "Other"]
    today = date(2025, 12, 31)
    for i in range(1, 501):
        dtype = random.choice(device_types)
        intake = today - timedelta(days=random.randint(0, 364))
        status = random.choices(
            ["Completed", "Waiting for Parts", "Repairing", "Diagnosing", "Unrepairable"],
            [.72, .08, .08, .08, .04])[0]
        completion = (intake + timedelta(days=random.randint(1, 12))).isoformat() if status == "Completed" else None
        con.execute("INSERT INTO devices VALUES (?,?,?,?,?,?)", (
            i, random.randint(1, 4), dtype, random.choice(makers[dtype]),
            f"Model-{random.randint(100, 999)}", random.choice(["Good", "Fair", "Damaged"])))
        cur = con.execute("""INSERT INTO work_orders
            (device_id, technician_id, issue_category, priority, intake_date,
             completion_date, status, labor_hours, parts_cost, repeat_repair)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", (
                i, random.randint(1, 3), random.choice(issues),
                random.choice(["Low", "Normal", "High", "Urgent"]),
                intake.isoformat(), completion, status,
                round(random.uniform(.25, 3.5), 2),
                round(random.choice([0, 0, 0, 12, 18, 25, 35, 60, 90]), 2),
                int(random.random() < .07)))
        work_order_id = cur.lastrowid
        con.execute("INSERT INTO status_history(work_order_id,status,event_date,notes) VALUES (?,?,?,?)",
                    (work_order_id, "Received", intake.isoformat(), "Device checked in"))
        if completion:
            con.execute("INSERT INTO status_history(work_order_id,status,event_date,notes) VALUES (?,?,?,?)",
                        (work_order_id, "Completed", completion, "Repair completed"))
    con.commit()
    con.close()
    print(f"Created 500 synthetic work orders in {DB}")

if __name__ == "__main__":
    main()
