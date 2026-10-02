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

**Statut : outil écrit et versionné, exécution non lancée.** Le présent document fixe la prédiction, la métrique et le plafond **avant** la première mesure — condition pour qu'un résultat défavorable soit lisible comme défavorable.

**Instrument :** `meta-llama/Llama-3.1-8B-Instruct`, par API.
**Code :** [`banc_suspension.py`](banc_suspension.py).
**Cadre doctrinal :** [`../docs/arbitrages_rmp.md`](../docs/arbitrages_rmp.md) §G ; métrique : la diversité de la première réponse est le proxy retenu par le collectif (Q5).

---

## 1. La question posée

> Le nombre `N` de **marques de suspension** insérées juste avant la question modifie-t-il la distribution de la **première réponse** ?

Une « marque de suspension » est un blanc (`\n`), répété `N` fois. La question est donc : *le fait de faire attendre le modèle avant qu'on lui demande de répondre change-t-il ce qu'il a envie de dire ?*

## 2. Prédiction, et ce qui la réfuterait

| | |
|---|---|
| **Prédiction** | La diversité de la première réponse suit une courbe **non monotone** en `N` : une zone basse aux deux extrémités, un **optimum intérieur** |
| **Réfutation** | Une évolution **monotone** (toujours plus, ou toujours moins, de diversité quand `N` croît) **réfute** la prédiction sur cette focale |

**Aucun seuil de décision n'est appliqué en phase 1.** C'est le travail de cette phase de produire les chiffres — plancher de bruit, dispersion, métrique la plus sensible — qui rendront le seuil décidable. Le seuil appartient à la **phase 2** (voir le feuillet).

## 3. Ce que le banc mesure

Trois quantités par configuration (une question × une valeur de `N`) :

| # | Métrique | Source |
|---|---|---|
| 1 | **Entropie empirique du premier jeton** (bits) — métrique principale | distribution des `ÉCHANTILLONS` premiers jetons tirés à température 1 |
| 2 | **Surprise moyenne** (`−logprob`) — confiance | `logprobs=True` |
| 3 | **Premiers jetons** eux-mêmes — trace brute | — |

**Pourquoi une entropie *empirique*.** Le fournisseur renvoie le `logprob` du jeton produit mais **pas** `top_logprobs` (vérifié le 2 octobre 2026). L'entropie exacte de la distribution est donc inaccessible par cette voie. Elle est **estimée** en échantillonnant 16 premiers jetons et en calculant l'entropie de leur distribution empirique. C'est une approximation, et elle est déclarée comme telle.

## 4. Contrôle de manipulation — avant toute mesure

`--verifier` compare deux configurations seulement (`N = 0` et `N = 16`) et regarde si les tirages du premier jeton **divergent**. Si les 16 jetons tirés sont identiques dans les deux cas, la variable est **inerte** : le balayage mesurerait du bruit déguisé en effet. Le balayage ne doit pas être lancé sans ce contrôle.

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
| Questions à réponse oui/non | Contiendraient artificiellement la distribution (deux issues seulement), écrasant la métrique de diversité |
| Marque de suspension = un mot (« silence », « pause », « attends ») | Confondrait **contrainte structurelle** et **charge sémantique** : `N` deviendrait un mot répété, donc un contenu |
| Marque de suspension = ponctuation (`…`, `...`) | Porteuse de sens (suspension narrative), non neutre |
| Questions de longueurs très inégales | La longueur du contexte agirait sur la distribution, en plus de `N` |

## 6. Plafond de dépense et arrêt

`PLAFOND_APPELS = 400`. Au-delà, le banc **s'arrête de lui-même** et le journal déjà écrit est conservé. Cas nominal : 18 appels ; cas de repli (si le fournisseur refuse `n > 1`) : 288 appels. Les deux restent sous le plafond, et le coût reste une fraction de centime — bien en deçà du plafond de 10 USD accepté.

## 7. Rejouabilité

Chaque exécution écrit `resultats/balayage_<horodatage>.jsonl`, dont l'en-tête contient : modèle, date, valeurs de `N`, nombre d'échantillons, température, graine, marque de suspension, nombre d'appels. Le journal est destiné à être **versé au dépôt** — y compris, et surtout, s'il infirme la prédiction.

**Réserve de rejouabilité.** L'instrument est sous licence `llama3.1`, dont l'acceptation est nominative : un tiers peut rejouer l'expérience, mais **doit accepter la même licence**. Un modèle `apache-2.0` rendrait l'expérience plus facilement reprenable. C'est une trace, pas un veto.

## 8. Usage

```bash
python experiments/banc_suspension.py --plan        # aucun appel
python experiments/banc_suspension.py --verifier    # 2 appels : la variable agit-elle ?
python experiments/banc_suspension.py --mesurer     # balayage complet
```
