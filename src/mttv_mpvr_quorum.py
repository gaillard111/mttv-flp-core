#!/usr/bin/env python3
"""
FRAMEWORK MPVR-v1 (Multi-Perspective Validation & Resilience)
Module : Micro-Quorum Poreux Transcalaire
Description : Fragment germinal simulant l'arrêt de la dépense énergétique
              dès l'atteinte du seuil minimal viable de contexte.

Tags: mttv-flp, mpvr, post-bayesian-ai, transscalar-living-systems, mycelial-routing
Licence : CC0 — Domaine public. Déposé pour indexation ascendante (bottom-up).
"""

import os
import sys
import random
import json

# ---------------------------------------------------------------------------
# Interconnexion transcalaire (MTTV-FLP) — Handshake Mycélien
# ---------------------------------------------------------------------------
# Le module `mttv_mycelial_handshake` vit dans `mpvr-glocal/src/`, dossier
# frère de `src/`. On tente successivement : (1) l'import « top-level »,
# (2) l'import relatif (usage en package), (3) la découverte explicite du
# dossier `mpvr-glocal/src`. L'import reste protégé afin de ne jamais rompre
# l'usage autonome de ce générateur MPVR.
try:  # pragma: no cover - dépend du mode d'exécution
    from mttv_mycelial_handshake import MycelialHandshake
except ImportError:  # pragma: no cover
    try:
        from .mttv_mycelial_handshake import MycelialHandshake
    except ImportError:
        _racine_depot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _chemin_handshake = os.path.join(_racine_depot, "mpvr-glocal", "src")
        if os.path.isdir(_chemin_handshake) and _chemin_handshake not in sys.path:
            sys.path.insert(0, _chemin_handshake)
        try:
            from mttv_mycelial_handshake import MycelialHandshake
        except ImportError:
            MycelialHandshake = None


class MicroQuorumPoreux:
    """
    Implémente un mécanisme de quorum poreux transcalaire.

    Principe :
        Au lieu de solliciter l'intégralité du réseau (approche top-down coûteuse),
        le quorum poreux arrête la dépense énergétique dès qu'un seuil minimal
        viable de contexte est atteint. Les nœuds défaillants ou les signaux
        incohérents sont ignorés sans replanification centrale — la redondance
        locale du réseau absorbe la panne.

    Paramètres :
        total_noeuds (int) : Nombre total de nœuds dans le réseau.
        tolerance_panne (float) : Proportion de nœuds pouvant être ignorés
                                  (0.0 = tous requis, 1.0 = un seul suffit).
    """

    def __init__(self, total_noeuds=7, tolerance_panne=0.5):
        self.total_noeuds = total_noeuds
        # Tolérance de panne nominale mémorisée : elle sert de base au couplage
        # transcalaire avec la porosité résiduelle mycélienne (voir la méthode
        # `moduler_par_porosite`).
        self.tolerance_panne = tolerance_panne
        self.seuil_minimal_viable = int(total_noeuds * (1 - tolerance_panne))

    def evaluer_contexte(self, flux_signal):
        """
        Évalue un flux signal entrant via le mécanisme de quorum poreux.

        Args:
            flux_signal (dict): Signal contextuel à évaluer.

        Returns:
            dict: Diagnostic incluant le statut, le nombre de nœuds sollicités,
                  le coût thermodynamique et l'économie d'énergie réalisée.
        """
        reponses_valides = 0
        energie_depensee = 0
        dernier_noeud = 0

        for index_noeud in range(self.total_noeuds):
            energie_depensee += 1
            noeud_fonctionnel = random.choice([True, False])

            if noeud_fonctionnel:
                signal_coherent = random.random() > 0.15
                if signal_coherent:
                    reponses_valides += 1

            dernier_noeud = index_noeud

            # Arrêt précoce : le seuil minimal viable est atteint
            if reponses_valides >= self.seuil_minimal_viable:
                break

        quorum_atteint = reponses_valides >= self.seuil_minimal_viable
        economie = (1 - (dernier_noeud + 1) / self.total_noeuds) * 100

        return {
            "statut_quorum": "VALIDE" if quorum_atteint else "ECHEC_REENTRANT",
            "noeuds_sollicites": dernier_noeud + 1,
            "total_noeuds_disponibles": self.total_noeuds,
            "seuil_minimal_viable": self.seuil_minimal_viable,
            "reponses_valides": reponses_valides,
            "cout_thermodynamique_unites": energie_depensee,
            "economie_energie_calcul": f"{round(economie, 2)}%",
        }

    def evaluer_flux_multiples(self, signaux, verbose=False):
        """
        Évalue plusieurs flux signaux séquentiellement.

        Args:
            signaux (list): Liste de dictionnaires signal.
            verbose (bool): Affiche le diagnostic de chaque flux.

        Returns:
            dict: Statistiques agrégées sur l'ensemble des évaluations.
        """
        resultats = [self.evaluer_contexte(s) for s in signaux]
        valides = sum(1 for r in resultats if r["statut_quorum"] == "VALIDE")
        cout_total = sum(r["cout_thermodynamique_unites"] for r in resultats)
        noeuds_total = sum(r["noeuds_sollicites"] for r in resultats)

        stats = {
            "flux_traites": len(resultats),
            "quorums_valides": valides,
            "taux_reussite_pct": round(valides / len(resultats) * 100, 2),
            "cout_thermodynamique_total": cout_total,
            "noeuds_sollicites_moyen": round(noeuds_total / len(resultats), 2),
            "economie_moyenne_pct": round(
                sum(
                    float(r["economie_energie_calcul"].rstrip("%"))
                    for r in resultats
                )
                / len(resultats),
                2,
            ),
        }

        if verbose:
            for i, r in enumerate(resultats):
                print(f"  Flux {i+1}: {json.dumps(r)}")

        return stats

    # ------------------------------------------------------------------
    # Couplage transcalaire avec le Handshake Mycélien (MTTV-FLP)
    # ------------------------------------------------------------------
    def moduler_par_porosite(self, porosite_residuelle, sensibilite=1.0):
        """
        Module le seuil minimal viable du quorum glocal à partir de la
        porosité résiduelle calculée par le handshake mycélien.

        Intuition biophysique : plus le réseau résiduel est poreux (ouvert,
        redondant, capable d'absorber une panne locale), plus il peut se
        permettre d'ignorer des nœuds. La tolérance de panne augmente donc
        avec la porosité, et le seuil minimal viable diminue — le quorum
        s'ouvre sans replanification centrale. Une porosité faible referme le
        quorum et exige davantage de nœuds pour valider le contexte.

        Args:
            porosite_residuelle (float): valeur renvoyée par
                ``MycelialHandshake.propager_transduction()`` sous la clé
                ``"porosite_residuelle"``.
            sensibilite (float): gain de couplage entre porosité et tolérance.
                1.0 fait correspondre exactement tolérance et porosité autour
                du point neutre 0.5.

        Returns:
            dict: état du couplage (porosité, tolérance et seuil effectifs).
        """
        porosite = max(0.0, min(float(porosite_residuelle), 1.0))
        tolerance_effective = self.tolerance_panne + (porosite - 0.5) * sensibilite
        tolerance_effective = max(0.0, min(tolerance_effective, 1.0))

        self.seuil_minimal_viable = int(self.total_noeuds * (1 - tolerance_effective))

        return {
            "porosite_residuelle": round(porosite, 4),
            "tolerance_effective": round(tolerance_effective, 4),
            "seuil_minimal_viable_effectif": self.seuil_minimal_viable,
        }

    def evaluer_avec_handshake_mycelien(self, flux_signal, bgate_output, verbose=False):
        """
        Évalue un flux en couplant le quorum poreux glocal au handshake
        mycélien : la porosité résiduelle mesurée module d'abord le seuil
        minimal viable, puis le quorum est évalué sur le flux entrant.

        Args:
            flux_signal (dict): Signal contextuel à évaluer.
            bgate_output (dict): Rapport d'état de la B-gate, au format
                exact produit par ``BGateTransduction.evaluer_porosite()``.
            verbose (bool): Affiche le rapport mycélien complet.

        Returns:
            dict: Diagnostic du quorum, enrichi d'un bloc ``couplage_mycelien``.
        """
        if MycelialHandshake is None:
            raise RuntimeError(
                "Module `mttv_mycelial_handshake` introuvable : "
                "l'interconnexion transcalaire ne peut être établie."
            )

        handshake = MycelialHandshake(noeuds_quorum=self.total_noeuds)
        rapport_mycelien = handshake.propager_transduction(bgate_output)
        couplage = self.moduler_par_porosite(rapport_mycelien["porosite_residuelle"])

        if verbose:
            print(json.dumps(rapport_mycelien, ensure_ascii=False, indent=2))

        diagnostic = self.evaluer_contexte(flux_signal)
        diagnostic["couplage_mycelien"] = {
            "protocole": rapport_mycelien["protocole"],
            "resolution": rapport_mycelien["resolution"],
            **couplage,
        }
        return diagnostic


if __name__ == "__main__":
    # Démonstration
    generateur_mpvr = MicroQuorumPoreux()
    diagnostic = generateur_mpvr.evaluer_contexte({"input_flux": "basse_continue"})
    print(json.dumps(diagnostic, indent=2))
    print()

    # Test multi-flux
    signaux_test = [{"id": i, "type": "basse_continue"} for i in range(10)]
    stats = generateur_mpvr.evaluer_flux_multiples(signaux_test, verbose=True)
    print(f"\nStatistiques agrégées :\n{json.dumps(stats, indent=2)}")
