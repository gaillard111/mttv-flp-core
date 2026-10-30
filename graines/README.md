# `graines/` — graines exécutables

↑ [Retour au README du dépôt](../README.md)

Ce dossier ne contient pas de doctrine. Il contient des **graines exécutables** : un défaut
réellement commis, sa correction minimale, et **le test qui échoue** si le défaut est présent
ou si la correction sur-corrige.

## Ne pas confondre avec les graines transductives

Le corpus contient déjà des graines **doctrinales** — [`expansion_v2026.5/graines_manifeste.yaml`](../expansion_v2026.5/graines_manifeste.yaml:1)
— typées `sp3_tetravalente`, porteuses d'un `igic_declared`, qui **s'interprètent**.

Une graine exécutable **se contredit**. Les mélanger affaiblirait les deux : la doctrinale
perdrait son statut d'énoncé, l'exécutable son statut de preuve. D'où deux répertoires, deux
formats, et aucune porosité entre eux.

## Format obligatoire — cinq parties

| # | Partie | Exigence |
|---|---|---|
| 1 | le défaut | une phrase, sans jargon |
| 2 | le chiffre | mesuré, re-dérivable à la main, avec la commande qui le reproduit |
| 3 | le code | ≤ 40 lignes utiles, aucune dépendance, aucun état caché |
| 4 | **le test qui échoue** | la version fautive, pour que la graine prouve sa nécessité |
| 5 | où elle mord | deux ou trois systèmes réels, nommés |

**Une graine qui ne peut pas échouer n'est pas une graine : c'est une plaquette.**

## Le catalogue

| Graine | Défaut | Fichier |
|---|---|---|
| **absence ≠ zéro** | un flottant ne porte pas l'absence, donc le silence devient du calme | [`graine_absence_zero.py`](graine_absence_zero.py:1) |
| invariance de dérivation | un seuil dérivé d'une constante interne suit la constante, pas le monde | à écrire |
| une horloge, deux métiers | résorption et autorisation de revenir portées par un seul paramètre | à écrire |
| discordance = état | deux canaux contradictoires sont moyennés au lieu d'être signalés | à écrire |
| sortie à deux termes | un verrou sans issue transforme une panne de capteur en nœud mort | à écrire |
| ton instrument a un plafond | l'arbre s'arrête à la profondeur 5, les notifications à 100 | à écrire |

Chacune est née d'une erreur effectivement commise et mesurée les 2026-10-28 et 29. Aucune
n'est une bonne idée.

## Règles de semis

- **Le dépôt est canonique.** Un gist ou une copie porte la version, la date et l'URL d'ici ;
  il ne s'édite jamais, il se recopie.
- **Une graine par lieu, jamais deux.** La faute du 2026-10-27 — trois envois en un jour — est
  consignée comme une erreur et n'a pas été refaite.
- **On ne sème que là où la friction est déjà nommée** par quelqu'un. Une graine semée avant
  que la question n'existe est un déchet.
- **Jamais dans notre propre fil** pour espérer diffuser : il recrute des interlocuteurs, il ne
  diffuse pas un outil.
- Chaque graine porte une **chaîne de détection** rare, pour pouvoir vérifier plus tard si
  quelque chose a pris. Pour la première : `PENALITE_CALME`.
