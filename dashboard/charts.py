import plotly.graph_objects as go
from utils.my_palette import get_my_palette

colors = get_my_palette(as_dict=True)
base_color = colors["Cornflower"][3]
success_color = colors["Lime Green"][3]
trend_color = colors["Tomato"][3]

def build_product_chart(df):
    df = df.sort_values('Deal Created Month')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['deals_count'],
        name='All Deals',
        marker_color=base_color,
        opacity=0.5,
        hovertemplate='Month: %{x|%b %Y}<br>Deals: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=df['Deal Created Month'],
        y=df['success_count'],
        name='Payment Done',
        marker_color=success_color,
        opacity=0.9,
        hovertemplate='Month: %{x|%b %Y}<br>Payment Done: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df['Deal Created Month'],
        y=df['conversion'],
        mode='lines+markers',
        name='Conversion %',
        yaxis='y2',
        line=dict(color=trend_color, width=2.5, dash='dot'),
        marker=dict(size=6, color=trend_color),
        hovertemplate='Month: %{x|%b %Y}<br>Conversion: %{y:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        barmode='overlay',
        template='plotly_white',
        height=500,
        margin=dict(l=60, r=80, t=70, b=50),
        xaxis=dict(
            title='Month (Created)',
            tickangle=-45,
            tickformat='%b %Y',
            tickfont=dict(size=9),
            showgrid=True
        ),
        yaxis=dict(
            title='Number of Deals',
            titlefont=dict(color=base_color),
            tickfont=dict(color=base_color),
            showgrid=True
        ),
        yaxis2=dict(
            title='Conversion (%)',
            overlaying='y',
            side='right',
            titlefont=dict(color=trend_color),
            tickfont=dict(color=trend_color),
            showgrid=False
        )
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

    stage_colors = {
        'payment done': colors['Lime Green'][3],
        'in progress': colors['Yellowsoft'][2],
        'lost': colors['Tomato'][2],
        'call delayed': colors['Lavender'][1],
        'waiting for payment': colors['Cornflower'][2],
        'other': colors['Neutral'][2]
    }

    sources, targets, values, link_colors = [], [], [], []

    for _, row in agg.iterrows():
        s = row['Source']
        p = row['Product']
        st = row['Stage']
        c = row['count']

        col = stage_colors.get(st, stage_colors['other'])

        sources.append(label_index[s])
        targets.append(label_index[p])
        values.append(c)
        link_colors.append(col)

        sources.append(label_index[p])
        targets.append(label_index[st])
        values.append(c)
        link_colors.append(col)

    node_colors = [colors['Neutral'][2]] * len(labels)

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color='white', width=1),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    ))

    fig.update_layout(
        title_text='Deal Flow: Source → Product → Stage',
        title_x=0.5,
        template='plotly_white',
        height=650,
        margin=dict(t=70, l=40, r=40, b=40)
    )

    return fig
