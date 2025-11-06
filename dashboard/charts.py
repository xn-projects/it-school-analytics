import plotly.graph_objects as go
from utils.my_palette import get_my_palette
import plotly.express as px

colors = get_my_palette(as_dict=True)

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

    sources_unique = list(agg['Source'].unique())
    products_unique = list(agg['Product'].unique())
    stages_unique = list(agg['Stage'].unique())

    labels = sources_unique + products_unique + stages_unique
    label_index = {label: i for i, label in enumerate(labels)}

    node_colors = []
    node_colors += [colors["Cornflower"][i % 5] for i in range(len(sources_unique))]
    node_colors += [colors["Lime Green"][i % 5] for i in range(len(products_unique))]
    node_colors += [colors["Tomato"][i % 5] for i in range(len(stages_unique))]

    labels = [f'<b>{label}</b>' for label in labels]

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

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=22,
            line=dict(color='white', width=1),
            label=labels,
            color=node_colors,
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    ))

    fig.update_layout(
        title_text='<b>Deal Flow: Source → Product → Stage</b>',
        title_x=0.5,
        template='plotly_white',
        height=650,
        margin=dict(t=70, l=40, r=40, b=40),
        font=dict(size=13, color="black")
    )

    return fig


def build_success_sunburst(df):
    df = df.copy()

    df['Stage'] = df['Stage'].astype(str).str.lower().str.strip()
    df = df[df['Stage'] == 'payment done']
    if df.empty:
        return go.Figure()

    df['German Level'] = df['German Level'].fillna('Unknown').astype(str).str.strip()
    df['Product'] = df['Product'].fillna('Unknown').astype(str).str.strip()

    color_groups = get_my_palette(as_dict=True)

    level_colormap = {
        'A0': color_groups['Neutral'][3],
        'A1': color_groups['Lavender'][4],
        'A2': color_groups['Tomato'][4],
        'B1': color_groups['Lime Green'][4],
        'B2': color_groups['Cornflower'][3],
        'C1': color_groups['Yellowsoft'][4],
        'C2': color_groups['Lime Green'][2],
        'Unknown': color_groups['Neutral'][1],
    }

    product_palette = (
        color_groups['Cornflower'] +
        color_groups['Lime Green'] +
        color_groups['Tomato'] +
        color_groups['Yellowsoft'] +
        color_groups['Lavender']
    )

    products = df['Product'].unique().tolist()
    product_colors = {p: product_palette[i % len(product_palette)] for i, p in enumerate(products)}

    agg = (
        df.groupby(['Product', 'German Level'])
        .size()
        .reset_index(name='count')
    )

    labels = []
    parents = []
    values = []
    colors = []

    for product in products:
        product_total = agg.loc[agg['Product'] == product, 'count'].sum()

        labels.append(product)
        parents.append("")
        values.append(product_total)
        colors.append(product_colors[product])

        sub = agg[agg['Product'] == product]
        for _, row in sub.iterrows():
            labels.append(row['German Level'])
            parents.append(product)
            values.append(row['count'])
            colors.append(level_colormap.get(row['German Level'], level_colormap['Unknown']))

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues='total',
        marker=dict(
            colors=colors,
            line=dict(width=1, color='white')
        ),
        insidetextorientation='auto',
        textfont=dict(size=14, weight='bold')
    ))

    fig.update_layout(
        title='<b>Successful Deals Breakdown: Product → German Level</b>',
        title_x=0.5,
        height=650,
        margin=dict(t=60, l=40, r=40, b=40)
    )

    return fig
