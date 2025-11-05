import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from .data_prep import load_data, prepare_data, compute_kpi
from .charts import build_product_chart, build_education_chart
from utils.my_palette import get_my_palette


deals, calls, contacts, spend = load_data()
deals, agg_product, agg_edu = prepare_data(deals, calls)

products = ['Total'] + sorted(agg_product['Product'].unique())

colors = get_my_palette(as_dict=True)
CALLS_COLOR = colors['Cornflower'][4]
DEALS_COLOR = colors['Lime Green'][4]
SUCCESS_COLOR = colors['Tomato'][4]

def make_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, style={'textAlign': 'center'}),
            html.H3(f'{value:,}', style={'textAlign': 'center', 'color': color})
        ]),
        style={'borderRadius': '12px'}
    )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server


app.layout = dbc.Container([
    html.H2("Sales Dashboard", style={'textAlign': 'center', 'marginTop': '20px'}),

    dcc.Dropdown(
        id='product_filter',
        options=[{'label': p, 'value': p} for p in products],
        value='Total',
        clearable=False,
        style={'width': '300px', 'margin': '0 auto 30px auto'}
    ),

    dbc.Row([
        dbc.Col(html.Div(id='kpi_calls'), width=4),
        dbc.Col(html.Div(id='kpi_deals'), width=4),
        dbc.Col(html.Div(id='kpi_success'), width=4),
    ], style={'marginBottom': '30px'}),

    dcc.Graph(id='product_graph', style={'marginBottom': '40px'}),
    dcc.Graph(id='education_graph')
], fluid=True)

@app.callback(
    Output('kpi_calls', 'children'),
    Output('kpi_deals', 'children'),
    Output('kpi_success', 'children'),
    Output('product_graph', 'figure'),
    Output('education_graph', 'figure'),
    Input('product_filter', 'value')
)
def update_dashboard(selected_product):

    total_calls, total_deals, total_success = compute_kpi(deals, selected_product)
    calls_card = make_card('Calls', int(total_calls), CALLS_COLOR)
    deals_card = make_card('Deals', int(total_deals), DEALS_COLOR)
    success_card = make_card('Success Deals', int(total_success), SUCCESS_COLOR)

    if selected_product == 'Total':
        dfp = agg_product.groupby('Deal Created Month').sum(numeric_only=True).reset_index()
        dfp['conversion'] = (dfp['success_count'] / dfp['deals_count'] * 100).fillna(0)
    else:
        dfp = agg_product[agg_product['Product'] == selected_product]

    fig_product = build_product_chart(dfp)

    df_edu = deals.copy()
    if selected_product != 'Total':
        df_edu = df_edu[df_edu['Product'] == selected_product]

    agg_edu_filtered = df_edu.groupby(['Deal Created Month', 'Education Type']).agg(
        deals_count=('Id', 'count'),
        success_count=('is_success', 'sum')
    ).reset_index()

    agg_edu_filtered['conversion'] = (
            agg_edu_filtered['success_count'] / agg_edu_filtered['deals_count'] * 100
        ).fillna(0)

    fig_edu = build_education_chart(agg_edu_filtered)

    return calls_card, deals_card, success_card, fig_product, fig_edu

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
