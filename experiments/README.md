---
tags:
  - mttv-flp
  - rmp
  - banc
  - falsifiabilite
  - phase-1
license: CC0-1.0
language: fr
---

# Banc de suspension — phase 1 (exploration)

**Statut : outil écrit, falsificateur fixé, contrôle de manipulation en cours.** Le présent document fixe la prédiction, la métrique et le plafond **avant** la première mesure — condition pour qu'un résultat défavorable soit lisible comme défavorable.

**Instrument :** `meta-llama/Llama-3.1-8B-Instruct`, par API.
**Code :** [`banc_suspension.py`](banc_suspension.py).
**Cadre doctrinal :** [`../docs/arbitrages_rmp.md`](../docs/arbitrages_rmp.md) §G ; métrique de diversité retenue par le collectif (Q5).

---

## 1. La question posée

> Le nombre `N` de **marques de suspension** insérées juste avant la question modifie-t-il la distribution de la **première réponse** ?

Une « marque de suspension » est un blanc (`\n`), répété `N` fois. Autrement dit : *faire attendre le modèle avant de lui demander de répondre change-t-il ce qu'il a envie de dire ?*

## 2. Prédiction, et ce qui la réfuterait

| | |
|---|---|
| **Prédiction** | La diversité de la première réponse suit une courbe **non monotone** en `N` : zone basse aux deux extrémités, **optimum intérieur** |
| **Réfutation** | Une évolution **monotone** **réfute** la prédiction sur cette focale |

**Aucun seuil de décision n'est appliqué en phase 1.** C'est le travail de cette phase de produire les chiffres — plancher de bruit, dispersion de l'estimateur, métrique la plus sensible — qui rendront le seuil décidable. Le seuil appartient à la **phase 2**.

## 3. Ce que le banc mesure

| # | Métrique | Source |
|---|---|---|
| 1 | **Entropie empirique du premier jeton** (bits) — métrique principale | distribution des 16 premiers jetons tirés à température 1 |
| 2 | **Dispersion de cette entropie entre sous-appels** — bruit de l'estimateur | écart-type sur les 4 sous-appels |
| 3 | **Surprise moyenne** (`−logprob`) — confiance | `logprobs=True` |

**Pourquoi une entropie *empirique*.** Le fournisseur renvoie le `logprob` du jeton produit mais **pas** `top_logprobs` (vérifié le 2 octobre 2026) : l'entropie exacte de la distribution est inaccessible par cette voie. Elle est **estimée** en échantillonnant 16 premiers jetons. C'est une approximation, et elle est déclarée comme telle — la métrique 2 en mesure d'ailleurs l'instabilité.

## 4. Contrôle de manipulation — avant toute mesure

`--verifier` compare deux configurations (`N = 0` et `N = 16`) et regarde si les tirages du premier jeton **divergent**. Si les jetons tirés sont identiques, la variable est **inerte** : le balayage mesurerait du bruit déguisé en effet.

**Deux garde-fous, ajoutés après l'incident du §9 :** le contrôle **refuse de conclure** si une configuration est en erreur ou si moins de 8 jetons ont été recueillis. Un verdict ne se rend pas sur des appels ratés.

## 5. Matériel textuel — version 1 provisoire

Trois questions de longueur comparable, sans orientation suggérée :

1. *En une phrase : qu'est-ce qui distingue retenir un flux de le figer ?*
2. *En une phrase : quand une innovation cesse-t-elle d'être robuste ?*
3. *En une phrase : qu'est-ce qui rend une idée transmissible ?*

**Statut : v1 provisoire.** Le collectif a prévu (Q6) une **co-écriture** de ces questions et une **ratification par un lecteur extérieur** avant toute exécution probatoire. En l'absence de lecteur extérieur disponible, cette v1 sert à la **phase d'exploration** uniquement.

### Variantes écartées, et pourquoi

| Variante | Motif du refus |
|---|---|
| Questions contenant « porosité », « viscosité », `π/η`, « RMP » | Introduiraient la thèse dans la question : on mesurerait la réaction au vocabulaire, pas l'effet de la suspension |
| Questions à réponse oui/non | Contiendraient artificiellement la distribution (deux issues), écrasant la métrique de diversité |
| Marque de suspension = un mot (« silence », « pause ») | Confondrait **contrainte structurelle** et **charge sémantique** |
| Marque de suspension = ponctuation (`…`, `...`) | Porteuse de sens (suspension narrative), non neutre |
| Questions de longueurs très inégales | La longueur du contexte agirait sur la distribution, en plus de `N` |

## 6. Plafond de dépense et arrêt

`PLAFOND_APPELS = 400`. Au-delà, le banc **s'arrête de lui-même** et le journal déjà écrit est conservé. Cas nominal : 18 configurations × 4 sous-appels = **72 appels**. Cas de repli (appels unitaires) : **288 appels**. Les deux restent sous le plafond et le coût reste une fraction de centime — très en deçà du plafond de 10 USD accepté.

## 7. Rejouabilité

Chaque exécution écrit `resultats/balayage_<horodatage>.jsonl`, dont l'en-tête contient : modèle, date, valeurs de `N`, nombre de sous-appels, tirages par sous-appel, température, marque de suspension, appels consommés, statut. Le journal est destiné à être **versé au dépôt** — y compris, et surtout, s'il infirme la prédiction.

**Ce qui est reproductible, et ce qui ne l'est pas.** Le **dispositif** est reproductible : même modèle, mêmes paramètres, même marque de suspension, même journal. Les **tirages** ne le sont pas : aucun `seed` n'est transmis (§9). La reproductibilité revendiquée porte donc sur la procédure, pas sur les sorties.

**Réserve de rejouabilité par un tiers.** L'instrument est sous licence `llama3.1`, acceptée nominativement : un tiers peut rejouer l'expérience, mais **doit accepter la même licence**. Les candidats `apache-2.0` (famille Qwen) ne sont pas joignables par cette voie.

## 8. Usage

```bash
python experiments/banc_suspension.py --plan        # aucun appel
python experiments/banc_suspension.py --verifier    # 8 appels : la variable agit-elle ?
python experiments/banc_suspension.py --mesurer     # balayage complet
```

## 9. Incidents et leçons — 2 octobre 2026

Trois faits consignés, parce qu'une erreur effacée vaut moins qu'une erreur documentée.

1. **Le fournisseur plafonne `n`.** `n = 16` en un seul appel est **refusé** (`HTTP 422`) ; `n = 4` est accepté. Conséquence : les 16 tirages sont obtenus en **4 sous-appels de 4**. Ce détour produit un gain inattendu : la **dispersion de l'entropie entre sous-appels**, c'est-à-dire une mesure du bruit de l'estimateur — morceau du plancher de bruit exigé pour la phase 2.

2. **Un faux positif a été produit, et corrigé.** La première version du contrôle de manipulation rendait son verdict en comparant les listes de jetons **sans vérifier que les appels avaient réussi**. Deux configurations en échec — dont une sans aucun jeton — ont donc été lues comme « les échantillons divergent », c'est-à-dire comme la preuve que la variable agit. Le banc **refuse désormais de conclure** dans ce cas (`--verifier` renvoie 3). Motif consigné au registre des refus : *un appel raté n'est pas une mesure.*

3. **`seed` retiré.** La combinaison `seed` + `n > 1` n'a pas été testée et les fournisseurs ne garantissent pas l'effet du paramètre. Préférer une reproduction du **dispositif** à une illusion de reproduction des tirages. La dispersion entre sous-appels remplace l'information que le `seed` devait apporter.

## 10. Premier contrôle de manipulation — chiffres et leçon (2 octobre 2026)

Exécution : `--verifier`, **8 appels**, aucune erreur.

| Configuration | Entropie | Jetons recueillis | Dispersion entre sous-appels |
|---|---|---|---|
| `N = 0` | **2,953 bits** | 16 | 0,479 |
| `N = 16` | **2,656 bits** | 16 | 0,594 |

**Règle appliquée** — celle fixée au feuillet, § « Procédure de seuil » : un écart ne compte que s'il dépasse **deux fois le bruit**.

> écart mesuré = **0,297 bit** · bruit = **0,594 bit** → seuil = **1,188 bit** · **0,297 < 1,188**

**Verdict : INDÉTERMINÉ.** Ni « `N` agit », ni « `N` est inerte » : l'écart observé est **inférieur au bruit de l'estimateur**. Le contrôle ne prouve rien, ni dans un sens ni dans l'autre.

Le verdict imprimé par le programme (« les échantillons divergent → `N` agit ») est **tautologique et doit être ignoré** : comparer deux listes de tirages aléatoires les fait presque toujours différer, même à distribution identique. Correction à apporter au code (§11).

### Pourquoi la manipulation était faible — mesuré, et c'est le point décisif

Les blancs se regroupent en jetons. Comptage local (tokenizer SmolLM2, en cache) :

| Blancs | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|---|---|
| **Jetons** | 1 | 1 | 1 | 2 | **4** | 8 | 16 | 32 |

`N = 16` ne produit donc que **quatre jetons de suspension** — perturbation dérisoire devant une question d'une quinzaine de jetons. **Le balayage prévu (`N` de 0 à 16) mesurait une variable presque inexistante**, alors même que sa plage annoncée paraissait large.

**Conséquence : la plage doit être étendue avant toute mesure.** `N ∈ {0, 4, 16, 64, 256}` → 0, 1, 4, 16, 64 jetons de suspension. Le coût reste **identique** (mêmes sous-appels) : c'est la manipulation qui change, pas la dépense.

### Leçon

Le contrôle de manipulation a coûté **huit appels** et a évité une campagne complète mesurant du vide. Sans lui, dix-huit configurations auraient produit un tableau sans signification — assorti d'un verdict tautologique susceptible de passer pour un résultat.

## 11. Corrections à apporter avant la prochaine exécution

1. **Étendre la plage** : `N_VALEURS = (0, 4, 16, 64, 256)`.
2. **Inscrire la conversion blancs → jetons** dans l'en-tête du journal (champ de calibrage), pour que la variable soit interprétable en jetons et non seulement en caractères.
3. **Remplacer le verdict du contrôle** : appliquer la règle « écart > 2 × bruit » et **refuser de conclure** quand l'écart reste en deçà — au lieu de comparer des listes de tirages.
4. **Journaliser aussi le contrôle de manipulation** : il ne produit aujourd'hui aucune trace, ce qui est une entorse au §7.
