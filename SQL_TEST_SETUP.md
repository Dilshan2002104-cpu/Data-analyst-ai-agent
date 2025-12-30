# SQL Test Database Setup Guide

This guide explains how to set up test databases for the Data Analyst AI Agent.

## Files Included

- `test_database_mysql.sql` - MySQL/MariaDB setup script
- `test_database_postgresql.sql` - PostgreSQL setup script

## Database Schema

Both scripts create the same schema with the following tables:

### Tables
1. **regions** - Geographic regions (North, South, East, West, Europe, Asia)
2. **customers** - Customer information (10 sample customers)
3. **products** - Product catalog (10 electronics and accessories)
4. **orders** - Order records (15 sample orders)
5. **order_items** - Order line items (detailed order contents)

### Views
- **sales_summary** - Aggregated sales by region
- **top_products** - Best-selling products by revenue

## Setup Instructions

### MySQL Setup

1. **Install MySQL** (if not already installed)
   ```bash
   # Windows: Download from https://dev.mysql.com/downloads/installer/
   # Or use XAMPP/WAMP which includes MySQL
   ```

2. **Run the setup script**
   ```bash
   mysql -u root -p < test_database_mysql.sql
   ```

   Or using MySQL Workbench:
   - Open MySQL Workbench
   - File → Open SQL Script → Select `test_database_mysql.sql`
   - Execute (⚡ icon)

3. **Create a read-only user** (recommended for security)
   ```sql
   CREATE USER 'analyst_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT SELECT ON sales_test_db.* TO 'analyst_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Connection details for the app:**
   - Database Type: MySQL
   - Host: `localhost`
   - Port: `3306`
   - Database: `sales_test_db`
   - Username: `analyst_user`
   - Password: `your_password`

### PostgreSQL Setup

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # Windows: Download from https://www.postgresql.org/download/windows/
   ```

2. **Create the database**
   ```bash
   psql -U postgres
   CREATE DATABASE sales_test_db;
   \q
   ```

3. **Run the setup script**
   ```bash
   psql -U postgres -d sales_test_db -f test_database_postgresql.sql
   ```

   Or using pgAdmin:
   - Open pgAdmin
   - Right-click on sales_test_db → Query Tool
   - Open `test_database_postgresql.sql`
   - Execute (▶ icon)

4. **Create a read-only user** (recommended for security)
   ```sql
   CREATE USER analyst_user WITH PASSWORD 'your_password';
   GRANT CONNECT ON DATABASE sales_test_db TO analyst_user;
   GRANT USAGE ON SCHEMA public TO analyst_user;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_user;
   ```

5. **Connection details for the app:**
   - Database Type: PostgreSQL
   - Host: `localhost`
   - Port: `5432`
   - Database: `sales_test_db`
   - Username: `analyst_user`
   - Password: `your_password`

## Test Data Summary

- **10 Customers** across 6 regions
- **10 Products** (Electronics and Accessories)
- **15 Orders** (Jan-Feb 2024)
- **Total Revenue**: ~$32,000 (completed orders)

## Sample Questions to Test

Once connected, try these questions in the Unified Chat:

### SQL-Only Queries
1. "What are the top 5 customers by total spending?"
2. "Show me sales by region"
3. "Which products are best sellers?"
4. "What's the monthly sales trend?"
5. "How many pending orders do we have?"

### Cross-Source Queries (if you also have CSV uploaded)
1. "Compare sales.csv with the database"
2. "Is the CSV data consistent with the database?"
3. "Show me a chart combining both sources"

## Verification

After running the setup script, you should see:
```
Database setup complete!
total_customers: 10
total_products: 10
total_orders: 15
total_revenue: 32100.00
```

## Troubleshooting

### MySQL Connection Issues
- Check if MySQL service is running
- Verify port 3306 is not blocked by firewall
- Ensure user has proper permissions

### PostgreSQL Connection Issues
- Check if PostgreSQL service is running
- Verify port 5432 is not blocked by firewall
- Check `pg_hba.conf` for connection permissions

### Permission Errors
- Make sure the user has SELECT permissions
- For testing, you can use root/postgres, but read-only is recommended

## Security Notes

⚠️ **Important Security Practices:**
1. Always use read-only users for the application
2. Never use root/postgres accounts in production
3. Use strong passwords
4. Restrict network access to localhost for testing
5. The app only allows SELECT queries (no INSERT/UPDATE/DELETE)
