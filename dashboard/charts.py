import plotly.graph_objects as go
from utils.my_palette import get_my_palette

colors = get_my_palette(as_dict=True)
BASE_COLOR = colors["Cornflower"][3]
SUCCESS_COLOR = colors["Lime Green"][3]
TREND_COLOR = colors["Tomato"][3]

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
        'payment done': colors["Lime Green"][3],
        'in progress': colors["Yellowsoft"][2],
        'lost': colors["Tomato"][2],
        'call delayed': colors["Lavender"][1],
        'waiting for payment': colors["Cornflower"][2],
        'other': colors["Neutral"][2]
    }

    sources, targets, values, link_colors = [], [], [], []

    for _, row in agg.iterrows():
        s = row['Source']
        p = row['Product']
        st = row['Stage']
        c = row['count']

        col = stage_colors.get(st, stage_colors['other'])

        # Source → Product (цвет по Stage!)
        sources.append(label_index[s])
        targets.append(label_index[p])
        values.append(c)
        link_colors.append(col)

        # Product → Stage
        sources.append(label_index[p])
        targets.append(label_index[st])
        values.append(c)
        link_colors.append(col)

    # Nodes окрашиваем нейтрально (фокус на потоках)
    node_colors = [colors["Neutral"][2]] * len(labels)

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="white", width=1),
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
        title_text="Deal Flow: Source → Product → Stage",
        title_x=0.5,
        template="plotly_white",
        height=650,
        margin=dict(t=70, l=40, r=40, b=40)
    )

    return fig
