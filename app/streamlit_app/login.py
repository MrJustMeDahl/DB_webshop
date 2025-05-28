import streamlit as st
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        port=7003,
        user="root",
        password="rootpassword",
        database="webshop_db"
    )

def login(username, password):
    conn = connect_db()
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
