import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.my_palette import get_my_palette
import plotly.express as px

colors = get_my_palette(as_dict=True)

def build_sankey_chart(df):

    df = df.copy()

    for col in ['Source', 'Product', 'Stage']:
        df[col] = df[col].astype(str).str.strip().fillna('Unknown')

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

    labels = (
        list(agg['Source'].unique()) +
        list(agg['Product'].unique()) +
        list(agg['Stage'].unique())
    )
    label_index = {label: i for i, label in enumerate(labels)}

    colors = get_my_palette(as_dict=True)
    stage_colors = {
        'payment done': colors['Lime Green'][3],
        'in progress': colors['Yellowsoft'][2],
        'lost': colors['Tomato'][2],
        'call delayed': colors['Lavender'][1],
        'waiting for payment':  colors['Cornflower'][2],
        'other': colors['Neutral'][2]
    }

    sources, targets, values, colors_links = [], [], [], []

    group_sp = (
        agg.groupby(['Source', 'Product', 'Stage'])['count']
        .sum()
        .reset_index()
    )
    for _, row in group_sp.iterrows():
        sources.append(label_index[row['Source']])
        targets.append(label_index[row['Product']])
        values.append(row['count'])

        stage_name = row['Stage'].strip().lower()
        color = stage_colors.get(stage_name, stage_colors['other'])
        colors_links.append(color)

    for _, row in agg.iterrows():
        sources.append(label_index[row['Product']])
        targets.append(label_index[row['Stage']])
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

    df['Stage'] = (df['Stage']
        .fillna('')
        .astype(str)
        .str.strip()
        .str.lower())

    df['Payment Type'] = (df['Payment Type']
        .fillna('Unknown')
        .astype(str)
        .str.strip()
        .replace({'': 'Unknown'})
    )

    df_success = df[df['Stage'] == 'payment done'].copy()

    if df_success.empty:
        fig = px.pie(title='No Successful Deals')
        fig.update_layout(height=480)
        return fig

    agg = (
        df_success.groupby('Payment Type')
        .size()
        .reset_index(name='success_deals')
    )
    agg = agg[agg['Payment Type'] != 'Unknown']
    
    total_success = agg['success_deals'].sum()

    agg['success_rate'] = (agg['success_deals'] / total_success * 100).round(1)

    palette = get_my_palette(as_dict=True)
    color_list = [
        palette['Lime Green'][2],
        palette['Cornflower'][3],
        palette['Tomato'][2],
        palette['Lavender'][1],
    ]

    fig = px.pie(
        agg,
        names='Payment Type',
        values='success_deals',
        color='Payment Type',
        color_discrete_sequence=color_list,
        hole=0.4,
        title='Successful Deals by Payment Type'
    )

    fig.update_traces(
        textinfo='label+percent',
        pull=[
            0.03 if x == agg['success_deals'].max() else 0
            for x in agg['success_deals']
        ],
        textfont_size=14
    )

    fig.update_layout(
        template='plotly_white',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False,
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
        custom_data=['Successful Deals', 'ROI (%)'],
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
        marker=dict(sizemin=6, line=dict(width=0)),
        textposition='top center',
        textfont=dict(size=11, color='black'),
        opacity=1.0,
        hovertemplate=(
            '<b>%{hovertext}</b><br>'
            'Deals: %{x}<br>'
            'CR: %{y:.1f}%<br>'
            'ROI: %{customdata[1]:.1f}%<br>'
            'Successful Deals: %{customdata[0]}<extra></extra>'
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
        coloraxis=dict(
            colorbar=dict(
                title='ROI (%)',
                thickness=10,
                len=0.6,
                title_side='right'
            )
        ),
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
        annotation_position='bottom right',
        layer='below'
    )
    fig.add_hline(
        y=median_y,
        line_dash='dot',
        line_color=get_my_palette(group='Tomato')[3],
        annotation_text='Median CR',
        annotation_position='top right',
        layer='below'
    )

    return fig


def build_campaign_scatter_new(campaign_summary):

    df_plot = campaign_summary.copy()

    for col in ['Spend', 'Successful Deals', 'Total Paid (Success)']:
        if col in df_plot.columns:
            df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce').fillna(0)

    df_plot.rename(columns={
        'Total Paid (Success)': 'Revenue',
        'Successful Deals': 'Leads'
    }, inplace=True)

    df_plot = df_plot[df_plot['Spend'] >= 0]

    df_plot['size_safe'] = df_plot['Revenue'].clip(lower=1)

    median_x = df_plot['Spend'].median()
    median_y = df_plot['Leads'].median()
    
    palette = get_my_palette(as_dict=True)
    discrete_colors = [
        palette['Tomato'][3],
        palette['Cornflower'][3],
        palette['Lime Green'][3],
        palette['Lavender'][3],
        palette['Yellowsoft'][3],
        palette['Neutral'][3]
    ]
    
    fig = px.scatter(
        df_plot,
        x='Spend',
        y='Leads',
        size='size_safe',
        color='Source',
        text='Source',
        custom_data=['Revenue', 'Leads'],
        color_discrete_sequence=discrete_colors,
        size_max=55,
        height=500,
        title='Source Matrix: Spend vs Successful Leads vs Revenue',
        title_x=0.5
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='white'),
            sizemin=10
        ),
        textposition='top center',
        opacity=1.0,
        hovertemplate=(
            '<b>%{hovertext}</b><br>'
            'Spend: €%{x:,.0f}<br>'
            'Successful Leads: %{y}<br>'
            'Revenue: €%{customdata[0]:,.0f}'
            '<extra></extra>'
        )
    )

    fig.add_vline(
        x=median_x,
        line_dash='dot',
        line_width=2,
        line_color=get_my_palette(group='Cornflower')[3],
        layer='below',
        annotation_text='Median Spend',
        annotation_position='bottom right',
        annotation_font=dict(size=11, color='#333'),
        annotation_bgcolor='rgba(255,255,255,0.85)',
        annotation_bordercolor='rgba(0,0,0,0.15)'
    )

    fig.add_hline(
        y=median_y,
        line_dash='dot',
        line_width=2,
        line_color=get_my_palette(group='Tomato')[3],
        layer='below',
        annotation_text='Median Leads',
        annotation_position='top right',
        annotation_font=dict(size=11, color='#333'),
        annotation_bgcolor='rgba(255,255,255,0.85)',
        annotation_bordercolor='rgba(0,0,0,0.15)'
    )

    fig.update_layout(
        plot_bgcolor='rgb(248,248,245)',
        hoverlabel=dict(bgcolor='white'),
        font=dict(size=12, color='#333'),
        xaxis=dict(
            title='Spend (€)',
            gridcolor='rgba(0,0,0,0.15)',
            zeroline=False
        ),
        yaxis=dict(
            title='Successful Leads',
            gridcolor='rgba(0,0,0,0.15)',
            zeroline=False
        ),
        margin=dict(l=60, r=60, t=70, b=60),
        showlegend=False
    )

    return fig
