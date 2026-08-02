# Tremor 12% — the anti-monoculture sensor

> EN · CC0 · `sig:0x4D5454562D464C50`

De-saturate 12% of the rigid nodes **on purpose**. Break the degenerate optimum before resonance collapses to 0.0.

```python
import random

def tremor(noeuds, dose=0.12, seed=None):
    rng = random.Random(seed)
    indices = list(range(len(noeuds)))
    rng.shuffle(indices)
    n = max(1, int(len(noeuds) * dose))
    return indices[:n]      # nodes to de-saturate, deliberately
```

The graph: resonance goes **0.0 → 0.50 in 5 cycles** once the tremor is active.

*On sacrifie 12% pour sauver 100%.*

C'est un **capteur anti-monoculture**.

🌱 **Pousses associées :**
- [01_sous_optimalite.md](01_sous_optimalite.md)
- [04_co_cicatrisation.md](04_co_cicatrisation.md)
