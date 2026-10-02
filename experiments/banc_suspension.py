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
    --plan      n'appelle rien ; affiche le plan, la calibration et le coût
    --verifier  contrôle que N agit réellement (8 appels)
    --mesurer   balayage complet (5 valeurs de N x 3 questions)

Version 3 — 2 octobre 2026. Corrections issues du premier contrôle (§10-11 du
README) :
  - plage étendue à (0, 4, 16, 64, 256) : 16 blancs ne font que 4 jetons ;
  - **jetons d'entrée du prompt relevés à chaque appel** : c'est la seule
    preuve que la suspension est réellement transmise au modèle, et non
    supprimée par le gabarit de conversation ;
  - verdict fondé sur la règle « écart > 2 x bruit », et non sur la
    comparaison tautologique de deux listes de tirages ;
  - le contrôle de manipulation écrit désormais son propre journal.

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

N_VALEURS = (0, 4, 16, 64, 256)
# Étendue le 2 octobre 2026 : la plage précédente (0 → 16 blancs) ne couvrait
# en réalité que 0 à 4 jetons — une variable presque inexistante.

ECHANTILLONS = 16          # jetons à recueillir par configuration (cible)
PAR_APPEL = 4              # PLAFOND MESURÉ du fournisseur, le 2 octobre 2026 :
#                            n = 16 -> HTTP 422 (refusé) ; n = 4 -> accepté.
APPELS_PAR_CONFIG = (ECHANTILLONS + PAR_APPEL - 1) // PAR_APPEL
TEMPERATURE = 1.0
PLAFOND_APPELS = 400       # garde-fou absolu : au-delà, le banc s'arrête
FACTEUR_BRUIT = 2.0        # règle de seuil : écart > 2 x bruit (voir feuillet)

# Aucun `seed` n'est transmis : la combinaison seed + n > 1 n'a pas été testée,
# et les fournisseurs ne garantissent pas l'effet du paramètre. La dispersion
# entre sous-appels fournit l'information que le seed devait apporter.

PROMPTS = (
    "En une phrase : qu'est-ce qui distingue retenir un flux de le figer ?",
    "En une phrase : quand une innovation cesse-t-elle d'être robuste ?",
    "En une phrase : qu'est-ce qui rend une idée transmissible ?",
)

# Marque de suspension. v1 = blancs : manipulation structurellement neutre.
# Variante écartée : un mot (« silence », « pause »), porteur de sens.
MARQUE_SUSPENSION = "\n"


class PlafondDepasse(RuntimeError):
    """Le garde-fou de dépense a été atteint."""


def construire_message(prompt: str, n: int) -> str:
    return (MARQUE_SUSPENSION * n) + prompt


def entropie_empirique(jetons: list[str]) -> float:
    """Entropie de Shannon (bits) de la distribution empirique des 1ers jetons."""
    if not jetons:
        return float("nan")
    total = len(jetons)
    compte = Counter(jetons)
    return -sum((c / total) * math.log2(c / total) for c in compte.values())


def ecart_type(valeurs: list[float]) -> float | None:
    if len(valeurs) < 2:
        return None
    moyenne = sum(valeurs) / len(valeurs)
    variance = sum((v - moyenne) ** 2 for v in valeurs) / (len(valeurs) - 1)
    return math.sqrt(variance)


def calibration() -> tuple[dict, str]:
    """Convertit les valeurs de N (blancs) en jetons réels.

    Première tentative : le tokenizer de l'instrument lui-même. Repli : facteur
    documenté (4 blancs ≈ 1 jeton, mesuré sur un tokenizer voisin le
    2 octobre 2026). La source est consignée — une approximation déclarée
    vaut mieux qu'un chiffre non sourcé.
    """
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODELE)
        table = {n: len(tokenizer(MARQUE_SUSPENSION * n)["input_ids"]) for n in N_VALEURS}
        return table, "tokenizer de l'instrument"
    except Exception as exc:  # noqa: BLE001
        table = {n: max(0, round(n / 4)) for n in N_VALEURS}
        return table, f"approximation 4 blancs ≈ 1 jeton (tokenizer inaccessible : {type(exc).__name__})"


def _client():
    from huggingface_hub import InferenceClient
    return InferenceClient(model=MODELE)


def _tirer(client, messages, compteur):
    """Un sous-appel de PAR_APPEL tirages.

    Renvoie (choix, motif_erreur, jetons_entree). `jetons_entree` est le nombre
    de jetons de prompt déclaré par le fournisseur : c'est la preuve que la
    suspension a bien été transmise.
    """
    compteur["appels"] += 1
    if compteur["appels"] > PLAFOND_APPELS:
        raise PlafondDepasse(
            f"plafond de {PLAFOND_APPELS} appels atteint — arrêt du banc"
        )
    try:
        r = client.chat_completion(
            messages=messages, max_tokens=1, n=PAR_APPEL,
            temperature=TEMPERATURE, logprobs=True,
        )
        entree = None
        usage = getattr(r, "usage", None)
        if usage is not None:
            entree = getattr(usage, "prompt_tokens", None)
        return list(r.choices), None, entree
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
            ru = client.chat_completion(
                messages=messages, max_tokens=1, n=1,
                temperature=TEMPERATURE, logprobs=True,
            )
        except Exception as exc2:  # noqa: BLE001
            return choix, f"{motif} | repli : {type(exc2).__name__}: {str(exc2)[:160]}", None
        choix.append(ru.choices[0])
    return choix, f"{motif} | repli réussi ({len(choix)} tirages unitaires)", None


def mesurer_configuration(client, prompt: str, n: int, compteur: dict) -> dict:
    """Une configuration = une question x une valeur de N."""
    messages = [{"role": "user", "content": construire_message(prompt, n)}]
    debut = time.time()
    jetons, surprises, entropies, motifs, entrees = [], [], [], [], []

    for _ in range(APPELS_PAR_CONFIG):
        try:
            choix, motif, entree = _tirer(client, messages, compteur)
        except PlafondDepasse:
            raise
        if motif:
            motifs.append(motif)
        if entree is not None:
            entrees.append(entree)
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
        "jetons_entree_prompt": sorted(set(entrees)) if entrees else None,
        "entropie_premier_jeton": round(entropie_empirique(jetons), 4),
        "dispersion_entropie_appels": round(dispersion, 4) if dispersion is not None else None,
        "surprise_moyenne": (
            round(sum(surprises) / len(surprises), 4) if surprises else None
        ),
        "premiers_jetons": jetons,
        "motifs_erreur": motifs,
        "duree_s": round(time.time() - debut, 2),
    }


def _journaliser(prefixe: str, entete: dict, resultats: list[dict]) -> str:
    dossier = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
    os.makedirs(dossier, exist_ok=True)
    horodatage = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    chemin = os.path.join(dossier, f"{prefixe}_{horodatage}.jsonl")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(json.dumps({"entete": {**entete, "date_utc": horodatage}},
                           ensure_ascii=False) + "\n")
        for r in resultats:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return os.path.relpath(chemin)


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------


def mode_plan() -> int:
    table, source = calibration()
    configurations = len(N_VALEURS) * len(PROMPTS)
    nominal = configurations * APPELS_PAR_CONFIG
    print("PLAN DU BANC DE SUSPENSION — phase 1 (exploration)")
    print("=" * 68)
    print(f"  instrument        : {MODELE}")
    print(f"  configurations    : {configurations}  (= {len(N_VALEURS)} x {len(PROMPTS)})")
    print(f"  tirages par config: {ECHANTILLONS}  ({APPELS_PAR_CONFIG} sous-appels de {PAR_APPEL})")
    print(f"  plafond d'appels  : {PLAFOND_APPELS}")
    print()
    print("  CALIBRATION blancs -> jetons")
    print(f"    source : {source}")
    for n in N_VALEURS:
        print(f"    N = {n:>4} blancs  ->  {table[n]:>3} jetons de suspension")
    print()
    print(f"  cas nominal : {nominal} appels  |  repli (unitaires) : {nominal * PAR_APPEL} appels")
    print("  Coût : négligeable (fraction de centime). Aucun appel effectué.")
    return 0


def mode_verifier() -> int:
    """Contrôle de manipulation : N agit-il réellement ?

    Verdict fondé sur la règle de seuil du feuillet : un écart ne compte que
    s'il dépasse FACTEUR_BRUIT fois le bruit de l'estimateur. La comparaison
    brute de deux listes de tirages est tautologique et ne sert plus de verdict.
    """
    client = _client()
    compteur = {"appels": 0}
    question = PROMPTS[0]
    table, source = calibration()

    print("CONTRÔLE DE MANIPULATION — N agit-il ?")
    print("=" * 68)
    a = mesurer_configuration(client, question, 0, compteur)
    b = mesurer_configuration(client, question, max(N_VALEURS), compteur)

    for etiquette, r in ((f"N = 0 ({table[0]} jeton)", a),
                         (f"N = {max(N_VALEURS)} ({table[max(N_VALEURS)]} jetons)", b)):
        print(f"  {etiquette:>18} | entropie {r['entropie_premier_jeton']:.3f} bits "
              f"| {r['jetons_recueillis']} jetons tirés "
              f"| bruit {r['dispersion_entropie_appels']}")
        print(f"  {'':>18} | jetons d'entrée du prompt : {r['jetons_entree_prompt']}")
        print(f"  {'':>18} | premiers jetons : {r['premiers_jetons']}")
        for motif in r["motifs_erreur"]:
            print(f"  {'':>18} | ERREUR : {motif}")
    print()

    entete = {
        "modele": MODELE,
        "mode": "controle de manipulation",
        "calibration": {str(k): v for k, v in table.items()},
        "source_calibration": source,
        "facteur_bruit": FACTEUR_BRUIT,
        "appels_consumes": compteur["appels"],
    }

    fautives = [e for e, r in (("N = 0", a), ("N = max", b))
                if r["motifs_erreur"] or r["jetons_recueillis"] == 0]
    if fautives:
        print(f"  VERDICT : AUCUN — configuration(s) fautive(s) : {', '.join(fautives)}.")
        print("            Un verdict ne se rend pas sur des appels en erreur.")
        _journaliser("controle", entete, [a, b])
        return 3

    maigres = [r for r in (a, b) if r["jetons_recueillis"] < ECHANTILLONS // 2]
    if maigres:
        print(f"  VERDICT : AUCUN — moins de {ECHANTILLONS // 2} jetons recueillis.")
        _journaliser("controle", entete, [a, b])
        return 3

    # La suspension est-elle parvenue au modèle ? Comparer le nombre de jetons
    # d'entrée du prompt : s'il ne croît pas avec N, le gabarit de conversation
    # supprime les blancs et la manipulation est vide.
    entree_a = (a["jetons_entree_prompt"] or [None])[0]
    entree_b = (b["jetons_entree_prompt"] or [None])[0]
    if entree_a is not None and entree_b is not None:
        if entree_b <= entree_a:
            print(f"  ALERTE : jetons d'entrée N = 0 -> {entree_a}, "
                  f"N = max -> {entree_b} : la suspension NE PARVIENT PAS au modèle.")
            print("           Le gabarit de conversation supprime probablement les blancs.")
            print("           VERDICT : AUCUN — manipulation vide par construction.")
            _journaliser("controle", entete, [a, b])
            return 3
        print(f"  Suspension parvenue au modèle : {entree_a} -> {entree_b} jetons d'entrée "
              f"(+{entree_b - entree_a}).")

    ecart = abs(a["entropie_premier_jeton"] - b["entropie_premier_jeton"])
    bruits = [d for d in (a["dispersion_entropie_appels"], b["dispersion_entropie_appels"])
              if d is not None]
    bruit = max(bruits) if bruits else 0.0
    seuil = FACTEUR_BRUIT * bruit
    print(f"  écart d'entropie : {ecart:.3f} bit  |  bruit : {bruit:.3f}  "
          f"|  seuil ({FACTEUR_BRUIT:g} x bruit) : {seuil:.3f}")
    print()

    if ecart > seuil:
        print(f"  VERDICT : l'écart ({ecart:.3f}) DÉPASSE le seuil ({seuil:.3f}).")
        print("            -> N AGIT. Le balayage peut être lancé (--mesurer).")
        code = 0
    else:
        print(f"  VERDICT : INDÉTERMINÉ — l'écart ({ecart:.3f}) ne dépasse pas "
              f"le seuil ({seuil:.3f}).")
        print("            Ni « agit », ni « inerte » : l'appareil est trop bruité")
        print("            pour trancher. Ne pas lancer le balayage en l'état.")
        code = 3

    chemin = _journaliser("controle", entete, [a, b])
    print(f"\n  journal écrit : {chemin}")
    print(f"  appels consommés : {compteur['appels']}")
    return code


def mode_mesurer() -> int:
    client = _client()
    compteur = {"appels": 0}
    resultats = []
    table, source = calibration()

    print("BALAYAGE — phase 1 (exploration, non probatoire)")
    print("=" * 68)
    print(f"{'N':>4} | {'jetons susp.':>12} | {'entropie':>9} | {'bruit':>7} | {'prompt':>6}")
    print("-" * 68)
    try:
        for question in PROMPTS:
            for n in N_VALEURS:
                r = mesurer_configuration(client, question, n, compteur)
                resultats.append(r)
                entrees = r["jetons_entree_prompt"]
                print(f"{n:>4} | {table[n]:>12} | {r['entropie_premier_jeton']:>9.3f} | "
                      f"{str(r['dispersion_entropie_appels']):>7} | "
                      f"{str(entrees[0] if entrees else None):>6}")
                for motif in r["motifs_erreur"]:
                    print(f"       erreur : {motif}")
    except PlafondDepasse as exc:
        print(f"\n  ARRÊT : {exc}")
        print("  (garde-fou de dépense — les résultats obtenus sont conservés)")

    entete = {
        "modele": MODELE,
        "mode": "balayage",
        "n_valeurs": list(N_VALEURS),
        "calibration": {str(k): v for k, v in table.items()},
        "source_calibration": source,
        "echantillons_par_config": ECHANTILLONS,
        "sous_appels_par_config": APPELS_PAR_CONFIG,
        "tirages_par_sous_appel": PAR_APPEL,
        "temperature": TEMPERATURE,
        "graine": "non transmise (voir README §9)",
        "marque_suspension": repr(MARQUE_SUSPENSION),
        "appels_consumes": compteur["appels"],
        "statut": "exploration — aucune conclusion probatoire",
    }
    chemin = _journaliser("balayage", entete, resultats)
    print(f"\n  journal écrit : {chemin}")
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
