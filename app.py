import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="EduPro Online Platform",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 EduPro Online Platform")
st.markdown("### Course Analytics & Executive Dashboard")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

FILE_NAME = "EduPro Online Platform.xlsx"

if not os.path.exists(FILE_NAME):
    st.error(
        f"Could not find the Excel file: {FILE_NAME}. "
        "Make sure it is in the same folder as app.py."
    )
    st.stop()

try:
    excel_file = pd.ExcelFile(FILE_NAME)
    sheet_names = excel_file.sheet_names

    # Use the first sheet by default
    df = pd.read_excel(FILE_NAME, sheet_name=sheet_names[0])

except Exception as e:
    st.error(f"Error reading Excel file: {e}")
    st.stop()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

df.columns = df.columns.str.strip()

# Convert numeric-looking columns
for col in df.columns:
    converted = pd.to_numeric(df[col], errors="coerce")

    # Only replace if a reasonable amount of the column is numeric
    if converted.notna().sum() >= len(df) * 0.5:
        df[col] = converted

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

st.sidebar.write(f"**Rows:** {len(df):,}")
st.sidebar.write(f"**Columns:** {len(df.columns):,}")

# Category filter
categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

filtered_df = df.copy()

if categorical_columns:

    selected_column = st.sidebar.selectbox(
        "Filter by",
        ["None"] + categorical_columns
    )

    if selected_column != "None":

        values = sorted(
            filtered_df[selected_column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_values = st.sidebar.multiselect(
            f"Select {selected_column}",
            values,
            default=values
        )

        if selected_values:
            filtered_df = filtered_df[
                filtered_df[selected_column].astype(str).isin(selected_values)
            ]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Key Performance Indicators")

numeric_columns = filtered_df.select_dtypes(
    include=np.number
).columns.tolist()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "Total Records",
        f"{len(filtered_df):,}"
    )

with kpi2:
    st.metric(
        "Total Columns",
        f"{len(filtered_df.columns):,}"
    )

with kpi3:
    if "Course Rating" in filtered_df.columns:
        rating = filtered_df["Course Rating"].mean()
        st.metric(
            "Average Course Rating",
            f"{rating:.2f}"
        )
    else:
        st.metric(
            "Numeric Variables",
            f"{len(numeric_columns):,}"
        )

with kpi4:
    if "Instructor Rating" in filtered_df.columns:
        instructor_rating = filtered_df["Instructor Rating"].mean()
        st.metric(
            "Avg Instructor Rating",
            f"{instructor_rating:.2f}"
        )
    else:
        st.metric(
            "Missing Values",
            f"{filtered_df.isna().sum().sum():,}"
        )

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.subheader("📋 Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.write("**Dataset Shape**")
    st.write(
        f"{filtered_df.shape[0]:,} rows × "
        f"{filtered_df.shape[1]:,} columns"
    )

with col2:
    st.write("**Missing Values**")
    missing = filtered_df.isna().sum().sum()
    st.write(f"{missing:,} missing values")

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

with st.expander("🔎 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# --------------------------------------------------
# NUMERIC ANALYSIS
# --------------------------------------------------

if numeric_columns:

    st.subheader("📈 Numeric Analysis")

    selected_numeric = st.selectbox(
        "Select a numerical variable",
        numeric_columns
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    data = filtered_df[selected_numeric].dropna()

    with metric_col1:
        st.metric(
            "Average",
            f"{data.mean():.2f}"
        )

    with metric_col2:
        st.metric(
            "Minimum",
            f"{data.min():.2f}"
        )

    with metric_col3:
        st.metric(
            "Maximum",
            f"{data.max():.2f}"
        )

    # Histogram
    fig, ax = plt.subplots()

    ax.hist(data, bins=20)
    ax.set_title(f"Distribution of {selected_numeric}")
    ax.set_xlabel(selected_numeric)
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

st.subheader("🔗 Correlation Analysis")

if len(numeric_columns) >= 2:

    correlation = filtered_df[numeric_columns].corr()

    st.dataframe(
        correlation.round(2),
        use_container_width=True
    )

    # Course rating vs instructor rating
    if (
        "Course Rating" in filtered_df.columns
        and "Instructor Rating" in filtered_df.columns
    ):

        corr_value = filtered_df[
            ["Course Rating", "Instructor Rating"]
        ].corr().iloc[0, 1]

        st.info(
            f"Correlation between Course Rating and "
            f"Instructor Rating: **{corr_value:.2f}**"
        )

        if abs(corr_value) < 0.1:
            st.write(
                "Interpretation: There is essentially no linear "
                "relationship between instructor rating and course rating."
            )

# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

if categorical_columns:

    st.subheader("📊 Category Analysis")

    selected_category = st.selectbox(
        "Select a categorical variable",
        categorical_columns,
        key="category_analysis"
    )

    category_counts = (
        filtered_df[selected_category]
        .value_counts()
        .head(15)
    )

    fig, ax = plt.subplots()

    category_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        f"Top Categories - {selected_category}"
    )

    ax.set_xlabel(selected_category)
    ax.set_ylabel("Count")

    plt.xticks(rotation=45, ha="right")

    st.pyplot(fig)

# --------------------------------------------------
# COURSE RATING ANALYSIS
# --------------------------------------------------

if "Course Rating" in filtered_df.columns:

    st.subheader("⭐ Course Rating Analysis")

    rating_data = filtered_df["Course Rating"].dropna()

    fig, ax = plt.subplots()

    ax.hist(
        rating_data,
        bins=10
    )

    ax.set_title("Course Rating Distribution")
    ax.set_xlabel("Course Rating")
    ax.set_ylabel("Number of Courses")

    st.pyplot(fig)

# --------------------------------------------------
# INSTRUCTOR RATING ANALYSIS
# --------------------------------------------------

if "Instructor Rating" in filtered_df.columns:

    st.subheader("👨‍🏫 Instructor Rating Analysis")

    instructor_data = filtered_df[
        "Instructor Rating"
    ].dropna()

    fig, ax = plt.subplots()

    ax.hist(
        instructor_data,
        bins=10
    )

    ax.set_title("Instructor Rating Distribution")
    ax.set_xlabel("Instructor Rating")
    ax.set_ylabel("Number of Courses")

    st.pyplot(fig)

# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------

st.subheader("💡 Executive Insights")

insights = []

insights.append(
    f"The dataset contains **{len(filtered_df):,} records** "
    f"across **{len(filtered_df.columns):,} variables**."
)

if "Course Rating" in filtered_df.columns:
    insights.append(
        f"The average course rating is "
        f"**{filtered_df['Course Rating'].mean():.2f}**."
    )

if "Instructor Rating" in filtered_df.columns:
    insights.append(
        f"The average instructor rating is "
        f"**{filtered_df['Instructor Rating'].mean():.2f}**."
    )

if (
    "Course Rating" in filtered_df.columns
    and "Instructor Rating" in filtered_df.columns
):

    corr = filtered_df[
        ["Course Rating", "Instructor Rating"]
    ].corr().iloc[0, 1]

    if abs(corr) < 0.1:
        insights.append(
            "Instructor rating and course rating show "
            "essentially no linear correlation."
        )
    elif corr > 0:
        insights.append(
            "Instructor rating and course rating show "
            "a positive relationship."
        )
    else:
        insights.append(
            "Instructor rating and course rating show "
            "a negative relationship."
        )

for insight in insights:
    st.markdown(f"- {insight}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "EduPro Online Platform | Data Analytics Dashboard"
)