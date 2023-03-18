import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTEN

DIR_DATA_GOUV = ".\\data\\data_gouv_fr\\"

DF_DEV_TRAIN_PATH = 'pickles/df-dev-train.pkl'
DF_DEV_TEST_PATH = 'pickles/df-dev-test.pkl'
DF_PRD_TRAIN_PATH = 'pickles/df-prd-train.pkl'
DF_PRD_TEST_PATH = 'pickles/df-prd-test.pkl'


def load_proj_df(start_year, end_year, verbose=0):
    """
    Returns into a DataFrame the data on the period [start_year, end_year]

    :param start_year: year defining the lower bound of the period
    :param end_year:   year defining the higher bound of the period
    :param verbose:    if 1 the execution is verbose
    """
    df, dic_usagers, dic_caract, dic_lieux, dic_vehic = get_work_df(start_year, end_year, verbose)
    if verbose: display_stats_data_load(dic_usagers, dic_caract, dic_lieux, dic_vehic, start_year, end_year)

    # rmv col related to geographical info
    df = drop_columns_from_df(df, ['com', 'adr', 'lat', 'long', 'pr', 'pr1'], verbose)
    # rmv col not known before the accident
    df = drop_columns_from_df(df, ['obs', 'obsm', 'choc', 'manv'], verbose)

    df = rmv_col_too_much_null(df, 0.08, verbose)
    df = clean_categ_not_specified(df)
    df = drop_lines_with_null(df, verbose)
    df = create_age(df)
    df = create_age_cls(df)
    df = clean_col_dep(df, True)
    df = clean_nbv(df)
    df = clean_actp(df)
    df = clean_etatp(df)
    df = clean_catv(df)
    df = clean_catu(df)
    df = clean_circ(df)
    df = clean_hrmn(df)
    df = create_datetime(df)
    df = create_joursem(df)
    df = create_grav_lbl(df)
    df = drop_columns_from_df(df,
                              ['an_nais', 'age', 'grav_lbl', 'Num_Acc', 'datetime', 'an', 'num_veh', 'jour', 'hrmn', 'senc'],
                              verbose)
    df = encode_grav(df, verbose)
    df = set_target_first_column(df, verbose)

    if verbose: df.info(verbose=True, show_counts=True)

    return df


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


# DATA PRE-PROCESSING --------------------------------------------
def preproc_usagers(dic_usagers, verbose):
    df_usagers = concat_df_from_dict(dic_usagers, verbose)
    df_usagers = manage_duplicated(df_usagers, verbose)

    return df_usagers


def preproc_caract(dic_caract, verbose):
    df_caract = concat_df_from_dict(dic_caract, verbose)
    df_caract = manage_duplicated(df_caract, verbose)
    df_caract['an'] = df_caract['an'].replace(
        to_replace=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        value=[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
               2015, 2016, 2017, 2018])

    return df_caract


def preproc_vehic(dic_vehic, verbose):
    df_vehic = concat_df_from_dict(dic_vehic, verbose)
    df_vehic = manage_duplicated(df_vehic, verbose)
    df_vehic = manage_vehic_duplicated(df_vehic, verbose)

    return df_vehic


def preproc_lieux(dic_lieux, verbose):
    df_lieux = concat_df_from_dict(dic_lieux, verbose)
    df_lieux = manage_duplicated(df_lieux, verbose)

    return df_lieux


def concat_df_from_dict(dic, verbose):
    """
    Concatenates all DataFrames contained in dic in one single DataFrame
    :param dic: A dictionary with key value pairs like dic[year] = dataframe
    :param verbose: 1 to display information message
    :return: a DataFrame fed consistenly with all data from dic
    """
    [start_year, end_year] = get_start_end_years_from_dic(dic)
    for year in dic.keys():
        df = dic[year]
        if year == start_year:
            df_final = df
        else:
            df_final = pd.concat([df_final, df], ignore_index=True, axis=0)
    if verbose:
        chk_concat(dic, df_final)
    return df_final


def manage_duplicated(df, verbose):
    """
    Removes the duplicates in df
    :param df: the DataFrame
    :param verbose: 1 to display information
    :return: the df with no duplicate
    """
    if verbose: print(f"nombre de doublons avant traîtement : {df.duplicated().sum()}")
    df = df.drop_duplicates()
    if verbose: print(f"nombre de doublons après traîtement : {df.duplicated().sum()}")

    return df


def clean_categ_not_specified(df):
    """
    Replaces in df the nan by -1 in columns where -1 is allowed
    :param df: the dataframe to be updated
    :return: the dataframe with non replaced by -1
    """
    col_minusone = ['place', 'catu', 'grav', 'sexe', 'trajet', 'secu', 'locp', 'actp',
                    'etatp', 'secu1', 'secu2', 'secu3', 'lum', 'agg', 'int', 'atm',
                    'col', 'catr', 'circ', 'nbv', 'vosp', 'prof', 'plan', 'lartpc',
                    'larrout', 'surf', 'infra', 'situ', 'env1', 'vma', 'senc', 'catv',
                    'occutc', 'obs', 'obsm', 'choc', 'manv', 'motor']
    col_to_chk = []
    for col in col_minusone:
        if col in df.columns:
            col_to_chk.append(col)
    df[col_to_chk] = df[col_to_chk].replace(to_replace=np.nan, value=-1)

    return df


def rmv_col_too_much_null(df, threshold, verbose):
    rate_missing = df.isnull().sum() / len(df)
    df_miss = pd.DataFrame({'column_name': df.columns, 'rate_missing': rate_missing})
    df_miss.sort_values('rate_missing', inplace=True, ascending=False)
    to_drop = df_miss[df_miss.rate_missing >= threshold]['column_name']
    df = df.drop(columns=to_drop.index, axis=1)

    if verbose:
        df_miss.rate_missing *= 100
        print(f"Colonnes supprimées : {to_drop.index}")
        print(f"\n{df_miss}")
    return df


def manage_vehic_duplicated(df_vehic, verbose):
    if verbose:
        df_vehic_dupl = df_vehic.duplicated(['Num_Acc', 'num_veh'])
        print(
            f"Véhicules en doublons vis à vis de la clé fonctionnelle avant traitement : {df_vehic_dupl[df_vehic_dupl].sum()}")

    df_vehic.drop_duplicates(['Num_Acc', 'num_veh'], keep='first', inplace=True)

    if verbose:
        df_vehic_dupl = df_vehic.duplicated(['Num_Acc', 'num_veh'])
        print(
            f"Véhicules en doublons vis à vis de la clé fonctionnelle après traitement : {df_vehic_dupl[df_vehic_dupl].sum()}")

    return df_vehic


def get_start_end_years_from_dic(dic):
    str_y = list(dic.keys())[0]
    end_y = list(dic.keys())[-1:]
    return [str_y, end_y]


def chk_concat(dic, df):
    """Checks that the sum of lines for all keys of the Dictionary 'dic' equals the number of lines of the DataFrame 'df'"""
    nb_lines = 0
    start_year = list(dic.keys())[0]
    end_year = list(dic.keys())[-1:]
    for year in dic.keys():
        nb_lines += dic[year].shape[0]

    print(f"somme des lignes 'dic': {nb_lines}")
    print(f"nombre de lignes 'df' : {df.shape[0]}")


def proc_usagers_secu(dic_usagers):
    """
    Concat all df usagers from 2005 to 2018 -> ['secu'] is splitted into ['secu1', 'secu2', 'secu3']
    for year in range(start_year, end_year + 1):
    """
    [start_year, end_year] = get_start_end_years_from_dic(dic_usagers)
    for year in dic_usagers.keys():
        df = dic_usagers[year]
        if 2005 <= year <= 2018:
            # create columns ['secu1', 'secu2', 'secu3'] and drop old 'secu'
            df['secu'] = df['secu'].replace(to_replace=np.nan, value=-1)
            df['secu1'] = df['secu'] // 10
            df['secu2'] = df['secu'] % 10
            df['secu3'] = np.ones(len(df['secu'])) * (-1)

            df = df.drop(columns=['secu'])
            df['secu1'] = df['secu1'].astype('int')
            df['secu2'] = df['secu2'].astype('int')
            df['secu3'] = df['secu3'].astype('int')

        return df


def proc_caract_gps(dic_caract):
    [start_year, end_year] = get_start_end_years_from_dic(dic_caract)
    for year in dic_caract.keys():
        df = dic_caract[year]
        if 'gps' in df.columns:
            df = df.drop(columns=['gps'], axis=1)
    return df


def create_age(df):
    df['age'] = df['an'] - df['an_nais']

    return df


def create_age_cls(df):
    # partially inspired from https://www.cerema.fr/system/files/documents/2017/11/rapport_classes_age_version_web_14032017_cle73f1e2.pdf
    # (Accidentalité et classes d'âge - Analyse des données 2011-2013 du fichier BAAC - Rapport de mars 2017
    df['age_cls'] = pd.cut(df['age'], bins=[df['age'].min() - 1, 15, 25, 45, 65, df['age'].max()],
                           labels=[0, 1, 2, 3, 4])

    return df


def create_datetime(df):
    df['hr'] = [hrmn[0] + hrmn[1] for hrmn in df.hrmn]
    df['mn'] = [hrmn[3] + hrmn[4] for hrmn in df.hrmn]
    dic1 = {'an': 'year', 'mois': 'month', 'jour': 'day', 'hr': 'hour', 'mn': 'minute'}
    dic2 = {'year': 'an', 'month': 'mois', 'day': 'jour', 'hour': 'hr', 'minute': 'mn'}
    df = df.rename(dic1, axis=1)
    df["datetime"] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']], errors='coerce')
    df = df.rename(dic2, axis=1)
    df = df.drop(columns=['hr', 'mn'], axis=1)

    return df


def create_grav_lbl(df):
    labels = ['Indemne', 'Tué', 'Blessé hospitalisé', 'Blessé léger']
    df['grav_lbl'] = [labels[grav - 1] for grav in df.grav]

    return df


def create_joursem(df):
    df['joursem'] = df["datetime"].dt.dayofweek
    # df['joursem'] = df['joursem'].replace([0, 1, 2, 3, 4, 5, 6],
    #                                       ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'])
    return df


def clean_col_dep(df, verbose):
    if verbose: print(f"Départements avant nettoyage : \n{df.sort_values(by='dep').dep.unique()}")

    df['dep'] = [get_dep_code(dep) for dep in df.dep]

    if verbose: print(f"Départements après nettoyage : \n{df.sort_values(by='dep').dep.unique()}")

    return df


def merge_dataframes(df_usagers, df_caract, df_vehic, df_lieux):
    """"
    Merges the 4 dataframes in input into a single one
    """
    df = df_usagers
    df = df.merge(on=['Num_Acc'], right=df_caract, how='left')
    df = df.merge(on='Num_Acc', right=df_lieux, how='left')
    if 'id_vehicule' in df_vehic.columns:
        df = df.merge(on=['Num_Acc', 'id_vehicule', 'num_veh'], right=df_vehic, how='left')
    else:
        df = df.merge(on=['Num_Acc', 'num_veh'], right=df_vehic, how='left')
    return df


def get_work_df(start_year, end_year, verbose=0):
    # load data into dictionnaries
    dic_usagers = load_usagers(start_year, end_year)
    dic_caract = load_caract(start_year, end_year)
    dic_vehic = load_vehicules(start_year, end_year)
    dic_lieux = load_lieux(start_year, end_year)

    # Preprocessings pour la construction de : df_usagers, df_caract, df_vehic, df_lieux
    if verbose: print(f"\nusagers :")
    df_usagers = preproc_usagers(dic_usagers, verbose)
    if verbose: print(f"\ncaractéristiques :")
    df_caract = preproc_caract(dic_caract, verbose)
    if verbose: print(f"\nvéhicules :")
    df_vehic = preproc_vehic(dic_vehic, verbose)
    if verbose: print(f"\nlieux :")
    df_lieux = preproc_lieux(dic_lieux, verbose)

    # Merge dans un seul DataFrame
    df = merge_dataframes(df_usagers=df_usagers, df_caract=df_caract, df_vehic=df_vehic, df_lieux=df_lieux)

    return [df, dic_usagers, dic_caract, dic_lieux, dic_vehic]


def get_dep_code(dep):
    dep_code = dep
    if len(dep) == 1:
        dep_code = "0" + dep
    if len(dep) == 3 and dep[-1] == "0":
        dep_code = dep[0:2]
    if (dep == '201') or (dep == '2A'): dep_code = '20'
    if (dep == '202') or (dep == '2B'): dep_code = '20'

    return dep_code


def clean_nbv(df):
    df['nbv'] = [-1 if nbv > 6 else nbv for nbv in df.nbv]

    return df


def clean_actp(df):
    df.actp = df.actp.replace(to_replace=[' -1', 'A', 'B'], value=[-1, 10, 11])

    return df

def clean_etatp(df):
    df.etatp = df.etatp.replace(to_replace=[0], value=[-1])

    return df

def clean_catv(df):
    df['catv'] = [catv if (catv in [7, 33, 10, 2, 30, 1]) else -1 for catv in df.catv]

    return df


def clean_catu(df):
    df['catu'] = df['catu'].replace(to_replace=[4], value=[-1])

    return df


def clean_circ(df):
    df['circ'] = df['circ'].replace(to_replace=[0], value=[-1])

    return df


def clean_senc(df):
    df.senc = df.senc.replace(to_replace=[0, 3], value=-1)

    return df


def clean_hrmn(df):
    df['hrmn'] = [get_hh_mn(chaine) for chaine in df.hrmn]

    return df


def drop_lines_with_null(df, verbose):
    if verbose:
        print("Suppression des lignes avec Null : ")
        nb_bef = df.shape[0]
        print(f"Nombre de lignes avant : {nb_bef}")
    df = df.dropna(axis=0, how='any')
    if verbose:
        nb_aft = df.shape[0]
        print(f"Nombre de lignes après : {nb_aft}")
        print(f"Taux de perte : {(nb_bef - nb_aft) / nb_aft * 100:.2f} %")

    return df


def drop_columns_from_df(df, columns, verbose):
    for col in columns:
        if col in df.columns:
            df = df.drop(columns=col, axis=1)
    if verbose:
        for col in columns:
            if not (col in df.columns):
                print(f"Colonne {col} supprimée")

    return df


def get_hh_mn(chaine):
    if len(chaine) == 1: return "00:0" + chaine
    if len(chaine) == 2: return "00:" + chaine
    if len(chaine) == 3: return "0" + chaine[0] + ":00"
    if len(chaine) == 4: return f"{chaine[0]}{chaine[1]}:{chaine[2]}{chaine[3]}"
    if len(chaine) > 4: return chaine


def set_target_first_column(df, verbose):
    col = df.pop("grav")
    df.insert(0, col.name, col)
    if verbose:
        print("'grav' has been set as first column")
        df.head()
    return df


def display_stats_data_load(dic_usagers, dic_caract, dic_lieux, dic_vehic, start_year, end_year):
    dic = {'usagers': dic_usagers, 'caract': dic_caract, 'lieux': dic_lieux, 'vehic': dic_vehic}

    for key in dic.keys():
        print(f"{key} : \n")
        nb_lin = []
        nb_col = []

        for year in range(start_year, end_year + 1):
            dic_data = dic[key]
            df_tmp = dic_data[year]
            nb_lin.append(df_tmp.shape[0])
            nb_col.append(df_tmp.shape[1])
            print(f'{key} {year} : {df_tmp.shape[0]} lignes x {df_tmp.shape[1]} colonnes')

        print(f"\nnombre de lignes min : {min(nb_lin)}")
        print(f"nombre de lignes max : {max(nb_lin)}\n")


def encode_dummies_col(df, col, verbose):
    df_encoded = df.join(pd.get_dummies(df[col], prefix=col))
    df_encoded = df_encoded.drop(columns=[col], axis=1)
    if verbose: print(f"Column {col} has been dummies encoded")

    return df_encoded


def encode_grav(df, verbose):
    df['grav'] = df['grav'].replace(to_replace=[[1, 4], [2, 3]], value=[0, 1]).astype('int')
    if verbose: print(f"column grav encoded into 2 classes")

    return df


def train_test_split_along_time(data, target, year):
    filter_train = data.an < year
    filter_test = data.an >= year
    X_train = data[filter_train]
    y_train = target[filter_train]
    X_test = data[filter_test]
    y_test = target[filter_test]

    return X_train, y_train, X_test, y_test


def get_train_valid_test_data(run_type, columns=None):
    if run_type == 'dev': file_train, file_test = DF_DEV_TRAIN_PATH, DF_DEV_TEST_PATH
    if run_type == 'prd': file_train, file_test = DF_PRD_TRAIN_PATH, DF_PRD_TEST_PATH

    df_train, df_test = pd.read_pickle(f'./{file_train}'), pd.read_pickle(f'./{file_test}')

    data_train, X_test = df_train.iloc[:, 1:], df_test.iloc[:, 1:]

    target_train, y_test = df_train['grav'], df_test['grav']

    if not (columns is None): data_train, X_test = data_train[columns], X_test[columns]

    X_train, X_valid, y_train, y_valid, = train_test_split(data_train, target_train, test_size=0.2, random_state=222)

    return X_train, y_train, X_valid, y_valid, X_test, y_test


def get_data_resampled(X, y, verbose=0):
    sampler = SMOTEN(sampling_strategy='auto', k_neighbors=5, n_jobs=-1)

    start_time = time.time()
    X_rs, y_rs = sampler.fit_resample(X, y)
    if 'actp' in X.columns: X_rs['actp'] = X_rs['actp'].astype('int')
    if 'dep' in X.columns: X_rs['dep'] = X_rs['dep'].astype('int')

    if verbose:
        print(f"--- Smote applied in %s seconds ---" % (time.time() - start_time))
        print("Classes cardinality after resampling :")
        print(y_rs.value_counts())
        print(f"X shape : {X.shape} -> {X_rs.shape}")
        print(f"y shape : {y.shape} -> {y_rs.shape}")

    return X_rs, y_rs


def plot_data_augmentation(y, y_rs):
    s_1 = [len(y[y == 1]), len(y_rs[y_rs == 1])]
    s_0 = [len(y[y == 0]), len(y_rs[y_rs == 0])]

    df_tmp = pd.DataFrame({'Classe 1': s_1, 'Classe 0': s_0}, index=['Original', 'Après SMOTE'])
    df_tmp.plot(kind='bar', stacked=True, color=['teal', 'powderblue'],
                title="Compositions du dataset avant et après application de SMOTE",
                rot=0);
