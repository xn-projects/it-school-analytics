# Spend Dataset Cleaning (`01_data_cleaning.py`)

This document provides a detailed explanation of the **data cleaning process** for the `Spend` dataset.  

---

## 1️⃣ Initial Data Overview

The raw dataset was analyzed using the `DataSummary` utility, which profiled each field for completeness, data type, and distinct values.  
This helped identify issues such as duplicate records, missing fields, and test data that needed to be removed.
 
![Spend Info Raw](figures/spend_info_raw.png)

---

## 2️⃣ Duplicate Detection and Removal

Full-row duplicates were identified using the `find_duplicates()` function  
and then removed with the `clean_duplicates()` routine.

**Result:** All duplicate entries were successfully removed.  
**Output DataFrame:** `clean_spend`

This ensured that every advertising record (by date, source, campaign, and ad) is unique and consistent.

---

## 3️⃣ Removal of Test Records

A separate check was performed for rows where the **`Source`** field was labeled as `Test`.  
These represented experimental or placeholder entries not relevant for production analytics.

All such records were removed to maintain dataset purity.

**Removed:** All rows where `Source = 'Test'`  

---

## 4️⃣ Handling Missing Fields

To standardize incomplete campaign metadata, missing values in the following columns were filled with `'Unknown'`:

- `Campaign`  
- `AdGroup`  
- `Ad`

This approach preserves data structure while making missingness explicit for analysts.

**Result:** All missing text fields replaced with `"Unknown"`  
**Rationale:** Prevents merge errors during joins with CRM and Ad tracking data.

---

## 5️⃣ Type Conversion

The `Source` column was converted to a **categorical** data type to optimize memory usage and enable efficient grouping and filtering in further analysis.

**Converted columns:** `Source` → `category`

---

## 6️⃣ Final Data Summary (After Cleaning)

A new data summary was generated using the `DataSummary` class to verify cleaning results.

![Spend Info Clean](figures/spend_info_clean.png)

---

## 7️⃣ Results and Exports

| Step | Description |
|------|--------------|
| Data profiling | Created initial field summary via `DataSummary` |
| Duplicate removal | Removed fully identical records |
| Test data removal | Excluded rows where `Source = 'Test'` |
| Missing fields | Replaced with `"Unknown"` for key metadata columns |
| Type conversion | Converted `Source` to categorical type |
| Exports | Saved clean dataset and PNG summaries |

---

## Next step:
Proceed with cleaning and enrichment of the **Deals** dataset to link ad performance with lead conversion.
