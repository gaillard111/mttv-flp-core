---
license: cc-by-nc-sa-4.0
language:
  - fr
pretty_name: MTTV-FLP — MPVR Quorum Coupling Runs
tags:
  - mttv-flp
  - mpvr
  - mycelial-routing
  - post-bayesian-ai
  - transscalar-living-systems
  - synthetic
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/mttv_mpvr_runs.csv
---

# MTTV-FLP — MPVR Quorum Coupling Runs

Jeu de données **synthétique** décrivant la loi de couplage transcalaire du
modèle MTTV-FLP : la **porosité résiduelle** ρ calculée par le handshake mycélien
module le **seuil minimal viable** du quorum poreux glocal.

## Origine

Généré de façon déterministe (graine `20260101`) par
`generate_runs.py`, sans accès réseau, à partir de l'implémentation de référence :

- `MycelialHandshake.propager_transduction()` — routage multi-chemins (hyphes).
- `MicroQuorumPoreux.moduler_par_porosite()` — loi de couplage ρ → tolérance.

Code source : <https://github.com/gaillard111/mttv-flp-core>

> **Renvoi croisé.** Le dépôt GitHub est sous le compte `gaillard111`, la
> publication HuggingFace sous le compte `girard444` : ce sont **deux hébergements
> d'un même projet** (Collectif Les Fils de la Pensée). Démonstrateur associé :
> [Space `mttv-mycelial-handshake`](https://huggingface.co/spaces/girard444/mttv-mycelial-handshake)
> — application directe : <https://girard444-mttv-mycelial-handshake.static.hf.space/>.

## Schéma

| Colonne | Type | Description |
|---|---|---|
| `run_id` | int | Identifiant de la transduction |
| `noeuds_quorum` | int | Nombre de nœuds du réseau |
| `extraction` | float | Tension d'extraction soumise à la B-gate |
| `bgate_activation` | bool | B-gate activée (extraction > 0.25) |
| `porosite_sigma` | float | Porosité Σ fournie au handshake |
| `bios` | float | Valeur du pôle Bios (B) |
| `metrique_quorum` | float | Moyenne de résonance du réseau |
| `porosite_residuelle` | float | ρ = métrique × Σ |
| `tolerance_effective` | float | Tolérance de panne modulée |
| `seuil_minimal_viable` | int | Seuil recalculé du quorum |
| `statut_quorum` | str | `VALIDE` ou `ECHEC_REENTRANT` |
| `noeuds_sollicites` | int | Nœuds effectivement sollicités |
| `economie_energie_pct` | str | Économie d'énergie mesurée |

## Loi de couplage

```
tolérance_effective = clamp( 0.5 + (ρ − 0.5) · 1.0 , 0 , 1 )
seuil_minimal_viable = ⌊ noeuds · (1 − tolérance_effective) ⌋
```

À ρ = 0.5, le quorum retrouve son comportement d'origine (rétrocompatibilité).

## Limites

- Données **synthétiques** : elles illustrent une loi de couplage, elles ne
  constituent pas une validation empirique du modèle.
- `porosite_sigma` est fournie explicitement car l'implémentation courante de la
  B-gate ramène Σ à 0 après normalisation (limitation documentée dans le dépôt).

## Licence

CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
