# Getting Started with Data Cleaning (`01_data_cleaning.py`)

This notebook performs the **first step of the data pipeline** — downloading, reading, and logging raw Excel files for the *IT School Analytics* project.


## Table of Contents
1. [Environment Initialization](#1️⃣-environment-initialization)
2. [Importing Custom Utility Functions](#2️⃣-importing-custom-utility-functions)
3. [Logging Setup](#3️⃣-logging-setup)
4. [Downloading Raw Excel Files](#4️⃣-downloading-raw-excel-files)
5. [Reading Data into Pandas DataFrames](#5️⃣-reading-data-into-pandas-dataframes)
6. [Summary of Initial Preparation](#6️⃣-summary-of-initial-preparation)
7. [Next Step](#7️⃣-next-step)

---

## 1️⃣ Environment Initialization

The work was carried out in **Google Colab**, which provides seamless integration with GitHub and an automatic Python runtime environment.  

At the beginning of the script, all essential libraries are installed and imported:
- **dataframe-image** — for saving pandas DataFrames as images,  
- **matplotlib** — for building visualizations,  
- **pandas** and **numpy** — for structured data and numerical operations.

Additionally, standard Python modules such as `os`, `datetime`, `re`, `logging`, `time`, and `warnings` were used for file management, logging, and handling warnings.

---

## 2️⃣ Importing Custom Utility Functions

A set of project-specific helper functions and classes was imported from the `utils` module to support the data cleaning workflow:

- **setup_logging()** — initializes the logging system,  
- **log_section()** — marks logical sections in the logs,  
- **DataSummary** — generates statistical summaries of dataset structure,  
- **find_duplicates()**, **clean_duplicates()** — for duplicate detection and removal,  
- **convert_columns()** — converts columns to proper data types,  
- **clean_amount()**, **normalize_german_level()**, **convert_to_seconds()** — normalization and transformation utilities,  
- **load_files()**, **save_clean_data()**, **save_plot()** — handle file loading, saving, and visualization.

This modular structure ensures clarity and reusability across all data-cleaning stages.

---

## 3️⃣ Logging Setup

The **setup_logging()** function activates a structured logging system that records each stage of the workflow:
- file downloads,  
- data transformations,  
- cleaning results and anomalies.

Logs are displayed in the console and saved to file, allowing for full traceability of the cleaning process.

---

## 4️⃣ Downloading Raw Excel Files

Data was downloaded directly from the project’s GitHub repository:

**Repository:**  
[`xn-projects/it-school-analytics`](https://github.com/xn-projects/it-school-analytics)

**Path:**  
`/data/raw/`

Files downloaded:
- `calls.xlsx` — call database,  
- `contacts.xlsx` — contact database,  
- `deals.xlsx` — deal database,  
- `spend.xlsx` — marketing spend data.

The **load_files()** function handles file retrieval and validation.  
Once complete, the log reports:  
> *“Downloaded 4 files successfully.”*

---

## 5️⃣ Reading Data into Pandas DataFrames

Each Excel file was read into a **pandas.DataFrame** using the `openpyxl` engine.  
To ensure consistent typing, several columns were explicitly defined as strings during import:

| File | Columns (dtype enforced) | Description |
|------|---------------------------|--------------|
| `calls.xlsx` | `Id`, `CONTACTID` → `str` | Keep identifiers as strings |
| `contacts.xlsx` | `Id` → `str` | Ensure proper ID import |
| `deals.xlsx` | `Id`, `Contact Name` → `str` | Preserve textual data |
| `spend.xlsx` | — | Default import |

After reading, the data was successfully stored in the following objects:
- `df_calls`  
- `df_contacts`  
- `df_deals`  
- `df_spend`

The log confirms:
> *“All files successfully loaded into DataFrames.”*

---

## 6️⃣ Summary of Initial Preparation

| Step | Status |
|------|--------|
| Library installation | Completed successfully |
| Utility import | All custom functions loaded |
| Logging setup | Activated and running |
| File download | 4 files retrieved from GitHub |
| Data import | All datasets read into DataFrames |

---

## 7️⃣ Next Step

With the environment ready and the raw data imported, the project proceeds to **data cleaning** — beginning with the `Calls` dataset, Continue to: [01_2_calls_cleaning.md](01_2_calls_cleaning.md)
