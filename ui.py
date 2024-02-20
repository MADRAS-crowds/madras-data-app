import streamlit as st
from pathlib import Path


def setup_app() -> None:
    """Set up the Streamlit page configuration."""
    st.set_page_config(
        page_title="Madras Project",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/PedestrianDynamics/madras-data-app",
            "Report a bug": "https://github.com/PedestrianDynamics/madras-data-app//issues",
            "About": "# Field observation for Madras project.\n This is a tool to analyse and visualise several field data of pedestrian dynamics during the festival of lights in 2022:\n\n :flag-fr: - :flag-de: Germany.",
        },
    )
    st.title("Madras project: Festival of light 2022")


def init_app_looks():
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute()

    gh = "https://badgen.net/badge/icon/GitHub?icon=github&label"
    repo = "https://github.com/PedestrianDynamics/madras-data-app"
    repo_name = f"[![Repo]({gh})]({repo})"
    c1, c2 = st.sidebar.columns((1.2, 0.5))
    c2.markdown(repo_name, unsafe_allow_html=True)
    c1.write(
        "[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7697604.svg)](https://doi.org/10.5281/zenodo.7697604)"
    )
    st.sidebar.image(f"{ROOT_DIR}/logo.png", use_column_width=True)


def init_sidebar():
    """Init sidebar and 3 tabs."""
    c1, c2 = st.sidebar.columns((1.8, 0.2))
    flag = c2.empty()
    tab1, tab2, tab3 = st.tabs(
        [
            "🗺️ Map",
            "👫🏻 View trajectories",
            "📉 Analysis",
        ]
    )

    # country = c1.selectbox("Select a country:", st.session_state.config.countries)
    # if "jap" in country:
    #     flag.write(":flag-jp:")
    # if "aus" in country:
    #     flag.write(":flag-ac:")
    # if "chn" in country:
    #     flag.write(":flag-cn:")
    # if "ger" in country:
    #     flag.write(":flag-de:")
    # if "pal" in country:
    #     flag.write(":flag-ps:")

    return tab1, tab2, tab3
