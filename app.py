import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Financial Planner", page_icon="💰", layout="wide")

# ----------------------------
# App Title
# ----------------------------
st.title("💰 Long-Term Wealth & Cash Flow Planner")
st.markdown("### Plan your financial future with interactive projections")

# ----------------------------
# User Inputs
# ----------------------------
st.sidebar.header("📊 Input Your Details")

initial_investment = st.sidebar.number_input("Initial Investment (₹)", min_value=0, value=100000)
monthly_investment = st.sidebar.number_input("Monthly Investment (₹)", min_value=0, value=10000)
expected_return = st.sidebar.slider("Expected Annual Return (%)", 1.0, 20.0, 12.0)
years = st.sidebar.slider("Investment Duration (Years)", 1, 50, 20)

# ----------------------------
# Calculations
# ----------------------------
months = years * 12
monthly_rate = expected_return / 100 / 12

wealth = []
cashflow = []

future_value = initial_investment
for month in range(1, months + 1):
    future_value = future_value * (1 + monthly_rate) + monthly_investment
    wealth.append(future_value)
    cashflow.append(monthly_investment * month + initial_investment)

df = pd.DataFrame({
    "Month": range(1, months + 1),
    "Wealth Projection": wealth,
    "Cash Invested": cashflow
})

df["Year"] = df["Month"] / 12

# ----------------------------
# Charts (Dark Mode with Plotly)
# ----------------------------
st.subheader("📈 Wealth Growth Over Time")

fig1 = px.line(df, x="Year", y="Wealth Projection", title="Projected Wealth Over Time")
fig1.update_layout(template="plotly_dark", xaxis_title="Years", yaxis_title="₹ Value")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.line(df, x="Year", y=["Wealth Projection", "Cash Invested"],
               title="Wealth vs Cash Invested")
fig2.update_layout(template="plotly_dark", xaxis_title="Years", yaxis_title="₹ Value")
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Final Numbers
# ----------------------------
st.subheader("💡 Summary")
st.metric("Total Invested", f"₹{cashflow[-1]:,.0f}")
st.metric("Projected Wealth", f"₹{wealth[-1]:,.0f}")
st.metric("Profit / Gains", f"₹{wealth[-1] - cashflow[-1]:,.0f}")
