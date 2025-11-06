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


def prepare_data(df_deals):
    df = df_deals.copy()

    df['Stage'] = df['Stage'].astype(str).str.strip().str.lower()
    df['Payment Type'] = df['Payment Type'].astype(str).str.strip()
    df['Product'] = df['Product'].astype(str).str.strip()
    df['Education Type'] = df['Education Type'].astype(str).str.strip()

    df['is_success'] = (df['Stage'] == 'payment done').astype(int)

    df['Created Time'] = pd.to_datetime(df['Created Time'], errors='coerce')
    df['Deal Created Month'] = df['Created Time'].dt.to_period('M').dt.to_timestamp()

    df = df[
        (df['Product'] != 'Unknown') &
        (df['Education Type'] != 'Unknown') &
        (df['Payment Type'] != 'Unknown')
    ].copy()

    return df


def compute_kpi(df):
    total_deals = len(df)
    success_deals = (df['Stage'].str.lower().str.strip() == 'payment done').sum()
    lost_deals = (df['Stage'].str.lower().str.strip() == 'lost').sum()
    closed_deals = df['Closing Date'].notna().sum()

    return total_deals, success_deals, lost_deals, closed_deals
