import streamlit as st
from pages.libs import comp

comp.sidebar_info()

objective = """
            - ##### Construire des prédicteurs de gravité d'accident
            - ##### Comparer leurs performances 
            - ##### Mettre en évidence leurs limites
            """
def_gravite =   """
                ##### Gravité des blessures subies par un usager de la route impliqué dans un accident
                """
source_data =   """
                ##### Fichier BAAC : *Base de données Annuelles des Accidents Corporels de la circulation routière (2005 à 2021)*
                """

comp.header("Contexte")
st.markdown("---")
comp.subheader("Objectifs")
st.markdown(objective)

comp.subheader("Source de données")
st.markdown(source_data)

comp.subheader("Variable cible")
st.markdown(def_gravite)



