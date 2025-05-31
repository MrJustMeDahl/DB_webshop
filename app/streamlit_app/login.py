import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql

def login(username, password):
    conn = connect_mysql()
    if not conn:
        return False
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT customer_id, username FROM customer WHERE username=%s AND password=%s AND is_active=TRUE", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        st.session_state.logged_in = True
        st.session_state.username = user["username"]
        st.session_state.user_id = user["customer_id"]
        return True
    return False


with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        if login(username, password):
            st.success("Login successful!")

            st.info("You can now add items to your cart and make purchases.")
        else:
            st.error("Invalid username or password.")
