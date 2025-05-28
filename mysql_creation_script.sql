CREATE DATABASE  IF NOT EXISTS `webshop_db`;
USE `webshop_db`;

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
  `customer_id` int NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `order_date` varchar(45) NOT NULL,
  `total_price` float NOT NULL DEFAULT '0',
  `customer_id` int NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id_idx` (`customer_id`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `date_paid` datetime NOT NULL,
  `order_id` int DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `order_id_idx` (`order_id`),
  CONSTRAINT `order_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `product`;

CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `description` varchar(45) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `review`;

CREATE TABLE `reviews` (
  `review_id` varchar(45) NOT NULL,
  `rating` float NOT NULL,
  `customer_id` int NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`review_id`),
  KEY `product_id_review_idx` (`product_id`),
  KEY `customer_id_review_idx` (`customer_id`),
  CONSTRAINT `customer_id_review` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `product_id_review` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `order_lines`;

CREATE TABLE `order_lines` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `product_id_idx` (`product_id`),
  CONSTRAINT `order_id_lines` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
