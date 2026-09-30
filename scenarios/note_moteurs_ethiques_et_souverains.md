# Note de cadrage — Moteurs de recherche éthiques et souverains

**Objet** : proposer un protocole d'application du framework MTTV-FLP à la couche la plus extractive du web : la recherche.
**Dossier** : `scenarios/` — applications du modèle dans la noosphère, l'agriculture, l'urbanisme.
**Statut** : note de travail. Rien n'est engagé, rien n'est envoyé.

---

## 1. Pourquoi la recherche concentre le problème

Un moteur de recherche est l'endroit où l'extraction est la plus pure : il **indexe** le travail d'autrui, le **résume**, le **classe**, et **monétise l'attention** obtenue. Le contenu humain y devient une matière première, et le lecteur y devient l'inventaire.

Depuis l'arrivée des résumés générés, la boucle s'est refermée : le moteur ne renvoie plus vers la source, il **répond à sa place**. La source n'est plus visitée, donc plus financée, donc plus produite.

C'est précisément le point que le MTTV-FLP désigne comme prédation cognitive — et c'est là que son apport peut être concret plutôt que théorique.

## 2. Ce qu'un moteur éthique et souverain cherche déjà

Les moteurs alternatifs poursuivent déjà trois objectifs que le framework rejoint :

| Objectif d'un moteur éthique | Correspondance dans le dépôt |
|---|---|
| Sobriété énergétique | `mpvr-glocal/` : quorum poreux, routage multi-chemins, **−64,9 % d'énergie en situation de crise** |
| Transparence & redevabilité | Traçabilité par conception : chaque nœud du modèle référence sa source |
| Multilinguisme réel | Traitement de la géométrie du langage **sans langue pivot** |

## 3. Quatre propositions concrètes

### 3.1 Attribution traçante

Toute réponse affiche **et lie** la source humaine. Non pas en bas de page, mais dans le corps de la réponse. Le protocole ne remplace pas la source : il structure le chemin vers elle.

> « L'IA devient un péage transparent : elle oriente vers la pensée humaine originale et redistribue la valeur à l'émetteur initial. »

### 3.2 Refus de la substitution

Un résumé généré qui remplace la source détruit l'écosystème qu'il exploite. La règle : **la synthèse renvoie à la source**, elle ne s'y substitue pas. Concrètement — un résultat de recherche ne devrait jamais être consommable sans que la source soit accessible et créditée.

### 3.3 Multilinguisme sans langue pivot

Aucune étape de traduction obligatoire vers une langue dominante. La proximité conceptuelle se calcule dans l'espace abstrait, pas par conversion (français → anglais → résultat). Conséquence directe pour un moteur européen : une requête en français, en breton ou en persan ne subit pas de **biais anglo-saxon** avant d'être traitée.

### 3.4 Routage multi-chemins plutôt que réponse unique

C'est l'apport le plus spécifique du module MPVR, et le plus directement applicable à la recherche.

Un moteur classique produit **une** réponse, la mieux classée selon un score unique. Le MPVR propose l'inverse : plusieurs chemins validés par **quorum poreux**, où les désaccords locaux ne sont pas écrasés mais conservés comme information.

Pour la recherche, cela signifie : sortir du **monopole de la réponse unique** et rendre visibles les perspectives divergentes au lieu de les moyenner.

## 4. Ce que le dépôt permet d'affirmer — et ce qu'il ne permet pas

**Affirmable aujourd'hui, vérifiable par un tiers :**

- Dépôt public et auditable : `github.com/gaillard111/mttv-flp-core`
- Archive citable avec DOI : `10.5281/zenodo.20830060` (Core 2026)
- Implémentation de référence publiée : `src/mttv_mpvr_quorum.py`
- Résultats de test publiés : `tests/test_sigma4.ipynb`, `tests/test_sigma4_report.md`
- Benchmark mesuré et daté (SOPH-IA) : `soph-ia/benchmark_T4_teaser.csv`, DOI `10.5281/zenodo.21414425`
- Licences explicites : CC-BY-NC-SA-4.0 (noyau), CC0-1.0 (MPVR), CC-BY-4.0 (SOPH-IA)

**Non affirmable à ce stade — à ne pas laisser entendre :**

- Aucun partenariat n'existe avec un moteur de recherche
- Aucun déploiement à l'échelle de production
- Le framework n'est pas une bibliothèque logicielle packagée et installable
- Les gains annoncés (−64,9 %, −30 % de temps total) portent sur des **bancs de test précis**, pas sur une charge de production

**Formuler ces limites est ce qui protège la crédibilité du reste.**

## 5. Note d'intention — texte prêt à envoyer

> **Objet : Protocole non extractif pour la recherche — proposition d'expérimentation**
>
> Madame, Monsieur,
>
> Les moteurs de recherche sont aujourd'hui la couche la plus extractive du web, et l'arrivée des résumés générés en accentue le mécanisme : la réponse se substitue à la source, qui n'est plus visitée ni financée.
>
> Le collectif Les Fils de la Pensée développe un framework alternatif, **auditable publiquement et archivé avec DOI citable**, qui poursuit trois objectifs proches des vôtres : sobriété énergétique mesurée, traçabilité native des sources, et traitement multilingue sans langue pivot.
>
> Nous proposons une expérimentation limitée et vérifiable : appliquer notre mécanisme de **routage multi-chemins à quorum poreux** à un échantillon de requêtes, et mesurer trois choses — la part de réponses renvoyant effectivement à la source, le coût énergétique par requête, et le maintien des perspectives divergentes au lieu de leur moyennage.
>
> Le dépôt, les tests et les licences sont publics ; les résultats sont reproductibles et les éventuels désaccords peuvent être discutés en *Issues*.
>
> Nous serions honorés d'en discuter.
>
> Collectif Les Fils de la Pensée — https://github.com/gaillard111/mttv-flp-core

**Destinataires publics à vérifier avant envoi** : `hello@ecosia.org`, `info@ecosia.org` — et l'adresse de contact indiquée sur le site d'Ecosia.

## 6. Checklist avant envoi

- [ ] Vérifier que les DOI cités résolvent (20830060, 21414425)
- [ ] Vérifier que le dépôt est public au moment de l'envoi
- [ ] Vérifier les adresses de contact sur le site officiel
- [ ] Relire la note d'intention à voix haute : si elle sonne comme une promesse, retirer une phrase
- [ ] Ne jamais présenter les chiffres de banc de test comme des résultats de production
