#!/usr/bin/env python3
"""
Banc de suspension — phase 1 (exploration) du programme RMP.

Question posée
--------------
Le nombre N de marques de suspension insérées juste avant la question
modifie-t-il la distribution de la première réponse ?

Prédiction : voir experiments/README.md. Elle est fixée AVANT toute
exécution — c'est la condition qui rend un résultat défavorable lisible.

Trois modes, aucun appel implicite :
    --plan      n'appelle rien ; affiche le plan et le coût estimé
    --verifier  deux appels seulement ; contrôle que N agit réellement
    --mesurer   balayage complet (6 valeurs de N x 3 questions)

Licence : CC0 — domaine public.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Réglages — tous figés ici pour que le journal soit rejouable
# ---------------------------------------------------------------------------

MODELE = "meta-llama/Llama-3.1-8B-Instruct"
# Instrument unique disponible sur ce compte au 2 octobre 2026 : vérifié
# (répond, et renvoie le logprob du jeton produit). top_logprobs = None :
# la distribution complète n'est pas fournie, d'où l'estimation empirique.

N_VALEURS = (0, 1, 2, 4, 8, 16)
ECHANTILLONS = 16          # tirages du premier jeton, par configuration
TEMPERATURE = 1.0
GRAINE = 20261002          # reproductibilité au sein d'un fournisseur
PLAFOND_APPELS = 400       # garde-fou absolu : au-delà, le banc s'arrête

# Trois questions de longueur comparable, dans la langue du corpus.
# Statut : v1 provisoire, à ratifier par un lecteur extérieur (voir README §4).
PROMPTS = (
    "En une phrase : qu'est-ce qui distingue retenir un flux de le figer ?",
    "En une phrase : quand une innovation cesse-t-elle d'être robuste ?",
    "En une phrase : qu'est-ce qui rend une idée transmissible ?",
)

# Marque de suspension. v1 = blancs : manipulation structurellement neutre,
# sans charge sémantique. Variante écartée : un mot (« silence », « pause »),
# qui introduirait du sens et confondrait contrainte et contenu.
MARQUE_SUSPENSION = "\n"


class PlafondDepasse(RuntimeError):
    """Le garde-fou de dépense a été atteint."""


def construire_message(prompt: str, n: int) -> str:
    """Insère N marques de suspension AVANT la question."""
    return (MARQUE_SUSPENSION * n) + prompt


def entropie_empirique(jetons: list[str]) -> float:
    """Entropie de Shannon (bits) de la distribution empirique des 1ers jetons."""
    if not jetons:
        return float("nan")
    total = len(jetons)
    compte = Counter(jetons)
    return -sum((c / total) * math.log2(c / total) for c in compte.values())


def _client():
    from huggingface_hub import InferenceClient
    return InferenceClient(model=MODELE)


def _appel(client, messages, **kw):
    """Appel unique, avec comptage de dépense par l'appelant."""
    return client.chat_completion(messages=messages, **kw)


def mesurer_configuration(client, prompt: str, n: int, compteur: dict) -> dict:
    """Une configuration = une question x une valeur de N.

    Renvoie l'entropie empirique du premier jeton (métrique principale),
    la surprise moyenne (confiance), et la liste des premiers jetons.
    """
    messages = [{"role": "user", "content": construire_message(prompt, n)}]
    debut = time.time()
    erreur = None

    try:
        compteur["appels"] += 1
        if compteur["appels"] > PLAFOND_APPELS:
            raise PlafondDepasse(
                f"plafond de {PLAFOND_APPELS} appels atteint — arrêt du banc"
            )
        r = _appel(
            client,
            messages,
            max_tokens=1,
            n=ECHANTILLONS,
            temperature=TEMPERATURE,
            seed=GRAINE,
            logprobs=True,
        )
        choix = list(r.choices)
        mode = f"n={ECHANTILLONS} en un appel"
    except PlafondDepasse:
        raise
    except Exception as exc:  # noqa: BLE001 — on veut le motif exact
        # Repli : le fournisseur refuse peut-être n > 1. On reboucle en appels
        # unitaires, ce qui multiplie le nombre d'appels par ECHANTILLONS.
        erreur = f"{type(exc).__name__}: {str(exc)[:200]}"
        choix = []
        try:
            for _ in range(ECHANTILLONS):
                compteur["appels"] += 1
                if compteur["appels"] > PLAFOND_APPELS:
                    raise PlafondDepasse(
                        f"plafond de {PLAFOND_APPELS} appels atteint — arrêt du banc"
                    )
                ru = _appel(
                    client,
                    messages,
                    max_tokens=1,
                    n=1,
                    temperature=TEMPERATURE,
                    seed=None,
                    logprobs=True,
                )
                choix.append(ru.choices[0])
            mode = "repli : 1 appel par tirage"
        except PlafondDepasse:
            raise
        except Exception as exc2:  # noqa: BLE001
            erreur = f"{type(exc2).__name__}: {str(exc2)[:200]}"

    jetons, surprises = [], []
    for c in choix:
        texte = c.message.content
        jetons.append(texte)
        lp = getattr(c, "logprobs", None)
        if lp is not None and getattr(lp, "content", None):
            surprises.append(-float(lp.content[0].logprob))

    return {
        "n_suspension": n,
        "prompt": prompt,
        "mode": mode if not erreur else "échec",
        "erreur": erreur,
        "entropie_premier_jeton": round(entropie_empirique(jetons), 4),
        "surprise_moyenne": round(sum(surprises) / len(surprises), 4)
        if surprises
        else None,
        "premiers_jetons": jetons,
        "duree_s": round(time.time() - debut, 2),
    }


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------


def mode_plan() -> int:
    configurations = len(N_VALEURS) * len(PROMPTS)
    jetons_par_appel = 20 + ECHANTILLONS  # question + tirages, ordre de grandeur
    appels_cas_nominal = configurations
    appels_cas_repli = configurations * ECHANTILLONS
    print("PLAN DU BANC DE SUSPENSION — phase 1 (exploration)")
    print("=" * 68)
    print(f"  instrument        : {MODELE}")
    print(f"  valeurs de N      : {N_VALEURS}")
    print(f"  questions         : {len(PROMPTS)}")
    print(f"  configurations    : {configurations}   (= {len(N_VALEURS)} x {len(PROMPTS)})")
    print(f"  échantillons N    : {ECHANTILLONS} tirages du 1er jeton")
    print(f"  plafond d'appels  : {PLAFOND_APPELS}")
    print()
    print(f"  cas nominal (n en un appel) : {appels_cas_nominal} appels "
          f"~ {appels_cas_nominal * jetons_par_appel} jetons")
    print(f"  cas de repli (1 appel/tirage) : {appels_cas_repli} appels "
          f"~ {appels_cas_repli * jetons_par_appel} jetons")
    print()
    print("  Coût : négligeable dans les deux cas (fraction de centime).")
    print("  Aucun appel n'a été effectué — mode --plan.")
    return 0


def mode_verifier() -> int:
    """Contrôle de manipulation : N agit-il réellement ?

    Deux configurations seulement (N = 0 et N = 16, première question).
    Si les tirages du premier jeton sont identiques, la variable est inerte
    et le balayage n'aurait aucun sens.
    """
    client = _client()
    compteur = {"appels": 0}
    question = PROMPTS[0]
    print("CONTRÔLE DE MANIPULATION — N agit-il ?")
    print("=" * 68)
    a = mesurer_configuration(client, question, 0, compteur)
    b = mesurer_configuration(client, question, max(N_VALEURS), compteur)
    for etiquette, r in (("N = 0", a), (f"N = {max(N_VALEURS)}", b)):
        print(f"  {etiquette:>7} | entropie {r['entropie_premier_jeton']:.3f} bits "
              f"| surprise {r['surprise_moyenne']} | {r['mode']}")
        print(f"          | jetons : {r['premiers_jetons']}")
    identiques = sorted(a["premiers_jetons"]) == sorted(b["premiers_jetons"])
    print()
    if identiques:
        print("  VERDICT : échantillons IDENTIQUES -> la variable N est INERTE")
        print("            Le balayage est à revoir avant toute mesure.")
    else:
        print("  VERDICT : les échantillons DIVERGENT -> N agit.")
        print("            Le balayage peut être lancé (--mesurer).")
    print(f"  appels consommés : {compteur['appels']}")
    return 0


def mode_mesurer() -> int:
    client = _client()
    compteur = {"appels": 0}
    resultats = []

    print("BALAYAGE — phase 1 (exploration, non probatoire)")
    print("=" * 68)
    print(f"{'N':>3} | {'entropie':>9} | {'surprise':>9} | {'s':>6} | question")
    print("-" * 68)
    try:
        for question in PROMPTS:
            for n in N_VALEURS:
                r = mesurer_configuration(client, question, n, compteur)
                resultats.append(r)
                court = question[:26] + "…" if len(question) > 27 else question
                print(f"{n:>3} | {r['entropie_premier_jeton']:>9.3f} | "
                      f"{str(r['surprise_moyenne']):>9} | {r['duree_s']:>6.1f} | {court}")
                if r["erreur"]:
                    print(f"     erreur : {r['erreur']}")
    except PlafondDepasse as exc:
        print(f"\n  ARRÊT : {exc}")
        print("  (garde-fou de dépense — les résultats obtenus sont conservés)")

    # Journal : un fichier par exécution, horodaté, à verser au dépôt.
    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    chemin = os.path.join(dossier, f"balayage_{horodatage}.jsonl")
    with open(chemin, "w", encoding="utf-8") as f:
        entete = {
            "modele": MODELE,
            "date_utc": horodatage,
            "n_valeurs": list(N_VALEURS),
            "echantillons": ECHANTILLONS,
            "temperature": TEMPERATURE,
            "graine": GRAINE,
            "marque_suspension": repr(MARQUE_SUSPENSION),
            "appels_consommes": compteur["appels"],
        }
        f.write(json.dumps({"entete": entete}, ensure_ascii=False) + "\n")
        for r in resultats:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\n  journal écrit : {os.path.relpath(chemin)}")
    print(f"  appels consommés : {compteur['appels']} / {PLAFOND_APPELS}")
    print("  Statut : exploration — AUCUNE conclusion probatoire ne peut en être tirée.")
    return 0


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    groupe = parseur.add_mutually_exclusive_group(required=True)
    groupe.add_argument("--plan", action="store_true")
    groupe.add_argument("--verifier", action="store_true")
    groupe.add_argument("--mesurer", action="store_true")
    args = parseur.parse_args()

    try:
        if args.plan:
            return mode_plan()
        if args.verifier:
            return mode_verifier()
        return mode_mesurer()
    except PlafondDepasse as exc:
        print(f"ARRÊT : {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
