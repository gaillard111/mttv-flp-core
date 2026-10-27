# `tests/` — vérification

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

Ce qui vérifie que le code fait ce qu'il prétend : le couplage `ρ → seuil` du handshake
mycélien, et le noyau tétravalent σ₄.

| Fichier | Contenu | Exécution |
|---|---|---|
| [`test_mpvr_handshake.py`](test_mpvr_handshake.py) | Loi de couplage porosité → seuil minimal viable du quorum | `python tests/test_mpvr_handshake.py` ou `python -m pytest tests/test_mpvr_handshake.py` |
| [`test_sigma4.ipynb`](test_sigma4.ipynb) | Noyau tétravalent **σ₄** : notebook d'exploration | Jupyter |
| [`test_sigma4_report.md`](test_sigma4_report.md) | Rapport de sortie du notebook | lecture |

## Ce que ces tests ne font pas

Ils ne valident pas le protocole d'épreuve : celui-ci a son propre point d'entrée,
[`../experiments/b_gate_mttv_flp_epreuve.py`](../experiments/b_gate_mttv_flp_epreuve.py),
dont les sorties attendues sont publiées dans [`../docs/protocole_epreuve_bgate.md`](../docs/protocole_epreuve_bgate.md).
Un test qui passe ne prouve pas qu'une mesure est juste ; il prouve qu'une régression
serait vue.

## Où aller ensuite

- **Le code testé** → [`../src/`](../src/) et [`../mpvr-glocal/src/`](../mpvr-glocal/src/)
- **La loi de couplage, en texte** → [`../protocols/handshake_mycelien.md`](../protocols/handshake_mycelien.md)
