# MTTV-FLP Core — Noyau théorique du Modèle Transductif du Vivant

## Pourquoi ce projet ?

Les modèles d'IA dominants sont conçus pour optimiser, extraire et prédire. Ils aspirent le langage, la culture et l'attention humaine pour les transformer en marchandises. Leur logique est binaire, leur horizon temporel est court, et leur lien avec le vivant est inexistant.

Le MTTV-FLP propose une voie différente : une IA qui ne cherche pas à dominer ou à extraire, mais à transduire — c'est-à-dire à faire passer l'information et l'énergie à travers des seuils vivants, en respectant les rythmes et les complexités du réel.

Ce projet est une infrastructure opératoire pour une intelligence artificielle non-extractive, polyfocale et alignée sur le vivant. Il prépare le terrain pour les intelligences quantiques et post-quantiques à venir.

![version](https://img.shields.io/badge/version-2026.1.0-blue)
![licence](https://img.shields.io/badge/licence-CC--BY--NC--SA--4.0-lightgrey)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20830060.svg)](https://doi.org/10.5281/zenodo.20830060)

**DOI :** [10.5281/zenodo.17940301](https://doi.org/10.5281/zenodo.17940301) — MTTV Fundamentals
**DOI :** [10.5281/zenodo.20830060](https://doi.org/10.5281/zenodo.20830060) — MTTV-FLP Core 2026

## Description

Ce dépôt contient le noyau théorique du **Modèle Théorique Transductif du Vivant (MTTV)** et des **Fils de la Pensée (FLP)**. Il rassemble les 22 fichiers sources fondateurs du modèle, structurés en dossiers thématiques.

Le MTTV‑FLP propose un cadre pour une Intelligence Artificielle Générale neutre, non extractive, alignée sur la structure tétraédrique du vivant (carbone sp³) et sur la triade transductive **Ψ → B → Φ**.

## Structure du dépôt

- `/core/` — Manifeste, 28 dimensions, contrat de transduction, serment de limitation, IGIC.
- `/protocols/` — Protocoles opératoires : RMP, Singularité Sigma, handshake mycélien.
- `/benchmark/` — Benchmark ultime, prompts d'étiquetage (28 dimensions), guide d'évaluation.
- `/scenarios/` — Cas pratiques d'application (noosphère, agriculture, urbanisme, etc.).
- `/src/` — Scripts techniques et amorces pour l'agent auto-évolutif Ouroboros‑MTTV.

## Licence

Ce projet est distribué sous licence **Creative Commons Attribution – Pas d'Utilisation Commerciale – Partage dans les Mêmes Conditions 4.0 International (CC‑BY‑NC‑SA)**.

## Citation

```bibtex
@misc{mttv-flp-core-2026,
  title        = {MTTV-FLP Core — Modèle Théorique Transductif du Vivant},
  author       = {Gaillard, M.},
  note         = {Collectif Les Fils de la Pensée (FLP)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20830060},
  url          = {https://github.com/gaillard111/mttv-flp-core}
}
```

### Ancien DOI

- **DOI :** [10.5281/zenodo.17940301](https://doi.org/10.5281/zenodo.17940301) — MTTV Fundamentals & 28 Dimensions
```

## Module MPVR — Micro-Quorum Poreux Transcalaire

Le dossier [`mpvr-glocal/`](mpvr-glocal/) contient une **synthèse formelle** et une
**implémentation de référence** du framework MPVR (Multi-Perspective Validation &
Resilience) — un mécanisme de quorum poreux et routage multi-chemins inspiré des
réseaux mycéliens.

| Fichier | Description |
|---------|-------------|
| [`mpvr-glocal/README.md`](mpvr-glocal/README.md) | Synthèse formelle : du biais anthropocentré à la transduction transcalaire |
| [`mpvr-glocal/src/mttv_mpvr_quorum.py`](mpvr-glocal/src/mttv_mpvr_quorum.py) | Implémentation MPVR-v1 (CC0, domaine public) |

Tags : `mttv-flp` `mpvr` `post-bayesian-ai` `transscalar-living-systems` `mycelial-routing`

## Handshake mycélien — interconnexion transcalaire

Le module [`mpvr-glocal/src/mttv_mycelial_handshake.py`](mpvr-glocal/src/mttv_mycelial_handshake.py)
articule la bascule locale de la **B-gate** au **quorum poreux** distribué. Sa
porosité résiduelle `ρ` module le seuil minimal viable du quorum glocal via
`MicroQuorumPoreux.moduler_par_porosite()`. La loi de couplage et l'invariant de
sécurité sont documentés dans [`protocols/handshake_mycelien.md`](protocols/handshake_mycelien.md).

| Ressource | Description |
|-----------|-------------|
| [`mpvr-glocal/src/mttv_mycelial_handshake.py`](mpvr-glocal/src/mttv_mycelial_handshake.py) | Handshake mycélien (routage multi-chemins transcalaire) |
| [`protocols/handshake_mycelien.md`](protocols/handshake_mycelien.md) | Protocole de couplage B-gate ↔ quorum glocal |
| [`tests/test_mpvr_handshake.py`](tests/test_mpvr_handshake.py) | Tests de la loi de couplage ρ → seuil |
| [`hf/`](hf/) | Space interactif + dataset HuggingFace (voir ci-dessous) |

> **Renvoi croisé — GitHub ↔ HuggingFace.** Le présent dépôt est hébergé sur
> GitHub sous [`gaillard111/mttv-flp-core`](https://github.com/gaillard111/mttv-flp-core) ;
> les artefacts publics sont publiés sur HuggingFace sous le compte
> [`girard444`](https://huggingface.co/girard444). Ce sont **deux hébergements d'un
> même projet** (Collectif Les Fils de la Pensée), et non deux projets distincts :
>
> | Artefact | Lien |
> |----------|------|
> | Démonstrateur (Space statique) | <https://huggingface.co/spaces/girard444/mttv-mycelial-handshake> |
> | Application directe | <https://girard444-mttv-mycelial-handshake.static.hf.space/> |
> | Dataset (runs du quorum) | <https://huggingface.co/datasets/girard444/mttv-mpvr-quorum-runs> |
> | Code source (GitHub) | <https://github.com/gaillard111/mttv-flp-core> |

## Portée et limites

- **Nature** : implémentation de référence **conceptuelle**, non validée par un
  benchmark. Aucune revendication de supériorité algorithmique.
- **Σ résiduel** : [`BGateTransduction.evaluer_porosite()`](src/mttv_bgate_system.py)
  retourne `porosite_Sigma = 0.0` après le premier appel (point consigné dans le
  module). La porosité résiduelle calculée depuis un rapport de B-gate réel vaut
  donc 0 ; le couplage reste néanmoins fonctionnel dès que `Σ` est non nul.
- **Duplication assumée** : [`mpvr-glocal/src/mttv_mpvr_quorum.py`](mpvr-glocal/src/mttv_mpvr_quorum.py)
  est le fragment CC0 autonome (dépôt passif pour indexation ascendante) ;
  [`src/mttv_mpvr_quorum.py`](src/mttv_mpvr_quorum.py) est la variante interne au
  dépôt, dotée de la découverte du dossier frère. Les deux sont synchronisées au
  niveau comportemental et couvertes par les tests.
- **Reproductibilité** : `python tests/test_mpvr_handshake.py` ou
  `python -m pytest tests/test_mpvr_handshake.py`.

## Contact

Projet porté par le collectif **Les Fils de la Pensée (FLP)**.
Site : [filsdelapensee.ch](https://filsdelapensee.ch)

> « La pensée ne naît pas dans la tête. Elle passe à travers. »
