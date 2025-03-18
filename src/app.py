import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title='Healthcare Analytics Dashboard', layout='wide')

# Title
st.markdown("##Healthcare Analytics Dashboard")

st.sidebar.header("Filter Options")
age = st.sidebar.slider("Age", 18, 100, 50)
bmi = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
hba1c = st.sidebar.slider("HbA1c (%)", 4.0, 12.0, 5.5)
systolic_bp = st.sidebar.slider("Systolic BP", 80, 200, 120)
diastolic_bp = st.sidebar.slider("Diastolic BP", 40, 120, 80)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Non-Smoker", "Former Smoker", "Current Smoker"])
income = st.sidebar.number_input("Income ($)", min_value=1000, max_value=500000, value=50000, step=1000)
healthcare_expense = st.sidebar.number_input("Healthcare Expenses ($)", min_value=0, max_value=100000, value=5000, step=500)
healthcare_coverage = st.sidebar.number_input("Healthcare Coverage ($)", min_value=0, max_value=200000, value=90000, step=1000)

risk_prob = np.random.uniform(50, 90) 
trend = np.random.uniform(5, 20)
predicted_cost = np.random.randint(1000, 20000)

data = {
    "Risk Level": "Low" if hba1c < 6 else "High",
    "Readmission Risk": f"{risk_prob:.2f}%",
    "Utilization Trend": f"{trend:.1f}%",
    "Predicted Cost": f"${predicted_cost:,}"
}

df = pd.DataFrame([data])

# Display Data
st.markdown("### 🔍 Patient Analysis")
st.write(df)

st.markdown("### 📊 Analysis Results")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Diabetes Risk", df['Risk Level'][0])
col2.metric("Readmission Risk", df['Readmission Risk'][0])
col3.metric("Utilization Trend", df['Utilization Trend'][0])
col4.metric("Predicted Cost", df['Predicted Cost'][0])
