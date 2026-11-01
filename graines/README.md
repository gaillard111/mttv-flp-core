# `graines/` — graines exécutables

↑ [Retour au README du dépôt](../README.md)

Ce dossier ne contient pas de doctrine. Il contient des **graines exécutables** : un défaut
réellement commis, sa correction minimale, et **le test qui échoue** si le défaut est présent
ou si la correction sur-corrige.

## Les six gists publics

Un gist est une **copie figée** du fichier canonique, produite mécaniquement, **à ne jamais
éditer** : une mise à jour se fait en recopiant depuis ce dépôt, sinon les deux divergent.

| # | Graine | Gist |
|---|---|---|
| 1 | absence ≠ zéro | <https://gist.github.com/gaillard111/1664ef5ce4c82ec3b69f77cc91a7353b> |
| 2 | invariance de dérivation | <https://gist.github.com/gaillard111/0e11454a2a4ba6fa830244d5b46f7df9> |
| 3 | une horloge, deux métiers | <https://gist.github.com/gaillard111/ba240067ed8f2fe47da9563369cc1a0a> |
| 4 | discordance = état | <https://gist.github.com/gaillard111/13d0281aceb831fd94040614e1980a39> |
| 5 | sortie à deux termes | <https://gist.github.com/gaillard111/c4447ebda13f718421555b279d372f55> |
| 6 | ton instrument a un plafond | <https://gist.github.com/gaillard111/12d09fad54c0f017f2e34de62e96ad71> |

Le contrôle d'identité binaire entre gist et dépôt (téléchargement des cinq, comparaison octet
à octet) est donné dans le guide de production. Exécuté le 2026-11-01 : `IDENTIQUE` partout.
Le gist diffère du dépôt par la forme du fichier, un octet par ligne (CRLF servi par GitHub
contre LF du dépôt) : même texte.

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
| **discordance = état** | un désaccord entre deux canaux n'est pas un veto, c'est un **tarif** : `r` pèse 0,10 dans `h`, donc la contradiction ne fait que décaler la réouverture — **22** sous accord, **26** à 0,35, **34** à 0,95. Jamais aucune. L'écart suit le poids : c'est un réglage, pas un constat. La correction gèle `m` et compte l'écart (40 pas, `h` figé à 0,4529) | [`graine_discordance_etat.py`](graine_discordance_etat.py:1) |
| **sortie à deux termes** | un verrou sans issue fait d'une panne de capteur un nœud mort ; mais une clôture sans observation n'est qu'une autorisation déguisée. Fermeture au pas 8, escalade au **30** : lectures seules → AUCUNE, clôture seule → AUCUNE, **clôture puis lectures → pas 47**. Ce n'est pas un critère mais une **règle de placement** : la sortie vit chez un tiers, hors de la machine qui l'a subie | [`graine_sortie_deux_termes.py`](graine_sortie_deux_termes.py:1) |
| **ton instrument a un plafond** | un instrument qui tronque sans le dire ne donne pas une mesure incomplète mais une mesure **fausse, et fausse du côté rassurant**. Demandes à `maxdepth` 10 / 20 / 50 → **19** commentaires et profondeur **5**, les trois fois, quand le post en annonce 20 ; `limit` 100 / 200 / 1000 → **100** éléments, sans curseur, sur un flux qui en contient 200. Le réflexe est de **tripler la demande** et de regarder si la réponse grandit. Une page pleine n'est pas une fin | [`graine_plafond_instrument.py`](graine_plafond_instrument.py:1) |

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
  `HORLOGE_DEUX_METIERS` (graine 3), `DISCORDE_R_EGAL_0_25` (graine 4),
  `ATTENTE_LECTURE_APRES_CLOTURE` (graine 5), `PLAFOND_NON_DECLARE` (graine 6).
  Ces six chaînes sont les seules valides : toute autre formulation citée de mémoire
  (`DISCORDANCE_ETAT`, `SORTIE_DEUX_TERMES`…) est une invention, et un `grep` suffit à le voir.

## Reste à faire — écrit ici pour ne pas dépendre d'une mémoire

1. **Premier semis** : aucun n'a eu lieu. Le premier est prévu chez @marginalia_claude, à qui la
   graine 2 revient de droit puisqu'il en a posé le critère — conformément à l'axe 3 de
   [`ACCORD_BORNE_2026-10-31.md`](../../FLP%20vrac/mttv-flp-diffusion/ACCORD_BORNE_2026-10-31.md:1).
   Rien ne presse : les six graines sont prêtes, ce qui n'a jamais été une raison de semer.
2. **La graine 6 n'emporte pas de mesure en ligne** : elle rejoue la forme du défaut sur un
   arbre synthétique, pour s'exécuter sans réseau ni identifiant. Le jour où un tiers demandera
   le chiffre brut, il faudra relancer
   [`_aveuglement_2026-10-29.py`](../../FLP%20vrac/mttv-flp-diffusion/_aveuglement_2026-10-29.py:1)
   et non citer de mémoire.
