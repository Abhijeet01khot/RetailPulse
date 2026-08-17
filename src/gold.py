import os

# Windows Hadoop configuration
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, round


# --------------------------------------------------
# Create Spark session
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("RetailPulse-Gold")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# --------------------------------------------------
# File locations
# --------------------------------------------------

input_path = "data/silver/orders"
output_path = "data/gold/sales"


# --------------------------------------------------
# Read Silver data
# --------------------------------------------------

df = spark.read.option("header", True).csv(input_path)

print("\n=== RetailPulse Gold Layer ===")

print(f"Silver records read: {df.count()}")


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
# Calculate order revenue
# --------------------------------------------------

df = df.withColumn(
    "revenue",
    col("quantity") * col("unit_price")
)


# --------------------------------------------------
# Create business-level sales summary
# --------------------------------------------------

gold_df = (
    df.groupBy(
        "product_id",
        "product_name",
        "category"
    )
    .agg(
        sum("quantity").alias("total_quantity"),
        round(sum("revenue"), 2).alias("total_revenue")
    )
    .orderBy(
        col("total_revenue").desc()
    )
)


# --------------------------------------------------
# Display Gold results
# --------------------------------------------------

print("\n=== Sales Summary ===")

gold_df.show(20, truncate=False)


# --------------------------------------------------
# Write Gold dataset
# --------------------------------------------------

gold_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(output_path)


print(f"\nGold data written to: {output_path}")

print("\n=== Gold Layer Completed Successfully ===")


# --------------------------------------------------
# Stop Spark
# --------------------------------------------------

spark.stop()