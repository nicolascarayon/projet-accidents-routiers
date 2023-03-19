import streamlit as st
from pages.libs import comp, utils

comp.sidebar_info()

comp.header("Features processing")

tab_trait, tab_dataset = st.tabs(["Traitements", "Dataset de travail"])

with tab_trait:
    comp.subheader("Traitements")
    st.markdown("- ##### Suppression des variables considérées inutiles vis à vis du problème (adresse postale, coord GPS, etc...)")
    st.markdown("- ##### Suppression des variables avec trop de valeurs *Null*")
    st.markdown("- ##### Ré-encodage de variables avec trop de modalités (ex : catégorie de véhicules passée de 40 à 7)")
    st.markdown("- ##### Target encoding de la variable *Département* (en raison du grand nombre de modalités)")
    st.markdown("- ##### One Hot Encoding de toutes les variables catégorielles")
    st.markdown("- ##### Ré-encodage de la cible en 2 modalités : *Non grave* (0) vs. *Grave* (1)")
    st.markdown("- ##### Ré-équilibrage des classes par algorithme SMOTE (Synthetic Minority Oversampling TEchnique)")

    exp_principle = st.expander("Principe")
    with exp_principle:
        st.image("./pics/smote-principle.png")

    exp_apply = st.expander("Application")
    with exp_apply:
        st.image("./pics/smote-application.png")


with tab_dataset:
    comp.header("Working Dataset")
    with st.spinner('Wait for it...'):
        df = utils.get_working_dataset()
        df.actp = df.actp.astype('int')
        df.age_cls = df.age_cls.astype('Int64')

    st.dataframe(df)

