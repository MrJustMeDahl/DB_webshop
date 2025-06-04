import streamlit as st
from database.db_functionality.redis_functionality import (
    get_cart, get_redis_connection, remove_item_from_cart, clear_cart
)
from database.db_functionality.cart_functionality import get_product_info
from database.db_connectors.connect_mysql import connect_mysql  # needed for stored procedure call

if "username" not in st.session_state or "user_id" not in st.session_state:
    st.error("Please log in to view your cart.")
    st.stop()

username = st.session_state["username"]
customer_id = st.session_state["user_id"]


redis_conn = get_redis_connection()
if not redis_conn:
    st.error("Could not connect to Redis.")
    st.stop()

cart_key, cart = get_cart(redis_conn, username)
if not cart:
    st.info("Your cart is empty.")
else:
    total = 0
    for product_id, quantity in cart.items():
        product = get_product_info(product_id)
        if product:
            subtotal = product["price"] * int(quantity)
            total += subtotal
            st.subheader(f"{product['description']} (x{quantity})")
            st.write(f"Price: ${product['price']} | Subtotal: ${subtotal:.2f}")
            if st.button("Remove", key=f"remove_{product_id}"):
                remove_item_from_cart(redis_conn, cart_key, product_id)
                st.rerun()

    st.markdown(f"### Total: ${total:.2f}")

    if st.button("Clear Cart"):
        clear_cart(redis_conn, cart_key)
        st.success("Cart cleared!")
        st.rerun()

    if st.button("Checkout"):
        conn = connect_mysql()
        if not conn:
            st.error("Database connection error.")
            st.stop()

        try:
            cursor = conn.cursor()
            order_id = 0  # initial INOUT value

            for product_id, quantity in cart.items():
                cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
                result = cursor.fetchone()
                if not result:
                    continue
                price = float(result[0])

                args = [customer_id, product_id, int(quantity), price, order_id]
                result_args = cursor.callproc("create_order_with_line", args)
                order_id = result_args[4]  # update INOUT value after first call

            conn.commit()
            clear_cart(redis_conn, cart_key)
            st.success(f"Order placed successfully! Your Order ID is #{order_id}")

        except Exception as e:
            conn.rollback()
            st.error(f"Checkout failed: {e}")
        finally:
            conn.close()
