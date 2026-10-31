# -*- coding: utf-8 -*-
"""GRAINE — un seuil ne doit pas deriver de sa propre constante.

1. LE DEFAUT, EN UNE PHRASE
   Un seuil calcule a partir d'une constante interne suit cette constante : il finit par
   mesurer la memoire du systeme au lieu de mesurer le monde.

2. LE CHIFFRE
   Un seuil de peremption derive de la demi-vie de la cicatrice, tau = ln(0,5)/ln(decay) :

     decay        0,80   0,85   0,90   0,95   0,99
     seuil         10     13     20     41    207   cycles

   Le meme seuil derive de la cadence des lectures, pour trois lectures manquees tolerees :
     decay        0,80   0,85   0,90   0,95   0,99
     seuil          3      3      3      3      3    cycles

   Reproduire :  python graines/graine_invariance_derivation.py
   Re-derivable a la main : tau = ln(0,5)/ln(decay), puis ceil(3 x tau).

3. LE CODE MINIMAL  (quinze lignes utiles, aucune dependance, aucun etat)
   ------------------------------------------------------------------
   import math

   def seuil_par_demi_vie(decay, demi_vies=3):
       return int(math.ceil(demi_vies * math.log(0.5) / math.log(decay)))

   def seuil_par_cadence(cadence, manques=3):
       return manques * cadence
   ------------------------------------------------------------------
   La seconde fonction n'accepte pas `decay` : sa **signature** est l'invariant.

4. LE TEST QUI ECHOUE
   Trois conditions, verifiees plus bas :
     - la version fautive DOIT bouger quand la decroissance bouge (sinon le defaut
       n'apparait pas et la graine ne prouve rien) ;
     - la version correcte NE DOIT PAS bouger ;
     - le rapport entre les deux doit croitre de plus d'un ordre de grandeur, faute de
       quoi la difference serait anecdotique.

5. OU ELLE MORD
   - tout hyperparametre presente comme une mesure du monde (timeout, TTL, seuil d'alerte) ;
   - les temporisations calibrees « en nombre de cycles » d'un modele dont on change la
     constante de decroissance ;
   - les fenetres glissantes dimensionnees par une constante du modele plutot que par la
     cadence reelle des donnees.
   Chaine de detection : DEMI_VIES_TOLEREES
"""

import math

DECAYS = (0.80, 0.85, 0.90, 0.95, 0.99)
CADENCE = 1                 # une lecture attendue par cycle
DEMI_VIES_TOLEREES = 3
MANQUES_TOLEREES = 3


def seuil_par_demi_vie(decay, demi_vies=DEMI_VIES_TOLEREES):
    """Version fautive : le seuil depend d'une constante interne au systeme."""
    return int(math.ceil(demi_vies * math.log(0.5) / math.log(decay)))


def seuil_par_cadence(cadence=CADENCE, manques=MANQUES_TOLEREES):
    """Version corrigee : le seuil ne depend que de la cadence du monde.

    La signature est l'invariant : ni `decay`, ni une memoire, ni un etat n'y entrent.
    """
    return manques * cadence


if __name__ == "__main__":
    print("GRAINE invariance de derivation")
    print()
    print("  %-8s %-24s %-24s" % ("decay", "seuil par demi-vie", "seuil par cadence"))
    fautifs, corrects = [], []
    for d in DECAYS:
        a, b = seuil_par_demi_vie(d), seuil_par_cadence()
        fautifs.append(a)
        corrects.append(b)
        print("  %-8.2f %-24d %-24d" % (d, a, b))
    print()

    ecart = max(fautifs) / float(min(fautifs))
    print("  Rapport entre la plus grande et la plus petite valeur fautive : %.1f x" % ecart)
    print()

    # 4. LE TEST QUI ECHOUE
    assert len(set(fautifs)) > 1, \
        "le defaut n'apparait pas : la version fautive est deja invariante"
    assert len(set(corrects)) == 1, \
        "la version corrigee derive : elle lit encore une constante interne"
    assert ecart > 10, \
        "l'ecart entre les deux derives est trop faible pour prouver quelque chose"

    print("  Les trois conditions tiennent :")
    print("    - la version fautive varie de %d a %d cycles ;" % (min(fautifs), max(fautifs)))
    print("    - la version corrigee reste a %d cycle(s) ;" % corrects[0])
    print("    - l'ecart atteint %.0f x, il n'est pas anecdotique." % ecart)
    print()
    print("  Le critere, transposable a tout reglage : change la constante interne du")
    print("  modele. Si le seuil bouge, il ne mesurait pas le monde.")
