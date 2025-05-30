import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql

# Ensure login
if "username" not in st.session_state:
    st.error("Please log in to view your orders.")
    st.stop()

conn = connect_mysql()
if not conn:
    st.error("Could not connect to database.")
    st.stop()

cursor = conn.cursor(dictionary=True)
username = st.session_state["username"]

# Fetch unpaid orders
cursor.execute("""
    SELECT * FROM unpaid_orders_view
    WHERE customer_id = (SELECT customer_id FROM customer WHERE username = %s)
""", (username,))
unpaid_orders = cursor.fetchall()

# Fetch paid orders
cursor.execute("""
    SELECT * FROM paid_orders_view
    WHERE customer_id = (SELECT customer_id FROM customer WHERE username = %s)
    ORDER BY date_paid DESC
""", (username,))
paid_orders = cursor.fetchall()


# Unpaid Orders
st.subheader("Unpaid Orders")
if not unpaid_orders:
    st.info("You have no unpaid orders.")
else:
    for order in unpaid_orders:
        with st.container():
            st.markdown("----")
            cols = st.columns([6, 2])
            with cols[0]:
                st.markdown(f"""
                    **Order #{order['order_id']}**  
                    Date: `{order['order_date']}`  
                    Total: **${order['total_price']:.2f}**
                """)
            with cols[1]:
                if st.button("Pay now", key=f"pay_{order['order_id']}"):
                    try:
                        cursor.callproc("create_payment", (order['order_id'],))
                        conn.commit()
                        st.success(f"Order #{order['order_id']} marked as paid.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Payment failed: {e}")

st.subheader("Completed Orders")
if not paid_orders:
    st.info("No completed orders yet.")
else:
    for order in paid_orders:
        with st.container():
            st.markdown("----")
            st.markdown(f"""
                **Order #{order['order_id']}**  
                Ordered: `{order['order_date']}`  
                Paid: `{order['date_paid']}`  
                Total: **${order['total_price']:.2f}**
            """)

conn.close()
