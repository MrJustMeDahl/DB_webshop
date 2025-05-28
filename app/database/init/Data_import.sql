USE webshop_db;

-- 1. Insert customers
INSERT IGNORE INTO customer (customer_id, username, password)
SELECT DISTINCT
    CustomerID,
    CONCAT('user_', CustomerID),
    LEFT(MD5(CustomerID), 10)
FROM raw_data
WHERE CustomerID IS NOT NULL;

-- 2. Map products using StockCode as product_id (VARCHAR)
DROP TEMPORARY TABLE IF EXISTS product_map;
CREATE TEMPORARY TABLE product_map AS
SELECT DISTINCT
    StockCode AS product_id,
    LEFT(MAX(Description), 45) AS description,
    MAX(UnitPrice) AS price
FROM raw_data
WHERE UnitPrice > 0
GROUP BY StockCode;

DROP TABLE IF EXISTS product_map_final;
CREATE TABLE product_map_final AS SELECT * FROM product_map;

INSERT IGNORE INTO products (product_id, description, price)
SELECT product_id, description, price
FROM product_map_final;

-- 3. Map orders using InvoiceNo as order_id (INT)
DROP TEMPORARY TABLE IF EXISTS order_map;
CREATE TEMPORARY TABLE order_map AS
SELECT DISTINCT
    CAST(InvoiceNo AS UNSIGNED) AS order_id,
    MAX(InvoiceDate) AS order_date,
    MAX(CustomerID) AS customer_id,
    0 AS total_price
FROM raw_data
WHERE CustomerID IS NOT NULL AND InvoiceNo REGEXP '^[0-9]+$'
GROUP BY InvoiceNo;

DROP TABLE IF EXISTS order_map_final;
CREATE TABLE order_map_final AS SELECT * FROM order_map;

INSERT IGNORE INTO orders (order_id, order_date, total_price, customer_id)
SELECT order_id, order_date, total_price, customer_id
FROM order_map_final;

-- 4. Insert order lines in chunks using id ranges

-- CHUNK 1
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 1 AND 100000;

-- CHUNK 2
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 100001 AND 200000;

-- CHUNK 3
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 200001 AND 300000;

-- CHUNK 4
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 300001 AND 400000;

-- CHUNK 5
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 400001 AND 470000;

-- CHUNK 6
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT 
    CAST(rd.InvoiceNo AS UNSIGNED),
    rd.StockCode,
    rd.Quantity,
    rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.product_id
JOIN order_map_final om ON rd.InvoiceNo = om.order_id
WHERE rd.id BETWEEN 470001 AND 541909;
