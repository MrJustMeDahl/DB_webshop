import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql

# Ensure login
if "username" and "user_id" not in st.session_state:
    st.error("Please log in to view your orders.")
    st.stop()

conn = connect_mysql()
if not conn:
    st.error("Could not connect to database.")
    st.stop()

cursor = conn.cursor(dictionary=True)
user_id = st.session_state["user_id"]

# Fetch unpaid orders
cursor.execute("""
    SELECT * FROM unpaid_orders_view
    WHERE customer_id = %s
""", (user_id,))
unpaid_orders = cursor.fetchall()

# Fetch paid orders
cursor.execute("""
    SELECT * FROM paid_orders_view
    WHERE customer_id = %s
    ORDER BY date_paid DESC
""", (user_id,))
paid_orders = cursor.fetchall()


# Unpaid Orders
st.subheader("Unpaid Orders")
if not unpaid_orders:
    st.info("You have no unpaid orders.")
else:
    for order in unpaid_orders:
        with st.expander(f"Order #{order['order_id']} • Total: ${order['total_price']:.2f} • Date: {order['order_date']}"):
            cursor.execute("""
                SELECT p.description, ol.quantity, ol.price
                FROM order_lines ol
                JOIN products p ON ol.product_id = p.product_id
                WHERE ol.order_id = %s
            """, (order['order_id'],))
            items = cursor.fetchall()

            for item in items:
                st.write(f"{item['description']} x{item['quantity']} @ ${item['price']:.2f}")

            if st.button("Pay now", key=f"pay_{order['order_id']}"):
                try:
                    cursor.callproc("create_payment", (order['order_id'],))
                    conn.commit()
                    st.success(f"Order #{order['order_id']} marked as paid.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Payment failed: {e}")


# Paid Orders
st.subheader("Completed Orders")
if not paid_orders:
    st.info("No completed orders yet.")
else:
    for order in paid_orders:
        with st.expander(f"Order #{order['order_id']} • Paid: {order['date_paid']} • Total: ${order['total_price']:.2f}"):
            cursor.execute("""
                SELECT p.description, ol.quantity, ol.price
                FROM order_lines ol
                JOIN products p ON ol.product_id = p.product_id
                WHERE ol.order_id = %s
            """, (order['order_id'],))
            items = cursor.fetchall()

            for item in items:
                st.write(f"{item['description']} x{item['quantity']} @ ${item['price']:.2f}")

conn.close()
