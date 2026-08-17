import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

products = [
    ("P001", "Laptop", "Electronics", 65000),
    ("P002", "Smartphone", "Electronics", 30000),
    ("P003", "Headphones", "Electronics", 3000),
    ("P004", "Office Chair", "Furniture", 8500),
    ("P005", "Desk", "Furniture", 12000),
    ("P006", "Keyboard", "Electronics", 2500),
    ("P007", "Backpack", "Accessories", 1800),
    ("P008", "Monitor", "Electronics", 15000),
]

customers = [
    ("C001", "Abhishek", "Pune"),
    ("C002", "Rahul", "Mumbai"),
    ("C003", "Sneha", "Bengaluru"),
    ("C004", "Priya", "Delhi"),
    ("C005", "Amit", "Hyderabad"),
    ("C006", "Neha", "Pune"),
    ("C007", "Rohan", "Mumbai"),
    ("C008", "Anjali", "Bengaluru"),
]

rows = []

start_date = datetime(2026, 1, 1)

for i in range(1, 501):
    product = random.choice(products)
    customer = random.choice(customers)

    order_date = start_date + timedelta(
        days=random.randint(0, 180)
    )

    quantity = random.randint(1, 5)

    rows.append({
        "order_id": f"O{i:04d}",
        "customer_id": customer[0],
        "customer_name": customer[1],
        "city": customer[2],
        "product_id": product[0],
        "product_name": product[1],
        "category": product[2],
        "quantity": quantity,
        "unit_price": product[3],
        "order_date": order_date.strftime("%Y-%m-%d")
    })

df = pd.DataFrame(rows)

# Intentionally introduce a few bad records
df.loc[10, "customer_name"] = None
df.loc[25, "city"] = None
df.loc[40, "quantity"] = -2

output_path = Path("data/raw/orders.csv")

df.to_csv(output_path, index=False)

print(f"Generated {len(df)} orders")
print(f"Saved to {output_path}")