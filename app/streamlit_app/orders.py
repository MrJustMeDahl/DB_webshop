import streamlit as st
from database.db_functionality.order_functionality import get_unpaid_orders, get_paid_orders, get_order_items, pay_order

if "username" not in st.session_state or "user_id" not in st.session_state:
    st.error("Please log in to view your orders.")
    st.stop()

user_id = st.session_state["user_id"]

st.subheader("Unpaid Orders")
unpaid_orders = get_unpaid_orders(user_id)

if not unpaid_orders:
    st.info("You have no unpaid orders.")
else:
    for order in unpaid_orders:
        with st.expander(f"Order #{order['order_id']}   -   Total: ${order['total_price']:.2f}   -   Date: {order['order_date']}"):
            items = get_order_items(order['order_id'])
            for item in items:
                st.write(f"{item['description']} x{item['quantity']} @ ${item['price']:.2f}")
            if st.button("Pay now", key=f"pay_{order['order_id']}"):
                if pay_order(order['order_id']):
                    st.success(f"Order #{order['order_id']} marked as paid.")
                    st.rerun()
                else:
                    st.error("Payment failed.")

st.subheader("Completed Orders")
paid_orders = get_paid_orders(user_id)

if not paid_orders:
    st.info("No completed orders yet.")
else:
    for order in paid_orders:
        with st.expander(f"Order #{order['order_id']} • Paid: {order['date_paid']} • Total: ${order['total_price']:.2f}"):
            items = get_order_items(order['order_id'])
            for item in items:
                st.write(f"{item['description']} x{item['quantity']} @ ${item['price']:.2f}")
