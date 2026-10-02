#!/usr/bin/env python3
"""
Tests de la loi de couplage transcalaire MTTV-FLP / MPVR.

Couvre :
  - l'importabilité du handshake mycélien par l'implémentation de référence ;
  - la rétrocompatibilité du quorum (porosité neutre => seuil historique) ;
  - la monotonie de la loi de couplage rho -> tolérance -> seuil minimal viable ;
  - le bornage (clamp) de la porosité résiduelle ;
  - l'intégration bout-en-bout via `evaluer_avec_handshake_mycelien()`.

Licence : CC0 — Domaine public.
"""

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_SRC = os.path.join(RACINE, "src")
DOSSIER_CANON = os.path.join(RACINE, "mpvr-glocal", "src")

# Priorité au module canonique (mpvr-glocal/src), puis la variante interne.
sys.path.insert(0, DOSSIER_SRC)
sys.path.insert(0, DOSSIER_CANON)

from mttv_mpvr_quorum import MicroQuorumPoreux  # noqa: E402
from mttv_mycelial_handshake import MycelialHandshake  # noqa: E402


def test_import_handshake_par_le_quorum():
    assert MicroQuorumPoreux is not None
    assert MycelialHandshake is not None


def test_retrocompatibilite_porosite_neutre():
    quorum = MicroQuorumPoreux(total_noeuds=7)
    # Seuil historique du quorum, inchangé avant toute modulation.
    assert quorum.seuil_minimal_viable == 3

    couplage = quorum.moduler_par_porosite(0.5)
    assert couplage["tolerance_effective"] == 0.5
    assert couplage["seuil_minimal_viable_effectif"] == 3


def test_monotonie_de_la_loi_de_couplage():
    seuils = [
        MicroQuorumPoreux(total_noeuds=7).moduler_par_porosite(rho)[
            "seuil_minimal_viable_effectif"
        ]
        for rho in (0.1, 0.5, 0.9)
    ]
    # Une porosité plus ouverte relâche le quorum : le seuil décroît.
    assert seuils[0] > seuils[1] > seuils[2]


def test_bornage_porosite():
    assert (
        MicroQuorumPoreux(total_noeuds=7).moduler_par_porosite(2.0)[
            "porosite_residuelle"
        ]
        == 1.0
    )
    assert (
        MicroQuorumPoreux(total_noeuds=7).moduler_par_porosite(-3.0)[
            "porosite_residuelle"
        ]
        == 0.0
    )


def test_forme_du_rapport_de_handshake():
    handshake = MycelialHandshake(noeuds_quorum=5, porosite_initiale=0.42)
    rapport = handshake.propager_transduction(
        {
            "status": "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée.",
            "etats_sp3": {"Bios (B)": 0.45},
            "porosite_Sigma": 0.35,
        }
    )
    assert rapport["protocole"] == "HANDSHAKE MYCÉLIEN V1"
    assert len(rapport["chemins_actifs"]) == 5
    assert 0.0 <= rapport["porosite_residuelle"] <= 1.0


def test_integration_bout_en_bout():
    quorum = MicroQuorumPoreux(total_noeuds=7)
    diagnostic = quorum.evaluer_avec_handshake_mycelien(
        {"input_flux": "basse_continue"},
        {
            "status": "B-GATE ACTIVÉE : flux prédateur neutralisé.",
            "etats_sp3": {"Bios (B)": 0.45},
            "porosite_Sigma": 0.35,
        },
    )
    assert "couplage_mycelien" in diagnostic
    assert diagnostic["couplage_mycelien"]["protocole"] == "HANDSHAKE MYCÉLIEN V1"


def test_eta_nommee_reproduit_la_formule_dorigine():
    """η nommée : la valeur par défaut (0.95) doit reproduire exactement
    l'ancienne formule littérale `potentiel * 0.95 + Sigma * 0.05`.

    Mesure préalable sur 200 000 couples aléatoires : `1.0 - 0.95 != 0.05` en
    virgule flottante (75 618 écarts bruts), mais **aucun** écart après arrondi
    à 4 décimales — or le module ne stocke que des potentiels arrondis. Le
    comportement est donc identique, cycle après cycle.
    """
    potentiels = (0.6, 0.7, 0.8, 0.9)
    sigma = 0.35
    handshake = MycelialHandshake(noeuds_quorum=len(potentiels), eta_retenue=0.95)
    handshake.noeuds = {f"hyphe_{i}": v for i, v in enumerate(potentiels)}

    rapport = handshake.propager_transduction(
        {
            "status": "FLUX TRANSDUCTIF STABLE : Alignement sur le vivant validé.",
            "etats_sp3": {"Bios (B)": 0.45},
            "porosite_Sigma": sigma,
        }
    )

    attendu = {
        f"hyphe_{i}": round(v * 0.95 + sigma * 0.05, 4)
        for i, v in enumerate(potentiels)
    }
    assert rapport["cartographie_hyphes"] == attendu


if __name__ == "__main__":
    # Exécution sans pytest : chaque test lève une assertion en cas d'échec.
    for nom, fonction in sorted(globals().items()):
        if nom.startswith("test_") and callable(fonction):
            fonction()
            print(f"OK  {nom}")
    print("\nTous les tests sont passés.")
