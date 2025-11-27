import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.my_palette import get_my_palette
import plotly.express as px

colors = get_my_palette(as_dict=True)

def build_sankey_chart(df):
    df = df.copy()

    for col in ['Source', 'Product', 'Stage']:
        df[col] = df[col].fillna('Unknown').astype(str).str.strip()

    df = df[
        (df['Source'] != 'Unknown') &
        (df['Product'] != 'Unknown') &
        (df['Stage'] != 'Unknown')
    ].copy()

    agg = (
        df.groupby(['Source', 'Product', 'Stage'])
        .size()
        .reset_index(name='count')
    )

    agg['source_label'] = 'SRC: ' + agg['Source']
    agg['product_label'] = 'PRD: ' + agg['Product']
    agg['stage_label'] = 'STG: ' + agg['Stage']

    labels = (
        list(agg['source_label'].unique()) +
        list(agg['product_label'].unique()) +
        list(agg['stage_label'].unique())
    )
    label_index = {l: i for i, l in enumerate(labels)}

    stage_colors = {
        'payment done': colors['Lime Green'][3],
        'in progress': colors['Yellowsoft'][2],
        'lost': colors['Tomato'][2],
        'call delayed': colors['Lavender'][1],
        'waiting for payment':  colors['Cornflower'][2],
        'other': colors['Neutral'][2]
    }

    sources, targets, values, colors_links = [], [], [], []

    for _, row in agg.iterrows():
        sources.append(label_index[row['source_label']])
        targets.append(label_index[row['product_label']])
        values.append(row['count'])

        stage_name = row['Stage'].strip().lower()
        color = stage_colors.get(stage_name, stage_colors['other'])
        colors_links.append(color)

    for _, row in agg.iterrows():
        sources.append(label_index[row['product_label']])
        targets.append(label_index[row['stage_label']])
        values.append(row['count'])

        stage_name = row['Stage'].strip().lower()
        color = stage_colors.get(stage_name, stage_colors['other'])
        colors_links.append(color)

    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color='white', width=1),
            label=labels,
            color=[colors['Lavender'][3], colors['Cornflower'][3], colors['Tomato'][3],
                   colors['Lime Green'][3], colors['Yellowsoft'][3]] * (len(labels)//5 + 1)
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors_links,
            hovertemplate=(
                'From: %{source.label}<br>'
                'To: %{target.label}<br>'
                'Deals: %{value}<extra></extra>'
            )
        )
    )])

    fig.update_layout(
        title_text='<b>Deal Flow: Source → Product → Stage</b>',
        title_x=0.5,
        template='plotly_white',
        height=500,
        margin=dict(t=70, l=40, r=40, b=40),
        font=dict(size=12, color='black')
    )

    return fig


def build_payment_pie(df):
    df = df.copy()

    for col in ['Product', 'Payment Type', 'Stage']:
        df[col] = df[col].fillna('Unknown').astype(str).str.strip()

    df = df[
        (df['Product'] != 'Unknown') &
        (df['Payment Type'] != 'Unknown') &
        (df['Stage'] != 'Unknown')
    ].copy()

    df['is_success'] = df['Stage'].str.lower().eq('payment done').astype(int)

    agg = (
        df.groupby('Payment Type')
        .agg(
            total_deals=('Id', 'count'),
            success_count=('is_success', 'sum')
        )
        .reset_index()
    )

    agg['success_rate'] = (
        agg['success_count'] / agg['total_deals']
    ).replace([float('inf')], 0).fillna(0)

    if agg.empty:
        fig = px.pie(title='Success Rate by Payment Type')
        fig.update_layout(height=480)
        return fig

    palette = get_my_palette(as_dict=True)

    color_list = [
        palette['Lime Green'][2],
        palette['Cornflower'][3],
        palette['Tomato'][2],
        palette['Lavender'][1],
        palette['Lime Green'][0],
    ]

    fig = px.pie(
        agg,
        names='Payment Type',
        values='success_rate',
        color='Payment Type',
        color_discrete_sequence=color_list,
        hole=0.4,
        title='Success Rate by Payment Type'
    )

    fig.update_traces(
        textinfo='label+percent',
        pull=[
            0.05 if x == agg['success_rate'].max() else 0
            for x in agg['success_rate']
        ],
        textfont_size=14
    )

    fig.update_layout(
        template='plotly_white',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(size=12, color='#333')
    )

    return fig
    

def build_campaign_scatter(campaign_summary):

    lavender = get_my_palette(group='Lavender')
    tomato = get_my_palette(group='Tomato')
    lime = get_my_palette(group='Lime Green')
    cornflower = get_my_palette(group='Cornflower')

    colors_combined = tomato + cornflower + lime
    color_scale = [
        [i / (len(colors_combined) - 1), color]
        for i, color in enumerate(colors_combined)
    ]

    df_plot = campaign_summary.copy()

    for col in ['Deals Count', 'Successful Deals', 'CR (%)', 'ROI (%)']:
        df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce').fillna(0)

    df_plot = df_plot[df_plot['Deals Count'].fillna(0).astype(float) >= 0]

    if df_plot.empty:
        fig = px.scatter(title='Campaign Effectiveness (no data)')
        fig.update_layout(height=500)
        return fig

    df_plot['size_safe'] = df_plot['Successful Deals'].clip(lower=1)
    df_plot['cr_safe'] = df_plot['CR (%)'].clip(lower=0.1)

    fig = px.scatter(
        df_plot,
        x='Deals Count',
        y='cr_safe',
        size='size_safe',
        color='ROI (%)',
        hover_name='Source',
        text='Source',
        color_continuous_scale=color_scale,
        title='Campaign Effectiveness Landscape: Deals, Conversion, and ROI',
        labels={
            'Deals Count': 'Number of Deals',
            'CR (%)': 'Conversion Rate (CR, %)',
            'ROI (%)': 'Return on Investment (ROI, %)',
            'Successful Deals': 'Successful Deals'
        },
        size_max=55,
        height=500
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color='white'), sizemin=6),
        textposition='top center',
        textfont=dict(size=11, color='black'),
        opacity=0.85,
        hovertemplate=(
            '<b>%{hovertext}</b><br>'
            'Deals: %{x}<br>'
            'CR: %{y:.1f}%<br>'
            'ROI: %{marker.color:.1f}%<br>'
            'Successful Deals: %{marker.size}<extra></extra>'
        )
    )

    fig.update_layout(
        xaxis=dict(
            title='Number of Deals',
            showgrid=True,
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title='Conversion Rate (CR, %)',
            showgrid=True,
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=11)
        ),
        plot_bgcolor='rgb(248,248,245)',
        coloraxis_colorbar=dict(title='ROI (%)'),
        font=dict(size=12, color='#333'),
        hoverlabel=dict(bgcolor='white', font_size=11),
        margin=dict(l=60, r=60, t=70, b=60)
    )

    median_x = df_plot['Deals Count'].median()
    median_y = df_plot['CR (%)'].median()

    fig.add_vline(
        x=median_x,
        line_dash='dot',
        line_color=get_my_palette(group='Cornflower')[3],
        annotation_text='Median Deals',
        annotation_position='bottom left',
        layer='below'
    )
    fig.add_hline(
        y=median_y,
        line_dash='dot',
        line_color=get_my_palette(group='Cornflower')[3],
        annotation_text='Median CR',
        annotation_position='top right',
        layer='below'
    )

    fig.add_annotation(
        x=median_x * 4, y=median_y * 3,
        text='High Volume / High CR',
        showarrow=False,
        font=dict(size=11, weight='bold')
    )
    fig.add_annotation(
        x=median_x * 0.65, y=median_y * 3,
        text='Low Volume / High CR',
        showarrow=False,
        font=dict(size=11, weight='bold')
    )
    fig.add_annotation(
        x=median_x * 4, y=median_y * 0.2,
        text='High Volume / Low CR',
        showarrow=False,
        font=dict(size=11, weight='bold')
    )
    fig.add_annotation(
        x=median_x * 0.65, y=median_y * 0.2,
        text='Low Volume / Low CR',
        showarrow=False,
        font=dict(size=11, weight='bold')
    )

    return fig
