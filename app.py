import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Product Profitability Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 Product Line Profitability & Margin Performance Dashboard")

st.markdown(
    """
    **Nassau Candy Distributor Analysis**

    This dashboard provides an interactive analysis of product profitability,
    gross margin, division performance, regional performance, and Pareto
    contribution.
    """
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        dayfirst=True,
        errors="coerce"
    )

    return df


df = load_data()

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

df["Gross Margin %"] = (
    df["Gross Profit"] / df["Sales"]
) * 100

df["Profit per Unit"] = (
    df["Gross Profit"] / df["Units"]
)

df["Cost per Unit"] = (
    df["Cost"] / df["Units"]
)

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

divisions = ["All"] + sorted(
    df["Division"].dropna().unique().tolist()
)

selected_division = st.sidebar.selectbox(
    "Select Division",
    divisions
)

regions = ["All"] + sorted(
    df["Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

filtered_df = df.copy()

if selected_division != "All":
    filtered_df = filtered_df[
        filtered_df["Division"] == selected_division
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------

total_sales = filtered_df["Sales"].sum()
total_cost = filtered_df["Cost"].sum()
total_profit = filtered_df["Gross Profit"].sum()

gross_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

profit_per_unit = (
    total_profit / filtered_df["Units"].sum()
    if filtered_df["Units"].sum() != 0 else 0
)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Sales",
    f"₹{total_sales:,.2f}"
)

col2.metric(
    "Total Cost",
    f"₹{total_cost:,.2f}"
)

col3.metric(
    "Gross Profit",
    f"₹{total_profit:,.2f}"
)

col4.metric(
    "Gross Margin",
    f"{gross_margin:.2f}%"
)

col5.metric(
    "Profit / Unit",
    f"₹{profit_per_unit:.2f}"
)

st.divider()

# --------------------------------------------------
# Product Profitability
# --------------------------------------------------

st.header("🍫 Product Profitability Analysis")

product_analysis = (
    filtered_df
    .groupby("Product Name")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum")
    )
    .reset_index()
)

product_analysis["Gross Margin %"] = (
    product_analysis["Total_Gross_Profit"]
    / product_analysis["Total_Sales"]
) * 100

product_analysis["Profit per Unit"] = (
    product_analysis["Total_Gross_Profit"]
    / product_analysis["Total_Units"]
)

product_analysis = product_analysis.sort_values(
    "Total_Gross_Profit",
    ascending=False
)

st.dataframe(
    product_analysis,
    use_container_width=True
)

# --------------------------------------------------
# Top Products Chart
# --------------------------------------------------

st.subheader("🏆 Top 10 Products by Gross Profit")

top_products = product_analysis.head(10)

fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    top_products["Product Name"][::-1],
    top_products["Total_Gross_Profit"][::-1]
)

ax.set_xlabel("Gross Profit")
ax.set_ylabel("Product")
ax.set_title("Top 10 Products by Gross Profit")

plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# Division Analysis
# --------------------------------------------------

st.header("🏢 Division Performance")

division_analysis = (
    filtered_df
    .groupby("Division")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum")
    )
    .reset_index()
)

division_analysis["Gross Margin %"] = (
    division_analysis["Total_Gross_Profit"]
    / division_analysis["Total_Sales"]
) * 100

division_analysis["Profit per Unit"] = (
    division_analysis["Total_Gross_Profit"]
    / division_analysis["Total_Units"]
)

st.dataframe(
    division_analysis,
    use_container_width=True
)

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    division_analysis["Division"],
    division_analysis["Total_Gross_Profit"]
)

ax.set_title("Gross Profit by Division")
ax.set_xlabel("Division")
ax.set_ylabel("Gross Profit")

plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# Regional Analysis
# --------------------------------------------------

st.header("🌎 Regional Performance")

region_analysis = (
    filtered_df
    .groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Gross_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum")
    )
    .reset_index()
)

region_analysis["Gross Margin %"] = (
    region_analysis["Total_Gross_Profit"]
    / region_analysis["Total_Sales"]
) * 100

region_analysis["Profit per Unit"] = (
    region_analysis["Total_Gross_Profit"]
    / region_analysis["Total_Units"]
)

st.dataframe(
    region_analysis,
    use_container_width=True
)

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(
    region_analysis["Region"],
    region_analysis["Total_Gross_Profit"]
)

ax.set_title("Gross Profit by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Gross Profit")

plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# Pareto Analysis
# --------------------------------------------------

st.header("📊 Pareto Analysis")

pareto = product_analysis[
    ["Product Name", "Total_Gross_Profit"]
].copy()

pareto = pareto.sort_values(
    "Total_Gross_Profit",
    ascending=False
).reset_index(drop=True)

pareto["Cumulative Gross Profit"] = (
    pareto["Total_Gross_Profit"].cumsum()
)

pareto["Cumulative Profit %"] = (
    pareto["Cumulative Gross Profit"]
    / pareto["Total_Gross_Profit"].sum()
) * 100

st.dataframe(
    pareto,
    use_container_width=True
)

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(
    pareto["Product Name"].head(10),
    pareto["Total_Gross_Profit"].head(10)
)

ax1.set_xlabel("Product")
ax1.set_ylabel("Gross Profit")
ax1.tick_params(axis="x", rotation=45)

ax2 = ax1.twinx()

ax2.plot(
    pareto["Product Name"].head(10),
    pareto["Cumulative Profit %"].head(10),
    marker="o"
)

ax2.axhline(
    80,
    linestyle="--"
)

ax2.set_ylabel("Cumulative Gross Profit (%)")
ax2.set_ylim(0, 110)

plt.title("Pareto Analysis of Product Gross Profit")

plt.tight_layout()

st.pyplot(fig)

# --------------------------------------------------
# Business Insights
# --------------------------------------------------

st.header("💡 Business Insights")

top_product = product_analysis.iloc[0]["Product Name"]
top_profit = product_analysis.iloc[0]["Total_Gross_Profit"]

st.write(
    f"• **{top_product}** is the highest gross-profit contributing product "
    f"with approximately ₹{top_profit:,.2f} gross profit."
)

st.write(
    f"• The overall gross margin for the selected filters is "
    f"**{gross_margin:.2f}%**."
)

st.write(
    f"• The selected products generated approximately "
    f"**₹{total_profit:,.2f}** in gross profit."
)

st.write(
    "• Pareto analysis helps identify products responsible for the "
    "largest share of overall profitability."
)

# --------------------------------------------------
# Dataset Summary
# --------------------------------------------------

st.header("📋 Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Rows",
    f"{filtered_df.shape[0]:,}"
)

col2.metric(
    "Columns",
    f"{filtered_df.shape[1]:,}"
)

col3.metric(
    "Products",
    f"{filtered_df['Product Name'].nunique():,}"
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown(
    """
    **Developed by Kartik Dnyaneshwar Borikar**

    Data Analyst Internship Project | Unified Mentor
    """
)
