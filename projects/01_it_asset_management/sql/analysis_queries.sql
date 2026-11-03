-- 1. Workload and completion by device type
SELECT d.device_type, COUNT(*) AS orders,
       SUM(CASE WHEN w.status = 'Completed' THEN 1 ELSE 0 END) AS completed
FROM work_orders w JOIN devices d USING (device_id)
GROUP BY d.device_type ORDER BY orders DESC;

-- 2. Average turnaround for completed orders
SELECT d.device_type,
       ROUND(AVG(julianday(w.completion_date) - julianday(w.intake_date)), 2) AS avg_days
FROM work_orders w JOIN devices d USING (device_id)
WHERE w.status = 'Completed' AND w.completion_date IS NOT NULL
GROUP BY d.device_type;

-- 3. Issue categories with highest costs
SELECT issue_category, COUNT(*) AS orders,
       ROUND(AVG(labor_hours), 2) AS avg_labor_hours,
       ROUND(AVG(parts_cost), 2) AS avg_parts_cost,
       ROUND(AVG(labor_hours * 28 + parts_cost), 2) AS avg_total_cost
FROM work_orders
GROUP BY issue_category ORDER BY avg_total_cost DESC;

-- 4. Technician workload and repeat repair frequency
SELECT t.technician_name, COUNT(*) AS assigned_orders,
       SUM(CASE WHEN w.status = 'Completed' THEN 1 ELSE 0 END) AS completed_orders,
       ROUND(100.0 * AVG(w.repeat_repair), 1) AS repeat_repair_pct
FROM work_orders w JOIN technicians t USING (technician_id)
GROUP BY t.technician_name ORDER BY assigned_orders DESC;

-- 5. Monthly operations from the view
SELECT * FROM vw_monthly_operations ORDER BY intake_month;
