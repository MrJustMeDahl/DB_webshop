import redis

def connect_redis():
    try:
        r = redis.Redis(host='redis-master-node', port=6379, decode_responses=True)
        r.ping()
        print("Redis connection successful.")
        return r
    except redis.ConnectionError as err:
        print(f"Redis connection error: {err}")
        return None
