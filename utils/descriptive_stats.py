import logging
import pandas as pd
import numpy as np
from IPython.display import display, HTML
from utils import cmap_cornflower, cmap_lime, cmap_tomato, cmap_yellow, cmap_lavender


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

    stats_summary = stats_summary.applymap(lambda x: round(x, 2) if pd.notnull(x) else x)

    styled = (
    stats_summary.style
        .background_gradient(cmap=cmap_cornflower, subset=['Count','Mean', 'Median', 'Mode' ], axis=0)
        .background_gradient(cmap=cmap_yellow, subset=['Range','IQR', 'Std Dev', 'CoeffVar (%)','Skewness'], axis=0)
        .background_gradient(cmap=cmap_lime, subset=['Min', 'Max', '5%', '25%', '50%', '75%', '95%'], axis=0)
        .set_properties(**{'text-align': 'center'})
        .format(precision=2)
    )
    if show:
        display(styled)
        display(HTML('<br>'))

    logging.info(f'{df_name}: Processed {len(num_cols)} numeric columns successfully.')
    logging.info(f'Numeric columns: {", ".join(num_cols)}')

    return stats_summary


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

    return summary
