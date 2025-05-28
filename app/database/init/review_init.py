from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_mongodb import connect_mongodb
import random
from lorem_text import lorem

def init_review_database():
    
    mysql_conn = connect_mysql()
    
    if mysql_conn:
        cursor = mysql_conn.cursor()
        cursor.execute("SELECT DISTINCT customer_id, product_id from webshop_db.orders as o JOIN webshop_db.order_lines as ol ON o.order_id = ol.order_id")
        result = cursor.fetchall()

        cursor.close()
        

        if result:
            mongo_conn = connect_mongodb()
            if mongo_conn:
                db = mongo_conn['webshop_db']
                collection = db['reviews']
                generated_reviews = {}
                for row in range(len(result)):
                    review = {
                        "review_text": lorem.sentence(),
                    }
                    mongo_result = collection.insert_one(review)
                    review['review_id'] = str(mongo_result.inserted_id)
                    review['customer_id'] = result[row][0]
                    review['product_id'] = result[row][1]
                    generated_reviews[row] = review

                mongo_conn.close()

            cursor = mysql_conn.cursor()
            for review in generated_reviews:
                cursor.execute("INSERT INTO webshop_db.reviews (review_id, rating, customer_id, product_id) VALUES (%s, %s, %s, %s)",
                               (generated_reviews[review]['review_id'], random.randint(1, 5), generated_reviews[review]['customer_id'], generated_reviews[review]['product_id']))
            cursor.close()
            mysql_conn.commit()
        mysql_conn.close()

    else:
        print("Failed to connect to MySQL database.")

init_review_database()