from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

layout = html.Div([
    html.H2("💸 Monthly Expense Breakdown"),
    html.P("Enter your expenses:"),
    dcc.Input(id="rent", type="number", placeholder="Rent", value=1000),
    dcc.Input(id="food", type="number", placeholder="Food", value=500),
    dcc.Input(id="transport", type="number", placeholder="Transport", value=200),
    dcc.Input(id="others", type="number", placeholder="Others", value=300),
    html.Button("Analyze", id="analyze_btn"),
    dcc.Graph(id="expense_pie")
], style={"padding":"20px"})

@callback(
    Output("expense_pie", "figure"),
    Input("analyze_btn", "n_clicks"),
    Input("rent", "value"),
    Input("food", "value"),
    Input("transport", "value"),
    Input("others", "value"),
    prevent_initial_call=True
)
def update_expense_pie(n_clicks, rent, food, transport, others):
    df = pd.DataFrame({
        "Category":["Rent","Food","Transport","Others"],
        "Amount":[rent, food, transport, others]
    })
    fig = px.pie(df, names="Category", values="Amount", title="Expense Breakdown")
    fig.update_layout(paper_bgcolor="#1e1e1e", font_color="white")
    return fig
