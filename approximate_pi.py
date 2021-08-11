#! /usr/bin/env python3
"""
Génération d'une image animée GIF à partir de 10 images PPM.

->3 arguments depuis la ligne de commande :
 -taille de l'image (carrée)
 -nombre de points n à utliser dans la simulatin
 -nombre de chiffres après la virgule à utiliser dans l'affichage de la valeur approximative de pi
->fonction : generate_ppm_file()
"""
import sys
import subprocess
import simulator


def genere_nom_approx(approx_pi, cav, num_img):
    """Génère le nom du fichier et la string de l'approx de pi.

    Ces 2 éléments dépendent du nombre de chiffre après la virgul voulu.
    Prend 3 arguments:
    -> approx_pi : flottant étant l'approximation de pi sur laquelle l'image se base
    -> cav : le nombre de Chiffres Après la Virgule (d'où cav). Entier naturel
    -> num_img : le numéro de l'image que l'on veut générer (de 0 à 9)
    Renvoie le nom de l'image et le string de l'approx de pi.
    """
    nom_image = 'img{num_img}_'.format(num_img = num_img)
    liste = str(approx_pi).split('.')
    resultat = liste[0]+'.'
    nom_image += liste[0]
    nom_image += '-'
    if len(liste[1]) < cav:
        nom_image += liste[1]
        resultat += liste[1]
    else:
        nom_image += liste[1][:cav]
        resultat += liste[1][:cav]
    nom_image += '.ppm'
    return nom_image, resultat

def generate_ppm_file(img_sze, approx_pi, tab, cav, num_img):
    """Génère une image PPM avec la simulation de PI au centre.

    Prend 5 arguments:
    -> img_sze : la taille de l'image (entier naturel strictement positif)
    -> approx_pi : le flottant qui l'approximation de ppi dont
    l'image est la représentation.
    -> tab : matrice carrée (un array numpy) de taille img_sze contenant des 0, des 1 et des 2.
    Si tab[i][j] = 0 : pixel non tiré, si =1 : pixel tiré mais hors cercle,
    si =2 : pixel tiré et dans le cercle
    -> cav : nombre de chiffre après la virgule voulu dans l'affichage de
    l'approximation de pi (entier naturel)
    -> num_img : numéro de l'image dont il est question
    Retourne le nom de l'image donné
    """
    nom_image, simu_pi_cav = genere_nom_approx(approx_pi, cav, num_img)
    image = open("{}".format(nom_image), 'w')
    chaine = "P3 \n"+ f"{img_sze} {img_sze} \n" + "255 \n"
    for i in range(0, img_sze ):
        for j in range(0, img_sze ):
            if tab[i][j] == 2:
                chaine += "255 0 0 \n"
            elif tab[i][j] == 1:
                chaine += "0 0 255 \n"
            else:
                chaine += "255 255 255 \n"
    image.write(chaine)
    image.close()
    subprocess.call(f"convert {nom_image} -pointsize {img_sze // 10} \
        -annotate +{img_sze // 2 - ((cav + 2)*(img_sze // 20)) // 2}+{img_sze // 2 + (img_sze // 100)} \
             '{simu_pi_cav}' {nom_image}", shell = True)
    return nom_image

def generate_gif_file(ntpat, img_sze, cav):
    """Génère le GIF contenant 10 images PPM avec chacune son approximation de PI.

    Prend 3 arguments:
    -> ntpat : nombre total de points à tirer  lors de l'application de la méthode de Monte-Carlo
    (effectuée dans simulator)(entier naturel)
    -> img_sze : taille de l'image (entier naturel strictement positif)
    -> cav : nombre de chiffre après la virgule voulu dans l'affichage de la simulation de PI
    Ne retourne rien.
    """
    #--- EXCEPTIONS ---
    ntpat = int(ntpat)
    img_sze = int(img_sze)
    cav = int(cav)
    if ntpat <= 0:
        raise ValueError("ntpat n'est pas un entier strictement positif")
    if img_sze <= 0:
        raise ValueError("img_sze n'est pas un entier strictement positif")
    if cav <= 0:
        raise ValueError("cav n'est pas un entier strictement positif")
    #------------------
    lapprox, liste_tab = simulator.approximation_pi(ntpat, img_sze)
    lst_noms = []
    for i in range(len(lapprox)):
        #debut = time.time()
        lst_noms.append(generate_ppm_file(img_sze, lapprox[i], liste_tab[i], cav, i))
        #fin = time.time()
        #print(fin - debut)
    subprocess.call(f"convert -delay 150 -loop 5 {' '.join(lst_noms)} approx_pi.gif", shell = True)

if __name__ == "__main__":
    assert (len(sys.argv) == 4), "Pas le bon nombre d'arguments"
    #start = time.time()
    generate_gif_file(int(sys.argv[2]), int(sys.argv[1]), int(sys.argv[3]))
    #stop = time.time()
    #print(stop - start)
