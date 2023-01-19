import pandas as pd


def load_vehic_immat(folder_path, start_year, end_year):
    """Retourne les données dans un dictionnaire de dataframes dont la clé est l'année au format entier

    ex : vehic = load_vehicles(2019, 2021)
    les données de l'années 2020 sont accessibles vehic[2020]

    Id_accident : Numéro d'identifiant de l’accident
    Lettre Conventionnelle Véhicule : Identifiant de chaque véhicule impliqué dans un même accident – Code alpha
    Année : Année de l'accident
    Lieu Admin Actuel - Territoire Nom : 'Métropole', 'DOM', ou 'Autres OM'
    Type Accident - Libellé (old) : accident léger, mortel, ou grave
    CNIT : numéro d’identification national associé à chaque type, variante et version (TVV) de chaque réception communautaire de véhicules
    Catégorie véhicule : Cyclo, Moto légère, moto lourdez, VT, VU, PL, Autres
    Age véhicule : Age du véhicule à partir de la date de 1ère mise en circulation jusqu’à la date de l’accident

    """
    vehic = {}
    for year in range(start_year, end_year + 1):
        if year == 2009:
            vehic[2009] = pd.read_csv(folder_path + '2009.csv', sep=';')
        if year == 2010:
            vehic[2010] = pd.read_csv(folder_path + '2010.csv', sep=';')
        if year == 2011:
            vehic[2011] = pd.read_csv(folder_path + '2011.csv', sep=';')
        if year == 2012:
            vehic[2012] = pd.read_csv(folder_path + '2012.csv', sep=';')
        if year == 2013:
            vehic[2013] = pd.read_csv(folder_path + '2013.csv', sep=';')
        if year == 2014:
            vehic[2014] = pd.read_csv(folder_path + '2014.csv', sep=';')
        if year == 2015:
            vehic[2015] = pd.read_csv(folder_path + '2015.csv', sep=';')
        if year == 2016:
            vehic[2016] = pd.read_csv(folder_path + '2016.csv', sep=';')
        if year == 2017:
            vehic[2017] = pd.read_csv(folder_path + 'usagers-2017.csv', sep=';')
        if year == 2018:
            vehic[2018] = pd.read_csv(folder_path + 'usagers-2018.csv', sep=';')
        if year == 2019:
            vehic[2019] = pd.read_csv(folder_path + 'usagers-2019.csv', sep=';')
        if year == 2020:
            vehic[2020] = pd.read_csv(folder_path + 'usagers-2020.csv', sep=';')
        if year == 2021:
            vehic[2021] = pd.read_csv(folder_path + 'usagers-2021.csv', sep=';')

    return vehic


def load_caract(folder_path, start_year, end_year):
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
    for year in range(start_year, end_year + 1):
        if year == 2005:
            caract[2005] = pd.read_csv(folder_path + 'caracteristiques_2005.csv', sep=',', encoding='ISO-8859-1')
        if year == 2006:
            caract[2006] = pd.read_csv(folder_path + 'caracteristiques_2006.csv', sep=',', encoding='ISO-8859-1')
        if year == 2007:
            caract[2007] = pd.read_csv(folder_path + 'caracteristiques_2007.csv', sep=',', encoding='ISO-8859-1')
        if year == 2008:
            caract[2008] = pd.read_csv(folder_path + 'caracteristiques_2008.csv', sep=',', encoding='ISO-8859-1')
        if year == 2009:
            caract[2009] = pd.read_csv(folder_path + 'caracteristiques_2009.csv', sep='\t', encoding='ISO-8859-1')
        if year == 2010:
            caract[2010] = pd.read_csv(folder_path + 'caracteristiques_2010.csv', sep=',', encoding='ISO-8859-1')
        if year == 2011:
            caract[2011] = pd.read_csv(folder_path + 'caracteristiques_2011.csv', sep=',', encoding='ISO-8859-1')
        if year == 2012:
            caract[2012] = pd.read_csv(folder_path + 'caracteristiques_2012.csv', sep=',', encoding='ISO-8859-1')
        if year == 2013:
            caract[2013] = pd.read_csv(folder_path + 'caracteristiques_2013.csv', sep=',', encoding='ISO-8859-1')
        if year == 2014:
            caract[2014] = pd.read_csv(folder_path + 'caracteristiques_2014.csv', sep=',', encoding='ISO-8859-1')
        if year == 2015:
            caract[2015] = pd.read_csv(folder_path + 'caracteristiques_2015.csv', sep=',', encoding='ISO-8859-1')
        if year == 2016:
            caract[2016] = pd.read_csv(folder_path + 'caracteristiques_2016.csv', sep=',', encoding='ISO-8859-1')
        if year == 2017:
            caract[2017] = pd.read_csv(folder_path + 'caracteristiques-2017.csv', sep=',', encoding='ISO-8859-1')
        if year == 2018:
            caract[2018] = pd.read_csv(folder_path + 'caracteristiques-2018.csv', sep=',', encoding='ISO-8859-1')
        if year == 2019:
            caract[2019] = pd.read_csv(folder_path + 'caracteristiques-2019.csv', sep=';')
        if year == 2020:
            caract[2020] = pd.read_csv(folder_path + 'caracteristiques-2020.csv', sep=';')
        if year == 2021:
            caract[2021] = pd.read_csv(folder_path + 'carcteristiques-2021.csv', sep=';')

    return caract


def load_lieux(folder_path, start_year, end_year):
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
    for year in range(start_year, end_year + 1):
        if year == 2005:
            lieux[2005] = pd.read_csv(folder_path + 'lieux_2005.csv', sep=',')
        if year == 2006:
            lieux[2006] = pd.read_csv(folder_path + 'lieux_2006.csv', sep=',')
        if year == 2007:
            lieux[2007] = pd.read_csv(folder_path + 'lieux_2007.csv', sep=',')
        if year == 2008:
            lieux[2008] = pd.read_csv(folder_path + 'lieux_2008.csv', sep=',')
        if year == 2009:
            lieux[2009] = pd.read_csv(folder_path + 'lieux_2009.csv', sep=',')
        if year == 2010:
            lieux[2010] = pd.read_csv(folder_path + 'lieux_2010.csv', sep=',')
        if year == 2011:
            lieux[2011] = pd.read_csv(folder_path + 'lieux_2011.csv', sep=',')
        if year == 2012:
            lieux[2012] = pd.read_csv(folder_path + 'lieux_2012.csv', sep=',')
        if year == 2013:
            lieux[2013] = pd.read_csv(folder_path + 'lieux_2013.csv', sep=',')
        if year == 2014:
            lieux[2014] = pd.read_csv(folder_path + 'lieux_2014.csv', sep=',')
        if year == 2015:
            lieux[2015] = pd.read_csv(folder_path + 'lieux_2015.csv', sep=',')
        if year == 2016:
            lieux[2016] = pd.read_csv(folder_path + 'lieux_2016.csv', sep=',')
        if year == 2017:
            lieux[2017] = pd.read_csv(folder_path + 'lieux-2017.csv', sep=',')
        if year == 2018:
            lieux[2018] = pd.read_csv(folder_path + 'lieux-2018.csv', sep=',')
        if year == 2019:
            lieux[2019] = pd.read_csv(folder_path + 'lieux-2019.csv', sep=';')
        if year == 2020:
            lieux[2020] = pd.read_csv(folder_path + 'lieux-2020.csv', sep=';')
        if year == 2021:
            lieux[2021] = pd.read_csv(folder_path + 'lieux-2021.csv', sep=';')

    return lieux


def load_usagers(folder_path, start_year, end_year):
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
    for year in range(start_year, end_year + 1):
        if year == 2005:
            usagers[2005] = pd.read_csv(folder_path + 'usagers_2005.csv', sep=',')
        if year == 2006:
            usagers[2006] = pd.read_csv(folder_path + 'usagers_2006.csv', sep=',')
        if year == 2007:
            usagers[2007] = pd.read_csv(folder_path + 'usagers_2007.csv', sep=',')
        if year == 2008:
            usagers[2008] = pd.read_csv(folder_path + 'usagers_2008.csv', sep=',')
        if year == 2009:
            usagers[2009] = pd.read_csv(folder_path + 'usagers_2009.csv', sep=',')
        if year == 2010:
            usagers[2010] = pd.read_csv(folder_path + 'usagers_2010.csv', sep=',')
        if year == 2011:
            usagers[2011] = pd.read_csv(folder_path + 'usagers_2011.csv', sep=',')
        if year == 2012:
            usagers[2012] = pd.read_csv(folder_path + 'usagers_2012.csv', sep=',')
        if year == 2013:
            usagers[2013] = pd.read_csv(folder_path + 'usagers_2013.csv', sep=',')
        if year == 2014:
            usagers[2014] = pd.read_csv(folder_path + 'usagers_2014.csv', sep=',')
        if year == 2015:
            usagers[2015] = pd.read_csv(folder_path + 'usagers_2015.csv', sep=',')
        if year == 2016:
            usagers[2016] = pd.read_csv(folder_path + 'usagers_2016.csv', sep=',')
        if year == 2017:
            usagers[2017] = pd.read_csv(folder_path + 'usagers-2017.csv', sep=',')
        if year == 2018:
            usagers[2018] = pd.read_csv(folder_path + 'usagers-2018.csv', sep=',')
        if year == 2019:
            usagers[2019] = pd.read_csv(folder_path + 'usagers-2019.csv', sep=';')
        if year == 2020:
            usagers[2020] = pd.read_csv(folder_path + 'usagers-2020.csv', sep=';')
        if year == 2021:
            usagers[2021] = pd.read_csv(folder_path + 'usagers-2021.csv', sep=';')

    return usagers


def load_vehicules(folder_path, start_year, end_year):
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
    for year in range(start_year, end_year + 1):
        if year == 2005:
            vehic[2005] = pd.read_csv(folder_path + 'vehicules_2005.csv', sep=',')
        if year == 2006:
            vehic[2006] = pd.read_csv(folder_path + 'vehicules_2006.csv', sep=',')
        if year == 2007:
            vehic[2007] = pd.read_csv(folder_path + 'vehicules_2007.csv', sep=',')
        if year == 2008:
            vehic[2008] = pd.read_csv(folder_path + 'vehicules_2008.csv', sep=',')
        if year == 2009:
            vehic[2009] = pd.read_csv(folder_path + 'vehicules_2009.csv', sep=',')
        if year == 2010:
            vehic[2010] = pd.read_csv(folder_path + 'vehicules_2010.csv', sep=',')
        if year == 2011:
            vehic[2011] = pd.read_csv(folder_path + 'vehicules_2011.csv', sep=',')
        if year == 2012:
            vehic[2012] = pd.read_csv(folder_path + 'vehicules_2012.csv', sep=',')
        if year == 2013:
            vehic[2013] = pd.read_csv(folder_path + 'vehicules_2013.csv', sep=',')
        if year == 2014:
            vehic[2014] = pd.read_csv(folder_path + 'vehicules_2014.csv', sep=',')
        if year == 2015:
            vehic[2015] = pd.read_csv(folder_path + 'vehicules_2015.csv', sep=',')
        if year == 2016:
            vehic[2016] = pd.read_csv(folder_path + 'vehicules_2016.csv', sep=',')
        if year == 2017:
            vehic[2017] = pd.read_csv(folder_path + 'vehicules-2017.csv', sep=',')
        if year == 2018:
            vehic[2018] = pd.read_csv(folder_path + 'vehicules-2018.csv', sep=',')
        if year == 2019:
            vehic[2019] = pd.read_csv(folder_path + 'vehicules-2019.csv', sep=';')
        if year == 2020:
            vehic[2020] = pd.read_csv(folder_path + 'vehicules-2020.csv', sep=';')
        if year == 2021:
            vehic[2021] = pd.read_csv(folder_path + 'vehicules-2021.csv', sep=';')

    return vehic
