from db_connectors.connect_mysql import connect_mysql
from db_connectors.connect_mongodb import connect_mongodb
from db_connectors.connect_redis import connect_redis

def main():
    mysql_conn = connect_mysql()
    mongodb_client = connect_mongodb()
    redis_conn = connect_redis()

    if mysql_conn:
        mysql_conn.close()
    if redis_conn:
        redis_conn.close()
    if mongodb_client:
        mongodb_client.close()

if __name__ == "__main__":
    main()
