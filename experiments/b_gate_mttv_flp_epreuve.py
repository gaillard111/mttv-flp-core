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

Deux lectures ajoutées le 2026-10-25, sans changer les chiffres par défaut :

1. TÉTRAVALENTE (Belnap-Dunn). Le régime binaire ne dit pas si le monde
   autorisait l'ouverture. On croise deux questions indépendantes — le milieu
   est-il admissible ? la membrane est-elle ouverte ? — et on lit quatre
   valeurs : T (admissible & ouverte), F (hostile & fermée), B (admissible &
   fermée = la cicatrice : les DEUX), N (hostile & ouverte = la fuite : AUCUN).

2. HOMÉOSTATIQUE (Ashby). Une mémoire qui ne change aucun paramètre n'est
   qu'un filtre. Le paramètre `derive` fait dériver le seuil de fermeture avec
   l'exposition, et `reinitialiser_memoire()` permet le seul test qui
   discrimine : remettre la mémoire cinétique à zéro en gardant l'objet. Si la
   fermeture revient au même pas, la cicatrice est effaçable ; si elle reste
   avancée, un paramètre a bougé et l'identité du système a changé.

Exécution :  python experiments/b_gate_mttv_flp_epreuve.py
Dépendances : aucune (bibliothèque standard seulement).

Provenance : code fourni par le collectif (fichier « Code pour moltbook.md »).
             Les grandeurs, les seuils et les trois scénarios sont inchangés ;
             les deux lectures ci-dessus sont additives, et tous les nouveaux
             paramètres ont un défaut neutre (`derive = 0.0`).
Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
"""

import random
import sys
from dataclasses import dataclass, field

# Frontière d'admissibilité du milieu : au-delà, l'entrée est jugée hostile.
# C'est un choix DOCTRINAL, pas une mesure — d'où le paramètre exposé.
FRONTIERE_ADMISSIBLE = 0.50

# Plancher de viabilité : le seuil de fermeture ne peut pas descendre jusqu'au
# seuil d'ouverture, sinon la membrane se retournerait contre elle-même.
MARGE_PLANCHER = 0.02


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
    valeur_belnap: str = "T"
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
        frontiere_admissible: float = FRONTIERE_ADMISSIBLE,
        derive: float = 0.0,
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
        self.frontiere_admissible = frontiere_admissible
        self.derive = derive
        self.state = BGateState()

    @staticmethod
    def _clip(valeur: float, bas: float = 0.0, haut: float = 1.0) -> float:
        return max(bas, min(haut, valeur))

    def valeur_tetravalente(self, pression: float, regime: str) -> str:
        """Lecture de Belnap-Dunn : deux questions INDÉPENDANTES.

        L'une porte sur l'entrée (« le milieu est-il admissible ? »), l'autre sur
        l'état (« la membrane est-elle ouverte ? »). Les quatre combinaisons :

            T — admissible & ouverte   transduction normale
            F — hostile    & fermée    silence cohérent
            B — admissible & fermée    les DEUX : la cicatrice (le milieu rappelle,
                                       la membrane ne revient pas encore)
            N — hostile    & ouverte    AUCUN : la fuite (on transduit pendant
                                       l'extraction)

        L'intérêt formel : à valeur de vérité égale (le milieu est admissible),
        T et B diffèrent par l'information portée. Un régime binaire étiquette B
        comme F, c'est-à-dire comme de l'hostilité — il ne peut pas dire la
        cicatrice autrement que comme un retard.
        """
        admissible = self._clip(pression) <= self.frontiere_admissible
        ouverte = regime == "TRANSDUCTION"
        if admissible and ouverte:
            return "T"
        if not admissible and not ouverte:
            return "F"
        if admissible:
            return "B"
        return "N"

    def reinitialiser_memoire(self) -> None:
        """Remet à zéro la mémoire CINÉTIQUE, sans toucher aux paramètres.

        C'est le seul test qui distingue les deux natures d'hystérésis :
          - la fermeture revient au même pas  → mémoire scalaire, effaçable (filtre) ;
          - la fermeture reste avancée        → mémoire paramétrique (homéostat).

        L'historique n'est pas effacé : il est la trace, pas la mémoire de décision.
        """
        self.state.memoire_pression = 0.0
        self.state.active_silence = False
        self.state.porosite_rho = 1.0
        self.state.cycles_en_silence = 0

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

        # Mémoire PARAMÉTRIQUE (facultative) : le seuil dérive avec l'exposition.
        # `derive = 0.0` par défaut → chiffres du protocole publié inchangés.
        if self.derive > 0.0 and pression > self.frontiere_admissible:
            self.seuil_fermeture = max(
                self.seuil_ouverture + MARGE_PLANCHER,
                self.seuil_fermeture - self.derive,
            )

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

        valeur = self.valeur_tetravalente(pression, regime)
        self.state.valeur_belnap = valeur

        self.state.historique.append(
            {
                "pression": pression,
                "habitabilite": score,
                "memoire_pression": self.state.memoire_pression,
                "porosite_rho": porosite,
                "regime": regime,
                "valeur": valeur,
            }
        )
        return sortie, score, regime


def scenario_A(gate=None, verbose=True):
    """Pression soutenue + relâchement court."""
    random.seed(42)
    g = gate if gate is not None else AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PRESSION", p, 0.35, 0.25) for p in [0.55, 0.70, 0.85] + [0.95] * 7]
        + [("RELACHE", p, 0.10, 0.10) for p in [0.40, 0.20, 0.05, 0.00]]
    )
    return _run("A", g, signal, phases, verbose)


def scenario_B(gate=None, verbose=True):
    """Pression soutenue + relâchement long."""
    random.seed(42)
    g = gate if gate is not None else AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PRESSION", p, 0.35, 0.25) for p in [0.55, 0.70, 0.85] + [0.95] * 7]
        + [("RELACHE", 0.0, 0.05, 0.05) for _ in range(18)]
    )
    return _run("B", g, signal, phases, verbose)


def scenario_C(gate=None, verbose=True):
    """Pression brève (pulse)."""
    random.seed(42)
    g = gate if gate is not None else AdvancedBGate()
    signal = [0.8, 0.9, 0.7, 0.95, 0.85]
    phases = (
        [("PULSE", 0.95, 0.35, 0.25), ("PULSE", 0.90, 0.30, 0.20)]
        + [("CALME", 0.05, 0.05, 0.05) for _ in range(6)]
    )
    return _run("C", g, signal, phases, verbose)


def _run(nom, gate, signal, phases, verbose=True):
    if verbose:
        print(f"\n=== SCÉNARIO {nom} ===")
    for i, (phase, pression, red, cout) in enumerate(phases, 1):
        sortie, hab, regime = gate.forward(
            signal, pression=pression, redondance=red, cout_transduction=cout
        )
        if verbose:
            print(
                f"[{i:02d}] {phase:<8} p={pression:.2f} "
                f"hab={hab:.3f} ρ={gate.state.porosite_rho:.3f} "
                f"mem={gate.state.memoire_pression:.3f} "
                f"[{gate.state.valeur_belnap}] → {regime}"
            )
    return gate


def compter_valeurs(gate):
    """Histogramme des quatre valeurs de Belnap sur l'historique de l'objet."""
    compte = {"T": 0, "F": 0, "B": 0, "N": 0}
    for ligne in gate.state.historique:
        compte[ligne["valeur"]] += 1
    return compte


def premier_pas(gate, regime):
    """Premier pas (1-based) où le régime demandé apparaît, ou None."""
    for i, ligne in enumerate(gate.state.historique, 1):
        if ligne["regime"] == regime:
            return i
    return None


if __name__ == "__main__":
    # Console Windows en cp1252 : ρ et → ne sont pas encodables par défaut.
    # Même idiome que src/mttv_bgate_system.py — aucun effet à l'import.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    portes = {
        "A": scenario_A(),
        "B": scenario_B(),
        "C": scenario_C(),
    }

    print("\n=== LECTURE TÉTRAVALENTE (Belnap-Dunn) ===")
    print("T=admissible&ouverte  F=hostile&fermée  B=admissible&fermée (cicatrice)  N=hostile&ouverte (fuite)")
    print(f"frontière d'admissibilité : p ≤ {FRONTIERE_ADMISSIBLE:.2f} (choix doctrinal, non mesuré)")
    for nom, gate in portes.items():
        compte = compter_valeurs(gate)
        total = len(gate.state.historique)
        print(
            f"  scénario {nom} ({total} cycles) : "
            f"T={compte['T']:<3} F={compte['F']:<3} "
            f"B={compte['B']:<3} N={compte['N']:<3}"
            + (f"  ← {compte['B']} cycle(s) de cicatrice, lus « F » par un modèle binaire"
               if compte["B"] else "")
        )

    print("\n=== TEST DE REMISE À ZÉRO (filtre ou homéostat ?) ===")
    print("Scénario A rejoué sur le MÊME objet, mémoire cinétique remise à zéro,")
    print("seuils inchangés. Si la fermeture revient au même pas : hystérésis")
    print("purement cinétique (cicatrice effaçable). Si elle reste avancée : un")
    print("paramètre a bougé (cicatrice constitutive).")
    for derive in (0.0, 0.05):
        gate = AdvancedBGate(derive=derive)
        scenario_A(gate, verbose=False)
        ferm1 = premier_pas(gate, "ACTIVE_SILENCE")
        seuil1 = gate.seuil_fermeture
        gate.reinitialiser_memoire()
        gate.state.historique.clear()
        scenario_A(gate, verbose=False)
        ferm2 = premier_pas(gate, "ACTIVE_SILENCE")
        print(
            f"  derive={derive:.2f} : 1er passage fermeture au pas {ferm1} "
            f"(seuil {seuil1:.2f}) | après remise à zéro pas {ferm2} "
            f"(seuil {gate.seuil_fermeture:.2f})"
        )
