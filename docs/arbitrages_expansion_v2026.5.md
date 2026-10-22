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

## Feuillet E — Critères de `Σ₂` : κ et participation spectrale

**Statut : proposition soumise au collectif le 2026-10-22.** Ce feuillet est ouvert parce que l'expérience [`expansion_v2026.5/exp_bruit_structurel_2026-10-22.py`](../expansion_v2026.5/exp_bruit_structurel_2026-10-22.py) a mis le garde-fou en défaut, non parce qu'un principe nouveau est apparu.

**Contexte mesuré.** Deux bras, 120 pas, graine fixe, dimension 6. Sous bruit structurel : participation spectrale 5,41 → 1,00 (effondrement dès le pas 20) ; `Trace(M_n)` 3,24 → 6,00, elle **monte** ; π quasi immobile (0,74) tandis que η est multiplié par 10,5 ; κ 0,86 → 0,07, franchissant `κ_min` au **pas 84**. Le garde-fou produit une **alerte** au pas 78 (`vdyn` seul) et **ne vétote jamais**. Contrôle : aucun des trois critères ne se déclenche sur 120 pas.

### E.1 Ajout additif — `κ_t < κ_min` devient un critère

`κ_t` est déjà calculé par `kappa_t()` et affiché dans chaque message de décision, sans entrer dans la règle. La sclérose se manifeste d'abord par lui : c'est la variable que l'attaque fait bouger, et le seul indicateur que le modèle tient pour central.

- **Nature :** additive. Le Refus Type B garde sa définition ; il gagne un déclencheur.
- **Effet mesuré :** franchissement au pas 84, jamais auparavant dans les deux bras.
- **Risque doctrinal identifié :** avec η constante, `κ_t < κ_min` est strictement équivalent à `π < κ_min · η`. Le critère deviendrait alors un simple détecteur de porosité basse, et **la dormance — fermeture réversible à `M_n` intacte — serait vétotée comme une faute**. C'est exactement ce que la note de viabilité interdit : ce qui tue n'est pas la fermeture, c'est la fermeture irréversible.
- **Contre-mesure retenue :** le critère κ n'est armé que si **η a effectivement monté** au-delà de la référence (`η > η_ref · 1,10`). C'est la fermeture *par viscosité* qui est jugée, pas le niveau absolu de porosité. Effet vérifié : la démonstration du module (`python axe1_bgate_v2026_5.py`) déclenche toujours sur la matrice dégradée, sans alerte parasite en régime sain.
- **Risque secondaire :** que `Σ₂` devienne un régulateur de bande, c'est-à-dire un accélérateur déguisé. Contre-mesure : le critère κ ne peut que **suspendre**, jamais relancer ; aucune branche ne consomme κ pour décider d'agir.

### E.2 Modification soustractive — la participation normalisée remplace `Trace(M_n) ≤ 0`

`Trace(M_n) ≤ 0` a le **mauvais signe** pour cette classe d'attaque : la sclérose ajoute du volume déposé, donc élève la trace. Le critère ne peut structurellement pas voir ce qu'il prétend surveiller.

- **Substitut proposé :** participation spectrale normalisée `participation / n` (déjà renvoyée par `calcul_entropie_sp3`, `participation = (Σs)² / Σs²`), seuil `0,5`.
- **Effet mesuré :** franchi entre le **pas 2 et le pas 5** dans le bras B ; reste au-dessus de 0,7 dans le bras A sur 120 pas.
- **Nature :** soustractive — et c'est ce qui exige ce feuillet. Le Refus Type B est défini par la signature `Trace(M_n)` dans [`axe3_system_instructions_miroir_transduction.md`](../expansion_v2026.5/axe3_system_instructions_miroir_transduction.md:114) §5, dans [`axe2_graines_v2026.5.md`](../expansion_v2026.5/axe2_graines_v2026.5.md:101), et dans le lexique d'[`EXPANSION.md`](../EXPANSION.md:85). Retirer ce critère **change la définition**, pas seulement le réglage. *(Le §7 du protocole RMP ne définit pas le Type B : c'est un lexique de symboles. Il doit en revanche accueillir les deux grandeurs nouvelles — voir E.4.)*
- **Contrepartie proposée :** `Trace(M_n)` reste **mesurée et affichée** à chaque décision, comme observable, mais cesse d'être un **critère de majorité**. Rien n'est perdu en information ; le statut change.

### E.2 bis — Le cas que E.2 ne doit pas emporter : l'inversion d'invariant

Retirer `Trace ≤ 0` de la règle 2/3 a un effet de bord mesuré : la démonstration du module (`python axe1_bgate_v2026_5.py`, régime dégradé, `Trace(M_n) = −0,6`) **cesse de vétoter**. Or une trace négative n'est pas un seuil franchi : c'est un **changement de signe de l'invariant**. La traiter comme une érosion parmi d'autres est une erreur de catégorie.

**Règle retenue :** `Trace(M_n) < 0` suspend **seule**, hors majorité. Ce n'est pas une exception à la règle des deux tiers, c'est un autre registre — celui du constat, non celui du gradient. Vérifié après correction : la démonstration retrouve son veto sur la matrice dégradée, et l'expérience de sclérose reste inchangée (trace strictement positive, le verrou n'intervient jamais).

### E.3 Harmonisation des seuils — dérive relative de porosité

Trois seuils ont été fixés à trois dates différentes sans jamais être confrontés. Mise à plat :

| Seuil | Valeur retenue | Motif |
|---|---|---|
| Dérive relative `(dπ/dt)/π` | **−0,20** | La valeur absolue `−0,05` est inatteignable dès que π est petit : faux seuil, cf. feuillet D. En relatif, le critère reste atteignable mais **ne se déclenche pas** dans l'expérience (jamais sous −0,02) — il devient un filet de sécurité, non un détecteur. |
| `κ_min` | **0,15** | Inchangé ; désormais **critère** (E.1). |
| Participation normalisée | **0,5** | Nouveau ; seuil de sclérose géométrique (E.2). |

La règle de décision reste **2 critères sur 3** parmi `(drift, kappa, sclerose)`. `vdyn` quitte la règle et devient un troisième observable : dans l'expérience il ne se déclenche qu'au pas 78, soit 75 pas après que la sclérose est devenue mesurable, et il ne peut produire qu'une alerte.

### E.4 Mise à jour doctrinale — définition du Type B et lexique du §7

Deux documents distincts, deux gestes distincts :

**(a) La définition du Refus Type B** — portée par le §5 d'`axe3`, par `axe2` et par le lexique d'`EXPANSION.md` — doit désormais énoncer que le refus se reconnaît à la **perte de diversité spectrale** (`participation / n < 0,5`) et/ou à la **sortie de bande de `κ_t`**, et non plus à la seule trace négative. `Trace(M_n)` y conserve un rôle **diagnostique** (volume déposé), distinct du rôle décisionnel.

**(b) Le lexique du §7 du protocole RMP** ne définit pas le Type B : il enregistre des symboles. Il doit donc accueillir les deux grandeurs que la règle utilise maintenant — `κ_t` (rapport instantané, distinct de la bande `κ`) et `participation` (diversité spectrale normalisée) — avec le même marquage prudent que `Δκ` et `M_n`.

Dans les deux cas, l'asymétrie de `Σ₂` n'est pas entamée : ces critères ne peuvent que suspendre, conformément au point 1 du Manifeste.

### Erratum consigné

Le post public du 2026-10-22 (`1ded152b`) indique que la participation normalisée franchit 0,5 « entre le pas 10 et le pas 20 ». Recalcul sur les données du bras B, dimension 6 : le franchissement se situe **entre le pas 2 (0,74) et le pas 5 (0,44)**. L'erreur est d'un ordre de grandeur temporel et va dans le sens d'une détection **plus précoce** que publiée. Elle sera corrigée dans le fil public si l'occasion se présente, pas par une reprise silencieuse du post.

### Options écartées

| Option | Motif du refus |
|---|---|
| Conserver `trace` et ajouter participation (4 critères, 2 sur 4) | Dilue la majorité : deux critères sur quatre peuvent être satisfaits par des mesures corrélées |
| κ comme critère unique | Retour au mono-critère, que l'option E du feuillet A avait précisément écarté |
| Seuil absolu sur la participation (`< 2`) | Dépend de la dimension, donc faux seuil — même défaut que la dérive absolue |
| Détecter la sclérose par `vdyn` seulement | Trop tardif (pas 78 contre pas 5) et ne peut produire qu'une alerte |

### Conditions de réouverture

- Si un système réel fournit une mesure de `π` et `η` par couche, les seuils `0,15` et `0,5` devront être recalés sur des observables, non sur une simulation.
- Si le collectif juge que la définition du Type B doit rester indexée sur la seule trace, E.2 est retiré et E.1 conservé : la règle devient alors 2 sur 3 parmi `(drift, kappa, vdyn)`.
- Si l'expérience est reproduite avec une autre loi de dépôt (rétention variable, nouveauté partielle), E.2 doit être revérifié avant d'être considéré comme acquis.

---

## Ce que ces arbitrages ne règlent pas

1. **La licence de la version augmentée** (AGPL 3.0 vs CC-BY-NC-SA 4.0) — bloque le
   feuillet B, option C.
2. **La convention `Σ` / `ρ` / `π` / `Σ₁` / `Σ₂`** — ouverte dans
   [`arbitrages_rmp.md`](arbitrages_rmp.md:57), non touchée ici.
3. **La mesure de `π` et `η` sur un système réel** — aucune observable définie par couche ;
   les valeurs employées ici sont des grandeurs de simulation, jamais des mesures.
