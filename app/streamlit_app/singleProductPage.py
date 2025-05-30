import streamlit as st
from database.db_connectors.connect_mysql import connect_mysql
from database.db_connectors.connect_mongodb import connect_mongodb
from database.db_connectors.connect_redis import connect_redis
from bson import ObjectId

REVIEWS_PER_PAGE = 3


def get_paginated_review_details(product_id, limit, offset):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT review_id, rating, username 
        FROM reviews_for_product 
        WHERE product_id = %s 
        LIMIT %s OFFSET %s
    """, (product_id, limit, offset))
    result = cursor.fetchall()
    conn.close()
    return result


def get_total_review_count(product_id):
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM reviews_for_product 
        WHERE product_id = %s
    """, (product_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_reviews_for_product(review_ids):
    if not review_ids:
        return []

    client = connect_mongodb()
    db = client["webshop_db"]
    collection = db["reviews"]

    object_ids = [ObjectId(rid.strip()) for rid in review_ids if ObjectId.is_valid(rid.strip())]
    if not object_ids:
        return []

    return list(collection.find({"_id": {"$in": object_ids}}))


if "chosen_product" in st.session_state:
    product = st.session_state.chosen_product

    redis_conn = connect_redis()
    if not redis_conn:
        st.stop()
    cart_key = None
    if "username" not in st.session_state:
        st.write("You must be logged in to add items to the cart.")
    else:
        username = st.session_state["username"]
        cart_key = f"cart:{username}"

    if "review_page" not in st.session_state:
        st.session_state.review_page = 0

    st.title(product["description"])

    cols = st.columns([2, 3])
    with cols[0]:
        st.image("./ressources/placeholder.png", use_container_width=True)
    with cols[1]:
        st.subheader(product['description'])
        st.write(f"**Price:** ${product['price']}")
        st.write(f"Product # {product['product_id']}")
        if st.button("Add to cart", key=f"add_{product['product_id']}"):
            if st.session_state.get("username") is None:
                st.error("You must be logged in to add items to the cart.")
            else:
                redis_conn.hincrby(cart_key, product["product_id"], 1)
                redis_conn.expire(cart_key, 3600)  
                st.success(f"Added product #{product['product_id']} to cart!")

    st.markdown("---")
    st.header("Customer Reviews")

    total_reviews = get_total_review_count(product["product_id"])
    offset = st.session_state.review_page * REVIEWS_PER_PAGE
    review_details = get_paginated_review_details(product["product_id"], REVIEWS_PER_PAGE, offset)

    if review_details:
        review_meta_map = {
            str(row[0]): {
                "rating": row[1],
                "username": row[2]
            }
            for row in review_details
        }

        reviews = get_reviews_for_product(list(review_meta_map.keys()))

        for r in reviews:
            rid = str(r["_id"])
            meta = review_meta_map.get(rid, {})
            rating = meta.get("rating", "N/A")
            username = meta.get("username", "Unknown")

            with st.container():
                st.subheader(f"Rating: {rating}/5.0")
                st.write(r.get("review_text", "No text"))
                st.caption(f"By: {username}")
                st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.review_page > 0:
                if st.button("⬅️ Previous"):
                    st.session_state.review_page -= 1
                    st.rerun()
        with col3:
            if (st.session_state.review_page + 1) * REVIEWS_PER_PAGE < total_reviews:
                if st.button("Next ➡️"):
                    st.session_state.review_page += 1
                    st.rerun()

        with col2:
            current_page = st.session_state.review_page + 1
            total_pages = (total_reviews + REVIEWS_PER_PAGE - 1) // REVIEWS_PER_PAGE
            st.markdown(f"<p style='text-align:center;'>Page {current_page} of {total_pages}</p>", unsafe_allow_html=True)

    else:
        st.info("No reviews for this product yet.")
else:
    st.title("No product found")
