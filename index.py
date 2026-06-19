import streamlit as st
import pandas as pd
from request_db import db_connection

# connexion = db_connection()


st.title("Classification app")

st.markdown("Bienvenue sur l'app de classification de l'expertise")


# Side bar definition
side_bar_comp = st.sidebar
side_bar_comp.header("Filtres")
side_bar_comp.selectbox("Références",["1","2"])
side_bar_comp.selectbox("Désignations",["1","2"])
side_bar_comp.selectbox("Projets",["1","2"])
# side_bar_comp.select_slider("Dates")



if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(
        [],
        columns=["a", "b", "c"],
    )

st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    key="df_editor",
    disabled=["c"],
)