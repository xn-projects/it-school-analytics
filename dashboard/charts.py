import plotly.graph_objects as go
from ..utils.my_palette import get_my_palette

colors = get_my_palette(as_dict=True)
BASE_COLOR = colors["Cornflower"][3]
SUCCESS_COLOR = colors["Lime Green"][3]
TREND_COLOR = colors["Tomato"][3]

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
        mode='lines+markers',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=TREND_COLOR, width=2.5, dash='dot'),
        marker=dict(size=6, color=TREND_COLOR)
    ))

    fig.update_layout(
        barmode='overlay',
        template='plotly_white',
        yaxis2=dict(overlaying='y', side='right')
    )

    return fig


def build_education_chart(df_edu, edu_type):
    """
    df_edu — срез данных по конкретному Education Type
    edu_type — строка (название типа обучения)
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_edu['Deal Created Month'],
        y=df_edu['deals_count'],
        name='All Deals',
        marker_color=BASE_COLOR,
        opacity=0.5,
        hovertemplate="Month: %{x|%b %Y}<br>Deals: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        x=df_edu['Deal Created Month'],
        y=df_edu['success_count'],
        name='Payment Done',
        marker_color=SUCCESS_COLOR,
        opacity=0.9,
        hovertemplate="Month: %{x|%b %Y}<br>Payment Done: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df_edu['Deal Created Month'],
        y=df_edu['conversion'],
        mode='lines+markers',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=TREND_COLOR, width=2.5, dash='dot'),
        marker=dict(size=6, color=TREND_COLOR),
        hovertemplate="Month: %{x|%b %Y}<br>Conversion: %{y:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        title=f"{edu_type}: Deals, Payment Done and Conversion",
        title_x=0.5,
        barmode='overlay',
        template='plotly_white',

        xaxis=dict(
            title="Month (Created)",
            tickangle=-45,
            tickformat="%b %Y",
            tickfont=dict(size=9),
            showgrid=True
        ),
        yaxis=dict(
            title="Number of Deals",
            titlefont=dict(color=BASE_COLOR),
            tickfont=dict(color=BASE_COLOR),
            showgrid=True
        ),
        yaxis2=dict(
            title="Conversion (%)",
            overlaying='y',
            side='right',
            titlefont=dict(color=TREND_COLOR),
            tickfont=dict(color=TREND_COLOR),
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=9)
        ),
        margin=dict(l=60, r=80, t=70, b=50),
        height=500,
        width=950
    )

    return fig
