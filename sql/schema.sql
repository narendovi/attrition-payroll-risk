-- Create Database
CREATE DATABASE IF NOT EXISTS attrition_db;
USE attrition_db;

-- Table 1: Raw Employee Data
CREATE TABLE IF NOT EXISTS employee_raw (
    EmployeeNumber INT PRIMARY KEY,
    Age INT,
    Attrition VARCHAR(5),
    BusinessTravel VARCHAR(50),
    Department VARCHAR(50),
    DistanceFromHome INT,
    Education INT,
    EducationField VARCHAR(50),
    EnvironmentSatisfaction INT,
    Gender VARCHAR(10),
    JobLevel INT,
    JobRole VARCHAR(50),
    JobSatisfaction INT,
    MaritalStatus VARCHAR(20),
    MonthlyIncome INT,
    NumCompaniesWorked INT,
    OverTime VARCHAR(5),
    PercentSalaryHike INT,
    PerformanceRating INT,
    RelationshipSatisfaction INT,
    StockOptionLevel INT,
    TotalWorkingYears INT,
    TrainingTimesLastYear INT,
    WorkLifeBalance INT,
    YearsAtCompany INT,
    YearsInCurrentRole INT,
    YearsSinceLastPromotion INT,
    YearsWithCurrManager INT
);

-- Table 2: Engineered Payroll Features
CREATE TABLE IF NOT EXISTS employee_features (
    EmployeeNumber INT PRIMARY KEY,
    Attrition_Flag INT,
    Compensation_Ratio FLOAT,
    Hike_Band VARCHAR(10),
    OverTime_Flag INT,
    Overtime_LowHike_Risk INT,
    Tenure_Per_Level FLOAT,
    Total_Comp_Score FLOAT,
    Exp_Pay_Ratio FLOAT,
    FOREIGN KEY (EmployeeNumber) REFERENCES employee_raw(EmployeeNumber)
);

-- Table 3: Model Predictions
CREATE TABLE IF NOT EXISTS employee_predictions (
    EmployeeNumber INT PRIMARY KEY,
    Attrition_Probability FLOAT,
    Attrition_Prediction INT,
    Risk_Category VARCHAR(20),
    FOREIGN KEY (EmployeeNumber) REFERENCES employee_raw(EmployeeNumber)
);