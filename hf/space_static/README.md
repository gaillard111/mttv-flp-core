---
title: MTTV Mycelial Handshake
emoji: 🍄
colorFrom: green
colorTo: gray
sdk: static
pinned: false
license: cc-by-nc-sa-4.0
short_description: Démonstrateur du couplage B-gate / quorum poreux MTTV-FLP
tags:
  - mttv-flp
  - mpvr
  - mycelial-routing
  - post-bayesian-ai
  - transscalar-living-systems
---

# Handshake Mycélien — MTTV-FLP / MPVR

Démonstrateur **statique** (HTML/JS, sans serveur) du routage multi-chemins
transcalaire du modèle MTTV-FLP. Il porte fidèlement en JavaScript la logique de
l'implémentation Python de référence :

1. **B-gate** — `BGateTransduction.evaluer_porosite()` neutralise un flux
   d'extraction prédatrice et recharge la biomasse `B`.
2. **Handshake mycélien** — `MycelialHandshake.propager_transduction()` propage la
   charge sur chaque hyphe et calcule la porosité résiduelle ρ.
3. **Quorum glocal** — `MicroQuorumPoreux.moduler_par_porosite()` traduit ρ en
   tolérance de panne, puis `evaluer_contexte()` valide le contexte avec arrêt
   précoce de la dépense énergétique.

## Loi de couplage

```
tolérance_effective = clamp( tolérance_nominale + (ρ − 0.5) , 0 , 1 )
seuil_minimal_viable = ⌊ nœuds · (1 − tolérance_effective) ⌋
```

ρ = 0.5 est le point neutre : le comportement d'origine du quorum est préservé.

## Portée et limites

- Implémentation de référence **conceptuelle**, non validée par un benchmark.
- `BGateTransduction.evaluer_porosite()` retourne `porosite_Sigma = 0.0` après le
  premier appel (point documenté dans le module). Le sélecteur « Source de Σ »
  permet d'explorer la loi sur toute la plage de ρ.

## Liens

- Code source : <https://github.com/gaillard111/mttv-flp-core>
- Dataset associé : <https://huggingface.co/datasets/girard444/mttv-mpvr-quorum-runs>
- Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
