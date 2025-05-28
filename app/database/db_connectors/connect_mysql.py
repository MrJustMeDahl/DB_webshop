import mysql.connector

def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host="mysql-db",
            user="root",
            password="rootpassword",
            database="webshop_db"
        )
        print("MySQL connection successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL connection error: {err}")
        return None
