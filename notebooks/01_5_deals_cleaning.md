# Deals Dataset Cleaning (`01_data_cleaning.py`)

This document provides a **comprehensive overview** of the data cleaning and transformation process for the `Deals` dataset.  

## Table of Contents

1. [Initial Data Overview](#1️⃣-initial-data-overview)  
2. [Intelligent Filling of Missing Values](#2️⃣-intelligent-filling-of-missing-values)  
3. [Duplicate and Test Data Removal](#3️⃣-duplicate-and-test-data-removal)  
4. [Missing and Invalid IDs](#4️⃣-missing-and-invalid-ids)  
5. [Product-Level Filtering](#5️⃣-product-level-filtering)  
6. [Handling Duplicate Contacts with Empty Key Fields](#6️⃣-handling-duplicate-contacts-with-empty-key-fields)  
7. [Datetime Standardization](#7️⃣-datetime-standardization)  
8. [City Normalization and Geodata Enrichment](#8️⃣-city-normalization-and-geodata-enrichment)  
9. [Cleaning Monetary Fields](#9️⃣-cleaning-monetary-fields)  
10. [Filling Payment Type](#1️⃣0️⃣-filling-payment-type)  
11. [Correcting Logical Inconsistencies in Dates](#1️⃣1️⃣-correcting-logical-inconsistencies-in-dates)  
12. [Filling Missing Closing Dates](#1️⃣2️⃣-filling-missing-closing-dates)  
13. [Normalizing German Language Level](#1️⃣3️⃣-normalizing-german-language-level)  
14. [Outlier Removal — Abnormal Created Time](#1️⃣4️⃣-outlier-removal--abnormal-created-time)  
15. [Column Quality Transformation](#1️⃣5️⃣-column-quality-transformation)  
16. [SLA Standardization and Conversion](#1️⃣6️⃣-sla-standardization-and-conversion)  
17. [Filling Remaining Missing Fields](#1️⃣7️⃣-filling-remaining-missing-fields)  
18. [Data Type Conversion](#1️⃣8️⃣-data-type-conversion)
19. [Final Data Summary](#1️⃣9️⃣-final-data-summary)
20. [Results and Exports](#2️⃣0️⃣1️-results-and-exports)
21. [Next Step](#2️⃣1️⃣-next-step)  

---

## 1️⃣ Initial Data Overview

The raw dataset was profiled using the `DataSummary` utility to identify data types, missing values, and unique entries across all columns.

![Deals Info Raw](figures/deals_info_raw.png)

The initial inspection revealed:
- Presence of duplicate records  
- Incomplete city and language fields  
- Test and demo data  
- Irregular numeric and time formats  
- Occasional logical inconsistencies (e.g., inverted dates)

---

## 2️⃣ Intelligent Filling of Missing Values

To preserve information integrity, missing values were filled **based on frequent values per contact**.  
The following columns were completed using the most common (mode) value within each `Contact Name` group:

| Column | Filling Logic |
|---------|----------------|
| `City` | Filled from other deals of the same contact |
| `Level of Deutsch` | Filled with the most frequent value per contact |
| `Deal Owner Name` | Filled using mode from contact’s other records |
| `Course duration` | Filled using most frequent combination of `(Contact Name, Product)` |

This ensured consistency for recurring contacts and products.

---

## 3️⃣ Duplicate and Test Data Removal

### Duplicate Removal
Duplicate deals were detected with `find_duplicates()` and cleaned using `clean_duplicates()`.

Additionally, records where `Lost Reason = "Duplicate"` were excluded.

### Removal of Test Data
Rows where `Source = 'Test'` were identified and deleted to ensure analytical accuracy.

---

## 4️⃣ Missing and Invalid IDs

Records with missing `Id` were isolated, reviewed, and removed from the dataset.

![Deals Missing ID](figures/deals_missing_id.png)

---

## 5️⃣ Product-Level Filtering

Irrelevant or deprecated educational programs were removed:
- `Data Analytics`
- `Find Yourself in IT`
  
---

## 6️⃣ Handling Duplicate Contacts with Empty Key Fields

Duplicate `Contact Name` entries were analyzed.  
If all key fields (`Course duration`, `Months of study`, `Offer Total Amount`, etc.) were empty, such rows were removed as incomplete duplicates.

This reduced noise while preserving essential deal information.

---

## 7️⃣ Datetime Standardization

Datetime columns were converted to `datetime64[ns]`:
- `Created Time`
- `Closing Date`

If `Created Time` was later than `Closing Date`, the values were **swapped** to maintain chronological logic.

---

## 8️⃣ City Normalization and Geodata Enrichment

City names were cleaned and standardized by:
- Removing special hyphen characters  
- Applying manual corrections:

| Original Value | Corrected Value |
|----------------|----------------|
| Karl-Liebknecht str. 24, Hildburghausen, Thüringen | Thüringen |
| Vor Ebersbach 1, 77761 Schiltach | Schiltach |
| Poland , Gdansk , Al. Grunwaldzka 7, ap. 1a | Gdańsk |

Additionally, an updated **city metadata file** (`cities_updated.json`) was created with:
- normalized city names,
- country and federal state,
- latitude and longitude.

New columns added to the dataset:
| Column | Description |
|---------|-------------|
| `Federal state` | German federal region derived from JSON |
| `Country` | Country of the city |
| `Latitude` | Geographic latitude |
| `Longitude` | Geographic longitude |

---

## 9️⃣ Cleaning Monetary Fields

Monetary columns were standardized using the `clean_amount()` utility:
- `Initial Amount Paid`
- `Offer Total Amount`

If `Offer Total Amount` < `Initial Amount Paid`, the values were swapped to restore logical order.  
All currency symbols and separators were cleaned for numeric consistency.

---

## 1️⃣0️⃣ Filling Payment Type

Payment type was inferred based on transaction logic:

| Condition | Assigned Type |
|------------|----------------|
| Both amounts = 0 | `No Payments` |
| Small initial amount (≤ 200 €) | `Reservation` |
| Equal or near-equal amounts | `One Payment` |
| All other cases | `Recurring Payments` |
| Unresolved cases | `Unknown` |

This automated classification ensures consistent financial analytics.

---

## 1️⃣1️⃣ Correcting Logical Inconsistencies in Dates

In cases where `Created Time` was later than `Closing Date`, values were swapped to maintain chronological integrity.

---

## 1️⃣2️⃣ Filling Missing Closing Dates

If a record met the following:
- `Months of study` = `Course duration`
- `Stage` = `Payment Done`
- `Closing Date` = missing  

Then the missing `Closing Date` was filled with:  
→ `Created Time + average (mode) duration per Product`.

---

## 1️⃣3️⃣ Normalizing German Language Level

The column `Level of Deutsch` was normalized using the custom `normalize_german_level()` function,  
producing a clean categorical field `German Level`.

| Example Distribution | Count |
|----------------------|--------|
| A1–C2 | Standard CEFR levels |
| Unknown | Missing or invalid values |

The original column `Level of Deutsch` was removed after transformation.

---

## 1️⃣4️⃣ Outlier Removal — Abnormal Created Time

Anomalous rows with unusually early `Created Time` (October 2022) were identified and removed.

![Deals Earliest Rows](figures/deals_earliest_rows.png)

---

## 1️⃣5️⃣ Column Quality Transformation

The `Quality` column was standardized by:
- Replacing single-letter codes (`F`) → `Special`
- Removing dashes and extracting the meaningful label
- Filling blanks with `"Unknown"`

---

## 1️⃣6️⃣ SLA Standardization and Conversion

The `SLA` column was cleaned and converted into multiple time-based metrics:
1. Converted string and `datetime.time` formats to timedelta  
2. Created new numeric fields:
   - `SLA Seconds`
   - `SLA Minutes`
   - `SLA Hours`  
3. Dropped the original `SLA` column after successful conversion.

This enables time-based performance and response analysis at different levels.

---

## 1️⃣7️⃣ Filling Remaining Missing Fields

The following text-based columns were filled with `"Unknown"`:
`Lost Reason`, `Education Type`, `Deal Owner Name`, `Content`, `Term`, `Campaign`, `Contact Name`, `Federal state`, `Country`.

Additionally:
- Empty or invalid `City` values (`'-'`, `' '`, `'None'`, etc.) were replaced with `"Unknown"`.
- The `Term` column’s underscores (`_`) were replaced with `"Unknown"`.

---

## 1️⃣8️⃣ Data Type Conversion

Converted to `Int64`:
- `Course duration`
- `Months of study`
- `Initial Amount Paid`
- `Offer Total Amount`

Categorical conversion for analytical grouping:
| Column | Type |
|---------|------|
| `Stage` | category |
| `Quality` | category |
| `Source` | category |
| `Product` | category |
| `Lost Reason` | category |
| `Education Type` | category |
| `German Level` | category |
| `Payment Type` | category |

---

## 1️⃣9️⃣ Final Data Summary

A final dataset summary was generated to verify successful cleaning and consistency.

![Deals Info Clean](figures/deals_info_clean.png)

---

## 2️⃣0️⃣ Results and Exports

| Step | Description |
|------|--------------|
| Missing value imputation | Mode-based filling per contact and product |
| Duplicate & test removal | Removed flagged and test records |
| Product filtering | Focused on active academic programs |
| Geodata enrichment | Added city, region, and coordinate data |
| Monetary cleanup | Standardized and corrected financial fields |
| Payment inference | Derived logical `Payment Type` values |
| Datetime logic | Corrected and filled time inconsistencies |
| Categorical normalization | Standardized language, quality, and type fields |
| SLA conversion | Extracted multiple time-based measures |
| Exports | Saved cleaned dataset and generated summary visuals |


## 2️⃣1️⃣ Next Step

With the Deals dataset fully cleaned, verified, and ready for analysis, the next stage focuses on **Descriptive Statistics** — summarizing numerical and categorical distributions, identifying key trends, and validating data quality through exploratory metrics and visualizations.

**Continue to:** [02_1_calls_descriptive_stats.md](02_1_calls_descriptive_stats.md)
