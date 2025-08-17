import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server   # Required for Render deployment

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    style={"display": "flex", "height": "100vh", "backgroundColor": "#121212", "color": "white", "fontFamily": "Arial"},
    children=[

        # Left Sidebar - Inputs
        html.Div(
            style={"width": "30%", "padding": "30px", "backgroundColor": "#1e1e1e", "boxShadow": "2px 0px 5px rgba(0,0,0,0.5)"},
            children=[
                html.H2("💰 Finance Planner", style={"color": "#FFD700", "textAlign": "center"}),

                html.Label("Initial Investment (₹)", style={"marginTop": "15px"}),
                dcc.Input(id="initial_invest", type="number", value=500000, style={"width": "100%", "padding": "10px"}),

                html.Label("Monthly Contribution (₹)", style={"marginTop": "15px"}),
                dcc.Input(id="monthly_invest", type="number", value=20000, style={"width": "100%", "padding": "10px"}),

                html.Label("Expected Annual Return (%)", style={"marginTop": "15px"}),
                dcc.Input(id="annual_return", type="number", value=10, style={"width": "100%", "padding": "10px"}),

                html.Label("Inflation Rate (%)", style={"marginTop": "15px"}),
                dcc.Input(id="inflation_rate", type="number", value=6, style={"width": "100%", "padding": "10px"}),

                html.Label("Monthly Expenses (₹)", style={"marginTop": "15px"}),
                dcc.Input(id="monthly_expense", type="number", value=40000, style={"width": "100%", "padding": "10px"}),

                html.Label("Investment Horizon (Years)", style={"marginTop": "15px"}),
                dcc.Input(id="years", type="number", value=20, style={"width": "100%", "padding": "10px"}),

                html.Div(id="summary", style={"marginTop": "20px", "fontSize": "18px", "color": "#90EE90"})
            ]
        ),

        # Right Side - Graphs
        html.Div(
            style={"width": "70%", "padding": "30px"},
            children=[
                dcc.Graph(id="wealth_graph", style={"height": "45vh"}),
                dcc.Graph(id="cashflow_graph", style={"height": "45vh"})
            ]
        )
    ]
)


# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    [Output("wealth_graph", "figure"),
     Output("cashflow_graph", "figure"),
     Output("summary", "children")],
    [Input("initial_invest", "value"),
     Input("monthly_invest", "value"),
     Input("annual_return", "value"),
     Input("inflation_rate", "value"),
     Input("monthly_expense", "value"),
     Input("years", "value")]
)
def update_graphs(initial_invest, monthly_invest, annual_return, inflation_rate, monthly_expense, years):
    months = years * 12
    rate = (annual_return / 100) / 12
    inflation = (inflation_rate / 100) / 12

    # Wealth projection
    wealth = [initial_invest]
    for m in range(1, months + 1):
        prev = wealth[-1]
        future = prev * (1 + rate) + monthly_invest
        wealth.append(future)

    # Expenses projection (adjusted for inflation)
    expenses = []
    for m in range(months + 1):
        adj_expense = monthly_expense * ((1 + inflation) ** m)
        expenses.append(adj_expense)

    # Wealth Graph
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=wealth, mode="lines", name="Projected Wealth", line=dict(color="#FFD700", width=3)))
    fig1.update_layout(title="📈 Wealth Projection", paper_bgcolor="#121212", plot_bgcolor="#121212",
                       font=dict(color="white"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    # Cashflow Graph
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=expenses, mode="lines", name="Monthly Expenses", line=dict(color="#FF6347", width=3)))
    fig2.update_layout(title="💸 Expense Growth (Inflation Adjusted)", paper_bgcolor="#121212", plot_bgcolor="#121212",
                       font=dict(color="white"), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    summary = f"After {years} years, projected wealth ≈ ₹{wealth[-1]:,.0f}"

    return fig1, fig2, summary


# Run app locally
if __name__ == "__main__":
    app.run_server(debug=True)
