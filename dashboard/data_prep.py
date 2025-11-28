import os
import pandas as pd
import numpy as np

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

    df['Created Time'] = pd.to_datetime(df['Created Time'], errors='coerce')
    df['Deal Created Month'] = df['Created Time'].dt.to_period('M').dt.to_timestamp()
    df['Offer Total Amount'] = pd.to_numeric(df['Offer Total Amount'], errors='coerce').fillna(0)

    return df


def compute_kpi(df):
   
    total_deals = len(df)
    success_deals = (df['Stage'].str.lower().str.strip() == 'payment done').sum()
    conversion_rate = (success_deals / total_deals) * 100 if total_deals > 0 else 0
    lost_deals = (df['Stage'].str.lower().str.strip() == 'lost').sum()
    closed_deals = df['Closing Date'].notna().sum()
    revenue = df.loc[
        df['Stage'].str.lower().str.strip() == 'payment done',
        'Offer Total Amount'
    ].sum()

    return total_deals, success_deals, conversion_rate, lost_deals, closed_deals, revenue


def prepare_campaign_summary(deals, spend):
    
    df_deals = deals.copy()
    df_spend = spend.copy()

    df_deals['Is Successful'] = df_deals['Stage'].str.lower().eq('payment done')

    deals_total = (
        df_deals.groupby('Source')
        .agg({
            'Contact Name': 'count',
            'Campaign': 'nunique',
            'Offer Total Amount': 'sum',
            'Initial Amount Paid': 'sum'
        })
        .rename(columns={
            'Contact Name': 'Deals Count',
            'Campaign': 'Campaigns Count',
            'Offer Total Amount': 'Total Offer Amount',
            'Initial Amount Paid': 'Total Paid'
        })
    )

    deals_success = (
        df_deals[df_deals['Is Successful']]
        .groupby('Source')
        .agg({
            'Contact Name': 'count',
            'Offer Total Amount': 'sum',
            'Initial Amount Paid': 'sum'
        })
        .rename(columns={
            'Contact Name': 'Successful Deals',
            'Offer Total Amount': 'Total Offer Amount (Success)',
            'Initial Amount Paid': 'Total Paid (Success)'
        })
    )

    spend_grouped = (
        df_spend.groupby('Source')
        .agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Spend': 'sum'
        })
    )

    campaign_summary = (
        deals_total
        .merge(deals_success, on='Source', how='outer')
        .merge(spend_grouped, on='Source', how='outer')
        .fillna(0)
        .reset_index()
    )

    campaign_summary['CR (%)'] = (
        campaign_summary['Successful Deals'] / campaign_summary['Deals Count'] * 100
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    campaign_summary['CTR (%)'] = (
        campaign_summary['Clicks'] / campaign_summary['Impressions'] * 100
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    campaign_summary['CPC (€)'] = (
        campaign_summary['Spend'] / campaign_summary['Clicks']
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    campaign_summary['CPL (€)'] = (
        campaign_summary['Spend'] / campaign_summary['Deals Count']
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    campaign_summary['CPA (€)'] = (
        campaign_summary['Spend'] / campaign_summary['Successful Deals']
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    campaign_summary['ROI (%)'] = (
        (campaign_summary['Total Paid (Success)'] - campaign_summary['Spend']) /
        campaign_summary['Spend'] * 100
    ).replace([np.inf, -np.inf], np.nan).fillna(0).round(2)

    return campaign_summary
