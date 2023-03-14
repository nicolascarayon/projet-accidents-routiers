import pandas as pd
import streamlit as st
import my_libs.ref_labels as refs
from pages.libs import comp, utils
from joblib import load

comp.sidebar_info()

comp.header("Explicabilité du modèle Catboost à l'aide de la librairie Shapash")

tab_shap, tab_app_cb = st.tabs(["Valeurs de Shapley", "Application sur CatBoost"])

with tab_shap:
    comp.subheader("Valeurs de Shapley")
    st.markdown("- ##### Mesure de la contribution de chaque variable dans la prédiction finale")
    st.markdown("- ##### Pour chaque donnée les valeurs de Shapley mesurent la contribution marginale de chaque caractéristique à la différence entre la prédiction moyenne du modèle et la prdiction individuelle pour la donnée en question")

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


    col_btn, col_cb_acc_type, col_empty = st.columns([1,1, 6])
    with col_btn:
        acc_grav_only = st.checkbox(label="Accidents graves")
        model = load("./h5_models/model_cb_prd_64000x26.h5")
        data_test = pd.read_pickle("./pickles/df-prd-test.pkl")
        X_test = data_test.drop(columns=['grav'], axis=1)
        y_test = data_test.grav
        X_acc, y_acc, ind = utils.get_random_accident(X_test, y_test, acc_grav_only)

        st.session_state.sb_dep    = refs.dic_dep[int(X_acc.dep)]
        st.session_state.sb_catv   = refs.dic_catv[int(X_acc.catv)]
        st.session_state.sb_catr   = refs.dic_catr[int(X_acc.catr)]
        st.session_state.sb_col    = refs.dic_col[int(X_acc.col)]
        st.session_state.sb_agg    = refs.dic_agg[int(X_acc['agg'])]
        st.session_state.sb_trajet = refs.dic_trajet[int(X_acc.trajet)]
        st.session_state.sb_mois   = refs.dic_mois[int(X_acc.mois)]
        st.session_state.sb_catu   = refs.dic_catu[int(X_acc.catu)]
        st.session_state.sb_situ   = refs.dic_situ[int(X_acc.situ)]
        st.session_state.sb_place  = refs.dic_place[int(X_acc.place)]
    with col_cb_acc_type:
        if st.button('New accident'):
            st.experimental_rerun()

    col1, col2 = st.columns([1, 4])

    with col1:
        dep_val = st.selectbox(label="Département", options=list(refs.dic_dep.values()), key='sb_dep')
        dep_key = refs.get_key_from_value(refs.dic_dep, dep_val)

        catv_val = st.selectbox(label="Catégorie de véhicule", options=list(refs.dic_catv.values()), key='sb_catv')
        catv_key = refs.get_key_from_value(refs.dic_catv, catv_val)

        catr_val = st.selectbox(label="Catégorie de route", options=list(refs.dic_catr.values()), key='sb_catr')
        catr_key = refs.get_key_from_value(refs.dic_catr, catr_val)

        col_val = st.selectbox(label="Type de collision", options=list(refs.dic_col.values()), key='sb_col')
        col_key = refs.get_key_from_value(refs.dic_col, col_val)

        agg_val = st.selectbox(label="Localisation", options=list(refs.dic_agg.values()), key='sb_agg')
        agg_key = refs.get_key_from_value(refs.dic_agg, agg_val)

        trajet_val = st.selectbox(label="Motif du déplacement", options=list(refs.dic_trajet.values()), key='sb_trajet')
        trajet_key = refs.get_key_from_value(refs.dic_trajet, trajet_val)

        mois_val = st.selectbox(label="Mois", options=list(refs.dic_mois.values()), key='sb_mois')
        mois_key = refs.get_key_from_value(refs.dic_mois, mois_val)

        catu_val = st.selectbox(label="Catégorie d'usager", options=list(refs.dic_catu.values()), key='sb_catu')
        catu_key = refs.get_key_from_value(refs.dic_catu, catu_val)

        situ_val = st.selectbox(label="Situation de l'accident", options=list(refs.dic_situ.values()), key='sb_situ')
        situ_key = refs.get_key_from_value(refs.dic_situ, situ_val)

        place_val = st.selectbox(label="Place de l'usager", options=list(refs.dic_place.values()), key='sb_place')
        place_key = refs.get_key_from_value(refs.dic_place, place_val)

    # X = [dep_key, catv_key, catr_key, col_key, agg_key, trajet_key, mois_key, catu_key, situ_key, place_key]

    with col2:
        tab_results, tab_empty = st.tabs(["Prédiction", "..."])

        with tab_results:
            col_graph_densities, col_diagnosis = st.columns([1,1])
            with col_graph_densities:
                fig, y_pred_proba, y_true = utils.plot_prob_densities(model, X_test, y_test, ind)
                st.pyplot(fig)
            with col_diagnosis:
                pred = "Grave" if y_pred_proba >= 0.5 else "Non grave"
                vraie_valeur = "Grave" if y_true==1 else "Non grave"

                st.info(f"Probabilité prédite d'accident grave : {int(y_pred_proba*100)}%")
                if pred==vraie_valeur:
                    st.success(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
                else:
                    st.error(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")

                if 'xpl' not in st.session_state:
                    print('load smart explainer')
                    st.session_state['xpl'] = utils.get_smart_xpl(model, X_test, y_test)

                if st.session_state['xpl'] is not None:
                    fig_loc_expl = utils.get_local_explanation_fig(st.session_state.xpl, ind)
                    st.title("Shapash Local Explanation")
                    st.write("Individual index:", ind)
                    st.pyplot(fig_loc_expl)
                    # print("should plot here...")
                    # print(type(st.session_state['fig_loc_expl']))
                    # st.pyplot(st.session_state['fig_loc_expl'])
                    # st.session_state['xpl'].plot.local_plot(row_num=0)


    with tab_empty:
            st.write("...")