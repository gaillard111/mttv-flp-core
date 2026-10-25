"""
MTTV-FLP — B-Gate : balayage d'un paramètre à la fois

Module : b_gate_balayage_parametres
Objet  : répondre à la seule question que le protocole d'épreuve laisse ouverte
         dans le scénario B — « à partir de combien de cycles la membrane se
         rouvre-t-elle ? » — et mesurer la sensibilité de cette durée à UN
         paramètre modifié à la fois (tous les autres restant aux défauts).

Scénario utilisé : B (10 cycles de pression puis relâchement à p = 0, 40 cycles
de marge). On rapporte :
    - le pas de fermeture (ou None),
    - le pas de réouverture (ou None),
    - le nombre de cycles de relâchement nécessaires (ou None).

Exécution :  python experiments/b_gate_balayage_parametres.py
Dépendances : aucune.

Provenance : écrit pour le protocole d'épreuve du 2026-10-25. Le module épreuvé
             n'est pas modifié — il est chargé par chemin.
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
"""

import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "epreuve", os.path.join(ICI, "b_gate_mttv_flp_epreuve.py")
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

SIGNAL = [0.8, 0.9, 0.7, 0.95, 0.85]
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
RELAX_MAX = 40


def mesurer(**surcharges):
    """Rejoue le scénario B et renvoie (pas_fermeture, pas_reouverture, cycles_relax)."""
    gate = MOD.AdvancedBGate(**surcharges)

    fermeture = None
    for i, p in enumerate(PRESSION, 1):
        _, _, regime = gate.forward(SIGNAL, pression=p, redondance=0.35, cout_transduction=0.25)
        if regime == "ACTIVE_SILENCE" and fermeture is None:
            fermeture = i

    if fermeture is None:
        return None, None, None

    base = len(PRESSION)
    for k in range(1, RELAX_MAX + 1):
        _, _, regime = gate.forward(SIGNAL, pression=0.0, redondance=0.05, cout_transduction=0.05)
        if regime == "TRANSDUCTION":
            return fermeture, base + k, k

    return fermeture, None, None


def ligne(libelle, **surcharges):
    fermeture, ouverture, cycles = mesurer(**surcharges)
    ouverture = "—" if ouverture is None else f"pas {ouverture}"
    cycles = "jamais" if cycles is None else str(cycles)
    print(f"{libelle:<34} fermeture={fermeture!s:<6} réouverture={ouverture:<9} cicatrice={cycles}")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    print("Scénario B — pression soutenue puis relâchement à p = 0")
    print("Un seul paramètre varie par bloc, les autres restent aux défauts.\n")

    print("Défauts")
    ligne("  (aucune surcharge)")

    print("\nmemoire_decay")
    for d in [0.95, 0.92, 0.90, 0.88, 0.85, 0.80]:
        ligne(f"  memoire_decay = {d:.2f}", memoire_decay=d)

    print("\nseuil_ouverture")
    for s in [0.05, 0.10, 0.15, 0.20, 0.25]:
        ligne(f"  seuil_ouverture = {s:.2f}", seuil_ouverture=s)

    print("\nseuil_fermeture")
    for s in [0.30, 0.40, 0.45, 0.50, 0.60]:
        ligne(f"  seuil_fermeture = {s:.2f}", seuil_fermeture=s)

    print("\nporosite_reouverture_max")
    for s in [0.05, 0.20, 0.50]:
        ligne(f"  porosite_reouverture_max = {s:.2f}", porosite_reouverture_max=s)
