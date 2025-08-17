from dash import html, dcc, Input, Output, callback
import pandas as pd

layout = html.Div([
    html.H2("📈 Cashflow Projection"),
    html.Div([
        "Initial Investment: ",
        dcc.Input(id="init_invest", type="number", value=10000, step=1000)
    ]),
    html.Div([
        "Monthly Contribution: ",
        dcc.Input(id="monthly_contrib", type="number", value=500, step=100)
    ]),
    html.Div([
        "Annual Growth Rate (%): ",
        dcc.Input(id="growth_rate", type="number", value=7, step=0.5)
    ]),
    html.Button("Run Projection", id="run_btn"),
    dcc.Graph(id="cashflow_chart"),
    html.Button("Download Excel", id="btn_download"),
    dcc.Download(id="download-dataframe-xlsx")
], style={"padding":"20px"})

@callback(
    Output("cashflow_chart", "figure"),
    Input("run_btn", "n_clicks"),
    Input("init_invest", "value"),
    Input("monthly_contrib", "value"),
    Input("growth_rate", "value"),
    prevent_initial_call=True
)
def update_projection(n_clicks, init_invest, monthly_contrib, growth_rate):
    years = list(range(1, 21))
    values = []
    wealth = init_invest
    for y in years:
        wealth = wealth * (1 + growth_rate/100) + monthly_contrib*12
        values.append(wealth)

    df = pd.DataFrame({"Year": years, "Projected Wealth": values})
    fig = {
        "data": [{"x": df["Year"], "y": df["Projected Wealth"], "type": "line", "name": "Wealth"}],
        "layout": {"title": "20-Year Wealth Projection", "paper_bgcolor":"#1e1e1e", "plot_bgcolor":"#1e1e1e", "font":{"color":"white"}}
    }
    return fig

@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_download", "n_clicks"),
    Input("init_invest", "value"),
    Input("monthly_contrib", "value"),
    Input("growth_rate", "value"),
    prevent_initial_call=True
)
def download_excel(n_clicks, init_invest, monthly_contrib, growth_rate):
    years = list(range(1, 21))
    values = []
    wealth = init_invest
    for y in years:
        wealth = wealth * (1 + growth_rate/100) + monthly_contrib*12
        values.append(wealth)

    df = pd.DataFrame({"Year": years, "Projected Wealth": values})
    return dcc.send_data_frame(df.to_excel, "cashflow.xlsx", index=False)
