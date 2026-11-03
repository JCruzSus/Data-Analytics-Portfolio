PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_monthly_operations;
DROP VIEW IF EXISTS vw_issue_performance;
DROP TABLE IF EXISTS status_history;
DROP TABLE IF EXISTS work_orders;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS technicians;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_type TEXT NOT NULL CHECK (customer_type IN ('School District', 'Business', 'Individual'))
);

CREATE TABLE technicians (
    technician_id INTEGER PRIMARY KEY,
    technician_name TEXT NOT NULL,
    team TEXT NOT NULL
);

CREATE TABLE devices (
    device_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    device_type TEXT NOT NULL CHECK (device_type IN ('Chromebook', 'Windows Laptop', 'iPad')),
    manufacturer TEXT NOT NULL,
    model TEXT NOT NULL,
    received_condition TEXT NOT NULL
);

CREATE TABLE work_orders (
    work_order_id INTEGER PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(device_id),
    technician_id INTEGER NOT NULL REFERENCES technicians(technician_id),
    issue_category TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('Low', 'Normal', 'High', 'Urgent')),
    intake_date TEXT NOT NULL,
    completion_date TEXT,
    status TEXT NOT NULL CHECK (status IN ('Received', 'Diagnosing', 'Waiting for Parts', 'Repairing', 'Quality Check', 'Completed', 'Unrepairable')),
    labor_hours REAL NOT NULL CHECK (labor_hours >= 0),
    parts_cost REAL NOT NULL CHECK (parts_cost >= 0),
    repeat_repair INTEGER NOT NULL DEFAULT 0 CHECK (repeat_repair IN (0,1))
);

CREATE TABLE status_history (
    event_id INTEGER PRIMARY KEY,
    work_order_id INTEGER NOT NULL REFERENCES work_orders(work_order_id),
    status TEXT NOT NULL,
    event_date TEXT NOT NULL,
    notes TEXT
);

CREATE INDEX idx_work_orders_intake ON work_orders(intake_date);
CREATE INDEX idx_work_orders_status ON work_orders(status);
CREATE INDEX idx_devices_type ON devices(device_type);

CREATE VIEW vw_issue_performance AS
SELECT issue_category,
       COUNT(*) AS work_orders,
       ROUND(AVG(labor_hours), 2) AS avg_labor_hours,
       ROUND(AVG(parts_cost), 2) AS avg_parts_cost,
       ROUND(100.0 * AVG(repeat_repair), 1) AS repeat_repair_pct
FROM work_orders
GROUP BY issue_category;

CREATE VIEW vw_monthly_operations AS
SELECT substr(intake_date, 1, 7) AS intake_month,
       COUNT(*) AS orders_received,
       SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS orders_completed,
       ROUND(AVG(CASE WHEN completion_date IS NOT NULL
           THEN julianday(completion_date) - julianday(intake_date) END), 2) AS avg_turnaround_days
FROM work_orders
GROUP BY substr(intake_date, 1, 7);
