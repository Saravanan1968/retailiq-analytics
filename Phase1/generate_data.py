from dotenv import load_dotenv
import os
import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

fake = Faker('en_IN')  # Indian locale for realistic data
load_dotenv()

# ---- Connect to MySQL ----
conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)
cursor = conn.cursor()

print("Connected to MySQL!")

# ---- 1. Insert Customers (500 records) ----
cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]
if customer_count == 0:
    print("Inserting customers...")
    customers = []
    for _ in range(500):
        customers.append((
            fake.first_name(),
            fake.last_name(),
            fake.unique.email(),
            fake.phone_number()[:15],
            fake.city(),
            fake.state(),
            'India'
        ))

    cursor.executemany("""
        INSERT INTO customers (first_name, last_name, email, phone, city, state, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, customers)
    conn.commit()
    print(f"✅ Inserted {len(customers)} customers")
else:
    print(f"✅ Using existing {customer_count} customers")


# ---- 2. Insert Products (100 records) ----
categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys', 'Grocery']
brands = ['Samsung', 'Apple', 'Nike', 'Puma', 'Prestige', 'Penguin', 'Dove', 'Lego', 'Amul', 'Boat']

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]
if product_count == 0:
    print("Inserting products...")
    products = []
    for _ in range(100):
        price = round(random.uniform(99, 49999), 2)
        cost = round(price * random.uniform(0.4, 0.7), 2)
        products.append((
            fake.catch_phrase(),
            random.choice(categories),
            random.choice(brands),
            price,
            cost
        ))

    cursor.executemany("""
        INSERT INTO products (product_name, category, brand, price, cost_price)
        VALUES (%s, %s, %s, %s, %s)
    """, products)
    conn.commit()
    print(f"✅ Inserted {len(products)} products")
else:
    print(f"✅ Using existing {product_count} products")


# ---- 3. Insert Inventory ----
print("Inserting inventory...")
cursor.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("""
    SELECT p.product_id
    FROM products p
    LEFT JOIN inventory i ON i.product_id = p.product_id
    WHERE i.product_id IS NULL
""")
missing_product_ids = [row[0] for row in cursor.fetchall()]
inventory = [(pid, random.randint(0, 500)) for pid in missing_product_ids]
cursor.executemany("""
    INSERT INTO inventory (product_id, quantity_in_stock)
    VALUES (%s, %s)
""", inventory)
conn.commit()
print(f"✅ Inserted inventory for {len(inventory)} products")


# ---- 4. Insert Orders + Order Items + Payments ----
print("Inserting orders, items, payments...")
cursor.execute("SELECT customer_id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]

statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
payment_methods = ['credit_card', 'debit_card', 'upi', 'net_banking', 'cod']
payment_statuses = ['completed', 'completed', 'completed', 'failed', 'pending']  # weighted

order_count = 0
for _ in range(2000):  # 2000 orders
    customer_id = random.choice(customer_ids)
    days_ago = random.randint(0, 730)  # last 2 years
    order_date = datetime.now() - timedelta(days=days_ago)
    status = random.choice(statuses)

    # Pick 1-5 products per order
    num_items = random.randint(1, 5)
    selected_products = random.sample(product_ids, num_items)

    total = 0
    items = []
    for pid in selected_products:
        cursor.execute("SELECT price FROM products WHERE product_id = %s", (pid,))
        price = cursor.fetchone()[0]
        qty = random.randint(1, 4)
        discount = Decimal(str(round(random.uniform(0, 20), 2)))
        line_total = (price * qty * (Decimal("1") - discount / Decimal("100"))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        total += line_total
        items.append((pid, qty, price, discount))

    total = round(total, 2)

    # Insert order
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_city)
        VALUES (%s, %s, %s, %s, %s)
    """, (customer_id, order_date, status, total, fake.city()))
    order_id = cursor.lastrowid

    # Insert order items
    for pid, qty, price, discount in items:
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, pid, qty, price, discount))

    # Insert payment
    pay_status = 'completed' if status == 'delivered' else random.choice(payment_statuses)
    cursor.execute("""
        INSERT INTO payments (order_id, payment_date, amount, payment_method, payment_status)
        VALUES (%s, %s, %s, %s, %s)
    """, (order_id, order_date, total, random.choice(payment_methods), pay_status))

    order_count += 1

conn.commit()
print(f"✅ Inserted {order_count} orders with items and payments")

cursor.close()
conn.close()
print("\n🎉 All data generated successfully!")