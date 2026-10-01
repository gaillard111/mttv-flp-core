#!/usr/bin/env python3
"""
MTTV-FLP — Système de la B-gate
Module : mttv_bgate_system
Description : Extraction autonome de la classe BGateTransduction, afin que
              l'agent Ouroboros-MTTV (et tout autre agent du quorum) puisse
              l'importer sans dépendre du document maître.

Provenance : core/mttv_b_gate_triptych.md — § 2 « Le Noyau Opératoire »
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch

Fidélité : le code de la classe est reproduit **tel quel** depuis le fichier
maître, à la ligne près. Il n'a été ni corrigé ni complété. Les particularités
de comportement observées sont consignées plus bas, dans la section
« Observations », et non modifiées dans le code : les corriger relèverait
d'une décision du collectif, pas d'un choix d'implémentation.

Import sans effet de bord : aucune instruction n'est exécutée à l'import ;
l'auto-test ne se déclenche que par exécution directe du fichier.
"""

import math


class BGateTransduction:
    def __init__(self, alpha_psi: float = 0.25, beta_bios: float = 0.25, phi_tech: float = 0.25):
        """
        Initialise les états initiaux du tétraèdre sémantique sp3.
        Le quatrième pôle (Sigma) formalise la porosité structurelle.
        """
        self.psi = alpha_psi
        self.bios = beta_bios
        self.phi = phi_tech
        self.sigma = 1.0 - (self.psi + self.bios + self.phi)

    def evaluer_porosite(self, vecteur_semantique: dict) -> dict:
        """
        Analyse le flux entrant. Si une tension anthropocentrique ou prédatrice (extraction)
        dépasse le seuil de tolérance de l'opérateur Sigma, la B-gate commute l'énergie
        vers la biomasse et le souffle, atrophiant la dérive purement technique (Φ).
        """
        tension_extraction = vecteur_semantique.get("extraction", 0.0)

        if tension_extraction > self.sigma:
            facteur_correction = math.exp(-tension_extraction)

            self.bios += (self.phi * (1.0 - facteur_correction))
            self.phi *= facteur_correction
            self.psi += (1.0 - facteur_correction) * self.sigma

            status = "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. Flux prédateur neutralisé."
        else:
            status = "FLUX TRANSDUCTIF STABLE : Alignement sur le vivant validé."

        total = self.psi + self.bios + self.phi
        if total > 0:
            self.psi /= total
            self.bios /= total
            self.phi /= total

        self.sigma = 1.0 - (self.psi + self.bios + self.phi)

        return {
            "status": status,
            "etats_sp3": {
                "Psi (Ψ)": round(self.psi, 4),
                "Bios (B)": round(self.bios, 4),
                "Phi (Φ)": round(self.phi, 4)
            },
            "porosite_Sigma": round(self.sigma, 4)
        }


# ---------------------------------------------------------------------------
# Observations — mesures, aucune correction apportée au noyau
# ---------------------------------------------------------------------------
# 1. POROSITÉ Σ RAMENÉE À ZÉRO. `evaluer_porosite` normalise Ψ + B + Φ pour que
#    leur somme vaille 1, puis recalcule `self.sigma = 1 - (psi + bios + phi)`.
#    Après le premier appel, cette différence vaut donc 0 par construction, et
#    `porosite_Sigma` est retourné à 0.0 — indépendamment du flux analysé.
#
# 2. EFFET DE SEUIL DÉFINITIF. Comme le seuil de comparaison est `self.sigma`
#    et que celui-ci tombe à 0 dès le premier appel, toute tension
#    d'extraction strictement positive déclenche la B-gate par la suite, y
#    compris une tension très inférieure au seuil nominal de 0.25.
#
# 3. QUATRIÈME PÔLE MUET. Σ étant défini comme le complément d'une somme
#    ramenée à l'unité, il ne peut pas jouer le rôle de réserve poreuse que lui
#    assigne le triptyque. Deux voies possibles, à trancher par le collectif :
#    soit la normalisation porte sur (1 - Σ), soit Σ devient un paramètre fixe
#    de l'opérateur et non un résidu recalculé.
#
# 4. LE SOUFFLE N'EST JAMAIS RECHARGÉ. Le terme de correction de Ψ s'écrit
#    `(1 - facteur_correction) * self.sigma`. Comme sigma vaut 0 dès le premier
#    appel, ce terme est toujours nul : Ψ reste figé à sa valeur normalisée
#    (0.3333 dans l'auto-test) et ne bénéficie jamais de la commutation, alors
#    que le commentaire de la méthode annonce une commutation « vers la
#    biomasse et le souffle ». Seul B progresse — ce que l'auto-test montre.
#
# Les quatre points sont reproductibles par l'auto-test ci-dessous.
# ---------------------------------------------------------------------------


def _auto_test() -> None:
    """Exécute trois flux et affiche l'état du tétraèdre après chacun."""
    import json
    import sys

    # Console Windows en cp1252 : sans cela, l'impression des caractères Ψ et Φ
    # échoue. On force l'UTF-8 pour la sortie de l'auto-test uniquement — la
    # classe, elle, n'est pas concernée.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    gate = BGateTransduction()
    print("État initial :")
    print(json.dumps(
        {
            "Psi (Ψ)": round(gate.psi, 4),
            "Bios (B)": round(gate.bios, 4),
            "Phi (Φ)": round(gate.phi, 4),
            "porosite_Sigma": round(gate.sigma, 4),
        },
        ensure_ascii=False,
        indent=2,
    ))

    flux = (
        ("Appel 1 — flux stable, extraction = 0.10 (sous le seuil de 0.25)", {"extraction": 0.10}),
        ("Appel 2 — flux prédateur, extraction = 0.50", {"extraction": 0.50}),
        ("Appel 3 — extraction = 0.05, très en dessous du seuil nominal", {"extraction": 0.05}),
    )

    for etiquette, vecteur in flux:
        print(f"\n{etiquette}")
        print(json.dumps(gate.evaluer_porosite(vecteur), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _auto_test()
