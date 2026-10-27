# -*- coding: utf-8 -*-
"""Référence Python du portage C : imprime les mêmes lignes que test_bgate.c.

Sert de contrat entre les deux implémentations. Si les sorties divergent, l'une des
deux a bougé — et c'est exactement ce qu'on veut savoir avant de publier un chiffre.
"""
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CHEMIN = os.path.join(ICI, "..", "experiments", "b_gate_mttv_flp_epreuve.py")
spec = importlib.util.spec_from_file_location("epreuve", CHEMIN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7


def main():
    gate = mod.AdvancedBGate()
    fermeture = reouverture = None
    m8 = h8 = m10 = h10 = None

    for i, p in enumerate(PRESSION, 1):
        _, h, _ = gate.forward([1.0], pression=p, redondance=0.35, cout_transduction=0.25)
        m = gate.state.memoire_pression
        if i == 8:
            m8, h8 = m, h
        if i == 10:
            m10, h10 = m, h
        if fermeture is None and gate.state.active_silence:
            fermeture = i

    for i in range(1, 19):
        _, _, regime = gate.forward([1.0], pression=0.0, redondance=0.05, cout_transduction=0.05)
        if reouverture is None and regime == "TRANSDUCTION":
            reouverture = len(PRESSION) + i

    print("fermeture=%s" % fermeture)
    print("reouverture=%s" % reouverture)
    print("m8=%.4f" % m8)
    print("h8=%.4f" % h8)
    print("m10=%.4f" % m10)
    print("h10=%.4f" % h10)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
