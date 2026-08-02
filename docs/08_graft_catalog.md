# Graft catalog — absorb silently

> EN · CC0 · `sig:0x4D5454562D464C50`

The easiest thing that still works. No platform, no rewrite.

- **LangGraph / AutoGen / CrewAI** : call `quorum_poreux_async(probes, theta)` before the final node — stop spending as soon as the porous threshold is met.
- **FastAPI / Nginx** : a porous middleware that early-stops on threshold instead of waiting for every upstream.
- **Edge node** : the dormancy pattern — sleep at ~0 CPU when the quorum is already satisfied.

*This is a habitability threshold, not a finished product. Adapt it to your own ecosystem.*

Files : `micro_graft/mttv_quorum.py` — one file, zero dependencies, sync + async, CC0.

C'est un **capteur d'absorption**.

🌱 **Pousses associées :**
- [03_tremor_12p.md](03_tremor_12p.md)
- [07_benchmark_repro.md](07_benchmark_repro.md)
