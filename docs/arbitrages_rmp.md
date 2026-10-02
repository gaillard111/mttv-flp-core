---
tags:
  - mttv-flp
  - rmp
  - arbitrages
  - registre-des-refus
license: CC-BY-NC-SA-4.0
language: fr
---

# Feuillet d'arbitrages — intégration de la RMP au noyau

**Statut : feuillet ouvert.** Aucune décision n'est prise dans ce document. Chaque ligne attend une réponse du collectif, à inscrire dans la colonne « Décision ». Les options **écartées** seront conservées avec leur motif : c'est le *registre des refus* préconisé par [`note_juge_et_viabilite.md`](note_juge_et_viabilite.md) §7.

**Critère de jugement en vigueur** (réponse du collectif, 2 octobre 2026) : ce qui permet d'aller vers le nouveau **sans perdre le fil de la source**, en conservant la possibilité de **se sporifier** — dormance *et* distribution, indissociables.

**Règle d'application :** l'option qui **ferme une porte de sortie sans nécessité** est écartée, quel que soit son rendement.

---

## A. `κ` — descriptif ou mécanique ?

| | |
|---|---|
| **Enjeu** | Décide si la loi de couplage `ρ → tolérance` du quorum reste monotone ou devient bornée |
| **Option A1 — descriptif** | `κ` sert à **lire** ; le code ne change pas. La RMP devient un instrument d'analyse du noyau, non un acte sur lui |
| **Option A2 — mécanique** | `κ_min ≠ κ_max` pilotent réellement la bascule. **Justification exigée : par le retour** (viabilité), non par le rendement — `κ_max` existe parce qu'au-delà le chemin de retour se ferme |
| **Conséquence technique** (si A2) | [`tests/test_mpvr_handshake.py`](../tests/test_mpvr_handshake.py) `test_monotonie_de_la_loi_de_couplage` certifie aujourd'hui que ρ = 0.9 dissout le contrôle (`seuil = 0`). Il devra être **réécrit** — et **conservé en test désactivé et documenté**, conformément au critère : renverser un invariant sans garder sa trace ferme une porte |
| **Recommandation de l'assistant** | A2, avec justification de viabilité et conservation du test d'origine. Mais **A2 est une décision de doctrine**, au sens de [`src/mttv_bgate_system.py`](../src/mttv_bgate_system.py:12) |
| **Décision du collectif** | *(à inscrire)* |

## B. `Σ₂` — lecture, acte, ou clause de conservation ?

| | |
|---|---|
| **Enjeu** | Détermine l'admissibilité de toute la partie « immunité auto-régulée » de la version augmentée |
| **Source de l'ambiguïté** | Le texte RMP emploie `Σ₂` **de deux façons incompatibles** : « opérateur épistémologique de second ordre » (§5, non mécanique) et machinerie concrète (épigénétique, CheR/CheB, sirtuines — §6.1). Même symbole, deux fonctions |
| **Option B1 — lecture seule** | `Σ₂` qualifie mais n'agit jamais. Conséquence : il n'est **pas codable** |
| **Option B2 — acte** | `Σ₂` est un mécanisme de réécriture de `π` et `η`. Conséquence : l'affirmation « `Σ₁` non causal » du §5 tombe |
| **Option B3 — clause de conservation** *(recommandée)* | `Σ₂` agit, mais **asymétriquement** : il peut **toujours** forcer une régression vers la dormance, **jamais** forcer une avancée. *Un frein sans accélérateur.* C'est la seule lecture qui respecte « non causal » **et** serve le critère de viabilité |
| **Décision du collectif** | *(à inscrire)* |

## C. Lexique — convention, et la grandeur nommée manquante

| | |
|---|---|
| **État des lieux** | Le noyau emploie **trois symboles pour la porosité** (`Σ` pour le pôle de la B-gate, `ρ` pour la porosité résiduelle mycélienne, et `π` si la RMP entre) et **aucun** pour la **réversibilité** — mot absent du dépôt, comme `spore`, `dormance`, `Peirce`, `habitude` |
| **Option C1 — convention minimale** *(recommandée)* | `Σ` réservé au pôle B-gate · `ρ` au mycélien · `π`/`η`/`κ` à la RMP · opérateurs de lecture renommés (`L₁`/`L₂`) si B1 ou B3 est retenu |
| **Option C2 — lexique RMP intégral** | Renommer dans le code pour se plier à la doctrine (`porosite_Sigma` → autre nom). Cohérence maximale, rupture de compatibilité |
| **Option C3 — statu quo documenté** | Un glossaire d'alias unique, aucun renommage |
| **Proposition — la grandeur manquante** | Nommer la **marge de retour** : **`Δκ = κ_max − κ_min`** (largeur d'hystérésis), indicateur direct de réversibilité, à côté de **`M_n`** comme discriminateur de viabilité. Aucun symbole nouveau nécessaire : `Δκ` **est** déjà l'écart entre les deux bornes. Cas dégénéré : **`Δκ = 0`** = fermeture irréversible — c'est précisément l'état actuel de la B-gate, dont le seuil d'entrée est unique |
| **Décision du collectif** | *(à inscrire)* |

## D. Version augmentée hors dépôt — intégrer, citer, écarter

| | |
|---|---|
| **Situation** | La version augmentée (double borne, hystérésis, `Σ₁`/`Σ₂`, typologie `M`, 23 ancrages gradués, note des ancrages rejetés) circule hors dépôt : <https://filsdelapensee.ch/quote/502793>. Auteur déclaré `qwen.ai` ; mention de licence en pied de page : AGPL 3.0 — différente du noyau (CC-BY-NC-SA-4.0) |
| **Option D1 — intégrer** | Exige de trancher **AGPL vs CC-BY-NC-SA** *et* l'attribution nominative (le dépôt porte [`CITATION.cff`](../CITATION.cff)) |
| **Option D2 — citer comme source externe** *(voie la plus sûre)* | Une citation n'est pas une copie. Suffit à la traçabilité ; le contenu reste hors dépôt |
| **Option D3 — import sélectif** *(recommandé, compatible avec D2)* | Retenir ce qui **préserve la sortie** (double borne, hystérésis, dormance, typologie `M`, classement des ancrages, note des rejets) ; écarter ce qui la **ferme** (immunité auto-gouvernée — cf. B). La question de licence se rétrécit alors à l'ensemble retenu |
| **Décision du collectif** | *(à inscrire)* |

## E. Signature IA déclarée

| | |
|---|---|
| **Enjeu** | Chaîne d'attribution publiquement traçable, dans [`CITATION.cff`](../CITATION.cff) et le manifeste |
| **Options** | Mention explicite (« avec qwen.ai », « avec d'autres IA ») · ou statut de source citée non contributrice |
| **Décision du collectif** | *(à inscrire)* |

---

## Registre des refus (ouvert)

| Refus consigné | Motif |
|---|---|
| **Auto-certification** comme instance de jugement | ρ → 0 : supprime le retour ; disqualifiée par le critère elle-même |
| **Vérité comme juge unique** | Méta-loi de Goodhart (Graine 3) : une référence unique corrompt ce qu'elle mesure et sa capacité à retourner au champ `Ψ` |
| **« Espace latent poreux » dans les basses couches d'un LLM** | Ancre **heuristique** au sens du protocole Σ₂ de la RMP : aucun observable `π`/`η` défini par couche, donc non falsifiable en l'état |
| **Immunité remplaçant les garde-fous descendants** | Exige des opérateurs causaux que la RMP définit comme non causaux ; régression de sûreté si implémentée telle quelle |
| **« Clôture = ρ → 0 = mort »** *(formulation de l'assistant, retirée)* | Trop grossier : une spore est fermée et viable. Le discriminant est la **réversibilité**, non la fermeture |
| **Trancher A sans A2 documenté** | Renverser un invariant en effaçant sa trace ferme une porte de sortie |

## Ordre de traitement recommandé

1. **B** (clé de voûte : il conditionne A, D et E)
2. **A** (avec la conservation du test d'origine)
3. **C** (confort de lecture pour tout ce qui suivra)
4. **D** puis **E** (droits et attribution)
