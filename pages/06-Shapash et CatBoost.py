import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Explicabilité du modèle Catboost à l'aide de la librairie Shapash")

tab_shap, tab_app_cb = st.tabs(["Valeurs de SHAP", "Application sur CatBoost"])

with tab_shap:
    comp.subheader("Valeurs de Shap")
    st.markdown("- ##### Mesure de la contribution de chaque variable dans la prédiction finale")
    st.markdown("- ##### Pour chaque donnée les valeurs de SHAP mesurent la contribution marginale de chaque caractéristique à la différence entre la prédiction moyenne du modèle et la prdiction individuelle pour la donnée en question")

    comp.subheader("Shapash")
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("- ##### Bibliothèque open source développée par une équipe de Data Scientists de la MAIF")
        st.markdown("- ##### Met en oeuvre les valeurs de Shapley pour fournir des tableaux interactifs aidant à la compréhension des modèles")
        st.markdown("- ##### Facilite les discussions avec le métier")
    with col2:
        st.image("./pics/shapash-logo.png", width=150)
    with col3:
        st.image("./pics/logo-maif.png", width=150)

with tab_app_cb:
    comp.subheader("...")
    from joblib import load
    import joblib as joblib
    st.write(help(joblib.load))
    model = load("./h5_models/model_cb_prd_64000.h5")
