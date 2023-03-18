import pandas as pd
import numpy as np
import plotly
from my_libs import ref_labels as refs

from my_libs import lib_tools as pt
import matplotlib.pyplot as plt
import seaborn as sns

DIR_DATA_GOUV = ".\\data\\data_gouv_fr\\"


def get_local_summary_plot(df):
    feat_names = []
    feat_contrib = []
    mult = 1
    for ind in df.index:
        if ind == "y_pred":
            if df.loc[ind] == "Indemne - Blessé léger":
                mult = -1
        if "feature_" in ind: feat_names.append(df.loc[ind])
        if "contribution_" in ind: feat_contrib.append(mult * df.loc[ind])

    data = pd.DataFrame(columns=['feature', 'contrib'])
    data['feature'] = feat_names
    data['contrib'] = feat_contrib
    data = data.sort_values(by='contrib', ascending=False)

    fig = plt.figure(figsize=(8, 12))
    # sns.set_color_codes("pastel")
    # sns.barplot(x="contrib", y="feature", data=data, alpha=0.6)
    colors = ['lightskyblue' if x < 0 else 'orange' for x in data['contrib']]
    sns.barplot(x="contrib", y="feature", data=data, alpha=0.5, palette=colors)
    plt.grid(axis='x', linestyle='--')
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)
    plt.xlabel("")
    plt.ylabel("")

    return fig


def get_random_accident(data_test, y_pred, acc_types, pred_types):
    acc_grav_val, pred_types_val = [], []

    if len(acc_types) == 0 and len(pred_types) == 0: return None, None, None

    for val in acc_types:
        acc_grav_val.append(refs.get_key_from_value(refs.dic_grav_sht, val))
    for val in pred_types:
        pred_types_val.append(refs.get_key_from_value(refs.dic_pred_type, val))

    data_test_filtered = data_test[data_test.grav.isin(acc_grav_val)]
    y_pred_filtered = y_pred[data_test.grav.isin(acc_grav_val)]

    i = int(np.random.uniform(low=0, high=data_test_filtered.shape[0] - 1))
    print(f"i : {i}")
    print(f"data_test_filtered : {data_test_filtered.shape}")
    data_test_acc = data_test_filtered.iloc[i, :]

    y_pred_acc = y_pred_filtered.iloc[i]

    # look for a good prediction
    if pred_types == [refs.dic_pred_type[0]]:
        print("filtre pred good")
        while (data_test_acc.grav != y_pred_acc):
            i = int(np.random.uniform(low=0, high=data_test_filtered.shape[0] - 1))
            data_test_acc = data_test_filtered.iloc[i, :]
            y_pred_acc = y_pred_filtered.iloc[i]

    # look for a wrong prediction
    if pred_types == [refs.dic_pred_type[1]]:
        print("filtre pred wrong")

    X_acc = data_test_acc.drop('grav')
    y_acc = data_test_acc.grav

    return (X_acc, y_acc, data_test_filtered.index[i])


def get_DataFrame(file_type, year):
    if file_type == 'usagers'  : df = load_usagers(year, year)
    if file_type == 'accidents': df = load_caract(year, year)
    if file_type == 'lieux'    : df = load_lieux(year, year)
    if file_type == 'véhicules': df = load_vehicules(year, year)

    return df


def get_working_dataset():
    X_train, y_train, X_valid, y_valid, X_test, y_test = pt.get_train_valid_test_data('dev')
    return X_train


def load_caract(start_year, end_year):
    """
    Retourne les données dans un dictionnaire de dataframes dont la clé est l'année au format entier

    ex : caract = load_caract(2019, 2021)
    les données de l'années 2020 sont accessibles caract[2020]

    Num_Acc : identifiant de l'accident
    jour : jour de l'accident
    mois : mois de l'accident
    an : année de l'accident
    hrmn : hh:mm de l'accident
    lum : conditions de luminosité (1: Plein jour, ..., 5:Nuit avec éclairage public allumé)
    dep : département (code INSEE)
    com : commune (code INSEE)
    agg : localisation (1: hors agglomération, 2: en agglomération)
    int : intersection (1: Hors intersection, ..., 9: Autre intersection)
    atm : conditions atmosphériques (-1: Non renseigné, 1: Normale, ..., 8: Temps couvert, 9: Autre)
    col : type de collision (-1: Non renseigné, 1:Deux véhicules - frontale, ..., 6: Autre collision, 7: Sans collision)
    adr : adresse postale
    lat : latitude
    long : longitude

    """
    caract = {}
    dic_types = {'Num_Acc': 'Int64', 'jour': 'Int64', 'mois': 'Int64', 'an': 'Int64', 'hrmn': 'str',
                 'lum': 'Int64', 'dep': 'str', 'com': 'str', 'agg': 'Int64', 'int': 'Int64', 'atm': 'Int64',
                 'col': 'Int64', 'adr': 'str', 'lat': 'str', 'long': 'str'}
    for year in range(start_year, end_year + 1):
        car = '_' if 2005 <= year <= 2016 else '-'
        if year == 2009:
            sep = '\t'
        else:
            sep = ',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2020:
            caract[year] = pd.read_csv(DIR_DATA_GOUV + f'caracteristiques{car}{year}.csv', sep=sep,
                                       encoding='ISO-8859-1', dtype=dic_types)
        if year == 2021:
            caract[year] = pd.read_csv(DIR_DATA_GOUV + f'carcteristiques{car}{year}.csv', sep=sep,
                                       encoding='ISO-8859-1', dtype=dic_types)
    return caract


def load_lieux(start_year, end_year):
    """
    Retourne les données dans un dictionnaire de dataframes dont la clé est l'année au format entier

    ex : lieux = load_lieux(2019, 2021)
    les données de l'années 2020 sont accessibles lieux[2020]

    Num_Acc : identifiant de l'accident
    catr : catégorie de route
    voie : numéro de la route
    v1 : indice numérique du numéro de route
    v2 : lettre indice alphanumérique de la route
    circ : régime de circulation
    nbv : nombre total de voies de circulation
    vosp : signale l’existence d’une voie réservée, indépendamment du fait que l’accident ait lieu ou non sur cette voie.
    prof : profil en long décrit la déclivité de la route à l'endroit de l'accident
    pr : numéro du PR de rattachement (numéro de la borne amont)
    pr1 : distance en mètres au PR (par rapport à la borne amont)
    plan : tracé en plan ( 1:Partie rectiligne, 2:En courbe à gauche, 3:En courbe à droite, 4:En "S")
    lartpc : Largeur du terre plein central (TPC) s'il existe
    larrout : Largeur de la chaussée affectée à la circulation des véhicules ne sont pas compris les bandes d'arrêt d'urgence, les TPC et les places de stationnement
    surf : état de la surface
    infra : aménagement - Infrastructure
    situ : situation de l’accident
    vma : point école : proximité d'une école

    """
    lieux = {}
    dic_type = {'catr': 'Int64', 'voie': 'str', 'v1': 'str', 'v2': 'str', 'circ': 'Int64', 'nbv': 'Int64',
                'vosp': 'Int64', 'prof': 'Int64', 'plan': 'Int64',
                'lartpc': 'str', 'surf': 'Int64', 'infra': 'Int64', 'situ': 'Int64'}
    for year in range(start_year, end_year + 1):
        car = '_' if 2005 <= year <= 2016 else '-'
        sep = ',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            lieux[year] = pd.read_csv(DIR_DATA_GOUV + f'lieux{car}{year}.csv', sep=sep, dtype=dic_type)
    return lieux


def load_usagers(start_year, end_year):
    """Retourne les données dans un dictionnaire de dataframes dont la clé est l'année au format entier

    ex : usagers = load_usagers(2019, 2021)
    les données de l'années 2020 sont accesibles usagers[2020]

    Num_Acc : identifiant de l'accident
    id_vehicule : identifiant unique du véhicule repris pour chacun des usagers occupant ce véhicule
    num_veh : identifiant du véhicule repris pour chacun des usagers occupant ce véhicule
    place : permet de situer la place occupée dans le véhicule par l'usager au moment de l'accident
    catu : catégorie d'usager
    grav : gravité de l'accident (!!!VARIABLE CIBLE!!!)
    sexe : sexe de l'usager
    an_nais : année de naissance de l'usager
    trajet : motif du déplacement au moment de l’accident
    secu1 : le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité
    secu2 : le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité
    secu3 : le renseignement du caractère indique la présence et l’utilisation de l’équipement de sécurité
    locp : localisation du piéton
    actp : action du piéton
    etatp : etatp
    """
    usagers = {}
    dic_types = {'place': 'Int64', 'catu': 'Int64', 'grav': 'Int64', 'sexe': 'Int64', 'an_nais': 'Int64',
                 'trajet': 'Int64',
                 'secu': 'str', 'secu1': 'Int64', 'secu2': 'Int64', 'secu3': 'Int64', 'locp': 'Int64', 'actp': 'str',
                 'etatp': 'Int64'}
    for year in range(start_year, end_year + 1):
        car = '_' if 2005 <= year <= 2016 else '-'
        sep = ',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            usagers[year] = pd.read_csv(DIR_DATA_GOUV + f'usagers{car}{year}.csv', sep=sep, dtype=dic_types)
    return usagers


def load_vehicules(start_year, end_year):
    """Retourne les données dans un dictionnaire de dataframes dont la clé est l'année au format entier

    ex : vehicles = load_vehicules(2019, 2021)
    les données de l'années 2020 sont accesibles vehicles[2020]

    Num_Acc : identifiant de l'accident
    id_vehicule : identifiant du véhicule
    num_veh : identifiant du véhicule repris pour chacun des usagers occupant ce véhicule
    senc : sens de circulation
    catv : catégorie du véhicule
    obs : obstacle fixe heurté
    obsm : obstacle mobile heurté
    choc : point de choc initial
    manv : manoeuvre principale avant l'accident
    motor : type de motorisation du véhicule
    occutc : nombre d’occupants dans le transport en commun
    """
    vehic = {}
    dic_types = {'senc': 'Int64', 'catv': 'Int64', 'obs': 'Int64', 'obsm': 'Int64', 'choc': 'Int64', 'manv': 'Int64',
                 'motor': 'Int64', 'occutc': 'Int64'}
    for year in range(start_year, end_year + 1):
        car = '_' if 2005 <= year <= 2016 else '-'
        sep = ',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            vehic[year] = pd.read_csv(DIR_DATA_GOUV + f'vehicules{car}{year}.csv', sep=sep, dtype=dic_types)
    return vehic


def get_dep_list():
    return ['01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '20',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
            '32',
            '33',
            '34',
            '35',
            '36',
            '37',
            '38',
            '39',
            '40',
            '41',
            '42',
            '43',
            '44',
            '45',
            '46',
            '47',
            '48',
            '49',
            '50',
            '51',
            '52',
            '53',
            '54',
            '55',
            '56',
            '57',
            '58',
            '59',
            '60',
            '61',
            '62',
            '63',
            '64',
            '65',
            '66',
            '67',
            '68',
            '69',
            '70',
            '71',
            '72',
            '73',
            '74',
            '75',
            '76',
            '77',
            '78',
            '79',
            '80',
            '81',
            '82',
            '83',
            '84',
            '85',
            '86',
            '87',
            '88',
            '89',
            '90',
            '91',
            '92',
            '93',
            '94',
            '95',
            '971',
            '972',
            '973',
            '974',
            '976']


def get_catv_list():
    return [-1,
            1,
            2,
            7,
            10,
            30,
            33]


def plot_compare_models():
    df = pd.DataFrame(data=[], columns=['precision', 'recall', 'f1-score'],
                      index=['Decision Tree', 'Random Forests', 'Gradient Boosting', 'CatBoost'])
    df.precision = [0.36, 0.27, 0.38, 0.43]
    df.recall = [0.51, 0.76, 0.70, 0.55]
    df['f1-score'] = [0.36, 0.40, 0.49, 0.48]
    df['accuracy'] = [0.66, 0.57, 0.73, 0.78]

    fig, axs = plt.subplots(1, 4, figsize=(12, 4), sharey=True)
    palette = sns.color_palette("pastel")

    sns.barplot(x=df.index, y='precision', data=df, palette=palette, ax=axs[0])
    axs[0].set_title('Precision')

    sns.barplot(x=df.index, y='recall', data=df, palette=palette, ax=axs[1])
    axs[1].set_title('Recall')

    sns.barplot(x=df.index, y='f1-score', data=df, palette=palette, ax=axs[2])
    axs[2].set_title('F1-score')

    sns.barplot(x=df.index, y='accuracy', data=df, palette=palette, ax=axs[3])
    axs[3].set_title('Accuracy')

    for ax in axs:
        ax.set_ylim([0, 1])
        ax.set_xticklabels(df.index, rotation=80)
        ax.grid(True, axis='y', linestyle='--', linewidth='0.3')
        ax.get_yaxis().set_visible(True)

    return df, fig


def plot_prob_densities(model, X_test, y_test, index):
    if index is None: return None, None, None

    X_test.dep = X_test.dep.astype('int')
    y_pred_proba = model.predict_proba(X_test)

    y_pred_prob_single = model.predict_proba(X_test.loc[index])[1]
    y_true = y_test.loc[index]

    fig = plt.figure(figsize=(12, 12))
    # sns.kdeplot(y_pred_proba[:, 1], shade=True, cut=0, label="Non grave")
    sns.kdeplot(y_pred_proba[:, 1], shade=True, cut=0, label="Grave", color="darkorange")
    # plt.legend(loc='upper center')
    if y_pred_prob_single is not None: plt.axvline(x=y_pred_prob_single, color='r', linestyle='--', linewidth=4)

    return fig, y_pred_prob_single, y_true


def get_smart_xpl(model, X_test, y_test):
    from shapash import SmartExplainer
    from my_libs import ref_labels
    import pickle
    import shap
    shap.initjs()

    all_var = True
    if all_var:
        label_dict = ref_labels.dic_target
        preprocessing = ref_labels.dic_preproc
        features_dic = ref_labels.dic_features
    else:
        label_dict = None
        preprocessing = None
        features_dic = None

    xpl = SmartExplainer(
        model=model,
        label_dict=label_dict,
        preprocessing=preprocessing,
        features_dict=features_dic,  # Optional parameter
    )

    y_test.index = X_test.index

    xpl.compile(
        x=X_test,
        # y_pred=y_pred, # Optional: for your own prediction (by default: model.predict)
        y_target=y_test,  # Optional: allows to display True Values vs Predicted Values
    )
    return xpl


def get_local_explanation(xpl, ind):
    # local_summary = xpl.summarize(row_num=ind)
    # # Display the local explanation summary in a readable format
    # local_summary.to_pandas()
    # Plot the local explanation
    # xpl.plot.config.backend = "matplotlib"

    fig = plt.figure(figsize=(3, 3))
    summary_df = xpl.to_pandas(proba=True)
    xpl.plot.local_plot(row_num=ind)
    # fig, _ = xpl.plot.local_plot(index=individual_index)

    return fig, summary_df
