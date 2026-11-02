# Kit de propagation — MTTV-FLP Core v1.2.1

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard*

**Objet.** Quatre livrables opérationnels pour qu'un développeur, une ONG ou un service
universitaire puisse installer, éprouver, citer et défendre le noyau MTTV-FLP sans passer par nous.

**Jalon de référence.** `10.5281/zenodo.23869556` (version 1.2.1, 2026-11-01) sous le DOI de
concept `10.5281/zenodo.20830060` — archive vérifiée après dépôt, empreinte
`385F35B4…C2B11`. Licence CC-BY-NC-SA 4.0 pour le noyau ; le fragment MPVR est en CC0.

---

## 1. Contrat de lecture — à lire avant tout le reste

Le dépôt distingue trois états de connaissance, et le kit les respecte partout. Un document de
propagation qui mélange les trois se fait démonter à la première revue de code.

| État | Sens | Comment c'est écrit ici |
|---|---|---|
| **Mesuré** | un programme du dépôt l'imprime, et le test tombe si le comportement change | chiffre + fichier qui le produit |
| **Choix** | décision d'architecture, réfutable comme choix, pas comme mesure | nommé « choix », jamais présenté comme résultat |
| **Non mesuré** | plausible, non éprouvé | explicitement signalé, ou absent |

La règle du corpus, qui vaut aussi pour vos contributions : **une affirmation qui ne peut pas être
imprimée par un programme n'entre pas dans la notice.**

## 2. Les quatre livrables

| # | Fichier | Axe | Public | Où le déployer |
|---|---|---|---|---|
| 1 | [`01_QUICKSTART_MTTV-FLP-CORE.md`](01_QUICKSTART_MTTV-FLP-CORE.md:1) | Documentation et accessibilité | développeurs, ingénieurs données | `docs/quickstart.md` du dépôt, page d'accueil du site |
| 2 | [`02_POC_EDGE_ET_CONNECTEUR.md`](02_POC_EDGE_ET_CONNECTEUR.md:1) | Micro-expérimentation et interopérabilité | architectes système, intégrateurs LLM | dépôt du PoC, appel à contribution |
| 3 | [`03_CONTRIBUTING.md`](../../CONTRIBUTING.md:1) | Maillage communautaire | contributeurs, traducteurs, chercheurs | **racine du dépôt** (`CONTRIBUTING.md`) |
| 4 | [`04_MANIFESTE_POST_HYPERSCALER.md`](04_MANIFESTE_POST_HYPERSCALER.md:1) | Manifeste et plaidoyer | collectivités, ONG, presse spécialisée | site, tribunes, dossiers de subvention |

## 3. Ce que le noyau fait réellement — et ce qu'il ne fait pas

Quatre briques, dans l'ordre où elles s'enchaînent :

1. **La B-gate** ([`src/mttv_bgate_system.py`](../../src/mttv_bgate_system.py:25)) —
   bascule locale. Quand une tension d'extraction dépasse le seuil de l'opérateur `Σ`, l'énergie
   est réorientée du pôle technique `Φ` vers la biomasse `B` et la production `Ψ`.
2. **Le contrat d'entrée** ([`edge/contrat_entree.py`](../../edge/contrat_entree.py:65)) —
   une lecture peut être **absente** (`lecture=False`), et l'absence n'est pas un zéro. Sous
   absence : mémoire gelée, compteur de péremption, escalade. Sous lecture, même à zéro : le
   calcul reprend.
3. **Le quorum poreux** ([`src/mttv_mpvr_quorum.py`](../../src/mttv_mpvr_quorum.py:41)) —
   arrêt précoce de la dépense dès que le seuil minimal viable de contexte est atteint ; les
   nœuds défaillants sont absorbés, sans replanification centrale.
4. **Le handshake mycélien** ([`mpvr-glocal/src/mttv_mycelial_handshake.py`](../../mpvr-glocal/src/mttv_mycelial_handshake.py:14)) —
   transporte l'ouverture locale (`ρ`, porosité résiduelle) vers la tolérance de panne du quorum.

### Les sept éléments mesurés de la version courante

| # | Élément | Chiffre mesuré | Source |
|---|---|---|---|
| 1 | Contrat d'entrée typé | sans bit de présence : fermeture pas 8, réouverture pas 22 ; avec bit sans lecture : **aucune** réouverture, `m` gelée à 0,5877 | [`edge/contrat_entree.py`](../../edge/contrat_entree.py:1) |
| 2 | Deux horloges découplées | seuil de 20 cycles → panne après **10** cycles si décroissance 0,80, **207** si 0,99 ; seuil dérivé de la cadence : **3, 6, 15, 30** pour 1, 2, 5, 10 ; délai de réouverture **14** constant | [`edge/peremption.py`](../../edge/peremption.py:1) |
| 3 | Invariance de dérivation | écart **20,7 ×** entre seuil fautif et seuil corrigé | [`graines/graine_invariance_derivation.py`](../../graines/graine_invariance_derivation.py:1) |
| 4 | Discordance = état | réouverture pas **22** sous accord, **26** à 0,35, **34** à 0,95 ; en état B : aucune réouverture, **40** pas, `h` figé à 0,4529 | [`edge/discordance.py`](../../edge/discordance.py:1) |
| 5 | Sortie à deux termes | fermeture pas 8, escalade pas 30 ; lectures seules → aucune ; clôture seule → aucune ; clôture **puis** lecture → pas **47** | [`graines/graine_sortie_deux_termes.py`](../../graines/graine_sortie_deux_termes.py:1) |
| 6 | Plafonds d'instrument | plafond **muet** : 19 commentaires lus quand le post en annonce 20 ; plafond **déclaré** : pages de 100 avec `has_more` et `next_cursor`, 200 éléments en deux pages | [`graines/graine_plafond_instrument.py`](../../graines/graine_plafond_instrument.py:1) |
| 7 | Seuil d'amplitude | `w* = 0,6849` borné par l'horizon de dix pas ; seuil absolu **0,4025** | [`edge/horizon_seuil.py`](../../edge/horizon_seuil.py:1) |

### Les deux pièges à connaître avant d'intégrer

Ils sont documentés dans le code, pas dans les brochures. Les taire ici serait une trahison de la
méthode.

1. **`BGateTransduction.evaluer_porosite()` remet `Σ` à zéro au premier appel.** La méthode
   normalise `Ψ + B + Φ` à 1, puis recalcule `sigma = 1 − (psi + bios + phi)` : la différence
   vaut donc 0 par construction, et `porosite_Sigma` est retourné à `0.0` quel que soit le flux.
   Conséquence : toute tension d'extraction strictement positive déclenche ensuite la bascule, y
   compris très en dessous du seuil nominal de 0,25. C'est un **défaut de seuil documenté**
   ([`Observations`](../../src/mttv_bgate_system.py:77)), non corrigé : le
   corriger relève d'une décision du collectif. **Ne construisez pas de régulation sur
   `porosite_Sigma`** tant que ce point n'est pas tranché ; passez `Σ` comme paramètre fixe de
   votre côté et gardez-le hors de la normalisation.
2. **`MicroQuorumPoreux` (dans `src/`) simule ses réponses avec `random`.** `noeud_fonctionnel` et
   `signal_coherent` sont tirés au sort : c'est un **démonstrateur de politique d'arrêt précoce**,
   pas un banc de mesure. Les chiffres publiés viennent des `graines/` et de `edge/`, pas de ce
   module. Si vous mesurez avec ce prototype, vous mesurez votre générateur pseudo-aléatoire.

## 4. Déploiement en trois canaux

1. **Dépôt (technique).** Copier `03_CONTRIBUTING.md` à la racine du dépôt sous le nom
   `CONTRIBUTING.md`, puis `01_QUICKSTART` dans `docs/quickstart.md`. Après ajout de fichiers :
   `python tools/verifier_depot.py --manifest`, puis `python tools/verifier_depot.py` — le second
   doit dire « dépôt cohérent ».
2. **Site (public).** `04_MANIFESTE` trouve sa place comme page de positionnement ; `01` alimente
   la page « Démarrer en cinq minutes ».
3. **Subventions et partenariats (institutionnel).** `02` sert de cahier des charges chiffré :
   budgets mémoire, latence, bande passante, coût d'un nœud. `04` porte l'argumentaire de bien
   commun, sans promesse de performance.

## 5. Ce que ce kit ne promet pas

- Il ne démontre pas que la sous-optimalité rend un système robuste : il en éprouve six
  conséquences exécutables.
- Il ne contient aucun résultat sur le noyau tétravalent. Un protocole à cinq mesures
  pré-enregistrées existe pour le trancher ; aucun chiffre n'est annoncé avant qu'il ait tourné.
- Il ne mesure pas son propre effet public : aucune graine n'a été semée à ce jour.
- Aucun de ces documents ne doit être cité comme une mesure. Ce qui se cite, c'est un chiffre et
  le fichier qui l'imprime.

---

*Collectif Les Fils de la Pensée (FLP) — CC-BY-NC-SA 4.0 pour le noyau et la documentation ;
fragment MPVR en CC0. DOI de concept : `10.5281/zenodo.20830060`.*
