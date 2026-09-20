# E-Commerce Sales Analytics Dashboard

## Overview

An interactive E-Commerce Sales Analytics project developed using Python, Pandas, NumPy, Streamlit, and Plotly.

The project demonstrates a complete data analytics workflow including data cleaning, preprocessing, feature engineering, KPI generation, and interactive visualization.

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Git
- GitHub

## Dataset

The original dataset contains:

- 932 rows
- 13 columns

After data cleaning, duplicate removal, invalid-record handling, missing-value treatment, outlier handling, and feature engineering, the final dataset contains:

- 891 rows
- 16 columns

## Data Cleaning

The pipeline performs:

1. Data loading and inspection
2. Duplicate removal
3. Text standardization
4. Email validation
5. Date parsing
6. Missing-value handling
7. Invalid quantity removal
8. Outlier treatment
9. Feature engineering
10. KPI generation

## Key Results

- Total Orders: 891
- Total Revenue: ₹2,344,477.46
- Average Order Value: ₹2,631.29
- Delivered Rate: 41.9%
- Cancelled / Returned Rate: 28.5%

## Dashboard Features

The Streamlit dashboard includes:

- Monthly revenue analysis
- Revenue by product category
- Revenue by region
- Order status distribution
- Payment method analysis
- Top products by revenue
- Interactive filters
- Filtered CSV download

## Project Structure

```text
E-Commerce-Sales-Analytics/
├── raw_ecommerce_sales.csv
├── cleaned_ecommerce_sales.csv
├── data_cleaning_pipeline.py
├── dashboard.py
├── dashboard_data.json
├── requirements.txt
└── README.md
