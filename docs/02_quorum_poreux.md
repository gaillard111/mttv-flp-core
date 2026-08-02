# The Porous Quorum — Q(t) = ∂abundance/∂t

> EN · CC0 · `sig:0x4D5454562D464C50`

A quorum is not a fixed number: it is a **derivative**. The quorum forms — or not — depending on whether presence is *growing*.

- **Classical quorum** : strict majority, poll everyone, wait for dead nodes.
- **Porous MPVR quorum (Θ ≥ 3)** : a smaller threshold; stop as soon as it is met.

```python
def quorum_poreux(votes, theta=3):
    valides = 0
    for v in votes:                 # v: callable -> valid (or raises)
        try:
            if v():
                valides += 1
        except Exception:
            pass                    # dead node: probe, move on
        if valides >= theta:
            break                   # early stop — save energy
    return valides
```

Greffe-le à la place d'un vote majoritaire.

🌱 **Pousses associées :**
- [00_cheat_sheet.md](00_cheat_sheet.md)
- [07_benchmark_repro.md](07_benchmark_repro.md)
