-- Query 1: Overall Attrition Rate
SELECT
    COUNT(*) AS Total_Employees,
    SUM(Attrition_Flag) AS Attrited,
    ROUND(SUM(Attrition_Flag) * 100.0 / COUNT(*), 2) AS Attrition_Rate_Pct
FROM employee_features;

-- Query 2: Attrition by Department
SELECT
    e.Department,
    COUNT(*) AS Total,
    SUM(f.Attrition_Flag) AS Attrited,
    ROUND(SUM(f.Attrition_Flag) * 100.0 / COUNT(*), 2) AS Attrition_Rate_Pct
FROM employee_raw e
JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
GROUP BY e.Department
ORDER BY Attrition_Rate_Pct DESC;

-- Query 3: Average Salary of Leavers vs Stayers
SELECT
    CASE WHEN f.Attrition_Flag = 1 THEN 'Left' ELSE 'Stayed' END AS Status,
    ROUND(AVG(e.MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(e.PercentSalaryHike), 2) AS Avg_Hike_Pct
FROM employee_raw e
JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
GROUP BY f.Attrition_Flag;

-- Query 4: Overtime Impact on Attrition
SELECT
    e.OverTime,
    COUNT(*) AS Total,
    SUM(f.Attrition_Flag) AS Attrited,
    ROUND(SUM(f.Attrition_Flag) * 100.0 / COUNT(*), 2) AS Attrition_Rate_Pct
FROM employee_raw e
JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
GROUP BY e.OverTime;

-- Query 5: High Risk Employees (Prediction Based)
SELECT
    p.EmployeeNumber,
    e.Department,
    e.JobRole,
    e.MonthlyIncome,
    p.Attrition_Probability,
    p.Risk_Category
FROM employee_predictions p
JOIN employee_raw e ON p.EmployeeNumber = e.EmployeeNumber
WHERE p.Risk_Category = 'High Risk'
ORDER BY p.Attrition_Probability DESC;

-- Query 6: Compensation Ratio vs Attrition
SELECT
    CASE
        WHEN f.Compensation_Ratio < 0.8 THEN 'Underpaid'
        WHEN f.Compensation_Ratio BETWEEN 0.8 AND 1.2 THEN 'Fair'
        ELSE 'Overpaid'
    END AS Pay_Band,
    COUNT(*) AS Total,
    SUM(f.Attrition_Flag) AS Attrited,
    ROUND(SUM(f.Attrition_Flag) * 100.0 / COUNT(*), 2) AS Attrition_Rate_Pct
FROM employee_features f
GROUP BY Pay_Band
ORDER BY Attrition_Rate_Pct DESC;

-- Query 7: Stagnation Risk - No Promotion in 3+ Years
SELECT
    e.Department,
    e.JobRole,
    COUNT(*) AS Stagnant_Employees,
    ROUND(AVG(e.MonthlyIncome), 2) AS Avg_Income,
    SUM(f.Attrition_Flag) AS Already_Left
FROM employee_raw e
JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
WHERE e.YearsSinceLastPromotion >= 3
GROUP BY e.Department, e.JobRole
ORDER BY Stagnant_Employees DESC;