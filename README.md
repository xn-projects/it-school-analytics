# IT School Analytics

This project provides a complete data analytics pipeline and interactive dashboard for analyzing CRM data from an IT school.  
The goal is to explore business metrics such as leads, call performance, deals conversion, product metrics, and marketing spending efficiency.

---

## Interactive CRM Analytics Dashboard

[Open the Dashboard](https://it-school-analytics.onrender.com) 

---
## Analysis Documentation Map

### Dataset Understanding

High-level overview of the CRM structure, entities, and business context.

[CRM Dataset Documentation](docs/crm_dataset_documentation.md)

### Data Cleaning & Preparation

Step-by-step transformation of raw CRM data into clean, analysis-ready datasets.

- [Data Preparation](notebooks/01_1_data_preparation.md)
- [Calls Cleaning](notebooks/01_2_calls_cleaning.md)
- [Contacts Cleaning](notebooks/01_3_contacts_cleaning.md)
- [Spend Cleaning](notebooks/01_4_spend_cleaning.md)
- [Deals Cleaning](notebooks/01_5_deals_cleaning.md)

### Descriptive Analytics

Exploration of key CRM metrics and baseline business performance.
- [Calls Description](notebooks/02_1_calls_descriptive_stats.md)
- [Contacts Description](notebooks/02_2_contacts_descriptive_stats.md)
- [Spend Description](notebooks/02_3_spend_descriptive_stats.md)
- [Deals Description](notebooks/02_4_deals_descriptive_stats.md)

### Product Analytics

Product-level performance and monetization insights.

[Product Analysis](product_analytics/04_product_analyse.md)

---

## Project Structure
```
📦 it-school-analytics/
├── 📁 analytics/
│   ├── 📁 figures/
│   │   └── (figures for analytics)
│   └── 03_analyse.py
│
├── 📁 dashboard/
│   ├── __init__.py
│   ├── app.py
│   ├── charts.py
│   ├── data_prep.py
│   └── 📁assets/
│       └── style.css
│
├── 📁 data/
│   ├── 📁 clean/
│   │   ├── calls_clean.xlsx
│   │   ├── cities_updated.json
│   │   ├── contacts_clean.xlsx
│   │   ├── data_all.xlsx
│   │   ├── deals_clean.xlsx
│   │   └── spend_clean.xlsx
│   └── 📁 raw/
│       ├── calls.xlsx
│       ├── city_data_google_en.json
│       ├── contacts.xlsx
│       ├── deals.xlsx
│       └── spend.xlsx
│
├── 📁 docs/
│   ├── 📁 images/
│   │   └── my_palette.png
│   └── crm_dataset_documentation.md
│
├── 📁 logs/
│   └── (logs)
│
├── 📁 notebooks/
│   ├── 📁 figures/
│   │   └── (figures for data cleaning & descriptive analysis)
│   ├── 01_1_data_preparation.md
│   ├── 01_2_calls_cleaning.md
│   ├── 01_3_contacts_cleaning.md
│   ├── 01_4_spend_cleaning.md
│   ├── 01_5_deals_cleaning.md
│   ├── 02_1_calls_descriptive_stats.md
│   ├── 02_2_contacts_descriptive_stats.md
│   ├── 02_3_spend_descriptive_stats.md
│   ├── 02_4_deals_descriptive_stats.md  
│   ├── 01_data_cleaning.py
│   └── 02_descriptive_statistics.py
│
├── 📁 product_analytics/
│   ├── 📁 figures/
│   │   └── (visual outputs for product metrics)
│   ├── 04_product_analyse.md
│   └── 04_product_analyse.py
│
├── 📁 utils/
│   ├── __init__.py
│   ├── cleaners.py
│   ├── data_io.py
│   ├── data_summary.py
│   ├── descriptive_stats.py
│   ├── logging_setup.py
│   ├── my_palette.py
│   └── product_analysis.py
│
├── Procfile
├── 📄 README.md
└── requirements.txt
```
