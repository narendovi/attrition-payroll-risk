# 👥 Employee Attrition & Payroll Risk Predictor

A end-to-end HR Analytics project combining 7.5 years of payroll domain expertise 
with Data Science to predict employee attrition risk and identify payroll anomalies.

---

## 🎯 Problem Statement

Employee attrition costs organizations 50-200% of an employee's annual salary in 
replacement costs. This project builds a predictive system to identify at-risk 
employees early using payroll, compensation, and HR data.

---

## 🏗️ Project Architecture

attrition-payroll-risk/
├── data/
│ └── processed/ # Cleaned & engineered data
├── notebooks/
│ ├── 01_data_exploration.ipynb
│ ├── 02_feature_engineering.ipynb
│ ├── 03_model_building.ipynb
│ └── 04_mysql_loading.ipynb
├── sql/
│ ├── schema.sql # MySQL table definitions
│ └── analysis_queries.sql # Business insight queries
├── app/
│ └── streamlit_app.py # Interactive dashboard
├── models/
│ ├── attrition_model.pkl # Trained XGBoost model
│ └── scaler.pkl # Feature scaler
└── requirements.txt

---

## 💡 Domain-Driven Feature Engineering

As a payroll professional with 7.5 years of experience, I engineered 6 
custom features that standard data science approaches miss:

| Feature | Business Logic |
|---|---|
| `Compensation_Ratio` | Employee salary vs job level average — below 0.85 = flight risk |
| `Hike_Band` | Low (≤11%), Medium (12-14%), High (15%+) increment bands |
| `Overtime_LowHike_Risk` | Overtime + low hike = highest attrition risk combination |
| `Tenure_Per_Level` | Years per job level — high value = stagnation risk |
| `Total_Comp_Score` | Holistic CTC score combining salary, stock options & hike |
| `Exp_Pay_Ratio` | Monthly income vs total experience — underpaid seniors |

---

## 🤖 Model Performance

| Model | Accuracy | ROC AUC |
|---|---|---|
| Random Forest | 81% | 0.7749 |
| **XGBoost** ✅ | **83%** | **0.7761** |

**XGBoost selected as final model** — above industry standard AUC of 0.75

### Top Predictive Features
- Job Level
- Overtime Flag *(engineered)*
- Total Working Years
- Stock Option Level
- Total Compensation Score *(engineered)*

---

## 📊 Key Business Insights

- **Sales department** has highest attrition rate at **20.63%**
- Employees working **overtime** are **3x more likely** to leave
- Employees with **low salary hike (≤11%)** show significantly higher attrition
- **No promotion in 3+ years** is a strong stagnation and attrition signal

---

## 🖥️ Streamlit Dashboard

Three interactive tabs:

1. **HR Analytics Dashboard** — Department, overtime, salary, tenure analysis
2. **Attrition Risk Report** — High/Medium/Low risk employee breakdown
3. **Predict Employee Risk** — Real-time attrition prediction with risk gauge

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Database | MySQL + SQLAlchemy |
| Visualization | Plotly, Seaborn, Matplotlib |
| Dashboard | Streamlit |
| IDE | VS Code |

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/narendovi/attrition-payroll-risk.git
cd attrition-payroll-risk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# Run the dashboard
streamlit run app/streamlit_app.py
```

---

## 📁 Dataset

**IBM HR Analytics Employee Attrition Dataset**
- 1,470 employee records
- 35 features
- Source: [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

---

## 👤 Author

**Narendran**  
HR & Payroll Professional → Data Science  
7.5 years experience in Indian Payroll Processing  
Currently enrolled: Data Science with AI & ML — GUVI HCL  

📧 narendovi@gmail.com  
🔗 [GitHub](https://github.com/narendovi)  
📍 Chennai, India