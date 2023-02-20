import pandas as pd
import numpy as np
from category_encoders import TargetEncoder
from sklearn.preprocessing import OneHotEncoder

DIR_DATA_GOUV = ".\\data\\data_gouv_fr\\"
DIR_DATA_KAGG = ".\\data\\kaggle\\"
def generate_pickle(df, filename):
    df.to_pickle(f"./{filename}")


def load_proj_df(start_year, end_year, chk=False):
    df, dic_usagers, dic_caract, dic_lieux, dic_vehic = get_work_df(start_year, end_year, chk)
    if chk:
        display_stats_data_load(dic_usagers, dic_caract, dic_lieux, dic_vehic, start_year, end_year)

        # rmv col related to geographical info
        df = drop_columns_from_df(df, ['com', 'adr', 'lat', 'long', 'pr', 'pr1'], chk)
        # rmv col not known before the accident
        df = drop_columns_from_df(df, ['obs', 'obsm', 'choc', 'manv'], chk)

        df = rmv_col_too_much_null(df, 0.08, chk)
        df = clean_categ_not_specified(df)
        df = drop_lines_with_null(df, chk)
        df = create_age(df)
        df = create_age_cls(df)
        df = clean_col_dep(df, True)
        df = clean_nbv(df)
        df = clean_actp(df)
        df = clean_catv(df)
        df = clean_hrmn(df)
        df = create_datetime(df)
        df = create_joursem(df)
        df = create_grav_lbl(df)
        df = drop_columns_from_df(df, ['an_nais'], chk)
        df = drop_columns_from_df(df, ['age'], chk)
        df = drop_columns_from_df(df, ['grav_lbl'], chk)    # drop column used only for data pre-analysis
        df = drop_columns_from_df(df, ['Num_Acc'], chk)
        df = drop_columns_from_df(df, ['datetime'], chk)
        # df = drop_columns_from_df(df, ['an'], chk)
        df = drop_columns_from_df(df, ['num_veh'], chk)
        df = drop_columns_from_df(df, ['jour'], chk)
        df = drop_columns_from_df(df, ['hrmn'], chk)
        df = encode_grav(df, chk)
        df = set_target_first_column(df, chk)

        if chk: df.info(verbose=True, show_counts=True)

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


def load_data_kagg():
    """Retourne les données dans un dictionnaire de DataFrames dont la clé est le type de donnée

    ex : my_dict = load_data_kagg(my_folder)
    les données des usagers sont accessibles via la clé 'usagers' : df_usagers = my_dict['usagers']
    les clés disponibles sont :
     - 'caracts'
     - 'lieux'
     - 'usagers'
     - 'vacances'
     - 'vehics'
    """
    data_dict = {'caract': pd.read_csv(DIR_DATA_KAGG + 'caracteristics.csv', sep=',', encoding='ISO-8859-1'),
                 'lieux': pd.read_csv(DIR_DATA_KAGG + 'places.csv', sep=','),
                 'usagers': pd.read_csv(DIR_DATA_KAGG + 'users.csv', sep=','),
                 'vacances': pd.read_csv(DIR_DATA_KAGG + 'holidays.csv', sep=','),
                 'vehic': pd.read_csv(DIR_DATA_KAGG + 'vehicles.csv', sep=',')
                 }
    return data_dict


def get_labels(varname, value):
    if varname == 'lum':
        if value == 1:
            return 'Plein jour'
        if value == 2:
            return 'Crépuscule ou aube'
        if value == 3:
            return 'Nuit sans éclairage public'
        if value == 4:
            return 'Nuit avec éclairage public non allumé'
        if value == 5:
            return 'Nuit avec éclairage public allumé'

    if varname == 'grav':
        if value == 1:
            return 'Indemne'
        if value == 2:
            return 'Tué'
        if value == 3:
            return 'Blessé hospitalisé'
        if value == 4:
            return 'Blessé léger'

    if varname == 'catu':
        if value == 1:
            return 'Conducteur'
        if value == 2:
            return 'Passager'
        if value == 3:
            return 'Piéton'

    if varname == 'sexe':
        if value == 1:
            return 'Masculin'
        if value == 2:
            return 'Féminin'

    if varname == 'agg':
        if value == 1:
            return 'hors agglomération'
        if value == 2:
            return 'en agglomération'

    if varname == 'int':
        if value == 1:
            return 'Hors intersection'
        if value == 2:
            return 'Intersection en X'
        if value == 3:
            return 'Intersection en T'
        if value == 4:
            return 'Intersection en Y'
        if value == 5:
            return 'Intersection à plus de 4 branches'
        if value == 6:
            return 'Giratoire'
        if value == 7:
            return 'Place'
        if value == 8:
            return 'Passage à niveau'
        if value == 9:
            return 'Autre intersection'

    if varname == 'atm':
        if value == '-1':
            return 'Non renseigné'
        if value == '1':
            return 'Normale'
        if value == '2':
            return 'Pluie légère'
        if value == '3':
            return 'Pluie forte'
        if value == '4':
            return 'Neige - grêle'
        if value == '5':
            return 'Brouillard - fumée'
        if value == '6':
            return 'Vent fort - tempête'
        if value == '7':
            return 'Temps éblouissant'
        if value == '8':
            return 'Temps couvert'
        if value == '9':
            return 'Autre'

    if varname == 'col':
        if value == '-1':
            return 'Non renseigné'
        if value == '1':
            return 'Deux véhicules - frontale'
        if value == '2':
            return "Deux véhicules - par l'arrière"
        if value == '3':
            return 'Deux véhicules - par le côté'
        if value == '4':
            return 'Trois véhicules et plus - en chaîne'
        if value == '5':
            return 'Trois véhicules et plus - collisions multiples'
        if value == '6':
            return 'Autre collision'
        if value == '7':
            return 'Sans collision'

    if varname == 'trajet':
        if value == '-1':
            return 'Non renseigné'
        if value == '0':
            return 'Non renseigné'
        if value == '1':
            return 'Domicile - travail'
        if value == '2':
            return 'Domicile - école'
        if value == '3':
            return 'Courses - achats'
        if value == '4':
            return 'Utilisation professionnelle'
        if value == '5':
            return 'Promende - loisirs'
        if value == '9':
            return 'Autre'

    if (varname == 'secu1') or (varname == 'secu2') or (varname == 'secu3'):
        if value == -1:
            return 'Non renseigné'
        if value == 0:
            return 'Aucun équipement'
        if value == 1:
            return 'Ceinture'
        if value == 2:
            return 'Casque'
        if value == 3:
            return 'Dispositif enfants'
        if value == 4:
            return 'Gilet réfléchissant'
        if value == 5:
            return 'Airbag (2RM/3RM)'
        if value == 6:
            return 'Gants (2RM/3RM)'
        if value == 7:
            return 'Non déterminable'
        if value == 8:
            return 'Autre'

    if varname == 'locp':
        if value == '-1':
            return 'Non renseigné'
        if value == '0':
            return 'Sans objet'
        if value == '1':
            return 'Sur chaussée - A +50 du pass piéton'
        if value == '2':
            return 'Sur chaussée - A -50 du pass piéton'
        if value == '3':
            return 'Sur pass piéton - Sans signalisation lumineuse'
        if value == '4':
            return 'Sur pass piéton - Avec signalisation lumineuse'
        if value == '5':
            return 'Sur trottoir'
        if value == '6':
            return 'Sur accotement'
        if value == '7':
            return 'Sur refuge ou BAU'
        if value == '8':
            return 'Sur contre allée'
        if value == '9':
            return 'Inconnue'

    if varname == 'actp':
        if value == '-1':
            return 'Non renseigné'
        if value == '0':
            return 'Se déplaçant - Non renseigné ou sans objet'
        if value == '1':
            return 'Se déplaçant - Sens véhicule ou heurtant'
        if value == '2':
            return 'Se déplaçant - Sens inverse du véhicule'
        if value == '3':
            return 'Traversant'
        if value == '4':
            return 'Masqué'
        if value == '5':
            return 'Jouant - courant'
        if value == '6':
            return 'Avec animal'
        if value == '9':
            return 'Autre'
        if value == 'A':
            return 'Monte/descend du véhicule'
        if value == 'B':
            return 'Inconnue'

    if varname == 'etatp':
        if value == '-1':
            return 'Non renseigné'
        if value == '1':
            return 'Seul'
        if value == '2':
            return 'Accompagné'
        if value == '3':
            return 'En groupe'


# DATA PRE-PROCESSING --------------------------------------------
def get_cl_age(age):
    if age <= 25:
        return '0-25'
    if 25 < age <= 37:
        return '26-37'
    if 37 < age <= 53:
        return '38-53'
    if 53 < age:
        return '>53'


def preproc_usagers(dic_usagers, chk):
    df_usagers = concat_df_from_dict(dic_usagers, chk)
    df_usagers = manage_duplicated(df_usagers, chk)

    return df_usagers


def preproc_caract(dic_caract, chk):
    df_caract = concat_df_from_dict(dic_caract, chk)
    df_caract = manage_duplicated(df_caract, chk)
    df_caract['an'] = df_caract['an'].replace(
        to_replace=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        value=[2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
               2015, 2016, 2017, 2018])

    return df_caract


def preproc_vehic(dic_vehic, chk):
    df_vehic = concat_df_from_dict(dic_vehic, chk)
    df_vehic = manage_duplicated(df_vehic, chk)
    df_vehic = manage_vehic_duplicated(df_vehic, chk)

    return df_vehic


def preproc_lieux(dic_lieux, chk):
    df_lieux = concat_df_from_dict(dic_lieux, chk)
    df_lieux = manage_duplicated(df_lieux, chk)

    return df_lieux


def concat_df_from_dict(dic, chk):
    [start_year, end_year] = get_start_end_years_from_dic(dic)
    for year in dic.keys():
        df = dic[year]
        if year == start_year:
            df_final = df
        else:
            df_final = pd.concat([df_final, df], ignore_index=True, axis=0)
    if chk:
        chk_concat(dic, df_final)
    return df_final


def manage_duplicated(df, chk):
    if chk: print(f"nombre de doublons avant traîtement : {df.duplicated().sum()}")
    df = df.drop_duplicates()
    if chk: print(f"nombre de doublons après traîtement : {df.duplicated().sum()}")

    return df


def manage_not_specified(df):
    df = df.replace(to_replace=['-1', ' -1'], value='-1')
    return df


def clean_categ_not_specified(df):
    col_minusone = get_col_minusone_allowed()
    col_to_chk = []
    for col in col_minusone:
        if col in df.columns:
            col_to_chk.append(col)
    df[col_to_chk] = df[col_to_chk].replace(to_replace=np.nan, value=-1)

    return df


def get_col_minusone_allowed():
    return ['place', 'catu', 'grav', 'sexe', 'trajet', 'secu', 'locp', 'actp',
            'etatp', 'secu1', 'secu2', 'secu3', 'lum', 'agg', 'int', 'atm',
            'col', 'catr', 'circ', 'nbv', 'vosp', 'prof', 'plan', 'lartpc',
            'larrout', 'surf', 'infra', 'situ', 'env1', 'vma', 'senc', 'catv',
            'occutc', 'obs', 'obsm', 'choc', 'manv', 'motor']


def replace_null_mode(df, chk):
    cols = df.columns[df.isnull().any()]
    k = 0
    for col in cols:
        mode = df[col].mode()[0]
        df = df.fillna(mode)
        # df_all = df_all.fillna(df_all[col].value_counts().index[0])  # faster than mode()[0]
        k += 1
        if chk: print(f"{col}\t-> ok (nan replaced with {mode}) \t- {len(cols) - k} columns remaining...")

    return df


def rmv_col_too_much_null(df, threshold, chk):
    rate_missing = df.isnull().sum() / len(df)
    df_miss = pd.DataFrame({'column_name': df.columns, 'rate_missing': rate_missing})
    df_miss.sort_values('rate_missing', inplace=True, ascending=False)
    to_drop = df_miss[df_miss.rate_missing >= threshold]['column_name']
    df = df.drop(columns=to_drop.index, axis=1)

    if chk:
        df_miss.rate_missing *= 100
        print(f"Colonnes supprimées : {to_drop.index}")
        print(f"\n{df_miss}")
    return df


def manage_vehic_duplicated(df_vehic, chk):
    if chk:
        df_vehic_dupl = df_vehic.duplicated(['Num_Acc', 'num_veh'])
        print(
            f"Véhicules en doublons vis à vis de la clé fonctionnelle avant traitement : {df_vehic_dupl[df_vehic_dupl].sum()}")

    df_vehic.drop_duplicates(['Num_Acc', 'num_veh'], keep='first', inplace=True)

    if chk:
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


def rmv_outliers(column, df):
    if column == "an_nais":
        df = df.drop(df[(df.an_nais == 1)].index)
    if column == "age":
        df = df.drop(df[(df.age > 120)].index)

    return df


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
    df['age_cls'] = pd.cut(df['age'], bins=[df['age'].min()-1, 15, 25, 45, 65, df['age'].max()], labels=[0, 1, 2, 3, 4])

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


def clean_col_dep(df, chk):
    if chk: print(f"Départements avant nettoyage : \n{df.sort_values(by='dep').dep.unique()}")

    df['dep'] = [clean_dep(dep) for dep in df.dep]

    if chk: print(f"Départements après nettoyage : \n{df.sort_values(by='dep').dep.unique()}")

    return df


def merge_dataframes(df_usagers, df_caract, df_vehic, df_lieux):
    df = df_usagers
    df = df.merge(on=['Num_Acc'], right=df_caract, how='left')
    df = df.merge(on='Num_Acc', right=df_lieux, how='left')
    if 'id_vehicule' in df_vehic.columns:
        df = df.merge(on=['Num_Acc', 'id_vehicule', 'num_veh'], right=df_vehic, how='left')
    else:
        df = df.merge(on=['Num_Acc', 'num_veh'], right=df_vehic, how='left')
    return df


def get_work_df(start_year, end_year, sample_size=None, chk=False):
    # load data into dictionnaries
    dic_usagers = load_usagers(start_year, end_year)
    dic_caract = load_caract(start_year, end_year)
    dic_vehic = load_vehicules(start_year, end_year)
    dic_lieux = load_lieux(start_year, end_year)

    # Preprocessings pour la construction de : df_usagers, df_caract, df_vehic, df_lieux
    if chk: print(f"\nusagers :")
    df_usagers = preproc_usagers(dic_usagers, chk)
    if chk: print(f"\ncaractéristiques :")
    df_caract = preproc_caract(dic_caract, chk)
    if chk: print(f"\nvéhicules :")
    df_vehic = preproc_vehic(dic_vehic, chk)
    if chk: print(f"\nlieux :")
    df_lieux = preproc_lieux(dic_lieux, chk)

    # Merge dans un seul DataFrame
    df = merge_dataframes(df_usagers=df_usagers, df_caract=df_caract, df_vehic=df_vehic, df_lieux=df_lieux)

    return [df, dic_usagers, dic_caract, dic_lieux, dic_vehic]


def dep_codes_get():
    """
    source : https://fr.wikipedia.org/wiki/Num%C3%A9rotation_des_d%C3%A9partements_fran%C3%A7ais
    """
    dep_lst = []
    for k in range(1, 96):
        s = str(k)
        if len(s) == 1: s = "0" + s
        dep_lst.append(s)

    for k in range(971, 979):
        dep_lst.append(str(k))

    dep_lst.append('984')  # Terres Australes et Antarctiques Françaises
    dep_lst.append('986')  # Wallis et Fotuna
    dep_lst.append('987')  # Polynésie Française
    dep_lst.append('988')  # Nouvelle-Calédonie
    dep_lst.append('989')  # Ile de Clipperton

    dep_lst.append('2A')  # Corse-du-Sud
    dep_lst.append('2B')  # Haute-Corse
    dep_lst.append('69D')  # Rhône
    dep_lst.append('69M')  # Métropole de Lyon

    dep_lst.remove('20')

    return dep_lst


def clean_dep(dep):
    dep_clean = dep
    if len(dep) == 1:
        dep_clean = "0" + dep
    if len(dep) == 3 and dep[-1] == "0":
        dep_clean = dep[0:2]
    if (dep == '201') or (dep == '2A'): dep_clean = '20'
    if (dep == '202') or (dep == '2B'): dep_clean = '20'

    return dep_clean

def clean_nbv(df):
    df['nbv'] = [-1 if nbv > 6 else nbv for nbv in df.nbv]

    return df

def clean_actp(df):
    df.actp = df.actp.replace(to_replace=[' -1', 'A', 'B'], value=[-1, 10, 11])

    return df
def clean_catv(df):
    df['catv'] = [catv if (catv in [7, 33, 10, 2, 30, 1]) else -1 for catv in df.catv]

    return df


def clean_senc(df):
    df.senc = df.senc.replace(to_replace=[0, 3], value=-1)

    return df


def clean_hrmn(df):
    df['hrmn'] = [get_hh_mn(chaine) for chaine in df.hrmn]

    return df


def drop_lines_with_null(df, chk):
    if chk:
        print("Suppression des lignes avec Null : ")
        nb_bef = df.shape[0]
        print(f"Nombre de lignes avant : {nb_bef}")
    df = df.dropna(axis=0, how='any')
    if chk:
        nb_aft = df.shape[0]
        print(f"Nombre de lignes après : {nb_aft}")
        print(f"Taux de perte : {(nb_bef - nb_aft) / nb_aft * 100:.2f} %")

    return df


def drop_columns_from_df(df, columns, chk):
    for col in columns:
        if col in df.columns:
            df = df.drop(columns=col, axis=1)
    if chk:
        for col in columns:
            if not (col in df.columns):
                print(f"Column {col} correctly dropped from DataFrame")

    return df


def get_hh_mn(chaine):
    if len(chaine) == 1: return "00:0" + chaine
    if len(chaine) == 2: return "00:" + chaine
    if len(chaine) == 3: return "0" + chaine[0] + ":00"
    if len(chaine) == 4: return f"{chaine[0]}{chaine[1]}:{chaine[2]}{chaine[3]}"
    if len(chaine) > 4: return chaine


def set_target_first_column(df, chk):
    col = df.pop("grav")
    df.insert(0, col.name, col)
    if chk:
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
            print(f'{key} {year} : {df_tmp.shape[1]} colonnes x {df_tmp.shape[0]} lignes')

        print(f"\nnombre de lignes min : {min(nb_lin)}")
        print(f"nombre de lignes max : {max(nb_lin)}")


def encode_dummies_col(df, col, chk):
    df_encoded = df.join(pd.get_dummies(df[col], prefix=col))
    df_encoded = df_encoded.drop(columns=[col], axis=1)
    if chk: print(f"Column {col} has been dummies encoded")

    return df_encoded

def encode_target_col(df, col, target, chk):
    encoder = TargetEncoder()
    df[f"{col}"] = encoder.fit_transform(df[col].astype('str'), target)
    # df = df.drop(columns=[col], axis=1)
    if chk: print(f"Column {col} has been target encoded")

    return df

def encode_grav(df, chk):
    df['grav'] = df['grav'].replace(to_replace=[[1, 4], [2, 3]], value=[0, 1]).astype('int')
    if chk : print(f"column grav encoded into 2 classes")

    return df

def train_test_split_along_time(data, target, year):
    filter_train = data.an < year
    filter_test = data.an >= year
    X_train = data[filter_train]
    y_train = target[filter_train]
    X_test = data[filter_test]
    y_test = target[filter_test]

    return X_train, y_train, X_test, y_test

def get_train_valid_test_data(filename_train, filename_test, columns=None):

    df_train = pd.read_pickle(f'./{filename_train}')
    df_test  = pd.read_pickle(f'./{filename_test}')

    data_train = df_train.iloc[:, 1:]
    target_train = df_train['grav']
    if not (columns==None): data_train = data_train[columns]

    data_test = df_test.iloc[:, 1:]
    target_test = df_test['grav']
    if not (columns==None): data_test = data_test[columns]

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test, = train_test_split(data_train, target_train, test_size=0.2, random_state=222)
    X_test_final, y_test_final = data_test, target_test

    return X_train, y_train, X_test, y_test, X_test_final, y_test_final