#! /usr/bin/env python3
"""
Module permettant une simulation d'approximation de pi par la méthode de Monte-Carlo.
Prend un argument dans la commande : un nombre entier.
Ce nombre entier doit être suffisamment grand pour que la méthode soit effective.
notée à 10/10 sur pylint
"""
import sys
import random as r
import numpy as np

def in_circle(abscisse, ordonnee):
    """Dit si le point (x,y) est dans le cercle de centre (0,0) et de rayon 1.

    Cette fonction prend 3 arguments:
    -> abscisse : pixel d'abscisse (entier naturel)
    -> ordonnee : pixel d'ordonnée (entier naturel)
    Retourne True si le point est dans le cercle; False sinon.
    """
    return abscisse**2 + ordonnee**2 <= 1

def approximation_pi(ntpat, img_sze):
    """Génère une approximation de PI.

    Prend 2 arguments:
    -> ntpat : nombre total de points à tirer (entier naturel)
    -> img_sze : taille de l'image voulue
    Retourne:
    -> une liste d'approximation de pi de longueur 10. Elle montre une évolution de la simulation
    de PI dès qu'un dixième de points est tiré
    -> Une liste de tableau/matrice. Chaque matrice est de taille img_sze. La matrice i représente
    tous les points tirés alétoirement tous les dixièmes de points.
    """
    # --- EXCEPTIONS --
    img_sze = int(img_sze)
    ntpat = int(ntpat)
    if ntpat <= 0 or img_sze <= 0:
        raise ValueError("ntpat ou img_sze n'est pas un entier strictement positif")
    # -----------------
    lapprox = []
    cptr = 0 #On initialise le compteur à 0
    liste_tab = []
    for i in range(1, 11):
        tableau = np.zeros((img_sze, img_sze), dtype = int)
        for _ in range(ntpat // 10):
            abscisse = r.uniform(- 1, 1)
            ordonnee = r.uniform(- 1, 1)
            abs_new = int((abscisse + 1)*(img_sze // 2))
            ord_new = int((ordonnee + 1)*(img_sze // 2))
            if len(liste_tab) == 0:
                if np.equal(in_circle(abscisse, ordonnee), True):
                    tableau[abs_new][ord_new] = 2
                    cptr += 1
                else:
                    tableau[abs_new][ord_new] = 1
            else:
                if np.equal(liste_tab[- 1][abs_new][ord_new], 0):
                    if np.equal(in_circle(abscisse, ordonnee), True):
                        tableau[abs_new][ord_new] = 2
                        cptr += 1
                    else:
                        tableau[abs_new][ord_new] = 1
                else:
                    if np.equal(in_circle(abscisse, ordonnee), True):
                        cptr += 1
        lapprox.append(4 * cptr / (i * (ntpat // 10)))
        if i == 1:
            liste_tab.append(tableau)
        else:
            liste_tab.append(liste_tab[- 1]+ tableau)
    return lapprox, liste_tab

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "Pas le bon nombre d'arguments"
    liste_approx, liste_tableaux = approximation_pi(int(sys.argv[1]), 800)
    print('approximation =', liste_approx[-1])
