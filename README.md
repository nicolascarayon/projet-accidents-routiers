> Ce repository est la matérialisation du projet effectué dans le cadre du parcours Data Scientist de datascientest.com
> 
> Il constitue une tentative d'élaboration de prédicteur de gravité d'accidents routiers en fonction de variables liées aux usagers, véhicules, lieux, et caractéristiques des accidents recencés en France entre 2005 et 2021.
>
> Les données sont issues du fichier BAAC en licence ouverte  
> 
> https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/

### Outils nécessaires pour le bon fonctionnement du projet 

- Anaconda : https://www.anaconda.com/products/distribution
- jupyter : https://jupyter.org/install
- git : https://git-scm.com/downloads

Projet développé avec Python 3.9.13

### Notebooks disponibles

* **00-dataset-generation.ipynb** 
    *  Charge et traite les données issues des fichiers .csv sur la période 2005 à 2021 et contenus dans le répertoire *data/data_gouv_fr* 
    *  Les fichiers pickles créés à l'issue du traitement sont stockés dans le répertoire *pickles/*
    *  **df-prd-train.pkl** et **df-prd-test.pkl** constituent les dataframes d'entraînement et de test des modèles
    *  **df-dev-train.pkl** et **df-dev-test.pkl** constituent les dataframes d'entraînement et de test des modèles en environnement de développement 
    *  Ils permettent d'alimenter les notebooks préfixés 02.x traitant de modélisation

* **01-data-load-viz.ipynb** : notebook présentant une exploration des données et détaillant le process de taitement du notebook **00-dataset-generation.ipynb**   

* **02.1-DecisionTreeClassifier.ipynb** : notebook consacré à l'élaboration du prédicteur à base d'arbre de décision

* **02.2-RandomForestClassifier.ipynb** : notebook consacré à l'élaboration du prédicteur à base de forêts aléatoires

* **02.3-XgBoostCLassifier.ipynb** : notebook consacré à l'élaboration du prédicteur à base de Gradient Boosting 

* **02.4-CatBoostClassifier.ipynb** : notebook consacré à l'élaboration du prédicteur à base de l'algorithme CatBoost
  
### Librairies nécessitant potentiellement une installation particulière :
* shapash : https://github.com/MAIF/shapash 
* catboost : https://catboost.ai/ 
* optuna : https://optuna.org/
* imblearn : https://imbalanced-learn.org/stable/
* category_encoders : https://pypi.org/project/category-encoders/

