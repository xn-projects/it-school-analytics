import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'clean', 'data_all.xlsx')

def load_data(path=DATA_PATH):
    deals = pd.read_excel(path, sheet_name='deals')
    calls = pd.read_excel(path, sheet_name='calls')
    contacts = pd.read_excel(path, sheet_name='contacts')
    spend = pd.read_excel(path, sheet_name='spend')

    return deals, calls, contacts, spend


def prepare_data(deals):
    deals['Stage'] = deals['Stage'].astype(str).str.strip().str.lower()
    deals['Product'] = deals['Product'].astype(str).str.strip().fillna('Unknown')
    deals['Education Type'] = deals['Education Type'].astype(str).str.strip().fillna('Unknown')
    deals['Payment Type'] = deals['Payment Type'].astype(str).str.strip().fillna('Unknown')

    deals = deals[
        (deals['Product'] != 'Unknown') &
        (deals['Education Type'] != 'Unknown') &
        (deals['Payment Type'] != 'Unknown')
    ].copy()

    deals['is_success'] = deals['Stage'].eq('payment done').astype(int)

    deals['Deal Created Month'] = pd.to_datetime(deals['Deal Created Month']).dt.to_period('M').dt.to_timestamp()

    agg_product = (
        deals.groupby(['Deal Created Month', 'Product'])
        .agg(deals_count=('Id', 'count'),
             success_count=('is_success', 'sum'))
        .reset_index()
    )
    agg_product['conversion'] = (agg_product['success_count'] / agg_product['deals_count'] * 100).fillna(0)

    agg_edu = (
        deals.groupby(['Deal Created Month', 'Education Type', 'Product'])
        .agg(deals_count=('Id', 'count'),
             success_count=('is_success', 'sum'))
        .reset_index()
    )
    agg_edu['conversion'] = (agg_edu['success_count'] / agg_edu['deals_count'] * 100).fillna(0)

    return deals, agg_product, agg_edu


def compute_kpi(deals, selected_product=None):
    df = deals.copy()

    if selected_product and selected_product != 'Total':
        df = df[df['Product'] == selected_product]

    total_deals = len(df)
    success_deals = df['is_success'].sum()
    open_deals = df['Created Time'].notna().sum()
    closed_deals = df['Closing Date'].notna().sum()

    return total_deals, success_deals, open_deals, closed_deals
