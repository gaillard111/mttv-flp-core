# Reproducible benchmark — the teeth

> EN · CC0 · `sig:0x4D5454562D464C50`

One click, pure stdlib: `python benchmark/benchmark_mpvr.py` (or paste into a Colab cell).

**Protocol** : fixed seed (42), N = 7, **paired comparison** (the same draws are served to both strategies), fault injection 15 / 30 / 40 % node loss. Majority vote vs porous MPVR quorum.

**Measured** : success rate, energy units, latency.

**Result (honest)** : energy economy **24–41 %**, better success under stress, latency roughly halved. The porous threshold is lower (3 vs 4) — the methodology states it openly.

Files : `benchmark/benchmark_mpvr.py` · results : `benchmark/benchmark_mpvr_results.json`.

C'est un **capteur de preuve** — mesurez, ne croyez pas.

🌱 **Pousses associées :**
- [02_quorum_poreux.md](02_quorum_poreux.md)
- [08_graft_catalog.md](08_graft_catalog.md)
