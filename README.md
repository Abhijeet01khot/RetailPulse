# RetailPulse — End-to-End Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PySpark](https://img.shields.io/badge/PySpark-3.5.7-orange)
![SQL](https://img.shields.io/badge/SQL-Analytics-lightgrey)
![Pipeline](https://img.shields.io/badge/Pipeline-Bronze%20%7C%20Silver%20%7C%20Gold-green)

RetailPulse is an end-to-end data engineering portfolio project that demonstrates how raw retail order data can be transformed into clean, validated, and analytics-ready datasets.

The project uses **Python, PySpark, and SQL** to implement a layered data pipeline with automated data-quality checks.

---

## Project Overview

RetailPulse simulates a retail/e-commerce data platform.

The pipeline starts with raw order data and processes it through three data layers:

```text
                    RetailPulse Data Pipeline

 Raw Orders
    │
    │ Python
    ▼
┌──────────────┐
│    BRONZE    │
│ Raw/Staged   │
│     Data     │
└──────┬───────┘
       │
       │ PySpark
       ▼
┌──────────────┐
│    SILVER    │
│ Cleaned &    │
│  Validated   │
│     Data     │
└──────┬───────┘
       │
       │ PySpark
       ▼
┌──────────────┐
│     GOLD     │
│ Business &   │
│   Analytics  │
└──────┬───────┘
       │
       ▼
   SQL Analytics
```

The architecture follows the common **Bronze → Silver → Gold** data-lake pattern.

---

# Key Features

- Synthetic retail order data generation
- PySpark-based data ingestion
- Bronze data layer
- Silver data cleansing and validation
- Gold business-level aggregations
- Automated data-quality checks
- SQL analytics queries
- Git/GitHub version control
- Reproducible local development environment

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and project scripting |
| PySpark | Distributed-style data processing and transformations |
| Pandas | Synthetic data generation |
| SQL | Analytical queries |
| Git | Version control |
| GitHub | Source code and project collaboration |

---

# Dataset

The project generates **500 synthetic retail orders**.

Each order contains:

- Order ID
- Customer ID
- Customer name
- City
- Product ID
- Product name
- Product category
- Quantity
- Unit price
- Order date

Example:

| order_id | customer_id | product_name | category | quantity | unit_price | order_date |
|---|---|---|---|---:|---:|---|
| O0001 | C001 | Smartphone | Electronics | 2 | 30000 | 2026-03-12 |
| O0002 | C003 | Office Chair | Furniture | 5 | 8500 | 2026-01-27 |
| O0003 | C007 | Smartphone | Electronics | 1 | 30000 | 2026-01-09 |

The generated dataset intentionally contains a small number of invalid records so that the data-quality and Silver-layer transformations can be demonstrated.

---

# Pipeline Architecture

## 1. Raw Layer

The `generate_data.py` script creates the initial retail order dataset.

```text
src/generate_data.py
        │
        ▼
data/raw/orders.csv
```

The dataset contains 500 records.

Some records intentionally contain data-quality issues such as:

- Missing customer information
- Missing city information
- Invalid negative quantity

This allows the pipeline to demonstrate real-world data cleansing.

---

# 2. Bronze Layer

The Bronze layer ingests the raw CSV using PySpark.

### Responsibilities

- Read raw CSV data
- Infer the initial schema
- Preserve the ingested records
- Store the staged dataset

Implementation:

```text
src/bronze.py
```

Input:

```text
data/raw/orders.csv
```

Output:

```text
data/bronze/orders
```

The Bronze layer represents the initial staged version of the dataset before business cleaning.

---

# 3. Silver Layer

The Silver layer performs data cleaning and validation using PySpark.

Implementation:

```text
src/silver.py
```

### Transformations

The pipeline performs:

- Duplicate order removal
- Required-field validation
- String trimming
- Numeric type conversion
- Date conversion
- Positive quantity validation
- Positive price validation

The pipeline reduced the dataset from:

```text
500 records
     ↓
499 valid records
```

The cleaned dataset is written to:

```text
data/silver/orders
```

### Silver Data Model

```text
order_id
customer_id
customer_name
city
product_id
product_name
category
quantity
unit_price
order_date
```

---

# 4. Gold Layer

The Gold layer creates business-ready analytical data.

Implementation:

```text
src/gold.py
```

The pipeline calculates:

```text
Revenue = Quantity × Unit Price
```

The Gold layer aggregates sales by:

- Product
- Product category

### Example Gold Metrics

```text
total_quantity
total_revenue
```

Output:

```text
data/gold/sales
```

This layer is designed to provide datasets that can be consumed by analysts, dashboards, or downstream applications.

---

# 5. Data Quality

Data quality checks are implemented in:

```text
src/quality_checks.py
```

The pipeline validates:

### Duplicate order IDs

```text
Duplicate order IDs: 0
```

### Missing required fields

```text
Records with missing required fields: 0
```

### Invalid quantities

```text
Records with invalid quantity: 0
```

### Invalid prices

```text
Records with invalid price: 0
```

### Final result

```text
PASS - All data quality checks passed.
```

This provides a basic automated quality gate before downstream analytical processing.

---

# SQL Analytics

SQL analytics are stored in:

```text
sql/analytics.sql
```

The queries demonstrate common business analytics such as:

### Total revenue

```sql
SELECT
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders;
```

### Revenue by product

```sql
SELECT
    product_name,
    category,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY
    product_name,
    category
ORDER BY total_revenue DESC;
```

### Revenue by category

```sql
SELECT
    category,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY category
ORDER BY total_revenue DESC;
```

### Revenue by city

```sql
SELECT
    city,
    SUM(quantity * unit_price) AS total_revenue
FROM silver_orders
GROUP BY city
ORDER BY total_revenue DESC;
```

---

# Project Structure

```text
RetailPulse/
│
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── generate_data.py
│   ├── bronze.py
│   ├── silver.py
│   ├── gold.py
│   └── quality_checks.py
│
├── sql/
│   └── analytics.sql
│
├── notebooks/
│
├── docs/
│
├── .gitignore
├── README.md
└── requirements.txt
```

Generated datasets and local environments are excluded from Git using `.gitignore`.

---

# How to Run

## 1. Clone the repository

```bash
git clone https://github.com/Abhijeet01khot/RetailPulse.git
cd RetailPulse
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell execution policy prevents activation, the project can also be run directly using:

```powershell
.venv\Scripts\python.exe
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Required packages include:

```text
pandas
pyspark
```

---

## 4. Generate the raw dataset

```bash
python src/generate_data.py
```

Expected output:

```text
Generated 500 orders
Saved to data/raw/orders.csv
```

---

## 5. Run the Bronze layer

```bash
python src/bronze.py
```

The Bronze layer reads:

```text
data/raw/orders.csv
```

and produces:

```text
data/bronze/orders
```

---

## 6. Run the Silver layer

```bash
python src/silver.py
```

The Silver layer cleans and validates the Bronze data.

Expected result:

```text
Records before cleaning: 500
Records after cleaning: 499
```

---

## 7. Run the Gold layer

```bash
python src/gold.py
```

The Gold layer creates aggregated sales metrics.

---

## 8. Run data-quality checks

```bash
python src/quality_checks.py
```

Expected result:

```text
Total records: 499
Duplicate order IDs: 0
Records with missing required fields: 0
Records with invalid quantity: 0
Records with invalid price: 0

=== QUALITY RESULT ===
PASS - All data quality checks passed.
```

---

# Data Engineering Concepts Demonstrated

This project demonstrates several practical data engineering concepts:

### Data ingestion

Reading structured raw data into a processing pipeline.

### ETL / ELT

Transforming raw records into clean and analytical datasets.

### Layered architecture

Using Bronze, Silver, and Gold data layers.

### Data cleansing

Removing duplicates, handling missing data, and validating values.

### Schema management

Converting fields into appropriate data types.

### Data quality

Creating automated checks for common data issues.

### Aggregation

Creating business-level metrics from transactional data.

### SQL analytics

Writing analytical queries for downstream consumption.

### Version control

Using Git and GitHub to manage the project.

---

# Future Architecture

The current implementation is designed to run locally.

A future cloud deployment could extend the architecture to:

```text
                    Azure Cloud Architecture

                         Raw Data
                            │
                            ▼
                    Azure Data Factory
                            │
                            ▼
                    Azure Data Lake
                            │
                            ▼
                    Azure Databricks
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Bronze          Silver          Gold
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
                         Snowflake
                            │
                            ▼
                    Analytics / BI
```

Potential future technologies include:

- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- Delta Lake
- Snowflake
- Azure DevOps
- CI/CD
- Pipeline monitoring
- Incremental data processing

These are planned extensions rather than components of the current local implementation.

---

# Possible Improvements

Future versions of RetailPulse could include:

- Incremental ingestion
- Partitioned datasets
- Slowly Changing Dimensions
- Data lineage
- Pipeline orchestration
- Retry mechanisms
- Logging and monitoring
- Unit tests
- CI/CD pipelines
- Delta Lake tables
- Azure Data Factory pipelines
- Azure Databricks jobs
- Snowflake warehouse integration
- Dashboarding with Power BI

---

# Learning Outcomes

Through this project, I practiced:

- Python data engineering
- PySpark transformations
- Data-quality validation
- Layered data architecture
- SQL analytics
- ETL pipeline development
- Git/GitHub workflow
- Designing data pipelines for downstream analytics

---

# Author

**Abhijeet Khot**

GitHub:

https://github.com/Abhijeet01khot

---

## Disclaimer

This project uses synthetic retail data created specifically for demonstration and learning purposes. No real customer or business data is used.