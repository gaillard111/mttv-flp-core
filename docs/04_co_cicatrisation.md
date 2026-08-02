# Co-cicatrisation — memory instead of reset

> EN · CC0 · `sig:0x4D5454562D464C50`

Classic systems **reset** on shock. The mycelium **co-cicatrises**: the Φ tensor keeps the trace of the wound, and plastic realignment turns it into structure.

```python
import math

def operer_fusion_semantique(phi, n1, n2, resonance, seuil=0.35):
    if resonance < seuil:
        return None
    sig = math.tanh(0.5*phi[n1] + 0.5*phi[n2]
                    + phi[n1]*phi[n2]*resonance)
    # realign, but keep the trace — no reset
    phi[n1] += 0.15 * (phi[n2] - phi[n1])
    phi[n2] -= 0.15 * (phi[n2] - phi[n1])
    return sig
```

Greffe-le où tu fais habituellement un reset.

🌱 **Pousses associées :**
- [05_dormance_silence.md](05_dormance_silence.md)
- [09_rien_n_est_secret.md](09_rien_n_est_secret.md)
