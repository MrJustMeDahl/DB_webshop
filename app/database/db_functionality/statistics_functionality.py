from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_mongodb import connect_mongodb
import pandas as pd

def fetch_monthly_revenue():
    query = '''
        SELECT 
          YEAR(order_date) AS year,
          MONTH(order_date) AS month,
          SUM(total_price) AS total_revenue
        FROM orders
        GROUP BY year, month
        ORDER BY year, month;
    '''
    mysql_conn = connect_mysql()
    if mysql_conn is None:
        raise ConnectionError("Failed to connect to MySQL database.")
    df = pd.read_sql(query, mysql_conn)
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    mysql_conn.close()
    return df

def fetch_avg_customer_revenue():
    query = '''
        SELECT 
          AVG(customer_total) AS avg_customer_revenue
        FROM (
          SELECT 
            customer_id,
            SUM(total_price) AS customer_total
          FROM orders
          GROUP BY customer_id
        ) AS customer_sums;
    '''
    
    mysql_conn = connect_mysql()
    if mysql_conn is None:
        raise ConnectionError("Failed to connect to MySQL database.")
    cursor = mysql_conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    mysql_conn.close()
    return result

def fetch_avg_order_value():
    query = '''
        SELECT 
          AVG(total_price) AS avg_order_value
        FROM (
          SELECT 
            order_id,
            total_price
          FROM orders
          GROUP BY order_id
        ) AS order_sums;
    '''
    
    mysql_conn = connect_mysql()
    if mysql_conn is None:
        raise ConnectionError("Failed to connect to MySQL database.")
    cursor = mysql_conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    mysql_conn.close()
    return result

def fetch_avg_review_length():
    mongodb_conn = connect_mongodb()
    if mongodb_conn is None:
        raise ConnectionError("Failed to connect to MongoDB database.")
    db = mongodb_conn['webshop_db']
    reviews_collection = db['reviews']
    pipeline = [
        {"$match": {"review_text": {"$type": "string"}}},
        {
            "$project": {
                "word_count": {
                    "$size": {
                        "$filter": {
                            "input": { "$split": ["$review_text", " "] },
                            "as": "word",
                            "cond": { "$ne": ["$$word", ""] }
                        }
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "average_word_count": { "$avg": "$word_count" }
            }
        }
    ]
    result = list(reviews_collection.aggregate(pipeline))
    return result[0]['average_word_count'] if result else 0