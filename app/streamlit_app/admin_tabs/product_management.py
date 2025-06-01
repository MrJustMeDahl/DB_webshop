import streamlit as st


def display_product_management():
    st.subheader("Product Management")
    
    if "products" not in st.session_state:
        st.session_state.products = []
    
    if "search_filter" not in st.session_state:
        st.session_state.search_filter = ""
    
    search = st.text_input("Search products by description", value=st.session_state.search_filter)
    
    if search != st.session_state.search_filter:
        st.session_state.search_filter = search

    
    if st.session_state.products:
        for product in st.session_state.products:
            st.write(f"Product ID: {product['product_id']}, Description: {product['description']}")
    else:
        st.info("No products found.")
    
