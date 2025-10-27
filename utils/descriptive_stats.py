import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, HTML
from utils import get_my_palette, cmap_cornflower, cmap_lime, cmap_tomato, cmap_yellow, cmap_lavender, cmap_neutral, save_plot


def describe_num(df, df_name='DataFrame', quantiles=True, show=True):
    """
    Universal function for descriptive statistics of numeric columns in a DataFrame.
    """
    num_cols = df.select_dtypes(include=['int', 'float']).columns
    if len(num_cols) == 0:
        logging.warning(f'{df_name}: No numeric columns found.')
        print('No numeric columns found in this DataFrame.')
        return None

    stats_summary = pd.DataFrame({
        'Count': df[num_cols].count(),
        'Mean': df[num_cols].mean(),
        'Median': df[num_cols].median(),
        'Mode': [
            df[c].mode().iloc[0] if not df[c].mode().empty else np.nan
            for c in num_cols
        ],
        'Min': df[num_cols].min(),
        '5%': df[num_cols].quantile(0.05),
        '25%': df[num_cols].quantile(0.25),
        '50%': df[num_cols].quantile(0.5),
        '75%': df[num_cols].quantile(0.75),
        '95%': df[num_cols].quantile(0.95),
        'Max': df[num_cols].max(),
        'Range': df[num_cols].max() - df[num_cols].min(),
        'IQR': df[num_cols].quantile(0.75) - df[num_cols].quantile(0.25),
        'Std Dev': df[num_cols].std(),
        'CoeffVar (%)': (df[num_cols].std() / df[num_cols].mean()) * 100,
        'Skewness': df[num_cols].skew(),
    })

    styled = (
    stats_summary.style
        .background_gradient(cmap=cmap_tomato, subset=['Count'], axis=1)
        .background_gradient(cmap=cmap_cornflower, subset=['Mean', 'Median', 'Mode'], axis=1)
        .background_gradient(cmap=cmap_yellow, subset=['Range', 'IQR', 'Std Dev'], axis=1)
        .background_gradient(cmap=cmap_yellow, subset=[ 'CoeffVar (%)', 'Skewness'], axis=0)
        .background_gradient(cmap=cmap_lime, subset=['Min', 'Max', '5%', '25%', '50%', '75%', '95%'], axis=1)
        .set_properties(**{'text-align': 'center'})
        .format(precision=2)
    )
    if show:
        display(styled)
        display(HTML('<br>'))

    logging.info(f'{df_name}: Processed {len(num_cols)} numeric columns successfully.')
    logging.info(f'Numeric columns: {", ".join(num_cols)}')

    return styled


def describe_cat(df, df_name='DataFrame', show=True):
    """
    Descriptive statistics for categorical (object/string) columns.
    """
    cat_cols = df.select_dtypes(include='object').columns
    if len(cat_cols) == 0:
        logging.warning(f'{df_name}: No categorical columns found.')
        print('No categorical columns found in this DataFrame.')
        return

    data = []
    for col in cat_cols:
        series = df[col].dropna()
        count = len(series)
        unique = series.nunique()
        mode = series.mode().iloc[0] if not series.mode().empty else np.nan
        freq = series.value_counts().iloc[0] if not series.value_counts().empty else np.nan
        percent = round((freq / count) * 100, 2) if count > 0 else np.nan
        data.append([count, unique, mode, freq, percent])

    summary = pd.DataFrame(
        data,
        columns=['Count', 'Unique', 'Mode', 'Frequency', 'Percent'],
        index=cat_cols
    )

    styled = (
        summary.style
        .background_gradient(cmap=cmap_lavender, subset=['Count', 'Unique'], axis=0)
        .background_gradient(cmap=cmap_tomato, subset=['Frequency'], axis=0)
        .background_gradient(cmap=cmap_yellow, subset=['Percent'], axis=0)
        .set_properties(**{'text-align': 'center'})
        .format({'Percent': '{:.2f}%'})
    )
    if show:
        display(styled)
        display(HTML('<br>'))

    logging.info(f'{df_name}: Processed {len(cat_cols)} categorical columns successfully.')
    logging.info(f'Categorical columns: {", ".join(cat_cols)}')

    return styled


def compare_distributions(df, col_original, col_transformed, df_name='DataFrame'):
    """
    Compare descriptive statistics before and after transformation.
    """
    if col_original not in df.columns or col_transformed not in df.columns:
        logging.warning(f'{df_name}: Columns not found ({col_original}, {col_transformed})')
        return None

    orig = df[col_original].dropna()
    trans = df[col_transformed].dropna()

    compare = pd.DataFrame({
        'Mean': [orig.mean(), trans.mean()],
        'Median': [orig.median(), trans.median()],
        'Std Dev': [orig.std(), trans.std()],
        'IQR': [
            orig.quantile(0.75) - orig.quantile(0.25),
            trans.quantile(0.75) - trans.quantile(0.25)
        ],
        'Range': [orig.max() - orig.min(), trans.max() - trans.min()],
        'CoeffVar (%)': [(orig.std() / orig.mean()) * 100,
                         (trans.std() / trans.mean()) * 100],
        'Skewness': [orig.skew(), trans.skew()],
        'Kurtosis': [orig.kurt(), trans.kurt()],
    }, index=['Original', 'Log'])

    logging.info(f'{df_name}: Compared distributions ({col_original} → {col_transformed}).')
    return compare.round(2)


def plot_change(compare, orig_label='Original', trans_label='Log', name='relative_change', subfolder=None):
    """
    Plot relative change (%) between transformed and original statistics after log transformation.
    """
    if orig_label not in compare.index or trans_label not in compare.index:
        logging.warning(f'Index labels not found ({orig_label}, {trans_label}) in compare DataFrame.')
        return None

    delta = (compare.loc[trans_label] - compare.loc[orig_label]) / compare.loc[orig_label] * 100

    cornflower = get_my_palette(group='Cornflower')
    lime = get_my_palette(group='Lime Green')
    tomato = get_my_palette(group='Tomato')
    yellow = get_my_palette(group='Yellowsoft')
    lavender = get_my_palette(group='Lavender')
    neutral = get_my_palette(group='Neutral')

    color_map = {
        'Mean': cornflower[4],
        'Median': lavender[4],
        'Std Dev': lime[2],
        'IQR': yellow[3],
        'Range': tomato[3],
        'CoeffVar (%)': cornflower[2],
        'Skewness': lavender[2],
        'Kurtosis': neutral[3]
    }

    colors = [color_map.get(col, lime[3]) for col in delta.index]

    plt.figure(figsize=(8, 4))
    ax = sns.barplot(x=delta.index, y=delta.values, palette=colors)

    for i, v in enumerate(delta.values):
        ax.text(
            i, v / 3,
            f'{v:.1f}%',
            ha='center',
            va='center',
            fontsize=9,
        )

    plt.title('Change After Log Transformation (%)', fontsize=12, pad=12)
    plt.xticks(rotation=30, ha='right', fontsize=9)
    plt.ylabel('Change (%)', fontsize=9)
    plt.axhline(0, linestyle='--', linewidth=1)
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()

    save_plot(name, subfolder=subfolder)
    plt.show()

    logging.info(f'Plot {name}.png saved successfully.')
    return delta.round(2)
