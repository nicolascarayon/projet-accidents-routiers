import pandas as pd
import streamlit as st
import my_libs.ref_labels as refs
from pages.libs import comp, utils
from joblib import load
comp.sidebar_info()

comp.header("Explicabilité du modèle Catboost à l'aide de la librairie Shapash")

tab_shap, tab_app_cb = st.tabs(["Valeurs de Shapley", "Application sur CatBoost"])

feats = ['dep','catv','catr','col','agg','trajet','mois','catu','situ','place','sexe','catr','locp','etatp','lum',
         'int','atm','circ','nbv','vosp','prof','plan','surf','infra','situ','joursem','age_cls']
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
    if 'model' not in st.session_state.keys(): st.session_state['model'] = load("./h5_models/model_cb_prd_64000x26.h5")
    if 'data_test' not in st.session_state.keys(): st.session_state['data_test'] = pd.read_pickle(
        "./pickles/df-prd-test.pkl")
    if 'X_test' not in st.session_state.keys(): st.session_state['X_test'] = st.session_state['data_test'].drop(
        columns=['grav'], axis=1)
    if 'y_test' not in st.session_state.keys(): st.session_state['y_test'] = st.session_state['data_test'].grav
    if 'X_acc' not in st.session_state.keys():
        print("get_random_accident dans tab_app_cb")
        st.session_state['acc_grav_only'] = False
        st.session_state['X_acc'], st.session_state['y_acc'], st.session_state['index'] = \
            utils.get_random_accident(st.session_state['X_test'], st.session_state['y_test'],
                                      st.session_state['acc_grav_only'])
    if 'xpl' not in st.session_state.keys():
        st.session_state['xpl'] = utils.get_smart_xpl(st.session_state.model, st.session_state.X_test,
                                                      st.session_state.y_test)
        st.session_state['y_pred'] = pd.Series(st.session_state.model.predict(st.session_state.X_test))
        st.session_state.y_pred.index = st.session_state.X_test.index
        st.session_state.xpl.compile(
            x=st.session_state.X_test,
            y_pred=st.session_state.y_pred,
            y_target=st.session_state.y_test,
        )
        st.session_state['summary_df'] = st.session_state.xpl.to_pandas(proba=False, max_contrib=10)

    col_btn, col_cb_acc_type, col_index, col_empty = st.columns([1, 1, 1, 6])
    with col_btn:
        st.session_state['acc_grav_only'] = st.checkbox(label="Accidents graves")

        # print("get_random_accident dans col_btn")
        # st.session_state['X_acc'], st.session_state['y_acc'], st.session_state['index'] = utils.get_random_accident(st.session_state['X_test'], st.session_state['y_test'], st.session_state['acc_grav_only'])
        # st.experimental_rerun()

    with col_cb_acc_type:
        if st.button('New accident'):
            st.write("")
            # st.experimental_rerun()
            print("get_random_accident dans col_cb_acc_type")
            st.session_state['X_acc'], st.session_state['y_acc'], st.session_state['index'] = utils.get_random_accident(
                st.session_state.X_test,
                st.session_state.y_test,
                st.session_state.acc_grav_only)

    with col_index:
        index = st.text_input(label="index", label_visibility="collapsed", value=st.session_state.index, placeholder="index")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        col_label, col_value = st.columns([0.8, 1])

        with col_label:
            disp_acc_labels()

        with col_value:
            st.write("")
            if st.session_state['X_acc'] is not None:
                X_acc = st.session_state['X_acc']
                disp_acc_values(X_acc)

    with col2:
        col_graph_densities, col_diagnosis = st.columns([1, 1])
        # with col_graph_densities:
        fig, y_pred_proba, y_true = utils.plot_prob_densities(st.session_state.model, st.session_state.X_test,
                                                              st.session_state.y_test, st.session_state.index)
        pred = "Grave" if y_pred_proba >= 0.5 else "Non grave"
        vraie_valeur = "Grave" if y_true == 1 else "Non grave"

        st.info(f"Probabilité prédite d'accident grave : {int(y_pred_proba * 100)}%")
        if pred == vraie_valeur:
            st.success(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
        else:
            st.error(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
        st.pyplot(fig)

    with col3:
        st.subheader("Contribution par feature")
        fig = utils.get_local_summary_plot(st.session_state.summary_df.loc[st.session_state.index])
        st.pyplot(fig)
