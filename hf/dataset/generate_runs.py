#!/usr/bin/env python3
"""
Génération du dataset « MTTV-FLP MPVR Quorum Coupling Runs ».

Balaye la loi de couplage transcalaire rho -> tolérance -> seuil minimal viable
sur un ensemble déterministe de paramètres. Chaque ligne décrit une transduction
complète : B-gate (contractuelle) -> handshake mycélien -> quorum glocal.

Reproductibilité : graine fixée (SEED), aucun accès réseau.

Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
"""

import csv
import json
import os
import random
import sys

SEED = 20260101

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_CANON = os.path.normpath(os.path.join(ICI, "..", "..", "mpvr-glocal", "src"))
sys.path.insert(0, DOSSIER_CANON)

from mttv_mpvr_quorum import MicroQuorumPoreux  # noqa: E402
from mttv_mycelial_handshake import MycelialHandshake  # noqa: E402


# Grille de balayage
EXTRACTIONS = [0.05, 0.15, 0.25, 0.35, 0.50, 0.70]
POROSITES_SIGMA = [0.10, 0.20, 0.35, 0.50]
NOEUDS = [3, 5, 7, 9]
SEUIL_BGATE = 0.25  # seuil de l'opérateur Sigma par défaut


def construire_rapport_bgate(extraction, porosite_sigma, valeur_bios):
    """
    Rapport d'état de B-gate au format du contrat consommé par le handshake.

    La porosité Σ est fournie explicitement (paramètre du balayage) car
    l'implémentation courante de `BGateTransduction` ramène Σ à 0 après
    normalisation — limitation documentée.
    """
    active = extraction > SEUIL_BGATE
    if active:
        status = (
            "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. "
            "Flux prédateur neutralisé."
        )
    else:
        status = "FLUX TRANSDUCTIF STABLE : Alignement sur le vivant validé."

    return {
        "status": status,
        "etats_sp3": {"Bios (B)": valeur_bios},
        "porosite_Sigma": porosite_sigma,
    }


def generer_lignes():
    rng = random.Random(SEED)
    lignes = []
    run_id = 0

    for noeuds in NOEUDS:
        for extraction in EXTRACTIONS:
            for porosite_sigma in POROSITES_SIGMA:
                run_id += 1
                valeur_bios = round(rng.uniform(0.2, 0.6), 4)

                rapport_bgate = construire_rapport_bgate(
                    extraction, porosite_sigma, valeur_bios
                )
                active = "B-GATE ACTIVÉE" in rapport_bgate["status"]

                handshake = MycelialHandshake(
                    noeuds_quorum=noeuds, porosite_initiale=porosite_sigma
                )
                rapport_mycelien = handshake.propager_transduction(rapport_bgate)

                quorum = MicroQuorumPoreux(total_noeuds=noeuds, tolerance_panne=0.5)
                couplage = quorum.moduler_par_porosite(
                    rapport_mycelien["porosite_residuelle"]
                )
                diagnostic = quorum.evaluer_contexte({"input_flux": "basse_continue"})

                lignes.append(
                    {
                        "run_id": run_id,
                        "noeuds_quorum": noeuds,
                        "extraction": extraction,
                        "bgate_activation": active,
                        "porosite_sigma": porosite_sigma,
                        "bios": valeur_bios,
                        "metrique_quorum": rapport_mycelien["metrique_quorum"],
                        "porosite_residuelle": rapport_mycelien["porosite_residuelle"],
                        "tolerance_effective": couplage["tolerance_effective"],
                        "seuil_minimal_viable": couplage[
                            "seuil_minimal_viable_effectif"
                        ],
                        "statut_quorum": diagnostic["statut_quorum"],
                        "noeuds_sollicites": diagnostic["noeuds_sollicites"],
                        "economie_energie_pct": diagnostic["economie_energie_calcul"],
                    }
                )
    return lignes


def ecrire_sorties(lignes):
    dossier_data = os.path.join(ICI, "data")
    os.makedirs(dossier_data, exist_ok=True)

    chemin_csv = os.path.join(dossier_data, "mttv_mpvr_runs.csv")
    chemin_jsonl = os.path.join(dossier_data, "mttv_mpvr_runs.jsonl")

    with open(chemin_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        writer.writeheader()
        writer.writerows(lignes)

    with open(chemin_jsonl, "w", encoding="utf-8") as f:
        for ligne in lignes:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")

    return chemin_csv, chemin_jsonl


if __name__ == "__main__":
    lignes = generer_lignes()
    csv_path, jsonl_path = ecrire_sorties(lignes)
    print(f"{len(lignes)} lignes écrites.")
    print(f"CSV   : {csv_path}")
    print(f"JSONL : {jsonl_path}")
