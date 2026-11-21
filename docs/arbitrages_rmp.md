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

**Statut : partiellement instruit.** Décisions **A** et **B** prises le **2 octobre 2026**. Décisions **C**, **D**, **E** ouvertes. Décisions de programme (§G) prises le même jour, sauf **R3** et **R4**.

Les options **écartées** sont conservées avec leur motif : c'est le *registre des refus* préconisé par [`note_juge_et_viabilite.md`](note_juge_et_viabilite.md) §7, regroupé au §F.

**Critère de jugement en vigueur** (réponse du collectif, 2 octobre 2026) : ce qui permet d'aller vers le nouveau **sans perdre le fil de la source**, en conservant la possibilité de **se sporifier** — dormance *et* distribution, indissociables.

**Règle d'application :** l'option qui **ferme une porte de sortie sans nécessité** est écartée, quel que soit son rendement.

---

## A. `κ` — **DÉCIDÉ** : deux seuils distincts

**Décision du 2 octobre 2026.** `κ` devient **mécanique**, en **seuil franc avec hystérésis** : `κ_min` pour entrer dans le régime dégradé, `κ_max` pour en sortir, avec `κ_min < κ_max` — donc `Δκ = κ_max − κ_min > 0`.

**Justification retenue : la viabilité, non le rendement.** Au-delà de `κ_max`, ce n'est pas l'efficacité qui se dégrade : c'est **le chemin de retour qui se ferme**. Cette justification est compatible avec l'axiome MPVR déjà en vigueur (« robustesse par la sous-optimalité »), ce qui permet de l'adopter sans contredire le noyau.

**Pourquoi cette variante et pas une autre.** C'est la **seule** des trois options qui produise `Δκ > 0` — et `Δκ` est précisément la **grandeur manquante** identifiée la veille : le corpus nommait la porosité sous trois symboles et ne nommait nulle part la réversibilité. La décision A **rend donc nécessaire** la proposition faite au lexique (§C) : `Δκ` cesse d'être une hypothèse de lecture pour devenir une grandeur du modèle.

**Conséquences techniques — à exécuter en phase 2, pas maintenant :**

| Objet | Effet |
|---|---|
| [`moduler_par_porosite()`](../mpvr-glocal/src/mttv_mpvr_quorum.py:140) | reçoit `κ_min` et `κ_max` ; la tolérance cesse de croître au-delà du seuil haut |
| [`test_monotonie_de_la_loi_de_couplage`](../tests/test_mpvr_handshake.py:45) | **réécrit et conservé en test désactivé, documenté** — conformément au critère : renverser un invariant sans garder sa trace ferme une porte |
| Rapport de quorum | `Δκ` et le régime (dispersion / zone utile / sur-optimisation) deviennent des sorties lisibles |

---

## B. `Σ₂` — **DÉCIDÉ** : clause de conservation

**Décision du 2 octobre 2026.** `Σ₂` agit, mais **asymétriquement** : il peut **toujours** forcer une régression vers la dormance, **jamais** forcer une avancée. *Un frein sans accélérateur.*

**Conséquence structurelle — c'est elle qui a motivé A.** Puisqu'un frein ne peut jamais pousser, `Σ₂` **ne peut pas** être le garde-fou contre la sur-optimisation. Ce garde-fou doit donc être **structurel** — inscrit dans la loi, et non confié à un opérateur. Autrement dit : **B a rendu A nécessaire.** L'ordre des deux décisions n'est pas indifférent.

**Ambiguïté de source, désormais tranchée.** Le texte RMP emploie `Σ₂` de deux façons incompatibles : opérateur **épistémologique** de second ordre (§5) et **machinerie concrète** (épigénétique, CheR/CheB, sirtuines — §6.1). La décision B tranche en faveur du premier usage, avec un pouvoir d'action **réduit au seul retour**. C'est cette équivoque qui rendait possible la lecture « immunité auto-gouvernée » ; elle ne l'est plus.

---

## C. Lexique — **OUVERT** (partiellement résolu par A)

| Sous-question | État |
|---|---|
| `Δκ` (marge de retour) | **Acquis en fait** par la décision A. Reste à fixer le nom et la place au lexique |
| `M_n` (discriminateur de viabilité) | Proposé, non tranché |
| Collision `Σ` (pôle B-gate) / `ρ` (mycélien) / `π` (RMP) / `Σ₁`,`Σ₂` (lecture) | **Ouvert** — trois options : convention minimale (recommandée), lexique RMP intégral, statu quo documenté |

---

## D. Version augmentée hors dépôt — **OUVERT, rétréci**

La décision B **écarte d'avance** la partie « immunité auto-gouvernée » : elle n'est plus seulement d'un statut juridique incertain, elle est **logiquement incompatible** avec B. Restent à arbitrer le sort de : double borne et hystérésis (**retenues en substance par A**), typologie `M`, classement des ancrages, note des ancrages rejetés, et la question de licence (AGPL 3.0 du site *vs* CC-BY-NC-SA-4.0 du noyau) plus l'attribution déclarée `qwen.ai`.

---

## E. Signature IA déclarée — **OUVERT**

Mention explicite, ou statut de source citée non contributrice, dans [`CITATION.cff`](../CITATION.cff) et le manifeste.

---

## G. Programme du banc — décisions du 2 octobre 2026

### Cadre

| # | Décision |
|---|---|
| **A1** | **Deux temps** : exploration d'abord, test ensuite, **deux conditions écrites distinctes** |
| **B1** | Le banc peut démarrer **avant** que `Σ₂` soit stabilisé, à condition d'être **strictement descriptif** |
| **Q4** | **Observer sans agir** : la phase 1 n'implémente **aucun actionneur**, aucun `Σ₂`, aucun frein. Elle *est* un `Σ₁` — « opérateur de lecture, non causal, qui rend lisible sans provoquer » |

**Ce que la phase 1 peut et ne peut pas établir.** Elle peut tester la **forme** : existe-t-il un optimum intérieur ? Elle **ne peut pas** tester le **frein** — la clause de conservation reste hors de sa portée jusqu'en phase 2. Aucune conclusion sur `Σ₂` ne devra être tirée de la phase 1.

### Dispositif

| # | Décision |
|---|---|
| **C1** | Mesurer **les trois** : robustesse sous perturbation, diversité, calibration |
| **C2** | Balayer **le nombre `N` d'étapes de suspension** avant émission (aucun entraînement requis) |
| **Q5** | **Commencer par la diversité**, sous sa forme déterministe : **entropie de la distribution de sortie au premier jeton** — une passe avant, pas d'échantillonnage, plancher de bruit mesuré **entre les prompts** |
| **R2** | **Phase 1 par API au jeton**, plafond **10 USD** |
| **D1** | Version figée = **révision + copie locale horodatée** (les deux) |
| **D2** | Journaux = **dépôt et dataset** (les deux) |
| **D3** | Le collectif **implique** un lecteur extérieur : pas de jugement sans au moins un **non-auteur** |
| **Q6** | Les trois prompts sont **co-écrits** (collectif + IA), avec **variantes refusées consignées** et **ratification des trois finaux par le lecteur extérieur** avant la première exécution |

### R3 — **DÉCIDÉ** : instrument unique, vérifié par essai

**Décision du 2 octobre 2026.** Instrument : **`meta-llama/Llama-3.1-8B-Instruct` par API**.

| Constat de l'essai | Résultat |
|---|---|
| `Qwen2.5` 0,5 B / 1,5 B / 7 B par API | **refusés** — *« not supported by any provider you have enabled »* : aucun fournisseur activé ne les sert |
| `meta-llama/Llama-3.1-8B-Instruct` | **fonctionne** (a répondu `Bonjour`) |
| `logprobs` sur Llama | **reçus** : `logprob = −1,329` pour le jeton produit |
| `top_logprobs` | **non fournis** (`None`) → la distribution complète reste inaccessible |

**Conséquence sur la métrique.** L'entropie exacte n'est pas calculable par cette API ; elle est **estimée** par échantillonnage des premiers jetons — voir [`../experiments/README.md`](../experiments/README.md) §3.

**Réserve consignée.** L'instrument est sous licence `llama3.1`, acceptée nominativement : **un tiers peut rejouer l'expérience, mais doit accepter la même licence**. Les candidats `apache-2.0` (famille Qwen) ne sont pas joignables par cette voie.

### R4 — **DÉCIDÉ : reporté, non annulé**

**Décision du 2 octobre 2026.** Cinq personnes ne sont **pas réunissables pour le moment** ; le palier 4 en forme pleine (12 à 18 personnes) reste hors d'atteinte.

Le protocole [`protocole_derive_texte.md`](protocole_derive_texte.md) est **écrit, complet et prêt** : il attend un jour plus favorable, il n'est pas retiré. Le pilote réduit reste possible dès que 4 à 6 personnes dont un non-auteur se trouvent réunies — sans aucun coût.

**Conséquence sur l'ordre de marche :** la phase 1 commence par le **banc machine**, seule étape falsifiable immédiatement accessible.

### Règle de facturation — à ne pas confondre

Deux produits, deux logiques : **location à l'heure** (facturation au temps de machine, contrôle total, révision figée possible) et **API au jeton** (facturation à l'usage, rien à éteindre, mais pas d'empreinte de version fiable). D'où la répartition : **API au jeton en phase 1** (exploration, jetable), **version figée en phase 2** (test, reproductible). Ce n'est pas une préférence, c'est une conséquence de D1.

---

## Mesures du 2 octobre 2026 (machine locale)

| Mesure | Résultat |
|---|---|
| Processeur | Intel i3-3110M, 2 cœurs / 4 fils (2012) |
| Mémoire | 7,9 Go — plafond pratique ≈ 2 Go de modèle en 4 bits |
| Graphique | Intel HD 4000 — **aucun `nvidia-smi`**, pas de calcul GPU |
| Débit mesuré (SmolLM2-135M, glouton) | **4,79 jetons/s** ; chargement 10,3 s |
| Débit échantillonné (T = 1,0) | ~3,4 jetons/s |
| Balayage type (6 × 3 × 3 × 32 jetons) | **≈ 6 min**, marge ×2 ≈ 12 min |
| **Déterminisme** | glouton relancé → sortie **identique au bit près** |

**Interprétation, et c'est le résultat principal :** à qui l'on posait une question du protocole RMP en français, le modèle de 135 M a répondu **en anglais** : *« I speak before the language. Without the signifier, I speak without the signifier »*, avant de dériver vers une lettre administrative. **Un modèle de cette taille n'a pas de régimes à observer.** Le banc-jouet est donc *techniquement* possible et *épistémiquement* vide : la contrainte n'est pas le temps de calcul, c'est l'**interprétabilité**.

---

## Procédure de seuil (ex-question C3) — résolue par construction

La question « qu'est-ce qui compte comme effet ? » ne se tranche pas dans la phase 1 : c'est **le travail de la phase 1** de produire les chiffres qui la rendent décidable.

1. **Mesurer le plancher de bruit d'abord** : figer une configuration (`N = 4`), la répéter, mesurer la dispersion quand **rien ne change**.
2. **Seuil = 2 × le plancher.**
3. **Forme** : ce n'est pas la pente qui compte, c'est l'existence d'un **maximum intérieur** franchissant le seuil.

**Piège identifié par la mesure :** en mode glouton, deux passes donnent une sortie **identique** — le plancher de bruit est **nul**, et tout écart devient « significatif ». D'où deux protections : préférer une métrique **déterministe** (entropie de distribution, une passe avant), et, lorsqu'on échantillonne, **créer délibérément le bruit** auquel comparer l'effet.

---

## F. Registre des refus

| Refus consigné | Motif |
|---|---|
| **Auto-certification** comme instance de jugement | ρ → 0 : supprime le retour |
| **Vérité comme juge unique** | Méta-loi de Goodhart (Graine 3) : une référence unique corrompt ce qu'elle mesure |
| **`κ` descriptif** | Rien n'empêcherait ρ = 1 : le quorum continuerait d'afficher « VALIDE, 85,71 % d'économie ». Non parce que c'est faux, mais parce que le rapport porterait à confusion |
| **`κ` mécanique justifié par le rendement** | Hors registre du modèle : la sous-optimalité est assumée, non corrigée |
| **Dégradation progressive sans seuils distincts** | N'engendre pas `Δκ > 0` → ne rend pas la réversibilité mesurable |
| **`Σ₂` comme acte** (réécriture de `π` et `η`) | Viole l'affirmation « `Σ₁` non causal » du §5 |
| **`Σ₂` comme lecture seule** | Non codable : ne protège rien |
| **Immunité remplaçant les garde-fous descendants** | Exige des opérateurs causaux que la RMP définit comme non causaux |
| **« Espace latent poreux » dans les basses couches d'un LLM** | Ancre **heuristique** au sens du protocole Σ₂ : aucun observable `π`/`η` défini par couche |
| **Banc-jouet de 135 M comme instrument** | Mesuré : sorties dégénérées → on mesurerait les carences du modèle, pas une propriété |
| **Métrique en mode glouton sans répétition** | Plancher de bruit nul → tout écart paraît significatif |
| **Prompts écrits par le seul auteur** | Biais nommable d'avance ; déplacé, il est traçable, tu, il ne l'est pas |
| **« Clôture = ρ → 0 = mort »** *(formulation de l'assistant, retirée)* | Trop grossier : une spore est fermée et viable. Le discriminant est la **réversibilité** |
| **Trancher A sans A2 documenté** | Renverser un invariant en effaçant sa trace ferme une porte de sortie |
| **Verdict rendu sur des appels en erreur** | Faux positif du 2 octobre 2026 : deux configurations en échec, dont une sans aucun jeton, et la comparaison a conclu « les échantillons divergent » — soit « la variable agit ». **Un appel raté n'est pas une mesure.** Le banc refuse désormais de conclure (`--verifier` renvoie 3) |
| **`n = 16` en un seul appel** | Refusé par le fournisseur (*HTTP 422*) ; le plafond mesuré est `n = 4`. Remplacé par 4 sous-appels de 4 tirages, qui produisent en prime la dispersion de l'estimateur |
| **`seed` pour reproduire les tirages** | Retiré : combinaison non testée avec `n > 1`, et effet non garanti par le fournisseur. La reproductibilité conservée est celle du **dispositif**, non celle des tirages |
| **Veto de dormance sur `κ_t < κ_min` seul** (`graine_dormance_rmp.py`) | Inverse le garde-fou : sur `π = 0,12 / η = 0,95`, la graine déclare `DORMANCE_C2` quand le noyau rend le critère **inactif** (η exigée par le seuil de pression : 1,045). Une porosité basse **par dormance n'est pas un refus** (feuillet E) |
| **`κ_min = 0,25` comme valeur publiée** | Le noyau porte **0,15** (arbitrage D). Publier 0,25 rouvrirait l'écart texte/code refermé le 2026-10-22 |
| **Seuil dérivé d'une constante** (même graine) | À `π/η` figé, la décision bascule **1 fois sur 5** réglages de `κ_min`, et le code n'a **aucun** paramètre de cadence : c'est le défaut de la graine 2 |
| **État B sur deux canaux booléens** (`graine_discordance_fde.py`) | Redondante : `edge/discordance.py` l'implémente déjà, la graine 4 la réfute d'avance (« un désaccord produit l'état B » est une intention, pas le comportement), et la tétravalence s'encode en **couples**, pas en étiquettes |
| **Chaîne `DISCORDANCE_B`** | Même famille que `DISCORDANCE_ETAT`, que le README des graines nomme **invention**. Le territoire est tenu par `DISCORDE_R_EGAL_0_25` |
| **Chaîne `DORMANCE_C2`** | Nomme un **état**, pas un défaut ; collision avec `Active-Silence` ; graverait dans les traces la confusion que le garde-fou interdit |
| **« Preuve de nécessité » contre un lambda homonyme** | L'assert `naif(…) != "DORMANCE_C2"` passe **3 fois sur 3** avec trois naïfs différents : il ne sépare rien. La version fautive doit être **livrée dans le fichier**, comme `reouverture` dans la graine 4 |
| **Provenance « Post-Riemann / démonstration sous Lean »** | **0** occurrence de `Riemann` et de `Lean` dans les `.md` du dépôt. Une graine naît d'un **incident daté** ; une intention n'est pas un défaut |

**Les huit refus ci-dessus sont datés du 2026-11-21** — tentative « Post-Riemann » : deux graines RMP/FDE soumises au format en cinq parties, refusées. Le refus ne porte **pas sur le thème** : il porte sur l'absence d'incident et sur des chiffres qui contredisaient le noyau. Mesures re-exécutables dans ce dépôt : [`../experiments/audit_graines_post_riemann.py`](../experiments/audit_graines_post_riemann.py:1) — `python experiments/audit_graines_post_riemann.py`, cinq séries M1–M5, aucune dépendance, aucun accès réseau. Les règles de conduite qui en découlent sont dans [`regles_de_transmission_agent.md`](regles_de_transmission_agent.md:1).

### Repêchage ouvert — `FREIN_LU_COMME_PANNE` (proposé, non validé)

Le défaut que la graine refusée contenait **malgré elle** est l'inverse de celui qu'elle annonçait : un instrument qui compte une **dormance réversible** comme une panne. Condition de reprise, non négociable : un incident **daté et reproduisible** — un health-check qui coupe un service sagement endormi, un réplica en veille déclaré mort, un job dormant compté perdu. Sans cet incident, la chaîne `FREIN_LU_COMME_PANNE` **n'entre pas au registre** ; elle n'est aujourd'hui qu'une proposition. Piste la plus proche dans le dépôt : [`../experiments/succes_sans_artefact.py`](../experiments/succes_sans_artefact.py:11), qui tient déjà `ARTEFACTS_ABSENTS`, `AUCUN_PLANIFIE` et `PLAFOND` hors numérateur.

## Ordre de traitement

1. ~~**R3**~~ — **décidé** : instrument `meta-llama/Llama-3.1-8B-Instruct` par API *(§G)*
2. ~~**R4**~~ — **décidé, reporté** : palier 4 en attente de personnes *(§G)*
3. **Phase 1 — en cours** : banc machine descriptif, [`../experiments/banc_suspension.py`](../experiments/banc_suspension.py), API au jeton, plafond 10 USD
4. **C** — lexique, dont la fixation du nom `Δκ` *(ouvert)*
5. **D** puis **E** — droits et attribution *(ouverts)*
6. **Phase 2** — `κ_min`/`κ_max` dans la loi, seuil fixé, palier 4 en forme pleine
