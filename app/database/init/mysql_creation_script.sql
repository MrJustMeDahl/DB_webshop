CREATE DATABASE IF NOT EXISTS webshop_db;
USE webshop_db;

DROP TABLE IF EXISTS customer;
CREATE TABLE customer (
  customer_id INT NOT NULL,
  username VARCHAR(45) NOT NULL,
  password VARCHAR(45) NOT NULL,
  PRIMARY KEY (customer_id),
  UNIQUE KEY username_UNIQUE (username)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  product_id INT NOT NULL,
  description VARCHAR(45) NOT NULL,
  price FLOAT NOT NULL,
  PRIMARY KEY (product_id)
);

DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  order_id INT NOT NULL,
  order_date VARCHAR(45) NOT NULL,
  total_price FLOAT NOT NULL DEFAULT '0',
  customer_id INT NOT NULL,
  PRIMARY KEY (order_id),
  KEY customer_id_idx (customer_id),
  CONSTRAINT customer_id FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

DROP TABLE IF EXISTS order_lines;
CREATE TABLE order_lines (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  price FLOAT NOT NULL,
  PRIMARY KEY (order_id, product_id),
  KEY product_id_idx (product_id),
  CONSTRAINT order_id_lines FOREIGN KEY (order_id) REFERENCES `order` (order_id),
  CONSTRAINT product_id FOREIGN KEY (product_id) REFERENCES product (product_id)
);

DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
  payment_id INT NOT NULL AUTO_INCREMENT,
  date_paid DATETIME NOT NULL,
  order_id INT DEFAULT NULL,
  PRIMARY KEY (payment_id),
  KEY order_id_idx (order_id),
  CONSTRAINT order_id FOREIGN KEY (order_id) REFERENCES `order` (order_id)
);

DROP TABLE IF EXISTS review;
CREATE TABLE review (
  review_id INT NOT NULL,
  rating FLOAT NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL,
  PRIMARY KEY (review_id),
  KEY product_id_review_idx (product_id),
  KEY customer_id_review_idx (customer_id),
  CONSTRAINT customer_id_review FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
  CONSTRAINT product_id_review FOREIGN KEY (product_id) REFERENCES product (product_id)
);
