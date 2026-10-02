---
tags:
  - mttv-flp
  - rmp
  - reprise
  - journal
license: CC-BY-NC-SA-4.0
language: fr
---

# Point de reprise — chantier RMP / mycélisation

**Note de reprise**, rédigée le **2 octobre 2026** pour que l'état du chantier soit lisible **sans la conversation qui l'a produit**. Elle est volontairement factuelle : ce qui est fait, ce qui est mesuré, ce qui est ouvert, et le prochain geste exact.

**Critère de jugement en vigueur :** aller vers le nouveau **sans perdre le fil de la source**, en conservant la possibilité de **se sporifier** — dormance *et* distribution, indissociables. Voir [`note_juge_et_viabilite.md`](note_juge_et_viabilite.md).

---

## 1. Fait et poussé (dépôt `gaillard111/mttv-flp-core`)

| Commit | Objet |
|---|---|
| `754d9f4` | Annexe 3.1 (RMP) transcrite en Markdown **indexable** + raccords README et glossaire |
| `88b5178` | Fil Peirce rattaché (« quasi-esprit », sémiosis illimitée) · `η` **nommée** dans le code (`eta_retenue = 0.95`, comportement inchangé, test attesté) · `Δκ` et `M_n` proposés au lexique |
| `d515a58` | **Feuillet instruit** : `κ` à deux seuils distincts (A) · `Σ₂` clause de conservation (B) · programme du banc consigné · registre des refus ouvert |
| `fbf0398` · `eb053d3` · `42e64cc` | **Banc de suspension** : falsificateur fixé avant exécution, plafond de dépense, garde-fous, calibration en jetons, relevé des jetons d'entrée |
| `129d3c6` | Premier contrôle de manipulation : chiffres et leçon |
| `a6787b9` | **Sonde passive des couches internes** (attention, CKA, rang effectif, cristallisation) |

Documents créés : [`../protocols/rmp_mecanisme_pre_transducteur.md`](../protocols/rmp_mecanisme_pre_transducteur.md) · [`arbitrages_rmp.md`](arbitrages_rmp.md) · [`note_juge_et_viabilite.md`](note_juge_et_viabilite.md) · [`protocole_derive_texte.md`](protocole_derive_texte.md) · [`../experiments/banc_suspension.py`](../experiments/banc_suspension.py) · [`../experiments/sonder_couches.py`](../experiments/sonder_couches.py).

## 2. Mesuré (et non supposé)

### Machine locale
Intel i3-3110M, 2 cœurs · 7,9 Go de RAM · Intel HD 4000, **aucun calcul GPU** · 104 Go libres · `torch 2.12.1+cpu`, `transformers 5.12.1`.
Débit mesuré : **4,79 jetons/s** sur un modèle de 135 M (glouton), ~3,4 en échantillonné. **Glouton = sortie identique au bit près** ; l'échantillonnage est donc la seule source de variation.

### Accès par API (2 octobre 2026)
`meta-llama/Llama-3.1-8B-Instruct` **fonctionne** ; `logprobs` du jeton produit **reçus**, `top_logprobs` **absents**.: la distribution complète n'est pas accessible. Famille `Qwen2.5` (0,5 B / 1,5 B / 7 B) **refusée** : aucun fournisseur activé ne les sert. `n = 16` en un appel → **HTTP 422** ; `n = 4` accepté.

### Deux défauts trouvés et corrigés
1. **Faux positif** : un verdict a été rendu sur deux appels en échec (dont un sans jeton) → lu comme « la variable agit ». Le banc **refuse** désormais de conclure (`--verifier` renvoie 3). *Un appel raté n'est pas une mesure.*
2. **Manipulation vide** : les blancs sont **supprimés par le gabarit de conversation** — jetons d'entrée du prompt **identiques** (31) pour `N = 0` et `N = 256`. L'hypothèse « insérer des blancs » est **morte par mesure**. Le relevé des jetons d'entrée est désormais une **porte obligatoire** pour tout marqueur envisagé.

### Sonde interne — relevé de référence (SmolLM2-135M-Instruct)
Entrée 53 jetons · 30 couches · dimension cachée 576.

| Observable | Valeur |
|---|---|
| **Entropie d'attention** | max **3,62** (couche 0) → min **0,47** (couche 24) ; ressaut à 2,46 / 2,39 aux couches 10-11 |
| **CKA entre couches voisines** | ≈ **1,000** presque partout ; chutes à 0→1 (0,611), 1→2 (0,595), **9→10 (0,443)**, **11→12 (0,364)**, 29→30 (0,054) |
| **Rang effectif** | 33,6 (0) → 41,2 (10) → **1,4 (couches 12 à 15)** → ~2 (27) → **8,1** (29) → **32,8** (30) |
| **Cristallisation** | la prédiction ne se stabilise **jamais** avant la dernière couche ; prédiction finale : **un guillemet `"`** |

**Interprétation consignée :** le tiers médian de ce modèle est **écrasé à ≈ 1,4 dimension** ; le guillemet initial explique la dérive verbale observée par ailleurs (le modèle ouvre des guillemets, donc produit un texte qui ressemble à une citation). Sur cet instrument, l'« espace latent » n'est **pas poreux : il est comprimé**. C'est une mesure, pas un jugement.

## 3. Ouvert, et par qui

| Objet | État |
|---|---|
| **C** — lexique : nom de `Δκ`, convention `Σ` / `ρ` / `π` | ouvert, à trancher par le collectif |
| **D** — version augmentée de la RMP | ouvert ; **rétréci** par B (l'immunité auto-gouvernée est écartée pour raison logique, non juridique) ; reste la licence AGPL 3.0 *vs* CC-BY-NC-SA-4.0 |
| **E** — attribution `qwen.ai` dans `CITATION.cff` | ouvert |
| **R4** — palier 4 humain | **reporté**, faute de 5 personnes ; le protocole est écrit et prêt |
| **Corrections mineures** | journaliser la sonde (elle n'écrit aucune trace — entorse au §7) · relever les marqueurs qui survivent au gabarit |

## 4. Le prochain geste exact

1. **Profil de référence multi-questions** : rejouer la sonde sur 5 à 10 questions et 2 longueurs → obtenir une moyenne **et une dispersion** (le plancher de bruit) pour chaque observable.
2. **Comparaison d'instrument** : rejouer la **même** sonde sur `Qwen/Qwen2.5-0.5B-Instruct` en local (~2 Go, tient dans la RAM) → **le rang du tiers médian croît-il avec la taille ?** Ce serait la première mesure *comparative* de « porosité ».
3. **Définir l'intervention avant de mesurer** — le registre en contexte (Graines V1/V2/V3 : *« émettre une fréquence et observer si le système résonne »*), **et la direction attendue**. Sans cela, on finira par trouver un effet en cherchant assez.

## 5. Les règles qui gouvernent tout ce chantier

1. **Un écart ne compte que s'il dépasse deux fois le bruit.** Aucun résultat ne se lit hors de cette règle.
2. **Un appel raté n'est pas une mesure.** Aucun verdict sur des appels en erreur.
3. **Une manipulation non livrée est une manipulation vide** : vérifier qu'elle atteint le modèle, pas qu'elle est bien écrite.
4. **Falsificateur rédigé et versionné avant l'exécution**, jamais après.
5. **Consigner les refus** avec leur motif : ce que le corpus a écarté vaut autant que ce qu'il a retenu.
6. **Une erreur documentée vaut mieux qu'une erreur effacée** — cette note n'existerait pas sans deux faux pas corrigés.
