import pandas as pd
import numpy as np
from utils import get_my_palette

def prod_analysis(df_deals, df_contacts, df_spend, product=None):
    UA = df_contacts['Id'].nunique()

    df_deals['Contact Name'] = df_deals['Contact Name'].astype(str).str.strip()
    df_contacts['Id'] = df_contacts['Id'].astype(str).str.strip()

    merged = pd.merge(df_deals, df_contacts, left_on='Contact Name', right_on='Id', how='inner')

    if product:
        merged = merged[merged['Product'].astype(str).str.strip() == product]

    merged['AOV_i'] = (
        (merged['Initial Amount Paid'] +
         (merged['Offer Total Amount'] - merged['Initial Amount Paid']) /
         (merged['Course duration'] - 1) *
         (merged['Months of study'] - 1)) /
        merged['Months of study']
    )

    merged['R_i'] = merged['AOV_i'] * merged['Months of study']

    B = merged[merged['Stage'].astype(str).str.lower().str.strip() == 'payment done']
    C1 = round(len(B) / UA * 100, 2)

    if product is None or product == 'Total':
        AC = float(df_spend['Spend'].sum())
        CPA = round(AC / UA, 2)
    else:
        CPA = round(float(df_spend['Spend'].sum()) / df_contacts['Id'].nunique(), 2)
        AC = round(UA * CPA, 2)

    REV = round(float(merged['R_i'].sum()), 2)
    T = round(float(merged['Months of study'].sum()), 2)
    AOV = round(REV / T if T > 0 else 0, 2)
    APC = round(T / len(B) if len(B) > 0 else 0, 2)
    CLTV = round(AOV * APC, 2)
    LTV = round(CLTV * (C1 / 100), 2)
    CM = round(UA * (LTV - CPA), 2)

    base = pd.DataFrame([{
        'Product': product if product else 'Total',
        'UA': UA,
        'B': len(B),
        'C1': C1,
        'AOV': AOV,
        'CPA': CPA,
        'AC': round(AC, 2),
        'REV': REV,
        'T': T,
        'APC': APC,
        'CLTV': CLTV,
        'LTV': LTV,
        'CM': CM,
    }])

    scenarios = pd.concat([base] * 6, ignore_index=True)
    scenarios.loc[1, 'Product'] = 'UA ↑'
    scenarios.loc[1, 'UA'] *= 1.05

    scenarios.loc[2, 'Product'] = 'C1 ↑'
    scenarios.loc[2, 'C1'] *= 1.05

    scenarios.loc[3, 'Product'] = 'AOV ↑'
    scenarios.loc[3, 'AOV'] *= 1.05

    scenarios.loc[4, 'Product'] = 'CPA ↓'
    scenarios.loc[4, 'CPA'] *= 0.95

    scenarios.loc[5, 'Product'] = 'APC ↑'
    scenarios.loc[5, 'APC'] *= 1.05

    scenarios['B'] = round(scenarios['UA'] * (scenarios['C1'] / 100), 2)
    scenarios['T'] = round(scenarios['B'] * scenarios['APC'], 2)
    scenarios['REV'] = round(scenarios['AOV'] * scenarios['T'], 2)
    scenarios['CLTV'] = round(scenarios['AOV'] * scenarios['APC'], 2)
    scenarios['LTV'] = round(scenarios['CLTV'] * (scenarios['C1'] / 100), 2)
    scenarios['AC'] = round(scenarios['UA'] * scenarios['CPA'], 2)
    scenarios['CM'] = round(scenarios['UA'] * (scenarios['LTV'] - scenarios['CPA']), 2)

    highlight_color = get_my_palette(group='Yellowsoft')[2]
    max_color = get_my_palette(group='Lavender')[1]

    fmt = {
        'UA': '{:,.0f}'.format, 'B': '{:,.0f}'.format, 'C1': '{:,.2f}'.format,
        'AOV': '{:,.2f}'.format, 'CPA': '{:,.2f}'.format, 'AC': '{:,.2f}'.format,
        'REV': '{:,.2f}'.format, 'T': '{:,.0f}'.format, 'APC': '{:,.2f}'.format,
        'CLTV': '{:,.2f}'.format, 'LTV': '{:,.2f}'.format, 'CM': '{:,.2f}'.format,
    }

    def highlight_changed(row):
        style = [''] * len(row)
        col_idx = row.index.get_loc
        if row.name == 1:
            style[col_idx('UA')] = f'background-color: {highlight_color}; font-weight: bold;'
        elif row.name == 2:
            style[col_idx('C1')] = f'background-color: {highlight_color}; font-weight: bold;'
        elif row.name == 3:
            style[col_idx('AOV')] = f'background-color: {highlight_color}; font-weight: bold;'
        elif row.name == 4:
            style[col_idx('CPA')] = f'background-color: {highlight_color}; font-weight: bold;'
        elif row.name == 5:
            style[col_idx('APC')] = f'background-color: {highlight_color}; font-weight: bold;'
        return style

    styled = (
        scenarios.style
        .format(fmt, thousands=' ')
        .apply(highlight_changed, axis=1)
        .apply(
            lambda s: [
                f'background-color: {max_color}; font-weight: bold;' if v == s.max() else ''
                for v in s
            ],
            subset=['CM']
        )
        .set_caption(f'Product analysis — {product if product else "Total"}')
        .set_table_styles([
            {'selector': 'caption', 'props': [
                ('font-size', '16px'),
                ('font-weight', 'bold'),
                ('text-align', 'center')
            ]}
        ])
    )

    return styled
