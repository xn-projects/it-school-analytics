# Deals Dataset Cleaning

This document provides a **comprehensive overview** of the data cleaning and transformation process for the `Deals` dataset.  

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

This approach ensured that consistent information was retained for recurring contacts.

---

## 3️⃣ Duplicate and Test Data Removal

### Duplicate Removal
Duplicate deals were detected with `find_duplicates()` and cleaned using `clean_duplicates()`.

Additionally, records where **`Lost Reason = "Duplicate"`** were excluded, since these represent intentional duplicates flagged during data entry.

### Removal of Test Data
Two types of test records were identified and removed:
- Rows where `Source = 'Test'`
- Rows where `Page` matched `'/test'` or `'/eng/test'`

---

## 4️⃣ Missing and Invalid IDs

Records with missing deal identifiers (`Id`) were isolated for review and then removed from the dataset.

![Deals Missing ID](figures/deals_missing_id.png)

---

## 5️⃣ Product-Level Filtering

Irrelevant educational programs were excluded to focus analysis on current active courses.

Removed products:
- `Data Analytics`  
- `Find Yourself in IT`

Cleaned dataset now focuses on the relevant products for the target academic portfolio.

---

## 6️⃣ Handling Duplicate Contacts with Empty Key Fields

Duplicate `Contact Name` entries were analyzed.  
If all important columns (`Course duration`, `Months of study`, `Offer Total Amount`, etc.) were empty, such rows were removed as **incomplete duplicates**.

This step reduced noise in the dataset without losing critical business information.

---

## 7️⃣ Datetime Standardization

Datetime columns were converted to `datetime64[ns]`:
- `Created Time`
- `Closing Date`

This enables consistent chronological analysis and filtering.

---

## 8️⃣ City Normalization

To ensure regional consistency, city names were standardized by removing special hyphen characters and applying manual corrections.

| Original Value | Corrected Value |
|----------------|----------------|
| Karl-Liebknecht str. 24, Hildburghausen, Thüringen | Thüringen |
| Vor Ebersbach 1, 77761 Schiltach | Schiltach |
| Poland , Gdansk , Al. Grunwaldzka 7, ap. 1a | Gdańsk |


---

## 9️⃣ Cleaning Monetary Fields

Columns containing monetary values were cleaned and standardized:
- `Initial Amount Paid`
- `Offer Total Amount`

The `clean_amount()` function corrected string-based formats (e.g., commas, symbols) and converted all values to numeric form.

If `Offer Total Amount` was accidentally smaller than `Initial Amount Paid`, the values were swapped to preserve logical order.

Ensured consistent and realistic payment values across all deals.

---

## 1️⃣0️⃣ Filling Payment Type

Payment type was intelligently inferred based on transaction amounts:

| Condition | Assigned Type |
|------------|----------------|
| Both amounts = 0 | `No Payments` |
| Small initial amount (≤ 200 €) | `Reservation` |
| Equal or near-equal amounts | `One Payment` |
| All other cases | `Recurring Payments` |

Unknown cases were labeled `"Unknown"`.

---

## 1️⃣1️⃣ Correcting Logical Inconsistencies in Dates

In some records, `Created Time` appeared **later** than `Closing Date`.  
These timestamps were swapped to maintain logical chronological order.

---

## 1️⃣2️⃣ Filling Missing Closing Dates

For deals with:
- Equal `Months of study` and `Course duration`
- Stage = `Payment Done`
- Missing `Closing Date`

→ The date was imputed as `Created Time + average duration` per product, derived from mode differences.

---

## 1️⃣3️⃣ Normalizing German Language Level

The column `Level of Deutsch` was normalized into a new, standardized field — **`German Level`**.


After verification, the original `Level of Deutsch` column was removed.

✅ Consistent and analytical representation of German proficiency achieved.

---

## 1️⃣4️⃣ Outlier Removal — Abnormal Created Time

Anomalous records with an **earlier-than-expected creation date (October 2022)** were isolated and removed.

![Deals Earliest Rows](figures/deals_earliest_rows.png)


---

## 1️⃣5️⃣ Column Quality Transformation

The `Quality` column contained inconsistent and multi-symbol formats.  
It was standardized by:
- Replacing `F` → `Special`
- Removing unwanted symbols and dashes  
- Extracting the core quality label after “–”
- Filling empty cells with `"Unknown"`

---

## 1️⃣6️⃣ SLA Standardization and Conversion

The `SLA` column was unified to a single time format and converted into total seconds (`SLA Seconds`).

Steps:
1. Convert string and `datetime.time` formats to timedelta  
2. Extract total seconds via `convert_to_seconds()`  
3. Drop the original `SLA` column  

This standardization enables direct quantitative SLA analysis.

---

## 1️⃣7️⃣ Filling Remaining Missing Fields

For categorical columns such as:
`Lost Reason`, `Education Type`, `Deal Owner Name`, `Content`, `Term`, `Campaign`, `Contact Name`  
→ All missing values were replaced with `"Unknown"` to ensure consistency during group operations.

---

## 1️⃣8️⃣ Data Type Conversion

Converted to `Int64`:
- `Course duration`
- `Months of study`
- `Initial Amount Paid`
- `Offer Total Amount`

Optimized memory and grouping performance:
- `Stage`, `Quality`, `Source`, `Product`
- `Lost Reason`, `Education Type`
- `German Level`, `Payment Type`

---

## 1️⃣9️⃣ Final Data Summary

A new summary table confirmed the successful transformation and consistency of all fields.

![Deals Info Clean](figures/deals_info_clean.png)

---

## 2️⃣0️⃣ Results and Exports

| Step | Description |
|------|--------------|
| Intelligent missing value filling | Used modal value per contact |
| Duplicate & test removal | Cleaned technical duplicates and `/test` data |
| Product filtering | Removed non-relevant products |
| Monetary cleanup | Standardized and corrected numeric fields |
| Payment inference | Assigned logical `Payment Type` |
| Datetime logic | Fixed and filled inconsistent or missing timestamps |
| Categorical normalization | Standardized language, quality, and type fields |
| Exports | Saved cleaned dataset and visual reports |

---
