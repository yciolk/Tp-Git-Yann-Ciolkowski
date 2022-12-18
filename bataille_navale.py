# Contributeur : Rémi Synave, Yann Ciolkowski
# Bonjour Monsieur Synave,
# Je suis désolé mais n'ai pas eu le temps de finir ce tp avant la fin de l'échéance. Mon programme ne fonctionne pas et je n'ai su le faire marcher à temps,
# aussi je vous rends un tp incomplet et veux m'excuser pour la gêne occasionée.
#      Bonne soirée, 
#                 CIOLKOWSKI Yann


"""
Jeu de la bataille navale à un joueur.

Le plateau par défaut est de taille 10 et sont placés aléatoirement :
- un porte-avion de 5 cases.
- un croiseur de 4 cases.
- deux destroyers de 3 cases.
- un torpilleur de 2 cases.

Attention ! Chaque bateau porte un numéro pour qu'on ne confonde pas les deux destroyers !

Le joueur tir en donnant, dans un premier temps, le numéro de la ligne, puis, le numéro de la colonne.

Les numéros de ligne et de colonne doivent être compris entre 1 et la taille du plateau inclus.

Si le numéro de ligne vaut 0 alors la partie s'arrête.
"""


import sys
import random
partie_sauvegardee=[]


def placement_possible(plateau, origine_bateau, nombre_cases, orientation):
    """
    Vérifie si le placement du bateau passé en paramètre est possible sur le plateau donc s'il n'y a pas un autre bateau qui entre en collision.
    """
    assert (orientation == 'H') or (orientation == 'V')

    ligne, colonne = origine_bateau[0], origine_bateau[1]
    if orientation == 'H':
        for j in range(nombre_cases):
            if(plateau[ligne][colonne+j]['contenu'] != 'Eau'):
                return False
    else:
        for i in range(nombre_cases):
            if(plateau[ligne+i][colonne]['contenu'] != 'Eau'):
                return False

    return True


def genere_position_aleatoire(taille_plateau, nb_cases):
    """
    Génère une position aléatoire sur un plateau dont la taille est passée en paramètre et pour un bateau du nombre de cases passé en paramètre.
    """
    if(random.randint(0,1) == 0):
        orientation = 'H'
    else:
        orientation = 'V'
    
    if(orientation == 'H'):
        irand = random.randint(0,len(plateau)-1)
        jrand = random.randint(0,len(plateau)-nb_cases)
    else:
        irand = random.randint(0,len(plateau)-nb_cases)
        jrand = random.randint(0,len(plateau)-1)

    return orientation, (irand, jrand)


def genere_bateau(plateau, type_bateau, numero_bateau):
    """
    Place un bateau sur le plateau. L'algo vérifie si le bateau n'entre pas en collision avec un autre bateau précédemment généré.
    """
    assert (type_bateau == 'Porte-avions') or (type_bateau == 'Croiseur') or (type_bateau == 'Destroyer') or (type_bateau == 'Torpilleur')

    nb_cases = 5
    if(type_bateau == 'Porte-avions'):
        nb_cases = 5
    if(type_bateau == 'Croiseur'):
        nb_cases = 4
    if(type_bateau == 'Destroyer'):
        nb_cases = 3
    if(type_bateau == 'Torpilleur'):
        nb_cases = 2

    orientation, position = genere_position_aleatoire(len(plateau), nb_cases)
    
    while(placement_possible(plateau, position, nb_cases, orientation) == False):
        orientation, position = genere_position_aleatoire(len(plateau), nb_cases)

    if(orientation == 'H'):
        for j in range(nb_cases):
            plateau[position[0]][position[1]+j] = {'contenu':type_bateau, 'numero':numero_bateau, 'etat':'Neuf'}
    else:
        for i in range(nb_cases):
            plateau[position[0]+i][position[1]] = {'contenu':type_bateau, 'numero':numero_bateau, 'etat':'Neuf'}


def creer_plateau_vide(taille_grille):
    """
    Crée un plateau vide.
    """
    plateau = []
    for i in range(taille_grille):
        ligne = []
        for j in range(taille_grille):
            ligne.append({'contenu':'Eau', 'numero':0, 'etat':'Neuf'})
        plateau.append(ligne)

    return plateau


def remplir_plateau(plateau):
    """
    Place tous les bateaux sur le plateau.
    """
    genere_bateau(plateau, 'Porte-avions', 0)
    genere_bateau(plateau, 'Croiseur', 0)
    genere_bateau(plateau, 'Destroyer', 0)
    genere_bateau(plateau, 'Destroyer', 1)
    genere_bateau(plateau, 'Torpilleur', 0)


def afficher_plateau_triche(plateau):
    """
    Affiche le plateau en mode console. Le plateau est affiché en totalité avec l'ensemble des bateaux visibles.
    """
    print('MODE TRICHE :')
    print('-'*(len(plateau) + 2))
    for ligne in plateau:
        a_afficher = '|'
        for colonne in ligne:
            if(colonne['contenu'] == 'Eau'):
                a_afficher = a_afficher+' '
            else:
                a_afficher = a_afficher + '{}'.format(colonne['contenu'][0])
        a_afficher = a_afficher + '|'
        print(a_afficher)
    print('-'*(len(plateau) + 2))


def afficher_plateau_jeu(plateau):
    """
    Affiche le plateau de jeu tel que le joueur doit le voir. On y voit donc les différents tirs déjà opérés et les bateaux déjà touchés.
    """
    print('-'*(len(plateau) + 2))
    for ligne in plateau:
        a_afficher = '|'
        for colonne in ligne:
            if(colonne['etat'] == 'Neuf'):
                a_afficher=a_afficher + ' '
            else:
                if(colonne['contenu'] == 'Eau'):
                    a_afficher = a_afficher + 'X'
                else:
                    a_afficher = a_afficher + '{}'.format(colonne['contenu'][0].lower())
        a_afficher = a_afficher + '|'
        print(a_afficher)
    print('-'*(len(plateau) + 2))


def verif_coule(plateau, type_bateau, numero_bateau):
    """
    Vérifie si un bateau passé en paramètes est déjà coulé.
    """
    for ligne in plateau:
        for colonne in ligne:
            if colonne['contenu'] == type_bateau and colonne['numero'] == numero_bateau and colonne['etat'] == 'Neuf':
                return False
    return True


def tir(plateau, position):
    """
    Fais les modifications sur le plateau pour un tir donné.
    """
    if(plateau[position[0]][position[1]]['etat'] == 'Touche'):
        print('Position déjà touchée')
    else:
        plateau[position[0]][position[1]]['etat'] = 'Touche'
        if(plateau[position[0]][position[1]]['contenu'] == 'Eau'):
            print('A l\'eau')
        else:
            if(verif_coule(plateau,plateau[position[0]][position[1]]['contenu'],plateau[position[0]][position[1]]['numero'])):
                print(plateau[position[0]][position[1]]['contenu'], plateau[position[0]][position[1]]['numero'], 'coulé')
            else:
                print(plateau[position[0]][position[1]]['contenu'], plateau[position[0]][position[1]]['numero'], 'touché')


def fin_partie(plateau):
    """
    Vérifie si tous les bateaux ont été coulés.
    """
    for ligne in plateau:
        for colonne in ligne:
            if((colonne['contenu'] != 'Eau') and (colonne['etat'] == 'Neuf')):
               return False

    return True


def sauvegarde_partie(plateau,taille_grille):
    partie_sauvegardee=[]
    coups_joues=0
    partie_sauvegardee.append(taille_grille)
    for ligne in plateau :
        for colonne in ligne :
            if colonne['etat'] == 'Touche':
                coups_joues=coups_joues+1
    partie_sauvegardee.append(coups_joues)
    print(partie_sauvegardee)
    for ligne in plateau :
        for colonne in ligne :
            partie_sauvegardee.append(colonne['contenu']['numero']['etat'])
    print(partie_sauvegardee)
    return(partie_sauvegardee)
    
    
def charge_partie(partie_sauvegardee) :
    taille_grille=partie_sauvegardee[0]
    nombre_tir=partie_sauvegardee[1]
    i=2
    for ligne in plateau :
        for colonne in ligne :
            colonne['contenu']=partie_sauvegardee[i]['contenu']
            colonne['numero']=partie_sauvegardee[i]['numero']
            colonne['etat']=partie_sauvegardee[i]['etat']
            i=i+1
    return(plateau, nombre_tir, taille_grille)
            
    



if __name__ == "__main__":
    # Initialisations
    taille_grille=10
    plateau = creer_plateau_vide(taille_grille)

    nombre_tir = 0

    # Remplissage du plateau avec les bateaux par défaut.
    remplir_plateau(plateau)
    # Premier affichage du plateau.
    afficher_plateau_jeu(plateau)

    # Boucle principale de jeu
    while(not fin_partie(plateau)):
        # On demande le numéro de ligne.
        print('où voulez vous tirer ? - 0 pour quitter')
        i = (int)(input('Numéro de ligne entre 1 et {} : '.format(len(plateau))))
        # Si le numéro de ligne entré vaut 0 alors, on arrête le jeu.
        if(i == 0):
            print('Tu ne vas même pas jusqu\'au bout du jeu ? Tant pis. Bye !')
            sys.exit(0)

        # On demande le numéro de colonne
        j = (int)(input('Numéro de colonne entre 1 et {} : '.format(len(plateau))))

        # On vérifie les coordonnées.
        if(i > len(plateau)) or (j > len(plateau)):
            if input("Voulez-vous charger la dernière partie enregistrée ? (Y/N)")=="Y" or "y" :
                charge_partie(partie_sauvegardee)
        elif (i < 0) or (j < 0) :
            if input("Voulez-vous sauvegarder la partie en cours ? (Y/N)")=="Y" or "y" :
                sauvegarde_partie(plateau,taille_grille)
                print("Partie enregistrée.")
        else:
            # Si tout est OK, on tire ! BOUM ! ou pas...
            tir(plateau, (i-1, j-1))
            nombre_tir = nombre_tir + 1
            afficher_plateau_jeu(plateau)
    
    # Si on arrive ici, c'est qu'on a coulé tous les bateaux.
    print('Tu as coulé tous les bateaux en', nombre_tir, 'tirs.')
    print('GG')
