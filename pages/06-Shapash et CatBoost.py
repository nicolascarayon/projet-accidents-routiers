import streamlit as st
import my_libs.ref_labels as refs
from pages.libs import comp, utils

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
    # import joblib as joblib
    model = load("./h5_models/model_cb_prd_64000x10.h5")


    fields = ['dep', 'catv', 'catr', 'col', 'agg', 'trajet', 'mois', 'catu', 'situ', 'place']

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dep = st.selectbox(label="Département", options=utils.get_dep_list(), key='sb_dep')

        catv_val = st.selectbox(label="Catégorie de véhicule", options=list(refs.dic_catv.values()), key='sb_catv')
        catv_key = refs.get_key_from_value(refs.dic_catv, catv_val)
        # st.write(catv_key)

        catr_val = st.selectbox(label="Catégorie de route", options=list(refs.dic_catr.values()), key='sb_catr')
        catr_key = refs.get_key_from_value(refs.dic_catr, catr_val)
        # st.write(catr_key)

        col_val = st.selectbox(label="Type de collision", options=list(refs.dic_col.values()), key='sb_col')
        col_key = refs.get_key_from_value(refs.dic_col, col_val)
        # st.write(col_key)

    with col2:
        agg_val = st.selectbox(label="Localisation", options=list(refs.dic_agg.values()), key='sb_agg')
        agg_key = refs.get_key_from_value(refs.dic_agg, agg_val)
        # st.write(agg_key)

        trajet = st.text_input('trajet', key='6', value=1)

    with col3:
        mois   = st.text_input('mois',   key='7', value=1)
        catu   = st.text_input('catu',   key='8', value=1)

    with col4:
        situ   = st.text_input('situ',   key='9', value=1)
        place  = st.text_input('place',  key='10',value=1)






    X = [dep, catv_key, catr_key, col_key, agg_key, trajet, mois, catu, situ, place]

    predict = st.button("Predict")
    if predict:
        y_pred = model.predict(X)
        st.write(y_pred)
#%%
