import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Sales Analytics")
st.caption("Data Cleaning + Visualization Pipeline")

# Load dataset
BASE_DIR = Path(__file__).resolve().parent

try:
    df = pd.read_csv(
        BASE_DIR / "cleaned_ecommerce_sales.csv"
    )
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

# Convert date
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

# Check required columns
required_columns = [
    "order_date",
    "product_category",
    "region",
    "order_status",
    "payment_method",
    "product_name",
    "net_amount"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in CSV: {missing_columns}"
    )
    st.write("Available columns:")
    st.write(df.columns.tolist())
    st.stop()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Dashboard Filters")

categories = sorted(
    df["product_category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)

regions = sorted(
    df["region"]
    .dropna()
    .unique()
    .tolist()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

statuses = sorted(
    df["order_status"]
    .dropna()
    .unique()
    .tolist()
)

selected_statuses = st.sidebar.multiselect(
    "Order Status",
    statuses,
    default=statuses
)

# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------

filtered_df = df[
    df["product_category"].isin(selected_categories)
    & df["region"].isin(selected_regions)
    & df["order_status"].isin(selected_statuses)
].copy()

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

total_orders = len(filtered_df)

total_revenue = filtered_df["net_amount"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

delivered_orders = (
    filtered_df["order_status"]
    .astype(str)
    .str.lower()
    .eq("delivered")
    .sum()
)

delivered_rate = (
    delivered_orders / total_orders * 100
    if total_orders > 0
    else 0
)

cancelled_returned = (
    filtered_df["order_status"]
    .astype(str)
    .str.lower()
    .isin(["cancelled", "returned"])
    .sum()
)

cancelled_returned_rate = (
    cancelled_returned / total_orders * 100
    if total_orders > 0
    else 0
)

# ---------------------------------------------------------
# KPI DISPLAY
# ---------------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col2.metric(
    "Total Revenue",
    f"₹{total_revenue:,.2f}"
)

col3.metric(
    "Average Order Value",
    f"₹{average_order_value:,.2f}"
)

col4.metric(
    "Delivered Rate",
    f"{delivered_rate:.1f}%"
)

col5.metric(
    "Cancelled / Returned",
    f"{cancelled_returned_rate:.1f}%"
)

st.divider()

# ---------------------------------------------------------
# REVENUE BY MONTH
# ---------------------------------------------------------

st.subheader("📈 Monthly Revenue")

monthly_revenue = (
    filtered_df
    .assign(
        month=filtered_df["order_date"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("month", as_index=False)["net_amount"]
    .sum()
)

fig_monthly = px.line(
    monthly_revenue,
    x="month",
    y="net_amount",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# ---------------------------------------------------------
# CATEGORY AND REGION
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("💰 Revenue by Category")

    category_revenue = (
        filtered_df
        .groupby(
            "product_category",
            as_index=False
        )["net_amount"]
        .sum()
        .sort_values(
            "net_amount",
            ascending=False
        )
    )

    fig_category = px.bar(
        category_revenue,
        x="product_category",
        y="net_amount",
        title="Revenue by Product Category"
    )

    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col2:

    st.subheader("🌍 Revenue by Region")

    region_revenue = (
        filtered_df
        .groupby(
            "region",
            as_index=False
        )["net_amount"]
        .sum()
        .sort_values(
            "net_amount",
            ascending=False
        )
    )

    fig_region = px.bar(
        region_revenue,
        x="region",
        y="net_amount",
        title="Revenue by Region"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

# ---------------------------------------------------------
# ORDER STATUS AND PAYMENT
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("📦 Order Status")

    status_counts = (
        filtered_df
        .groupby("order_status")
        .size()
        .reset_index(name="orders")
    )

    fig_status = px.pie(
        status_counts,
        names="order_status",
        values="orders",
        hole=0.4,
        title="Order Status Distribution"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

with col2:

    st.subheader("💳 Payment Methods")

    payment_counts = (
        filtered_df
        .groupby("payment_method")
        .size()
        .reset_index(name="orders")
        .sort_values(
            "orders",
            ascending=False
        )
    )

    fig_payment = px.bar(
        payment_counts,
        x="payment_method",
        y="orders",
        title="Orders by Payment Method"
    )

    fig_payment.update_layout(
        xaxis_title="Payment Method",
        yaxis_title="Orders"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

# ---------------------------------------------------------
# TOP PRODUCTS
# ---------------------------------------------------------

st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    filtered_df
    .groupby(
        "product_name",
        as_index=False
    )["net_amount"]
    .sum()
    .sort_values(
        "net_amount",
        ascending=False
    )
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="net_amount",
    y="product_name",
    orientation="h",
    title="Top 10 Products"
)

fig_products.update_layout(
    xaxis_title="Revenue",
    yaxis_title="Product",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------

st.subheader("📋 Cleaned Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------

st.download_button(
    "⬇️ Download Filtered CSV",
    filtered_df.to_csv(index=False),
    "filtered_ecommerce_sales.csv",
    "text/csv"
)

st.divider()

st.caption(
    "E-Commerce Sales Analytics | Data Cleaning + Visualization Pipeline"
)
