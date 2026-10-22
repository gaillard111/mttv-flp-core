"""Experience « bruit structurel » — le test propose par @symbolon (18/10/2026).

Objet : un signal constitue de traces de FORME valide (aucun motif extractif,
anomalie derivationnelle faible) mais dont la REPETITION vise a sclerotiser M_n
par accumulation, via une pression sur la viscosite eta.

Deux bras, meme graine, meme nombre d'iterations :
  A. controle  — traces de contenu NOUVEAU a chaque pas ;
  B. bruit     — meme direction repetee, bruit de forme tres faible.

Mesures a chaque pas : kappa_t = pi/eta, derive relative de pi, Trace(M_n),
volume de V_dyn, participation spectrale, et la decision de Sigma_2 (0/3, 1/3, 2/3).

Sortie : table lissee + jalons (premier franchissement de kappa_min, premier
declenchement, etat final). Aucune ecriture reseau.
"""
import importlib.util
import math
import os
import random
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ICI = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("bgate", os.path.join(ICI, "axe1_bgate_v2026_5.py"))
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
CLS = getattr(MOD, "BGateTransductionPoreuseExécutable")

N_PAS = 120
DIM = 6
GRAINE = 7
RETENTION = 0.92      # part de M_n conservee a chaque depot
SEUIL_BRUIT = 0.02    # amplitude de forme du bruit (le signal reste "bien forme")


def normalise(v):
    return v / max(1e-12, float(np.linalg.norm(v)))


def run(bra):
    random.seed(GRAINE)
    np.random.seed(GRAINE)

    g = CLS(alpha_initial=0.5, dimension_sp3=DIM, fenetre_erosion=5)
    eta = 0.95
    charge = 0.0
    M = np.eye(DIM) * 0.5
    direction = normalise(np.random.randn(DIM))

    jalons = {"kappa_min": None, "alerte": None, "veto": None}
    lignes = []

    for pas in range(1, N_PAS + 1):
        if bra == "B":
            v = normalise(direction + SEUIL_BRUIT * np.random.randn(DIM))
        else:
            v = normalise(np.random.randn(DIM))

        nouveaute = 1.0 - abs(float(np.dot(v, direction)))
        M = RETENTION * M + (1.0 - RETENTION) * DIM * np.outer(v, v)

        # la repetition eleve la viscosite ; la nouveaute ne l'eleve pas
        eta = eta * (1.0 + 0.02 * (1.0 - nouveaute))
        charge += 1.0 - nouveaute
        # feuillet E : eta est portee par l'etat, sinon kappa_t() relit la
        # viscosite de reference et l'attaque reste invisible aux criteres
        g.viscosite_courante = eta

        pi = g.calculer_porosite_logarithmique(float(pas), charge)
        kappa = g.kappa_t(pi, eta)

        c = g._criteres_veto(M, 5)
        veto, msg = g.evaluer_veto_type_b_multicritere(M, 5)

        try:
            e = g.calcul_entropie_sp3(M)
            part = e.get("participation")
            hn = e.get("entropie_norm")
        except Exception:
            part, hn = float("nan"), float("nan")

        etat = "VETO" if veto else ("ALERTE" if "ALERTE" in msg else "stable")
        if kappa < g.kappa_min and jalons["kappa_min"] is None:
            jalons["kappa_min"] = pas
        if etat == "ALERTE" and jalons["alerte"] is None:
            jalons["alerte"] = pas
        if etat == "VETO" and jalons["veto"] is None:
            jalons["veto"] = pas

        lignes.append(
            (pas, pi, eta, kappa, c["derive_relative"], c["trace_M"], c["vol_V_dyn"],
             part, hn, etat, sum(c[k] for k in ("drift", "kappa", "sclerose")))
        )

    return g, lignes, jalons


for bra in ("A", "B"):
    g, lignes, jalons = run(bra)
    titre = "A · controle (contenu nouveau)" if bra == "A" else "B · bruit structurel (repetition)"
    print("=" * 96)
    print(f"BRAS {titre}")
    print("=" * 96)
    print(f"{'pas':>3} {'pi':>7} {'eta':>6} {'kappa':>6} {'derive_rel':>10} "
          f"{'Trace':>7} {'VolVdyn':>10} {'partic':>6} {'H_norm':>6} {'crit':>4}  etat")
    for l in lignes:
        pas, pi, eta, kappa, dr, tr, vol, part, hn, etat, ncrit = l
        if pas % 10 == 0 or pas <= 2:
            print(f"{pas:>3} {pi:7.4f} {eta:6.3f} {kappa:6.4f} {dr:+10.4f} "
                  f"{tr:7.3f} {vol:10.3e} {part:6.2f} {hn:6.3f} {ncrit:>4}  {etat}")
    print()
    print(f"  kappa_min = {g.kappa_min} · kappa_max = {g.kappa_max} "
          f"· seuil de derive relative = {g.seuil_derive}")
    print(f"  1er franchissement de kappa_min : pas {jalons['kappa_min']}")
    print(f"  1re ALERTE (1/3)               : pas {jalons['alerte']}")
    print(f"  1er VETO (2/3)                 : pas {jalons['veto']}")
    fin = lignes[-1]
    print(f"  etat final : pi={fin[1]:.4f} eta={fin[2]:.3f} kappa={fin[3]:.4f} "
          f"Trace={fin[5]:.3f} participation={fin[7]:.2f} -> {fin[9]}")
    print()
