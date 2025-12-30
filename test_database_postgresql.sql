-- PostgreSQL Test Database Setup for Data Analyst AI Agent
-- This creates a sample sales database for testing the SQL integration

-- Create database (run this separately as postgres superuser)
-- CREATE DATABASE sales_test_db;
-- \c sales_test_db

-- Drop tables if they exist
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS regions CASCADE;

-- Create regions table
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Create customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    region_id INTEGER REFERENCES regions(region_id),
    signup_date DATE
);

-- Create products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    unit_price DECIMAL(10, 2),
    stock_quantity INTEGER
);

-- Create orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date DATE,
    status VARCHAR(20),
    total_amount DECIMAL(10, 2)
);

-- Create order_items table
CREATE TABLE order_items (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    price DECIMAL(10, 2)
);

-- Insert sample data into regions
INSERT INTO regions (region_name, country) VALUES
('North', 'USA'),
('South', 'USA'),
('East', 'USA'),
('West', 'USA'),
('Europe', 'UK'),
('Asia', 'Japan');

-- Insert sample data into customers
INSERT INTO customers (customer_name, email, region_id, signup_date) VALUES
('Acme Corporation', 'contact@acme.com', 1, '2023-01-15'),
('Tech Solutions Inc', 'info@techsol.com', 2, '2023-02-20'),
('Global Traders', 'sales@globaltraders.com', 3, '2023-03-10'),
('Mega Retail', 'support@megaretail.com', 4, '2023-04-05'),
('Euro Imports', 'hello@euroimports.com', 5, '2023-05-12'),
('Asia Pacific Ltd', 'contact@asiapacific.com', 6, '2023-06-18'),
('Prime Distributors', 'info@primedist.com', 1, '2023-07-22'),
('Quality Goods Co', 'sales@qualitygoods.com', 2, '2023-08-30'),
('Fast Logistics', 'support@fastlog.com', 3, '2023-09-14'),
('Smart Buyers', 'hello@smartbuyers.com', 4, '2023-10-25');

-- Insert sample data into products
INSERT INTO products (product_name, category, unit_price, stock_quantity) VALUES
('Laptop Pro 15', 'Electronics', 1200.00, 50),
('Wireless Mouse', 'Electronics', 25.00, 200),
('Mechanical Keyboard', 'Electronics', 75.00, 150),
('4K Monitor', 'Electronics', 350.00, 80),
('USB-C Hub', 'Electronics', 45.00, 120),
('Laptop Stand', 'Accessories', 30.00, 100),
('Webcam HD', 'Electronics', 80.00, 90),
('Headphones Pro', 'Electronics', 150.00, 110),
('Desk Lamp LED', 'Accessories', 35.00, 75),
('Cable Organizer', 'Accessories', 12.00, 200);

-- Insert sample data into orders
INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES
(1, '2024-01-05', 'Completed', 2500.00),
(2, '2024-01-08', 'Completed', 1800.00),
(3, '2024-01-12', 'Completed', 3200.00),
(4, '2024-01-15', 'Pending', 950.00),
(5, '2024-01-18', 'Completed', 4100.00),
(6, '2024-01-22', 'Completed', 1500.00),
(7, '2024-01-25', 'Shipped', 2800.00),
(8, '2024-01-28', 'Completed', 1200.00),
(9, '2024-02-02', 'Completed', 3500.00),
(10, '2024-02-05', 'Processing', 2200.00),
(1, '2024-02-08', 'Completed', 1900.00),
(2, '2024-02-12', 'Completed', 2700.00),
(3, '2024-02-15', 'Cancelled', 0.00),
(4, '2024-02-18', 'Completed', 3800.00),
(5, '2024-02-22', 'Completed', 1600.00);

-- Insert sample data into order_items
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 1200.00),
(1, 4, 1, 350.00),
(2, 1, 1, 1200.00),
(2, 8, 4, 150.00),
(3, 1, 2, 1200.00),
(3, 3, 10, 75.00),
(4, 2, 20, 25.00),
(4, 5, 10, 45.00),
(5, 1, 3, 1200.00),
(5, 7, 5, 80.00),
(6, 8, 10, 150.00),
(7, 1, 2, 1200.00),
(7, 6, 10, 30.00),
(8, 1, 1, 1200.00),
(9, 1, 2, 1200.00),
(9, 4, 3, 350.00),
(10, 3, 20, 75.00),
(10, 9, 20, 35.00),
(11, 1, 1, 1200.00),
(11, 2, 28, 25.00),
(12, 1, 2, 1200.00),
(12, 5, 5, 45.00),
(14, 1, 3, 1200.00),
(14, 6, 5, 30.00),
(15, 8, 10, 150.00),
(15, 9, 2, 35.00);

-- Create useful views for testing
CREATE VIEW sales_summary AS
SELECT 
    r.region_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN regions r ON c.region_id = r.region_id
WHERE o.status = 'Completed'
GROUP BY r.region_name;

CREATE VIEW top_products AS
SELECT 
    p.product_name,
    p.category,
    SUM(oi.quantity) as total_sold,
    SUM(oi.quantity * oi.price) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC;

-- Sample queries to test
-- Query 1: Top customers by revenue
-- SELECT c.customer_name, SUM(o.total_amount) as total_spent
-- FROM customers c JOIN orders o ON c.customer_id = o.customer_id
-- WHERE o.status = 'Completed'
-- GROUP BY c.customer_id, c.customer_name ORDER BY total_spent DESC LIMIT 10;

-- Query 2: Sales by region
-- SELECT * FROM sales_summary ORDER BY total_revenue DESC;

-- Query 3: Product performance
-- SELECT * FROM top_products LIMIT 10;

-- Query 4: Monthly sales trend
-- SELECT TO_CHAR(order_date, 'YYYY-MM') as month, 
--        COUNT(*) as orders, SUM(total_amount) as revenue
-- FROM orders WHERE status = 'Completed'
-- GROUP BY month ORDER BY month;

-- Grant permissions (adjust username as needed)
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO your_username;
-- GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO your_username;

SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as total_customers FROM customers;
SELECT COUNT(*) as total_products FROM products;
SELECT COUNT(*) as total_orders FROM orders;
SELECT SUM(total_amount) as total_revenue FROM orders WHERE status = 'Completed';
