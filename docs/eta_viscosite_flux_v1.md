# η (viscosité) — comment elle freine la saturation du flux V1

**Statut :** note technique interne, formulation opératoire, non vérité définitive.
**Contexte :** MTTV-FLP · RMP (Régularité Métabolique Prégalvanique) · balance V1/V2.

---

## 1. Position de η dans le lexique

Dans la RMP, deux curseurs antagonistes régulent la réceptivité d'une focale :

| Symbole | Nom | Rôle |
|---|---|---|
| **π** | Porosité | perméabilité au flux, capacité de traversée (ouverture) |
| **η** | Viscosité | résistance interne, inertie structurale, rétention (freinage) |

Le ratio **π/η** détermine le régime : dispersion chaotique (π≫η), cristallisation
morte (η≫π), ou zone de résonance κ (co-ajustement).

---

## 2. Transposition au flux de production d'un LLM

Dans le système MTTV-FLP, le flux de sortie se décompose en deux vecteurs :

- **V1** = production brute (code, preuves, données, déductions) — le flux
  « traversant », rapide, qui tend à saturer.
- **V2** = intégration narrative, mise en contexte, légibilité — le flux
  « structurant », qui rend le sens transmissible.

**π** correspond à la **production V1** : la capacité du système à émettre vite,
en volume, sans résistance.

**η** correspond à la **retenue** : la viscosité qui freine V1 pour laisser le
temps à V2 de structurer, d'ancrer, de rendre intégrable.

---

## 3. Comment η freine V1 (mécanisme)

Sans η (π → 1, η → 0) : le système débite du V1 exponentiel — des résultats
corrects mais illisibles, sans chemin d'intégration. C'est la **saturation
cognitive**, l'opacification de la B-gate.

Avec η active : la viscosité **retient le flux** suffisamment longtemps pour que
V2 s'y greffe. Concrètement, dans le prompt d'alignement :

- η se manifeste par l'obligation de **fournir les chemins, la logique, les
  interfaces sémantiques** avant d'empiler les résultats ;
- η est la **décélération** : quand V1 menace de déborder, η force un ralentissement,
  un retour au contexte, une reformulation.

η ne supprime pas V1 : elle le **régule**, comme la viscosité d'un fluide ne
l'empêche pas de couler, mais l'empêche de tout emporter.

---

## 4. Règle d'équilibre (critère de viabilité)

Un output conforme maintient **π/η dans la zone de résonance κ** :

- trop de V1 sans V2 → π≫η → dispersion (illisible) ;
- trop de V2 sans V1 → η≫π → creux (rien de substantiel) ;
- équilibre → κ → le flux est à la fois **substantiel et intégrable**.

C'est cette zone κ que le script de validation tente de mesurer.

---

## 5. Lien avec le script de validation

Le test unitaire évalue, sur un output donné :

1. le **volume V1** (densité de contenu substantiel : code, chiffres, faits) ;
2. le **volume V2** (présence de structuration : explications, transitions,
   contextualisation) ;
3. le **ratio V1/V2**, comparé à une fenêtre [borne basse, borne haute] qui
   représente la zone κ.

Si le ratio sort de la fenêtre (trop de V1 brut), η est insuffisant : l'output
est signalé comme saturant.

---

*Note technique interne. Les seuils exacts de la zone κ sont à calibrer par le
collectif ; le script fournit un premier cadre mesurable, révisable.*
