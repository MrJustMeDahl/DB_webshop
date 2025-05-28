USE webshop_db;

-- 1. Insert customers
INSERT IGNORE INTO customer (customer_id, username, password)
SELECT DISTINCT
    CustomerID,
    CONCAT('user_', CustomerID),
    LEFT(MD5(CustomerID), 10)
FROM raw_data
WHERE CustomerID IS NOT NULL;

-- 2. Map products
SET @pid := 0;


DROP TEMPORARY TABLE IF EXISTS product_map;
CREATE TEMPORARY TABLE product_map AS
SELECT
    @pid := @pid + 1 AS product_id,
    StockCode,
    MAX(LEFT(Description, 45)) AS description,
    MAX(UnitPrice) AS price
FROM raw_data
WHERE UnitPrice > 0
GROUP BY StockCode;

CREATE TABLE IF NOT EXISTS product_map_final AS SELECT * FROM product_map;

INSERT IGNORE INTO product (product_id, description, price)
SELECT product_id, description, price
FROM product_map_final;

-- 3. Map orders
SET @oid := 0;
DROP TEMPORARY TABLE IF EXISTS order_map;
CREATE TEMPORARY TABLE order_map AS
SELECT
    @oid := @oid + 1 AS order_id,
    InvoiceNo,
    MAX(InvoiceDate) AS order_date,
    MAX(CustomerID) AS customer_id,
    SUM(Quantity * UnitPrice) AS total_price
FROM raw_data
WHERE CustomerID IS NOT NULL
GROUP BY InvoiceNo;

CREATE TABLE IF NOT EXISTS order_map_final AS SELECT * FROM order_map;

INSERT IGNORE INTO `order` (order_id, order_date, total_price, customer_id)
SELECT order_id, order_date, total_price, customer_id
FROM order_map_final;

-- 4. Insert order lines in chunks using id ranges
-- Adjust ranges if needed (raw_data has ~541,000 rows)

-- CHUNK 1
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 1 AND 100000;

-- CHUNK 2
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 100001 AND 200000;

-- CHUNK 3
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 200001 AND 300000;

-- CHUNK 4
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 300001 AND 400000;

-- CHUNK 5
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 400001 AND 470000;

-- CHUNK 6
INSERT IGNORE INTO order_lines (order_id, product_id, quantity, price)
SELECT om.order_id, pm.product_id, rd.Quantity, rd.UnitPrice
FROM raw_data rd
JOIN product_map_final pm ON rd.StockCode = pm.StockCode
JOIN order_map_final om ON rd.InvoiceNo = om.InvoiceNo
WHERE rd.id BETWEEN 470001 AND 541909;

