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


def prepare_data(deals, calls):
    deals['Stage'] = deals['Stage'].astype(str).str.lower().str.strip()
    deals['is_success'] = (deals['Stage'] == 'payment done').astype(int)

    deals['Created Time'] = pd.to_datetime(deals['Created Time'], errors='coerce')
    deals['Deal Created Month'] = deals['Created Time'].dt.to_period('M').dt.to_timestamp()

    agg_product = deals.groupby(['Deal Created Month', 'Product']).agg(
        deals_count=('Id', 'count'),
        success_count=('is_success', 'sum')
    ).reset_index()
    agg_product['conversion'] = (agg_product['success_count'] / agg_product['deals_count'] * 100).fillna(0)

    calls_unique = calls.drop_duplicates(subset=['Id'])
    calls_count = calls_unique.groupby('Id').size().reset_index(name='calls_count')
    deals = deals.merge(calls_count, on='Id', how='left')
    deals['calls_count'] = deals['calls_count'].fillna(0)

    return deals, agg_product, agg_edu


def compute_kpi(deals, selected_product):
    df = deals.copy()

    if selected_product != 'Total':
        df = df[df['Product'] == selected_product]

    total_calls = df['calls_count'].sum()
    total_deals = len(df)
    total_success = df['is_success'].sum()

    return total_calls, total_deals, total_success
