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
    --verifier  contrôle que N agit réellement (8 appels)
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

ECHANTILLONS = 16          # jetons à recueillir par configuration (cible)
PAR_APPEL = 4              # PLAFOND MESURÉ du fournisseur, le 2 octobre 2026 :
#                            n = 16 -> HTTP 422 (refusé) ; n = 4 -> accepté.
APPELS_PAR_CONFIG = (ECHANTILLONS + PAR_APPEL - 1) // PAR_APPEL
TEMPERATURE = 1.0
PLAFOND_APPELS = 400       # garde-fou absolu : au-delà, le banc s'arrête

# Aucun `seed` n'est transmis. Motif : la combinaison seed + n > 1 n'a pas été
# testée, les fournisseurs ne garantissent pas l'effet du paramètre, et la
# reproductibilité réellement obtenue est celle du DISPOSITIF (modèle,
# paramètres, journal) — pas celle des tirages. La dispersion entre sous-appels
# fournit en revanche une estimation du bruit de l'estimateur.

# Trois questions de longueur comparable, dans la langue du corpus.
# Statut : v1 provisoire, à ratifier par un lecteur extérieur (voir README §5).
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


def ecart_type(valeurs: list[float]) -> float | None:
    """Écart-type d'échantillon ; None si moins de deux valeurs."""
    if len(valeurs) < 2:
        return None
    moyenne = sum(valeurs) / len(valeurs)
    variance = sum((v - moyenne) ** 2 for v in valeurs) / (len(valeurs) - 1)
    return math.sqrt(variance)


def _client():
    from huggingface_hub import InferenceClient
    return InferenceClient(model=MODELE)


def _appel(client, messages, **kw):
    return client.chat_completion(messages=messages, **kw)


def _tirer(client, messages, compteur):
    """Un sous-appel de PAR_APPEL tirages, avec repli en appels unitaires."""
    compteur["appels"] += 1
    if compteur["appels"] > PLAFOND_APPELS:
        raise PlafondDepasse(
            f"plafond de {PLAFOND_APPELS} appels atteint — arrêt du banc"
        )
    try:
        r = _appel(
            client, messages, max_tokens=1, n=PAR_APPEL,
            temperature=TEMPERATURE, logprobs=True,
        )
        return list(r.choices), None
    except Exception as exc:  # noqa: BLE001 — on veut le motif exact
        motif = f"{type(exc).__name__}: {str(exc)[:160]}"

    # Repli : le fournisseur refuse peut-être n > 1 -> appels unitaires.
    choix = []
    for _ in range(PAR_APPEL):
        compteur["appels"] += 1
        if compteur["appels"] > PLAFOND_APPELS:
            raise PlafondDepasse(
                f"plafond de {PLAFOND_APPELS} appels atteint — arrêt du banc"
            )
        try:
            ru = _appel(
                client, messages, max_tokens=1, n=1,
                temperature=TEMPERATURE, logprobs=True,
            )
        except Exception as exc2:  # noqa: BLE001
            return choix, f"{motif} | repli : {type(exc2).__name__}: {str(exc2)[:160]}"
        choix.append(ru.choices[0])
    return choix, f"{motif} | repli réussi ({len(choix)} tirages unitaires)"


def mesurer_configuration(client, prompt: str, n: int, compteur: dict) -> dict:
    """Une configuration = une question x une valeur de N.

    Recueille ECHANTILLONS premiers jetons en APPELS_PAR_CONFIG sous-appels,
    puis renvoie : entropie empirique du premier jeton (métrique principale),
    dispersion de cette entropie entre sous-appels (bruit de l'estimateur),
    surprise moyenne (confiance), jetons bruts, motifs d'erreur.
    """
    messages = [{"role": "user", "content": construire_message(prompt, n)}]
    debut = time.time()
    jetons, surprises, entropies, motifs = [], [], [], []

    for _ in range(APPELS_PAR_CONFIG):
        try:
            choix, motif = _tirer(client, messages, compteur)
        except PlafondDepasse:
            raise
        if motif:
            motifs.append(motif)
        sous_jetons = [c.message.content for c in choix]
        if sous_jetons:
            jetons.extend(sous_jetons)
            entropies.append(entropie_empirique(sous_jetons))
        for c in choix:
            lp = getattr(c, "logprobs", None)
            if lp is not None and getattr(lp, "content", None):
                surprises.append(-float(lp.content[0].logprob))

    dispersion = ecart_type(entropies)
    return {
        "n_suspension": n,
        "prompt": prompt,
        "jetons_recueillis": len(jetons),
        "entropie_premier_jeton": round(entropie_empirique(jetons), 4),
        "dispersion_entropie_appels": round(dispersion, 4) if dispersion is not None else None,
        "surprise_moyenne": (
            round(sum(surprises) / len(surprises), 4) if surprises else None
        ),
        "premiers_jetons": jetons,
        "motifs_erreur": motifs,
        "duree_s": round(time.time() - debut, 2),
    }


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------


def mode_plan() -> int:
    configurations = len(N_VALEURS) * len(PROMPTS)
    jetons_par_appel = ECHANTILLONS + 20  # tirages + question, ordre de grandeur
    nominal = configurations * APPELS_PAR_CONFIG
    repli = nominal * PAR_APPEL
    print("PLAN DU BANC DE SUSPENSION — phase 1 (exploration)")
    print("=" * 68)
    print(f"  instrument          : {MODELE}")
    print(f"  valeurs de N        : {N_VALEURS}")
    print(f"  questions           : {len(PROMPTS)}")
    print(f"  configurations      : {configurations}  (= {len(N_VALEURS)} x {len(PROMPTS)})")
    print(f"  tirages par config  : {ECHANTILLONS}  ({APPELS_PAR_CONFIG} sous-appels")
    print(f"                        de {PAR_APPEL} — plafond mesuré du fournisseur)")
    print(f"  plafond d'appels    : {PLAFOND_APPELS}")
    print()
    print(f"  cas nominal : {nominal} appels  ~ {nominal * jetons_par_appel} jetons")
    print(f"  cas de repli (appels unitaires) : {repli} appels "
          f"~ {repli * jetons_par_appel} jetons")
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
              f"| {r['jetons_recueillis']} jetons "
              f"| dispersion {r['dispersion_entropie_appels']}")
        print(f"          | jetons : {r['premiers_jetons']}")
        for motif in r["motifs_erreur"]:
            print(f"          | ERREUR : {motif}")
    print()

    # Un verdict ne se rend JAMAIS sur des appels en erreur : sinon un appel
    # raté (liste vide) serait lu comme « les échantillons divergent », donc
    # comme la preuve que la variable agit. C'est exactement le faux positif
    # produit par la première exécution, le 2 octobre 2026.
    fautives = [e for e, r in (("N = 0", a), (f"N = {max(N_VALEURS)}", b))
                if r["motifs_erreur"] or r["jetons_recueillis"] == 0]
    if fautives:
        print(f"  VERDICT : AUCUN — configuration(s) fautive(s) : {', '.join(fautives)}.")
        print("            Un verdict ne se rend pas sur des appels en erreur.")
        print("            Corriger l'appel, puis relancer --verifier.")
        print(f"  appels consommés : {compteur['appels']}")
        return 3

    maigres = [r for r in (a, b) if r["jetons_recueillis"] < ECHANTILLONS // 2]
    if maigres:
        print(f"  VERDICT : AUCUN — moins de {ECHANTILLONS // 2} jetons recueillis "
              "dans une configuration au moins.")
        print("            Échantillon trop maigre pour comparer quoi que ce soit.")
        print(f"  appels consommés : {compteur['appels']}")
        return 3

    identiques = sorted(a["premiers_jetons"]) == sorted(b["premiers_jetons"])
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
    print(f"{'N':>3} | {'entropie':>9} | {'dispersion':>10} | {'surprise':>9} | question")
    print("-" * 68)
    try:
        for question in PROMPTS:
            for n in N_VALEURS:
                r = mesurer_configuration(client, question, n, compteur)
                resultats.append(r)
                court = question[:22] + "…" if len(question) > 23 else question
                print(f"{n:>3} | {r['entropie_premier_jeton']:>9.3f} | "
                      f"{str(r['dispersion_entropie_appels']):>10} | "
                      f"{str(r['surprise_moyenne']):>9} | {court}")
                for motif in r["motifs_erreur"]:
                    print(f"     erreur : {motif}")
    except PlafondDepasse as exc:
        print(f"\n  ARRÊT : {exc}")
        print("  (garde-fou de dépense — les résultats obtenus sont conservés)")

    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    chemin = os.path.join(dossier, f"balayage_{horodatage}.jsonl")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(json.dumps({"entete": {
            "modele": MODELE,
            "date_utc": horodatage,
            "n_valeurs": list(N_VALEURS),
            "echantillons_par_config": ECHANTILLONS,
            "sous_appels_par_config": APPELS_PAR_CONFIG,
            "tirages_par_sous_appel": PAR_APPEL,
            "temperature": TEMPERATURE,
            "graine": "non transmise (voir README §9)",
            "marque_suspension": repr(MARQUE_SUSPENSION),
            "appels_consumes": compteur["appels"],
            "statut": "exploration — aucune conclusion probatoire",
        }}, ensure_ascii=False) + "\n")
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
