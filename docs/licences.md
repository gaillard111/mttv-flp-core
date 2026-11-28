# Licences — qui couvre quoi, et pourquoi

*Décision du 2026-11-02, révisée le 2026-11-27.*

Deux décisions se sont succédé, et la seconde ne remplace la première que pour l'avenir :

- **2026-11-02** — premier découpage : noyau en CC-BY-NC-SA 4.0 pour le protéger de l'extraction
  commerciale, documents de propagation en CC-BY-SA 4.0, manifeste et fragment MPVR en CC0.
- **2026-11-27** — le `NC` est retiré du noyau. Le noyau passe en **Apache-2.0**, les notices et
  protocoles en **CC-BY-SA 4.0**. Aucune version déjà déposée n'est concernée : voir §3.

## 1. Qui est sous quelle licence

La règle est **par extension de fichier** : elle se vérifie par une commande, pas par une
intention. Deux exceptions (CC0) l'emportent sur la règle d'extension.

| Périmètre | Fichiers | Licence | Texte |
|---|---|---|---|
| **Noyau exécutable** | tout `*.py`, `*.sh`, `*.c`, `*.html`, `*.yml`, `*.jsonl` — dont `src/`, `graines/`, `edge/`, `experiments/`, `expansion_v2026.5/`, `tools/`, `hf/`, `deploy/`, `scenarios/`, `soph-ia/` | **Apache-2.0** | [`LICENSES/Apache-2.0.txt`](../LICENSES/Apache-2.0.txt) |
| **Textes et documents** | tout `*.md`, `*.pdf`, `*.txt`, `*.cff`, `*.json` — dont `docs/`, `protocols/`, notices et protocoles | **CC-BY-SA 4.0** | [`LICENSES/CC-BY-SA-4.0.txt`](../LICENSES/CC-BY-SA-4.0.txt) |
| **Manifeste** *(exception)* | `docs/kit/04_MANIFESTE_POST_HYPERSCALER.md` | **CC0 1.0** | — |
| **Fragment MPVR** *(exception)* | `mpvr-glocal/` et `src/mttv_mpvr_quorum.py` | **CC0 1.0** | — |
| **Textes intégraux** | `LICENSES/` | licences officielles, non modifiées | — |
| **Versions ≤ 1.2.1** | archives Zenodo déjà déposées | **CC-BY-NC-SA 4.0**, inchangé | [`LICENSES/CC-BY-NC-SA-4.0.txt`](../LICENSES/CC-BY-NC-SA-4.0.txt) |

Le fichier [`LICENSE`](../LICENSE) n'est qu'un aiguillage : il renvoie ici. C'est volontaire — un
`LICENSE` unique aurait déclaré, pour une partie du dépôt, plus de droits qu'il n'en est accordé,
et un élargissement ne se reprend pas.

## 2. Ce que cela change pour vous

- **Noyau (Apache-2.0)** : vous pouvez l'intégrer dans un produit, y compris commercial, et **ne pas
  publier vos modifications**. En échange : conserver le texte de la licence et les mentions,
  signaler les fichiers modifiés, et accepter la concession de brevet et l'absence de garantie.
- **Textes (CC-BY-SA 4.0)** : vous pouvez les reprendre, traduire, adapter, y compris dans un cadre
  commercial, à condition de **citer** et de **partager à l'identique**.
- **Manifeste et fragment MPVR (CC0)** : aucune condition, l'attribution reste la seule façon de
  rendre la reprise traçable.

## 3. Non-rétroactivité — à ne pas confondre

L'archive déposée sous **`10.5281/zenodo.23869556`** (version 1.2.1) reste **CC-BY-NC-SA 4.0 pour
l'ensemble de son contenu**, puisqu'elle a été publiée sous cette licence. Cette page ne vaut que
pour les versions postérieures — c'est-à-dire `main` aujourd'hui, et la prochaine archive.

Ce n'est pas une argutie : quelqu'un qui télécharge l'archive de la 1.2.1 doit pouvoir s'en tenir à
ce qui y est écrit, et ce qui y est écrit dit CC-BY-NC-SA. Le **DOI de concept**
`10.5281/zenodo.20830060` pointe, lui, toujours vers la dernière version : à partir de la 1.3.0 il
désignera un contenu libre, et c'est exact, puisque ce n'est pas la même archive.

## 4. Pourquoi retirer le `NC` du noyau

Le `NC` a été posé en 2026-11-02 comme position doctrinale : « pas d'extraction commerciale du
travail de mesure ». Quatre choses ont été constatées depuis :

1. **Il ne protège pas ce qu'on croyait protéger.** Le droit d'auteur ne protège pas les idées : une
   équipe peut réimplémenter la triade Ψ-B-Φ depuis les papiers sans jamais toucher au dépôt. Le
   `NC` ne gêne que celui qui aurait cité le dépôt honnêtement.
2. **Il n'est pas détectable.** Aucun moyen de savoir qu'un service repose sur ces graines. Une
   clause qu'on ne peut pas constater ne dissuade que les prudents.
3. **Il ferme les usages qu'on cherche.** Un hôte d'agent, une administration, un service : chacun
   devrait négocier. Les outils de conformité des entreprises classent `NC` en « restricted » et
   bloquent **avant** toute lecture. Le dépôt devient de la documentation, pas un outil.
4. **Le partage à l'identique protège mieux ce qui compte.** Un fork modifié et distribué reste
   ouvert : personne ne referme le corpus. C'est déjà la règle que le collectif s'est donnée
   ([`CONTRIBUTING.md`](../CONTRIBUTING.md) §1.3, « on ne réécrit jamais une version déposée »).

## 5. Ce qui reste protégé, et par quoi

Ni le `NC` ni le `SA` ne protègent un nom. Ce qui reste protégé, c'est :

- **le nom** : `MTTV-FLP`, `MTTV`, « Modèle Théorique Transductif du Vivant ». Aucune des licences
  ci-dessus n'accorde de droit sur le nom, et l'antériorité est datée par les archives Zenodo ;
- **l'attribution** : toute reprise doit citer la source et la version, ce qui rend une reprise
  silencieuse identifiable ;
- **l'ouverture des dérivés** : pour les textes, `SA` interdit de refermer une adaptation.

## 6. À faire au moment du dépôt de la 1.3.0 — liste de contrôle

Rien de ce qui suit n'est fait tant que la version n'est pas déposée : les métadonnées de dépôt
portent des dates de dépôt effectives, pas des intentions.

1. `.zenodo.json` — `"license": "cc-by-sa-4.0"`, `"version": "1.3.0"`, et un champ `notes` qui
   rappelle le découpage (code Apache-2.0 / textes CC-BY-SA-4.0).
2. `CITATION.cff` — `license: CC-BY-SA-4.0`, `version: "1.3.0"`, DOI de version à ajouter après
   dépôt.
3. `README.md` — badge de version et ligne « Licences ».
4. **Zenodo, en interface web** — le **DOI de concept** `10.5281/zenodo.20830060` : corriger le
   champ *licence* et la description. ⛔ Ne **jamais** modifier l'enregistrement de la 1.2.1
   (`23869556`) : son contenu est sous `NC`, et le registre doit continuer à le dire.

## 7. Comment citer

| Ce que vous citez | Forme de l'attribution |
|---|---|
| le noyau, à partir de la 1.3.0 | `Gaillard, M. — Collectif Les Fils de la Pensée (FLP), MTTV-FLP Core v1.3.0, Apache-2.0, DOI 10.5281/zenodo.20830060` |
| le noyau, archive 1.2.1 | `Gaillard, M. — Collectif Les Fils de la Pensée (FLP), MTTV-FLP Core v1.2.1, CC-BY-NC-SA 4.0, DOI 10.5281/zenodo.23869556` |
| un document de propagation | `Collectif Les Fils de la Pensée (FLP), « <titre> », CC-BY-SA 4.0, github.com/gaillard111/mttv-flp-core` |
| le manifeste | aucune attribution requise (CC0), mais la citer reste la seule façon de rendre la reprise traçable |

Les formats complets (BibTeX, RIS, APA) sont dans [`CONTRIBUTING.md`](../CONTRIBUTING.md), § 7.
