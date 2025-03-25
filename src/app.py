import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Set page config
st.set_page_config(page_title='Diabetes Prediction Dashboard', layout='wide')

# Title
st.markdown("# 🏥 Diabetes Prediction Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
patient_name = st.sidebar.text_input("Patient Name", "John Doe")
age = st.sidebar.slider("Age", 18, 100, 50)
bmi = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
hba1c = st.sidebar.slider("HbA1c (%)", 4.0, 12.0, 5.5)
systolic_bp = st.sidebar.slider("Systolic BP", 80, 200, 120)
diastolic_bp = st.sidebar.slider("Diastolic BP", 40, 120, 80)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Non-Smoker", "Former Smoker", "Current Smoker"])

# Simulated Data
data_size = 200
np.random.seed(42)
df = pd.DataFrame({
    "Age": np.random.randint(18, 100, data_size),
    "BMI": np.random.uniform(18, 40, data_size),
    "HbA1c": np.random.uniform(4.5, 12, data_size),
    "Systolic BP": np.random.randint(90, 180, data_size),
    "Diastolic BP": np.random.randint(60, 110, data_size),
    "Smoking Status": np.random.choice(["Non-Smoker", "Former Smoker", "Current Smoker"], data_size),
    "Diabetes Risk": np.random.choice([0, 1], data_size, p=[0.7, 0.3])  # 0: No Diabetes, 1: Diabetes
})

# Train Logistic Regression Model
X = df[["Age", "BMI", "HbA1c", "Systolic BP", "Diastolic BP"]]
y = df["Diabetes Risk"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = LogisticRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

# Predict Diabetes Risk for the User Input
user_data = np.array([[age, bmi, hba1c, systolic_bp, diastolic_bp]])
user_data_scaled = scaler.transform(user_data)
user_prediction = model.predict(user_data_scaled)[0]
user_risk = "High" if user_prediction == 1 else "Low"

# Display Patient Information
st.markdown(f"### 🧑‍⚕️ Patient: {patient_name}")
st.markdown(f"**Predicted Diabetes Risk: {user_risk}**")

# Key Metrics
st.markdown("### 📊 Analysis Results")
col1, col2, col3 = st.columns(3)
col1.metric("Average BMI", f"{df['BMI'].mean():.1f}")
col2.metric("Average HbA1c", f"{df['HbA1c'].mean():.1f}")
col3.metric("Model Accuracy", f"{accuracy * 100:.2f}%")

col1, col2 = st.columns(2)
col1.metric("Smoking Prevalence", f"{(df['Smoking Status'] != 'Non-Smoker').mean() * 100:.1f}%")
col2.metric("Diabetes Prevalence", f"{df['Diabetes Risk'].mean() * 100:.1f}%")

# Two Charts in One Row
st.markdown("### 📊 Diabetes Risk & Healthcare Trends")
col1, col2 = st.columns(2)
fig_pie = px.pie(df, names=df["Diabetes Risk"].map({0: "Low", 1: "High"}), title="Diabetes Risk Distribution", color_discrete_sequence=px.colors.sequential.RdBu)
col1.plotly_chart(fig_pie, use_container_width=True)
fig_box = px.box(df, x="Smoking Status", y="HbA1c", color="Smoking Status", title="HbA1c Levels by Smoking Status", template="plotly")
col2.plotly_chart(fig_box, use_container_width=True)

# Additional Charts
st.markdown("### 📈 Blood Pressure & Healthcare Trends")
col1, col2 = st.columns(2)
fig_bp = px.scatter(df, x="Systolic BP", y="Diastolic BP", color=df["Diabetes Risk"].map({0: "Low", 1: "High"}), title="Blood Pressure Distribution", template="plotly_dark")
col1.plotly_chart(fig_bp, use_container_width=True)
fig_expense = px.histogram(df, x="BMI", title="BMI Distribution", template="plotly", color_discrete_sequence=["#FF6361"])
col2.plotly_chart(fig_expense, use_container_width=True)

# New Visualization: Diabetes Risk by Age Group
st.markdown("### 📊 Diabetes Risk by Age Group")
col1, col2 = st.columns(2)
# Create age groups and convert intervals to string labels
age_bins = [18, 30, 50, 70, 100]
age_labels = ["18-30", "31-50", "51-70", "71-100"]
df["Age Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels)

# Group by Age Group and calculate the mean Diabetes Risk
df_age_grouped = df.groupby("Age Group")["Diabetes Risk"].mean().reset_index()

# Create the bar chart
fig_age = px.bar(df_age_grouped, x="Age Group", y="Diabetes Risk", title="Diabetes Risk by Age Group", template="plotly", color_discrete_sequence=["#58508D"])
col1.plotly_chart(fig_age, use_container_width=True)



# New Visualization: Blood Pressure Box Plot
fig_bp_box = px.box(df, y=["Systolic BP", "Diastolic BP"], title="Blood Pressure Distribution", template="plotly")
col2.plotly_chart(fig_bp_box, use_container_width=True)

st.markdown("---")
st.markdown("**Designed for Predicting and Analyzing Diabetes Risk** 🚀")
