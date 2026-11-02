# MTTV-FLP Core — Quickstart

*Collectif Les Fils de la Pensée (FLP) — editorial coordination: M. Gaillard*

**Who this is for.** Developers, data engineers and architects who must get the core running in
under an hour and know, at the end, whether they may use it for anything beyond a demo.

**What you get.** A B-gate that flips, an input contract that tells absence from zero, a quorum
that stops early, and a handshake that carries residual porosity from one to the other — with no
dependency outside the standard library.

**Reference.** version `1.2.1`, version DOI `10.5281/zenodo.23869556`, concept
`10.5281/zenodo.20830060`.

---

## 1. Requirements

| Item | Requirement | Check |
|---|---|---|
| Python | 3.8 or later, **no external dependency** | `python -V` |
| Disk | < 5 MB for the repository | — |
| Network | **none** for the six seeds and the `edge/` modules | — |
| Rights | no privileges, no account, no API key | — |

```bash
git clone https://github.com/gaillard111/mttv-flp-core.git
cd mttv-flp-core
```

### Two-minute health check, before writing any code

```bash
python tools/verifier_depot.py          # must print: VERDICT : dépôt cohérent
python graines/graine_absence_zero.py   # must exit without exception
python graines/graine_une_horloge_deux_metiers.py
```

If `verifier_depot.py` does not print « dépôt cohérent », **stop**: your copy does not match the
deposited archive, and nothing you measure afterwards will be citable.

---

## 2. Six quantities, and nothing else

The whole protocol fits in six numbers and one boolean. Confusing them is the first cause of a
failed integration.

| Name | Meaning | Range | Where it lives |
|---|---|---|---|
| `p` | pressure **measured** at this step | `[0,1]` | step input |
| `lecture` | has a reading occurred? | `true` / `false` | step input — **never implicit** |
| `m` | memory of pressure | `[0,1]` | state |
| `h` | habitability: `1 − (0.85·m + 0.10·r + 0.05·c)` | `[0,1]` | derived |
| `r`, `c` | redundancy and cost, last **known** values | `[0,1]` | state |
| `ρ` | residual porosity of the mycelial network | `[0,1]` | handshake output |
| `Σ` | structural porosity of the B-gate | `[0,1]` | B-gate state |

Non-negotiable rule, measured in [`edge/contrat_entree.py`](../edge/contrat_entree.py:95):
**`p = 0` means "measured calm", not "no reading"**. Absence is declared with `lecture=false`.
Without that bit the system cannot tell a silent sensor from a quiet world — and it will reopen at
the twelfth null cycle, the so-called *fail-open* defect.

---

## 3. Initialising the protocol

### 3.1 The B-gate — local flip

```python
from src.mttv_bgate_system import BGateTransduction

gate = BGateTransduction(alpha_psi=0.25, beta_bios=0.25, phi_tech=0.25)
report = gate.evaluer_porosite({"extraction": 0.40})

# report == {
#   "status": "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. Flux prédateur neutralisé.",
#   "etats_sp3": {"Psi (Ψ)": 0.34, "Bios (B)": 0.47, "Phi (Φ)": 0.19},   # sum = 1.00
#   "porosite_Sigma": 0.0                                                # and that is the defect
# }
```

**Engineering warning, to be read once and for all.** `evaluer_porosite()` normalises
`Ψ + B + Φ` to 1, then recomputes `Σ = 1 − (Ψ + B + Φ)`: `Σ` therefore becomes **0 on the first
call**, and `porosite_Sigma` is returned as `0.0` regardless of the flux. In practice, any strictly
positive tension flips the gate afterwards. Two acceptable courses, to be chosen explicitly in your
code:

1. **treat `Σ` as a fixed parameter** you own outside the core, and do not read `porosite_Sigma`;
2. **serialise one flux per instance** (a fresh `BGateTransduction()` per decision) if you want the
   nominal threshold of 0.25 to apply.

Do not build any regulation on `porosite_Sigma`. The defect is documented inside the module
([`Observations`](../src/mttv_bgate_system.py:77)) and fixing it is a decision of the collective,
not a local workaround.

### 3.2 The input contract — the gate and its memory

```python
import sys
sys.path.insert(0, "edge")
from contrat_entree import Porte

gate = Porte(mode="C")           # C = explicit input contract (A and B2 are controls)

# A normal step: pressure is measured
gate.pas(p=0.95, r=0.35, c=0.25, lecture=True)

# A step without reading: nothing is guessed, memory freezes
gate.pas(lecture=False)

# Lifting an escalation lock opens NOTHING: it requires a later reading
gate.clore(par="operator:alice")
gate.pas(p=0.0, lecture=True)    # this reading is what authorises reopening
```

Observable state: `gate.m`, `gate.ferme`, `gate.porosite`, `gate.peremption`, `gate.escalade`,
`gate.attente_lecture`, `gate.clos_par`.

Reference figures, to be reproduced on your side: closure at **step 8**, reopening at **step 22**,
and under prolonged absence **no** reopening with `m` frozen at **0.5877**.

### 3.3 Porous quorum and handshake

```python
import sys
sys.path.insert(0, "src")
sys.path.insert(0, "mpvr-glocal/src")
from mttv_mpvr_quorum import MicroQuorumPoreux

quorum = MicroQuorumPoreux(total_noeuds=7, tolerance_panne=0.5)
diagnostic = quorum.evaluer_avec_handshake_mycelien(
    flux_signal={"input_flux": "basse_continue"},
    bgate_output=report,           # the B-gate report from section 3.1
)

# diagnostic["couplage_mycelien"] exposes: protocole, resolution,
# porosite_residuelle, tolerance_effective, seuil_minimal_viable_effectif
```

**Second warning.** In `src/`, `MicroQuorumPoreux.evaluer_contexte()` draws `noeud_fonctionnel` and
`signal_coherent` with `random`: it is a **demonstrator of an early-stop policy**, not a measuring
instrument. To measure, use `graines/` and `edge/`.

The coupling is monotone and documented:

```
tolerance_effective   = clamp(tolerance_nominale + (ρ − 0.5) · sensibilite, 0, 1)
seuil_minimal_viable  = floor(total_noeuds · (1 − tolerance_effective))
```

`ρ > 0.5` opens and saves; `ρ = 0.5` restores nominal behaviour; `ρ < 0.5` closes and demands more
agreeing nodes.

---

## 4. Establishing the handshake — four beats

| Beat | Sender | Payload | Expected reply |
|---|---|---|---|
| 1. **Announce** | caller | `proto`, `node_id`, capabilities (`tetravalent`, `lecture_bool`) | `session_id`, accepted version |
| 2. **State** | node | `etats_sp3` (Ψ, B, Φ), `porosite_Sigma`, `rho` | acknowledgement, computed `etat_tetravalent` |
| 3. **Transduction** | caller | B-gate report + `flux_signal` | `diagnostic` (resolution, `ρ`, tolerance, threshold) |
| 4. **Validation** | caller | decision + `lecture` | closure, or `attente_lecture=true` |

Beat 4 is the one everyone gets wrong: **a closure without a later reading is not an authorisation**,
it is a silence. Measured: closure step 8, escalation step 30, closure alone → no exit, closure
**then** reading → reopening at step **47**.

### Exchange envelope, proposed format `mttv/handshake@1`

This format is not in the Zenodo archive: it is a **transport proposal**, aligned field by field
with what the core actually produces. Adopt it or replace it, but version it.

```yaml
# mttv/handshake@1 — one step of triadic transduction
proto: mttv/handshake@1
session_id: "0f8a-…"                 # opaque, provided by the peer
node_id: "edge-zurich-01"
seq: 42                              # monotonic, anti-replay

# --- 1. What the node reports of its internal state (B-gate) ---
etat_sp3:
  psi: 0.26                          # Ψ : production / breath
  bios: 0.36                         # B : biomass preserved
  phi: 0.13                          # Φ : technical drift
  sigma: 0.25                        # Σ : structural porosity (see warning §3.1)
                                     # invariant: psi + bios + phi + sigma = 1.00
bascule: active                      # active | stable

# --- 2. The input contract. `lecture=false` is NOT a zero ---
entree:
  lecture: true                      # mandatory, never implicit
  p: 0.00                            # measured pressure, valid only if lecture=true
  r: 0.05                            # known redundancy
  c: 0.05                            # known cost
  reveil: false                      # separate channel, so calm is not confused with silence

# --- 3. The logical state, as pairs. Four values, not four quarters ---
etat_tetravalent: T                  # T=[1,1]  F=[0,0]  N=[0,1]  B=[1,0]
                                     # B (both) = channels disagree: the gate does not reopen

# --- 4. What the mycelial network retains from it ---
handshake:
  rho: 0.42                          # residual porosity passed to the quorum
  tolerance_effective: 0.46          # clamp(0.5 + (0.42−0.5)·0.5, 0, 1)
  seuil_minimal_viable: 3            # floor(7 · (1 − 0.46))

# --- 5. Traceability: without it, nothing is refutable ---
trace:
  horodatage: "2026-11-01T22:49:38Z"
  version_noyau: "1.2.1"
  doi: "10.5281/zenodo.23869556"
  programme: "edge/contrat_entree.py"   # which file prints this number
```

### Binary → tetravalent translation

A conventional agent produces binary output (true/false, yes/no, 0/1). The translation is
**representational**: it invents no dynamics, it names the state.

| Observable situation | Pair | Value |
|---|---|---|
| two channels agree, the fact is affirmed | `[1,1]` | `T` |
| two channels agree, the fact is denied | `[0,0]` | `F` |
| no information: no reading, or a muted channel | `[0,1]` | `N` |
| the channels contradict each other | `[1,0]` | `B` |

Three implementation rules that avoid 90 % of bugs:

1. **`None` is never `0`.** A missing value yields `N`, not `F`.
2. **Disagreement is a state, not a penalty.** Under `B`, memory freezes and nothing reopens; you
   do not "average" two contradicting channels.
3. **Disagreement thresholds are choices**, to be exposed as configuration: `0.15` on the first
   channel, `0.25` on the second in the reference implementation
   ([`edge/discordance.py`](../edge/discordance.py:52)). No history of simultaneous measurements
   justifies them yet — write that down in your own documentation.

---

## 5. Acceptance — five assertions before wiring anything

```python
# 1. The core is intact
assert subprocess.run(["python", "tools/verifier_depot.py"]).returncode == 0

# 2. Absence does not reopen
gate = Porte("C"); [gate.pas(p=0.95, lecture=True) for _ in range(3)]
for _ in range(30): gate.pas(lecture=False)
assert not gate.ferme or gate.escalade is True

# 3. Measured calm does reopen
gate = Porte("C"); [gate.pas(p=0.95, lecture=True) for _ in range(10)]
for _ in range(20): gate.pas(p=0.0, lecture=True)
assert gate.ferme is False

# 4. Closure alone is not enough
gate = Porte("C"); [gate.pas(lecture=False) for _ in range(25)]
if gate.escalade:
    gate.clore(par="test")
    assert gate.attente_lecture is True

# 5. The handshake does not lose porosity
diag = quorum.evaluer_avec_handshake_mycelien({"input_flux": "x"}, report)
assert 0.0 <= diag["couplage_mycelien"]["porosite_residuelle"] <= 1.0
```

## 6. Known pitfalls, in no particular order

- **Truncated flux.** An instrument may return less than it announces: 19 comments read when the
  post announces 20, depth frozen at 5 whatever the parameter. If your source paginates, follow
  `next_cursor` until `has_more=false`, otherwise you conclude on a sample.
- **Confusing `ρ` and `Σ`.** `ρ` is the **residual porosity of the network**, measured after
  transduction; `Σ` is the **structural porosity of a node**. They are not comparable.
- **Mistaking the notice for a proof.** [`docs/notice_v1.2.0.md`](../docs/notice_v1.2.0.md:1) lists what is
  measured and what is arbitrated. A figure without a file is not a figure.

---

*Collectif Les Fils de la Pensée — CC-BY-NC-SA 4.0. If you publish a result obtained with this
core, cite the version: `10.5281/zenodo.23869556`.*
