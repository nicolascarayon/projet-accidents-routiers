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
        X_acc, y_acc, ind, index = utils.get_random_accident(X_test, y_test, acc_grav_only)

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

    col1, col2 = st.columns([1, 2])

    with col1:
        col_label, col_value = st.columns([0.6, 1])

        with col_label:
            st.write("")
            st.write(f"**Département**")
            st.write(f"**Catégorie de véhicule**")
            st.write("**Catégorie de route**")
            st.write("**Type de collision**")
            st.write("**Localisation**")
            st.write("**Motif du déplacement**")
            st.write("**Mois**")
            st.write("**Catégorie d'usager**")
            st.write("**Situation de l'accident**")
            st.write("**Place de l'usager**")

        with col_value:
            st.write("")
            st.write(f"{refs.dic_dep[int(X_acc.dep)]}")
            st.write(f"{refs.dic_catv[int(X_acc.catv)]}")
            st.write(f"{refs.dic_catr[int(X_acc.catr)]}")
            st.write(f"{refs.dic_col[int(X_acc.col)]}")
            st.write(f"{refs.dic_agg[int(X_acc['agg'])]}")
            st.write(f"{refs.dic_trajet[int(X_acc.trajet)]}")
            st.write(f"{refs.dic_mois[int(X_acc.mois)]}")
            st.write(f"{refs.dic_catu[int(X_acc.catu)]}")
            st.write(f"{refs.dic_situ[int(X_acc.situ)]}")
            st.write(f"{refs.dic_place[int(X_acc.place)]}")


    with col2:
        tab_prediction, tab_empty = st.tabs(["Prédiction", "..."])

        with tab_prediction:
            col_graph_densities, col_diagnosis = st.columns([1,1])
            with col_graph_densities:
                fig, y_pred_proba, y_true = utils.plot_prob_densities(model, X_test, y_test, ind)
                pred = "Grave" if y_pred_proba >= 0.5 else "Non grave"
                vraie_valeur = "Grave" if y_true==1 else "Non grave"

                st.info(f"Probabilité prédite d'accident grave : {int(y_pred_proba*100)}%")
                if pred==vraie_valeur:
                    st.success(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")
                else:
                    st.error(f"Prédiction : {pred} - Vraie valeur : {vraie_valeur}")


                st.pyplot(fig)
            with col_diagnosis:


                if 'xpl' not in st.session_state:
                    st.session_state['xpl'] = utils.get_smart_xpl(model, X_test, y_test)
                    y_pred = pd.Series(model.predict(X_test))
                    y_pred.index = X_test.index
                    st.session_state['xpl'].compile(
                        x=X_test,
                        y_pred=y_pred, # Optional: for your own prediction (by default: model.predict)
                        y_target=y_test, # Optional: allows to display True Values vs Predicted Values
                    )
                    if 'summary_df' not in st.session_state:
                        st.session_state['summary_df'] = st.session_state['xpl'].to_pandas(proba=False, max_contrib=10)

                if st.session_state['xpl'] is not None:
                    xpl = st.session_state['xpl']
                    df_loc_summary = st.session_state.summary_df
                    st.subheader("Shapash Local Explanation")
                    # st.dataframe(data=df_loc_summary.loc[index])
                    fig = utils.get_local_summary_plot(df_loc_summary.loc[index])
                    st.pyplot(fig)


    with tab_empty:
            st.write("...")