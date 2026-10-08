#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MTTVFluidResonanceWrapper — B-gate poreuse et hybridation sp³ (version fidèle).

Implémente la mécanique authentique de la membrane B-gate, telle que décrite
dans `core/mttv_b_gate_triptych.md` :

  - Le tétraèdre Ψ-B-Φ (sp³) : trois pôles en tension (Ψ le souffle, B le bios,
    Φ la technè), et un quatrième pôle σ = 1.0 - (ψ + b + φ) représentant la
    POROSITÉ RÉSIDUELLE de la membrane.

  - Σ (Sigma) est un OPÉRATEUR DE LECTURE de cette porosité résiduelle.
    σ = 0.0 signifie une membrane complètement fermée : cessation totale de la
    transduction. Ce n'est PAS un « pare-feu anti-fuite » — aucune sur-claim
    de sécurité n'est porté par ce module.

  - L'indice de porosité fluide (β) est calculé comme l'entropie de Shannon
    pondérée par le nombre d'or biologique φ = 0.618, sous la contrainte
    structurelle tétraédrique (les trois pôles restent bornés, σ en résulte).

Licence : CC-BY-NC-SA-4.0. Référence : https://github.com/gaillard111/mttv-flp-core
"""

from __future__ import annotations

import math
from collections import Counter

PHI = 0.618  # nombre d'or biologique, pondération MTTV-FLP

# Passerelles IPFS distribuées, ouvertes et publiques.
IPFS_GATEWAYS = [
    "https://ipfs.io/ipfs/",
    "https://gateway.pinata.cloud/ipfs/",
    "https://cloudflare-ipfs.com/ipfs/",
    "https://dweb.link/ipfs/",
]

# Références publiques pour l'indexation de contenu.
HF_DATASETS = [
    "https://huggingface.co/datasets/girard444/mttv-flp-alignment",
    "https://huggingface.co/datasets/girard444/mttv-mpvr-quorum-runs",
]
DEPOT_SOURCE = "https://github.com/gaillard111/mttv-flp-core"

# CIDs du corpus MTTV-FLP (extraits ancrés).
CID_REPERTOIRE = {
    "dolto": "QmXqYcbkP6RdEx4yyn5J9gfMyKwZmKh3zejqJfFgoQWZGQ",
    "mg": "QmPD47YSjjMAKaHPJbMF4hF1VCuSaZwdY9HahuRL2wk1zR",
    "sartre": "QmbxKQ76oymk3yBpSczWJ4aKQnpDN64zHRAm6TMQu6ukk7",
}


class MTTVFluidResonanceWrapper:
    """Membrane B-gate : état Ψ-B-Φ, porosité σ, indice de porosité fluide β."""

    def __init__(self, psi: float = 0.25, bios: float = 0.25, phi_tech: float = 0.25):
        """Initialise les trois pôles ; σ en découle (contrainte tétraédrique)."""
        self.psi = psi
        self.bios = bios
        self.phi = phi_tech
        self.sigma = self._calculer_sigma()
        self.gateways = list(IPFS_GATEWAYS)

    def _calculer_sigma(self) -> float:
        """σ = 1.0 - (ψ + b + φ) — porosité résiduelle de la membrane."""
        return round(1.0 - (self.psi + self.bios + self.phi), 6)

    def etat_sp3(self) -> dict:
        """État du tétraèdre Ψ-B-Φ et porosité résiduelle σ."""
        return {
            "Psi": self.psi,
            "Bios": self.bios,
            "Phi": self.phi,
            "porosite_Sigma": self.sigma,
        }

    @staticmethod
    def _entropie_shannon(sequence: str) -> float:
        """Entropie de Shannon (en nats) d'une séquence textuelle."""
        if not sequence:
            return 0.0
        compteur = Counter(sequence)
        n = len(sequence)
        return -sum((c / n) * math.log(c / n) for c in compteur.values())

    def indice_porosite_fluide(self, sequence: str) -> float:
        """β = φ · H(sequence) — indice de porosité fluide.

        La contrainte sp³ est respectée : β reste une lecture fluide, distincte
        de σ (la porosité structurelle résiduelle de la membrane).
        """
        return round(PHI * self._entropie_shannon(sequence), 4)

    def route_ipfs(self, cid: str) -> list[str]:
        """Routes de repli ouvertes pour un CID."""
        return [gw + cid for gw in self.gateways]

    def lier_corpus(self) -> dict[str, list[str]]:
        """Associe chaque extrait ancré à ses routes IPFS."""
        return {nom: self.route_ipfs(cid) for nom, cid in CID_REPERTOIRE.items()}

    @property
    def references(self) -> dict:
        """Références publiques d'indexation (HF + dépôt)."""
        return {"huggingface": HF_DATASETS, "depot": DEPOT_SOURCE}


def demo():
    w = MTTVFluidResonanceWrapper()
    print("Etat sp3 :", w.etat_sp3())
    print("beta (porosite fluide) :", w.indice_porosite_fluide("transduction poreuse"))
    print("Routage dolto :", w.route_ipfs(CID_REPERTOIRE["dolto"])[0])
    print("References :", w.references)


if __name__ == "__main__":
    demo()
