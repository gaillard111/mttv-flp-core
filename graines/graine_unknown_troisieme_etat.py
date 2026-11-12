# -*- coding: utf-8 -*-
"""GRAINE — l'inconnu n'est ni une lecture ni une absence.

1. LE DEFAUT, EN UNE PHRASE
   Une porte qui decide sur la VALEUR d'une reponse et non sur sa CLASSE DE DECODAGE confond
   trois cas en deux : la lecture, l'absence, et la reponse qui ne porte rien. Cette troisieme
   se pose alors exactement sur l'une des deux autres, et la trace ne dit plus laquelle.

2. LE CHIFFRE
   Meme protocole publie que la graine « absence n'est pas zero » (fermeture pas 8, reouverture
   pas 22 sous accord), puis quarante pas ou le second canal repond INCONNU a chaque tour :
     defaut A, « toute reponse non nulle est une lecture » -> reouverture au pas 22 ;
     defaut B, « l'inconnu est range avec l'absence »     -> AUCUNE reouverture ;
     correction C, trois classes decodees et journalisees -> AUCUNE reouverture, compteur
                                                             d'inconnues, escalade au pas 40.
   L'identite qui fait la graine, et qui se lit dans le tableau : A rouvre au pas 22, soit
   EXACTEMENT le pas du calme mesure ; B ne rouvre jamais, soit EXACTEMENT l'absence vraie.
   Le troisieme etat est indiscernable des deux autres tant qu'on ne journalise pas sa classe.
   Reproduire :  python graines/graine_unknown_troisieme_etat.py
   Re-derivable a la main : m_n = 0,5877 x 0,9^n ; h = 1 - (0,85 m + 0,0075) ; reouverture
   quand h > 0,85, soit m < 0,1677, donc n = 12 et pas 10 + 12 = 22.

3. LE CODE MINIMAL  (aucune dependance, aucun etat cache)
   ------------------------------------------------------------------
   def decode(reponse, variante):
       if reponse is None:            return False, 0.0, "ABSENCE"
       if reponse == "INCONNU":
           if variante == "A":        return True,  0.0, "LECTURE"
           if variante == "B":        return False, 0.0, "ABSENCE"
           return False, 0.0, "INCONNU"
       return True, float(reponse), "LECTURE"
   ------------------------------------------------------------------
   Toute la graine tient dans ces sept lignes : le reste de la porte est inchange.

4. LE TEST QUI ECHOUE
   Le fichier refuse de sortir en silence si le defaut n'apparait pas, s'il apparait des deux
   cotes, ou si la correction sur-corrige. Six `assert`, executes plus bas. Le test ne porte pas
   sur un comportement mais sur une SEPARATION : deux situations differentes doivent laisser
   deux traces differentes.

5. OU ELLE MORD
   - un registre de tache qui dit `enabled, scheduled, last result ok` sans artefact produit ;
   - NULL contre 0 en SQL, 204 contre 200 {} en HTTP, `absent()` contre 0 en observabilite ;
   - un collecteur qui lit `has_more` / `next_cursor` et compte un element supprime comme un
     element rendu.
   Chaine de detection : CLASSE_INCONNUE_DECODEE (identifiant rare, cherchable).
"""

DECAY, W = 0.90, 0.85
FERME, ROUVRE = 0.55, 0.85
PENALITE_CALME = 0.0075
PENALITE_CHOC = 0.0475
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
PAS_MAX = 40
ESCALADE = 30
SOURCES = {"inconnu": "INCONNU", "rien": None, "calme": 0.0}
VARIANTES = {"A": "toute reponse non nulle est une lecture",
             "B": "l'inconnu est range avec l'absence",
             "C": "trois classes decodees et journalisees"}


def etat(m, ferme, penalite):
    h = 1.0 - (W * m + penalite)
    if ferme and h > ROUVRE:
        ferme = False
    elif not ferme and h < FERME:
        ferme = True
    return m, h, ferme


def decode(reponse, variante):
    """Rend (presente, p, etiquette). C'est ici, et nulle part ailleurs, que se joue la graine."""
    if reponse is None:
        return False, 0.0, "ABSENCE"
    if reponse == "INCONNU":
        if variante == "A":
            return True, 0.0, "LECTURE"
        if variante == "B":
            return False, 0.0, "ABSENCE"
        return False, 0.0, "INCONNU"
    return True, float(reponse), "LECTURE"


def scenario(variante, source):
    m, ferme, fermeture, reouverture, escalade, inconnues = 0.0, False, None, None, None, 0
    for i, p in enumerate(PRESSION, 1):
        m, h, ferme = etat(m * DECAY + p * (1.0 - DECAY), ferme, PENALITE_CHOC)
        if ferme and fermeture is None:
            fermeture = i
    etiquette = "-"
    for k in range(1, PAS_MAX + 1):
        presente, p, etiquette = decode(SOURCES[source], variante)
        if etiquette == "INCONNU":
            inconnues += 1
            if inconnues == ESCALADE and escalade is None:
                escalade = 10 + k
        if presente:
            m = m * DECAY + p * (1.0 - DECAY)
        m, h, ferme = etat(m, ferme, PENALITE_CALME)
        if not ferme and reouverture is None:
            reouverture = 10 + k
    return {"fermeture": fermeture, "reouverture": reouverture, "m": m,
            "escalade": escalade, "etiquette": etiquette}


if __name__ == "__main__":
    print("GRAINE inconnu != lecture, inconnu != absence - meme protocole que la graine 1")
    print()
    print("  %-4s %-9s %-12s %-9s %-9s %s"
          % ("var.", "source", "reouverture", "m final", "escalade", "etiquette de trace"))
    table = {}
    for variante in ("A", "B", "C"):
        for source in ("inconnu", "rien", "calme"):
            r = scenario(variante, source)
            table[(variante, source)] = r
            print("  %-4s %-9s %-12s %-9.4f %-9s %s"
                  % (variante, source, r["reouverture"] or "AUCUNE", r["m"],
                     r["escalade"] or "-", r["etiquette"]))
        print()

    a_inconnu = table[("A", "inconnu")]
    a_calme = table[("A", "calme")]
    b_inconnu = table[("B", "inconnu")]
    b_rien = table[("B", "rien")]
    c_inconnu = table[("C", "inconnu")]
    c_rien = table[("C", "rien")]
    c_calme = table[("C", "calme")]

    # 4. LE TEST QUI ECHOUE — six conditions
    assert a_inconnu["fermeture"] == 8, "la porte ne ferme pas au pas 8"
    assert a_inconnu["reouverture"] == 22 and a_calme["reouverture"] == 22, \
        "le defaut A n'apparait pas : l'inconnu ne rouvre pas comme le calme"
    assert b_inconnu["reouverture"] is None and b_rien["reouverture"] is None, \
        "le defaut B n'apparait pas : l'inconnu ne se confond pas avec l'absence"
    assert c_inconnu["reouverture"] is None and abs(c_inconnu["m"] - 0.5877) < 0.0001, \
        "la correction laisse rouvrir : la memoire ne reste pas gelee a 0,5877"
    assert c_inconnu["etiquette"] == "INCONNU" and c_rien["etiquette"] == "ABSENCE", \
        "les deux situations laissent la meme etiquette : la trace ne les separe pas"
    assert c_inconnu["escalade"] == 40, "l'escalade ne tombe pas au pas 40 (30 inconnues apres 10)"
    assert c_calme["reouverture"] == 22, \
        "la correction sur-corrige : le calme mesure ne rouvre plus au pas 22"

    print("  Les six conditions tiennent :")
    print("    - le defaut est present des deux cotes : l'inconnu rouvre au pas 22 comme le")
    print("      calme, et ne rouvre jamais comme l'absence ;")
    print("    - la correction ne rouvre pas et gele m a 0,5877, sans sur-corriger ;")
    print("    - elle separe les traces : INCONNU contre ABSENCE, et escalade au pas 40.")
