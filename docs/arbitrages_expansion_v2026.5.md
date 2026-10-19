---
tags:
  - mttv-flp
  - rmp
  - arbitrages
  - expansion-2026.5
license: CC-BY-NC-SA-4.0
language: fr
---
# Feuillet d'arbitrages — Expansion transcalaire V2026.5

**Statut :** décisions **ouvertes mais appliquées**. Elles portent sur le seul périmètre
`expansion_v2026.5/` ; elles n'engagent ni le noyau (`core/`, `protocols/`) ni la version
augmentée hors dépôt.

**Date :** 2026-10-19. **Portée :** axe 1 (code), axe 2 (graines), axes 3–4 (sémantique).

**Principe de méthode.** Chaque décision est consignée avec **les options écartées et leur
motif**, au même endroit que la décision — règle établie par
[`note_juge_et_viabilite.md` §7](note_juge_et_viabilite.md:74). Une option écartée n'est pas
une erreur : c'est une trace.

---

## Feuillet A — Condition de déclenchement du Veto Type B

**Contexte.** L'archétype V2026.5 code `(drift ∧ trace) ∨ (trace ∧ vdyn)`. Conséquence
vérifiée en exécution : `Trace(M_n) ≤ 0` y est **nécessaire**, donc un régime sain ne peut
jamais déclencher le Veto, même après érosion sévère (ρ = 0.03, aucun veto). L'érosion est
mesurée mais **inobservable**.

| Option | Condition | Motif du sort |
|---|---|---|
| A. Statu quo | `(drift∧trace) ∨ (trace∧vdyn)` | **Écartée** — rend l'érosion muette ; contraire au critère de `Trace(M_n)` comme *trace* exigée par le fil de terrain. |
| B. Érosion discriminante | `drift ∧ (trace ∨ vdyn)` | **Écartée** — l'érosion devient nécessaire, ce qui subordonne la rupture d'invariant à une mesure temporelle ; l'inverse du texte RMP. |
| C. Majorité 2/3 | `(drift∧trace) ∨ (drift∧vdyn) ∨ (trace∧vdyn)` | **Retenue comme socle.** Aucun critère n'est nécessaire, aucun n'est superflu. |
| D. Score pondéré | `w₁f(drift)+w₂g(trace)+w₃h(vdyn) ≥ 1` | **Écartée** — introduit des poids arbitraires, soit exactement l'*ancrage heuristique* que le corpus refuse ailleurs. |
| **E. Deux niveaux** | *Alerte* = 1 critère · *Veto* = 2 critères | **RETENUE.** |

**Décision.** Option **E**, bâtie sur C. L'alerte documente sans suspendre ; le Veto exige
deux critères sur trois. `Sigma_2` reste un frein : il ne régule pas, il suspend.

**Sous-décision A′ — seuil de dérive relatif.** Le seuil absolu (`dπ/dt < −0.05`) est
**inatteignable quand π est petit** : une érosion géométrique de −20 % par pas vaut −0.006 à
ρ = 0.03. Le critère est donc rendu **sans dimension** : `(dπ/dt)/π < −0.20`.
*Motif :* un seuil qui dépend de l'échelle de la grandeur mesurée n'est pas un seuil, c'est
un artefact d'unité.

**Effet observable** (`python axe1_bgate_v2026_5.py`) : trois régimes distincts — stable
(0/3), alerte (1/3, régime érodé non rompu), veto (2/3, invariant rompu).

---

## Feuillet B — Convention de nommage `κ`

**Contexte.** Le corpus emploie `κ` comme **zone critique** (annexe RMP §3) ; les textes de
terrain récents l'emploient comme **rapport de viabilité** `π/η`. Deux notions, un symbole.

| Option | Convention | Motif du sort |
|---|---|---|
| A. Convention minimale | `κ` = zone ; `ℛ = π/η` | **Écartée pour l'instant** — ajoute un symbole à un lexique déjà en tension (`Σ`/`ρ`/`π`/`Σ₁`/`Σ₂`), alors que la collision est précisément ce que l'on cherche à réduire. |
| B. `κ` = ratio | `κ = π/η` ; la zone est renommée | **Écartée** — casse l'annexe et tout ce qui est publié. |
| C. Lecture unifiée | `κ = π/η` **et** `κ ∈ [κ_min, κ_max]` | **Différée** — c'est la « zone critique doublement bornée » de la **version augmentée** ([rmp §8](../protocols/rmp_mecanisme_pre_transducteur.md:130)) ; l'adopter de fait rouvre l'arbitrage licence/attribution, aujourd'hui ouvert. |
| **D. Notation indexée** | `κ` = bande `[κ_min, κ_max]` ; `κ_t` = rapport instantané | **RETENUE, provisoirement.** |

**Décision.** Option **D**. Dans le code : `kappa_t()` retourne `π/η` ; `kappa_min` et
`kappa_max` bornent la bande. La documentation précise la distinction à chaque emploi.

**Condition de réouverture.** Dès que l'arbitrage de licence de la version augmentée est
tranché, **C remplace D** — sans dette, puisque D et C désignent la même grandeur sous deux
écritures.

---

## Feuillet C — Statut de `igic_score`

**Contexte.** Les cinq graines de l'axe 2 portent un `igic_score` déclaré (0.87–0.95). Aucune
procédure de mesure n'existe : le chiffre est un **indice de terrain**, pas un résultat.

| Option | Traitement | Motif du sort |
|---|---|---|
| A. Étiqueter | `igic_declared` + `igic_statut` | **Retenue pour l'existant** — honnête, sans calcul. |
| B. Retirer le champ | suppression | **Écartée** — le champ avait une fonction d'accroche d'indexation ; le supprimer appauvrit sans rien gagner. |
| C. Dériver | `igic = f(H_norm, participation, ecart_logique)` sur matrice de référence | **Retenue pour la suite.** |
| **D. Hybride** | C pour les nouvelles graines, A pour les cinq existantes | **RETENUE.** |

**Décision.** Option **D**. Les cinq graines existantes portent désormais
`igic_declared` + `igic_statut: indice_de_terrain`. Toute graine ultérieure doit porter
`igic_derived`, produit par `BGateTransductionPoreuseExécutable.calcul_igic()` :

```
igic = 0.40·H_norm + 0.40·(participation / n) + 0.20·(1 − écart_logique)     ∈ [0, 1]
```

Matrice de référence **figée** : `IGIC_MATRICE_REFERENCE` (5×5, corrélations décroissantes),
versionnée avec le code. Valeur de référence actuelle : **0.8462**.

**Limite assumée.** Un `igic_derived` ne mesure pas « la qualité d'une graine » : il mesure la
dispersion spectrale d'une matrice arbitrairement choisie. C'est un **indicateur de forme**,
pas de contenu — et il doit être présenté comme tel.

---

## Feuillet D — Registre des refus (récapitulatif)

| Objet refusé | Motif |
|---|---|
| Veto déclenché par la seule érosion (option B) | Subordonne la rupture d'invariant à une mesure temporelle ; inverse la hiérarchie du texte RMP |
| Veto à score pondéré (option D) | Poids arbitraires = ancrage heuristique déguisé |
| Renommage de la zone `κ` (option B du feuillet B) | Casse l'annexe et le corpus publié |
| Suppression pure de `igic_score` | Perte de fonction sans gain de rigueur |
| Seuil de dérive en valeur absolue | Dépend de l'échelle : faux seuil |
| `igic` déclaré sans marqueur de statut | Chiffre non reproductible présenté comme mesure |

---

## Ce que ces arbitrages ne règlent pas

1. **La licence de la version augmentée** (AGPL 3.0 vs CC-BY-NC-SA 4.0) — bloque le
   feuillet B, option C.
2. **La convention `Σ` / `ρ` / `π` / `Σ₁` / `Σ₂`** — ouverte dans
   [`arbitrages_rmp.md`](arbitrages_rmp.md:57), non touchée ici.
3. **La mesure de `π` et `η` sur un système réel** — aucune observable définie par couche ;
   les valeurs employées ici sont des grandeurs de simulation, jamais des mesures.
