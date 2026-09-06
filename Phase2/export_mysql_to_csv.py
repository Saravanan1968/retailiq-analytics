import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to MySQL
conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE')
)

os.makedirs('exported_data', exist_ok=True)

tables = ['customers', 'products', 'inventory', 'orders', 'order_items', 'payments']

for table in tables:
    print(f"Exporting {table}...")
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    df.to_csv(f'exported_data/{table}.csv', index=False)
    print(f"  ✅ {table}.csv saved — {len(df)} rows")

conn.close()
print("\n🎉 All tables exported to ./exported_data/")