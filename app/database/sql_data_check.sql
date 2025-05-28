USE webshop_db;

-- Raw data row count
SELECT 'raw_data rows' AS label, COUNT(*) AS total FROM raw_data;

-- Customers
SELECT 'customers' AS label, COUNT(*) AS total FROM customer;

-- Products
SELECT 'products' AS label, COUNT(*) AS total FROM products;

-- Orders
SELECT 'orders' AS label, COUNT(*) AS total FROM `orders`;

-- Order Lines
SELECT 'order_lines' AS label, COUNT(*) AS total FROM order_lines;

-- product IDs used in order_lines all exist
SELECT 'invalid product_ids in order_lines' AS label, COUNT(*) AS issues
FROM order_lines ol
LEFT JOIN product p ON ol.product_id = p.product_id
WHERE p.product_id IS NULL;

-- order IDs used in order_lines all exist
SELECT 'invalid order_ids in order_lines' AS label, COUNT(*) AS issues
FROM order_lines ol
LEFT JOIN `order` o ON ol.order_id = o.order_id
WHERE o.order_id IS NULL;

-- pick 5 random order lines
SELECT o.order_id, c.username, p.description, ol.quantity, ol.price
FROM order_lines ol
JOIN `order` o ON ol.order_id = o.order_id
JOIN customer c ON o.customer_id = c.customer_id
JOIN product p ON ol.product_id = p.product_id
LIMIT 5;

-- Optional: check for any missing usernames or passwords
SELECT 'missing usernames' AS label, COUNT(*) AS issues
FROM customer
WHERE username IS NULL OR password IS NULL;

-- Optional: check for NULLs in order fields
SELECT 'orders with NULL customer_id or date' AS label, COUNT(*) AS issues
FROM `order`
WHERE customer_id IS NULL OR order_date IS NULL;
