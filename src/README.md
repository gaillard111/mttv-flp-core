# `src/` — implémentations internes

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

Scripts techniques et amorces pour l'agent auto-évolutif **Ouroboros-MTTV**. C'est ici
qu'on entre si l'on veut lire une implémentation **sans** les PDF ni la théorie.

| Fichier | Contenu | Relation |
|---|---|---|
| [`mttv_bgate_system.py`](mttv_bgate_system.py) | B-gate : `BGateTransduction`, évaluation de porosité, veto | copie identique dans [`../hf/space/`](../hf/space/) — contrôlée par [`../tools/verifier_depot.py`](../tools/verifier_depot.py) |
| [`mttv_mpvr_quorum.py`](mttv_mpvr_quorum.py) | Variante **interne** du quorum poreux, avec découverte du dossier frère | **diffère** de [`../mpvr-glocal/src/mttv_mpvr_quorum.py`](../mpvr-glocal/src/mttv_mpvr_quorum.py), qui est le fragment CC0 autonome. La différence est assumée et vérifiée |

## Le point `Σ` résiduel, à connaître avant de lire

`BGateTransduction.evaluer_porosite()` retourne `porosite_Sigma = 0.0` **après le
premier appel**. La porosité résiduelle calculée depuis un rapport de B-gate réel vaut
donc 0 ; le couplage reste fonctionnel dès que `Σ` est non nul. C'est une limite
documentée, pas un bug caché — elle figure aussi dans le README du dépôt.

## Où aller ensuite

- **Le code mesurable** (celui qui publie des chiffres) → [`../experiments/README.md`](../experiments/README.md)
- **Le veto multi-critères exécutable** → [`../expansion_v2026.5/axe1_bgate_v2026_5.py`](../expansion_v2026.5/axe1_bgate_v2026_5.py)
- **Les tests** → [`../tests/README.md`](../tests/README.md)
