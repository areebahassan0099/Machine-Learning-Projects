# 🛒 Global Superstore — Interactive Business Dashboard

An interactive Streamlit dashboard built on the **Global Superstore** dataset (Kaggle).

---

## 🎯 Objective

To explore business performance across regions, product categories, and customer segments using an interactive, filter-driven dashboard that makes it easy for stakeholders to derive actionable insights from sales and profitability data.

---

## 🗂 Dataset

**Global Superstore Dataset** — available on [Kaggle](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset)

- ~51,000 rows of transactional order data
- Columns include: Order ID, Order Date, Region, Category, Sub-Category, Customer Name, Sales, Profit, Quantity, Discount, Shipping details

---

## 🔧 Approach

### 1. Data Loading & Cleaning
- Loaded CSV with `latin-1` encoding to handle special characters
- Dropped rows with missing values in critical columns (`Sales`, `Profit`, `Region`, `Category`)
- Parsed `Order Date` to extract year and month features
- Computed a derived `Profit Margin (%)` column

### 2. Sidebar Filters (Dynamic)
Users can slice the entire dashboard by:
- **Region** — Africa, Asia Pacific, Canada, EMEA, Europe, LATAM, US
- **Category** — Furniture, Office Supplies, Technology
- **Sub-Category** — dynamically updates based on Category selection
- **Year** — filter by order year(s)

All KPIs and charts respond live to filter changes.

### 3. KPIs
| Metric | Description |
|---|---|
| Total Sales | Sum of all sales in filtered view |
| Total Profit | Sum of all profit (color-coded green/red) |
| Total Orders | Count of unique Order IDs |
| Avg Profit Margin (%) | Mean profit margin across filtered rows |

### 4. Visualisations
| Chart | Purpose |
|---|---|
| Top 5 Customers (bar) | Revenue contribution by top customers |
| Sales & Profit by Region (grouped bar) | Compare regional performance |
| Sales Distribution by Category (donut) | Category-level sales share |
| Profit by Sub-Category (horizontal bar) | Identify loss-making vs profitable sub-categories |
| Monthly Sales Trend (line) | Time-series view of sales trajectory |
| Discount vs Profit (scatter + bubble) | Understand impact of discounting on profitability |

---

## 💡 Key Findings

1. **Technology** drives the highest sales but **Office Supplies** tends to have more consistent margins.
2. **Tables and Bookcases** (Furniture sub-categories) are consistently loss-making — high discounts are a likely contributor.
3. The **Discount vs Profit** scatter chart shows a clear negative relationship: orders with discounts above ~30% commonly yield negative profit.
4. Sales show a **seasonal uptick** toward Q4 (Oct–Dec), likely driven by year-end purchasing cycles.
5. **Consumer segment** customers dominate order volume, but **Corporate** customers contribute disproportionately higher average order values.

---

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run the App
1. Download the **Global Superstore CSV** from [Kaggle](https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset) and place it in the project root as:
   ```
   Global Superstore.csv
   ```
2. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```
3. The app will open at `http://localhost:8501` in your browser.

> **Note:** If the CSV is not found locally, the app provides a drag-and-drop file uploader as a fallback.

---

## 📁 Project Structure

```
global-superstore-dashboard/
│
├── app.py               ← Main Streamlit application
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Dashboard framework |
| Pandas | Data loading & transformation |
| Plotly Express | Interactive charts |

---

## 👩‍💻 Author

**Areeba Hassan** — Task 5


