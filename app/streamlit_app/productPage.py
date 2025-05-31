import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql
from database.db_functionality.redis_functionality import (
    get_cached_products, cache_products, get_redis_connection, add_to_cart
)
import json

DEFAULT_ITEMS_PER_PAGE = 10
PAGE_SIZE_OPTIONS = [10, 25, 50]

def get_products(limit, anchor_id, search_filter, direction):
    normalized_filter = (search_filter or "").strip().lower()
    cache_key = f"products:{normalized_filter}:{anchor_id}:{direction}:{limit}"

    cached_products, has_more = get_cached_products(cache_key)
    if cached_products is not None:
        return cached_products, has_more

    conn = connect_mysql()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "CALL pagination(%s, %s, %s, %s)",
        (limit + 1, anchor_id, search_filter, direction)
    )
    result = cursor.fetchall()
    conn.close()

    has_more = len(result) > limit
    products = result[:limit]

    if direction == "prev":
        products.reverse()

    cache_products(cache_key, products, has_more)
    return products, has_more


# Session state init
if "items_per_page" not in st.session_state:
    st.session_state.items_per_page = DEFAULT_ITEMS_PER_PAGE
if "search_filter" not in st.session_state:
    st.session_state.search_filter = ""
if "current_anchor" not in st.session_state:
    st.session_state.current_anchor = ""
if "products" not in st.session_state:
    st.session_state.products, st.session_state.has_next = get_products(
        st.session_state.items_per_page,
        st.session_state.current_anchor,
        st.session_state.search_filter,
        "next"
    )
    st.session_state.has_prev = False

# UI: Search + pagination
col1, col2 = st.columns([2, 1])
with col1:
    search = st.text_input("Search description", st.session_state.search_filter)
with col2:
    page_size = st.selectbox("Items per page", PAGE_SIZE_OPTIONS, index=PAGE_SIZE_OPTIONS.index(st.session_state.items_per_page))

if search != st.session_state.search_filter or page_size != st.session_state.items_per_page:
    st.session_state.search_filter = search
    st.session_state.items_per_page = page_size
    st.session_state.current_anchor = ""
    st.session_state.products, st.session_state.has_next = get_products(
        st.session_state.items_per_page,
        "",
        st.session_state.search_filter,
        "next"
    )
    st.session_state.has_prev = False
    st.rerun()

col_prev, _, col_next = st.columns([1, 8, 1])
with col_prev:
    if st.button("Prev", disabled=not st.session_state.has_prev):
        first_id = st.session_state.products[0]["product_id"]
        products, has_more = get_products(
            st.session_state.items_per_page,
            first_id,
            st.session_state.search_filter,
            "prev"
        )
        st.session_state.products = products
        st.session_state.has_prev = has_more
        st.session_state.has_next = True 
        st.session_state.current_anchor = products[0]["product_id"]
        st.rerun()

with col_next:
    if st.button("Next", disabled=not st.session_state.has_next):
        last_id = st.session_state.products[-1]["product_id"]
        products, has_more = get_products(
            st.session_state.items_per_page,
            last_id,
            st.session_state.search_filter,
            "next"
        )
        st.session_state.products = products
        st.session_state.has_prev = True
        st.session_state.has_next = has_more
        st.session_state.current_anchor = products[0]["product_id"]
        st.rerun()

# Cart
redis_conn = get_redis_connection()
if not redis_conn:
    st.stop()

if "username" not in st.session_state:
    st.write("You must be logged in to add items to the cart.")
    cart_key = None
else:
    username = st.session_state["username"]
    cart_key = f"cart:{username}"

# Display products
with st.container():
    cols2 = st.columns([5, 5])
    for index, product in enumerate(st.session_state.products):
        col = cols2[0] if index % 2 == 0 else cols2[1]
        with col:
            cols = st.columns([2, 3])
            with cols[0]:
                st.image("./ressources/placeholder.png", use_container_width=True)
            with cols[1]:
                st.subheader(product['description'])
                st.write(f"**Price:** ${product['price']}")
                st.write(f"Product # {product['product_id']}")

                if st.button("Add to cart", key=f"add_{product['product_id']}"):
                    if cart_key:
                        add_to_cart(redis_conn, cart_key, product["product_id"])
                        st.success(f"Added product #{product['product_id']} to cart!")
                    else:
                        st.error("You must be logged in to add items to the cart.")

                if st.button("View product details", key=f"view_product_{index}"):
                    st.session_state.chosen_product = product
                    st.session_state.review_page = 0
                    st.success("Navigate to Product page to view details!")

            st.markdown("---")
