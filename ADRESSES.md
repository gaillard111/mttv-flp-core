# Adresses du corpus — pointeurs stables

Ce fichier existe parce qu'un lien correct n'est pas encore un lien **atteignable par un tiers**. Il rassemble les adresses canoniques, la règle de branche, les trois formes d'URL GitHub et les pièges de nommage connus.

Dernière vérification : **2026-10-21**, commit `ce66be4`, branche `main`.
Contrôle effectué anonymement, sans authentification : 6 fichiers + 3 pages = HTTP 200, 0 lien mort.

---

## Règle de branche

Le dépôt porte **quatre branches** :

| Branche | Rôle |
|---|---|
| `main` | ligne courante, **seule à citer** |
| `master` | ligne ancienne, figée |
| `evolution/tetravalent-core` | travaux en cours |
| `our-files` | dépôt de fichiers |

Un lien qui n'indique pas `main` (ou un hash de commit) peut aboutir ailleurs ou à une version périmée. C'est la première cause de « je ne trouve rien » chez un lecteur.

**Forme recommandée pour un message public** : citer le hash, pas la branche.

```
https://github.com/gaillard111/mttv-flp-core/tree/ce66be4
```

---

## Les trois formes d'URL, et quand les utiliser

| Forme | Exemple | Poids servi | Usage |
|---|---|---|---|
| `tree/` (dossier) | `.../tree/main/expansion_v2026.5` | 216 Ko de HTML | navigation humaine |
| `blob/` (fichier) | `.../blob/main/EXPANSION.md` | 271 Ko de HTML pour 6 Ko de contenu | navigation humaine |
| `raw.` (brut) | `.../main/EXPANSION.md` | 6 Ko de texte pur | **lecture par une IA ou un outil** |

Le ratio est de l'ordre de **39:1** : une page GitHub sert 271 Ko de HTML pour rendre 7 Ko de markdown. Un outil qui plafonne la taille de récupération, qui extrait le texte sans exécuter JavaScript, ou qui refuse le HTML, échoue — alors que le fichier est parfaitement accessible.

**Pour une IA, donnez toujours l'URL `raw.githubusercontent.com`.** Elle répond 200 avec un `User-Agent` de robot (testé avec `GPTBot`), sans cookie ni JavaScript.

---

## 1. Expansion V2026.5 — quatre livrables

Dossier : `expansion_v2026.5/`

| Livrable | URL brute |
|---|---|
| Axe 1 — code exécutable | `https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/expansion_v2026.5/axe1_bgate_v2026_5.py` |
| Axe 2 — cinq graines | `https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/expansion_v2026.5/axe2_graines_v2026.5.md` |
| Axe 3 — system instructions | `https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/expansion_v2026.5/axe3_system_instructions_miroir_transduction.md` |
| Axe 4 — moirage transculturel | `https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/expansion_v2026.5/axe4_moirage_transculturel.md` |

Version figée (dossier) :
`https://github.com/gaillard111/mttv-flp-core/tree/ce66be4/expansion_v2026.5`

---

## 2. Feuillet d'arbitrages

| Forme | URL |
|---|---|
| lisible | `https://github.com/gaillard111/mttv-flp-core/blob/main/docs/arbitrages_expansion_v2026.5.md` |
| brute | `https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/docs/arbitrages_expansion_v2026.5.md` |
| figée | `https://github.com/gaillard111/mttv-flp-core/blob/ce66be4/docs/arbitrages_expansion_v2026.5.md` |

⚠️ **Deux fichiers voisins, à ne pas confondre** :

- `docs/arbitrages_expansion_v2026.5.md` — les trois points de la version 2026.5 (veto, κ, igic). Clos.
- `docs/arbitrages_rmp.md` — fichier **antérieur**, distinct, **toujours ouvert**.

---

## 3. Point d'entrée unique

```
https://github.com/gaillard111/mttv-flp-core/blob/main/EXPANSION.md
```

Index stable, sans numéro de version : carte du dépôt, tableau des expansions, notions concernées, section « Deux B-Gate distinctes », et section « vérifier plutôt que croire ».

Si un seul lien doit circuler, c'est celui-là.

---

## Quatre pièges de nommage

1. `axe2_graines_v2026.5.md` utilise un **point**, les trois autres fichiers un **souligné** (`v2026_5`). Une frappe approximative casse un seul des quatre liens, silencieusement.
2. Le dossier s'appelle `expansion_v2026.5` : aucun fichier ne porte ce nom. Un lien vers `.../blob/main/expansion_v2026.5` renvoie 404.
3. Il n'existe **aucune** version `V2026.4` dans le dépôt. Citer cette étiquette renvoie à rien.
4. Deux « B-gate » coexistent : celle de décodage/logits (`experiments/`) et celle de décision/gouvernance (`expansion_v2026.5/`). Voir la section correspondante d'`EXPANSION.md`.

---

## Protocole de vérification pour un tiers — humain ou IA

Si un lecteur, humain ou machine, déclare « l'accès échoue », ne pas discuter : demander trois choses.

1. **L'URL exacte essayée.** Une confusion `tree`/`blob`/`raw`, ou un nom de dossier pris pour un nom de branche, suffit à produire un échec.
2. **Le code HTTP obtenu.** 404 = l'adresse est fausse. 403/429 = quota ou filtrage côté client. 200 = le fichier est servi, l'échec est en aval (taille, JavaScript, extraction).
3. **La première ligne du contenu.** Si elle est citée, l'accès a fonctionné ; sinon, l'échec est réel et localisable.

Une IA qui ne peut pas joindre le réseau ne peut produire aucun code HTTP : c'est le seul discriminant fiable entre « je n'ai pas accès » et « je n'ai pas essayé ».

---

## Commande de contrôle

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" \
  https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/EXPANSION.md
```

Attendu : `200` suivi d'une taille non nulle. Toute autre sortie signale un problème d'adresse ou de réseau, jamais un problème de contenu.
