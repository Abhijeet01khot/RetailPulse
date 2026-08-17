import os

# Windows Hadoop configuration
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, to_date


# --------------------------------------------------
# Create Spark session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("RetailPulse-Silver")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# --------------------------------------------------
# File locations
# --------------------------------------------------

input_path = "data/bronze/orders"
output_path = "data/silver/orders"


# --------------------------------------------------
# Read Bronze
# --------------------------------------------------

df = spark.read.option("header", True).csv(input_path)

print("\n=== RetailPulse Silver Layer ===")

print(f"Records before cleaning: {df.count()}")


# --------------------------------------------------
# Clean string columns
# --------------------------------------------------

df = df.withColumn(
    "customer_name",
    trim(col("customer_name"))
)

df = df.withColumn(
    "city",
    trim(col("city"))
)


# --------------------------------------------------
# Remove duplicate orders
# --------------------------------------------------

df = df.dropDuplicates(["order_id"])


# --------------------------------------------------
# Remove records with missing required fields
# --------------------------------------------------

df = df.dropna(
    subset=[
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "unit_price",
        "order_date"
    ]
)


# --------------------------------------------------
# Convert numeric columns
# --------------------------------------------------

df = df.withColumn(
    "quantity",
    col("quantity").cast("integer")
)

df = df.withColumn(
    "unit_price",
    col("unit_price").cast("double")
)


# --------------------------------------------------
# Convert date
# --------------------------------------------------

df = df.withColumn(
    "order_date",
    to_date(col("order_date"))
)


# --------------------------------------------------
# Data-quality validation
# --------------------------------------------------

df = df.filter(col("quantity") > 0)

df = df.filter(col("unit_price") > 0)

df = df.filter(col("order_date").isNotNull())


# --------------------------------------------------
# Show results
# --------------------------------------------------

print(f"Records after cleaning: {df.count()}")

print("\nSilver schema:")
df.printSchema()

print("\nCleaned sample:")
df.show(10, truncate=False)


# --------------------------------------------------
# Write Silver
# --------------------------------------------------

df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(output_path)


print(f"\nSilver data written to: {output_path}")

print("\n=== Silver Layer Completed Successfully ===")


# --------------------------------------------------
# Stop Spark
# --------------------------------------------------

spark.stop()