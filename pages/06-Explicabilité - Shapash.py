import pandas as pd
import streamlit as st
import my_libs.ref_labels as refs
from pages.libs import comp, utils
from joblib import load
comp.sidebar_info()

comp.header("Explicabilité du modèle Catboost à l'aide de la librairie Shapash")

tab_shap, tab_app_cb = st.tabs(["Valeurs de Shapley", "Application sur CatBoost"])
feats = ['catv',
         'dep',
         'catr',
         'col',
         'trajet',
         'agg',
         'place',
         'int',
         'etatp',
         'mois',
         'sexe',
         'situ',
         'age_cls',
         'atm',
         'lum',
         'nbv',
         'catu',
         'plan',
         'surf',
         'circ',
         'locp',
         'vosp',
         'prof',
         'infra',
         'joursem']


def disp_acc_labels():
    st.write("")
    for feat in feats:
        st.write(f"**{refs.dic_features[feat]}**")

def disp_acc_values(X_acc):
    for feat in feats:
        dict_feat = refs.dic_feat_mods[feat]
        st.write(f"{dict_feat[int(X_acc[feat])]}")

with tab_shap:
    comp.subheader("Valeurs de Shapley")
    st.markdown("- ##### Mesure de la contribution de chaque variable dans la prédiction finale")
    st.markdown(
        "- ##### Pour chaque donnée les valeurs de Shapley mesurent la contribution marginale de chaque caractéristique à la différence entre la prédiction moyenne du modèle et la prdiction individuelle pour la donnée en question")

    comp.subheader("Shapash")
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("- ##### Bibliothèque open source développée par une équipe de Data Scientists de la MAIF")
        st.markdown(
            "- ##### Met en oeuvre les valeurs de Shapley pour fournir des tableaux interactifs aidant à la compréhension des modèles")
        st.markdown("- ##### Facilite les discussions avec le métier")
    with col2:
        st.image("./pics/shapash-logo.png", width=150)
    with col3:
        st.image("./pics/logo-maif.png", width=150)

with tab_app_cb:
    if 'model'      not in st.session_state.keys(): st.session_state['model']      = load("./h5_models/model_cb_prd_64000x26.h5")
    if 'data_test'  not in st.session_state.keys(): st.session_state['data_test']  = pd.read_pickle("./pickles/df-prd-test.pkl")
    if 'X_test'     not in st.session_state.keys(): st.session_state['X_test']     = st.session_state['data_test'].drop(columns=['grav'], axis=1)
    if 'y_test'     not in st.session_state.keys(): st.session_state['y_test']     = st.session_state['data_test'].grav
    if 'acc_types'  not in st.session_state.keys(): st.session_state['acc_types']  = [refs.dic_grav_sht[0], refs.dic_grav_sht[1]]
    if 'pred_types' not in st.session_state.keys(): st.session_state['pred_types'] = [refs.dic_pred_type[0], refs.dic_pred_type[1]]
    if 'threshold'  not in st.session_state.keys(): st.session_state['threshold'] = 50
    if 'xpl'        not in st.session_state.keys():
        st.session_state['xpl'] = utils.get_smart_xpl(st.session_state.model, st.session_state.X_test,
                                                      st.session_state.y_test)
        st.session_state['y_pred'] = pd.Series(st.session_state.model.predict(st.session_state.X_test))
        st.session_state['y_pred_proba'] = st.session_state.model.predict_proba(st.session_state.X_test)
        st.session_state.y_pred.index = st.session_state.X_test.index
        st.session_state.xpl.compile(
            x=st.session_state.X_test,
            y_pred=st.session_state.y_pred,
            y_target=st.session_state.y_test,
        )
        st.session_state['summary_df'] = st.session_state.xpl.to_pandas(proba=False, max_contrib=10)
    if 'X_acc'      not in st.session_state.keys():
        st.session_state['X_acc'], \
            st.session_state['y_acc'], \
            st.session_state['index'] = utils.get_random_accident(st.session_state.data_test,
                                                                  st.session_state.y_pred,
                                                                  st.session_state.y_pred_proba,
                                                                  st.session_state.acc_types,
                                                                  st.session_state.pred_types,
                                                                  st.session_state.threshold)

    # Options
    col_cb_acc_grave, col_pred_type, col_threshold, col_btn, col_index, col_empty = st.columns([2, 2, 2, 0.8, 1, 2.2])

    with col_cb_acc_grave:
        st.session_state.acc_types = st.multiselect(label="Type d'accident", options=refs.dic_grav_sht.values(), label_visibility="collapsed")

    with col_pred_type:
        st.session_state.pred_types = st.multiselect(label="Prédiction", options=refs.dic_pred_type.values(), label_visibility="collapsed")

    with col_threshold:
        slider_disabled = False if st.session_state.pred_types == [refs.dic_pred_type[0]] else True
        st.session_state.threshold = st.slider(label="Niveau de confiance", label_visibility="collapsed",
                                               value=st.session_state.threshold, disabled=slider_disabled)

    with col_btn:
        if st.button('Accident'):
            st.write("")
            # st.experimental_rerun()
            st.session_state['X_acc'], st.session_state['y_acc'], st.session_state['index'] = utils.get_random_accident(
                st.session_state.data_test,
                st.session_state.y_pred,
                st.session_state.y_pred_proba,
                st.session_state.acc_types,
                st.session_state.pred_types,
                st.session_state.threshold)

    with col_index:
        st.text_input(label="index", label_visibility="collapsed", value=st.session_state.index, placeholder="index", disabled=True)


    # Results
    col_acc, col_pred, col_shap = st.columns([1, 0.8, 1])

    with col_acc:
        col_label, col_value = st.columns([0.8, 1])

        with col_label:
            disp_acc_labels()

        with col_value:
            st.write("")
            if st.session_state['X_acc'] is not None:
                X_acc = st.session_state['X_acc']
                disp_acc_values(X_acc)

    with col_pred:
        col_graph_densities, col_diagnosis = st.columns([1, 1])
        # with col_graph_densities:
        fig, y_pred_proba, y_true = utils.plot_prob_densities(st.session_state.model,
                                                              st.session_state.X_test,
                                                              st.session_state.y_test,
                                                              st.session_state.index)
        if y_pred_proba is not None:
            pred = "Grave" if y_pred_proba >= 0.5 else "Non grave"
            vraie_valeur = "Grave" if y_true == 1 else "Non grave"

            st.info(f"Probabilité prédite d'accident grave : {int(y_pred_proba * 100)}%")
            if pred == vraie_valeur:
                st.success(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
            else:
                st.error(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
            st.pyplot(fig)

    with col_shap:
        st.subheader("Contribution par feature")
        if st.session_state['index'] is not None:
            fig = utils.get_local_summary_plot(st.session_state.summary_df.loc[st.session_state.index])
            st.pyplot(fig)
