import streamlit as st
from database.db_connectors.connect_redis import connect_redis
from database.db_connectors.connect_mysql import connect_mysql

# Ensure login
if "username" not in st.session_state:
    st.error("Please log in to view your cart.")
    st.stop()

username = st.session_state["username"]
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
    st.markdown(f"Total: ${total:.2f}")

    if st.button("Clear Cart"):
        redis_conn.delete(cart_key)
        st.success("Cart cleared!")
        st.rerun()
    if st.button("Checkout"):
        st.success("Checkout functionality is not implemented yet.")