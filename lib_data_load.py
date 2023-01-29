import pandas as pd

DIR_DATA = ".\\data\\data_gouv_fr\\"
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
    dic_types = {'com':'str', 'atm':'str', 'col':'str'}
    for year in range(start_year, end_year + 1):
        car='_' if 2005 <= year <= 2016 else '-'
        if year==2009 :
            sep='\t'
        else:
            sep=',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2020:
            caract[year] = pd.read_csv(DIR_DATA + f'caracteristiques{car}{year}.csv', sep=sep, encoding='ISO-8859-1', dtype=dic_types)
        if year == 2021:
            caract[year] = pd.read_csv(DIR_DATA + f'carcteristiques{car}{year}.csv', sep=sep, encoding='ISO-8859-1', dtype=dic_types)
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
    dic_type = {'catr':'str', 'voie':'str', 'v1':'str','v2':'str', 'circ':'str', 'nbv':'str', 'vosp':'str', 'prof':'str', 'plan':'str',
                'lartpc':'str', 'surf':'str', 'infra':'str', 'situ':'str'}
    for year in range(start_year, end_year + 1):
        car='_' if 2005 <= year <= 2016 else '-'
        sep=',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            lieux[year] = pd.read_csv(DIR_DATA + f'lieux{car}{year}.csv', sep=sep, dtype=dic_type)
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
    dic_types = {'place':'str', 'trajet':'str', 'secu':'Int64', 'locp':'str', 'actp':'str', 'etatp':'str', 'an_nais':'Int64'}
    for year in range(start_year, end_year + 1):
        car='_' if 2005 <= year <= 2016 else '-'
        sep=',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            usagers[year] = pd.read_csv(DIR_DATA + f'usagers{car}{year}.csv', sep=sep, dtype=dic_types)
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
    dic_types = {'obs':'Int64', 'obsm':'Int64', 'choc':'Int64', 'manv':'Int64'}
    for year in range(start_year, end_year + 1):
        car='_' if 2005 <= year <= 2016 else '-'
        sep=',' if 2005 <= year <= 2018 else ';'
        if 2005 <= year <= 2021:
            vehic[year] = pd.read_csv(DIR_DATA + f'vehicules{car}{year}.csv', sep=sep, dtype=dic_types)
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
    data_dict = { 'caract'  : pd.read_csv(DIR_DATA + 'caracteristics.csv', sep=',', encoding='ISO-8859-1'),
                  'lieux'    : pd.read_csv(DIR_DATA + 'places.csv', sep=','),
                  'usagers'  : pd.read_csv(DIR_DATA + 'users.csv', sep=','),
                  'vacances' : pd.read_csv(DIR_DATA + 'holidays.csv', sep=','),
                  'vehic'    : pd.read_csv(DIR_DATA + 'vehicles.csv', sep=',')
                }
    return data_dict


