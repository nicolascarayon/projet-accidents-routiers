import streamlit as st
from pages.libs import comp

st.set_page_config(
    page_title="Projet Accidents Routiers",
    layout="wide"
)

import pages.libs.comp as comp
comp.sidebar_info()

st.markdown("---")
col1, col2 = st.columns([1, 4])
with col1:
    st.image("./pics/logo_datascientest.png", width=200)
with col2:
    comp.header("Projet - Parcours Data Scientist")
    st.subheader("Bootcamp Data Scientist - DEC22")
st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    st.header("Application du Machine Learning dans le cadre de la")
    st.header("prédiction de gravité d'accidents routiers")
with col2:
    st.image("./pics/CarCrash2.jpg", width=400)


