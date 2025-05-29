import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql



def login(username, password):
    conn = connect_mysql()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Streamlit UI
st.title("Login")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.info("Now navigate to 'Document Manager' from the sidebar.")
        else:
            st.error("Invalid username or password.")
