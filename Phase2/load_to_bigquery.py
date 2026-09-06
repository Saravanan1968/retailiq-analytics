from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize BigQuery client
project_id = os.getenv('GCP_PROJECT_ID')
client = bigquery.Client(project=project_id)
dataset_id = 'retailiq_dwh'
dataset_ref = f'{project_id}.{dataset_id}'

client.create_dataset(bigquery.Dataset(dataset_ref), exists_ok=True)

print("Connected to BigQuery!")

# ─────────────────────────────────────────────
# HELPER FUNCTION to load CSV to BigQuery
# ─────────────────────────────────────────────
def load_table(csv_file, table_name, schema):
    print(f"\nLoading {table_name}...")
    df = pd.read_csv(csv_file, dtype={'phone': 'string'})

    timestamp_columns = [field.name for field in schema if field.field_type == 'TIMESTAMP']
    for column in timestamp_columns:
        df[column] = pd.to_datetime(df[column], utc=True)
    
    table_ref = f'{project_id}.{dataset_id}.{table_name}'
    
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition='WRITE_TRUNCATE'  # overwrite if exists
    )
    
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for completion
    
    table = client.get_table(table_ref)
    print(f"  ✅ {table_name} loaded — {table.num_rows} rows")


# ─────────────────────────────────────────────
# 1. dim_customers
# ─────────────────────────────────────────────
load_table('exported_data/customers.csv', 'dim_customers', [
    bigquery.SchemaField('customer_id', 'INTEGER'),
    bigquery.SchemaField('first_name', 'STRING'),
    bigquery.SchemaField('last_name', 'STRING'),
    bigquery.SchemaField('email', 'STRING'),
    bigquery.SchemaField('phone', 'STRING'),
    bigquery.SchemaField('city', 'STRING'),
    bigquery.SchemaField('state', 'STRING'),
    bigquery.SchemaField('country', 'STRING'),
    bigquery.SchemaField('created_at', 'TIMESTAMP'),
])

# ─────────────────────────────────────────────
# 2. dim_products
# ─────────────────────────────────────────────
load_table('exported_data/products.csv', 'dim_products', [
    bigquery.SchemaField('product_id', 'INTEGER'),
    bigquery.SchemaField('product_name', 'STRING'),
    bigquery.SchemaField('category', 'STRING'),
    bigquery.SchemaField('brand', 'STRING'),
    bigquery.SchemaField('price', 'FLOAT'),
    bigquery.SchemaField('cost_price', 'FLOAT'),
    bigquery.SchemaField('created_at', 'TIMESTAMP'),
])

# ─────────────────────────────────────────────
# 3. fact_orders (with order_items joined in)
# ─────────────────────────────────────────────
print("\nBuilding fact_orders (joining orders + order_items)...")
orders = pd.read_csv('exported_data/orders.csv')
order_items = pd.read_csv('exported_data/order_items.csv')
products = pd.read_csv('exported_data/products.csv')[['product_id', 'category', 'brand']]

# Join orders with order_items and product info
fact_orders = order_items.merge(orders, on='order_id')
fact_orders = fact_orders.merge(products, on='product_id')

# Calculate revenue per line item
fact_orders['revenue'] = (
    fact_orders['unit_price'] * fact_orders['quantity'] * (1 - fact_orders['discount'] / 100)
).round(2)

fact_orders['order_date'] = pd.to_datetime(fact_orders['order_date'])

# Select relevant columns
fact_orders = fact_orders[[
    'item_id', 'order_id', 'customer_id', 'product_id',
    'category', 'brand', 'order_date', 'status',
    'quantity', 'unit_price', 'discount', 'revenue', 'shipping_city'
]]

table_ref = f'{project_id}.{dataset_id}.fact_orders'
job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
job = client.load_table_from_dataframe(fact_orders, table_ref, job_config=job_config)
job.result()
table = client.get_table(table_ref)
print(f"  ✅ fact_orders loaded — {table.num_rows} rows")


# ─────────────────────────────────────────────
# 4. fact_payments
# ─────────────────────────────────────────────
load_table('exported_data/payments.csv', 'fact_payments', [
    bigquery.SchemaField('payment_id', 'INTEGER'),
    bigquery.SchemaField('order_id', 'INTEGER'),
    bigquery.SchemaField('payment_date', 'TIMESTAMP'),
    bigquery.SchemaField('amount', 'FLOAT'),
    bigquery.SchemaField('payment_method', 'STRING'),
    bigquery.SchemaField('payment_status', 'STRING'),
])

# ─────────────────────────────────────────────
# 5. dim_dates (Generate a date dimension)
# ─────────────────────────────────────────────
print("\nGenerating dim_dates...")
import numpy as np
dates = pd.date_range(start='2024-01-01', end='2026-12-31', freq='D')
dim_dates = pd.DataFrame({
    'date_id': dates.strftime('%Y%m%d').astype(int),
    'full_date': dates,
    'day': dates.day,
    'month': dates.month,
    'month_name': dates.strftime('%B'),
    'quarter': dates.quarter,
    'year': dates.year,
    'week_of_year': dates.isocalendar().week.values,
    'day_of_week': dates.day_name(),
    'is_weekend': dates.weekday >= 5
})

table_ref = f'{project_id}.{dataset_id}.dim_dates'
job_config = bigquery.LoadJobConfig(write_disposition='WRITE_TRUNCATE')
job = client.load_table_from_dataframe(dim_dates, table_ref, job_config=job_config)
job.result()
table = client.get_table(table_ref)
print(f"  ✅ dim_dates loaded — {table.num_rows} rows")

print("\n🎉 All tables loaded into BigQuery successfully!")