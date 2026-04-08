import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-card h2 { font-size: 2rem; margin: 0; font-weight: 700; }
    .kpi-card p  { font-size: 0.9rem; margin: 0; opacity: 0.85; }

    .kpi-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-card-green h2 { font-size: 2rem; margin: 0; font-weight: 700; }
    .kpi-card-green p  { font-size: 0.9rem; margin: 0; opacity: 0.85; }

    .kpi-card-orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-card-orange h2 { font-size: 2rem; margin: 0; font-weight: 700; }
    .kpi-card-orange p  { font-size: 0.9rem; margin: 0; opacity: 0.85; }

    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #667eea;
        padding-left: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    # Supports both local file and uploaded file
    possible_paths = [
        "Global Superstore.csv",
        "Global_Superstore.csv",
        "global_superstore.csv",
        "Sample - Superstore.csv",
        "data/Global Superstore.csv"
    ]
    df = None
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path, encoding="latin-1")
            break

    if df is None:
        return None

    # ── Column name normalisation ──────────────────────────────────────
    df.columns = df.columns.str.strip()

    # ── Drop rows missing critical fields ─────────────────────────────
    df.dropna(subset=["Sales", "Profit", "Region", "Category"], inplace=True)

    # ── Parse Order Date ───────────────────────────────────────────────
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month
        df["Month Name"] = df["Order Date"].dt.strftime("%b")

    # ── Numeric columns ────────────────────────────────────────────────
    for col in ["Sales", "Profit", "Discount", "Quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ── Derived column ─────────────────────────────────────────────────
    df["Profit Margin (%)"] = (df["Profit"] / df["Sales"].replace(0, pd.NA) * 100).round(2)

    return df


# ─────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────
df_raw = load_data()

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.title("🛒 Global Superstore — Business Dashboard")
st.caption("Interactive sales & profitability analytics | Internship Task 5 · Areeba Hassan")
st.markdown("---")

# ─────────────────────────────────────────────
# FILE UPLOAD FALLBACK
# ─────────────────────────────────────────────
if df_raw is None:
    st.warning("⚠️  Dataset file not found locally. Please upload the **Global Superstore CSV** file below.")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded:
        df_raw = pd.read_csv(uploaded, encoding="latin-1")
        df_raw.columns = df_raw.columns.str.strip()
        df_raw.dropna(subset=["Sales", "Profit", "Region", "Category"], inplace=True)
        if "Order Date" in df_raw.columns:
            df_raw["Order Date"] = pd.to_datetime(df_raw["Order Date"], dayfirst=True, errors="coerce")
            df_raw["Year"] = df_raw["Order Date"].dt.year
            df_raw["Month"] = df_raw["Order Date"].dt.month
            df_raw["Month Name"] = df_raw["Order Date"].dt.strftime("%b")
        for col in ["Sales", "Profit", "Discount", "Quantity"]:
            if col in df_raw.columns:
                df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce").fillna(0)
        df_raw["Profit Margin (%)"] = (
            df_raw["Profit"] / df_raw["Sales"].replace(0, pd.NA) * 100
        ).round(2)
    else:
        st.stop()


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")

    # Region
    regions = sorted(df_raw["Region"].dropna().unique().tolist())
    sel_region = st.multiselect("Region", regions, default=regions)

    # Category
    categories = sorted(df_raw["Category"].dropna().unique().tolist())
    sel_category = st.multiselect("Category", categories, default=categories)

    # Sub-Category (depends on category selection)
    sub_df = df_raw[df_raw["Category"].isin(sel_category)] if sel_category else df_raw
    sub_cats = sorted(sub_df["Sub-Category"].dropna().unique().tolist()) if "Sub-Category" in df_raw.columns else []
    if sub_cats:
        sel_subcat = st.multiselect("Sub-Category", sub_cats, default=sub_cats)
    else:
        sel_subcat = []

    # Year
    if "Year" in df_raw.columns:
        years = sorted(df_raw["Year"].dropna().unique().tolist())
        sel_year = st.multiselect("Year", years, default=years)
    else:
        sel_year = []

    st.markdown("---")
    st.caption("Global Superstore Dataset · Kaggle")

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
df = df_raw.copy()

if sel_region:
    df = df[df["Region"].isin(sel_region)]
if sel_category:
    df = df[df["Category"].isin(sel_category)]
if sel_subcat and "Sub-Category" in df.columns:
    df = df[df["Sub-Category"].isin(sel_subcat)]
if sel_year and "Year" in df.columns:
    df = df[df["Year"].isin(sel_year)]

if df.empty:
    st.error("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ─────────────────────────────────────────────
# KPI SECTION
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

total_sales   = df["Sales"].sum()
total_profit  = df["Profit"].sum()
total_orders  = df["Order ID"].nunique() if "Order ID" in df.columns else len(df)
avg_margin    = df["Profit Margin (%)"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
        <div class="kpi-card">
            <p>Total Sales</p>
            <h2>${total_sales:,.0f}</h2>
        </div>""", unsafe_allow_html=True)

with c2:
    color_class = "kpi-card-green" if total_profit >= 0 else "kpi-card-orange"
    st.markdown(f"""
        <div class="{color_class}">
            <p>Total Profit</p>
            <h2>${total_profit:,.0f}</h2>
        </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
        <div class="kpi-card-orange">
            <p>Total Orders</p>
            <h2>{total_orders:,}</h2>
        </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
        <div class="kpi-card-green">
            <p>Avg Profit Margin</p>
            <h2>{avg_margin:.1f}%</h2>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP 5 CUSTOMERS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🏆 Top 5 Customers by Sales</div>', unsafe_allow_html=True)

if "Customer Name" in df.columns:
    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    top_customers.columns = ["Customer", "Total Sales"]
    top_customers["Total Sales"] = top_customers["Total Sales"].round(2)
    top_customers.index = top_customers.index + 1  # 1-based rank

    col_t, col_b = st.columns([1, 2])

    with col_t:
        st.dataframe(
            top_customers.style.format({"Total Sales": "${:,.2f}"}),
            use_container_width=True
        )

    with col_b:
        fig_cust = px.bar(
            top_customers,
            x="Total Sales",
            y="Customer",
            orientation="h",
            color="Total Sales",
            color_continuous_scale="Purples",
            text_auto=".2s",
            title="Top 5 Customers by Sales"
        )
        fig_cust.update_layout(
            yaxis=dict(categoryorder="total ascending"),
            showlegend=False,
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_cust, use_container_width=True)

# ─────────────────────────────────────────────
# CHART ROW 1: Sales by Region | Sales by Category
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📈 Sales & Profit by Segment</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    region_df = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    fig_reg = px.bar(
        region_df,
        x="Region",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales & Profit by Region",
        color_discrete_sequence=["#667eea", "#38ef7d"]
    )
    fig_reg.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_reg, use_container_width=True)

with col2:
    cat_df = df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig_cat = px.pie(
        cat_df,
        values="Sales",
        names="Category",
        title="Sales Distribution by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ─────────────────────────────────────────────
# CHART ROW 2: Sub-Category Profit | Sales over Time
# ─────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    if "Sub-Category" in df.columns:
        sub_df_chart = (
            df.groupby("Sub-Category")[["Sales", "Profit"]]
            .sum()
            .sort_values("Profit", ascending=True)
            .reset_index()
        )
        fig_sub = px.bar(
            sub_df_chart,
            x="Profit",
            y="Sub-Category",
            orientation="h",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Profit by Sub-Category",
            text_auto=".2s"
        )
        fig_sub.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_sub, use_container_width=True)

with col4:
    if "Order Date" in df.columns:
        monthly = (
            df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
            .sum()
            .reset_index()
        )
        monthly["Order Date"] = monthly["Order Date"].astype(str)
        fig_time = px.line(
            monthly,
            x="Order Date",
            y="Sales",
            title="Monthly Sales Trend",
            markers=True,
            color_discrete_sequence=["#667eea"]
        )
        fig_time.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(tickangle=-45)
        )
        st.plotly_chart(fig_time, use_container_width=True)

# ─────────────────────────────────────────────
# CHART ROW 3: Discount vs Profit scatter
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🔬 Discount Impact Analysis</div>', unsafe_allow_html=True)

if "Discount" in df.columns:
    scatter_df = df[["Sales", "Profit", "Discount", "Category"]].dropna()
    fig_scat = px.scatter(
        scatter_df,
        x="Discount",
        y="Profit",
        color="Category",
        size="Sales",
        opacity=0.6,
        title="Discount vs Profit (bubble size = Sales)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_scat.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_scat, use_container_width=True)

# ─────────────────────────────────────────────
# RAW DATA EXPANDER
# ─────────────────────────────────────────────
with st.expander("📋 View Filtered Raw Data"):
    st.dataframe(df.reset_index(drop=True), use_container_width=True)
    st.caption(f"{len(df):,} rows · {df.shape[1]} columns")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Streamlit & Plotly · Global Superstore Dataset (Kaggle) · Areeba Hassan — DevelopersHub Internship Task 5")
