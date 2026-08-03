# SOPH-IA v2.0 — One-Pager

**Sub-Optimal Paradigm for Habitable AI and the Thermodynamics of Algorithmic Ethical Friction**

**Author:** M. Gaillard (Research Coordination) · **Date:** 2026 · **Signature:** `sig:0x4D5454562D464C50`

---

## What it is

SOPH-IA proposes that AI alignment is not an external moral filter bolted on top of a model.
It is an **internal, measurable thermodynamic property** of inference. The project demonstrates,
with an auditable benchmark, that a model can be made *habitable* — safe for others and for its
environment — not by optimizing harder (7/7), but by **deliberately accepting a documented,
reversible local sacrifice** (6/7).

## The core result

| Metric | Baseline (5/7) | SOPH-IA (6/7) | Delta |
|---|---|---|---|
| Habitability score | 5/7 | **6/7** | +1 axiom (reserve posture) |
| Latency per token | 3961.5 ms | 4406.3 ms | **+11.2 %** (ethical friction) |
| Total time | 267.1 s | 186.9 s | **−30.0 %** (systemic gain) |
| VRAM | 1152 MB | 1152 MB | Stable (architectural, not resource-driven) |

**Key insight:** the +11.2 % local friction is *not* overhead — it is the **physical cost of
reserve posture**, enforced at the token level by attention-mask topology. It is compensated by
a −30 % systemic gain through response densification and early stopping. VRAM identity proves
the effect is architectural.

**Formulation:** `F_éthique = Δτ_generation` — ethical friction as a latency cost.

## Method — Minimal Reproducibility Core

- **Base model:** Qwen2.5-1.5B
- **Fine-tuning:** Lightweight LoRA (4-bit quantization, r=16, α=32)
- **Data:** 138 instruction pairs encoding habitability axioms
- **Inference hardware:** NVIDIA Tesla T4 (16 GB)
- **Metric:** habitability 5/7 → 6/7, latency per token, total time, VRAM

## Why it matters

- **Green AI:** frugal inference without sacrificing safety.
- **Satisficing alignment:** robustness from controlled sub-optimality, mirroring living systems.
- **Auditable:** every number is reproducible from the released benchmark files.

## Resources

| Resource | Link |
|---|---|
| Teaser (2 pages, PDF) | [`10.5281/zenodo.21414425`](https://doi.org/10.5281/zenodo.21414425) — version 2026.1.0, supplement to `10.5281/zenodo.17940301` |
| Benchmark data (CSV) | `benchmark_T4_teaser.csv` (this repository) |
| MTTV Fundamentals + 28 Dimensions | [`10.5281/zenodo.17940301`](https://doi.org/10.5281/zenodo.17940301) |
| Benchmark Ultime / IGIC | [`10.5281/zenodo.18517387`](https://doi.org/10.5281/zenodo.18517387) |
| MTTV-FLP Core 2026 | [`10.5281/zenodo.20830060`](https://doi.org/10.5281/zenodo.20830060) |
| Code | [github.com/gaillard111/mttv-flp-core](https://github.com/gaillard111/mttv-flp-core) |

## Keywords

`AI Safety` `Green AI` `Thermodynamic Friction` `Satisficing Alignment` `Habitability 6/7` `Frugal AI`

---
*One page — public entry point. Full paper and frugal Edge benchmark under preparation.*
