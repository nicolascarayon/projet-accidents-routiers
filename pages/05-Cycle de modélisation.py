import streamlit as st
from pages.libs import comp

comp.sidebar_info()

comp.header("Cycle de modélisation")

tab_ctr, tab_opt, tab_dt, tab_rf, tab_gb, tab_cb = st.tabs(["Contraintes", "Optimisation d'hyperparamètres", "Decision Tree", "Random Forests", "Gradient Boosting", "CatBoost"])

with tab_ctr:
    comp.subheader("Cadre")
    st.markdown("- ##### Données tabulaires")
    st.markdown("- ##### Données essentiellement catégorielles")
    st.markdown("- ##### Recherche d'un modèle explicable")
    st.markdown("- ##### Temps et moyens matériels limités")

    comp.subheader("Stratégie")
    st.markdown("##### Tous ces éléments amènent aux choix d'algorithmes basés sur les arbres de décision")
    st.markdown("- ##### 1. Modèle simple : Decision Tree")
    st.markdown("- ##### 2. Aggrégation de modèles simples : Random Forests")
    st.markdown("- ##### 3. Méthode de Boosting : Gradient Boosting Classifier")
    st.markdown("- ##### 4. Algorithme de Boosting spécifique aux données catégorielles : CatBoost")

with tab_opt:
    comp.subheader("Optimisation d'hyperparamètres")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("- ##### Grâce à la librairie *Optuna* (et non GridSearchCV de scikit-learn) permettant une optimisation Bayesienne")
        st.markdown("- ##### Basée sur la recherche à base d'estimateur TPE (Tree-structured Parzen Estimator)")
        st.write("TPE utilise une distribution de probabilité pour estimer la performance de chaque combinaison d'hyperparamètres de façon itérative")
    with col2:
        st.image("./pics/optuna-logo.png", width=300)


with tab_dt:
    comp.subheader("Decision Tree")
    st.markdown("- ##### 1. Sélection de la variable qui divise le mieux l'ensemble par rapport à la variable cible (selon un critère défini)")
    st.markdown("- ##### 2. Détermination de la valeur de la variable qui divise l'ensemble en 2 sous-ensembles")
    st.markdown("- ##### 3. Création d'un noeud à partir de la variable et la valeur seuil - Répétition des étapes 1 à 3 sur les sous-ensembles créés")

    show_res_dt = st.checkbox("Résultats", key="chk_res_dt")
    if show_res_dt:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("./pics/dt-classif-report.png", width=500)
        with col2:
            st.image("./pics/dt-confusion.png", width=250)


with tab_rf:
    comp.subheader("Random Forest")
    st.markdown("- ##### Le vote d'un nombre important de classifieurs simples est meilleur que l'appel à un *expert* (aux sens de la précision et de la stabilité)")
    st.markdown("- ##### Construction d'un grand nombre d'arbres opérant chacun sur un sous ensemble aléatoire du jeu d'entraînement")
    st.markdown("- ##### La prédiction est le fruit de l'agrégation des prédictions de tous les arbres")

    show_res_rf = st.checkbox("Résultats", key="chk_res_rf")
    if show_res_rf:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("./pics/rf-classif-report.png", width=500)
        with col2:
            st.image("./pics/rf-confusion.png", width=250)

with tab_gb:
    comp.subheader("Gradient Boosting")

    show_res_gb = st.checkbox("Résultats", key="chk_res_gb")
    if show_res_gb:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("./pics/gb-classif-report.png", width=500)
        with col2:
            st.image("./pics/gb-confusion.png", width=250)

with tab_cb:
    comp.header("CatBoost")

    show_res_cb = st.checkbox("Résultats", key="chk_res_cb")
    if show_res_cb:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image("./pics/cb-classif-report.png", width=500)
        with col2:
            st.image("./pics/cb-confusion.png", width=250)
