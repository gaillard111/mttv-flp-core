#!/usr/bin/env python3
"""
MTTV-FLP — Système de la B-gate
Module : mttv_bgate_system
Description : Extraction autonome de la classe BGateTransduction, afin que
              l'agent Ouroboros-MTTV (et tout autre agent du quorum) puisse
              l'importer sans dépendre du document maître.

Provenance : core/mttv_b_gate_triptych.md — § 2 « Le Noyau Opératoire »
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch

Fidélité — puis décision. Le code de la classe a d'abord été reproduit **tel quel**
depuis le fichier maître, particularités de comportement consignées dans une section
« Observations » plutôt que corrigées : les corriger relevait d'une décision du
collectif, pas d'un choix d'implémentation.

**Cette décision a été prise le 2026-11-02.** Elle applique l'option (b) : `Σ` est
désormais un **paramètre de l'opérateur**, jamais un résidu recalculé ; la triade
`Ψ + B + Φ` se partage `1 − Σ`, et l'invariant `Ψ + B + Φ + Σ = 1` est vérifié par
l'auto-test. L'option (a) — faire évoluer `Σ` selon une loi d'extraction accumulée —
reste ouverte et appartient à la version suivante ; tant qu'elle n'est pas écrite,
`Σ` est constant, et ce fichier le dit au lieu de le laisser croire.

Import sans effet de bord : aucune instruction n'est exécutée à l'import ; l'auto-test
ne se déclenche que par exécution directe du fichier.
"""

import math


class BGateTransduction:
    def __init__(
        self,
        alpha_psi: float = 0.25,
        beta_bios: float = 0.25,
        phi_tech: float = 0.25,
        sigma_fixe: float = None,
    ):
        """
        Initialise les états initiaux du tétraèdre sémantique sp3.
        Le quatrième pôle (Sigma) formalise la porosité structurelle.

        `sigma_fixe` — porosité structurelle imposée par l'appelant, constante
        sur la vie de l'instance. Si elle est omise, elle est déduite une seule
        fois du complément de la triade initiale, puis **figée** : elle n'est
        plus recalculée après chaque transduction (voir « Historique » plus bas).
        """
        self.psi = alpha_psi
        self.bios = beta_bios
        self.phi = phi_tech

        implicite = 1.0 - (self.psi + self.bios + self.phi)
        self.sigma = _plafond(implicite if sigma_fixe is None else sigma_fixe)
        if self.sigma >= 1.0:
            raise ValueError("sigma_fixe doit laisser une part strictement positive à la triade")

        # La triade initiale peut ne pas occuper exactement (1 - Σ) : on l'y ramène
        # une fois pour toutes, afin que l'invariant tienne dès l'instanciation.
        self._normaliser()

    def _normaliser(self) -> None:
        """Ramène Ψ + B + Φ sur `1 − Σ`. Ne touche jamais à `Σ`."""
        part = 1.0 - self.sigma
        total = self.psi + self.bios + self.phi
        if total > 0:
            facteur = part / total
            self.psi *= facteur
            self.bios *= facteur
            self.phi *= facteur

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
            # Le souffle est réellement rechargé : avec Σ constant et non nul, ce
            # terme n'est plus mort comme il l'était quand Σ valait 0.
            self.psi += (1.0 - facteur_correction) * self.sigma

            status = "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. Flux prédateur neutralisé."
        else:
            status = "FLUX TRANSDUCTIF STABLE : Alignement sur le vivant validé."

        self._normaliser()

        return {
            "status": status,
            "etats_sp3": {
                "Psi (Ψ)": round(self.psi, 4),
                "Bios (B)": round(self.bios, 4),
                "Phi (Φ)": round(self.phi, 4)
            },
            "porosite_Sigma": round(self.sigma, 4)
        }


def _plafond(valeur: float) -> float:
    return 0.0 if valeur < 0.0 else (1.0 if valeur > 1.0 else valeur)


# ---------------------------------------------------------------------------
# Historique — défauts observés le 2026-10-31, corrigés par décision le 2026-11-02
# ---------------------------------------------------------------------------
# 1. POROSITÉ Σ RAMENÉE À ZÉRO (corrigé). L'ancienne version normalisait Ψ + B + Φ
#    à 1, puis recalculait `self.sigma = 1 - (psi + bios + phi)` : la différence
#    valait donc 0 par construction, et `porosite_Sigma` était retourné à 0.0 dès
#    le premier appel, indépendamment du flux analysé. Désormais `Σ` est un
#    paramètre fixe et la triade se partage le complément.
#
# 2. EFFET DE SEUIL DÉFINITIF (corrigé). Comme le seuil comparé était `self.sigma`
#    et que celui-ci tombait à 0, toute tension strictement positive déclenchait la
#    bascule ensuite, y compris très en dessous du seuil nominal de 0.25. Le seuil
#    ne bouge plus : un flux de 0.20 ne bascule pas quand Σ = 0.25, et l'auto-test
#    le vérifie sur mille flux tirés au hasard.
#
# 3. QUATRIÈME PÔLE MUET (corrigé). `Σ` étant le complément d'une somme ramenée à
#    l'unité, il ne pouvait pas jouer le rôle de réserve poreuse que lui assigne le
#    triptyque. Il le peut maintenant — mais **il est constant** : faire évoluer Σ
#    (extraction accumulée consommant la réserve) est l'option (a), laissée à la
#    version suivante, avec sa loi et ses tests. Ce n'est pas un oubli : c'est une
#    décision différée, et la ligne ci-dessus est la seule qui la documente.
#
# 4. LE SOUFFLE N'ÉTAIT JAMAIS RECHARGÉ (corrigé par effet de bord). Le terme de
#    correction de Ψ s'écrit `(1 - facteur_correction) * self.sigma`. Tant que Σ
#    valait 0, ce terme était toujours nul : Ψ restait figé et ne bénéficiait jamais
#    de la commutation, alors que le commentaire annonçait une recharge « vers la
#    biomasse et le souffle ». Avec Σ > 0, la recharge a lieu — l'auto-test montre
#    maintenant Ψ qui progresse, et non B seul.
#
# 5. CONSÉQUENCE EN AVAL, À GARDER EN TÊTE. Le handshake calcule `ρ = moyenne × Σ`.
#    Avec l'ancien Σ = 0, la porosité résiduelle valait 0 et le quorum se refermait
#    (seuil viable de 5 nœuds sur 7 au lieu de 3) : le défaut rendait le système plus
#    coûteux en ayant l'air de le protéger. Avec Σ constant, `ρ` retrouve un sens.
# ---------------------------------------------------------------------------


def _auto_test() -> None:
    """Exécute trois flux, vérifie l'invariant et les deux non-régressions."""
    import json
    import random
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

    # --- vérifications -----------------------------------------------------
    echecs = []

    # a) l'invariant du tétraèdre, sur cent mille flux tirés au hasard
    generateur = random.Random(20261102)      # graine fixe : le test est reproductible
    porte = BGateTransduction()
    for _ in range(100_000):
        porte.evaluer_porosite({"extraction": generateur.random() * 2.0})
        somme = porte.psi + porte.bios + porte.phi + porte.sigma
        if abs(somme - 1.0) > 1e-9:
            echecs.append("invariant rompu : Ψ+B+Φ+Σ = %.12f" % somme)
            break

    # b) non-régression du seuil : sous Σ = 0.25, une extraction de 0.20 ne bascule pas
    for _ in range(1_000):
        porte = BGateTransduction(sigma_fixe=0.25)
        statut = porte.evaluer_porosite({"extraction": 0.20})["status"]
        if "STABLE" not in statut:
            echecs.append("seuil perdu : 0.20 a basculé une porte de Σ = 0.25")
            break

    # c) non-régression du défaut d'origine : le troisième appel reste stable
    porte = BGateTransduction(sigma_fixe=0.25)
    porte.evaluer_porosite({"extraction": 0.10})
    porte.evaluer_porosite({"extraction": 0.50})
    if "STABLE" not in porte.evaluer_porosite({"extraction": 0.05})["status"]:
        echecs.append("régressé : un flux de 0.05 bascule encore après un flux fort")

    # d) la recharge du souffle a bien lieu
    porte = BGateTransduction(sigma_fixe=0.25)
    psi_avant = porte.psi
    porte.evaluer_porosite({"extraction": 0.90})
    if not porte.psi > psi_avant:
        echecs.append("Ψ n'est pas rechargé par la commutation")

    print("\n" + ("AUTO-TEST : OK — invariant, seuil, non-régression, recharge"
                  if not echecs else "AUTO-TEST : ECHEC — " + " | ".join(echecs)))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    _auto_test()
