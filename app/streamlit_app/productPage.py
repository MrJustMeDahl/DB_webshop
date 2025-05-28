import streamlit as st
import mysql.connector

# DB config
DB_HOST = "localhost"
DB_PORT = 7003
DB_USER = "root"
DB_PASSWORD = "rootpassword"
DB_NAME = "webshop_db"



# Connect to DB
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Count total number of products
def get_total_product_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Fetch products for a specific page
def get_products(offset, limit):
    conn = connect_db()
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

for product in products:
    with st.container():
        cols = st.columns([3, 7])
        with cols[0]:
            st.image("./ressources/placeholder.png", use_container_width=True)
        with cols[1]:
            st.subheader(f"Product #{product['product_id']}")
            st.write(f"**Price:** ${product['price']}")
            st.write(product["description"])
            if st.button(f"Add to cart - {product['product_id']}"):
                st.success(f"Added product #{product['product_id']} to cart!")
    st.markdown("---")
