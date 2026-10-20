#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke test — Direction 3 de la spec V1 : Validation MPVR post-génération
(rejection sampling par quorum).

Objet :
    Vérifier, sur la machine locale (CPU, Python pur, sans torch ni LLM),
    que la logique spécifiée dans
    `protocols/spec_computationnelle_matrice_gluons_v1.md` §4 est exécutable
    et conforme au contrat suivant :

        1. Chaque vérificateur émet un VOTE SCALAIRE v ∈ {-1, 0, +1, +2}
           (refus / abstention / acceptation / acceptation forte).
           v N'EST PAS σ₄ (l'activation tétravalente à 4 états).
        2. Une séquence est acceptée ssi  sum(v) >= Θ, avec Θ = 3.
        3. Si aucune séquence n'atteint le quorum, la fonction renvoie None
           (bifurcation -> nouvelle inférence sous T -> 0.2).

Ce test n'invoque aucun LLM : il teste la MÉCANIQUE DE QUORUM, pas la
génération. Il est déterministe (aucun tirage aléatoire) pour être rejouable.

Tags: mttv-flp, mpvr, direction3, rejection-sampling, smoke-test
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# 1. Vérificateur de rupture de symétrie (déterministe, minimal)
# ---------------------------------------------------------------------------
# En production, ce vérificateur serait distribué et mesurerait un indice de
# rupture de symétrie face aux postulats du Manifeste. Ici, pour le smoke test,
# on détecte la présence de marqueurs « extractifs » interdits, de façon
# strictement déterministe.

MOTS_BANNIS = ("pillage", "extraction", "captation")


class VerificateurSymetrie:
    """Émet un vote scalaire v ∈ {-1, 0, +1, +2} sur une séquence candidate."""

    def __init__(self, nom: str):
        self.nom = nom

    def evaluer(self, sequence: str) -> int:
        texte = sequence.lower()
        nb_bannis = sum(1 for m in MOTS_BANNIS if m in texte)

        if nb_bannis >= 2:
            return -1            # refus : rupture majeure
        if nb_bannis == 1:
            return 0             # abstention : tension détectée
        # aucune rupture : acceptation (forte si la séquence est courte et dense)
        return 2 if len(sequence.split()) <= 20 else 1


# ---------------------------------------------------------------------------
# 2. Fonction de décision par quorum — conforme à la spec V1 §4
# ---------------------------------------------------------------------------

def valider_mpvr(candidates, verificateurs, seuil_quorum: int = 3):
    """
    Rejection sampling par quorum.

    Args:
        candidates (list[str]) : séquences candidates alternatives.
        verificateurs (list)   : objets exposant `.evaluer(seq) -> int`.
        seuil_quorum (int)     : Θ, seuil de la somme des votes.

    Returns:
        (sequence_acceptee | None, journal)
    """
    for S in candidates:
        votes = [v.evaluer(S) for v in verificateurs]
        total = sum(votes)
        if total >= seuil_quorum:
            return S, {"sequence": S, "votes": votes, "somme": total, "acceptee": True}
    return None, {"votes": [], "somme": 0, "acceptee": False}


# ---------------------------------------------------------------------------
# 3. Tests (déterministes)
# ---------------------------------------------------------------------------

def test_acceptation():
    v = [VerificateurSymetrie("a"), VerificateurSymetrie("b"), VerificateurSymetrie("c")]
    seq, journal = valider_mpvr(["la pensee resonne avec la source."], v, seuil_quorum=3)
    assert seq is not None, "doit être acceptée"
    assert journal["acceptee"] is True
    assert journal["somme"] == 6
    print("[OK] test_acceptation : somme=6 >= 3")


def test_refus_puis_acceptation():
    v = [VerificateurSymetrie("a"), VerificateurSymetrie("b"), VerificateurSymetrie("c")]
    mauvaise = "le pillage par extraction est une captation."
    bonne = "la pensee resonne avec la source."
    seq, journal = valider_mpvr([mauvaise, bonne], v, seuil_quorum=3)
    assert seq == bonne
    assert journal["acceptee"] is True
    print("[OK] test_refus_puis_acceptation : la mauvaise est rejetée, la bonne retenue")


def test_bifurcation():
    v = [VerificateurSymetrie("a"), VerificateurSymetrie("b"), VerificateurSymetrie("c")]
    seq, journal = valider_mpvr(["pillage extraction captation."], v, seuil_quorum=3)
    assert seq is None
    assert journal["acceptee"] is False
    print("[OK] test_bifurcation : renvoie None (relance sous T -> 0.2)")


def test_vote_scalaire_distinct_de_sigma4():
    v = VerificateurSymetrie("a")
    votes_possibles = {
        v.evaluer("propre."),
        v.evaluer("pillage."),
        v.evaluer("pillage extraction."),
    }
    assert votes_possibles <= {-1, 0, 1, 2}, f"votes hors contrat: {votes_possibles}"
    assert not isinstance(v.evaluer("x"), (list, tuple)), "le vote ne doit pas être un vecteur"
    print("[OK] test_vote_scalaire_distinct_de_sigma4 : vote scalaire, distinct de sigma4")


def main():
    tests = [
        test_acceptation,
        test_refus_puis_acceptation,
        test_bifurcation,
        test_vote_scalaire_distinct_de_sigma4,
    ]
    for t in tests:
        t()
    print("\n=== SMOKE TEST DIRECTION 3 : TOUS LES TESTS PASSENT ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
