# Descriptive Statistics — Contacts Data (`02_descriptive_statistics.py`)

This section provides an overview of the **Contacts dataset**, focusing on both **numeric** and **categorical** variables.  
The objective is to analyze the structure of contact ownership, identify dominant agents, and assess the distribution of client records across the organization.

---

## Table of Contents

1. [Numeric Fields](#1️⃣-numeric-fields)  
2. [Categorical Fields](#2️⃣-categorical-fields)  
   - [2.1 Overview of Categorical Attributes](#21-overview-of-categorical-attributes)  
   - [2.2 Top 15 Contact Owners by Frequency](#22-top-15-contact-owners-by-frequency)  
3. [Key Insights](#3️⃣-key-insights)  
4. [Next Step](#4️⃣-next-step)

---

## 1️⃣ Numeric Fields

During preprocessing, the `describe_num()` function was executed to detect numerical features.

> **Result:**  
> `No numeric columns found.`  
>  
> The dataset consists entirely of **datetime and categorical information**, such as contact names, ownership, and source details.  
> This confirms that numerical analysis (e.g., mean, standard deviation) is **not applicable** to this dataset.

---

## 2️⃣ Categorical Fields

### 2.1 Overview of Categorical Attributes

Categorical analysis performed via `describe_cat()` revealed structural characteristics and distribution of key text-based fields.

![contacts_stats_cat.png](figures/contacts_stats_cat.png)

> - The dataset includes **18,509 unique contacts** assigned to **27 different owners**.  
> - The **Contact Owner Name** field is categorical and fully populated (no missing values).  
> - **Charlie Davis** is the most frequent owner, managing **2,018 contacts**, which represents **10.9% of the total dataset**.  
> - Ownership distribution indicates a **moderately centralized structure** with several dominant agents.

---

### 2.2 Top 15 Contact Owners by Frequency

The bar chart visualizes the **top 15 contact owners** ranked by the number of clients they manage.

![contacts_owners.png](figures/contacts_owners.png)

> Analytical Observations
> - The top 5 owners (**Charlie Davis**, **Ulysses Adams**, **Julia Nelson**, **Paula Underwood**, **Quincy Vincent**) together manage **over 40%** of all contacts.  
> - **Charlie Davis** alone accounts for **~11%** of total records — a clear operational leader.  
> - Ownership frequency declines gradually after the top 5, showing a **healthy mid-tier of active agents**.  
> - The distribution pattern suggests **centralized but not monopolized ownership**, allowing both control and scalability.
> Business Interpretation
> - **Charlie Davis** likely functions as a key relationship manager or senior CRM agent.  
> - Concentration of contacts in top performers can boost service consistency but also creates **dependency risk**.  
> - Mid-range owners (ranks 6–12) have balanced workloads (≈700–1,100 clients), indicating effective team utilization.  
> - Overall, the **contact allocation model** appears efficient, with gradual workload tapering and no extreme outliers.

---

## 3️⃣ Key Insights

- **Ownership concentration** is evident — a few top agents (led by *Charlie Davis* and *Ulysses Adams*) manage a significant share of the client base.  
- The **distribution of contacts** follows a balanced long-tail pattern: while top performers dominate volume, mid-tier owners maintain strong participation.  
- This structure suggests an **efficient but centralized CRM model**, ensuring both continuity of client relationships and operational scalability.  
- There remains an opportunity to **rebalance workloads** and **broaden ownership diversity**, potentially improving responsiveness and client retention.

---

## 4️⃣ Next Step

The next stage continues with the **Spend dataset**, applying the **same descriptive statistical approach** — analyzing both **numeric** and **categorical** fields to evaluate financial patterns and relationships with previous datasets.

**Continue to:** [02_3_spend_descriptive_stats.md](02_3_spend_descriptive_stats.md)
