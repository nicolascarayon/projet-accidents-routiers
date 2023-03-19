import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Dataset")

tab_desc, tab_mod_rel, tab_data_raw = st.tabs(["Description", "Modèle relationnel", "Données brutes"])

with tab_desc:
    comp.subheader("Description")
    # st.markdown("---")
    st.markdown("- ##### 4 types de fichiers .csv : usagers / caractéristiques des accidents / lieux / véhicules")
    st.markdown("- ##### pour chaque type, 1 fichier csv / an de 2005 à 2021")
    st.markdown("- ##### gravité : variable des fichiers *usagers* (4 modalités : Indemne, Blessé léger, Blessé hospitalisé, Tué)")
    st.markdown("- ##### Volumétrie : 342 Mo")

with tab_mod_rel:
    comp.subheader("Modèle relationnel")
    st.image("./pics/model-relational.jpg", width=600)

with tab_data_raw:
    from pages.libs import utils

    comp.subheader("Données brutes")

    cols = st.columns(8)
    file_type = cols[0].selectbox(label="Type de fichier", options=('usagers', 'accidents', 'lieux', 'véhicules'))
    year_sel  = cols[1].selectbox(label="Année", options=range(2005, 2022))

    with st.spinner('Wait for it...'):
        data_dic = utils.get_DataFrame(file_type, year_sel)
    df = data_dic[year_sel]

    st.dataframe(df)