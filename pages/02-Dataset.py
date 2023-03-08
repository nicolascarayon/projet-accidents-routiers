import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Dataset")

tab1, tab2, tab3 = st.tabs(["Description", "Modèle relationnel", "Entités"])

with tab1:
    comp.subheader("Description")
    # st.markdown("---")
    st.markdown("- ##### 4 types de fichiers .csv : usagers / caractéristiques des accidents / lieux / véhicules")
    st.markdown("- ##### pour chaque type, 1 fichier csv / an de 2005 à 2021")
    st.markdown("- ##### gravité : variable des fichiers *usagers* (4 modalités : Indemne, Blessé léger, Blessé hospitalisé, Tué)")
    st.markdown("- ##### Volumétrie : 342 Mo")

with tab2:
    comp.subheader("Modèle relationnel")
    st.image("./pics/model-relational.jpg", width=600)

with tab3:
    import pandas as pd
    import numpy as np
    import time
    from pages.libs import utils

    comp.subheader("Entités")

    cols = st.columns(8)
    file_type = cols[0].selectbox(label="Type de fichier", options=('usagers', 'accidents', 'lieux', 'véhicules'))
    year_sel  = cols[1].selectbox(label="Année", options=range(2005, 2022))
    print(file_type)
    print(year_sel)
    with st.spinner('Wait for it...'):
        data_dic = utils.get_DataFrame(file_type, year_sel)
    df = data_dic[year_sel]
    st.dataframe(df)