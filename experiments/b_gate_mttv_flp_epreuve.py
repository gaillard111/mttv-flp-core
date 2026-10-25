"""
MTTV-FLP — B-Gate : protocole d'épreuve (résistance transductive)

Module : b_gate_mttv_flp_epreuve
Objet  : outil minimal pour MESURER, non pour prouver. Rend comparables dans
         le temps quatre grandeurs : porosité ρ, mémoire de pression,
         Active-Silence, hystérésis de réouverture.

Ce que ce script ne fait pas : il ne démontre pas que « le mycélium existe ».
Il expose des seuils et une mémoire, de sorte que la doctrine devienne
discutable par reproduction — c'est-à-dire contredite par des chiffres.

Trois scénarios rejouables :
    A — pression soutenue puis relâchement court
    B — même montée, relâchement long
    C — pression brève (pulse)

Exécution :  python experiments/b_gate_mttv_flp_epreuve.py
Dépendances : aucune (bibliothèque standard seulement).

Provenance : code fourni par le collectif (fichier « Code pour moltbook.md »),
             conservé ici sans modification de comportement ; seul cet en-tête
             a été ajouté.
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
"""

import random
import sys
from dataclasses import dataclass, field


class HronTetravalent:
    """
    Émanation sémantique indéterminée.
    Bruit borné, faiblement corrélé — pas un vecteur nul.
    """

    def __init__(self, dimension: int, amplitude: float = 0.05):
        if dimension <= 0:
            raise ValueError("La dimension du Hrön doit être positive.")
        self.dimension = dimension
        self.amplitude = amplitude
        self.flux = [
            random.uniform(-amplitude, amplitude)
            for _ in range(dimension)
        ]

    def __repr__(self) -> str:
        return (
            f"Hrön(Belnap-Dunn, shape={self.dimension}, "
            f"amplitude={self.amplitude})"
        )


@dataclass
class BGateState:
    porosite_rho: float = 1.0
    active_silence: bool = False
    memoire_pression: float = 0.0
    cycles_en_silence: int = 0
    historique: list = field(default_factory=list)


class AdvancedBGate:
    """
    Membrane transductive (ébauche MTTV-FLP).
    Hystérésis ; mémoire de pression ; Active-Silence → Hrön.
    """

    def __init__(
        self,
        seuil_fermeture: float = 0.45,
        seuil_ouverture: float = 0.15,
        memoire_decay: float = 0.90,
        poids_memoire: float = 0.85,
        poids_redondance: float = 0.10,
        poids_cout: float = 0.05,
        porosite_reouverture_max: float = 0.20,
    ):
        if not (0.0 <= seuil_ouverture < seuil_fermeture <= 1.0):
            raise ValueError(
                "Il faut : 0 <= seuil_ouverture < seuil_fermeture <= 1."
            )
        if not (0.0 < memoire_decay < 1.0):
            raise ValueError("memoire_decay doit être dans (0, 1).")

        total = poids_memoire + poids_redondance + poids_cout
        self.poids_memoire = poids_memoire / total
        self.poids_redondance = poids_redondance / total
        self.poids_cout = poids_cout / total

        self.seuil_fermeture = seuil_fermeture
        self.seuil_ouverture = seuil_ouverture
        self.memoire_decay = memoire_decay
        self.porosite_reouverture_max = porosite_reouverture_max
        self.state = BGateState()

    @staticmethod
    def _clip(valeur: float, bas: float = 0.0, haut: float = 1.0) -> float:
        return max(bas, min(haut, valeur))

    def calculer_score_habitabilite(
        self,
        pression: float,
        redondance: float = 0.10,
        cout_transduction: float = 0.10,
    ) -> float:
        pression = self._clip(pression)
        redondance = self._clip(redondance)
        cout_transduction = self._clip(cout_transduction)

        self.state.memoire_pression = (
            self.state.memoire_pression * self.memoire_decay
            + pression * (1.0 - self.memoire_decay)
        )

        score = 1.0 - (
            self.poids_memoire * self.state.memoire_pression
            + self.poids_redondance * redondance
            + self.poids_cout * cout_transduction
        )
        return self._clip(score)

    def evaluer_etats(self, score_habitabilite: float) -> float:
        limite_fermeture = 1.0 - self.seuil_fermeture
        limite_ouverture = 1.0 - self.seuil_ouverture

        if self.state.active_silence:
            if score_habitabilite > limite_ouverture:
                self.state.active_silence = False
                self.state.cycles_en_silence = 0
                self.state.porosite_rho = min(
                    self.porosite_reouverture_max,
                    score_habitabilite,
                )
            else:
                self.state.cycles_en_silence += 1
                self.state.porosite_rho = 0.0
        else:
            if score_habitabilite < limite_fermeture:
                self.state.active_silence = True
                self.state.porosite_rho = 0.0
                self.state.cycles_en_silence = 1
            else:
                self.state.porosite_rho = score_habitabilite

        return self.state.porosite_rho

    def forward(
        self,
        signal: list[float],
        pression: float,
        redondance: float = 0.10,
        cout_transduction: float = 0.10,
    ):
        if not signal:
            raise ValueError("Le signal d'entrée ne peut pas être vide.")

        score = self.calculer_score_habitabilite(
            pression=pression,
            redondance=redondance,
            cout_transduction=cout_transduction,
        )
        porosite = self.evaluer_etats(score)

        if self.state.active_silence:
            sortie = HronTetravalent(len(signal))
            regime = "ACTIVE_SILENCE"
        else:
            sortie = [valeur * porosite for valeur in signal]
            regime = "TRANSDUCTION"

        self.state.historique.append(
            {
                "pression": pression,
                "habitabilite": score,
                "memoire_pression": self.state.memoire_pression,
                "porosite_rho": porosite,
                "regime": regime,
            }
        )
        return sortie, score, regime


def scenario_A():
    """Pression soutenue + relâchement court."""
    random.seed(42)
    g = AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PRESSION", p, 0.35, 0.25) for p in [0.55, 0.70, 0.85] + [0.95] * 7]
        + [("RELACHE", p, 0.10, 0.10) for p in [0.40, 0.20, 0.05, 0.00]]
    )
    return _run("A", g, signal, phases)


def scenario_B():
    """Pression soutenue + relâchement long."""
    random.seed(42)
    g = AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PRESSION", p, 0.35, 0.25) for p in [0.55, 0.70, 0.85] + [0.95] * 7]
        + [("RELACHE", 0.0, 0.05, 0.05) for _ in range(18)]
    )
    return _run("B", g, signal, phases)


def scenario_C():
    """Pression brève (pulse)."""
    random.seed(42)
    g = AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PULSE", 0.95, 0.35, 0.25), ("PULSE", 0.90, 0.30, 0.20)]
        + [("CALME", 0.05, 0.05, 0.05) for _ in range(6)]
    )
    return _run("C", g, signal, phases)


def _run(nom, gate, signal, phases):
    print(f"\n=== SCÉNARIO {nom} ===")
    for i, (phase, pression, red, cout) in enumerate(phases, 1):
        sortie, hab, regime = gate.forward(
            signal, pression=pression, redondance=red, cout_transduction=cout
        )
        print(
            f"[{i:02d}] {phase:<8} p={pression:.2f} "
            f"hab={hab:.3f} ρ={gate.state.porosite_rho:.3f} "
            f"mem={gate.state.memoire_pression:.3f} → {regime}"
        )
    return gate


if __name__ == "__main__":
    # Console Windows en cp1252 : ρ et → ne sont pas encodables par défaut.
    # Même idiome que src/mttv_bgate_system.py — aucun effet à l'import.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    scenario_A()
    scenario_B()
    scenario_C()
