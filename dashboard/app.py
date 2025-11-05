import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from utils.my_palette import get_my_palette
from .data_prep import load_data, prepare_data, compute_kpi
from .charts import build_product_chart, build_education_chart


deals, calls, contacts, spend = load_data()
deals, agg_product, agg_edu = prepare_data(deals)

colors = get_my_palette(as_dict=True)
OPEN_COLOR = colors["Cornflower"][4]
DEALS_COLOR = colors["Lime Green"][4]
SUCCESS_COLOR = colors["Tomato"][4]

products = ['Total'] + sorted(agg_product['Product'].unique())

def make_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, style={"textAlign": "center"}),
            html.H3(f"{value:,}", style={"textAlign": "center", "color": color})
        ]),
        style={"borderRadius": "12px"}
    )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.layout = dbc.Container([
    html.H2("IT school analytics Dashboard", style={"textAlign": "center", "marginTop": "20px"}),

    dcc.Dropdown(
        id="product_filter",
        options=[{"label": p, "value": p} for p in products],
        value="Total",
        clearable=False,
        style={"width": "300px", "margin": "0 auto 30px auto"}
    ),

    html.Div(id="kpi_cards", style={"marginBottom": "30px"}),
    
    dcc.Graph(id="product_graph", style={"marginBottom": "40px"}),
    dcc.Graph(id="education_graph", style={"marginBottom": "40px"}),
    dcc.Graph(id="sankey_graph")
], fluid=True)

@app.callback(
    Output('kpi_cards', 'children'),
    Output('product_graph', 'figure'),
    Output('education_graph', 'figure'),
    Output('sankey_graph', 'figure'),
    Input('product_filter', 'value')
)
def update_dashboard(selected_product):
    total_deals, closed_deals, open_deals = compute_kpi(deals, selected_product)
    cards = make_kpi_cards(total_deals, closed_deals, open_deals)

    if selected_product == "Total":
        dfp = agg_product_total.copy()
    else:
        dfp = agg_product[agg_product['Product'] == selected_product]
    fig_product = build_product_chart(dfp)

    if selected_product == "Total":
        df_edu = agg_edu.copy()
    else:
        df_edu = agg_edu[agg_edu['Product'] == selected_product]
    fig_edu = build_education_chart(df_edu, "Education Type")

    df_for_sankey = deals.copy()
    if selected_product != "Total":
        df_for_sankey = df_for_sankey[df_for_sankey['Product'] == selected_product]
    fig_sankey = build_sankey_chart(df_for_sankey)

    return cards, fig_product, fig_edu, fig_sankey


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
