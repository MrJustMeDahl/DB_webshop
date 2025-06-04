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

from database.db_connectors.connect_mysql import connect_mysql

def create_order_from_cart(customer_id, cart):
    conn = connect_mysql()
    if not conn:
        return None, "Database connection error"

    try:
        cursor = conn.cursor()

        # Set the INOUT parameter as a mutable variable (initially 0)
        order_id = 0

        for product_id, quantity in cart.items():
            # Get the product price
            cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if not result:
                continue
            price = float(result[0])

            # Call stored procedure with INOUT parameter
            args = [customer_id, product_id, int(quantity), price, order_id]
            results = cursor.callproc("create_order_with_line", args)

            # Update the order_id from the OUT parameter (last one)
            order_id = results[4]  # Get updated INOUT value

        conn.commit()
        return order_id, None

    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        conn.close()

