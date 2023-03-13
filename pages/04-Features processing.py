import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Features processing")

tab1, tab2, tab3 = st.tabs(["Données manquantes", "Relations gravité-variables", "Distributions  conditionnelles"])

with tab1:
    comp.header("Traitements")
    st.markdown("- ##### Suppression des variables considérées inutiles vis à vis du problème (adresse postale, coord; GPS, etc...)")
    st.markdown("- ##### Suppression des variables avec trop de valeurs *Null*")
    st.markdown("- ##### Ré-encodage de variables avec trop de modalités (ex : catégorie de véhicules passée de 40 à 7)")
    st.markdown("- ##### Target encoding de la variable *Département* (en raison du grand nombre de modalités)")
    st.markdown("- ##### One Hot Encoding de toutes les variables catégorielles")
    st.markdown("- ##### Ré-encodage de la cible en 2 modalités : 0 - Indemne/Blessé léger vs. 1 - Blessé hospitalisé/Tué")
    st.markdown("- ##### Ré-équilibrage des classes par algorithme SMOTE (Synthetic Minority Oversampling TEchnique)")

    col1, col2 = st.columns([1, 9])
    with col1:
        smote_principle   = st.checkbox("Principe")
    with col2:
        smote_application = st.checkbox("Application")

    if smote_principle   : st.image("./pics/smote-principle.png", width=500)
    if smote_application :  st.image("./pics/smote-application.png", width=500)

with tab2:
    comp.header("tab2")

with tab3:
    comp.header("tab3")