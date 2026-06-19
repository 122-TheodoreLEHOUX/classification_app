import streamlit as st
import pandas as pd
from request_db import db_connection
from data_handling import data_handler


st.title("Classification app")
st.markdown("Bienvenue sur l'app de classification de l'expertise")


# Initialize DB and handler
conn = db_connection()
handler = data_handler(conn)


# Side bar definition (basic filters)
side_bar_comp = st.sidebar
side_bar_comp.header("Filtres")
side_bar_comp.selectbox("Reference", options=["All"] + conn.get_data().get("Reference", []).dropna().unique().tolist())
side_bar_comp.selectbox("Designation", options=["All"] + conn.get_data().get("Designation", []).dropna().unique().tolist())
side_bar_comp.selectbox("Project", options=["All"] + conn.get_data().get("Project", []).dropna().unique().tolist())


if "df" not in st.session_state:
    # load from DB
    df = handler.load()
    if df is None or df.empty:
        df = pd.DataFrame(columns=conn.columns)
    st.session_state.df = df

# Show editable table
edited = st.data_editor(
    st.session_state.df,
    num_rows="dynamic",
    key="df_editor",
)

st.session_state.df = edited

if st.button("Save to DB"):
    try:
        handler.update(st.session_state.df)
        st.success("Saved to local DB.")
    except Exception as e:
        st.error(f"Error saving data: {e}")