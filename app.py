from dash import Dash, dcc, html, Input, Output
#import dash_auth
from layouts import home, cashflow, expenses

# --- Setup App ---
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deployment

# --- Basic Authentication ---
VALID_USERNAME_PASSWORD_PAIRS = {
    "admin": "password123",
    "guest": "guest123"
}
#auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# --- Router ---
app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/cashflow":
        return cashflow.layout
    elif pathname == "/expenses":
        return expenses.layout
    return home.layout

if __name__ == "__main__":
    app.run_server(debug=True)
