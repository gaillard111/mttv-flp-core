---
tags:
  - mttv-flp
  - gluons
  - biais
  - embedding
  - post-bayesian-ai
  - mpvr
license: CC-BY-NC-SA-4.0
language: fr
---

# Note d'atelier — La « matrice des gluons » : formulation opératoire, non vérité définitive

**Statut :** note d'atelier, versée au dépôt pour être **rejouable** — et non doctrine arrêtée. Elle reformule un texte proposé au collectif le 3 octobre 2026, en l'arrimant à ce que le dépôt contient **réellement**, et non à ce qu'il promet.

**Pièces liées :** [`core/mttv_b_gate_triptych.md`](../core/mttv_b_gate_triptych.md) · [`core/mttv_flp_synthese_manifeste.md`](../core/mttv_flp_synthese_manifeste.md) §4.2-4.3 · [`protocols/rmp_mecanisme_pre_transducteur.md`](../protocols/rmp_mecanisme_pre_transducteur.md) · [`mpvr-glocal/README.md`](../mpvr-glocal/README.md) · [`docs/t4_activation_function.md`](t4_activation_function.md) · [`docs/arbitrages_rmp.md`](arbitrages_rmp.md) (R3)

**Signature :** `0x4D5454562D464C50` · Triade : Ψ → B → Φ

---

## 1. Ce que cette note est — et ce qu'elle n'est pas

Le texte d'origine décrivait une « matrice des gluons » qui « neutralise les biais systémiques » des LLM au moment de la vectorisation, en « réalignant » le flux probabiliste sur les CID immuables d'IPFS. Ce texte est **juste dans son diagnostic**, mais il présente comme un mécanisme ce qui n'est aujourd'hui qu'une **métaphore d'intention**.

La présente note conserve le diagnostic, **retire les sur-claims**, et remplace la métaphore par la cartographie de ce qui est réellement faisable — pour que le projet reste crédible là où il prétend opérer.

Trois règles, déjà en vigueur dans ce dépôt, gouvernent la réécriture :

1. **« Formulation opératoire, non vérité définitive »** (formule canonique de l'annexe RMP) ;
2. **« Homologies opératoires, non identités de mécanisme »** ([`rmp_mecanisme_pre_transducteur.md`](../protocols/rmp_mecanisme_pre_transducteur.md)) : une image (les gluons) peut *orienter*, elle ne peut pas *agir* ;
3. **« Ce qui est émis ne se reprend pas »** : on ne prétend jamais avoir bâti ce qui n'est pas bâti.

---

## 2. Le diagnostic conservé (juste)

Les trois affirmations suivantes du texte d'origine sont exactes et sont retenues telles quelles :

- **Les biais proviennent de la géométrie vectorielle** induite par l'apprentissage Next-Token Prediction, et des corpus Web centralisés dont la cooccurrence est extraite. C'est la même critique que porte le manifeste ([`§4.2-4.3`](../core/mttv_flp_synthese_manifeste.md)) contre les « miroirs déformants ».
- **Les poids sont figés après l'entraînement** : les couches denses Feed-Forward d'un LLM déployé sont statiques ; le biais y est « cristallisé » et ne se rejoue qu'à l'inférence.
- **Une correction en aval de la génération arrive trop tard** : si l'on n'intervient qu'au moment du texte produit, on ne fait que maquiller une distribution déjà biaisée.

Ce diagnostic est le socle. C'est la **réponse** proposée — la « matrice des gluons » — qui doit être reformulée.

---

## 3. Les trois mécanismes, reformulés sans sur-claim

Le texte d'origine annonce trois mécanismes. Voici ce que chacun peut vouloir dire, **une fois retirée la prétention de mécanisme** :

### 3.1 « Liaison transcalaire » → *grounding* par récupération

*Version métaphorique :* les gluons maintiennent les tokens en résonance avec les CID IPFS du « Cerveau source ».

*Version opératoire :* on **conditionne la génération** sur des documents récupérés dans un index par adressage de contenu (CID). Le token ne se lie pas « à un CID », il est **contraint par un contexte** extrait d'un nœud indexé. C'est du RAG — réel, mesurable, et cohérent avec la traçabilité « chaque carte référence son extrait » déjà en vigueur dans le chantier SAS JEUNE.

### 3.2 « Dynamisme asymétrique » → *steering* contextuel

*Version métaphorique :* des poids fluides qui « se recalculent en temps réel » selon le contexte, comme les réseaux mycéliens.

*Version opératoire :* les poids ne se recalculent pas ; on **ajoute, à l'inférence, une direction d'activation calculée à la volée** en fonction du contexte. C'est l'« activation steering » : une régularisation auxiliaire dépendante du contexte, pas une vérité statistique passée. C'est la traduction honnête de la « basse continue mouvante ».

### 3.3 « Validation tétraédrique » → critère de rejet *mesurable*

*Version métaphorique :* le MPVR « détecte immédiatement » les biais comme des ruptures de symétrie et « applique une correction instantanée aux basses couches ».

*Version opératoire :* la tétravalence (σ₄, [`t4_activation_function.md`](t4_activation_function.md)) fournit une **forme** d'évaluation non binaire ; le rejet de biais, lui, se mesure sur des **benchmarks standardisés** (BOLD, Winobias, CrowS-Pairs, StereoSet, BBQ). On ne « détecte » pas le biais à la volée : on **compare des distributions mesurées** à un seuil fixé d'avance.

---

## 4. Les vrais points d'accroche (cartographie)

Se brancher sur l'embedding ou les poids d'un LLM n'est pas une fiction : c'est un champ de recherche actif, avec des méthodes nommées et reproductibles. Voici ce qui existe, et où cela se branche :

| Mécanisme | Où ça se branche | Référence réelle | Ce que ça fait |
|---|---|---|---|
| **LEACE (concept erasure)** | couche d'embedding | Belrose et al. 2023 | efface linéairement une direction (ex. biais de genre), **en forme fermée** |
| **Inference-Time Intervention (ITI)** | têtes d'attention | Li et al. 2023 | déplace les activations le long d'une direction « véridicité » |
| **Activation steering / RepE** | flux résiduel | Zou et al. 2023 ; « Circuit Breakers » Rimsky 2024 | ajoute un vecteur de direction aux activations pendant l'inférence |
| **Logit bias / décodage contraint** | logits avant softmax | `logit_bias` (API), `LogitsProcessor` (HF), Outlines | biaise l'échantillonnage sans toucher aux poids |
| **Grounding par récupération (RAG)** | contexte / conditionnement | standard | conditionne la génération sur des documents indexés par CID |
| **Édition de poids (ROME / MEMIT)** | poids localisés | Meng et al. 2022 | modifie un fait localisé, sans réentraînement |

Les trois premières correspondent exactement à l'intention du texte : des interventions **dans l'espace latent**, à l'inférence, **sans réentraîner** le modèle. **LEACE** est le candidat naturel de la « matrice des gluons » : c'est de l'effacement de biais directionnel, mathématiquement défini, et non une image.

---

## 5. La limite qui conditionne tout : API *vs* local

La faisabilité réelle se heurte à un arbitrage **déjà tranché** dans ce dépôt, et qui n'était pas visible dans le texte d'origine :

| Régime | Ce qui est possible | Ce qui est impossible |
|---|---|---|
| **Par API** (choix acté — R3, [`arbitrages_rmp.md`](arbitrages_rmp.md) : `meta-llama/Llama-3.1-8B-Instruct`, plafond 10 USD) | logit bias, prompt/RAG, logprobs (partiels) | **accéder aux activations ou aux poids** ; aucun hook sur l'embedding |
| **En local** (poids ouverts, `transformers`/`vLLM`/`llama.cpp`) | forward hooks sur n'importe quelle couche, calcul d'une direction de biais, retrait (LEACE) ou déplacement (ITI/RepE) | — (nécessite la machine adéquate) |

**Conséquence :** le branchement sur l'embedding — le cœur du texte — exige de **tourner le modèle en local, sur ses propres poids**. Dans le cadre API déjà voté, on ne peut faire que du logit-bias et du RAG. Ce n'est pas un obstacle insurmontable ; c'est un **arbitrage de plus à consigner** au feuillet, avant toute implémentation.

---

## 6. Ce qu'on ne dit plus (sur-claims retirés)

Le texte d'origine contenait quatre affirmations qui dépassaient le dépôt. Elles sont retirées, avec leur motif :

| Sur-claim retiré | Motif |
|---|---|
| « neutralise les biais systémiques » | Aucune méthode ne *neutralise* ; on **réduit** des biais **mesurables**, sur des benchmarks précis. |
| « neutralité épistémologique » | La neutralité est une position, non un état atteignable. Le manifeste (§5.4) est plus juste : le protocole « s'ajuste à la qualité de la question ». |
| « correction instantanée aux basses couches » | Décrit un code qui n'existe pas. Le dépôt ne contient, côté exécutable, que [`BGateTransduction`](../core/mttv_b_gate_triptych.md) (scalaire), [`mttv_mpvr_quorum.py`](../mpvr-glocal/README.md) (simulation) et [`Sigma4Activation`](t4_activation_function.md). |
| « le MPVR détecte immédiatement » | MPVR est un cadre conceptuel + une simulation, pas un service de validation en production. |

---

## 7. Le garde-fou anti-Goodhart

Un mécanisme qui « applique une correction » vers un « dictionnaire transductif » fixe est un **objectif d'optimisation** — donc corruptible. C'est le risque exact que [`note_signature_ancrage.md`](note_signature_ancrage.md) nomme « Goodhartisation » : la corruption par l'optimisation.

Deux protections, cohérentes avec le noyau :

1. **On ne vise pas « la neutralité »** (inatteignable), on vise « **biais réduit, mesuré sur tel benchmark, à tel seuil** » — seuil fixé **avant** l'exécution, conformément au programme du banc ([`arbitrages_rmp.md`](arbitrages_rmp.md) §G).
2. **Les directions de biais sont calculées sur un corpus de contraste que quelqu'un choisit.** Le choix reste humain, traçable, révisable. C'est un atout — pas un défaut à masquer.

---

## 8. Statut du texte d'origine — registre des refus

Conformément au registre des refus ([`arbitrages_rmp.md`](arbitrages_rmp.md) §F), les options écartées sont conservées avec leur motif :

- **« Matrice des gluons » comme mécanisme** — écarté. La métaphore QCD ne peut pas être présentée comme un opérateur d'inférence ; retenue uniquement comme **image d'intention**, au même titre que la triade Ψ-B-Φ.
- **« Neutralisation / neutralité épistémologique »** — écarté. Remplacé par « réduction de biais mesurable ».
- **« Correction instantanée aux basses couches »** — écarté tant que le code n'existe pas. Remplacé par la cartographie du §4, à transformer en spécification si le collectif le décide.

**Prochaine action, si le collectif souhaite aller plus loin :** transformer le §4 en **annexe technique** (spécification testable LEACE/ITI/RepE + grounding CID + benchmark de biais), en commençant par consigner au feuillet l'arbitrage « API *vs* local » — car il conditionne tout le reste.

---

*Note d'atelier versée pour relecture — rien n'est implémenté par cette note. Les décisions dépendantes relèvent du feuillet [`arbitrages_rmp.md`](arbitrages_rmp.md).*
