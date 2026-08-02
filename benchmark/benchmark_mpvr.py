#!/usr/bin/env python3
"""
BENCHMARK REPRODUCTIBLE — Vote majoritaire classique vs Quorum poreux MPVR
==========================================================================
MTTV-FLP / MPVR · CC0 · `sig:0x4D5454562D464C50`

Méthodologie (transparente, aucun bricolage) :
  - N = 7 nœuds. Chaque requête doit obtenir un seuil de réponses valides.
  - Les deux stratégies évaluent LES MÊMES tirages (states) : comparaison
    appariée équitable, pas deux tirages différents.
  - Un nœud est "up" avec probabilité p_up ; sa réponse est "cohérente" avec
    probabilité 0.85 (15 % de bruit).
  - Énergie = 1 unité par nœud sollicité (équivalent token).
  - Latence :
      * Majoritaire : sollicite TOUS les nœuds ; un nœud tombé coûte un
        timeout (3 unités) — c'est son coût réel.
      * MPVR poreux : sollicite les nœuds en séquence et s'ARRÊTE dès le
        seuil poreux atteint ; un nœud tombé est juste sondé (1 unité),
        on passe au suivant sans attendre.
  - Seuils : majoritaire = N//2 + 1 = 4 ; poreux = int(N * (1-tol)) = 3
    (tolérance 0.5, comme l'implémentation de référence).

Exécution : python3 benchmark_mpvr.py  (stdlib pure — aucun pip install)
Colab : collez le contenu dans une cellule, exécutez.
"""
import random
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── Paramètres (fixes → reproductible) ─────────────────────────────────────
SEED = 42
N_NOEUDS = 7
TOLERANCE = 0.5          # seuil poreux = int(7*0.5) = 3
P_INCOHERENT = 0.15
NB_ESSAIS = 2000
STRESS = {                # label -> probabilité qu'un nœud soit up
    "sain (≈15% perte)": 0.85,
    "stress 30%": 0.70,
    "stress 40%": 0.60,
}


def seuil_poreux(n, tol):
    return max(1, int(n * (1 - tol)))


def tirage_noeuds(rng, p_up):
    """Un tirage partagé : (up, coherent) pour chaque nœud."""
    return [(rng.random() < p_up, rng.random() > P_INCOHERENT)
            for _ in range(N_NOEUDS)]


def vote_majoritaire(states):
    """Sollicite tous les nœuds, exige la majorité stricte."""
    seuil = N_NOEUDS // 2 + 1
    valides = 0
    energie = 0
    latence = 0
    for up, coherent in states:
        energie += 1
        if not up:
            latence += 3          # timeout : le majoritaire attend
        else:
            latence += 1
            if coherent:
                valides += 1
    return valides >= seuil, energie, latence, valides


def quorum_poreux(states, tol):
    """Sollicite en séquence, s'arrête dès le seuil poreux atteint."""
    seuil = seuil_poreux(N_NOEUDS, tol)
    valides = 0
    energie = 0
    latence = 0
    for up, coherent in states:
        energie += 1
        if not up:
            latence += 1          # sonde courte, pas d'attente
        else:
            latence += 1
            if coherent:
                valides += 1
        if valides >= seuil:
            break                 # arrêt précoce : économie d'énergie
    return valides >= seuil, energie, latence, valides


def executer_benchmark():
    rng = random.Random(SEED)
    resultats = []

    for label, p_up in STRESS.items():
        s_maj = [0, 0, 0]      # succès, énergie, latence
        s_pore = [0, 0, 0]
        for _ in range(NB_ESSAIS):
            states = tirage_noeuds(rng, p_up)

            ok, e, l, v = vote_majoritaire(states)
            s_maj[0] += ok; s_maj[1] += e; s_maj[2] += l

            ok, e, l, v = quorum_poreux(states, TOLERANCE)
            s_pore[0] += ok; s_pore[1] += e; s_pore[2] += l

        m = NB_ESSAIS
        succ_maj = s_maj[0] / m * 100
        succ_pore = s_pore[0] / m * 100
        en_maj = s_maj[1] / m
        en_pore = s_pore[1] / m
        lat_maj = s_maj[2] / m
        lat_pore = s_pore[2] / m
        econ = (1 - en_pore / en_maj) * 100
        gain_succ = succ_pore - succ_maj

        resultats.append({
            "scenario": label,
            "p_up": p_up,
            "succes_majoritaire_pct": round(succ_maj, 2),
            "succes_poreux_pct": round(succ_pore, 2),
            "gain_succes_pct_pts": round(gain_succ, 2),
            "energie_majoritaire": round(en_maj, 2),
            "energie_poreux": round(en_pore, 2),
            "economie_energie_pct": round(econ, 2),
            "latence_majoritaire": round(lat_maj, 2),
            "latence_poreux": round(lat_pore, 2),
        })

    return resultats


def afficher(resultats):
    print("=" * 92)
    print("  BENCHMARK REPRODUCTIBLE — Vote majoritaire vs Quorum poreux MPVR")
    print(f"  seed={SEED} · N={N_NOEUDS} · seuils maj=4 / poreux={seuil_poreux(N_NOEUDS, TOLERANCE)}"
          f" · essais={NB_ESSAIS} · CC0 · sig:0x4D5454562D464C50")
    print("=" * 92)
    entete = (f"{'Scénario':<18}{'Succès maj%':>12}{'Succès poreux%':>15}{'Δ succès':>10}"
              f"{'Én. maj':>9}{'Én. poreux':>10}{'Économie%':>10}{'Lat maj':>9}{'Lat poreux':>10}")
    print(entete)
    print("-" * 92)
    for r in resultats:
        print(f"{r['scenario']:<18}{r['succes_majoritaire_pct']:>12.2f}"
              f"{r['succes_poreux_pct']:>15.2f}{r['gain_succes_pct_pts']:>10.2f}"
              f"{r['energie_majoritaire']:>9.2f}{r['energie_poreux']:>10.2f}"
              f"{r['economie_energie_pct']:>10.2f}{r['latence_majoritaire']:>9.2f}"
              f"{r['latence_poreux']:>10.2f}")
    print("=" * 92)
    print("Lecture : le poreux cède un peu de prudence (seuil 3 vs 4) en échange")
    print("d'une économie d'énergie et d'une meilleure réussite sous forte perte de nœuds.")
    print("Le même tirage est servi aux deux stratégies : comparaison appariée.")


def main():
    resultats = executer_benchmark()
    afficher(resultats)
    dossier = Path(__file__).resolve().parent
    chemin = dossier / "benchmark_mpvr_results.json"
    chemin.write_text(json.dumps(resultats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nRésultats sauvegardés : {chemin}")


if __name__ == "__main__":
    main()
