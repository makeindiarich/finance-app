import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Financial Planner", layout="wide")

st.title("📊 Personal Financial Planner")

# ---- Sidebar Inputs ----
st.sidebar.header("Income")
salary = st.sidebar.number_input("Annual Salary (₹)", min_value=0, value=800000, step=50000)
bonus = st.sidebar.number_input("Annual Bonus (₹)", min_value=0, value=100000, step=10000)
rent_income = st.sidebar.number_input("Annual Rent Income (₹)", min_value=0, value=0, step=10000)
dividends = st.sidebar.number_input("Annual Dividends (₹)", min_value=0, value=0, step=10000)
income_growth = st.sidebar.slider("Income Growth % per year", 0.0, 15.0, 5.0)

st.sidebar.header("Expenses")
expenses = st.sidebar.number_input("Annual Expenses (₹)", min_value=0, value=400000, step=50000)
expense_inflation = st.sidebar.slider("Expense Inflation %", 0.0, 15.0, 6.0)

st.sidebar.header("Assets")
cash_start = st.sidebar.number_input("Cash & Bank (₹)", 0, 1000000, 200000)
equity_start = st.sidebar.number_input("Equity Investments (₹)", 0, 5000000, 500000)
debt_start = st.sidebar.number_input("Debt / FD (₹)", 0, 5000000, 200000)
real_estate = st.sidebar.number_input("Real Estate Value (₹)", 0, 10000000, 0)

return_cash = st.sidebar.slider("Cash Return %", 0.0, 10.0, 3.0)
return_equity = st.sidebar.slider("Equity Return %", 0.0, 20.0, 12.0)
return_debt = st.sidebar.slider("Debt Return %", 0.0, 15.0, 7.0)
return_real = st.sidebar.slider("Real Estate Growth %", 0.0, 15.0, 5.0)

st.sidebar.header("Loan")
loan_amt = st.sidebar.number_input("Loan Amount (₹)", 0, 10000000, 0, step=50000)
loan_rate = st.sidebar.slider("Loan Interest %", 0.0, 20.0, 8.0)
loan_years = st.sidebar.slider("Loan Tenure (years)", 0, 30, 0)

st.sidebar.header("Projection Settings")
horizon = st.sidebar.slider("Projection Horizon (years)", 5, 50, 30)

# ---- Simulation ----
years = list(range(0, horizon + 1))

# Income projection
income = [(salary + bonus + rent_income + dividends) * ((1 + income_growth/100) ** yr) for yr in years]
# Expense projection
expenses_proj = [expenses * ((1 + expense_inflation/100) ** yr) for yr in years]
# Loan EMI
emi = 0
if loan_amt > 0 and loan_years > 0:
    n = loan_years * 12
    r = loan_rate/100/12
    emi = loan_amt * r * (1 + r) ** n / ((1 + r) ** n - 1)
annual_emi = emi * 12

# Wealth buckets
cash, equity, debt, real = [cash_start], [equity_start], [debt_start], [real_estate]

for yr in range(1, horizon+1):
    net_cf = income[yr] - expenses_proj[yr] - annual_emi
    # Assume 50% net CF to equity, 30% debt, 20% cash
    eq_new = equity[-1] * (1 + return_equity/100) + 0.5 * net_cf
    debt_new = debt[-1] * (1 + return_debt/100) + 0.3 * net_cf
    cash_new = cash[-1] * (1 + return_cash/100) + 0.2 * net_cf
    real_new = real[-1] * (1 + return_real/100)

    equity.append(eq_new); debt.append(debt_new); cash.append(cash_new); real.append(real_new)

# Combine results
df = pd.DataFrame({
    "Year": years,
    "Income": income,
    "Expenses": expenses_proj,
    "Net Cash Flow": np.array(income) - np.array(expenses_proj) - annual_emi,
    "Cash": cash,
    "Debt": debt,
    "Equity": equity,
    "RealEstate": real
})
df["Total Wealth"] = df["Cash"] + df["Debt"] + df["Equity"] + df["RealEstate"]

# ---- Dashboard ----
st.subheader("📈 Wealth Projection")
st.line_chart(df.set_index("Year")[["Cash","Debt","Equity","RealEstate","Total Wealth"]])

st.subheader("💰 Cash Flow Projection")
st.bar_chart(df.set_index("Year")[["Income","Expenses","Net Cash Flow"]])

st.subheader("📊 Summary (Year 0 vs Year End)")
col1, col2 = st.columns(2)
col1.metric("Starting Wealth", f"₹{df['Total Wealth'].iloc[0]:,.0f}")
col2.metric("Wealth After Horizon", f"₹{df['Total Wealth'].iloc[-1]:,.0f}")
st.dataframe(df.style.format("{:,.0f}"))
