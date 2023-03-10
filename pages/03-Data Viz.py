import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Data Viz")

tab1, tab2, tab3 = st.tabs(["Données manquantes", "Relations gravité-variables", "Distributions  conditionnelles"])

with tab1:
    st.markdown("##### Heatmap des données manquantes")
    chk_proc = st.checkbox("Suppression des variables avec plus de 8% de données manquantes")
    if chk_proc:
        st.image("./pics/null_in_data_aft_proc.jpg", width=1200)
    else:
        st.image("./pics/null_in_data_bef_proc.jpg", width=1200)

with tab2:
    comp.subheader("Heatmap des intercorrélations")
    st.image("./pics/corr-vars-heatmap.jpg", width=600)

with tab3:
    cols = st.columns(6)
    var_sel = cols[0].selectbox(label="Variable", options=('jour de la semaine', 'département'))
    if var_sel == 'jour de la semaine':
        st.image("./pics/grav-joursem.png")
    else:
        st.image("./pics/grav-dep.png")
