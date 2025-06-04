import streamlit as st
from streamlit_app.productPage import get_products
from database.db_functionality.product_functionality import (
    update_product, create_product, soft_delete_product
)

def display_product_management():

    DEFAULT_ITEMS_PER_PAGE = 10
    PAGE_SIZE_OPTIONS = [10, 25, 50]

    if "admin_items_per_page" not in st.session_state:
        st.session_state.admin_items_per_page = DEFAULT_ITEMS_PER_PAGE
    if "admin_search_filter" not in st.session_state:
        st.session_state.admin_search_filter = ""
    if "admin_current_anchor" not in st.session_state:
        st.session_state.admin_current_anchor = ""
    if "admin_products" not in st.session_state:
        st.session_state.admin_products, st.session_state.admin_has_next = get_products(
            st.session_state.admin_items_per_page,
            st.session_state.admin_current_anchor,
            st.session_state.admin_search_filter,
            "next"
        )
        st.session_state.admin_has_prev = False
    if "admin_chosen_product" not in st.session_state:
        st.session_state.admin_chosen_product = None

    st.subheader("Product Management")

    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search products by description", st.session_state.admin_search_filter)
    with col2:
        page_size = st.selectbox("Items per page", PAGE_SIZE_OPTIONS, index=PAGE_SIZE_OPTIONS.index(st.session_state.admin_items_per_page))

    if search != st.session_state.admin_search_filter or page_size != st.session_state.admin_items_per_page:
        st.session_state.admin_search_filter = search
        st.session_state.admin_items_per_page = page_size
        st.session_state.admin_current_anchor = ""
        st.session_state.admin_products, st.session_state.admin_has_next = get_products(
            st.session_state.admin_items_per_page,
            "",
            st.session_state.admin_search_filter,
            "next"
        )
        st.session_state.admin_has_prev = False
        st.rerun()

    col1, _, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("Prev", disabled=not st.session_state.admin_has_prev):
            first_id = st.session_state.admin_products[0]["product_id"]
            products, has_more = get_products(
                st.session_state.admin_items_per_page,
                first_id,
                st.session_state.admin_search_filter,
                "prev"
            )
            st.session_state.admin_products = products
            st.session_state.admin_has_prev = has_more
            st.session_state.admin_has_next = True
            st.session_state.admin_current_anchor = products[0]["product_id"]
            st.rerun()

    with col3:
        if st.button("Next", disabled=not st.session_state.admin_has_next):
            last_id = st.session_state.admin_products[-1]["product_id"]
            products, has_more = get_products(
                st.session_state.admin_items_per_page,
                last_id,
                st.session_state.admin_search_filter,
                "next"
            )
            st.session_state.admin_products = products
            st.session_state.admin_has_prev = True
            st.session_state.admin_has_next = has_more
            st.session_state.admin_current_anchor = products[0]["product_id"]
            st.rerun()

    if st.session_state.admin_chosen_product == None:
        
        for product in st.session_state.admin_products:
            st.write(f"**#{product['product_id']} - {product['description']}** (${product['price']})")
            cols = st.columns([1, 1])
            if cols[0].button("Edit", key=f"edit_{product['product_id']}"):
                st.session_state.admin_chosen_product = product
                st.rerun()
            if cols[1].button("Delete", key=f"del_{product['product_id']}"):
                if soft_delete_product(product['product_id']):
                    st.success("Product deleted.")
                    st.session_state.admin_search_filter = search
                    st.session_state.admin_items_per_page = page_size
                    st.session_state.admin_current_anchor = ""
                    st.session_state.admin_products, st.session_state.admin_has_next = get_products(
                    st.session_state.admin_items_per_page,
                    "",
                    st.session_state.admin_search_filter,
                    "next"
                    )
                    st.session_state.admin_has_prev = False
                    st.rerun()
                else:
                    st.error("Failed to delete product.")

    if st.session_state.admin_chosen_product:
        st.markdown("---")
        st.subheader("Edit Product")
        product = st.session_state.admin_chosen_product

        new_desc = st.text_input("Description", value=product["description"], key="desc")
        new_price = st.number_input("Price", min_value=0.0, value=float(product["price"]), key="price")

        if st.button("Save Changes"):
            if update_product(product["product_id"], new_desc, new_price):
                st.success("Product updated.")
                st.session_state.admin_chosen_product = None
                st.session_state.admin_search_filter = search
                st.session_state.admin_items_per_page = page_size
                st.session_state.admin_current_anchor = ""
                st.session_state.admin_products, st.session_state.admin_has_next = get_products(
                st.session_state.admin_items_per_page,
                "",
                st.session_state.admin_search_filter,
                "next"
                )
                st.session_state.admin_has_prev = False
                st.rerun()
            else:
                st.error("Update failed.")

    st.markdown("---")
    st.subheader("Create New Product")

    new_description = st.text_input("New Product Description")
    new_price = st.number_input("New Product Price", min_value=0.0)

    if st.button("Create Product"):
        if create_product(new_description, new_price):
            st.success("Product created.")
            st.rerun()
        else:
            st.error("Failed to create product.")
