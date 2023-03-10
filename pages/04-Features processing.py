import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Features processing")

tab1, tab2, tab3 = st.tabs(["Données manquantes", "Relations gravité-variables", "Distributions  conditionnelles"])

with tab1:
    comp.header("tab1")

with tab2:
    comp.header("tab2")

with tab3:
    comp.header("tab3")