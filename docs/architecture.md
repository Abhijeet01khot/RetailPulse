# RetailPulse Architecture


## Overview


RetailPulse is an end-to-end data engineering project that processes synthetic retail order data through a layered Bronze → Silver → Gold architecture.


The current implementation runs locally using Python and PySpark.


The architecture is designed so that the same processing pattern can later be extended to cloud technologies such as Azure Data Factory, Azure Data Lake Storage Gen2, Azure Databricks, Delta Lake, and Snowflake.


---


# 1. Current Local Architecture


```text
                    Synthetic Retail Data
                             |
                             v
                    generate_data.py
                             |
                             v
                    data/raw/orders.csv
                             |
                             v
                       BRONZE LAYER
                          PySpark
                             |
                             v
                       SILVER LAYER
                  Cleaning + Validation
                             |
                             v
                        GOLD LAYER
                  Business Aggregations
                             |
                             v
                       SQL Analytics
```
---

# 2. Data Generation

The project generates synthetic retail order data using Python.

The generated dataset contains 500 orders.

Each order includes:

Order ID
Customer ID
Customer name
City
Product ID
Product name
Category
Quantity
Unit price
Order date

The generated dataset intentionally contains a small number of data-quality issues so that the pipeline can demonstrate cleaning and validation.

Input Generation Script
src/generate_data.py
Generated Dataset
data/raw/orders.csv

---

# 3. Bronze Layer

The Bronze layer is responsible for ingesting the raw dataset using PySpark.

Responsibilities
Read raw CSV data
Infer the initial schema
Preserve the ingested records
Store staged data for downstream processing
Processing
Raw CSV
   |
   v
PySpark
   |
   v
Bronze Dataset
Input
data/raw/orders.csv
Implementation
src/bronze.py
Output
data/bronze/orders

The Bronze layer is intended to keep the data close to its original form before major business transformations are applied.

---

# 4. Silver Layer

The Silver layer performs data cleansing, standardization, and validation.

Responsibilities
Remove duplicate orders
Handle missing required fields
Trim string values
Convert numeric fields to appropriate types
Convert order dates to date types
Remove invalid quantities
Remove invalid prices
Transformations
Bronze Data
     |
     +--> Remove duplicates
     |
     +--> Validate required fields
     |
     +--> Standardize strings
     |
     +--> Convert data types
     |
     +--> Validate quantities
     |
     +--> Validate prices
     |
     v
Clean Silver Data
Implementation
src/silver.py
Input
data/bronze/orders
Output
data/silver/orders
Pipeline Result
500 raw records
       |
       v
Silver cleaning and validation
       |
       v
499 valid records

---

# 5. Data Quality Checks

RetailPulse includes automated data-quality validation using PySpark.

Implementation
src/quality_checks.py

The following checks are performed:

Duplicate Order IDs

Ensures each order has a unique order ID.

Missing Required Fields

Checks required fields including:

order_id
customer_id
product_id
quantity
unit_price
order_date
Invalid Quantity

Ensures quantity is greater than zero.

Invalid Price

Ensures unit price is greater than zero.

Example Result
=== RetailPulse Data Quality Checks ===


Total records: 499
Duplicate order IDs: 0
Records with missing required fields: 0
Records with invalid quantity: 0
Records with invalid price: 0


=== QUALITY RESULT ===
PASS - All data quality checks passed.

This quality-check stage acts as a validation gate before downstream analytics.

---

# 6. Gold Layer

The Gold layer creates business-ready analytical data.

The main business metric calculated by the pipeline is revenue.

Revenue = Quantity × Unit Price
Gold Aggregations

The Gold dataset aggregates data by:

Product
Product category
Metrics
product_id
product_name
category
total_quantity
total_revenue
Processing
Silver Data
     |
     v
Calculate Revenue
     |
     v
Group by Product
     |
     v
Group by Category
     |
     v
Business-ready Gold Dataset
Implementation
src/gold.py
Input
data/silver/orders
Output
data/gold/sales


---

# 7. SQL Analytics

SQL analytics are stored in:

sql/analytics.sql

The SQL layer demonstrates how downstream users can analyze the cleaned data.

Example analytical questions include:

What is the total revenue?
Which products generate the most revenue?
Which categories sell the most units?
Which cities generate the most revenue?
Which customers have the highest spending?

Example:

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

---

# 8. Current Project Architecture

```txt
                         RETAILPULSE
                              |
                              v
                     Synthetic Data
                              |
                              v
                    +----------------+
                    |     Python     |
                    | Data Generator |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |      RAW       |
                    |   orders.csv   |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |     BRONZE     |
                    |    PySpark     |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |     SILVER     |
                    | Clean + Valid  |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    |      GOLD      |
                    |  Aggregations  |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | SQL Analytics  |
                    +----------------+
```

---

# 9. Cloud Target Architecture

The local pipeline can be extended into a cloud-based architecture using Azure, Databricks, Delta Lake, and Snowflake.
```txt
                         Retail Data
                              |
                              v
                     Azure Data Factory
                              |
                              v
                  Azure Data Lake Storage
                         ADLS Gen2
                              |
                              v
                     Azure Databricks
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           BRONZE          SILVER           GOLD
          Raw Data        Clean Data     Business Data
              |               |               |
              +---------------+---------------+
                              |
                              v
                         Delta Lake
                              |
                              v
                           Snowflake
                              |
                              v
                      Analytics / BI
```
This represents a potential production architecture rather than the current local implementation.

---

# 10. Cloud Technology Mapping
Current Project	Potential Production Technology
Python	Python
PySpark	Azure Databricks
Local raw files	Azure Data Lake Storage Gen2
Bronze directory	Delta Lake Bronze
Silver directory	Delta Lake Silver
Gold directory	Delta Lake Gold
SQL analytics	Snowflake SQL
Local scripts	Databricks Jobs
Git	GitHub / Azure DevOps

---

# 11. Azure Data Factory

In a production implementation, Azure Data Factory could be used to orchestrate ingestion and pipeline execution.

A possible flow would be:

Source
  |
  v
Azure Data Factory
  |
  v
ADLS Gen2
  |
  v
Databricks Job
  |
  v
Bronze → Silver → Gold

Potential responsibilities include:

Pipeline orchestration
Scheduled ingestion
Dependency management
Pipeline monitoring
Trigger management
Failure handling

---

# 12. Azure Data Lake Storage Gen2

ADLS Gen2 could provide cloud storage for the different data layers.

Example structure:

retailpulse/
│
├── raw/
│
├── bronze/
│
├── silver/
│
└── gold/

The separation of layers makes it easier to manage data throughout its lifecycle.

---

# 13. Azure Databricks

Azure Databricks could execute the PySpark transformations in a production environment.

Potential Databricks workflow:

Raw Data
   |
   v
Databricks Notebook / Job
   |
   +------> Bronze
   |
   +------> Silver
   |
   +------> Gold

Databricks Jobs could be scheduled and monitored as part of an automated data pipeline.

---

# 14. Delta Lake

Delta Lake could be used to store Bronze, Silver, and Gold datasets as transactional tables.

Potential structure:

Bronze Delta Table
        |
        v
Silver Delta Table
        |
        v
Gold Delta Table

Potential benefits include:

ACID transactions
Schema enforcement
Schema evolution
Version history
Reliable data pipelines
Efficient analytical processing


---

# 15. Snowflake

Snowflake could be used as a downstream analytical warehouse.

A potential flow would be:

Azure Data Lake
       |
       v
Azure Databricks
       |
       v
Gold Data
       |
       v
Snowflake
       |
       v
SQL Analytics

Snowflake could provide a centralized environment for analytical workloads and reporting.

---

# 16. CI/CD

A production implementation could use GitHub or Azure DevOps to automate testing and deployment.

Example:

Developer
    |
    v
Git Commit
    |
    v
GitHub
    |
    v
CI Pipeline
    |
    +----> Unit Tests
    |
    +----> Data Quality Tests
    |
    +----> Code Validation
    |
    v
Deployment
    |
    v
Databricks / Azure Environment
---

# 17. Monitoring

A production version could include monitoring for:

Pipeline failures
Record-count anomalies
Data-quality failures
Processing duration
Job failures
Storage problems
Schema changes

Example:

Pipeline
   |
   v
Validation
   |
   +---- PASS ---> Continue
   |
   +---- FAIL ---> Alert

---

# 18. Incremental Processing

The current project processes the dataset as a batch.

A production implementation could support incremental processing.

Example:

Day 1
  |
  v
Orders 1-500
  |
  v
Processed


Day 2
  |
  v
New Orders
  |
  v
Incremental Processing
  |
  v
Silver / Gold

Possible approaches include:

Processing based on order date
Watermarking
Incremental file ingestion
Delta Lake versioning

---

# 19. Production Improvements

Potential future improvements include:

Azure Data Factory orchestration
Azure Data Lake Storage Gen2
Azure Databricks Jobs
Delta Lake tables
Snowflake integration
Incremental processing
Schema evolution
Data lineage
Pipeline monitoring
Automated alerting
Unit tests
Integration tests
CI/CD
Azure DevOps
Power BI reporting

---

# 20. Current vs Future Implementation
Current

The project currently demonstrates:

Python
PySpark
ETL processing
Bronze/Silver/Gold architecture
Data cleaning
Data validation
Data-quality checks
Business aggregations
SQL analytics
Git/GitHub
Future

The architecture can be extended to include:

Azure Data Factory
ADLS Gen2
Azure Databricks
Delta Lake
Snowflake
Azure DevOps
CI/CD
Monitoring

The cloud technologies listed above are planned extensions and are not claimed as part of the current local implementation.

---

# 21. Project Goal

The goal of RetailPulse is to demonstrate practical data engineering concepts through a complete pipeline rather than isolated scripts.

The project focuses on:

Ingestion
   ↓
Transformation
   ↓
Data Quality
   ↓
Business Modeling
   ↓
Analytics

The architecture provides a foundation that can be migrated from a local PySpark environment to a cloud-based data platform.