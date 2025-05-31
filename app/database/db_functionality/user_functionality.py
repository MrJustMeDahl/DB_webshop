from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_redis import connect_redis
from database.db_connectors.connect_mongodb import connect_mongodb

def find_by_id(user_id):
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return None

    cursor = mysql_conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s", (user_id,))
    user = cursor.fetchone()
    mysql_conn.close()

    if user:
        return {
            "customer_id": user[0],
            "username": user[1],
        }
    return None

def update_username_password(user_id, new_username, new_password):
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    cursor = mysql_conn.cursor()
    cursor.execute("UPDATE customer SET username = %s, password = %s WHERE customer_id = %s",
                   (new_username, new_password, user_id))
    mysql_conn.commit()
    cursor.close()
    mysql_conn.close()

    return True