import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
import pickle
import numpy as np
from dotenv import load_dotenv
import os

# ── Config ──────────────────────────────────────────────────────────────
load_dotenv('/Users/naren/Projects/attrition-payroll-risk/.env')

st.set_page_config(
    page_title="Employee Attrition & Payroll Risk Predictor",
    page_icon="👥",
    layout="wide"
)

# ── DB Connection ────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )

engine = get_engine()

# ── Load Data ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    query = """
        SELECT e.*, f.Attrition_Flag, f.Compensation_Ratio, f.Hike_Band,
               f.OverTime_Flag, f.Overtime_LowHike_Risk, f.Tenure_Per_Level,
               f.Total_Comp_Score, f.Exp_Pay_Ratio,
               p.Attrition_Probability, p.Attrition_Prediction, p.Risk_Category
        FROM employee_raw e
        JOIN employee_features f ON e.EmployeeNumber = f.EmployeeNumber
        JOIN employee_predictions p ON e.EmployeeNumber = p.EmployeeNumber
    """
    return pd.read_sql(query, con=engine)

@st.cache_resource
def load_model():
    with open('/Users/naren/Projects/attrition-payroll-risk/models/attrition_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('/Users/naren/Projects/attrition-payroll-risk/models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('/Users/naren/Projects/attrition-payroll-risk/models/feature_cols.pkl', 'rb') as f:
        features = pickle.load(f)
    return model, scaler, features

df = load_data()
model, scaler, feature_cols = load_model()

# ── Header ───────────────────────────────────────────────────────────────
st.title("👥 Employee Attrition & Payroll Risk Predictor")
st.markdown("Built using IBM HR Dataset | ML Model: XGBoost | Domain: Payroll Analytics")
st.divider()

# ── Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊 HR Analytics Dashboard",
    "⚠️ Attrition Risk Report",
    "🔮 Predict Employee Risk"
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1: HR Analytics Dashboard
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("📊 Workforce Overview")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    total = len(df)
    attrited = df['Attrition_Flag'].sum()
    attrition_rate = round(attrited / total * 100, 1)
    avg_salary = round(df['MonthlyIncome'].mean(), 0)

    col1.metric("Total Employees", total)
    col2.metric("Attrition Count", int(attrited))
    col3.metric("Attrition Rate", f"{attrition_rate}%")
    col4.metric("Avg Monthly Income", f"₹{int(avg_salary):,}")

    st.divider()

    # Row 1: Department & Overtime
    col1, col2 = st.columns(2)

    with col1:
        dept_data = df.groupby('Department').agg(
            Total=('EmployeeNumber', 'count'),
            Attrited=('Attrition_Flag', 'sum')
        ).reset_index()
        dept_data['Attrition_Rate'] = round(
            dept_data['Attrited'] / dept_data['Total'] * 100, 1)

        fig = px.bar(dept_data, x='Department', y='Attrition_Rate',
                     color='Attrition_Rate', color_continuous_scale='Reds',
                     title='Attrition Rate by Department (%)',
                     text='Attrition_Rate')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        ot_data = df.groupby('OverTime').agg(
            Total=('EmployeeNumber', 'count'),
            Attrited=('Attrition_Flag', 'sum')
        ).reset_index()
        ot_data['Attrition_Rate'] = round(
            ot_data['Attrited'] / ot_data['Total'] * 100, 1)

        fig = px.bar(ot_data, x='OverTime', y='Attrition_Rate',
                     color='OverTime', title='Attrition Rate by Overtime (%)',
                     text='Attrition_Rate', color_discrete_sequence=['#2ecc71','#e74c3c'])
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # Row 2: Salary & Hike Band
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(df, x='Attrition', y='MonthlyIncome',
                     color='Attrition', title='Monthly Income vs Attrition',
                     color_discrete_sequence=['#3498db','#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        hike_data = df.groupby('Hike_Band').agg(
            Total=('EmployeeNumber', 'count'),
            Attrited=('Attrition_Flag', 'sum')
        ).reset_index()
        hike_data['Attrition_Rate'] = round(
            hike_data['Attrited'] / hike_data['Total'] * 100, 1)

        fig = px.bar(hike_data, x='Hike_Band', y='Attrition_Rate',
                     color='Hike_Band', title='Attrition Rate by Salary Hike Band (%)',
                     text='Attrition_Rate',
                     color_discrete_sequence=['#e74c3c','#f39c12','#2ecc71'])
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # Row 3: Tenure & Job Level
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x='YearsAtCompany', color='Attrition',
                           barmode='overlay', title='Tenure Distribution by Attrition',
                           color_discrete_sequence=['#3498db','#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        jl_data = df.groupby('JobLevel').agg(
            Total=('EmployeeNumber', 'count'),
            Attrited=('Attrition_Flag', 'sum')
        ).reset_index()
        jl_data['Attrition_Rate'] = round(
            jl_data['Attrited'] / jl_data['Total'] * 100, 1)

        fig = px.bar(jl_data, x='JobLevel', y='Attrition_Rate',
                     color='Attrition_Rate', color_continuous_scale='Reds',
                     title='Attrition Rate by Job Level (%)',
                     text='Attrition_Rate')
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 2: Attrition Risk Report
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("⚠️ Employee Attrition Risk Report")

    # Risk Summary KPIs
    col1, col2, col3 = st.columns(3)
    high_risk = len(df[df['Risk_Category'] == 'High Risk'])
    medium_risk = len(df[df['Risk_Category'] == 'Medium Risk'])
    low_risk = len(df[df['Risk_Category'] == 'Low Risk'])

    col1.metric("🔴 High Risk", high_risk)
    col2.metric("🟡 Medium Risk", medium_risk)
    col3.metric("🟢 Low Risk", low_risk)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # Risk Distribution Pie
        risk_counts = df['Risk_Category'].value_counts().reset_index()
        risk_counts.columns = ['Risk_Category', 'Count']
        fig = px.pie(risk_counts, names='Risk_Category', values='Count',
                     title='Risk Category Distribution',
                     color='Risk_Category',
                     color_discrete_map={
                         'High Risk': '#e74c3c',
                         'Medium Risk': '#f39c12',
                         'Low Risk': '#2ecc71'
                     })
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Attrition Probability Distribution
        fig = px.histogram(df, x='Attrition_Probability', color='Risk_Category',
                           title='Attrition Probability Distribution',
                           color_discrete_map={
                               'High Risk': '#e74c3c',
                               'Medium Risk': '#f39c12',
                               'Low Risk': '#2ecc71'
                           })
        st.plotly_chart(fig, use_container_width=True)

    # High Risk Employee Table
    st.subheader("🔴 High Risk Employees")
    high_risk_df = df[df['Risk_Category'] == 'High Risk'][[
        'EmployeeNumber', 'Department', 'JobRole', 'MonthlyIncome',
        'YearsAtCompany', 'OverTime', 'Hike_Band',
        'Attrition_Probability', 'Risk_Category'
    ]].sort_values('Attrition_Probability', ascending=False)

    high_risk_df['Attrition_Probability'] = (
        high_risk_df['Attrition_Probability'] * 100
    ).round(1).astype(str) + '%'

    st.dataframe(high_risk_df, use_container_width=True)

    # Filter by Department
    st.subheader("🔍 Filter Risk by Department")
    dept_filter = st.selectbox("Select Department", df['Department'].unique())
    filtered = df[df['Department'] == dept_filter][[
        'EmployeeNumber', 'JobRole', 'MonthlyIncome',
        'Risk_Category', 'Attrition_Probability'
    ]].sort_values('Attrition_Probability', ascending=False)

    filtered['Attrition_Probability'] = (
        filtered['Attrition_Probability'] * 100
    ).round(1).astype(str) + '%'

    st.dataframe(filtered, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3: Predict Employee Risk
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🔮 Predict Attrition Risk for an Employee")
    st.markdown("Enter employee details below to get an instant attrition risk prediction.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Personal Details**")
        age = st.slider("Age", 18, 60, 30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        distance = st.slider("Distance From Home (km)", 1, 29, 10)
        num_companies = st.slider("Number of Companies Worked", 0, 9, 2)

    with col2:
        st.markdown("**Payroll & Compensation**")
        monthly_income = st.number_input("Monthly Income (₹)", 1000, 20000, 5000, step=500)
        salary_hike = st.slider("Salary Hike %", 11, 25, 13)
        job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
        stock_option = st.selectbox("Stock Option Level", [0, 1, 2, 3])
        overtime = st.selectbox("Overtime", ["Yes", "No"])

    with col3:
        st.markdown("**Work Experience**")
        total_working_years = st.slider("Total Working Years", 0, 40, 8)
        years_at_company = st.slider("Years at Company", 0, 40, 4)
        years_in_role = st.slider("Years in Current Role", 0, 18, 3)
        years_since_promo = st.slider("Years Since Last Promotion", 0, 15, 2)
        years_with_manager = st.slider("Years With Current Manager", 0, 17, 3)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Satisfaction Scores**")
        job_satisfaction = st.selectbox("Job Satisfaction (1-4)", [1, 2, 3, 4], index=2)
        env_satisfaction = st.selectbox("Environment Satisfaction (1-4)", [1, 2, 3, 4], index=2)
        work_life_balance = st.selectbox("Work Life Balance (1-4)", [1, 2, 3, 4], index=2)
        relationship_sat = st.selectbox("Relationship Satisfaction (1-4)", [1, 2, 3, 4], index=2)
        performance = st.selectbox("Performance Rating (1-4)", [3, 4], index=0)

    with col2:
        st.markdown("**Department & Role**")
        department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        job_role = st.selectbox("Job Role", [
            "Sales Executive", "Research Scientist", "Laboratory Technician",
            "Manufacturing Director", "Healthcare Representative", "Manager",
            "Sales Representative", "Research Director", "Human Resources"
        ])
        education_field = st.selectbox("Education Field", [
            "Life Sciences", "Medical", "Marketing",
            "Technical Degree", "Human Resources", "Other"
        ])
        business_travel = st.selectbox("Business Travel", [
            "Non-Travel", "Travel_Rarely", "Travel_Frequently"
        ])
        training_times = st.slider("Training Times Last Year", 0, 6, 2)

    with col3:
        st.markdown(" ")

    st.divider()

    if st.button("🔮 Predict Attrition Risk", use_container_width=True):

        # Encode categoricals
        gender_enc = 1 if gender == "Male" else 0
        overtime_flag = 1 if overtime == "Yes" else 0
        marital_enc = {"Single": 2, "Married": 1, "Divorced": 0}[marital_status]
        dept_enc = {"Sales": 2, "Research & Development": 1, "Human Resources": 0}[department]
        travel_enc = {"Non-Travel": 0, "Travel_Rarely": 2, "Travel_Frequently": 1}[business_travel]
        role_enc = {
            "Sales Executive": 7, "Research Scientist": 6,
            "Laboratory Technician": 3, "Manufacturing Director": 4,
            "Healthcare Representative": 2, "Manager": 5,
            "Sales Representative": 8, "Research Director": 5,
            "Human Resources": 1
        }.get(job_role, 0)
        edu_enc = {
            "Life Sciences": 3, "Medical": 4, "Marketing": 2,
            "Technical Degree": 5, "Human Resources": 0, "Other": 1
        }.get(education_field, 0)

        # Hike band
        if salary_hike <= 11:
            hike_band = 'Low'
            hike_enc = 1
        elif salary_hike <= 14:
            hike_band = 'Medium'
            hike_enc = 2
        else:
            hike_band = 'High'
            hike_enc = 0

        # Engineered features
        avg_income_by_level = df.groupby('JobLevel')['MonthlyIncome'].mean()
        compensation_ratio = monthly_income / avg_income_by_level.get(job_level, monthly_income)
        overtime_lowhike_risk = 1 if (overtime_flag == 1 and hike_band == 'Low') else 0
        tenure_per_level = years_at_company / (job_level + 1)
        total_comp_score = monthly_income * 0.6 + stock_option * 1000 + salary_hike * 100
        exp_pay_ratio = monthly_income / (total_working_years + 1)

        # Build input
        input_data = pd.DataFrame([{
            'Age': age,
            'MonthlyIncome': monthly_income,
            'PercentSalaryHike': salary_hike,
            'JobLevel': job_level,
            'YearsAtCompany': years_at_company,
            'TotalWorkingYears': total_working_years,
            'YearsInCurrentRole': years_in_role,
            'YearsSinceLastPromotion': years_since_promo,
            'YearsWithCurrManager': years_with_manager,
            'DistanceFromHome': distance,
            'NumCompaniesWorked': num_companies,
            'TrainingTimesLastYear': training_times,
            'WorkLifeBalance': work_life_balance,
            'JobSatisfaction': job_satisfaction,
            'EnvironmentSatisfaction': env_satisfaction,
            'RelationshipSatisfaction': relationship_sat,
            'PerformanceRating': performance,
            'StockOptionLevel': stock_option,
            'Compensation_Ratio': compensation_ratio,
            'OverTime_Flag': overtime_flag,
            'Overtime_LowHike_Risk': overtime_lowhike_risk,
            'Tenure_Per_Level': tenure_per_level,
            'Total_Comp_Score': total_comp_score,
            'Exp_Pay_Ratio': exp_pay_ratio,
            'BusinessTravel_Enc': travel_enc,
            'Department_Enc': dept_enc,
            'EducationField_Enc': edu_enc,
            'Gender_Enc': gender_enc,
            'JobRole_Enc': role_enc,
            'MaritalStatus_Enc': marital_enc,
            'Hike_Band_Enc': hike_enc
        }])

        # Scale & predict
        input_scaled = scaler.transform(input_data[feature_cols])
        probability = model.predict_proba(input_scaled)[0][1]
        prediction = model.predict(input_scaled)[0]

        if probability >= 0.7:
            risk = "🔴 HIGH RISK"
            color = "red"
        elif probability >= 0.4:
            risk = "🟡 MEDIUM RISK"
            color = "orange"
        else:
            risk = "🟢 LOW RISK"
            color = "green"

        # Display result
        st.divider()
        col1, col2, col3 = st.columns(3)

        col1.metric("Attrition Probability", f"{round(probability * 100, 1)}%")
        col2.metric("Risk Category", risk)
        col3.metric("Prediction", "Will Leave ⚠️" if prediction == 1 else "Will Stay ✅")

        # Risk Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(probability * 100, 1),
            title={'text': "Attrition Risk Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 40], 'color': '#2ecc71'},
                    {'range': [40, 70], 'color': '#f39c12'},
                    {'range': [70, 100], 'color': '#e74c3c'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # Key Risk Factors
        st.subheader("📌 Key Risk Factors Identified")
        factors = []
        if overtime_flag == 1:
            factors.append("⚠️ Employee is working overtime")
        if hike_band == 'Low':
            factors.append("⚠️ Salary hike is below average (≤11%)")
        if overtime_lowhike_risk == 1:
            factors.append("🔴 Overtime + Low Hike — Highest Risk Combination")
        if compensation_ratio < 0.85:
            factors.append("⚠️ Earning significantly below job level average")
        if years_since_promo >= 3:
            factors.append("⚠️ No promotion in 3+ years — stagnation risk")
        if job_satisfaction <= 2:
            factors.append("⚠️ Low job satisfaction score")
        if distance > 20:
            factors.append("⚠️ High commute distance")

        if factors:
            for f in factors:
                st.warning(f)
        else:
            st.success("✅ No major risk factors identified for this employee.")