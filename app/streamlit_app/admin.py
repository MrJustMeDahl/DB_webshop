import streamlit as st
from database.db_functionality.user_functionality import find_active_by_id, update_username_password, soft_delete_user

if "username" not in st.session_state:
    st.warning("You must be logged in to access this page.")
else:
    if st.session_state.username != "admin":
        st.warning("You must be an admin to access this page.")
    else:
        tabs = st.tabs(["Statistics", "Manage Products", "Manage Users", "View Orders"])

        with tabs[0]:
            st.write("Statistics will be displayed here.")
        with tabs[1]:
            st.write("Product management features will be implemented here.")
        with tabs[2]:
            st.subheader("User Management")
            user_id = st.text_input("Enter User ID to find user details:")
            if user_id:
                user = find_active_by_id(user_id)
                if user:
                    st.session_state.chosen_user = user['customer_id']
                else:
                    st.error("User not found.")
            else:
                st.info("Please enter a User ID to search.")

            if st.session_state.get("chosen_user"):
                user_tabs = st.tabs(["User Details", "Edit User", "Delete User"])
                with user_tabs[0]:
                    st.write(f"User ID: {st.session_state.chosen_user}")
                    st.write(f"Username: {user['username']}")
                with user_tabs[1]:
                    new_username = st.text_input("New Username", value=user['username'])
                    new_password = st.text_input("New Password", type="password")
                    if st.button("Update User"):
                        update_result = update_username_password(st.session_state.chosen_user, new_username, new_password)
                        if update_result == "no_changes":
                            st.info("No changes were made.")
                        elif update_result:
                            st.success("User updated successfully.")
                            user = update_result
                        else:
                            st.error("Failed to update user.")
                with user_tabs[2]:
                    st.write("Are you sure you want to delete this user?")
                    if st.button("Delete User"):
                        if soft_delete_user(st.session_state.chosen_user):
                            st.success("User deleted successfully.")
                            st.session_state.chosen_user = None
                            st.rerun()
                        else:
                            st.error("Failed to delete user.")
        with tabs[3]:
            st.write("Order management features will be implemented here.")