# -*- coding: utf-8 -*-
"""GRAINE — absence n'est pas zéro.

1. LE DEFAUT, EN UNE PHRASE
   Un nombre qui vaut « rien recu » et un nombre qui vaut « mesure a zero » sont le meme
   nombre. Tout ce qui decroit sur ce nombre prend le silence pour du calme.

2. LE CHIFFRE
   A entree nulle apres un choc (protocole publie) :
     sans le bit -> la memoire se vidange jusqu'a 0,0087 et la porte ROUVRE au pas 22 ;
     avec le bit -> la memoire reste gelee a 0,5877 et la porte ne rouvre JAMAIS.
   Reproduire :  python graines/graine_absence_zero.py
   Re-derivable a la main : m_n = 0,5877 x 0,9^n ; h = 1 - (0,85 m + 0,0075) ;
   reouverture quand h > 0,85, soit m < 0,1677. A n = 12, m = 0,1660, h = 0,8514.

3. LE CODE MINIMAL  (douze lignes, aucune dependance, aucun etat cache)
   ------------------------------------------------------------------
   DECAY, W = 0.90, 0.85
   FERME, ROUVRE = 0.55, 0.85

   def pas(m, p, presente, ferme, penalite=0.0075):
       if presente:                       # <- le seul ajout
           m = m * DECAY + p * (1.0 - DECAY)
       h = 1.0 - (W * m + penalite)
       if ferme and h > ROUVRE:    ferme = False
       elif not ferme and h < FERME: ferme = True
       return m, h, ferme
   ------------------------------------------------------------------

4. LE TEST QUI ECHOUE
   Ce fichier contient les deux versions et refuse de sortir en silence si le defaut
   n'apparait pas, ou si la correction sur-corrige. Trois `assert`, executes plus bas.

5. OU ELLE MORD
   - toute moyenne ou moyenne mobile sur un flux de mesures troue (telemetrie, capteurs) ;
   - les agregateurs qui remplacent une mesure manquante par zero plutot que par « absent » ;
   - les filtres a etat qui decroissent « par cycle » sans savoir si le cycle a eu lieu.
   Chaine de detection : PENALITE_CALME (identifiant rare, cherchable).
"""

DECAY, W = 0.90, 0.85
FERME, ROUVRE = 0.55, 0.85
PENALITE_CALME = 0.0075     # 0,10 x 0,05 + 0,05 x 0,05
PENALITE_CHOC = 0.0475      # 0,10 x 0,35 + 0,05 x 0,25
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7


def pas_sans_bit(m, p, ferme, penalite):
    """Version fautive : l'absence arrive comme un zero, la memoire se vidange."""
    m = m * DECAY + p * (1.0 - DECAY)
    return _etat(m, ferme, penalite)


def pas_avec_bit(m, p, presente, ferme, penalite):
    """Version corrigee : sans lecture, la memoire est gelee."""
    if presente:
        m = m * DECAY + p * (1.0 - DECAY)
    return _etat(m, ferme, penalite)


def _etat(m, ferme, penalite):
    h = 1.0 - (W * m + penalite)
    if ferme and h > ROUVRE:
        ferme = False
    elif not ferme and h < FERME:
        ferme = True
    return m, h, ferme


def scenario(avec_bit, presente):
    m, ferme, fermeture, reouverture, h_f = 0.0, False, None, None, None
    for i, p in enumerate(PRESSION, 1):
        m, h, ferme = pas_avec_bit(m, p, True, ferme, PENALITE_CHOC)
        if ferme and fermeture is None:
            fermeture, h_f = i, h
    for k in range(1, 41):
        if avec_bit:
            m, h, ferme = pas_avec_bit(m, 0.0, presente, ferme, PENALITE_CALME)
        else:
            m, h, ferme = pas_sans_bit(m, 0.0, ferme, PENALITE_CALME)
        if not ferme and reouverture is None:
            reouverture = 10 + k
    return fermeture, reouverture, m, h_f


if __name__ == "__main__":
    print("GRAINE absence != zero — protocole publie, a entree nulle apres un choc")
    print()
    print("  %-34s %-12s %-14s %s" % ("situation", "fermeture", "reouverture", "m final"))
    f0, r0, _, h0 = scenario(False, False)
    print("  %-34s %-12s %-14s" % ("sans le bit (defaut present)", f0, r0))
    f1, r1, m1, _ = scenario(True, False)
    print("  %-34s %-12s %-14s %.4f" % ("avec le bit, aucune lecture", f1,
                                        r1 if r1 else "AUCUNE", m1))
    f2, r2, _, _ = scenario(True, True)
    print("  %-34s %-12s %-14s" % ("avec le bit, calme MESURE (p=0)", f2, r2))
    print()

    # 4. LE TEST QUI ECHOUE — trois conditions, verifiees
    assert f0 == 8 and r0 == 22, "le defaut n'apparait pas : la graine ne prouve rien"
    assert abs(h0 - 0.5252) < 0.0001, "h a la fermeture ne vaut pas 0,5252"
    assert r1 is None and abs(m1 - 0.5877) < 0.0001, \
        "l'absence devrait geler la memoire a 0,5877 sans reouverture"
    assert r2 == 22, "la correction sur-corrige : le calme mesure ne rouvre plus"

    print("  Les trois conditions tiennent :")
    print("    - le defaut est present sans le bit (reouverture au pas 22) ;")
    print("    - le bit le supprime (memoire gelee, aucune reouverture) ;")
    print("    - le bit ne sur-corrige pas (calme mesure : reouverture au pas 22).")
