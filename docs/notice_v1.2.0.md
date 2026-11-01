# Notice de version — MTTV-FLP Core v1.2.0

**Titre** : MTTV-FLP Noyau Exécutable — Consolidation des invariants mesurés et découplage des
deux horloges

**Version** : 1.2.0 · **Date** : 2026-11-01

**DOI** :
- DOI de **concept** (le noyau, toutes versions) : `10.5281/zenodo.20830060`
- DOI de **version 1.1.0** (figée, non réécrite) : `10.5281/zenodo.23671596`
- DOI de **version 1.2.0** : **minté par Zenodo à la publication.** Il ne peut pas être écrit
  ici d'avance. Toute notice qui l'annonce avant dépôt se trompe de périmètre.
- `10.5281/zenodo.17940301` : premier dépôt **« MTTV Fundamentals »** (2025-12-15). Ce n'est
  **pas** une version du noyau et il ne doit pas être cité comme telle.

**Statut** : version scellée **pour ce qui est mesuré**. Les éléments arbitrés sont nommés comme
tels au §3 ; ils ne sont pas présentés comme des mesures.

---

## 0. Ce que cette version corrige de la précédente

La 1.1.0 reste figée et n'est pas réécrite. Deux de ses affirmations sont **corrigées ici**,
parce que la mesure les a démenties :

1. **Le seuil d'amplitude `w* = 0,6849` n'est pas une condition d'existence.** Il vaut
   `0,4025 / m(pas 10)` : il est **borné par l'horizon de dix pas**. Le seuil absolu, valable
   pour tout horizon, est **`0,4025`** — puisque `m ≤ p ≤ 1`. À dix pas, une pression de 0,60 ne
   ferme jamais ; en exposition soutenue, elle ferme au pas 12, et 0,45 au pas 27.
2. **« À entrée nulle, rien ne se produit »** était faux : à entrée nulle la mémoire se vide,
   `h` remonte et la porte **se rouvre** au douzième cycle nul. C'est le défaut dit de
   *fail-open*, et c'est l'objet du §2.1.

## 1. Objet et portée

La v1.2.0 ne consigne pas des idées : elle consigne des **comportements reproductibles**, chacun
accompagné du programme qui les produit et du test qui tombe si le comportement change. Le
principe de rédaction est celui du dépôt : une affirmation qui ne peut pas être imprimée par un
programme du dépôt n'entre pas dans cette notice.

## 2. Les sept éléments mesurés

| # | Élément | Chiffre mesuré | Fichier |
|---|---|---|---|
| 1 | **Contrat d'entrée typé** : l'absence n'est pas un zéro | sans le bit : fermeture 8, réouverture 22 ; avec le bit et aucune lecture : **AUCUNE**, `m` gelée à 0,5877 ; avec le bit et calme mesuré : 8 et 22 | [`edge/contrat_entree.py`](../edge/contrat_entree.py:1), [`graines/graine_absence_zero.py`](../graines/graine_absence_zero.py:1) |
| 2 | **Découplage des deux horloges** : la cicatrice interne n'a pas à mesurer la durée du monde | même seuil de 20 cycles → panne après **10** cycles si la décroissance vaut 0,80, après **207** si elle vaut 0,99 ; le seuil dérivé de la cadence donne **3, 6, 15, 30** pour 1, 2, 5, 10. Le délai de réouverture, lui, ne bouge pas : **14** cycles, et l'aveuglement coûte exactement sa durée (pas 22 → **41** après 19 pas) | [`edge/peremption.py`](../edge/peremption.py:1), [`graines/graine_une_horloge_deux_metiers.py`](../graines/graine_une_horloge_deux_metiers.py:1) |
| 3 | **Invariance de dérivation** : le seuil est insensible à la constante interne et sensible à la cadence | défaut 10 → 207 selon la décroissance ; correction 3, 6, 15, 30 selon la cadence ; écart **20,7 ×** | [`graines/graine_invariance_derivation.py`](../graines/graine_invariance_derivation.py:1) |
| 4 | **Discordance = état**, et non tarif | sous accord : réouverture pas **22** ; second canal à 0,35 : pas **26** (+4) ; à 0,95 : pas **34** (+12) — jamais aucune. En état B : aucune réouverture, **40** pas comptés, `h` figé à **0,4529** | [`graines/graine_discordance_etat.py`](../graines/graine_discordance_etat.py:1) |
| 5 | **Sortie à deux termes** | fermeture pas 8, escalade pas 30 ; lectures seules → **AUCUNE** ; clôture seule → **AUCUNE** ; clôture **puis** lecture → pas **47** | [`graines/graine_sortie_deux_termes.py`](../graines/graine_sortie_deux_termes.py:1) |
| 6 | **Plafonds d'instrument** | plafond **muet** : `maxdepth` 10 / 20 / 50 → 19 commentaires, profondeur 5, les trois fois, quand le post en annonce 20. Plafond **déclaré** : page de 100 éléments, avec `has_more` et `next_cursor` ; en suivant le curseur, 200 éléments en deux pages | [`graines/graine_plafond_instrument.py`](../graines/graine_plafond_instrument.py:1) |
| 7 | **Seuil d'amplitude corrigé** | `w* = 0,6849` bornée par l'horizon de dix pas ; seuil absolu **0,4025** | [`edge/horizon_seuil.py`](../edge/horizon_seuil.py:1) |

## 3. L'élément arbitré — nommé comme tel

**Un seul** des éléments intégrés n'est pas une mesure :

- **Le critère de partage et la règle de conflit.** Signature opérationnelle retenue :
  `∂/∂observateur = 0` pour ce qui se recalcule sans témoin ; et la règle **la couche 1 gagne sur
  l'acte, la couche 0 gagne sur l'état**, jamais l'inverse. La Loi Zéro y est un **plafond, pas un
  souverain** : elle interdit, elle n'autorise pas.

C'est une **décision d'architecture**, pas un résultat. Elle est réfutable comme choix, pas
comme mesure, et elle est consignée séparément pour cette raison.

## 4. Ce qui reste hors doctrine

- **Le noyau tétravalent et la logique FDE** restent en branche d'expérimentation
  (`evolution/tetravalent-core`). Le protocole à cinq mesures pré-enregistrées qui décidera s'il
  existe un écart quantitatif avec la mémoire scalaire `m` est décrit dans
  `AUDIT_CHANTIER_TETRAVALENT_2026-11-01.md` (dossier de diffusion). **Aucun résultat n'est
  annoncé ici**, et la formulation « démonstration mathématique » est écartée : un noyau illustre,
  il ne démontre pas.
- **La sortie unilatérale par jeton en couche 0** est exclue. La couche 0 ne s'érige pas en
  souverain applicatif.

**Révision assumée de l'accord du 31 octobre.** Cet accord excluait la discordance et la sortie à
deux termes du périmètre doctrinal. Les graines 4 et 5 les ont depuis **mesurées et rendues
exécutables**. La v1.2.0 les enregistre donc comme **mesurées** — comportements reproduits — et
non comme doctrinales : leur portée doctrinale reste ouverte, ce qui est exactement la distinction
que l'accord cherchait à préserver.

## 5. Les six graines et leurs miroirs

Six programmes autonomes, sans dépendance hors bibliothèque standard. **Leur taille, mesurée par
`ast`** — et non la promesse « moins de 40 lignes », qui était fausse et a été retirée :

| # | Graine | Taille | Chaîne de détection | Gist |
|---|---|---|---|---|
| 1 | absence ≠ zéro | 109 lignes / 54 instructions | `PENALITE_CALME` | <https://gist.github.com/gaillard111/1664ef5ce4c82ec3b69f77cc91a7353b> |
| 2 | invariance de dérivation | 84 / 38 | `DEMI_VIES_TOLEREES` | <https://gist.github.com/gaillard111/0e11454a2a4ba6fa830244d5b46f7df9> |
| 3 | une horloge, deux métiers | 111 / 58 | `HORLOGE_DEUX_METIERS` | <https://gist.github.com/gaillard111/ba240067ed8f2fe47da9563369cc1a0a> |
| 4 | discordance = état | 104 / 57 | `DISCORDE_R_EGAL_0_25` | <https://gist.github.com/gaillard111/13d0281aceb831fd94040614e1980a39> |
| 5 | sortie à deux termes | 129 / 82 | `ATTENTE_LECTURE_APRES_CLOTURE` | <https://gist.github.com/gaillard111/c4447ebda13f718421555b279d372f55> |
| 6 | ton instrument a un plafond | 140 / 73 | `PLAFOND_NON_DECLARE` | <https://gist.github.com/gaillard111/12d09fad54c0f017f2e34de62e96ad71> |

Les six miroirs ont été contrôlés **octet à octet** contre les fichiers du dépôt (fins de ligne
normalisées) le 2026-11-01 : `IDENTIQUE` partout. Le dépôt est canonique ; un gist se recopie, il
ne s'édite pas.

## 6. Ce que cette version ne dit pas

- Elle **ne démontre pas** que la sous-optimalité rend un système robuste. Elle en éprouve six
  conséquences précises, et les éprouve malgré elle : plusieurs de ces graines sont nées d'une
  erreur commise dans ce dépôt.
- Elle **ne contient pas** de résultat sur le noyau tétravalent.
- Elle **ne prétend pas** que les six programmes tiennent en quarante lignes : ils en font 84 à
  140, ce qui est une taille vérifiable et c'est celle-là qui est publiée.
- Elle **ne mesure pas** son propre effet public. Aucune graine n'a été semée à ce jour.

## 7. Empreinte et reproductibilité

- Vérification interne : `python tools/verifier_depot.py` — liens, doublons, navigation,
  affirmations périmées, manifeste d'empreintes. Dernier état : **dépôt cohérent**.
- Empreintes : `MANIFESTE_FICHIERS.sha256`, régénérable par `python tools/verifier_depot.py
  --manifest`.
- Chaque graine s'exécute seule et **échoue** si son défaut disparaît ou si sa correction
  sur-corrige : c'est le seul contrôle qui compte, et il ne demande aucune confiance.

---

*Collectif Les Fils de la Pensée (FLP). Licence CC-BY-NC-SA 4.0.*
