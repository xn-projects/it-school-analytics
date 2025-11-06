import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utils.my_palette import get_my_palette
from charts import build_sankey_chart
from data_prep import load_data, prepare_data, compute_kpi

# Load data
deals, calls, contacts, spend = load_data()
deals = prepare_data(deals)

colors = get_my_palette(as_dict=True)

# Dropdown options
product_options = ["Total"] + sorted(deals["Product"].unique())
edu_options = ["Total"] + sorted(deals["Education Type"].unique())


def make_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, style={"textAlign": "center"}),
            html.H3(f"{value:,}", style={"textAlign": "center", "color": color})
        ]),
        style={"borderRadius": "12px"}
    )


def make_kpi_cards(total, success, opened, closed):
    return dbc.Row([
        dbc.Col(make_card("Total Deals", total, colors["Cornflower"][4]), md=3),
        dbc.Col(make_card("Successful Deals", success, colors["Lime Green"][4]), md=3),
        dbc.Col(make_card("Opened Deals", opened, colors["Yellowsoft"][4]), md=3),
        dbc.Col(make_card("Closed Deals", closed, colors["Tomato"][4]), md=3),
    ], className="mb-4")


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.layout = dbc.Container([
    html.H2("IT School Analytics Dashboard", style={"textAlign": "center", "marginTop": "20px"}),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="product_filter",
            options=[{"label": p, "value": p} for p in product_options],
            value="Total",
            clearable=False,
        ), md=4),

        dbc.Col(dcc.Dropdown(
            id="edu_filter",
            options=[{"label": e, "value": e} for e in edu_options],
            value="Total",
            clearable=False,
        ), md=4),
    ], style={"marginBottom": "30px"}),

    html.Div(id="kpi_cards"),

    dcc.Graph(id="sankey_graph", style={"marginBottom": "40px"}),

], fluid=True)


@app.callback(
    [
        Output("kpi_cards", "children"),
        Output("sankey_graph", "figure")
    ],
    [
        Input("product_filter", "value"),
        Input("edu_filter", "value")
    ]
)
def update_dashboard(selected_product, selected_edu):
    df = deals.copy()

    if selected_edu != "Total":
        df = df[df["Education Type"] == selected_edu]

    if selected_product != "Total":
        df = df[df["Product"] == selected_product]

    total, success, opened, closed = compute_kpi(df)
    cards = make_kpi_cards(total, success, opened, closed)

    sankey_fig = build_sankey_chart(df)

    return cards, sankey_fig


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
