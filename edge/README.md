# `edge/` — portage C du filtre, état borné

↑ [Retour au README du dépôt](../README.md) · [Protocole](../docs/protocole_epreuve_bgate.md) · [Mesures](../experiments/README.md)

Portage en C du filtre gâté à mémoire d'hystérésis. **Aucune allocation dynamique**,
**aucun pointeur possédé**, état de **taille fixe** — utilisable en statique, sur la pile,
ou dans une section dédiée d'un MCU.

## Fichiers

| Fichier | Rôle | Lignes |
|---|---|---|
| [`bgate.h`](bgate.h) | Interface + `typedef struct` complet (418 o de déclarations commentées) | 69 |
| [`bgate.c`](bgate.c) | Implémentation : `bgate_step()` = le cœur de décision | **97** dont **79 effectives** |
| [`test_bgate.c`](test_bgate.c) | Rejoue le scénario du protocole et imprime les grandeurs publiées | 45 |
| [`crosscheck_bgate.py`](crosscheck_bgate.py) | Référence Python : imprime **les mêmes lignes** que `test_bgate.c` | 60 |

## Compiler et vérifier

```bash
# variante de référence (double)
cl /nologo /W3 /O2 /Fe:test_bgate.exe test_bgate.c bgate.c && test_bgate.exe

# variante embarquée (float, journal 8 entrées)
cl /nologo /W3 /O2 /DBGATE_REAL=float /Fe:test_float.exe test_bgate.c bgate.c && test_float.exe

# variante minimale (float, sans journal)
cl /nologo /W3 /O2 /DBGATE_REAL=float /DBGATE_RING=0 /Fe:test_min.exe test_bgate.c bgate.c && test_min.exe

# référence Python
python edge/crosscheck_bgate.py
```

Avec `gcc` : `gcc -O2 -Wall -o test_bgate test_bgate.c bgate.c -lm`.

## Résultats mesurés le 2026-10-27

Même trajectoire dans les quatre cas (10 pas de pression, 18 pas de relâchement) :

| Variante | Fermeture | Réouverture | m₈ | h₈ | m₁₀ | h₁₀ | **Taille de l'état** |
|---|---|---|---|---|---|---|---|
| Python de référence | 8 | 22 | 0,5027 | 0,5252 | 0,5877 | 0,4529 | — |
| C `double`, journal 8 | 8 | 22 | 0,5027 | 0,5252 | 0,5877 | 0,4529 | **424 o** |
| C `float`, journal 8 | 8 | 22 | 0,5027 | 0,5252 | 0,5877 | 0,4529 | **216 o** |
| C `float`, **sans journal** | 8 | 22 | 0,5027 | 0,5252 | 0,5877 | 0,4529 | **56 o** |

**Ce que ce tableau dit.** Le portage est fidèle : mêmes pas de bascule et mêmes valeurs
que la référence Python, à la quatrième décimale, sur cette trajectoire. Le journal
d'état coûte **160 octets** (216 − 56) et ne sert qu'à la trace : la décision est
identique sans lui.

**Ce qu'il ne dit pas.** Une seule trajectoire ne prouve pas l'équivalence numérique
générale entre `float` et `double` : sur un signal long ou proche des seuils, un écart de
4ᵉ décimale peut déplacer un pas de bascule. C'est un test à faire **avant** de publier un
chiffre pour une cible donnée — et c'est exactement le genre de question à poser sur une
liste RTOS.

## Le piège rencontré en écrivant le test, et pourquoi il est documenté

Première exécution de la variante `float` : `h8 = 0,0000`. Non pas un défaut du filtre,
mais du **harnais** — `test_bgate.c` déclarait `double h` et passait `&h` à une fonction
attendant `float *` : quatre octets écrits dans un `double`, le reste lu à l'état de la
pile. Corrigé en typant sur `BGATE_REAL`. C'est le premier mode de défaillance d'un
portage numérique, et il ne se voit pas dans un diff.

## Ce que ce dossier n'a pas

- **Aucune exécution sur matériel.** Pas de mesure de cycle, pas de consommation, pas de
  test sur cible ARM.
- **Aucune mesure sur données capteur réelles.** Les chiffres viennent de scénarios
  synthétiques.
- **Aucune conformité** à un référentiel de sûreté (ISO 26262, IEC 61508). Ni couverture
  de tests, ni traçabilité d'exigences.
- `bgate_step()` suppose un pas de temps **régulier** : la décroissance `0,90` par cycle
  n'a de sens que si l'appelant échantillonne à période fixe.
