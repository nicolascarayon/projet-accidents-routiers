import pandas as pd

# Labels for Shapash smart explainer

dic_target = {0: 'Indemne - Blessé léger',
              1: 'Tué - Blessé hospitalisé'}

dic_features = {'grav': 'Gravité',
                'senc': 'Sens de circulation',
                'place': "Place de l'usager",
                'catu': "Catégorie de l'usager",
                'sexe': "sexe de l'usager",
                'trajet': 'Motif du déplacement',
                'locp': 'Localisation du piéton',
                'actp': 'Action du piéton',
                'etatp': 'Piéton seul?',
                'mois': 'Mois',
                'lum': 'Conditions de luminosité',
                'agg': 'Localisation',
                'int': 'Intersection',
                'atm': 'Conditions atmosphériques',
                'col': 'Type de collision',
                'dep': 'Département',
                'catr': 'Catégorie de route',
                'circ': 'Conditions de circulation',
                'nbv': 'Nombre de voies',
                'vosp': 'Voie réservée?',
                'prof': 'Profil de la route',
                'plan': 'Tracé en plan',
                'surf': 'Etat de la surface',
                'infra': 'Aménagement - Infrastructure',
                'situ': "Situation de l'accident",
                'catv': 'Catégorie de véhicule',
                'age_cls': "Classe d'âge",
                'joursem': 'Jour de la semaine'}

dic_preproc = [{'col': 'catv',
                'mapping': pd.Series(data=[-1, 1, 2, 7, 10, 30, 33],
                                     index=['Autres', 'Bicyclette', 'Cyclomoteur <50cm3', 'VL seul',
                                            'VU seul', 'Scooter <50cm3', 'Motocyclette >125cm3']),
                'data_type': 'object'},
               {'col': 'agg',
                'mapping': pd.Series(data=[1, 2], index=['Hors agglomération', 'En agglomération']),
                'data_type': 'object'},
               {'col': 'col',
                'mapping': pd.Series(data=[-1, 1, 2, 3, 4, 5, 6, 7],
                                     index=['Non renseigné', '2 véhic-frontale', "2 véhic-par l'arrière",
                                            '2 vehic-par le côté', '3 vehic et +- en chaine',
                                            '3 vehic et plus - collisions multiples',
                                            'Autre collision', 'Sans collision']),
                'data_type': 'object'},
               {'col': 'catr',
                'mapping': pd.Series(data=[1, 2, 3, 4, 5, 6, 7, 9],
                                     index=['Autoroute', 'Route nationale', 'Route départementale',
                                            'Voies communales', 'Hors réseau public', 'Parc de stationnement',
                                            'Routes de métropole urbaine', 'Autre']),
                'data_type': 'object'},
               {'col': 'catu',
                'mapping': pd.Series(data=[-1, 1, 2, 3], index=['Non renseigné', 'Conducteur', 'Passager', 'Piéton']),
                'data_type': 'object'},
               {'col': 'trajet',
                'mapping': pd.Series(data=[-1, 0, 1, 2, 3, 4, 5, 9],
                                     index=['Non renseigné', 'Non renseigné', 'Domicile-travail',
                                            'Domicile-école', 'Courses-achats', 'Utilisation professionnelle',
                                            'Promenade-Loisirs', 'Autre']),
                'data_type': 'object'},
               {'col': 'locp',
                'mapping': pd.Series(data=[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                     index=['Non renseigné', 'Sans objet', 'A + 50 m du passage piéton',
                                            'A – 50 m du passage piéton',
                                            'Sur passage piéton sans signalisation lumineuse',
                                            'Sur passage piéton avec signalisation lumineuse',
                                            'Sur trottoir', 'Sur accotement', 'Sur refuge ou BAU',
                                            'Sur contre allée', 'Inconnue', ]),
                'data_type': 'object'},
               {'col': 'circ',
                'mapping': pd.Series(data=[-1, 1, 2, 3, 4], index=['Non renseigné', 'A sens unique', 'Bidirectionnelle',
                                                                   'A chaussées séparées',
                                                                   'Avec voies d’affectation variable']),
                'data_type': 'object'},

               {'col': 'situ',
                'mapping': pd.Series(data=[-1, 0, 1, 2, 3, 4, 5, 6, 8], index=['Non renseigné', 'Aucun', 'Sur chaussée',
                                                                               'Sur bande d’arrêt d’urgence',
                                                                               'Sur accotement', 'Sur trottoir',
                                                                               'Sur piste cyclable',
                                                                               'Sur autre voie spéciale', 'Autres']),
                'data_type': 'object'},
               {'col': 'lum',
                'mapping': pd.Series(data=[1, 2, 3, 4, 5],
                                     index=['Plein jour', 'Crépuscule ou aube', 'Nuit sans éclairage public',
                                            'Nuit avec éclairage public non allumé',
                                            'Nuit avec éclairage public allumé']),
                'data_type': 'object'},
               {'col': 'age_cls',
                'mapping': pd.Series(data=[0, 1, 2, 3, 4], index=['0-15', '16-25', '26-45', '46-65', '66-']),
                'data_type': 'object'},
               ]

dic_catv = {-1: 'Autres',
            1: 'Bicyclette',
            2: 'Cyclomoteur <50cm3',
            7: 'VL seul',
            10: 'VU seul',
            30: 'Scooter <50cm3',
            33: 'Motocyclette >125cm3'}

dic_catr = {1: 'Autoroute',
            2: 'Route nationale',
            3: 'Route départementale',
            4: 'Voie communale',
            5: 'Hors réseau public',
            6: 'Parc de stationnement ouvert à la circulation publique',
            7: 'Routes de métropole urbaine',
            9: 'Autre'}

dic_lum = {1: 'Plein jour',
           2: 'Crépuscule ou aube',
           3: 'Nuit sans éclairage public',
           4: 'Nuit avec éclairage public non allumé',
           5: 'Nuit avec éclairage public allumé'}

dic_grav = {0: 'Indemne - Blessé léger',
            1: 'Tué - Blessé hospitalisé'}

dic_grav_sht = {0: "Non grave",
                1: "Grave"}

dic_pred_type = {0: "Bonne prédiction",
                 1: "Mauvaise prédiction"}

dic_catu = {'def': "Catégorie d'usager",
            1: 'Conducteur',
            2: 'passager',
            3: 'Piéton'}

dic_sexe = {1: 'Masculin',
            2: 'Féminin'}

dic_agg = {1: 'Hors agglomération',
           2: 'En agglomération'}

dic_int = {1: 'Hors intersection',
           2: 'Intersection en X',
           3: 'Intersection en T',
           4: 'Intersection en Y',
           5: 'Intersection à plus de 4 branches',
           6: 'Giratoire',
           7: 'Place',
           8: 'Passage à niveau',
           9: 'Autre intersection'}

dic_atm = {-1: 'Non renseigné',
           1: 'Normale',
           2: 'Pluie légère',
           3: 'Pluie forte',
           4: 'Neige - grêle',
           5: 'Brouillard - fumée',
           6: 'Vent fort - tempête',
           7: 'Temps éblouissant',
           8: 'Temps couvert',
           9: 'Autre'}

dic_circ = {-1:"Non renseigné",
            1:"A sens unique",
            2:"Bidirectionnelle",
            3:"A chaussée séparée",
            4:"Avec des voies d'affectation variable"}

dic_nbv = {-1:-1, 0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6}

dic_col = {-1: 'Non renseigné',
           1: 'Deux véhicules - frontale',
           2: "Deux véhicules - par l'arrière",
           3: 'Deux véhicules - par le côté',
           4: 'Trois véhicules et plus - en chaîne',
           5: 'Trois véhicules et plus - collisions multiples',
           6: 'Autre collision',
           7: 'Sans collision'}

dic_trajet = {-1: 'Non renseigné',
              0: 'Non renseigné',
              1: 'Domicile - travail',
              2: 'Domicile - école',
              3: 'Courses - achats',
              4: 'Utilisation professionnelle',
              5: 'Promenade - loisirs',
              9: 'Autre'}

dic_actp = {-1: 'Non renseigné',
            0: 'Se déplaçant - Non renseigné ou sans objet',
            1: 'Se déplaçant - Sens véhicule ou heurtant',
            2: 'Se déplaçant - Sens inverse du véhicule',
            3: 'Traversant',
            4: 'Masqué',
            5: 'Jouant - courant',
            6: 'Avec animal',
            9: 'Autre',
            'A': 'Monte/descend du véhicule',
            'B': 'Inconnue'}

dic_etatp = {-1: 'Non renseigné',
             1: 'Seul',
             2: 'Accompagné',
             3: 'En groupe'}

dic_vosp = {-1 : "Non renseigné",
            0 : "Sans objet",
            1 : "Piste cyclable",
            2 : "Bande cyclable",
            3 : "Voie réservée"}

dic_prof = {-1 : "Non renseigné",
            1 : "Plat",
            2 : "Pente",
            3 : "Sommet de côte",
            4 : "Bas de côte"}

dic_plan = {-1 : "Non renseigné",
            1 : "Partie rectiligne",
            2 : "En courbe à gauche",
            3 : "En courbe à droite",
            4 : "En « S » "}

dic_surf = {-1 : "Non renseigné",
            1 : "Normale",
            2 : "Mouillée",
            3 : "Flaques",
            4 : "Inondée",
            5 : "Enneigée",
            6 : "Boue",
            7 : "Verglacée",
            8 : "Corps gras – huile",
            9 : "Autre"}

dic_infra = {-1 : "Non renseigné",
             0 : "Aucun",
             1 : "Souterrain - tunnel",
             2 : "Pont - autopont",
             3 : "Bretelle d’échangeur ou de raccordement",
             4 : "Voie ferrée",
             5 : "Carrefour aménagé",
             6 : "Zone piétonne",
             7 : "Zone de péage",
             8 : "Chantier",
             9 : "Autres"}

dic_age_cls = {0:'0-15',
               1:'16-25',
               2:'26-45',
               3:'46-65',
               4:'66-'}

dic_joursem = {0:'lundi',
               1:'mardi',
               2:'mercredi',
               3:'jeudi',
               4:'vendredi',
               5:'samedi',
               6:'dimanche'}

dic_secu1 = {'def': 'Equipement de sécurité 1',
             -1: 'Non renseigné',
             0: 'Aucun équipement',
             1: 'Ceinture',
             2: 'Casque',
             3: 'Dispositif enfants',
             4: 'Gilet réfléchissant',
             5: 'Airbag (2RM/3RM)',
             6: 'Gants (2RM/3RM)',
             7: 'Non déterminable',
             8: 'Autre'}

dic_secu2 = {'def': 'Equipement de sécurité 1',
             -1: 'Non renseigné',
             0: 'Aucun équipement',
             1: 'Ceinture',
             2: 'Casque',
             3: 'Dispositif enfants',
             4: 'Gilet réfléchissant',
             5: 'Airbag (2RM/3RM)',
             6: 'Gants (2RM/3RM)',
             7: 'Non déterminable',
             8: 'Autre'}

dic_secu3 = {'def': 'Equipement de sécurité 1',
             -1: 'Non renseigné',
             0: 'Aucun équipement',
             1: 'Ceinture',
             2: 'Casque',
             3: 'Dispositif enfants',
             4: 'Gilet réfléchissant',
             5: 'Airbag (2RM/3RM)',
             6: 'Gants (2RM/3RM)',
             7: 'Non déterminable',
             8: 'Autre'}

dic_locp = {'def': 'Localisation du piéton',
            -1: 'Non renseigné',
            0: 'Sans objet',
            1: 'Sur chaussée - A +50 du pass piéton',
            2: 'Sur chaussée - A -50 du pass piéton',
            3: 'Sur pass piéton - Sans signalisation lumineuse',
            4: 'Sur pass piéton - Avec signalisation lumineuse',
            5: 'Sur trottoir',
            6: 'Sur accotement',
            7: 'Sur refuge ou BAU',
            8: 'Sur contre allée',
            9: 'Inconnue'}

dic_mois = {1: 'Janvier',
            2: 'Février',
            3: 'Mars',
            4: 'Avril',
            5: 'Mai',
            6: 'Juin',
            7: 'Juillet',
            8: 'Août',
            9: 'Septembre',
            10: 'Octobre',
            11: 'Novembre',
            12: 'Décembre',
            }

dic_situ = {-1: 'Non renseigné',
            0: 'Aucun',
            1: 'Sur chaussée',
            2: "Sur bande d'arrêt d'urgence",
            3: "Sur accotement",
            4: "Sur trottoir",
            5: "Sur piste cyclable",
            6: "Sur autre voie spéciale",
            8: "Autres"
            }

dic_place = {-1: "Non renseigné",
             1: "Conducteur",
             2: "Passager avant droit (moto: passager)",
             3: "Passager arrière droit",
             4: "Passager arrière gauche",
             5: "Passager arrière central",
             6: "Passager avant central",
             7: "Passager latéral gauche",
             8: "Passager intermédiaire central",
             9: "Passager latéral droit",
             10: "Piéton (non applicable)"
             }

dic_dep = {1:"Ain",
           2:"Aisne",
           3:"Allier",
           4:"Alpes-de-Haute-Provence",
           5:"Hautes-Alpes",
           6:"Alpes-Maritimes",
           7:"Ardèche",
           8:"Ardennes",
           9:"Ariège",
           10:"Aube",
           11:"Aude",
           12:"Aveyron",
           13:"Bouches-du-Rhône",
           14:"Calvados",
           15:"Cantal",
           16:"Charente",
           17:"Charente-Maritime",
           18:"Cher",
           19:"Corrèze",
           20:"Corse",
           21:"Côte-d'Or",
           22:"Côtes-d'Armor",
           23:"Creuse",
           24:"Dordogne",
           25:"Doubs",
           26:"Drôme",
           27:"Eure",
           28:"Eure-et-Loir",
           29:"Finistère",
           30:"Gard",
           31:"Haute-Garonne",
           32:"Gers",
           33:"Gironde",
           34:"Hérault",
           35:"Ille-et-Vilaine",
           36:"Indre",
           37:"Indre-et-Loire",
           38:"Isère",
           39:"Jura",
           40:"Landes",
           41:"Loir-et-Cher",
           42:"Loire",
           43:"Haute-Loire",
           44:"Loire-Atlantique",
           45:"Loiret",
           46:"Lot",
           47:"Lot-et-Garonne",
           48:"Lozère",
           49:"Maine-et-Loire",
           50:"Manche",
           51:"Marne",
           52:"Haute-Marne",
           53:"Mayenne",
           54:"Meurthe-et-Moselle",
           55:"Meuse",
           56:"Morbihan",
           57:"Moselle",
           58:"Nièvre",
           59:"Nord",
           60:"Oise",
           61:"Orne",
           62:"Pas-de-Calais",
           63:"Puy-de-Dôme",
           64:"Pyrénées-Atlantiques",
           65:"Hautes-Pyrénées",
           66:"Pyrénées-Orientales",
           67:"Bas-Rhin",
           68:"Haut-Rhin",
           69:"Rhône",
           70:"Haute-Saône",
           71:"Saône-et-Loire",
           72:"Sarthe",
           73:"Savoie",
           74:"Haute-Savoie",
           75:"Paris",
           76:"Seine-Maritime",
           77:"Seine-et-Marne",
           78:"Yvelines",
           79:"Deux-Sèvres",
           80:"Somme",
           81:"Tarn",
           82:"Tarn-et-Garonne",
           83:"Var",
           84:"Vaucluse",
           85:"Vendée",
           86:"Vienne",
           87:"Haute-Vienne",
           88:"Vosges",
           89:"Yonne",
           90:"Territoire de Belfort",
           91:"Essonne",
           92:"Hauts-de-Seine",
           93:"Seine-Saint-Denis",
           94:"Val-de-Marne",
           95:"Val-d'Oise",
           971:"Guadeloupe",
           972:"Martinique",
           973:"Guyane",
           974:"La Réunion",
           975:"Saint-Pierre-et-Miquelon",
           976:"Mayotte",
           977:"Saint-Barthélemy",
           978:"Saint-Martin",
           986:"Wallis-et-Fotuna",
           987:"Polynésie Française",
           988:"Nouvelle-Calédonie"}

dic_feat_mods = {'dep':dic_dep,
                 'catv':dic_catv,
                 'catr':dic_catr,
                 'col':dic_col,
                 'agg':dic_agg,
                 'trajet':dic_trajet,
                 'mois':dic_mois,
                 'catu':dic_catu,
                 'situ':dic_situ,
                 'place':dic_place,
                 'sexe':dic_sexe,
                 'catr':dic_catr,
                 'locp':dic_locp,
                 'etatp':dic_etatp,
                 'lum':dic_lum,
                 'int':dic_int,
                 'atm':dic_atm,
                 'circ':dic_circ,
                 'nbv':dic_nbv,
                 'vosp':dic_vosp,
                 'prof':dic_prof,
                 'plan':dic_plan,
                 'surf':dic_surf,
                 'infra':dic_infra,
                 'situ':dic_situ,
                 'joursem':dic_joursem,
                 'age_cls':dic_age_cls}

def get_key_from_value(dict, val):
    keys = [k for k, v in dict.items() if v == val]
    if keys:
        return keys[0]
    return None
def get_labels(varname, value):
    if varname == 'lum': return dic_lum[value]
    if varname == 'grav': return dic_grav[value]
    if varname == 'catu': return dic_catu[value]
    if varname == 'sexe': return dic_sexe[value]
    if varname == 'agg': return dic_agg[value]
    if varname == 'int': return dic_int[value]
    if varname == 'atm': return dic_atm[value]
    if varname == 'col': return dic_col[value]
    if varname == 'trajet': return dic_trajet[value]
    if varname == 'actp': return dic_actp[value]
    if varname == 'etatp': return dic_etatp[value]
    if varname == 'secu1': return dic_secu1[value]
    if varname == 'secu2': return dic_secu2[value]
    if varname == 'secu3': return dic_secu3[value]
    if varname == 'locp': return dic_locp[value]