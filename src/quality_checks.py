import os

os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count


spark = (
    SparkSession.builder
    .appName("RetailPulse-QualityChecks")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

input_path = "data/silver/orders"

df = spark.read.option("header", True).csv(input_path)

# Convert types
df = df.withColumn("quantity", col("quantity").cast("integer"))
df = df.withColumn("unit_price", col("unit_price").cast("double"))


print("\n=== RetailPulse Data Quality Checks ===")

# 1. Row count
row_count = df.count()

print(f"\nTotal records: {row_count}")

# 2. Duplicate order IDs
duplicate_count = (
    df.groupBy("order_id")
    .count()
    .filter(col("count") > 1)
    .count()
)

print(f"Duplicate order IDs: {duplicate_count}")

# 3. Missing required fields
null_count = df.filter(
    col("order_id").isNull()
    | col("customer_id").isNull()
    | col("product_id").isNull()
    | col("quantity").isNull()
    | col("unit_price").isNull()
    | col("order_date").isNull()
).count()

print(f"Records with missing required fields: {null_count}")

# 4. Invalid quantities
invalid_quantity_count = df.filter(
    col("quantity") <= 0
).count()

print(f"Records with invalid quantity: {invalid_quantity_count}")

# 5. Invalid prices
invalid_price_count = df.filter(
    col("unit_price") <= 0
).count()

print(f"Records with invalid price: {invalid_price_count}")


# Overall result
checks_passed = (
    duplicate_count == 0
    and null_count == 0
    and invalid_quantity_count == 0
    and invalid_price_count == 0
)

print("\n=== QUALITY RESULT ===")

if checks_passed:
    print("PASS - All data quality checks passed.")
else:
    print("FAIL - One or more data quality checks failed.")


spark.stop()    