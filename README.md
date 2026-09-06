🛒 **RetailIQ — End-to-End E-Commerce Analytics Pipeline**

📌 Project Overview
RetailIQ is a complete end-to-end data engineering and analytics project that simulates a real-world e-commerce analytics pipeline. 
It covers the full data lifecycle — from transactional database design to cloud data warehousing and business intelligence dashboards.

🏗️ Architecture

MySQL (OLTP)          GCP BigQuery (OLAP)        Looker Studio
─────────────         ──────────────────         ─────────────
customers      →                           →
products       →    Python ETL Pipeline    →    Interactive
orders         →    (pandas, SQLAlchemy)   →    Dashboard
order_items    →                           →    (3 Pages)
payments       →    Star Schema Design     →
inventory      →    (fact + dim tables)    →


🛠️ Tech Stack
Layer	Technology
Transactional DB (OLTP)	MySQL 8.0
Cloud Data Warehouse (OLAP)	GCP BigQuery
ETL Pipeline	Python (pandas, mysql-connector, google-cloud-bigquery)
Data Generation	Python Faker library
Visualization	Looker Studio (Data Studio)
Version Control	Git / GitHub


📁 Project Structure

retailiq-analytics/
│
├── phase1-mysql/
│   ├── Schema.sql              ← Database schema (6 tables)
│   ├── Indexes.sql             ← Performance indexes
│   ├── generate_data.py        ← Mock data generator (2000+ orders)
│   └── Queries_practices/      ← SQL practice queries
│       ├── beginner.sql
│       ├── intermediate.sql
│       └── advanced.sql
│
├── phase2-bigquery/
│   ├── export_mysql_to_csv.py  ← Export MySQL → CSV
│   └── load_to_bigquery.py     ← Load CSV → BigQuery (Star Schema)
│
├── phase3-dashboard/
│   └── screenshots/
│       ├── dashboard_overview.png
│       ├── dashboard_products.png
│       └── dashboard_customers.png
│
├── .env.example                ← Environment variables template
├── .gitignore
└── README.md
🗃️ Phase 1 — MySQL Database Design
Schema (OLTP)
Designed a normalized relational schema with 6 tables:

Table	Description
customers	Customer profiles (500 records)
products	Product catalog (100 records)
inventory	Stock levels per product
orders	Order headers (2000+ records)
order_items	Line items per order (~6000 records)
payments	Payment transactions

Key SQL Skills Practiced:
Table design with primary & foreign keys
Performance indexing
Complex JOINs across multiple tables
Aggregate functions (SUM, COUNT, AVG)
Window functions (RANK, SUM OVER)
CTEs (Common Table Expressions)
Stored procedures

☁️ Phase 2 — GCP BigQuery (Data Warehouse)
Star Schema Design (OLAP)
Redesigned MySQL OLTP schema into a Star Schema for analytical workloads:

Table	Type	Description
fact_orders	Fact	Order line items with revenue
fact_payments	Fact	Payment transactions
dim_customers	Dimension	Customer attributes
dim_products	Dimension	Product attributes
dim_dates	Dimension	Date dimension (2024-2026)

ETL Pipeline:
Export MySQL tables → CSV files
Transform data (joins, calculated fields)
Load to BigQuery with defined schemas

BigQuery Analytics Queries:
Monthly revenue trends
Customer Lifetime Value (CLV)
Product profit margin analysis
Revenue by category
Customer cohort analysis
Running total revenue (Window Functions)

📊 Phase 3 — Looker Studio Dashboard

3-Page Interactive Dashboard:
Page 1 — Executive Overview

Total Revenue KPI
Total Orders KPI
Total Customers KPI
Average Order Value KPI
Monthly Revenue Trend (Line Chart)
Revenue by Payment Method (Pie Chart)
Order Status Distribution (Bar Chart)

Page 2 — Product Analytics
Revenue by Category (Pie Chart)
Top Products by Revenue (Bar Chart)
Units Sold by Category (Bar Chart)
Category Filter (Dropdown)

Page 3 — Customer Insights
Customers by State (Bar Chart)
Top Customers by Lifetime Value (Table)
Revenue by State (Bar Chart)
