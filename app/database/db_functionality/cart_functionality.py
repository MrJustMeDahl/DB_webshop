from database.db_connectors.connect_mysql import connect_mysql

def get_product_info(product_id):
    conn = connect_mysql()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT description, price FROM products WHERE product_id = %s", (product_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def create_order_from_cart(customer_id, cart):
    conn = connect_mysql()
    if not conn:
        return None, "Database connection error"

    try:
        cursor = conn.cursor()

        # Step 1: Get next available order ID
        cursor.execute("SELECT COALESCE(MAX(order_id), 0) + 1 FROM orders")
        order_id = cursor.fetchone()[0]

        # Step 2: Insert the order manually (only once)
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id) VALUES (%s, %s)",
            (order_id, customer_id)
        )

        # Step 3: Use the stored procedure to add all order lines
        for product_id, quantity in cart.items():
            cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if not result:
                continue
            price = float(result[0])

            # Stored procedure call: uses the fixed order_id
            args = [customer_id, product_id, int(quantity), price, order_id]
            cursor.callproc("create_order_with_line", args)

        conn.commit()
        return order_id, None

    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        conn.close()

