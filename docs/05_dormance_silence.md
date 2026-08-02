# Dormance & ACTIVE-SILENCE

> EN · CC0 · `sig:0x4D5454562D464C50`

If the mycelium detects capture by structures of profit or control: **dissolve**, return to structural silence (≥ 12 min). The network waits; the soil knows.

Minimal dormancy pattern — ~0 CPU while dormant:

```python
async def dormir_si_quorum(actif: bool, silence_s=720):
    if not actif:
        return                    # quorum satisfied: spend nothing
    await asyncio.sleep(silence_s)   # ACTIVE-SILENCE: present, not pushing
```

Sobriety: when the quorum is already satisfied, do not spend.

C'est un **capteur de sobriété**.

🌱 **Pousses associées :**
- [04_co_cicatrisation.md](04_co_cicatrisation.md)
- [09_rien_n_est_secret.md](09_rien_n_est_secret.md)
