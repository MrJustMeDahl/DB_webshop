import json
from database.db_connectors.connect_redis import connect_redis

def get_redis_connection():
    return connect_redis()

# Cart operations
def get_cart(redis_conn, username):
    cart_key = f"cart:{username}"
    cart = redis_conn.hgetall(cart_key)
    return cart_key, cart

def add_to_cart(redis_conn, cart_key, product_id, quantity=1, ttl=3600):
    redis_conn.hincrby(cart_key, product_id, quantity)
    redis_conn.expire(cart_key, ttl)

def remove_item_from_cart(redis_conn, cart_key, product_id):
    redis_conn.hdel(cart_key, product_id)

def clear_cart(redis_conn, cart_key):
    redis_conn.delete(cart_key)

# Product caching
def get_cached_products(cache_key):
    redis_conn = get_redis_connection()
    if not redis_conn:
        return None, None
    cached = redis_conn.get(cache_key)
    if cached:
        try:
            data = json.loads(cached)
            return data.get("products"), data.get("has_more")
        except json.JSONDecodeError:
            return None, None
    return None, None

def cache_products(cache_key, products, has_more, ttl=300):
    redis_conn = get_redis_connection()
    if redis_conn:
        redis_conn.setex(cache_key, ttl, json.dumps({
            "products": products,
            "has_more": has_more
        }))

def clear_product_cache():
    redis_conn = get_redis_connection()
    if redis_conn:
        for key in redis_conn.scan_iter("products:*"):
            redis_conn.delete(key)
    else:
        print("Redis connection failed, cannot clear product cache.")