import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_redis import connect_redis


# DB config
DB_HOST = "localhost"
DB_PORT = 7003
DB_USER = "root"
DB_PASSWORD = "rootpassword"
DB_NAME = "webshop_db"



# Count total number of products
def get_total_product_count():
    conn = connect_mysql()
    if not conn:
        return 0
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Fetch products for a specific page
def get_products(offset, limit):
    conn = connect_mysql()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT product_id, description, price FROM products LIMIT %s OFFSET %s",
        (limit, offset)
    )
    products = cursor.fetchall()
    conn.close()
    return products

# Streamlit UI
st.title("Product Catalog")

# Pagination logic
total_products = get_total_product_count()

# Limiting the total products to 50 pr page
ITEMS_PER_PAGE = 50
total_pages = (total_products + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

# Track page number in session
if "page_number" not in st.session_state:
    st.session_state.page_number = 0

# Pagination controls
column_prev, col_space, next_column = st.columns([1, 8, 1])

with column_prev:
    if st.button("Prev") and st.session_state.page_number > 0:
        st.session_state.page_number -= 1

with next_column:
    if st.button("Next") and st.session_state.page_number < total_pages - 1:
        st.session_state.page_number += 1

# Show products
offset = st.session_state.page_number * ITEMS_PER_PAGE
products = get_products(offset, ITEMS_PER_PAGE)

st.markdown(f"### Showing {offset + 1} to {min(offset + ITEMS_PER_PAGE, total_products)} of {total_products} products")



redis_conn = connect_redis()
if not redis_conn:
    st.stop()

cart_key = None
if "username" not in st.session_state:
    st.write("You must be logged in to add items to the cart.")
else:
    username = st.session_state["username"]
    cart_key = f"cart:{username}"




for product in products:
    with st.container():
        cols = st.columns([3, 7])
        with cols[0]:
            st.image("ressources/placeholder.png", use_container_width=True)
        with cols[1]:
            st.subheader(f"{product['description']}")
            st.write(f"**Price:** ${product['price']}")
            st.write(f"Product ID: {product['product_id']}")
            if st.button("Add to cart", key=f"add_{product['product_id']}"):
                if st.session_state.get("username") is None:
                    st.error("You must be logged in to add items to the cart.")
                else:
                    redis_conn.hincrby(cart_key, product["product_id"], 1)
                    redis_conn.expire(cart_key, 3600)  
                    st.success(f"Added product #{product['product_id']} to cart!")




