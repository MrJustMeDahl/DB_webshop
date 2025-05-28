USE webshop_db;

-- Drop existing staging table if needed
DROP TABLE IF EXISTS raw_data;

-- Create raw_data with an id for chunking
CREATE TABLE raw_data (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice FLOAT,
    CustomerID INT,
    Country VARCHAR(100)
);

-- Load the cleaned CSV file into raw_data
LOAD DATA INFILE '/var/lib/mysql-files/data_fixed.csv'
INTO TABLE raw_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(InvoiceNo, StockCode, Description, Quantity, @InvoiceDate, UnitPrice, @CustomerID, Country)
SET
  InvoiceDate = STR_TO_DATE(@InvoiceDate, '%Y-%m-%d %H:%i:%s'),
  CustomerID = NULLIF(@CustomerID, '');
