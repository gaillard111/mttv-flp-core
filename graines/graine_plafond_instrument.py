# -*- coding: utf-8 -*-
"""Ton instrument a un plafond.

1. LA PHRASE
   Un instrument qui tronque sans le dire ne produit pas une mesure incomplete : il
   produit une mesure fausse, et fausse du cote rassurant. Mais il y a deux facons de
   tronquer, et une seule est une faute de l'instrument : la seconde est une faute de
   lecture, et c'est la plus embarrassante.

2. LE CHIFFRE
   python3 graines/graine_plafond_instrument.py
   Plafond MUET -- arbre demande a maxdepth 10 / 20 / 50 : 19 commentaires lus,
   profondeur 5, les trois fois, quand le post en annoncait 20. Un seul manque, et il
   est en profondeur 6. L'instrument ne dit rien ; il coupe.
   Plafond DECLARE -- flux demande a limit 100 / 200 / 1000 : 100 elements rendus, les
   trois fois. Mais la reponse porte `has_more: true` et un `next_cursor`. Le flux nous
   a prevenus. Nous avons lu le tableau et jamais l'enveloppe, pendant trois jours.

3. LE CODE  (ci-dessous, aucune dependance, aucun reseau)

4. LE TEST QUI ECHOUE
   `assert profondeur(arbre, 50) == 50` echoue : 5.
   `assert len(flux_muet(200)) == 200` echoue : 100, et rien ne le signale.
   `assert not flux_declare(200)[1]` echoue aussi -- `has_more` vaut vrai. Ce troisieme
   echec est le notre : l'instrument avait parle, et nous ne l'avons pas ecoute.

5. OU CA MORD
   Reddit (`more`), Hacker News et ses listes paginees, Slack (`has_more` +
   `response_metadata`), limites de profondeur GraphQL, et tout tableau de bord dont la
   requete rend exactement le nombre de lignes de sa clause LIMIT. Partout ou une page
   pleine passe pour une fin.

6. ORIGINE ET CORRECTION
   Constat du 2026-10-29 sur une API reelle : `maxdepth` plafonne a la profondeur 5 quel
   que soit N (plafond muet), et le flux rend 100 elements par page (plafond declare).
   Le 2026-11-01, une relecture de l'enveloppe a montre `has_more` et `next_cursor` dans
   la reponse : notre phrase « plafonne a 100 sans curseur » etait fausse, et c'est
   exactement le defaut que cette graine denonce. Les chiffres du post 11 (20 annonces,
   19 lisibles) sont rejoues sur un arbre synthetique, pour que la graine s'execute
   partout.
"""
PLAFOND_PROFONDEUR = 5      # constate, non choisi
PLAFOND_FLUX = 100          # constate, non choisi
TOTAL_FLUX = 200            # ce que le flux contient reellement


def arbre_post11():
    """Vingt commentaires : une chaine de six, plus quatorze accroches en profondeur 2."""
    chaine = {"id": "d1", "depth": 1, "replies": []}
    courant = chaine
    for niveau in range(2, 7):
        suivant = {"id": "d%d" % niveau, "depth": niveau, "replies": []}
        courant["replies"].append(suivant)
        courant = suivant
    for i in range(14):
        chaine["replies"].append({"id": "s%02d" % i, "depth": 2, "replies": []})
    return [chaine]


def arbre(demandee):
    """Ce que l'instrument rend : il coupe a PLAFOND_PROFONDEUR, quoi qu'on demande."""
    coupe = min(demandee, PLAFOND_PROFONDEUR)

    def descendre(liste, niveau):
        if niveau > coupe:
            return []
        sortie = []
        for n in liste:
            sortie.append(n)
            sortie.extend(descendre(n["replies"], niveau + 1))
        return sortie

    return descendre(arbre_post11(), 1)


def profondeur(noeuds):
    return max([(n.get("depth") or 0) for n in noeuds] or [0])


def flux_muet(limite):
    """Plafond MUET : pas de curseur, pas de drapeau. L'instrument se tait."""
    return [{"id": "n%03d" % i} for i in range(min(limite, PLAFOND_FLUX))]


def flux_declare(limite, deja=0):
    """Plafond DECLARE : la page est coupee et le dit. -> (items, has_more, curseur)."""
    taille = min(min(limite, PLAFOND_FLUX), TOTAL_FLUX - deja)
    items = [{"id": "n%03d" % (deja + i)} for i in range(taille)]
    reste = (TOTAL_FLUX - deja) > taille
    return items, reste, ("c%d" % (deja + taille) if reste else None)


def drainer():
    """Suivre le curseur jusqu'a epuisement. -> (total atteint, nombre de pages)."""
    total, pages, reste = 0, 0, True
    while reste:
        items, reste, _ = flux_declare(PLAFOND_FLUX, deja=total)
        total += len(items)
        pages += 1
        if pages > 20:
            break
    return total, pages


def plafond_detecte(f, demandes=(10, 20, 50)):
    """Le reflexe pour un plafond muet : tripler la demande et voir si la reponse grandit."""
    return len(set(len(f(d)) for d in demandes)) == 1


def main():
    vus = [len(arbre(d)) for d in (10, 20, 50)]
    profs = [profondeur(arbre(d)) for d in (10, 20, 50)]
    assert vus == [19, 19, 19], "arbre : 19 lus aux trois demandes, mesure %s" % (vus,)
    assert profs == [5, 5, 5], "profondeur : 5 aux trois demandes, mesure %s" % (profs,)
    assert plafond_detecte(arbre, (10, 20, 50)), "le plafond de l'arbre doit etre detectable"
    assert not plafond_detecte(lambda d: arbre(d)[:d], (1, 2, 3)), \
        "un instrument sain ne doit pas etre declare plafonne"

    assert len(flux_muet(200)) == 100, "plafond muet : 100 elements, aucun signal"
    items, reste, curseur = flux_declare(200)
    assert (len(items), reste) == (100, True), "plafond declare : 100 elements et has_more"
    assert curseur is not None, "un plafond declare fournit un curseur"
    total, pages = drainer()
    assert (total, pages) == (TOTAL_FLUX, 2), \
        "en suivant le curseur on atteint %d en %d pages" % (total, pages)

    print("Ton instrument a un plafond")
    print("  plafond MUET    arbre : demande 10 / 20 / 50 -> %s lus, profondeur %s"
          % (vus, profs))
    print("                  le post annoncait 20 : %d manquant, en profondeur 6" % (20 - vus[0]))
    print("  plafond DECLARE flux  : demande 200 -> %d elements, has_more = %s, curseur = %s"
          % (len(items), reste, curseur))
    print("                  le flux contient %d elements ; il l'a dit, nous ne l'avons pas lu"
          % TOTAL_FLUX)
    print("  deux reflexes : tripler la demande (muet), lire l'enveloppe (declare)")
    print("  chaine de detection : PLAFOND_NON_DECLARE")


if __name__ == "__main__":
    main()
