import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# App Setup
# ----------------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deployment (Heroku, Render, etc.)

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    style={"backgroundColor": "#111111", "color": "white", "padding": "20px"},
    children=[
        html.H1("💰 Long-Term Wealth & Cash Flow Planner", style={"textAlign": "center"}),

        # Inputs
        html.Div([
            html.Label("Initial Investment (₹):"),
            dcc.Input(id="initial_investment", type="number", value=100000, style={"marginBottom": "10px"}),

            html.Label("Monthly Investment (₹):"),
            dcc.Input(id="monthly_investment", type="number", value=10000, style={"marginBottom": "10px"}),

            html.Label("Expected Annual Return (%):"),
            dcc.Slider(id="expected_return", min=1, max=20, step=0.5, value=12,
                       marks={i: f"{i}%" for i in range(1, 21)}),

            html.Label("Investment Duration (Years):"),
            dcc.Slider(id="years", min=1, max=50, step=1, value=20,
                       marks={i: str(i) for i in range(0, 55, 5)})
        ], style={"padding": "20px", "backgroundColor": "#222222", "borderRadius": "10px"}),

        html.Br(),

        # Charts
        dcc.Graph(id="wealth_chart"),
        dcc.Graph(id="compare_chart"),

        # Summary
        html.Div(id="summary", style={"textAlign": "center", "marginTop": "20px", "fontSize": "20px"})
    ]
)

# ----------------------------
# Callback for calculations
# ----------------------------
@app.callback(
    [Output("wealth_chart", "figure"),
     Output("compare_chart", "figure"),
     Output("summary", "children")],
    [Input("initial_investment", "value"),
     Input("monthly_investment", "value"),
     Input("expected_return", "value"),
     Input("years", "value")]
)
def update_projection(initial_investment, monthly_investment, expected_return, years):
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

    # Chart 1: Wealth over time
    fig1 = px.line(df, x="Year", y="Wealth Projection", title="Projected Wealth Over Time")
    fig1.update_layout(template="plotly_dark", xaxis_title="Years", yaxis_title="₹ Value")

    # Chart 2: Wealth vs Cash
    fig2 = px.line(df, x="Year", y=["Wealth Projection", "Cash Invested"],
                   title="Wealth vs Cash Invested")
    fig2.update_layout(template="plotly_dark", xaxis_title="Years", yaxis_title="₹ Value")

    # Summary
    total_invested = cashflow[-1]
    projected_wealth = wealth[-1]
    profit = projected_wealth - total_invested
    summary_text = [
        html.P(f"💵 Total Invested: ₹{total_invested:,.0f}"),
        html.P(f"📈 Projected Wealth: ₹{projected_wealth:,.0f}"),
        html.P(f"💡 Profit / Gains: ₹{profit:,.0f}")
    ]

    return fig1, fig2, summary_text


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
