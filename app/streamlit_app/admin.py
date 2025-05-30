import streamlit as st

if "username" not in st.session_state:
    st.warning("You must be logged in to access this page.")
else:
    if st.session_state.username != "admin":
        st.warning("You must be an admin to access this page.")
    else:
        st.write("Welcome to the admin dashboard.")