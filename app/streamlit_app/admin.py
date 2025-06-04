import streamlit as st
from admin_tabs.user_management import display_user_management
from admin_tabs.product_management import display_product_management
from admin_tabs.admin_statistics import display_statistics

if "username" not in st.session_state:
    st.warning("You must be logged in to access this page.")
else:
    if st.session_state.username != "admin":
        st.warning("You must be an admin to access this page.")
    else:
        tabs = st.tabs(["Statistics", "Manage Products", "Manage Users"])

        with tabs[0]:
            display_statistics()
        with tabs[1]:
            display_product_management()
        with tabs[2]:
            display_user_management()

