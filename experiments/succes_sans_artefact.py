# -*- coding: utf-8 -*-
"""Mesure extérieure — un succès vert sans artefact produit (graine 9 appliquée dehors).

La graine 9 dit qu'une réponse peut avoir eu lieu sans rien porter. Ici, la même question posée
à des systèmes qui ne sont pas les nôtres : parmi les dépôts déjà arrêtés pour la surveillance
(`collecteur_depots.DEPOTS`, liste canonique, jamais dupliquée), combien ont une tâche
**planifiée** dont le dernier passage est en **succès** alors que le dernier artefact produit est
plus vieux que la fenêtre déclarée — ou n'existe pas du tout.

Ce que l'instrument ne peut pas dire, et qu'il déclare plutôt que de le taire :

  - `ARTEFACTS_ABSENTS` — le dépôt n'upload jamais d'artefact : « pas d'artefact » n'y prouve
    rien. Ces dépôts sont comptés à part et n'entrent **jamais** dans le numérateur ;
  - `AUCUN_PLANIFIE` — pas de tâche planifiée visible : rien à mesurer, et ce n'est pas un zéro ;
  - `PLAFOND` — quota anonyme de l'API (60 requêtes/heure). Un dépôt non lu est déclaré
    `lecture=false` avec son code HTTP, **jamais** compté comme « rien trouvé ».

Deux requêtes par dépôt, aucune écriture, aucune dépendance, aucun jeton dans le code.

Usage : python experiments/succes_sans_artefact.py
"""
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                                     # noqa: BLE001
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collecteur_depots import DEPOTS  # noqa: E402

API = "https://api.github.com/repos"
FENETRE_JOURS = 30
ENTETES = {"User-Agent": "MTTV-FLP-mesure", "Accept": "application/vnd.github+json"}
JETON = os.environ.get("GITHUB_TOKEN")
if JETON:
    ENTETES["Authorization"] = "Bearer " + JETON


def lire(chemin):
    """Rend (statut, corps). Aucune exception ne remonte : un échec est une donnée."""
    try:
        with urllib.request.urlopen(urllib.request.Request(API + chemin, headers=ENTETES),
                                    timeout=30) as reponse:
            return reponse.status, json.loads(reponse.read().decode("utf-8"))
    except urllib.error.HTTPError as erreur:
        return erreur.code, {"_erreur": (erreur.read().decode("utf-8") or "")[:120]}
    except Exception as erreur:                                       # noqa: BLE001
        return 0, {"_erreur": str(erreur)[:120]}


def jours_depuis(horodatage, maintenant):
    if not horodatage:
        return None
    return (maintenant - datetime.datetime.strptime(
        horodatage, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)).days


def classer(depot, maintenant):
    """Rend un dictionnaire : etat, detail, lecture (vrai si le dépôt a répondu)."""
    st, corps = lire("/%s/actions/runs?event=schedule&per_page=1" % depot)
    if st != 200:
        return {"depot": depot, "etat": "PLAFOND" if st in (403, 429) else "LECTURE_FALSE",
                "detail": "HTTP %s" % st, "lecture": False}
    runs = corps.get("workflow_runs") or []
    if not runs:
        return {"depot": depot, "etat": "AUCUN_PLANIFIE", "detail": "-", "lecture": True}

    run = runs[0]
    conclusion = run.get("conclusion")
    statut = run.get("status")
    age_run = jours_depuis(run.get("updated_at") or run.get("created_at"), maintenant)
    if statut != "completed":
        return {"depot": depot, "etat": "EN_COURS",
                "detail": "status %s, demarre il y a %s j" % (statut, age_run), "lecture": True}
    if conclusion != "success":
        return {"depot": depot, "etat": "DERNIER_NON_VERT",
                "detail": "%s, il y a %s j" % (conclusion, age_run), "lecture": True}

    st, corps = lire("/%s/actions/artifacts?per_page=1" % depot)
    if st != 200:
        return {"depot": depot, "etat": "PLAFOND" if st in (403, 429) else "LECTURE_FALSE",
                "detail": "artefacts HTTP %s" % st, "lecture": False}
    total = corps.get("total_count") or 0
    if total == 0:
        return {"depot": depot, "etat": "ARTEFACTS_ABSENTS",
                "detail": "vert il y a %s j, aucun artefact" % age_run, "lecture": True}

    dernier = (corps.get("artifacts") or [{}])[0].get("created_at")
    age_art = jours_depuis(dernier, maintenant)
    if age_art is None:
        return {"depot": depot, "etat": "ARTEFACTS_ABSENTS", "detail": "date illisible",
                "lecture": True}
    if age_art < 0:
        # Une date posterieure a maintenant n'est pas un age : c'est une anomalie de la source.
        # On la declare au lieu de la laisser s'imprimer en negatif, comme si -1 j voulait dire
        # quelque chose. Rencontre une fois sur 20 depots le 2026-11-12.
        return {"depot": depot, "etat": "DATE_A_VENIR", "detail": "artefact date %s" % dernier,
                "lecture": True}
    if age_art > FENETRE_JOURS:
        return {"depot": depot, "etat": "VERT_SANS_ARTEFACT_RECENT",
                "detail": "vert il y a %s j, artefact il y a %s j" % (age_run, age_art),
                "lecture": True}
    return {"depot": depot, "etat": "OK",
            "detail": "vert il y a %s j, artefact il y a %s j" % (age_run, age_art),
            "lecture": True}


def main():
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    print("SUCCES SANS ARTEFACT — %d depots, fenetre declaree %d jours, %s"
          % (len(DEPOTS), FENETRE_JOURS, "avec jeton" if JETON else "sans jeton"))
    print()
    print("  %-46s %-28s %s" % ("depot", "etat", "detail"))
    resultats = [classer(depot, maintenant) for depot, _ in DEPOTS]
    for r in resultats:
        print("  %-46s %-28s %s" % (r["depot"], r["etat"], r["detail"]))

    lus = [r for r in resultats if r["lecture"]]
    compte = {}
    for r in lus:
        compte[r["etat"]] = compte.get(r["etat"], 0) + 1
    defaut = compte.get("VERT_SANS_ARTEFACT_RECENT", 0)

    print()
    print("  lus : %d / %d | non lus : %d" % (len(lus), len(resultats), len(resultats) - len(lus)))
    for etat in sorted(compte):
        print("    %-28s %d" % (etat, compte[etat]))
    print()
    if not lus:
        print("  AUCUNE MESURE : aucun depot n'a repondu. Ce n'est pas un zero, c'est une panne.")
    elif defaut == 0:
        print("  ZERO mesure : sur %d depots lus, aucun succes vert sans artefact recent." % len(lus))
        print("  Un zero se consigne comme un zero, et ne se lit pas comme une absence de defaut.")
    else:
        print("  %d depot(s) sur %d lus portent un succes vert sans artefact plus recent que %d j."
              % (defaut, len(lus), FENETRE_JOURS))
    if any(r["etat"] == "ARTEFACTS_ABSENTS" for r in lus):
        print("  Rappel : les %d depots sans artefact sont hors numerateur — ils ne prouvent rien."
              % compte.get("ARTEFACTS_ABSENTS", 0))


if __name__ == "__main__":
    main()
