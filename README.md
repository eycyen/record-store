# Record Store Management System

A comprehensive end-to-end database management solution designed to handle inventory, artist relations, and real-time sales transactions for a modern record store. This project serves as the final implementation for the Ankara University - COM2058 Database Management Systems course.

## Core Features

- Dynamic Digital Storefront: Automatically fetches high-resolution album covers from the Apple iTunes Search API based on database entries.
- Real-time Stock Management: Implements CHECK constraints to ensure StockQuantity never drops below zero. Stock levels are updated instantly upon purchase.
- ACID-Compliant Transactions: A single purchase flow synchronously updates the CUSTOMER, CUSTOMER_ORDER, and ORDER_ITEM tables to maintain data integrity.
- Relational Admin Dashboard: A centralized view for administrators to track full transaction histories, customer details, and total revenue across multiple joins.
- Advanced SQL Implementation: Optimized queries for artist-specific catalogs, stock alerts, and customer spending analysis.

## Technical Stack

- Frontend/Logic: Streamlit (Python)
- Database: MySQL 8.0
- External Integration: Apple iTunes Search API
- Data Handling: Pandas, Requests, MySQL Connector, Python-Dotenv

## Project Architecture

1. Schema (01_schema.sql): Defines the relational structure, including primary/foreign keys and business logic constraints.
2. Seed Data (02_seed.sql): Populates the environment with initial artists, multi-format album variants (Vinyl/CD), and sample transactions.
3. Application (app.py): The main interface bridging the MySQL backend with the user-facing Streamlit dashboard.

## Installation and Execution

1. Configure the .env file with your local MySQL credentials:
   DB_HOST=your_host
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=RECORD_STORE

2. Execute the SQL scripts in your MySQL environment to initialize the schema and seed data.

3. Install dependencies:
   pip install mysql-connector-python pandas requests python-dotenv streamlit

4. Launch the application:
   streamlit run app.py