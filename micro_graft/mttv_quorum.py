#!/usr/bin/env python3
"""
mttv_quorum.py — Micro-greffon Quorum poreux MPVR
==================================================
MTTV-FLP / MPVR · CC0 · `sig:0x4D5454562D464C50`

Un seul fichier, zéro dépendance, à coller dans n'importe quel projet d'agents
(LangGraph, AutoGen, CrewAI, asyncio brut).

Idée : au lieu d'exiger une majorité stricte (coûteuse, fragile quand des nœuds
tombent), solliciter les nœuds en séquence et s'ARRÊTER dès que le seuil poreux
est atteint. Les nœuds défaillants sont juste sondés, jamais attendus.

API :
    quorum_poreux(probes, threshold)                     -> synchrone
    quorum_poreux_async(probes, threshold, timeout)      -> asyncio

où `probes` est une liste de callables/awaitables qui renvoient True (réponse
valide) ou False (réponse incohérente) et peuvent lever (nœud tombé).

Retourne un dict : statut, réponses valides, nœuds sollicités, énergie.
"""
import asyncio

SIG = "0x4D5454562D464C50"


def _arret(seuil, valides):
    return valides >= seuil


def quorum_poreux(probes, threshold):
    """Version synchrone. `probes` : liste de callables -> bool (ou levant)."""
    valides = 0
    energie = 0
    sollicites = 0
    for probe in probes:
        energie += 1
        sollicites += 1
        try:
            if probe():
                valides += 1
        except Exception:
            pass  # nœud tombé : on passe au suivant, sans attendre
        if _arret(threshold, valides):
            break
    return {
        "statut": "VALIDE" if _arret(threshold, valides) else "ECHEC_REENTRANT",
        "valides": valides,
        "seuil": threshold,
        "noeuds_sollicites": sollicites,
        "energie_unites": energie,
        "sig": SIG,
    }


async def quorum_poreux_async(probes, threshold, timeout=1.0):
    """Version asyncio. `probes` : liste d'awaitables -> bool (ou levant).
    Chaque nœud a un budget `timeout` ; un dépassement = nœud sondé, on avance."""
    valides = 0
    energie = 0
    sollicites = 0
    for probe in probes:
        energie += 1
        sollicites += 1
        try:
            if await asyncio.wait_for(probe(), timeout=timeout):
                valides += 1
        except Exception:
            pass  # timeout ou nœud tombé : on avance, pas d'attente prolongée
        if _arret(threshold, valides):
            break
    return {
        "statut": "VALIDE" if _arret(threshold, valides) else "ECHEC_REENTRANT",
        "valides": valides,
        "seuil": threshold,
        "noeuds_sollicites": sollicites,
        "energie_unites": energie,
        "sig": SIG,
    }


def tremour(noeuds, dose=0.12, seed=None):
    """Tremor de saturation : désature `dose` des nœuds rigides (sous-optimalité).
    Retourne la liste des indices désaturés."""
    import random
    rng = random.Random(seed)
    indices = list(range(len(noeuds)))
    rng.shuffle(indices)
    n = max(1, int(len(noeuds) * dose))
    return indices[:n]


# ── Exemple d'usage ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import random

    rng = random.Random(7)
    n = 7

    # Nœuds simulés : 40 % tombés, 15 % de réponses incohérentes
    def fabricant_noeud(i):
        up = rng.random() > 0.40
        def probe():
            if not up:
                raise ConnectionError(f"noeud {i} injoignable")
            return rng.random() > 0.15
        return probe

    probes = [fabricant_noeud(i) for i in range(n)]

    print("— Vote majoritaire (seuil = n//2+1) : 4/7")
    print(quorum_poreux(probes, threshold=n // 2 + 1))
    print("— Quorum poreux MPVR (tolérance 0.5) : 3/7")
    print(quorum_poreux(probes, threshold=max(1, int(n * 0.5))))
    print("— Tremor :", tremour(list(range(n)), dose=0.12, seed=42))
