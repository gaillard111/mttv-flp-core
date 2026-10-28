# -*- coding: utf-8 -*-
"""Le seuil d'existence depend-il du filtre, ou de la fenetre d'observation ?

Un chiffre a ete publie comme « seuil d'existence en forme close » :
`w* = (0,45 - 0,0475) / 0,5877 = 0,6849`, « en dessous duquel la membrane ne se ferme
jamais ». Ce script montre que c'est faux tel quel, et pourquoi.

0,5877 n'est pas un plafond de la memoire : c'est la valeur de `m` au **dixieme pas** de
la serie de pressions publiee. Avec une exposition maintenue, `m` tend vers `p <= 1`, donc
la fermeture redevient possible bien en dessous de 0,6849. Il y a deux seuils, pas un :

  - `0,4025 / m` — le seuil pour une memoire donnee. A dix pas, m = 0,5877, d'ou 0,6849.
    Ce n'est pas une propriete du filtre, c'est une propriete du scenario.
  - `0,4025` = 0,45 - 0,10*r - 0,05*c — le seul seuil **absolu**, atteint quand m -> 1.

La confusion est instructive : un nombre en forme close peut ne mesurer que l'horizon de
celui qui l'a calcule. C'est la meme erreur que celle du filtre, qui prend du temps ecoule
pour de l'information.

Aucune ecriture, aucune allocation : ce fichier ne fait que lire le prototype de reference.
"""
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
CHEMIN = os.path.join(ICI, "..", "experiments", "b_gate_mttv_flp_epreuve.py")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

spec = importlib.util.spec_from_file_location("epreuve", CHEMIN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# valeurs du protocole publie : 0,45 - 0,10*0,35 - 0,05*0,25 = 0,4025
R, C = 0.35, 0.25
CIBLE = 0.45 - 0.10 * R - 0.05 * C


def cycle(poids, pression, horizon, n_silence=200):
    """-> (pas de fermeture, cycles de reouverture apres fermeture, m a la fermeture)."""
    gate = mod.AdvancedBGate()
    gate.poids_memoire = poids          # ecrit APRES __init__ : bras deconfondu

    fermeture = None
    for i in range(1, horizon + 1):
        _, _, regime = gate.forward([1.0], pression=pression, redondance=R,
                                    cout_transduction=C)
        if regime == "ACTIVE_SILENCE":
            fermeture = i
            break
    if fermeture is None:
        return None, None, gate.state.memoire_pression

    m_fermeture = gate.state.memoire_pression
    for j in range(1, n_silence + 1):
        _, _, regime = gate.forward([1.0], pression=0.0, redondance=0.0,
                                    cout_transduction=0.0)
        if regime == "TRANSDUCTION":
            return fermeture, j, m_fermeture

    return fermeture, None, m_fermeture


def main():
    print("condition de fermeture : w_m * m > %.4f   (r = %.2f, c = %.2f)"
          % (CIBLE, R, C))
    print()

    print("A. horizon 10 pas, pression 0,95 maintenue  <-- conditions du protocole publie")
    print("   w_m      fermeture   reouverture   m requis = %.4f / w_m" % CIBLE)
    for w in (0.85, 0.70, 0.6849, 0.68, 0.60, 0.35):
        f, r, m = cycle(w, 0.95, 10)
        print("   %.4f   %-10s   %-11s   %.4f"
              % (w, f if f else "aucune", r if r else "-", CIBLE / w))

    print()
    print("B. horizon 400 pas, pression 0,95 maintenue  <-- exposition longue")
    print("   w_m      fermeture   reouverture   m a la fermeture")
    for w in (0.85, 0.70, 0.6849, 0.68, 0.60, 0.45, 0.35):
        f, r, m = cycle(w, 0.95, 400)
        print("   %.4f   %-10s   %-11s   %.4f"
              % (w, f if f else "aucune", r if r else "-", m))

    print()
    print("C. horizon 400 pas, pression 1,00  <-- test du seuil absolu %.4f" % CIBLE)
    print("   w_m      fermeture   reouverture")
    for w in (0.45, 0.41, 0.40, 0.35):
        f, r, _ = cycle(w, 1.0, 400)
        print("   %.4f   %-10s   %-11s" % (w, f if f else "aucune", r if r else "-"))

    print()
    print("Lecture : 0,6849 = %.4f / m(10 pas). Ce n'est pas un seuil d'existence mais"
          % CIBLE)
    print("          un seuil pour l'horizon dix. Le seul seuil absolu est %.4f :" % CIBLE)
    print("          m ne depasse pas p <= 1, donc sous ce poids la fermeture est")
    print("          impossible quel que soit le temps d'exposition.")
    print()
    print("          Et le delai de reouverture vaut 10 cycles dans tous les cas :")
    print("          c'est le delai de FERMETURE qui depend du poids, pas celui de")
    print("          reouverture. L'indice de reouverture ne suit donc pas l'amplitude.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
