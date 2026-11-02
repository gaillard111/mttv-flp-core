# -*- coding: utf-8 -*-
"""GRAINE — fausse identite : le nom designe autre chose que le fautif.

1. LE DEFAUT, EN UNE PHRASE
   Un artefact nomme une identite — chemin, parametre, entite — qui n'est pas la fautive.
   Le nom est plausible, il existe, il se recopie : c'est pourquoi il se propage mieux qu'un
   silence. Celui qui le lit va reparer la mauvaise chose, et le defaut survivra au reparage.

2. LE CHIFFRE
   Six incidents, dont quatre ou un homonyme CONFORME se trouve dans le dossier demande :
     version fautive            -> 4 noms sur 6 designent une identite conforme ;
     version corrigee           -> 6 sur 6 designent la fautive ;
     memes incidents, noms rendus uniques, code fautif inchange -> 0 sur 6.
   La troisieme ligne est la clause de bascule du patron (CONTRIBUTING.md, section 5) : quand on
   remet les noms justes, le defaut tombe sans qu'aucune autre mesure ne bouge. Le defaut EST le
   nom ; il n'y a pas de douleur derriere l'etiquette.
   Reproduire :  python graines/graine_fausse_identite.py
   Re-derivable a la main : proximite = 2 points si le dossier correspond, 1 point si le nom de
   fichier correspond ; le code fautif retient le maximum, sans regarder l'etat.
     cas 1 -> reports/run-0041.json : 2 points (conforme) ; archive/run-0042.json : 1 point
              (fautif). Il nomme le premier, qui est conforme.
     cas 5 -> logs/worker.err : 2 points (fautif) ; other/worker.err : 1 point. Il nomme le bon.
   D'ou 4 fautifs sur 6, et non 6 sur 6 : un artefact toujours trompe serait un artefact aveugle,
   ce n'est pas ce defaut-la.

3. LE CODE MINIMAL  (huit lignes, aucune dependance, aucun etat cache)
   ------------------------------------------------------------------
   def proximite(demande, nom):
       points = 0
       if demande[0] == nom[0]: points += 2      # meme dossier
       if demande[1] == nom[1]: points += 1      # meme nom de fichier
       return points

   def nommer_fautif(demande, candidats):        # <- le defaut
       return max(candidats, key=lambda c: proximite(demande, c))

   def nommer_corrige(demande, candidats):       # <- la correction
       fautifs = [c for c in candidats if c[2] == "defaillante"]
       return fautifs[0] if len(fautifs) == 1 else None
   ------------------------------------------------------------------

4. LE TEST QUI ECHOUE
   Ce fichier contient les deux versions, mesure les trois lignes du 2 et refuse de sortir en
   silence si le defaut n'apparait pas, s'il est total, ou s'il survit a la correction des noms.
   Cinq `assert`, executes plus bas.

5. OU ELLE MORD
   - messages d'erreur qui suggerent le nom le plus proche au lieu de nommer le fautif ;
   - parametres fantomes : un message cite `min_periods` quand le code attend `min_count` ;
   - journaux de build qui accusent le fichier voisin du dossier analyse ;
   - renommages partiels : l'ancien nom survit dans une couche et designe la mauvaise entite.
   Chaine de detection : NOM_FAUTIF_ECARTE (identifiant rare, cherchable).
"""

NOM_FAUTIF_ECARTE = "nom ecarte : l'identite designee n'est pas la fautive"

CAS = [
    # (demande, [(dossier, fichier, etat), ...]) — un seul candidat defaillant par cas
    (("reports", "run-0042.json"), [("reports", "run-0041.json", "conforme"),
                                    ("archive", "run-0042.json", "defaillante")]),
    (("configs", "model.yaml"), [("configs", "model-v2.yaml", "conforme"),
                                 ("backup", "model.yaml", "defaillante")]),
    (("logs", "api.log"), [("logs", "api.log.1", "conforme"),
                           ("rotated", "api.log", "defaillante")]),
    (("data", "part-000.parquet"), [("data", "part-001.parquet", "conforme"),
                                    ("staging", "part-000.parquet", "defaillante")]),
    # cas sans homonyme conforme dans le dossier demande : le defaut ne peut pas se produire
    (("logs", "worker.err"), [("logs", "worker.err", "defaillante"),
                              ("other", "worker.err", "conforme")]),
    (("metrics", "snmp.json"), [("metrics", "snmp.json", "defaillante"),
                                ("old", "snmp.json", "conforme")]),
]


def proximite(demande, nom):
    """Deux points pour le dossier, un point pour le nom de fichier."""
    points = 0
    if demande[0] == nom[0]:
        points += 2
    if demande[1] == nom[1]:
        points += 1
    return points


def nommer_fautif(demande, candidats):
    """Version fautive : nomme le nom le plus proche, sans regarder l'etat."""
    return max(candidats, key=lambda c: proximite(demande, c))


def nommer_corrige(demande, candidats):
    """Version corrigee : ecarte les noms conformes, ne nomme que le fautif unique."""
    fautifs = [c for c in candidats if c[2] == "defaillante"]
    if len(fautifs) != 1:
        return None
    return fautifs[0]


def noms_uniques(cas):
    """Retire de chaque incident tout nom qui n'est pas celui du fautif."""
    return [(demande, [c for c in candidats if c[2] == "defaillante"])
            for demande, candidats in cas]


def mesurer(cas, nommeur):
    """Rend (faux, justes, aveugles) : faux = a nomme une identite conforme."""
    faux, justes, aveugles = 0, 0, 0
    for demande, candidats in cas:
        nom = nommeur(demande, candidats)
        if nom is None:
            aveugles += 1
        elif nom[2] == "defaillante":
            justes += 1
        else:
            faux += 1
    return faux, justes, aveugles


def etiquette(nom):
    if nom is None:
        return "%s (aucun nom)" % NOM_FAUTIF_ECARTE
    return "%s/%s [%s]" % (nom[0], nom[1], nom[2])


if __name__ == "__main__":
    print("GRAINE fausse identite — six incidents, deux identites qui se ressemblent")
    print()
    print("  %-3s %-24s %-34s %-34s" % ("#", "demande", "version fautive",
                                        "version corrigee"))
    for i, (demande, candidats) in enumerate(CAS, 1):
        demande_lisible = "%s/%s" % demande
        print("  %-3s %-24s %-34s %-34s" % (i, demande_lisible,
                                            etiquette(nommer_fautif(demande, candidats)),
                                            etiquette(nommer_corrige(demande, candidats))))
    print()

    faux, justes, _ = mesurer(CAS, nommer_fautif)
    faux_c, justes_c, _ = mesurer(CAS, nommer_corrige)

    uniques = noms_uniques(CAS)
    faux_u, justes_u, _ = mesurer(uniques, nommer_fautif)
    faux_uc, justes_uc, _ = mesurer(uniques, nommer_corrige)

    print("  %-46s %s" % ("version fautive, noms ambigus", "%d faux / %d justes" % (faux, justes)))
    print("  %-46s %s" % ("version corrigee, noms ambigus", "%d faux / %d justes"
                                                   % (faux_c, justes_c)))
    print("  %-46s %s" % ("version fautive, noms rendus uniques", "%d faux / %d justes"
                                                   % (faux_u, justes_u)))
    print("  %-46s %s" % ("version corrigee, noms uniques", "%d faux / %d justes"
                                                   % (faux_uc, justes_uc)))
    print()

    # 4. LE TEST QUI ECHOUE — cinq conditions, verifiees
    assert faux == 4, "le defaut n'apparait pas : la graine ne prouve rien"
    assert justes == 2, "le defaut est total : ce n'est plus une fausse identite, " \
                        "c'est un artefact aveugle"
    assert faux_c == 0 and justes_c == 6, "la correction ne nomme pas toujours la fautive"
    assert faux_u == 0, "le defaut survit a la correction des noms : ce n'est donc pas une " \
                        "erreur d'identite, c'est une classe et non une graine"
    assert justes_u == 6, "la correction sur-corrige : elle ne nomme plus rien quand tout est clair"

    print("  Les cinq conditions tiennent :")
    print("    - le defaut est present (4 noms sur 6 designent une identite conforme) ;")
    print("    - il n'est pas total (2 sur 6 sont justes, la ou aucun homonyme ne se presente) ;")
    print("    - la correction le supprime (6 sur 6 nomment la fautive) ;")
    print("    - les memes noms rendus uniques, le code fautif redevient juste (0 sur 6) :")
    print("      le defaut EST le nom, c'est ce qui fait de ce cas une graine et non une classe.")
