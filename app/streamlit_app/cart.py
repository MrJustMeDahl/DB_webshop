import streamlit as st
from database.db_connectors.connect_redis import connect_redis
from database.db_connectors.connect_mysql import connect_mysql

# Ensure login
if "username" not in st.session_state or "user_id" not in st.session_state:
    st.error("Please log in to view your cart.")
    st.stop()

username = st.session_state["username"]
customer_id = st.session_state["user_id"]
cart_key = f"cart:{username}"

redis_conn = connect_redis()
if not redis_conn:
    st.error("Could not connect to Redis.")
    st.stop()

st.title("🛒 Your Cart")

# Load cart data
cart = redis_conn.hgetall(cart_key)

if not cart:
    st.info("Your cart is empty.")
else:
    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    total = 0

    for product_id, quantity in cart.items():
        cursor.execute("SELECT description, price FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if product:
            subtotal = product["price"] * int(quantity)
            total += subtotal
            st.subheader(f"{product['description']} (x{quantity})")
            st.write(f"Price: ${product['price']} | Subtotal: ${subtotal:.2f}")
            if st.button(f"Remove {product_id}", key=f"remove_{product_id}"):
                redis_conn.hdel(cart_key, product_id)
                st.rerun()

    conn.close()
    st.markdown(f"### Total: ${total:.2f}")

    if st.button("Clear Cart"):
        redis_conn.delete(cart_key)
        st.success("Cart cleared!")
        st.rerun()

    if st.button("Checkout"):
        conn = connect_mysql()
        if not conn:
            st.error("Database error. Try again.")
            st.stop()

        try:
            cursor = conn.cursor()
            order_id = 0

            for product_id, quantity in cart.items():
                quantity = int(quantity)

                cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
                result = cursor.fetchone()
                if not result:
                    continue
                price = float(result[0])

                # Call stored procedure
                args = [customer_id, product_id, quantity, price, order_id]
                cursor.callproc("create_order_with_line", args)

                # Update order_id
                for result_set in cursor.stored_results():
                    pass
                order_id_query = "SELECT LAST_INSERT_ID()"
                cursor.execute(order_id_query)
                order_id = cursor.fetchone()[0]

            conn.commit()
            redis_conn.delete(cart_key)
            st.success(f"✅ Order placed successfully! Your Order ID is #{order_id}")

        except Exception as e:
            conn.rollback()
            st.error(f"❌ Checkout failed: {e}")
        finally:
            conn.close()
