import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utils.my_palette import get_my_palette
from .charts import build_sankey_chart, build_payment_pie, build_campaign_scatter
from .data_prep import load_data, compute_kpi, prepare_campaign_summary

deals, calls, contacts, spend = load_data()

colors = get_my_palette(as_dict=True)

product_options = ['All Courses'] + sorted(
    deals.loc[
        deals['Product'].notna() &
        (deals['Product'] != 'Unknown') &
        (deals['Product'].str.strip() != ''),
        'Product'
    ].unique()
)

edu_options = ['All Schedules'] + sorted(
    deals.loc[
        deals['Education Type'].notna() &
        (deals['Education Type'] != 'Unknown') &
        (deals['Education Type'].str.strip() != ''),
        'Education Type'
    ].unique()
)


def make_card(title, value, color):
    if isinstance(value, (int, float)):
        display_value = f'{value:,}'
    else:
        display_value = str(value)

    return dbc.Card(
        dbc.CardBody([
            html.H6(title, style={'textAlign': 'center'}),
            html.H3(display_value, style={'textAlign': 'center', 'color': color})
        ]),
        style={'borderRadius': '12px'}
    )


def make_kpi_cards(total, success, conversion_rate, lost, closed, revenue):
    return dbc.Row([
        dbc.Col(make_card('Total Deals', total, colors['Cornflower'][4]), md=2),
        dbc.Col(make_card('Successful Deals', success, colors['Lime Green'][4]), md=2),
        dbc.Col(make_card('Conversion Rate', f'{conversion_rate:.1f}%', colors['Neutral'][4]), md=2),
        dbc.Col(make_card('Lost Deals', lost, colors['Tomato'][4]), md=2),
        dbc.Col(make_card('Closed Deals', closed, colors['Yellowsoft'][4]), md=2),
        dbc.Col(make_card('Revenue', f'€{revenue:,.0f}', colors['Lavender'][4]), md=2),
    ], className='mb-4')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

min_date = pd.concat([
    deals['Created Time'],
    pd.to_datetime(deals['Closing Date'], errors='coerce')
]).min()

max_date = pd.concat([
    deals['Created Time'],
    pd.to_datetime(deals['Closing Date'], errors='coerce')
]).max()

app.layout = dbc.Container([
    html.H2('IT School Analytics', style={'textAlign': 'center', 'marginTop': '20px'}),

    html.Div(
        html.P(
            [
                'This dashboard analyzes sales performance, customer conversion, and revenue dynamics of the IT School.',
                html.Br(),
                'Interactive visualizations highlight lead flow, deal success rates, and segmentation by product and student level.',
                html.Br(),
                'Use the filters below to explore trends across time, education types, and products.'
            ],
            style={
                'textAlign': 'center',
                'maxWidth': '900px',
                'margin': '0 auto',
                'fontSize': '16px',
                'color': '#333'
            }
        ),
        style={'marginBottom': '25px'}
    ),

    dbc.Tabs([

        dbc.Tab(
            label='Sales Analytics',
            children=[
                
                html.H4(
                    'Sales Performance Overview',
                    style={
                        'textAlign': 'center',
                        'marginBottom': '25px',
                        'fontWeight': '600'
                    }
                ),

                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id='product_filter',
                        options=[{'label': p, 'value': p} for p in product_options],
                        value='All Courses',
                        clearable=False,
                    ), md=4),

                    dbc.Col(dcc.Dropdown(
                        id='edu_filter',
                        options=[{'label': e, 'value': e} for e in edu_options],
                        value='All Schedules',
                        clearable=False,
                    ), md=4),

                    dbc.Col(dcc.DatePickerRange(
                        id='date_filter',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=min_date,
                        end_date=max_date,
                        display_format='MMM YYYY',
                        className='date-picker',
                        style={'width': '100%'}
                    ), md=4),
                ], style={'marginBottom': '30px'}),

                html.Div(id='kpi_cards'),

                dbc.Row([
                    dbc.Col(dcc.Graph(id='sankey_graph'), md=8),
                    dbc.Col(dcc.Graph(id='pie_graph'), md=4),
                ], style={'marginBottom': '40px'}),
            ]
        ),

        dbc.Tab(
            label='Marketing Analytics',
            children=[

                html.H4(
                    'Campaign Effectiveness',
                    style={
                        'textAlign': 'center',
                        'marginBottom': '25px',
                        'fontWeight': '600'
                    }
                ),

                dbc.Row([
                    dbc.Col(dcc.Graph(id='campaign_scatter'), md=6)
                ])
            ]
        )
    ])
], fluid=True)

@app.callback(
    [
        Output('kpi_cards', 'children'),
        Output('sankey_graph', 'figure'),
        Output('pie_graph', 'figure'),
        Output('campaign_scatter', 'figure'),
    ],
    [
        Input('product_filter', 'value'),
        Input('edu_filter', 'value'),
        Input('date_filter', 'start_date'),
        Input('date_filter', 'end_date')
    ]
)


def update_dashboard(selected_product, selected_edu, start_date, end_date):
    df = deals.copy()

    if selected_edu != 'All Schedules':
        df = df[df['Education Type'] == selected_edu]

    if selected_product != 'All Courses':
        df = df[df['Product'] == selected_product]

    if start_date and end_date:
        df = df[
            (df['Created Time'] >= pd.to_datetime(start_date)) &
            (df['Created Time'] <= pd.to_datetime(end_date))
        ]

    total, success, conversion_rate, lost, closed, revenue = compute_kpi(df)

    cards = make_kpi_cards(
        total,
        success,
        conversion_rate,
        lost,
        closed,
        revenue
    )

    sankey_fig = build_sankey_chart(df)
    pie_chart = build_payment_pie(deals)
    campaign_summary = prepare_campaign_summary(deals, spend)
    campaign_fig = build_campaign_scatter(campaign_summary)

    return cards, sankey_fig, pie_chart, campaign_fig


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port)
