import plotly.graph_objects as go
from utils.my_palette import get_my_palette

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
        mode='lines',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=TREND_COLOR, width=2.5, dash='dot'),
        marker=dict(size=6, color=TREND_COLOR)
    ))

    fig.update_layout(
    barmode='overlay',
    template='plotly_white',
    yaxis=dict(
        title=dict(text="Number of Deals", font=dict(color=BASE_COLOR)),
        tickfont=dict(color=BASE_COLOR),
        showgrid=True
        ),
    yaxis2=dict(
        title=dict(text="Conversion (%)", font=dict(color=TREND_COLOR)),
        overlaying='y',
        side='right',
        tickfont=dict(color=TREND_COLOR),
        showgrid=False
        )
    )

    return fig


def build_education_chart(df_edu, edu_type):
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
        mode='lines',
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
            title=dict(text="Number of Deals", font=dict(color=BASE_COLOR)),
            tickfont=dict(color=BASE_COLOR),
            showgrid=True
        ),
        yaxis2=dict(
            title=dict(text="Conversion (%)", font=dict(color=TREND_COLOR)),
            overlaying='y',
            side='right',
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


def build_sankey_chart(df):
    df = df[['Source', 'Product', 'Stage']].copy()

    df['Source'] = df['Source'].astype(str).str.strip()
    df['Product'] = df['Product'].astype(str).str.strip()
    df['Stage'] = df['Stage'].astype(str).str.lower().str.strip()

    agg = (
        df.groupby(['Source', 'Product', 'Stage'])
        .size()
        .reset_index(name='count')
    )

    labels = list(agg['Source'].unique()) + list(agg['Product'].unique()) + list(agg['Stage'].unique())
    label_index = {label: i for i, label in enumerate(labels)}

    sources, targets, values, link_colors = [], [], [], []

    stage_colors = {
        'payment done': colors["Lime Green"][4],
        'lost': colors["Tomato"][4],
        'waiting for payment': colors["Yellowsoft"][3],
        'in progress': colors["Cornflower"][3],
        'call delayed': colors["Lavender"][3],
        'other': colors["Neutral"][3]
    }

    for _, row in agg.iterrows():
        s = row['Source']
        p = row['Product']
        st = row['Stage']

        c = row['count']
        col = stage_colors.get(st, stage_colors['other'])

        sources += [label_index[s], label_index[p]]
        targets += [label_index[p], label_index[st]]
        values += [c, c]
        link_colors += ["rgba(140,140,140,0.3)", col]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="white", width=1),
            label=labels,
            color=colors["Neutral"][2]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    ))

    fig.update_layout(
        title_text="Deal Flow: Source → Product → Stage",
        title_x=0.5,
        template="plotly_white",
        height=650,
        margin=dict(t=70, l=40, r=40, b=40)
    )

    return fig
