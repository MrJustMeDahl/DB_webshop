import streamlit as st


st.set_page_config(
    page_title="Main",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Now import other Streamlit-dependent modules
from st_pages import add_page_title, get_nav_from_toml


import os

base_dir = os.path.dirname(__file__)
toml_path = os.path.join(base_dir, "pages_sections.toml")
nav = get_nav_from_toml(toml_path)
if nav:
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()
else:
    st.write("No pages to show")