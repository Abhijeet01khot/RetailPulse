import os

# Windows Hadoop configuration
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"

from pyspark.sql import SparkSession


# Create Spark session
spark = (
    SparkSession.builder
    .appName("RetailPulse-Bronze")
    .master("local[*]")
    .getOrCreate()
)

# Keep Spark logs quieter
spark.sparkContext.setLogLevel("WARN")


# File locations
input_path = "data/raw/orders.csv"
output_path = "data/bronze/orders"


# --------------------------------------------------
# 1. Read raw data
# --------------------------------------------------

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_path)
)


# --------------------------------------------------
# 2. Display Bronze information
# --------------------------------------------------

print("\n=== RetailPulse Bronze Layer ===")

print(f"Record count: {df.count()}")

print("\nSchema:")
df.printSchema()

print("\nSample records:")
df.show(10, truncate=False)


# --------------------------------------------------
# 3. Write Bronze data
# --------------------------------------------------

df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(output_path)


print(f"\nBronze data written to: {output_path}")


# --------------------------------------------------
# 4. Stop Spark
# --------------------------------------------------

spark.stop()

print("\n=== Bronze Layer Completed Successfully ===")