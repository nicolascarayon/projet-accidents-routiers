import pandas as pd

# Labels for Shapash smart explainer

dic_target = {0: 'Indemne - Blessé léger',
              1: 'Tué - Blessé hospitalisé'}

dic_features = {'grav': 'Gravité',
                'place ': "Place de l'usager",
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
                'prof': 'profil de la route',
                'plan': 'tracé en plan',
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

dic_lum = {'def': 'Condition de luminosité',
           1: 'Plein jour',
           2: 'Crépuscule ou aube',
           3: 'Nuit sans éclairage public',
           4: 'Nuit avec éclairage public non allumé',
           5: 'Nuit avec éclairage public allumé'}

dic_grav = {'def': 'Gravité',
            0: 'Indemne - Blessé léger',
            1: 'Tué - Blessé hospitalisé'}

dic_catu = {'def': "Catégorie d'usager",
            1: 'Conducteur',
            2: 'passager',
            3: 'Piéton'}

dic_sexe = {'def': 'Sexe',
            1: 'Masculin',
            2: 'Féminin'}

dic_agg = {'def': 'Localisation',
           1: 'Hors agglomération',
           2: 'En agglomération'}

dic_int = {'def': 'Intersection',
           1: 'Hors intersection',
           2: 'Intersection en X',
           3: 'Intersection en T',
           4: 'Intersection en Y',
           5: 'Intersection à plus de 4 branches',
           6: 'Giratoire',
           7: 'Place',
           8: 'Passage à niveau',
           9: 'Autre intersection'}

dic_atm = {'def': 'Conditions atmosphériques',
           -1: 'Non renseigné',
           1: 'Normale',
           2: 'Pluie légère',
           3: 'Pluie forte',
           4: 'Neige - grêle',
           5: 'Brouillard - fumée',
           6: 'Vent fort - tempête',
           7: 'Temps éblouissant',
           8: 'Temps couvert',
           9: 'Autre'}

dic_col = {'def': 'Type de collision',
           -1: 'Non renseigné',
           1: 'Deux véhicules - frontale',
           2: "Deux véhicules - par l'arrière",
           3: 'Deux véhicules - par le côté',
           4: 'Trois véhicules et plus - en chaîne',
           5: 'Trois véhicules et plus - collisions multiples',
           6: 'Autre collision',
           7: 'Sans collision'}

dic_trajet = {'def': 'Motif du déplacement',
              -1: 'Non renseigné',
              0: 'Non renseigné',
              1: 'Domicile - travail',
              2: 'Domicile - école',
              3: 'Courses - achats',
              4: 'Utilisation professionnelle',
              5: 'Promende - loisirs',
              9: 'Autre'}

dic_actp = {'def': 'Action du piéton',
            -1: 'Non renseigné',
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

dic_etatp = {'def': 'Piéton seul on non',
             -1: 'Non renseigné',
             1: 'Seul',
             2: 'Accompagné',
             3: 'En groupe'}

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
