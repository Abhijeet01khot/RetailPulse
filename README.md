# RetailPulse - End-to-End Data Engineering Pipeline

## Overview

RetailPulse is an end-to-end data engineering project that simulates an e-commerce order data pipeline.

The project demonstrates data ingestion, transformation, data quality validation, and analytical data modeling using Python, PySpark, and SQL.

## Architecture

Raw CSV
   |
   v
Bronze Layer
   |
   v
Silver Layer
   |
   v
Gold Layer
   |
   v
SQL Analytics

## Technologies

- Python
- PySpark
- Pandas
- SQL
- Git
- GitHub

## Pipeline

### 1. Data Generation

`generate_data.py` creates 500 simulated e-commerce orders.

The dataset includes:

- Order information
- Customer information
- Product information
- Quantity
- Unit price
- Order date

Some intentionally invalid records are included to demonstrate data-quality processing.

### 2. Bronze Layer

The Bronze layer ingests the raw CSV data using PySpark.

Responsibilities:

- Read raw data
- Infer schema
- Preserve source data
- Store staged data

### 3. Silver Layer

The Silver layer cleans and validates the Bronze data.

Transformations include:

- Duplicate removal
- Null handling
- Data type conversion
- Date standardization
- Quantity validation
- Price validation

### 4. Gold Layer

The Gold layer creates business-ready sales information.

Metrics include:

- Total quantity sold
- Total revenue
- Revenue by product
- Revenue by category

### 5. Data Quality

Automated checks validate:

- Duplicate order IDs
- Required fields
- Positive quantities
- Positive prices

## Project Structure

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
├── requirements.txt
└── README.md
