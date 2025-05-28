import streamlit as st


st.set_page_config(
    page_title="Main",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Now import other Streamlit-dependent modules
from st_pages import add_page_title, get_nav_from_toml

import os

currentDir = os.getcwd()
toml_path = os.path.join(currentDir, "pages_sections.toml")

nav = get_nav_from_toml("pages_sections.toml")
if nav:
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()
else:
    st.write("No pages to show")