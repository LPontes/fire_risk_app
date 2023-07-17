import streamlit as st
from streamlit_option_menu import option_menu
from apps import incendio, clima, upload  # import your app modules here

st.set_page_config(page_title="Suzano Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": incendio.app, "title": "Risco de Incêndio", "icon": "bi bi-fire"},
    {"func": clima.app, "title": "Riscos Climáticos", "icon": "bi bi-thermometer-snow"}
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        Esse web app foi criado por [Lucas Pontes](https://github.com/LPontes) para o processo seletivo de pesquisador sênior na Suzano
            
        Source code: <https://github.com/LPontes/streamlit_demo>
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
