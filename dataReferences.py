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