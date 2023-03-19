import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Contexte")
st.markdown("---")

comp.subheader("Source de données")
st.markdown("""
            ##### Fichier BAAC : *Base de données Annuelles des Accidents Corporels de la circulation routière (2005 à 2021)*
            - géré par l'ONISR (Observatoire National Interministeriel de la Sécurité Routière)
            - recense tous les accidents corporels de la circulation routière survenus sur le territoire français
            - utilisé par l'ONISR pour analyser les tendances de l'accidentologie routière afin d'élaborer des politiques de sécurité routière plus efficaces
            - disponible sur data.gouv.fr : https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/
            - documentation : https://www.data.gouv.fr/fr/datasets/r/8ef4c2a3-91a0-4d98-ae3a-989bde87b62a
            """)

comp.subheader("Objectifs")
st.markdown("""
            - ##### Construire des prédicteurs de gravité d'accident
            - ##### Comparer leurs performances 
            - ##### Mettre en évidence et comprendre l'origine de leurs limites
            """)

# comp.subheader("Variable cible")
# st.markdown("""
#             - ##### Gravité des blessures subies par un usager de la route impliqué dans un accident
#             """)