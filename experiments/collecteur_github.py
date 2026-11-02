# -*- coding: utf-8 -*-
"""Collecteur L1 — recherche d'issues GitHub, lecture seule, plafond déclaré.

Spécification : `SPEC_AGENT_DETECTEUR_FRICTIONS.md` (dossier de diffusion), couche L1.

Ce que ce fichier fait, et rien d'autre : interroger l'API de recherche d'issues avec les mots
de la douleur, rendre des items bruts, et **déclarer son plafond**. Il ne poste rien, ne répond
à personne, ne mentionne personne : l'API de recherche est en lecture, et aucune fonction
d'écriture n'existe ici — une consigne se contourne, une fonction absente non.

Pourquoi la recherche d'issues plutôt qu'une liste de dépôts : l'API rend `total_count` et
`incomplete_results`, donc **on sait si l'on a tout lu**. C'est la graine 6 satisfaite par
construction et non par discipline.

Trois états par requête, jamais confondus :
    lu et complet      -> lecture=true,  plafond=false
    lu et tronqué      -> lecture=true,  plafond=true   (total_count > lus, ou incomplete_results)
    pas pu lire        -> lecture=false                 (réseau, quota, 403)

Usage :
    python experiments/collecteur_github.py              # banc hors ligne (aucun réseau)
    python experiments/collecteur_github.py --collecter  # passe réelle, sortie JSONL hors dépôt

Aucune dépendance. Le fichier de candidats s'écrit **hors du dépôt** (dossier par défaut :
%USERPROFILE%\\mttv_collecte) : des citations tierces avec URL et auteurs n'ont pas à entrer dans
une archive déposée.

Passage réel du 2026-11-02 — ce que ça a donné, et ce que ça invalide :

    6 requêtes, 3 répondues, 3 refusées (quota non authentifié, 10 requêtes/minute)
    500 items lus, 3 requêtes TRONQUÉES à 150 lus sur des totaux annoncés plus grands
    228 candidats sur 500 items, soit 46 % : entonnoir inutilisable
    précision mesurée à la main sur 20 candidats : 1/20, soit 5 %

Deux hypothèses testées et **réfutées**, dans cet ordre :

    borner le rapprochement à la phrase      -> 183 → 180 candidats (effet négligeable)
    exclure les pull requests (`is:issue`)   -> 180 → 228 candidats (effet inverse)

Conclusion : le problème n'est ni la fenêtre de rapprochement ni le type d'objet, c'est la
**recherche plein texte** elle-même. Deux causes, mesurées : les motifs L2 sont larges (toute
mention de « treated as zero » suffit), et le corpus public des issues est désormais massivement
peuplé de tickets générés par des agents — « Pages traffic report », alignements de PRD — qui
contiennent ce vocabulaire sans formuler aucune plainte.

Étape suivante, à **mesurer** avant d'être affirmée : restreindre L1 à un ensemble **curé de
dépôts** (10 à 30, choisis par domaine), ou exiger un **marqueur de douleur** en troisième
condition. Ne pas retenir l'une des deux sur la foi d'un raisonnement : les deux raisonnements
précédents étaient faux.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import filtre_frictions as l2  # noqa: E402  (couche L2, même dossier)

CHAINE_DE_DETECTION = "FRICTION_COLLECTOR_L1"

API = "https://api.github.com/search/issues"
PER_PAGE = 50
MAX_PAGES = 3
PLAFOND_DUR_API = 1000          # la recherche GitHub ne rend jamais plus de 1 000 résultats

# Choix éditorial, à réviser : chaque requête dit ce qu'on cherche. Vocabulaire d'exploitation,
# jamais le nôtre — « friction nommée dans notre vocabulaire n'est reconnue par personne ».
# Choix éditorial, à réviser — révision du 2026-11-02 après premier passage réel.
# Ce qui a changé, et pourquoi : `is:issue` exclusif. Deux des trois premiers candidats
# étaient des pull requests (« feat: Power Sankey… », « fix: treat an unset holiday slot… »),
# et une PR décrit un correctif, pas une plainte : elle ne nomme pas la friction, elle la
# referme. `in:body` reste, `in:title` serait plus dur mais laisse passer les vraies plaintes
# dont le titre est neutre.
REQUETES = [
    ("silence_lu_comme_zero", '"read as zero" OR "treated as zero" is:issue in:body'),
    ("seuil_qui_derive", 'threshold "depends on" decay is:issue in:body'),
    ("moyenne_qui_masque", 'average hides OR masks disagreement is:issue in:body'),
    ("verrou_sans_sortie", '"dead letter" never retried is:issue in:body'),
    ("plafond_muet", 'maxdepth OR max_depth truncated is:issue in:body'),
    ("plafond_declare", 'has_more next_cursor pagination is:issue in:body'),
]


def _url(requete: str, page: int) -> str:
    return "%s?q=%s&per_page=%d&page=%d" % (API, urllib.parse.quote(requete), PER_PAGE, page)


def _fetcher_http(url: str) -> dict:
    requete = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "flp-frictions/0.1 (lecture seule)",
    })
    with urllib.request.urlopen(requete, timeout=20) as reponse:
        return json.loads(reponse.read().decode("utf-8"))


def _item_brut(hit: dict) -> dict:
    return {
        "source": "github",
        "url": hit.get("html_url"),
        "date": (hit.get("created_at") or "")[:10],
        "auteur": (hit.get("user") or {}).get("login"),
        "texte": ((hit.get("title") or "") + " \n " + (hit.get("body") or "")).strip(),
    }


def collecter(fetcher=None, requetes=None, max_pages=MAX_PAGES):
    """Rend (items bruts, état par requête). `fetcher` est injectable : c'est ce qui rend
    la pagination et le plafond testables sans réseau."""
    fetcher = fetcher or _fetcher_http
    requetes = requetes or REQUETES
    items, etats, vus = [], {}, set()

    for nom, requete in requetes:
        lus, total, incomplete, erreur = 0, None, False, None
        try:
            for page in range(1, max_pages + 1):
                charge = fetcher(_url(requete, page))
                if total is None:
                    total = charge.get("total_count")
                incomplete = bool(charge.get("incomplete_results", False)) or incomplete
                hits = charge.get("items") or []
                if not hits:
                    break
                for hit in hits:
                    url = hit.get("html_url")
                    if url in vus:
                        continue
                    vus.add(url)
                    items.append(_item_brut(hit))
                    lus += 1
                if total is not None and lus >= min(total, PLAFOND_DUR_API):
                    break
        except Exception as e:                      # réseau, quota, 403 : on ne devine pas
            erreur = "%s: %s" % (type(e).__name__, e)

        if erreur:
            # lecture partielle possible : les items déjà reçus restent dans la liste, et le
            # rapport doit le montrer au lieu d'afficher « 0 rendu » avec 50 lus.
            etats[nom] = {"lecture": False, "lus": lus, "rendus": lus, "plafond": False,
                          "motif": erreur, "total_annonce": None}
            continue
        plafond = bool(incomplete)
        if total is not None and (lus < total or total > PLAFOND_DUR_API):
            plafond = True
        etats[nom] = {"lecture": True, "lus": lus, "rendus": lus, "plafond": plafond,
                      "total_annonce": total, "incomplete_results": incomplete}
    return items, etats


def candidats(items):
    """Passe les items bruts au filtre L2 et rend les candidats non vides."""
    sortie = []
    for item in items:
        candidat = l2.analyser(item)
        if candidat:
            sortie.append(candidat)
    return sortie


def ecrire_jsonl(chemin: str, lignes) -> int:
    """Append-only, une ligne par candidat. Aucune réécriture, aucun tri rétroactif."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "a", encoding="utf-8", newline="\n") as f:
        for ligne in lignes:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return len(lignes)


# ---------------------------------------------------------------------------
# Banc hors ligne — trois situations, aucune requête réseau
# ---------------------------------------------------------------------------
def _hit(url, titre, corps, auteur="exemple", date="2026-10-30"):
    return {"html_url": url, "title": titre, "body": corps, "created_at": date + "T10:00:00Z",
            "user": {"login": auteur}}


FIXTURE = {
    # requête 1 : trois résultats annoncés, trois lus sur deux pages -> complet
    "treated%20as%20zero": [
        {"total_count": 3, "incomplete_results": False, "items": [
            _hit("https://g/x/1", "Sensor timeout",
                 "When the sensor goes silent the controller reads a zero and opens the valve."),
            _hit("https://g/x/2", "Unrelated", "We bumped the base image to Debian 12."),
        ]},
        {"total_count": 3, "incomplete_results": False, "items": [
            _hit("https://g/x/3", "Retries",
                 "The retry timeout depends on the internal constant decay, not on the load."),
        ]},
    ],
    # requête 2 : 1 500 annoncés, six lus sur trois pages -> tronqué, et il le dit
    "depends%20on": [
        {"total_count": 1500, "incomplete_results": False, "items": [
            _hit("https://g/y/1", "Seuil", "Notre seuil de coupure bouge quand on touche le paramètre de décroissance."),
            _hit("https://g/y/2", "Fix", "Upgraded the driver to 3.2."),
        ]},
        {"total_count": 1500, "incomplete_results": False, "items": [
            _hit("https://g/y/3", "API", "The API returns 100 items when we ask for 1000 and nothing says more remain."),
            _hit("https://g/y/4", "Docs", "Documented the runbook for on-call rotation."),
        ]},
        {"total_count": 1500, "incomplete_results": False, "items": [
            _hit("https://g/y/5", "Lock", "We have a lock that never reopens after an escalation."),
            _hit("https://g/y/6", "Chat", "Merci pour ce partage, très bon post."),
        ]},
    ],
    # requête 3 : la source ne répond pas
    "average%20hides": RuntimeError("HTTP 403 rate limit exceeded"),
}


def _fixture_fetcher(url: str) -> dict:
    for cle, charge in FIXTURE.items():
        if cle in url:
            if isinstance(charge, Exception):
                raise charge
            page = int(url.rsplit("page=", 1)[1])
            return charge[min(page - 1, len(charge) - 1)]
    raise RuntimeError("URL absente de la fixture : %s" % url)


def _crible():
    echecs = []
    items, etats = collecter(fetcher=_fixture_fetcher)

    attendus = {"silence_lu_comme_zero": (3, False, True),
                "seuil_qui_derive": (6, True, True),
                "moyenne_qui_masque": (0, False, False)}
    for nom, (lus, plafond, lecture) in attendus.items():
        e = etats.get(nom, {})
        if e.get("lus") != lus:
            echecs.append("%s : %s lus au lieu de %d" % (nom, e.get("lus"), lus))
        if bool(e.get("plafond")) != plafond:
            echecs.append("%s : plafond=%s au lieu de %s" % (nom, e.get("plafond"), plafond))
        if bool(e.get("lecture")) != lecture:
            echecs.append("%s : lecture=%s au lieu de %s" % (nom, e.get("lecture"), lecture))

    # « pas pu lire » ne doit jamais être confondu avec « rien trouvé »
    if etats["moyenne_qui_masque"].get("motif") is None:
        echecs.append("une source non lue doit porter son motif")

    # rapport : trois états distincts
    rapport = l2.rapport_sources(etats)
    if rapport["couverture_complete"]:
        echecs.append("une couverture avec une source tronquée et une source non lue ne peut pas être complète")
    if "TRONQUE" not in rapport["sources"]["seuil_qui_derive"]["etat"]:
        echecs.append("le plafond d'une source tronquée doit apparaître dans le rapport")
    if rapport["sources"]["moyenne_qui_masque"]["etat"] != "NON LU":
        echecs.append("une source muette doit s'afficher NON LU, pas vide")

    # pas de doublon, et la couche L2 doit sortir des candidats
    urls = [i["url"] for i in items]
    if len(urls) != len(set(urls)):
        echecs.append("doublon d'URL dans les items")
    cands = candidats(items)
    if len(cands) < 3:
        echecs.append("trop peu de candidats : %d" % len(cands))
    if any(c["motif_declencheur"] == "" or c["ce_qui_refuterait_le_rapprochement"] == "à écrire" for c in cands):
        echecs.append("un candidat sans motif ou sans réfutation")
    return echecs, items, etats, cands


if __name__ == "__main__":
    collecter_reel = "--collecter" in sys.argv
    if not collecter_reel:
        echecs, items, etats, cands = _crible()
        print("chaîne de détection : %s" % CHAINE_DE_DETECTION)
        print("items collectés     : %d" % len(items))
        print("candidats L2        : %d" % len(cands))
        for nom, e in etats.items():
            if not e["lecture"]:
                etat = "NON LU"
            elif e["plafond"]:
                etat = "TRONQUE"
            else:
                etat = "lu"
            print("  %-24s %-8s lus=%-3d annoncés=%s" % (nom, etat, e["lus"], e["total_annonce"]))
        if echecs:
            print("\nCOLLECTEUR L1 : ECHEC")
            for e in echecs:
                print("  - " + e)
            sys.exit(1)
        print("\nCOLLECTEUR L1 : OK — pagination, plafond déclaré et source muette distingués")
    else:
        items, etats = collecter()
        cands = candidats(items)
        dossier = os.environ.get("FLP_COLLECTE") or os.path.join(
            os.path.expanduser("~"), "mttv_collecte")
        chemin = os.path.join(dossier, "candidats.jsonl")
        n = ecrire_jsonl(chemin, cands)
        rapport = l2.rapport_sources(etats)
        rapport.update({"items": len(items), "candidats": n, "fichier": chemin})
        with open(os.path.join(dossier, "rapport.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(rapport, f, ensure_ascii=False, indent=2)
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
