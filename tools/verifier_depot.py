#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vérificateur du dépôt MTTV-FLP — lecture seule, sans dépendance.

Il vérifie ce qu'un ménage doit garantir, et rien d'autre :

  1. les liens internes des .md existent (en retirant le suffixe `:N`, qui est une
     convention de ligne cliquable — l'ignorer produit des dizaines de faux positifs) ;
  2. aucun doublon exact non déclaré (sha256) ;
  3. les copies de déploiement déclarées sont bien IDENTIQUES à leur source ;
  4. les affirmations qu'on sait périmées ne réapparaissent pas, et celles qui
     doivent être présentes le sont ;
  5. le manifeste d'empreintes est à jour (--manifest pour le régénérer).

Usage :
    python tools/verifier_depot.py              # vérifie, code de sortie 0 ou 1
    python tools/verifier_depot.py --manifest   # régénère MANIFESTE_FICHIERS.sha256
    python tools/verifier_depot.py --liste      # affiche ce qui a été contrôlé
"""
import argparse
import hashlib
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MANIFESTE = os.path.join(RACINE, "MANIFESTE_FICHIERS.sha256")

IGNORE_DIRS = {".git", "__pycache__", ".ipynb_checkpoints", ".pytest_cache", ".mypy_cache"}

# Doublons assumés : mêmes contenus, chemins différents, exigés par un déploiement.
DOUBLONS_ASSUMES = {
    ("hf/space/mttv_bgate_system.py", "src/mttv_bgate_system.py"),
    ("hf/space/mttv_mpvr_quorum.py", "mpvr-glocal/src/mttv_mpvr_quorum.py"),
    ("hf/space/mttv_mycelial_handshake.py",
     "mpvr-glocal/src/mttv_mycelial_handshake.py"),
}

# Copies qui doivent rester identiques : une divergence est une erreur, pas un choix.
COPIES_IDENTIQUES = [
    ("src/mttv_bgate_system.py", "hf/space/mttv_bgate_system.py"),
    ("mpvr-glocal/src/mttv_mpvr_quorum.py", "hf/space/mttv_mpvr_quorum.py"),
    ("mpvr-glocal/src/mttv_mycelial_handshake.py", "hf/space/mttv_mycelial_handshake.py"),
]

# Ce qui ne doit plus apparaître nulle part.
INTERDITS = [
    (re.compile(r"22\s+fichiers", re.I),
     "décompte de fichiers périmé (le dépôt en suit davantage)"),
    (re.compile(r"version-2026\.1\.0"),
     "badge de version périmé (la version courante est 1.1.0)"),
]

# Ce qui doit rester présent, et où. Un fait mesuré qui disparaît est une régression.
PRESENCES = [
    ("README.md", "0,6849", "seuil d'amplitude, horizon 10 pas"),
    ("README.md", "0,4025", "seuil absolu de fermeture"),
    ("README.md", "10.5281/zenodo.23671596", "DOI de version 1.1.0"),
    ("CITATION.cff", "10.5281/zenodo.23671596", "DOI de version 1.1.0"),
    ("CHANGELOG.md", "1.1.0", "version journalisée"),
    ("docs/protocole_epreuve_bgate.md", "0,6849", "seuil d'amplitude, horizon 10 pas"),
    ("docs/protocole_epreuve_bgate.md", "0,4025", "seuil absolu"),
]

LIEN = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)\s]+)\)")


def fichiers():
    for dossier, sous, noms in os.walk(RACINE):
        sous[:] = [s for s in sous if s not in IGNORE_DIRS]
        for n in sorted(noms):
            yield os.path.join(dossier, n)


def rel(chemin):
    return os.path.relpath(chemin, RACINE).replace("\\", "/")


def sha(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def lire(chemin):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def verifier_liens(tous):
    problemes, avec_ligne = [], 0
    for f in tous:
        if not f.lower().endswith(".md"):
            continue
        base = os.path.dirname(f)
        for cible in LIEN.findall(lire(f)):
            c = cible.split("#")[0]
            if not c:
                continue
            sans_ligne = re.sub(r":\d+$", "", c)
            chemin = os.path.normpath(os.path.join(base, sans_ligne.replace("%20", " ")))
            if os.path.exists(chemin):
                if sans_ligne != c:
                    avec_ligne += 1
                continue
            problemes.append("%s → %s" % (rel(f), cible))
    return problemes, avec_ligne


def verifier_doublons(tous):
    par_sha = {}
    for f in tous:
        if os.path.getsize(f) > 0:
            par_sha.setdefault(sha(f), []).append(rel(f))
    problemes, assumes = [], 0
    for empreinte, chemins in par_sha.items():
        if len(chemins) < 2:
            continue
        paires = {(a, b) for i, a in enumerate(chemins) for b in chemins[i + 1:]}
        if paires and all(p in DOUBLONS_ASSUMES or (p[1], p[0]) in DOUBLONS_ASSUMES
                          for p in paires):
            assumes += 1
            continue
        problemes.append("doublon non déclaré (%s) : %s" % (empreinte[:12], " · ".join(chemins)))
    return problemes, assumes


def verifier_copies():
    problemes = []
    for source, copie in COPIES_IDENTIQUES:
        a, b = os.path.join(RACINE, source), os.path.join(RACINE, copie)
        if not (os.path.exists(a) and os.path.exists(b)):
            problemes.append("copie déclarée introuvable : %s / %s" % (source, copie))
        elif sha(a) != sha(b):
            problemes.append("copies divergentes : %s ≠ %s" % (source, copie))
    return problemes


def verifier_navigation(mds):
    """Tout document doit etre ATTEIGNABLE, tout dossier doit avoir sa porte.

    Un lien mort est visible (on clique, on tombe sur 404). Un document orphelin ne
    l'est pas : il existe, il est publie, et personne n'y arrive. C'est le defaut que
    cet audit a trouve en premier — 21 fichiers sur 43 dans ce cas.
    """
    mds = [f for f in mds if f.lower().endswith(".md")]
    sortants = {}
    for f in mds:
        cibles = set()
        for lien in LIEN.findall(lire(f)):
            sans_ligne = re.sub(r":\d+$", "", lien.split("#")[0]).replace("%20", " ")
            c = os.path.normpath(os.path.join(os.path.dirname(f), sans_ligne))
            if os.path.isfile(c) and c.lower().endswith(".md"):
                cibles.add(c)
        sortants[f] = cibles

    depart = os.path.join(RACINE, "README.md")
    vus, pile = {depart}, [depart]
    while pile:
        x = pile.pop()
        for y in sortants.get(x, ()):
            if y not in vus:
                vus.add(y)
                pile.append(y)

    problemes = ["document inatteignable depuis README.md : %s" % rel(f)
                 for f in sorted(set(mds) - vus)]

    for d in sorted({os.path.dirname(f) for f in mds}):
        noms = {os.path.basename(f) for f in mds if os.path.dirname(f) == d}
        if not (noms & {"README.md", "INDEX.md", "index.md"}):
            problemes.append("dossier sans porte d'entree (README/INDEX) : %s" % (rel(d) or "."))
    return problemes


def verifier_affirmations(tous):
    problemes = []
    for f in tous:
        if os.path.splitext(f)[1].lower() not in {".md", ".py", ".txt", ".cff", ".json"}:
            continue
        txt = lire(f)
        for motif, quoi in INTERDITS:
            for m in motif.finditer(txt):
                ligne = txt[: m.start()].count("\n") + 1
                problemes.append("%s:%d — %s (« %s »)" % (rel(f), ligne, quoi, m.group(0)))
    for chemin, extrait, quoi in PRESENCES:
        plein = os.path.join(RACINE, chemin)
        if not os.path.exists(plein):
            problemes.append("fichier attendu absent : %s" % chemin)
        elif extrait not in lire(plein):
            problemes.append("%s ne contient plus « %s » (%s)" % (chemin, extrait, quoi))
    return problemes


def ecrire_manifeste(tous):
    lignes = []
    for f in tous:
        r = rel(f)
        if r == "MANIFESTE_FICHIERS.sha256":
            continue
        lignes.append("%s  %s" % (sha(f), r))
    with open(MANIFESTE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(sorted(lignes, key=lambda x: x.split("  ", 1)[1])) + "\n")
    return len(lignes)


def verifier_manifeste(tous):
    if not os.path.exists(MANIFESTE):
        return ["MANIFESTE_FICHIERS.sha256 absent — lancer --manifest"]
    attendu = {}
    for ligne in lire(MANIFESTE).splitlines():
        if not ligne.strip():
            continue
        empreinte, chemin = ligne.split("  ", 1)
        attendu[chemin] = empreinte
    problemes = []
    presents = {rel(f) for f in tous} - {"MANIFESTE_FICHIERS.sha256"}
    for chemin in sorted(presents - set(attendu)):
        problemes.append("fichier non inscrit au manifeste : %s" % chemin)
    for chemin in sorted(set(attendu) - presents):
        problemes.append("fichier inscrit mais absent : %s" % chemin)
    for chemin in sorted(presents & set(attendu)):
        if sha(os.path.join(RACINE, chemin)) != attendu[chemin]:
            problemes.append("empreinte modifiée : %s" % chemin)
    return problemes


def main():
    ap = argparse.ArgumentParser(description="Vérification du dépôt MTTV-FLP.")
    ap.add_argument("--manifest", action="store_true", help="régénère le manifeste")
    ap.add_argument("--liste", action="store_true", help="affiche le détail contrôlé")
    args = ap.parse_args()

    tous = sorted(fichiers())

    if args.manifest:
        n = ecrire_manifeste(tous)
        print("manifeste régénéré : %d fichier(s)" % n)
        return 0

    liens, avec_ligne = verifier_liens(tous)
    doublons, assumés = verifier_doublons(tous)
    copies = verifier_copies()
    navigation = verifier_navigation(tous)
    affirmations = verifier_affirmations(tous)
    manifeste = verifier_manifeste(tous)

    blocs = [
        ("Liens internes morts", liens),
        ("Doublons non déclarés", doublons),
        ("Copies de déploiement divergentes", copies),
        ("Navigation (atteignabilité, portes d'entrée)", navigation),
        ("Affirmations périmées ou manquantes", affirmations),
        ("Manifeste d'empreintes", manifeste),
    ]

    total = sum(len(p) for _, p in blocs)
    print("racine   : %s" % RACINE)
    print("fichiers : %d" % len(tous))
    print("liens    : %d valides avec suffixe `:N` (faux positifs évités)" % avec_ligne)
    print("doublons : %d assumé(s) et identique(s)" % assumés)
    print("")
    for titre, problemes in blocs:
        etat = "OK" if not problemes else "%d problème(s)" % len(problemes)
        print("[%s] %s" % (etat, titre))
        for p in problemes:
            print("    - %s" % p)
        if args.liste and not problemes:
            print("    (rien à signaler)")

    print("")
    if total:
        print("VERDICT : %d problème(s)." % total)
        return 1
    print("VERDICT : dépôt cohérent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
