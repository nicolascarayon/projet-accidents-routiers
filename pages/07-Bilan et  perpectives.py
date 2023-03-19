import pandas as pd
import streamlit as st
from pages.libs import comp, utils

comp.sidebar_info()

comp.header("Bilan et perspectives")
st.markdown("---")

comp.subheader("Du positif")
st.markdown("- ##### Expérience très riche sur le plan didactique (data explo, features processing, modélisation, développement, rapport, streamlit, etc...)")
st.markdown("- ##### Pistes d'amélioration des performances :")
col1, col2 = st.columns([1, 19])
with col2:
    st.markdown("- ##### Travailler sur données ultérieures à 2019 pour introduire les nouvelles variables (équipements de sécurité, limites de vitesse, etc...")
    st.markdown("- ##### Etudier la piste de l'Oversampling qui a peut être été trop rapidement écartée (on dispose de beaucoup d'accidents graves non utilisés dans l'entraînement du modèle)")
    st.markdown("- ##### Surveiller de très près l'introduction des nouvelles features issues des boîtes noires obligatoires sur les nouveaux véhicules depuis juillet 2022  \n"
                "##### (vitesse, phase d'accélération ou de freinage, port de la ceinture de sécurité, usage du clignotant, force de la collision, régime moteur.)")