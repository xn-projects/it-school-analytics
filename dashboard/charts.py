import plotly.graph_objects as go
from utils.my_palette import get_my_palette

colors = get_my_palette(as_dict=True)
BASE_COLOR = colors['Cornflower'][3]
SUCCESS_COLOR = colors['Lime Green'][3]
TREND_COLOR = colors['Tomato'][3]


def build_product_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['deals_count'],
        name='All Deals',
        marker_color=BASE_COLOR,
        opacity=0.5
    ))

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['success_count'],
        name='Payment Done',
        marker_color=SUCCESS_COLOR,
        opacity=0.9
    ))

    fig.add_trace(go.Scatter(
        x=df['Deal Created Month'],
        y=df['conversion'],
        mode='lines',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=TREND_COLOR, width=2.5, dash='dot'),
        marker=dict(size=6, color=TREND_COLOR)
    ))

    fig.update_layout(
        template='plotly_white',
        barmode='overlay',
        yaxis2=dict(
            overlaying='y',
            side='right',
            title='Conversion (%)',
            titlefont=dict(color=TREND_COLOR),
            tickfont=dict(color=TREND_COLOR),
        )
    )

    return fig


def build_education_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['deals_count'],
        name='All Deals',
        marker_color=BASE_COLOR,
        opacity=0.5
    ))

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['success_count'],
        name='Payment Done',
        marker_color=SUCCESS_COLOR,
        opacity=0.9
    ))

    fig.add_trace(go.Scatter(
        x=df['Deal Created Month'],
        y=df['conversion'],
        mode='lines',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=TREND_COLOR, width=2.5, dash='dot'),
        marker=dict(size=6, color=TREND_COLOR)
    ))

    fig.update_layout(
        template='plotly_white',
        barmode='overlay',
        xaxis=dict(
            tickangle=-45,
            tickformat='%b %Y'
        ),
        yaxis=dict(title='Number of Deals'),
        yaxis2=dict(
            overlaying='y',
            side='right',
            title='Conversion (%)',
            titlefont=dict(color=TREND_COLOR),
            tickfont=dict(color=TREND_COLOR)
        )
    )

    return fig
