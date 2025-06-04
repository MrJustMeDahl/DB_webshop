from database.db_connectors.connect_mysql import connect_mysql

def get_unpaid_orders(customer_id):
    conn = connect_mysql()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM unpaid_orders_view
        WHERE customer_id = %s
    """, (customer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


def get_paid_orders(customer_id):
    conn = connect_mysql()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM paid_orders_view
        WHERE customer_id = %s
        ORDER BY date_paid DESC
    """, (customer_id,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders


def get_order_items(order_id):
    conn = connect_mysql()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.description, ol.quantity, ol.price
        FROM order_lines ol
        JOIN products p ON ol.product_id = p.product_id
        WHERE ol.order_id = %s
    """, (order_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return items


def pay_order(order_id):
    conn = connect_mysql()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.callproc("create_payment", (order_id,))
        conn.commit()
        cursor.close()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()
