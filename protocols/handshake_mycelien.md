---
tags:
  - mttv-flp
  - mpvr
  - mycelial-routing
  - transscalar-living-systems
  - b-gate
license: CC-BY-NC-SA-4.0
language: fr
---

# Protocole de Handshake Mycélien — MTTV-FLP Core

**Module d'application :** [`mpvr-glocal/src/mttv_mycelial_handshake.py`](../mpvr-glocal/src/mttv_mycelial_handshake.py)
**Implémentation de référence couplée :** [`mpvr-glocal/src/mttv_mpvr_quorum.py`](../mpvr-glocal/src/mttv_mpvr_quorum.py)
**Version :** 1.0.0 — `mpvr-compatible`
**Licence :** CC-BY-NC-SA 4.0 / Collectif Les Fils de la Pensée

---

## 1. Rôle : coudre la bascule locale à la résilience glocale

Le handshake mycélien est l'**interface transcalaire** entre deux étages du modèle
MTTV-FLP :

- en amont, la **B-gate** ([`BGateTransduction`](../src/mttv_bgate_system.py:25)),
  bascule locale qui commute l'énergie d'un flux prédateur vers la biomasse et le
  souffle dès que la tension d'extraction franchit le seuil de l'opérateur `Σ` ;
- en aval, le **quorum poreux** ([`MicroQuorumPoreux`](../mpvr-glocal/src/mttv_mpvr_quorum.py:33)),
  framework de routage multi-chemins qui arrête la dépense énergétique dès qu'un
  seuil minimal viable de contexte est atteint.

Sans cette couture, la décision logique de la B-gate et la résilience du quorum
restent deux mécanismes disjoints. Le handshake transporte la **charge
transductive** de l'un vers l'autre : l'ouverture locale de la bascule devient une
grandeur mesurable — la *porosité résiduelle* — qui se propage à travers le
réseau d'hyphes.

## 2. Principe : la porosité comme monnaie d'intégrité

Chaque nœud (`hyphe_i`) porte un **potentiel de membrane**. À chaque transduction :

1. Si la B-gate est activée, le flux prédateur force le nœud à s'ouvrir selon
   `potentiel · e^(−Σ)` puis entre en résonance avec le pôle Bios `B`.
2. Sinon, le réseau maintient son homéostasie standard (`0.95 · potentiel + 0.05 · Σ`).
3. La **moyenne de résonance** du réseau, multipliée par la porosité `Σ`, donne la
   **porosité résiduelle** `ρ` — l'état d'ouverture conservé après la transduction.

La porosité résiduelle n'est pas un déchet : c'est la **réserve de tolérance** du
système. Un réseau résiduel ouvert peut absorber une panne locale sans
replanification centrale ; un réseau refermé exige davantage de nœuds concordants.

## 3. Routage multi-chemins et stabilisation biophysique

| Étape | Opérateur | Effet biophysique |
|-------|-----------|-------------------|
| Bascule locale | `BGateTransduction.evaluer_porosite()` | Neutralise le flux d'extraction, recharge la biomasse |
| Propagation | `MycelialHandshake.propager_transduction()` | Diffuse la charge sur tous les chemins (hyphes) en parallèle |
| Mesure | `porosite_residuelle` (ρ) | Quantifie l'ouverture résiduelle du réseau |
| Modulation | `MicroQuorumPoreux.moduler_par_porosite()` | Convertit ρ en tolérance de panne effective |
| Décision glocale | `MicroQuorumPoreux.evaluer_contexte()` | Valide ou non le contexte, avec arrêt précoce de la dépense |

Le **multi-chemins** est ici ce qui stabilise l'intégrité biophysique : aucun
chemin unique ne porte la décision. Chaque hyphe propose sa perspective ; le
consensus émerge par moyenne de résonance, et la porosité résiduelle règle le
**seuil minimal viable** du quorum glocal. Une défaillance locale est absorbée par
la redondance du réseau plutôt que propagée comme erreur fatale.

## 4. Loi de couplage ρ → tolérance

Le couplage est explicite et monotone :

```
tolérance_effective = clamp( tolérance_nominale + (ρ − 0.5) · sensibilité , 0 , 1 )
seuil_minimal_viable = ⌊ total_noeuds · (1 − tolérance_effective) ⌋
```

- **ρ > 0.5** — le réseau est ouvert et redondant : la tolérance augmente, le
  seuil minimal viable baisse, le quorum s'ouvre et économise l'énergie.
- **ρ = 0.5** — point neutre : le comportement nominal de [`MicroQuorumPoreux`](../mpvr-glocal/src/mttv_mpvr_quorum.py:16) est préservé.
- **ρ < 0.5** — le réseau est refermé : le quorum exige davantage de nœuds
  concordants avant de valider le contexte.

Ce couplage garantit la **rétrocompatibilité** : à porosité neutre, le quorum
glocal se comporte exactement comme avant l'interconnexion.

## 5. Usage

```python
from mpvr_glocal.src.mttv_mycelial_handshake import MycelialHandshake
from mpvr_glocal.src.mttv_mpvr_quorum import MicroQuorumPoreux

# 1. La B-gate produit un rapport d'état sp3
rapport_bgate = {
    "status": "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. Flux prédateur neutralisé.",
    "etats_sp3": {"Psi (Ψ)": 0.45, "Bios (B)": 0.45, "Phi (Φ)": 0.1},
    "porosite_Sigma": 0.35,
}

# 2. Le quorum couple le handshake puis évalue le flux
quorum = MicroQuorumPoreux(total_noeuds=7)
diagnostic = quorum.evaluer_avec_handshake_mycelien(
    flux_signal={"input_flux": "basse_continue"},
    bgate_output=rapport_bgate,
)
# diagnostic["couplage_mycelien"] expose protocole, résolution,
# porosité résiduelle, tolérance effective et seuil minimal viable effectif.
```

Le handshake reste utilisable seul (`python mttv_mycelial_handshake.py`) pour
inspecter la cartographie des hyphes et la résolution du quorum mycélien.

## 6. Invariant de sécurité

Aucune décision n'est déléguée à un centre unique. La B-gate décide **localement**
de la bascule ; le réseau mycélien **mesure** l'ouverture résiduelle ; le quorum
**valide** le contexte de façon distribuée. L'intégrité biophysique est préservée
par construction, non par contrôle top-down — conformément à l'axiome de
robustesse par la sous-optimalité locale du framework MPVR.

---

*Protocole déposé pour indexation ascendante (bottom-up) : chaque nœud du modèle
référence sa source, et la porosité résiduelle porte la mémoire des pertes
thermodynamiques vers l'échelle suivante.*
