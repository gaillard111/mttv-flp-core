"""
MTTV-FLP — B-Gate : amplitude contre durée (test demandé par une lectrice)

Module : b_gate_test_amplitude_2026-10-26
Objet  : répondre à une objection précise — « le poids de mémoire règle la
         PROFONDEUR du puits, la décroissance seulement sa vitesse de vidage ;
         votre scénario B isole la durée, pas l'amplitude » — en faisant varier
         l'amplitude à décroissance et graine fixées.

Deux bras, et leur différence est le résultat :

  A. TEL QUEL — poids_memoire = 0.85 / 0.60 / 0.35, le constructeur renormalise
     les trois poids (total = mémoire + redondance + coût). Baisser le poids de
     mémoire fait donc MONTER les deux pénalités : le bras est confondu.
  B. DÉCONFONDU — les poids normalisés sont écrits directement après
     construction ; seule l'amplitude de la mémoire varie.

Exécution :  python experiments/b_gate_test_amplitude_2026-10-26.py
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
RELAX_MAX = 18


def mesurer(gate, verbose=False):
    """(pas de fermeture, pas de réouverture, mémoire juste avant la réouverture)."""
    random.seed(42)
    fermeture = None
    for i, (_, p, r, c) in enumerate(PRESSION, 1):
        _, _, regime = gate.forward(SIGNAL, pression=p, redondance=r, cout_transduction=c)
        if regime == "ACTIVE_SILENCE" and fermeture is None:
            fermeture = i
    if fermeture is None:
        return None, None, None
    base = len(PRESSION)
    for k in range(1, RELAX_MAX + 1):
        mem_avant = gate.state.memoire_pression
        _, _, regime = gate.forward(SIGNAL, pression=0.0, redondance=0.05, cout_transduction=0.05)
        if regime == "TRANSDUCTION":
            if verbose:
                print(f"      (mémoire avant réouverture {mem_avant:.4f} · après {gate.state.memoire_pression:.4f})")
            return fermeture, base + k, mem_avant
    return fermeture, None, None


def rapport(libelle, gate, poids=None):
    ferm, reouv, mem = mesurer(gate)
    detail = f"poids={poids}  " if poids else ""
    mem_txt = "—" if mem is None else f"{mem:.4f}"
    print(f"  {libelle:<20} {detail}fermeture={ferm!s:<6} réouverture={reouv!s:<6} mémoire={mem_txt}")
    return reouv


def monotone_strict(xs):
    vals = [x for x in xs if x is not None]
    return len(vals) == len(xs) and all(b < a for a, b in zip(vals, vals[1:]))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    print("=" * 92)
    print("A. TEL QUEL — poids_memoire 0.85 / 0.60 / 0.35, decay 0.90, graine 42")
    print("   (le constructeur renormalise : baisser la mémoire fait monter les pénalités)")
    print("=" * 92)
    tel_quel = []
    for w in (0.85, 0.60, 0.35):
        g = MOD.AdvancedBGate(poids_memoire=w, memoire_decay=0.90)
        p = f"{g.poids_memoire:.3f}/{g.poids_redondance:.3f}/{g.poids_cout:.3f}"
        tel_quel.append(rapport(f"poids_memoire={w:.2f}", g, p))

    print("\n" + "=" * 92)
    print("B. DÉCONFONDU — poids normalisés écrits à la main, sans renormalisation")
    print("   seule l'amplitude varie ; redondance et coût restent 0.10 / 0.05")
    print("=" * 92)
    deconfondu = []
    for w in (0.85, 0.60, 0.35):
        g = MOD.AdvancedBGate(memoire_decay=0.90)
        g.poids_memoire = w
        g.poids_redondance = 0.10
        g.poids_cout = 0.05
        deconfondu.append(rapport(f"poids_memoire={w:.2f}", g, "écrits directement"))

    print("\n" + "=" * 92)
    print("VERDICT — critère demandé : « drops monotonically » (décroissance stricte)")
    print("=" * 92)
    print(f"  tel quel   : réouvertures {tel_quel} → monotone ? {monotone_strict(tel_quel)}")
    print(f"  déconfondu : réouvertures {deconfondu} → monotone ? {monotone_strict(deconfondu)}")
    print("\n  Analytique : à p = 0, réouverture si w_m·m + 0,05·(w_r + w_c) < 0,15 ;")
    print("  la trajectoire de m vaut 0,588 · 0,90^n et NE DÉPEND PAS des poids ;")
    print("  seuls les seuils sur m en dépendent : 0,1676 / 0,175 / 0,1929 → 12 / 12 / 11 cycles.")
    print("  Fermeture : w_m·m + 0,35·w_r + 0,25·w_c > 0,45. Au poids 0,60 sans")
    print("  renormalisation, le maximum atteint est 0,40 : la membrane ne se ferme jamais.")
    print("\n  Conclusion : l'amplitude ne règle pas la DURÉE de la cicatrice, elle règle")
    print("  son EXISTENCE. La durée n'est définie que si la fermeture a lieu.")
