import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv('/Users/naren/Projects/attrition-payroll-risk/.env')

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

query = """
    SELECT e.*, f.Attrition_Flag, f.Compensation_Ratio, f.Hike_Band,
           f.OverTime_Flag, f.Overtime_LowHike_Risk, f.Tenure_Per_Level,
           f.Total_Comp_Score, f.Exp_Pay_Ratio,
           p.Attrition_Probability, p.Attrition_Prediction, p.Risk_Category
    FROM employee_raw e
    JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
    JOIN employee_predictions p ON e.EmployeeNumber = p.EmployeeNumber
"""

df = pd.read_sql(query, con=engine)
df.to_csv('data/processed/dashboard_data.csv', index=False)
print(f"Exported {len(df)} rows to dashboard_data.csv")
