import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Cycle de modélisation")

tab_ctr, tab_opt, tab_dt, tab_rf, tab_gb, tab_cb = st.tabs(["Contraintes", "Optimisation d'hyperparamètres", "Decision Tree", "Random Forests", "Gradient Boosting", "CatBoost"])

with tab_ctr:
    comp.subheader("Rappel du cadre")
    st.markdown("- ##### Données tabulaires")
    st.markdown("- ##### Données essentiellement catégorielles")
    st.markdown("- ##### Recherche d'un modèle explicable")
    st.markdown("- ##### Temps et moyens matériels limités")

    comp.subheader("Stratégie")
    st.markdown("##### Tous ces éléments amènent aux choix d'algorithmes basés sur les arbres de décision")
    st.markdown("- ##### 1. Modèle simple : Decision Tree")
    st.markdown("- ##### 2. Aggrégation de modèles simples : Random Forests")
    st.markdown("- ##### 3. Méthode de Boosting : Gradient Boosting Clssifier")
    st.markdown("- ##### 4. Algorithme de Boosting spécifique aux données catégorielles : CatBoost")

with tab_dt:
    comp.subheader("Decision Tree")

with tab_rf:
    comp.subheader("Random Forest")

with tab_gb:
    comp.subheader("Gradient Boosting")

with tab_cb:
    comp.header("CatBoost")
