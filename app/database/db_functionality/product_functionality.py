from database.db_connectors.connect_mysql import connect_mysql
from database.db_functionality.redis_functionality import (
    get_cached_products, cache_products, clear_product_cache
)


def update_product(product_id, description, price):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET description = %s, price = %s WHERE product_id = %s AND is_active = TRUE", (description, price, product_id))
    conn.commit()
    success = cursor.rowcount > 0
    cursor.close()
    conn.close()
    clear_product_cache()
    return success

def create_product(description, price):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (description, price) VALUES (%s, %s)", (description, price))
    conn.commit()
    success = cursor.lastrowid is not None
    cursor.close()
    conn.close()
    clear_product_cache()
    return success

def soft_delete_product(product_id):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET is_active = FALSE WHERE product_id = %s", (product_id,))
    conn.commit()
    success = cursor.rowcount > 0
    cursor.close()
    conn.close()
    clear_product_cache()
    return success

def get_products(limit, anchor_id, search_filter, direction):
    normalized_filter = (search_filter or "").strip().lower()
    cache_key = f"products:{normalized_filter}:{anchor_id}:{direction}:{limit}"

    cached_products, has_more = get_cached_products(cache_key)
    if cached_products is not None:
        return cached_products, has_more

    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "CALL pagination(%s, %s, %s, %s)",
        (limit + 1, anchor_id, search_filter, direction)
    )
    result = cursor.fetchall()
    conn.close()

    has_more = len(result) > limit
    products = result[:limit]

    if direction == "prev":
        products.reverse()

    cache_products(cache_key, products, has_more)
    return products, has_more