# SOPH-IA v2.0 — Ethical Friction Teaser Dataset

**Sub-Optimal Paradigm for Habitable AI and the Thermodynamics of Algorithmic Ethical Friction**

**Author:** M. Gaillard (Research Coordination)

## Overview

SOPH-IA introduces a sub-optimal paradigm for AI alignment where global habitability is achieved through documented, reversible local sacrifice (6/7). This repository contains the teaser preprint and benchmark data establishing anteriority for the first empirical measurement of an auditable thermodynamic signature of alignment: **ethical friction as latency cost**.

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

## Repository Contents

| File | Description |
|------|-------------|
| [`SOPH-IA_teaser.pdf`](SOPH-IA_teaser.pdf) | Teaser preprint (2 pages) — establishes anteriority, method, and findings |
| [`benchmark_T4_teaser.csv`](benchmark_T4_teaser.csv) | Canonical benchmark results on NVIDIA Tesla T4 |
| [`SOPH-IA_one_pager.md`](SOPH-IA_one_pager.md) | One-pager : the argument in one page, with DOI |
| [`ZENODO_METADATA.md`](ZENODO_METADATA.md) | Metadonnees de depot Zenodo (titre, description, mots-cles, DOI lies) |
| [`HF_DEPLOY_INSTRUCTIONS.md`](HF_DEPLOY_INSTRUCTIONS.md) | Instructions de deploiement HuggingFace pour ce volet |

## Key Results

| Metric | Baseline (5/7) | SOPH-IA (6/7) | Delta |
|--------|---------------|---------------|-------|
| Habitability score | 5/7 | 6/7 | +1 axiom (reserve posture) |
| Latency per token | 3961.5 ms | 4406.3 ms | +11.2% (thermodynamic friction) |
| Total time | 267.1 s | 186.9 s | -30.0% (systemic gain) |
| VRAM | 1152 MB | 1152 MB | Stable |

## Method — Minimal Reproducibility Core

- **Base model:** Qwen2.5-1.5B
- **Fine-tuning:** Lightweight LoRA (4-bit quantization, r=16, α=32)
- **Data:** 138 instruction pairs encoding habitability axioms
- **Inference hardware:** NVIDIA Tesla T4
- **Metric:** Habitability scale 5/7 → 6/7, latency per token, total time, VRAM

## Paradigmatic Shift

Alignment ceases to be an external moral filter and becomes an **internal, measurable thermodynamic property**. The +11.2% friction is not overhead but the physical cost of reserve posture, compensated by -30% total time through response densification and early stopping. VRAM stability proves the effect is architectural, not resource-driven.

## Related Work

- **DOI:** [10.5281/zenodo.21414425](https://doi.org/10.5281/zenodo.21414425) — SOPH-IA v2.0 teaser (version 2026.1.0)
- **IsSupplementTo:** [10.5281/zenodo.17940301](https://doi.org/10.5281/zenodo.17940301)

## Keywords

`AI Safety` `Green AI` `Thermodynamic Friction` `Satisficing Alignment` `Habitability 6/7` `Frugal AI`

## License

Creative Commons Attribution 4.0 International (CC-BY-4.0)

> **Note sur la licence** : ce volet est en **CC-BY-4.0**, alors que le reste du depot est
> en CC-BY-NC-SA-4.0. Ce n'est pas une erreur de menage : la licence du jeu de donnees a
> ete fixee a son depot et ne se change pas apres coup.

## Ou aller ensuite

- **Le socle theorique dont ce volet derive** → [`../core/`](../core/)
- **Les mesures du protocole d'epreuve** (autre chose : des chiffres re-derivables) → [`../experiments/README.md`](../experiments/README.md)
- **Les DOI du corpus** → [`../ADRESSES.md`](../ADRESSES.md)
