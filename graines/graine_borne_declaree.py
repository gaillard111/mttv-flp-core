# -*- coding: utf-8 -*-
"""GRAINE - borne declaree : le nombre imprime reste dans l'intervalle que son cadre definit.

1. LE DEFAUT, EN UNE PHRASE
   Un nombre imprime n'est pas verifie contre le cadre que son propre texte nomme : l'instrument
   regarde la borne haute, jamais la borne basse, et lit comme conforme ce dont le texte ne nomme
   aucune borne. Une duree negative, un age anterieur a sa creation, un compte au-dela de l'annonce
   passent donc pour des mesures saines.

2. LE CHIFFRE
   Dix nombres imprimes, dont cinq sortent du cadre que leur texte nomme.
     version fautive            -> 2 violations vues sur 5 ; 8 nombres declares conformes
     version corrigee           -> 5 sur 5, et 2 « non visible » declares comme tels
     les trois manquees         -> toutes par la borne basse (-100 s, -1 s, -3 j)
     les deux silences          -> un nombre sans cadre est declare conforme, non illisible
   La troisieme ligne est la clause de ce cas : quand le texte ne nomme aucune borne, il n'y a plus
   rien a verifier - mais l'instrument fautif n'a pas de troisieme valeur pour le dire, et fabrique
   du calme (cf. graine 1, PENALITE_CALME).
   Reproduire :  python graines/graine_borne_declaree.py
   Re-derivable a la main : une valeur est « violation » si elle depasse le max du cadre ou si elle
   passe sous son min ; « non visible » si le cadre vaut None. Le code fautif teste le max seul et
   rend « tenue » quand le cadre vaut None.
     cas 1 -> -100.0 s, cadre [0, -] : passe sous le min. Fautif : tenue. Corrige : violation.
     cas 3 -> 104.0 %, cadre [0, 100] : depasse le max. Fautif : violation. Corrige : violation.
     cas 7 -> 5.0 s, aucun cadre : rien a verifier. Fautif : tenue. Corrige : non visible.
   D'ou 2 vues sur 5 : un instrument qui ne regarderait qu'une borne ne serait pas un instrument,
   ce serait un seuil ; et un instrument qui appellerait violation tout nombre nu serait un
   accusateur. Les deux erreurs sont mesurees ici.

3. LE CODE MINIMAL  (deux bornes, trois valeurs, aucune dependance)
   ------------------------------------------------------------------
   def verdict_fautif(valeur, cadre):
       if cadre is None:                     return "tenue"        # <- le silence
       if cadre["max"] is not None and valeur > cadre["max"]:
                                             return "violation"
       return "tenue"                                                # <- le min ignore

   def verdict_corrige(valeur, cadre):
       if cadre is None:                     return "non visible"
       if cadre["max"] is not None and valeur > cadre["max"]:
                                             return "violation"
       if cadre["min"] is not None and valeur < cadre["min"]:
                                             return "violation"
       return "tenue"
   ------------------------------------------------------------------

4. LE TEST QUI ECHOUE
   Ce fichier porte les deux versions, imprime le tableau des dix nombres, et refuse de sortir en
   silence si le defaut n'apparait pas, s'il est total, si la correction ne rattrape pas les trois
   bornes basses, ou si elle se met a accuser les deux nombres sans cadre. Cinq `assert`.

5. OU ELLE MORD
   - integrations continues : « tache Normalize Release Tag - skipped - -1m40s », horodatage pris
     avant l'ouverture du travail et soustrait apres ;
   - compteurs de boucle qui ne peuvent pas decroitre (« 7 restantes » la ou l'annonce en donnait 5) ;
   - ages de fichiers anterieurs a leur creation, apres restauration d'une sauvegarde ;
   - pourcentages au-dela de 100 par cumul de sous-totaux deja comptes.
   Chaine de detection : PROPRIETE_NON_TENUE (identifiant rare, cherchable).
"""

PROPRIETE_NON_TENUE = "propriete non tenue : la valeur sort du cadre que son texte nomme"

TENUE, VIOLATION, NON_VISIBLE = "tenue", "violation", "non visible"

CADRE_DUREE = {"min": 0.0, "max": None}          # une duree ne peut pas etre negative
CADRE_PART = {"min": 0.0, "max": 100.0}          # un pourcentage de couverture
CADRE_AGE = {"min": 0.0, "max": None}            # un age ne precede pas sa creation
CADRE_RESTANT = {"min": 0.0, "max": 5.0}         # un reste ne depasse pas l'annonce

CAS = [
    # (texte cite, valeur imprimee, cadre nomme par le texte - None si aucun)
    ("Normalize Release Tag - skipped - -1m40s", -100.0, CADRE_DUREE),
    ("suite de tests : terminee en -1.0s", -1.0, CADRE_DUREE),
    ("couverture : 104 %", 104.0, CADRE_PART),
    ("couverture : 42 %", 42.0, CADRE_PART),
    ("age du fichier : -3 jours", -3.0, CADRE_AGE),
    ("cache chaud : 0.0s", 0.0, CADRE_DUREE),
    ("snmp took 5s", 5.0, None),
    ("worker up for 7 days", 7.0, None),
    ("restantes : 7, annonce : 5", 7.0, CADRE_RESTANT),
    ("build en 12s", 12.0, CADRE_DUREE),
]


def verdict_fautif(valeur, cadre):
    """Version fautive : la borne haute seule, et l'absence de cadre lue comme conformite."""
    if cadre is None:
        return TENUE
    if cadre["max"] is not None and valeur > cadre["max"]:
        return VIOLATION
    return TENUE


def verdict_corrige(valeur, cadre):
    """Version corrigee : les deux bornes, et une troisieme valeur pour ce qui n'est pas lisible."""
    if cadre is None:
        return NON_VISIBLE
    if cadre["max"] is not None and valeur > cadre["max"]:
        return VIOLATION
    if cadre["min"] is not None and valeur < cadre["min"]:
        return VIOLATION
    return TENUE


def cadre_lisible(cadre):
    if cadre is None:
        return "aucun"
    bas = "-" if cadre["min"] is None else "%g" % cadre["min"]
    haut = "-" if cadre["max"] is None else "%g" % cadre["max"]
    return "[%s, %s]" % (bas, haut)


def mesurer(verdict):
    """Rend (violations, tenues, non_visibles) sur les dix cas."""
    compte = {VIOLATION: 0, TENUE: 0, NON_VISIBLE: 0}
    for _, valeur, cadre in CAS:
        compte[verdict(valeur, cadre)] += 1
    return compte[VIOLATION], compte[TENUE], compte[NON_VISIBLE]


def compte_par_verdict(verdict):
    return [verdict(valeur, cadre) for _, valeur, cadre in CAS]


if __name__ == "__main__":
    print("GRAINE borne declaree - dix nombres, cinq hors de leur cadre")
    print()
    print("  %-3s %-42s %-12s %-14s %-14s" % ("#", "texte", "valeur", "fautif", "corrige"))
    fautives = compte_par_verdict(verdict_fautif)
    corrigees = compte_par_verdict(verdict_corrige)
    for i, ((texte, valeur, cadre), fautif, corrige) in enumerate(zip(CAS, fautives, corrigees), 1):
        print("  %-3s %-42s %-12s %-14s %-14s" % (i, texte[:42], "%g %s" % (valeur, cadre_lisible(cadre)),
                                                 fautif, corrige))
    print()

    v_f, t_f, n_f = mesurer(verdict_fautif)
    v_c, t_c, n_c = mesurer(verdict_corrige)
    manquees = sum(1 for f, c in zip(fautives, corrigees) if f != VIOLATION and c == VIOLATION)
    silences = sum(1 for f, c in zip(fautives, corrigees) if f == TENUE and c == NON_VISIBLE)

    print("  %-52s %s" % ("version fautive", "%d violations / %d tenues / %d non visibles"
                          % (v_f, t_f, n_f)))
    print("  %-52s %s" % ("version corrigee", "%d violations / %d tenues / %d non visibles"
                          % (v_c, t_c, n_c)))
    print("  %-52s %d" % ("violations manquees par la version fautive", manquees))
    print("  %-52s %d" % ("dont silences lus comme conformes (aucun cadre)", silences))
    print()

    # 4. LE TEST QUI ECHOUE - cinq conditions, verifiees
    assert v_f == 2, "le defaut n'apparait pas : la graine ne prouve rien"
    assert manquees == 3, "les bornes basses ne sont pas celles qui manquent"
    assert silences == 2, "l'absence de cadre n'est pas lue comme conformite"
    assert v_c == 5, "la correction ne voit pas les cinq valeurs hors cadre"
    assert t_c == 3 and n_c == 2, "la correction sur-detecte : un nombre sans cadre n'est pas " \
                                 "une violation"

    print("  Les cinq conditions tiennent :")
    print("    - le defaut est present (2 violations vues sur 5) ;")
    print("    - il n'est pas total (les deux depassements de max sont bien vus) ;")
    print("    - les trois manquees passent toutes par la borne basse ;")
    print("    - la correction les rattrape (5 sur 5) ;")
    print("    - et elle ne declare pas coupables les deux nombres dont le texte ne nomme")
    print("      aucune borne : elle dit « non visible ». C'est ce troisieme etat qui fait de")
    print("      ce cas une graine de propriete et non une chasse aux nombres negatifs.")
