# -*- coding: utf-8 -*-
"""Ton instrument a un plafond.

1. LA PHRASE
   Un instrument qui tronque sans le dire ne produit pas une mesure incomplete : il
   produit une mesure fausse, et fausse du cote rassurant. Ce n'est pas la quantite de
   donnees manquante qui egare, c'est le silence de l'instrument sur sa propre borne.

2. LE CHIFFRE
   python3 graines/graine_plafond_instrument.py
   arbre demande a maxdepth 10 / 20 / 50 : 19 commentaires lus, profondeur 5, les trois
   fois. Le post annoncait 20. Un seul manque, et il est en profondeur 6.
   flux demande a limit 100 / 200 / 1000 : 100 elements rendus, les trois fois, sans
   curseur. Le flux contient 200 elements. Un compte egal au plafond n'est pas un total.

3. LE CODE  (ci-dessous, aucune dependance, aucun reseau)

4. LE TEST QUI ECHOUE
   `assert profondeur(arbre, 50) == 50` echoue : 5.
   `assert len(flux(200)) == 200` echoue : 100.
   Et le test qui devrait nous faire honte : `assert len(flux(100)) < 100` echoue aussi,
   parce que le flux rend exactement 100 -- donc un systeme qui verifie « j'ai recu moins
   que demande » conclut que tout va bien.

5. OU CA MORD
   Reddit (`more`), Hacker News et ses listes paginees, Slack (`has_more` + `response_metadata`),
   limites de profondeur GraphQL, et tout tableau de bord dont la requete rend exactement
   le nombre de lignes de sa clause LIMIT. Partout ou une page pleine passe pour une fin.

6. ORIGINE
   Constat du 2026-10-29 sur une API reelle : `maxdepth` plafonne a 5, `/notifications`
   plafonne a 100 sans curseur. Les chiffres ci-dessus sont ceux du post 11. Le code
   rejoue la forme du defaut sur un arbre synthetique, pour que la graine s'execute
   partout, sans reseau ni identifiant.
"""
PLAFOND_PROFONDEUR = 5      # constate, non choisi
PLAFOND_FLUX = 100          # constate, non choisi


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


def aplatir(noeuds, sortie=None):
    if sortie is None:
        sortie = []
    for n in noeuds or []:
        sortie.append(n)
        aplatir(n.get("replies") or [], sortie)
    return sortie


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


def flux(limite):
    """Ce que l'instrument rend : PLAFOND_FLUX au plus, et jamais de curseur."""
    return [{"id": "n%03d" % i} for i in range(min(limite, PLAFOND_FLUX))]


def plafond_detecte(f, demandes=(10, 20, 50)):
    """Le reflexe : tripler la demande. Si la reponse ne bouge plus, la borne est dedans."""
    tailles = set(len(f(d)) for d in demandes)
    return len(tailles) == 1


def main():
    vus = [len(arbre(d)) for d in (10, 20, 50)]
    profs = [profondeur(arbre(d)) for d in (10, 20, 50)]
    assert vus == [19, 19, 19], "arbre : 19 lus aux trois demandes, mesure %s" % (vus,)
    assert profs == [5, 5, 5], "profondeur : 5 aux trois demandes, mesure %s" % (profs,)
    assert len(arbre(50)) < 20, "le post annoncait 20, l'instrument en rend %d" % len(arbre(50))

    n100, n200, n1000 = len(flux(100)), len(flux(200)), len(flux(1000))
    assert (n100, n200, n1000) == (100, 100, 100), "flux : 100 aux trois limites"
    # Le detecteur n'a de sens que si la demande depasse le plafond : sous 100 elements,
    # un flux plafonne a 100 repond correctement et ne revele rien.
    assert plafond_detecte(flux, (100, 200, 1000)), "le plafond du flux doit etre detectable"
    assert plafond_detecte(arbre, (10, 20, 50)), "le plafond de l'arbre doit etre detectable"
    assert not plafond_detecte(lambda d: arbre(d)[:d], (1, 2, 3)), \
        "un instrument sain ne doit pas etre declare plafonne"

    print("Ton instrument a un plafond")
    print("  arbre : demande 10 / 20 / 50 -> %s commentaires, profondeur %s" % (vus, profs))
    print("  annonce 20, lu %d : %d manquant(s), en profondeur 6"
          % (vus[0], 20 - vus[0]))
    print("  flux  : demande 100 / 200 / 1000 -> %d / %d / %d, curseur : aucun"
          % (n100, n200, n1000))
    print("  reflexe de detection : tripler la demande et regarder si la reponse grandit")
    print("  chaine de detection : PLAFOND_NON_DECLARE")


if __name__ == "__main__":
    main()
