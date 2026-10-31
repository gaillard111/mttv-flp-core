# `graines/` — graines exécutables

↑ [Retour au README du dépôt](../README.md)

Ce dossier ne contient pas de doctrine. Il contient des **graines exécutables** : un défaut
réellement commis, sa correction minimale, et **le test qui échoue** si le défaut est présent
ou si la correction sur-corrige.

> **Gist public de la graine 1** — <https://gist.github.com/gaillard111/1664ef5ce4c82ec3b69f77cc91a7353b>
> Copie du fichier canonique, faite mécaniquement (`gist_graine_1/creer_le_gist.bat`), **à ne
> jamais éditer** : une mise à jour se fait en recopiant depuis ce dépôt, sinon les deux
> divergent. Le gist diffère du dépôt d'un octet par ligne (CRLF local contre LF du dépôt) :
> même texte, forme de fichier différente.

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
| 3 | le code | ≤ 120 lignes de fichier et ≤ 60 instructions (comptées par `ast`), aucune dépendance hors bibliothèque standard, aucun état caché |
| 4 | **le test qui échoue** | la version fautive, pour que la graine prouve sa nécessité |
| 5 | où elle mord | deux ou trois systèmes réels, nommés |

**Une graine qui ne peut pas échouer n'est pas une graine : c'est une plaquette.**

La borne de la partie 3 a été réécrite le 2026-10-31 : la première rédaction exigeait « ≤ 40 lignes
utiles », chiffre qu'**aucune des trois graines ne tenait** — mesuré par `ast`, elles comptent 54,
38 et 58 instructions. Le critère est désormais celui qui se vérifie, et il est vérifié.

## Le catalogue

| Graine | Défaut | Fichier |
|---|---|---|
| **absence ≠ zéro** | un flottant ne porte pas l'absence, donc le silence devient du calme | [`graine_absence_zero.py`](graine_absence_zero.py:1) |
| **invariance de dérivation** | un seuil dérivé d'une constante interne suit la constante, pas le monde : **10 → 207 cycles** quand la décroissance va de 0,80 à 0,99. La correction est **insensible à la constante et sensible à la cadence** (3, 6, 15, 30 pour 1, 2, 5, 10) — les deux conditions, faute de quoi un seuil constant ne mesure plus rien | [`graine_invariance_derivation.py`](graine_invariance_derivation.py:1) |
| **une horloge, deux métiers** | la cicatrice `m` est **gelée** pendant l'aveuglement : compter un silence en demi-vies revient à mesurer avec une horloge arrêtée. Le même seuil de 20 cycles déclare une panne après **10** cycles si la décroissance vaut 0,80 et après **207** si elle vaut 0,99. En revanche l'aveuglement coûte exactement sa durée — réouverture au pas 22 sans absence, **41** après 19 pas : la pente vaut 1 | [`graine_une_horloge_deux_metiers.py`](graine_une_horloge_deux_metiers.py:1) |
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
  quelque chose a pris : `PENALITE_CALME` (graine 1), `DEMI_VIES_TOLEREES` (graine 2),
  `HORLOGE_DEUX_METIERS` (graine 3).
