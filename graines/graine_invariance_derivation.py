# -*- coding: utf-8 -*-
"""GRAINE 2 — Invariance de derivation.

1. LE DEFAUT, EN UNE PHRASE
   Un seuil calcule depuis une constante interne suit cette constante au lieu de suivre le
   monde : il mesure la memoire du systeme, pas l'ecoulement du milieu.

2. LE CHIFFRE, ET SA COMMANDE
   seuil par demi-vie  (decay 0,80 -> 0,99) : 10, 13, 20, 41, 207 cycles
   seuil par cadence   (cadence 1 -> 10)    :  3,  6, 15, 30 cycles
   ecart maximal entre les deux derives     : 20,7 x
   Reproduire : python graines/graine_invariance_derivation.py
   A la main  : ceil(3 x ln(0,5)/ln(decay)) contre 3 x cadence.

3. LE CODE — douze lignes utiles, aucune dependance, aucun etat
   (les deux versions sont ici, cote a cote : voir plus bas)

4. LE TEST QUI ECHOUE
   Quatre assertions, verifiees plus bas. Elles refusent de sortir en silence.

5. OU ELLE MORD
   TTL, timeouts, disjoncteurs, seuils d'alerte, fenetres glissantes : tout hyperparametre
   presente comme une mesure du monde alors qu'il est calcule depuis le modele.

CHAINE DE DETECTION : DEMI_VIES_TOLEREES
"""

import inspect
import math

DEMI_VIES_TOLEREES = 3
MANQUES_TOLEREES = 3
DECAYS = (0.80, 0.85, 0.90, 0.95, 0.99)
CADENCES = (1, 2, 5, 10)


def seuil_fautif(decay, demi_vies=DEMI_VIES_TOLEREES):
    """Version fautive : le seuil lit une constante interne, la demi-vie de la cicatrice."""
    return int(math.ceil(demi_vies * math.log(0.5) / math.log(decay)))


def seuil_corrige(cadence, manques=MANQUES_TOLEREES):
    """Version corrigee : le seuil ne lit que la cadence du monde.

    Sa signature EST l'invariant : ni `decay`, ni memoire, ni etat n'y entrent.
    """
    return manques * cadence


if __name__ == "__main__":
    fautifs = [seuil_fautif(d) for d in DECAYS]
    corriges = [seuil_corrige(c) for c in CADENCES]

    print("GRAINE 2 — invariance de derivation")
    print()
    print("  decay   :", "  ".join("%6.2f" % d for d in DECAYS))
    print("  fautif  :", "  ".join("%6d" % v for v in fautifs))
    print("  cadence :", "  ".join("%6d" % c for c in CADENCES))
    print("  corrige :", "  ".join("%6d" % v for v in corriges))
    print()

    ecart = max(fautifs) / float(min(fautifs))
    params = inspect.signature(seuil_corrige).parameters

    assert len(set(fautifs)) > 1, \
        "le defaut n'apparait pas : la version fautive est deja invariante"
    assert "decay" not in params, \
        "la version corrigee accepte encore la constante interne : la signature n'est pas l'invariant"
    assert len(set(corriges)) == len(CADENCES), \
        "la correction est devenue insensible au monde : un seuil constant n'est pas un seuil"
    assert ecart > 10, \
        "l'ecart entre les deux derivations est trop faible pour prouver quelque chose"

    print("  Les quatre conditions tiennent :")
    print("    1. le defaut se manifeste : %d a %d cycles selon la constante interne"
          % (min(fautifs), max(fautifs)))
    print("    2. la correction n'accepte pas la constante interne (signature verifiee)")
    print("    3. elle repond neanmoins au monde : %s cycles selon la cadence"
          % ", ".join(str(v) for v in corriges))
    print("    4. l'ecart atteint %.1f x : il n'est pas anecdotique" % ecart)
    print()
    print("  Le critere, transposable a tout reglage : change la constante interne du modele.")
    print("  Si le seuil bouge, il ne mesurait pas le monde. S'il ne bouge plus du tout quand")
    print("  la cadence change, il ne mesure plus rien.")
