#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validation unitaire — ratio π/η (porosité / viscosité) d'un output de LLM.

Mesure, sur un texte produit par un LLM, deux densités :

  - V1 (≈ π) : densité de contenu SUBSTANTIEL « brut » — code, chiffres,
               symboles, faits (le flux qui tend à saturer).
  - V2 (≈ η) : densité de STRUCTURATION — transitions, explications,
               contextualisation, connecteurs (le flux qui retient et rend
               lisible).

Le ratio V1/V2 est comparé à une fenêtre [BORNE_BASSE, BORNE_HAUTE] représentant
la zone de résonance κ. Sortie de fenêtre → signalement.

Ce script est un PREMIER CADRE MESURABLE, à calibrer par le collectif.
Il est déterministe (aucun appel réseau, aucune IA) pour être rejouable.

Tags: mttv-flp, rmp, pi, eta, v1-v2, validation
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import re
import sys

# Marqueurs heuristiques V1 (substance brute) et V2 (structuration).
V1_MARQUEURS = [
    r"\b\d+\b",                # nombres
    r"[{}()\[\];=<>+\-*/%]",   # symboles de code / math
    r"\b(def|class|return|import|function|lambda|if|else|for|while)\b",  # code
    r"\b\d{4}\b",              # années
]
V2_MARQUEURS = [
    r"\b(donc|ainsi|cependant|toutefois|en revanche|par conséquent|autrement dit|en résumé|par exemple|c'est-à-dire)\b",
    r"\b(parce que|puisque|car|afin que|pour que|si bien que)\b",
    r"\b(premièrement|deuxièmement|enfin|d'abord|ensuite|puis)\b",
]

# Zone de résonance κ par défaut (V1/V2). À calibrer.
BORNE_BASSE = 0.5   # en dessous : trop peu de substance (η≫π, creux)
BORNE_HAUTE = 2.5   # au-dessus : trop de substance brute (π≫η, saturation)


def compter_marqueurs(texte, motifs):
    total = 0
    for motif in motifs:
        total += len(re.findall(motif, texte, flags=re.IGNORECASE))
    return total


def densite(texte):
    """Retourne (densite_V1, densite_V2, ratio)."""
    nb_v1 = compter_marqueurs(texte, V1_MARQUEURS)
    nb_v2 = compter_marqueurs(texte, V2_MARQUEURS)
    # normalisation par 100 mots pour comparer des textes de tailles diverses
    mots = len(texte.split()) or 1
    d1 = nb_v1 / mots * 100
    d2 = nb_v2 / mots * 100
    ratio = (d1 / d2) if d2 > 0 else float("inf")
    return d1, d2, ratio


def valider(texte, basse=BORNE_BASSE, haute=BORNE_HAUTE):
    d1, d2, ratio = densite(texte)
    if ratio < basse:
        statut = "CREUX (eta>>pi : trop peu de substance)"
    elif ratio > haute:
        statut = "SATURATION (pi>>eta : trop de V1 brut, eta insuffisant)"
    else:
        statut = "ZONE kappa (equilibre pi/eta)"
    return {
        "densite_V1_pour_100_mots": round(d1, 2),
        "densite_V2_pour_100_mots": round(d2, 2),
        "ratio_V1_V2": round(ratio, 2) if ratio != float("inf") else "inf",
        "statut": statut,
    }


def main():
    # Exemples de test
    saturant = (
        "def f(x): return x*2 class A: pass 1 2 3 4 5 6 7 8 9 10 "
        "x=1 y=2 z=3 if else for while return 2024 2025"
    )
    structure = (
        "Ainsi, il convient d'abord de comprendre, puis de préciser. "
        "Par exemple, cette approche s'explique parce que le contexte compte, "
        "et c'est-à-dire que l'on reformule autrement dit pour clarifier."
    )
    equilibre = (
        "La fonction f(x)=x*2 double un entier. Par exemple, f(3) vaut 6. "
        "En revanche, il faut expliquer le pourquoi : car le lecteur doit suivre, "
        "autrement dit intégrer la logique sans se noyer dans les chiffres."
    )

    for nom, texte in [("SATURANT", saturant), ("STRUCTURE", structure), ("EQUILIBRE", equilibre)]:
        r = valider(texte)
        print(f"[{nom}] {r['statut']}  (V1={r['densite_V1_pour_100_mots']}, "
              f"V2={r['densite_V2_pour_100_mots']}, ratio={r['ratio_V1_V2']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
