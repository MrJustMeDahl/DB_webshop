from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_redis import connect_redis
from database.db_connectors.connect_mongodb import connect_mongodb

def find_active_by_id(user_id):
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return None

    cursor = mysql_conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer_id = %s AND is_active = TRUE", (user_id,))
    user = cursor.fetchone()
    mysql_conn.close()

    if user:
        return {
            "customer_id": user[0],
            "username": user[1],
        }
    return None

def update_username_password(user_id, new_username, new_password):
    if not new_username:
        new_username = None
    if not new_password:
        new_password = None

    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    cursor = mysql_conn.cursor()
    cursor.callproc("update_customer_credentials", (user_id, new_username, new_password))
    result_data = None
    for result in cursor.stored_results():
        result = result.fetchone()
        if result[0] == "no_changes":
            result_data = "no_changes"
        else:
            result_data = {
                "customer_id": result[0],
                "username": result[1],
            }
    cursor.close()
    mysql_conn.close()
    return result_data

def soft_delete_user(user_id):
    mysql_conn = connect_mysql()
    if not mysql_conn:
        return False

    cursor = mysql_conn.cursor()
    cursor.execute("UPDATE customer SET is_active = FALSE WHERE customer_id = %s", (user_id,))
    mysql_conn.commit()
    cursor.close()
    mysql_conn.close()
    return True