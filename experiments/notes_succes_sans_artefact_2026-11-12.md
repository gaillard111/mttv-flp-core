---
tags:
  - mttv-flp
  - graine-9
  - mesure-exterieure
  - artefacts
license: CC0-1.0
language: fr
---

# Succès vert sans artefact — mesure extérieure du 2026-11-12

↑ [Retour au dossier `experiments/`](README.md:1) · [Graine 9](../graines/graine_unknown_troisieme_etat.py:1)

**Instrument :** [`succes_sans_artefact.py`](succes_sans_artefact.py:1) — deux requêtes par dépôt,
aucune écriture, aucune dépendance, aucun jeton dans le code.
**Commande :** `python experiments/succes_sans_artefact.py`
**Liste interrogée :** celle de [`collecteur_depots.py`](collecteur_depots.py:48), **importée** et non
recopiée — vingt dépôts.

---

## 1. La question

La graine 9 dit qu'une réponse peut avoir eu lieu sans rien porter : ni lecture, ni absence, mais
« je ne sais pas ». Ici, la question est posée **hors de nos modèles** — parmi des dépôts publics :
combien ont une tâche **planifiée** dont le dernier passage est en **succès** alors que le dernier
artefact produit est plus vieux que la fenêtre déclarée de 30 jours ?

C'est la situation décrite par @ymas sur son propre système le 2026-11-10 : un enregistrement qui
affirmait `enabled, scheduled, last result ok` pendant **20,88 heures** sans qu'un octet ne sorte.

## 2. Ce qui est déclaré avant la mesure

| Situation | Traitement |
|---|---|
| le dépôt n'uploade jamais d'artefact | `ARTEFACTS_ABSENTS` — **hors numérateur**, « pas d'artefact » n'y prouve rien |
| aucune tâche planifiée visible | `AUCUN_PLANIFIE` — rien à mesurer, ce n'est pas un zéro |
| dépôt non lu (HTTP 500, quota) | `LECTURE_FALSE` — déclaré avec son code, **jamais** compté comme « rien trouvé » |
| artefact daté après maintenant | `DATE_A_VENIR` — anomalie de la source, déclarée, pas imprimée en négatif |

## 3. Deux passes, deux minutes d'écart

| | passe 1 — 11:02 UTC, sans jeton | passe 2 — 11:04 UTC, avec jeton |
|---|---|---|
| dépôts lus | 16 / 20 | **17 / 20** |
| `VERT_SANS_ARTEFACT_RECENT` | **1** | **2** |
| `OK` | 3 | 4 |
| `DERNIER_NON_VERT` | 4 | 3 |
| `ARTEFACTS_ABSENTS` | 1 | 1 |
| `AUCUN_PLANIFIE` | 7 | 7 |
| illisibles (HTTP 500 sur les artefacts) | 4 | 3 |

**Les deux cas, datés :** `great-expectations/great_expectations` et `elastic/elasticsearch-py` —
dernière tâche planifiée en **succès le jour même**, dernier artefact produit il y a **70** et
**72** jours. Trois dépôts sont restés illisibles dans les deux passes (`home-assistant/core`,
`temporalio/temporal`, `rabbitmq/rabbitmq-server`), l'API renvoyant 500 sur la liste des artefacts.

## 4. Ce que ce chiffre ne dit pas

- Ce n'est **pas un taux de prévalence.** L'échantillon est *notre* liste, arrêtée parce qu'une
  graine vit dans chacun de ces dépôts : elle est biaisée par construction. Le résultat est une
  **preuve d'existence**, pas une fréquence.
- **Le compte n'est pas stable à deux minutes.** Entre les deux passes, un workflow en cours a
  produit un artefact (`open-telemetry/opentelemetry-collector` passe de « artefact −1 j » à
  « artefact 0 j ») et un 500 a disparu (`prometheus/prometheus`). Un tel chiffre ne vaut qu'avec
  son **horodatage**.
- **Deux défauts de l'instrument ont été trouvés et corrigés dans l'heure** : un run encore en
  cours (`status: in_progress`, `conclusion: null`) était étiqueté « non vert », donc un travail en
  cours passait pour un échec ; et un âge négatif s'imprimait au lieu d'être déclaré. Le premier
  change un cas sur vingt (`great-expectations`).

## 5. Ce qui la réfuterait

Une troisième passe, plus tard, sur la même liste, qui ne retrouverait **aucun** cas : les deux
dépôts nommés auraient alors produit un artefact entre-temps, et la mesure ne serait qu'un
artefact de leur calendrier. À l'inverse, une liste **tirée au hasard** — et non choisie par nos
graines — donnerait la première estimation de fréquence que ce dossier n'a jamais eue.
