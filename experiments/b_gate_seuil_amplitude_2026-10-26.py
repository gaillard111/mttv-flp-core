"""
MTTV-FLP — B-Gate : où est le seuil d'amplitude, et module-t-il la durée ?

Module : b_gate_seuil_amplitude_2026-10-26
Objet  : le test du 26/10 ne donnait que trois points (0,85 se ferme ; 0,60 et 0,35
         jamais). Trois points ne localisent pas un seuil, et ne disent rien de la
         durée au-dessus de lui. Ce script fait les deux, en bras déconfondu — les
         poids normalisés sont écrits directement après construction, sans passer
         par la renormalisation du constructeur (cf. protocole § 1).

Résultats attendus (graine 42, scénario A, redondance 0,10 · coût 0,05) :
    - seuil de fermeture        w_m* = (0,45 − 0,0475) / 0,5877 = 0,6849
    - durée de la cicatrice     11 · 12 · 13 · 14 cycles pour w_m = 0,70 · 0,75 · 0,80 · 0,85

Exécution :  python experiments/b_gate_seuil_amplitude_2026-10-26.py
Dépendances : aucune. Aucune requête réseau.
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
"""

import importlib.util
import os
import random
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("epreuve", os.path.join(ICI, "b_gate_mttv_flp_epreuve.py"))
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

SIGNAL = [0.8, 0.9, 0.7, 0.95, 0.85]
PRESSION = [("PRESSION", p, 0.35, 0.25) for p in [0.55, 0.70, 0.85] + [0.95] * 7]


def porte(poids):
    """Objet en bras déconfondu : seule l'amplitude de la mémoire varie."""
    g = MOD.AdvancedBGate(memoire_decay=0.90)
    g.poids_memoire = poids
    g.poids_redondance = 0.10
    g.poids_cout = 0.05
    return g


def fermeture(poids):
    """Pas de fermeture (ou None)."""
    g = porte(poids)
    random.seed(42)
    for i, (_, p, r, c) in enumerate(PRESSION, 1):
        _, _, regime = g.forward(SIGNAL, pression=p, redondance=r, cout_transduction=c)
        if regime == "ACTIVE_SILENCE":
            return i
    return None


def duree(poids, relax_max=18):
    """(fermeture, réouverture, cicatrice) en cycles."""
    g = porte(poids)
    random.seed(42)
    ferm = None
    for i, (_, p, r, c) in enumerate(PRESSION, 1):
        _, _, regime = g.forward(SIGNAL, pression=p, redondance=r, cout_transduction=c)
        if regime == "ACTIVE_SILENCE" and ferm is None:
            ferm = i
    if ferm is None:
        return None, None, None
    for k in range(1, relax_max + 1):
        _, _, regime = g.forward(SIGNAL, pression=0.0, redondance=0.05, cout_transduction=0.05)
        if regime == "TRANSDUCTION":
            reouv = len(PRESSION) + k
            return ferm, reouv, reouv - ferm
    return ferm, None, None


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    # mémoire maximale atteinte dans le scénario A — indépendante des poids
    g = MOD.AdvancedBGate(memoire_decay=0.90)
    random.seed(42)
    max_m = 0.0
    for _, p, r, c in PRESSION:
        g.forward(SIGNAL, pression=p, redondance=r, cout_transduction=c)
        max_m = max(max_m, g.state.memoire_pression)

    print("Seuil de fermeture, bras déconfondu (redondance 0,10 · coût 0,05)")
    print(f"mémoire maximale atteinte dans le scénario A : {max_m:.4f}\n")
    print(f"{'poids_memoire':>14} | {'score max':>9} | fermeture")
    print("-" * 44)
    for poids in (0.40, 0.50, 0.55, 0.60, 0.62, 0.65, 0.70, 0.75, 0.80, 0.85):
        score_max = poids * max_m + 0.10 * 0.35 + 0.05 * 0.25
        print(f"{poids:>14.2f} | {score_max:>9.4f} | pas {fermeture(poids)}")

    seuil = (0.45 - 0.10 * 0.35 - 0.05 * 0.25) / max_m
    print(f"\nseuil analytique : (0,45 − 0,0475) / {max_m:.4f} = {seuil:.4f}")
    a, b = 0.40, 0.90
    for _ in range(40):
        m = (a + b) / 2
        if fermeture(m) is None:
            a = m
        else:
            b = m
    print(f"bissection numérique : {b:.4f}  (accord : {abs(b - seuil) < 1e-6})")

    print("\nDurée de la cicatrice au-dessus du seuil")
    print(f"{'poids_memoire':>14} | {'fermeture':>9} | {'réouverture':>11} | {'cicatrice':>9}")
    print("-" * 52)
    for poids in (0.70, 0.75, 0.80, 0.85):
        f, r, d = duree(poids)
        print(f"{poids:>14.2f} | {f!s:>9} | {r!s:>11} | {d!s:>9}")

    print("\nLecture : la réouverture exige m < (0,15 − 0,0475)/w_m = 0,1025/w_m.")
    print("Plus l'amplitude est forte, plus ce seuil est bas, plus la cicatrice est longue.")
    print("L'amplitude gouverne donc l'existence ET module la durée ; la décroissance")
    print("en reste le facteur dominant, pas le seul.")
