import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Data Viz")

tab1, tab2, tab3 = st.tabs(["Données manquantes", "Relations gravité-variables", "..."])

with tab1:
    st.markdown("##### Heatmap des données manquantes")
    # st.markdown("##### Avant traitement :")
    chk_proc = st.checkbox("Suppression des variables avec plus de 8% de données manquantes")
    if chk_proc:
        st.image("./pics/null_in_data_aft_proc.jpg", width=1200)
    else:
        st.image("./pics/null_in_data_bef_proc.jpg", width=1200)

with tab2:
    comp.subheader("Heatmap des intercorrélations")
    st.image("./pics/corr-vars-heatmap.jpg", width=600)

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