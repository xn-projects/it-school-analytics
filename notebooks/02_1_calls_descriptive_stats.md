# Descriptive Statistics — Calls Data (`02_descriptive_statistics.py`)

This analysis explores call data, focusing on **numeric** and **categorical** features.  
The goal is to understand the distribution of call durations, evaluate the impact of logarithmic transformation, and examine ownership patterns among call handlers.

---

## Numeric Fields

### 1️⃣ Descriptive Statistics

A summary of numerical variables — including mean, median, standard deviation, and distribution characteristics.  
![calls_stats_num.png](figures/calls_stats_num.png)

> The dataset contains over 92k calls. The average call duration is **170 seconds**, but the high standard deviation (≈407) and skewness (4.0) indicate a **right-skewed distribution** with many short calls and a few extremely long ones.

---

### 2️⃣ Call Duration Distribution — Before & After Log Transformation

Histogram and KDE plots showing the raw vs. log-transformed call durations.  
![call_duration_orig_vs_log.png](figures/call_duration_orig_vs_log.png)

> The original distribution is highly concentrated near zero with a long tail.  
> After applying a **log transformation**, the distribution becomes smoother and closer to normal — ideal for modeling or statistical inference.

---

### 3️⃣ Violin Plot — Distribution Comparison

Violin plots visualize the spread and quartiles of the original and transformed call durations.  
![call_duration_distribution.png](figures/call_duration_distribution.png)

> The violin plots confirm that the **spread is significantly reduced** after transformation,  
> eliminating extreme outliers and compressing long-duration values into a manageable range.

---

### 4️⃣ Statistical Comparison — Before vs. After Log

Comparison of descriptive measures before and after transformation.
![calls_compare.png](figures/calls_compare.png)  

> The **mean**, **range**, and **variance** drastically decrease after transformation, while **skewness** (4.00 → 0.41) and **kurtosis** (21.95 → -0.90) show a major improvement toward a symmetric, flatter distribution.

Visual representation of percentage change in key statistical metrics.
![call_change.png](figures/call_change.png)

> Most metrics drop by over **90%**, highlighting the stabilizing effect of the transformation.  
> The sharp reduction in variability (Standard Deviation ↓99%) and shape parameters (Skewness ↓90%) confirms better distribution symmetry.

---

##  Categorical Fields

### 5️⃣ Descriptive Statistics for Categorical Variables

A summary table showing unique counts, most frequent values, and frequency shares for categorical attributes.  
![calls_stats_cat.png](figures/calls_stats_cat.png)

> The dataset includes **33 call owners** and over **15000 unique contacts**.  
> Around **90% of calls are outbound**, and the most common owner (“Yara Edwards”) handles **over 9% of all calls**, suggesting a high concentration of workload.

---

### 6️⃣ Top 15 Call Owners — Exclusive & Unique Clients

Bar chart comparing the total number of calls, unique clients, and exclusive clients for the top 15 owners.  
![call_owners.png](figures/call_owners.png)

> **Yara Edwards** leads with 8,532 calls (≈ 9% of total).  
> Only a fraction of contacts are exclusive to a single owner, suggesting a **shared client base** and collaboration across agents.

---

## Key Insights

- **Right-Skewed Data:** Call durations follow a long-tail pattern, typical for communication datasets.
- **Log Transformation Success:** Strongly improves normality and variance stability.
- **Operational imbalance:** a few owners handle most calls.  
- **Client overlap:** many contacts appear under multiple owners. 
- **High Consistency in Status:** Outbound and completed calls dominate, indicating operational uniformity.
