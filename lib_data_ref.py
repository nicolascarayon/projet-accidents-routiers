def get_labels(varname, value):
    if varname=='lum':
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
    
    if varname=='grav':
        if value==1:
            return 'Indemne'
        if value==2:
            return 'Tué'
        if value==3:
            return 'Blessé hospitalisé'
        if value==4:
            return 'Blessé léger'

    if varname == 'catu':
        if value==1:
            return 'Conducteur'
        if value==2:
            return 'Passager'
        if value==3:
            return 'Piéton'

    if varname == 'sexe':
        if value==1:
            return 'Masculin'
        if value==2:
            return 'Féminin'
    
    if varname == 'agg':
        if value==1:
            return 'hors agglomération'
        if value==2:
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
        if value == -1:
            return 'Non renseigné'
        if value == 1:
            return 'Normale'
        if value == 2:
            return 'Pluie légère'
        if value == 3:
            return 'Pluie forte'
        if value == 4:
            return 'Neige - grêle'
        if value == 5:
            return 'Brouillard - fumée'
        if value == 6:
            return 'Vent fort - tempête'
        if value == 7:
            return 'Temps éblouissant'
        if value == 8:
            return 'Temps couvert'
        if value == 9:
            return 'Autre'

    if varname == 'col':
        if value == -1:
            return 'Non renseigné'
        if value == 1:
            return 'Deux véhicules - frontale'
        if value == 2:
            return "Deux véhicules - par l'arrière"
        if value == 3:
            return 'Deux véhicules - par le côté'
        if value == 4:
            return 'Trois véhicules et plus - en chaîne'
        if value == 5:
            return 'Trois véhicules et plus - collisions multiples'
        if value == 6:
            return 'Autre collision'
        if value == 7:
            return 'Sans collision'

    if varname == 'trajet':
        if value == -1: 
            return 'Non renseigné'
        if value == 0:
            return 'Non renseigné'
        if value == 1:
            return 'Domicile - travail'
        if value == 2:
            return  'Domicile - école'
        if value == 3:
            return 'Courses - achats'
        if value == 4:
            return  'Utilisation professionnelle'
        if value == 5:
            return 'Promende - loisirs'
        if value == 9:
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
        if value == -1:
            return 'Non renseigné'
        if value == 0:
            return 'Sans objet'
        if value == 1:
            return 'Sur chaussée - A +50 du pass piéton'
        if value == 2:
            return 'Sur chaussée - A -50 du pass piéton'
        if value == 3:
            return 'Sur pass piéton - Sans signalisation lumineuse'
        if value == 4:
            return 'Sur pass piéton - Avec signalisation lumineuse'
        if value == 5:
            return 'Sur trottoir'
        if value == 6:
            return 'Sur accotement'
        if value == 7:
            return 'Sur refuge ou BAU'
        if value == 8:
            return 'Sur contre allée'
        if value == 9:
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
        if value == -1:
            return 'Non renseigné'
        if value == 1:
            return 'Seul'
        if value == 2:
            return 'Accompagné'
        if value == 3:
            return 'En groupe'
