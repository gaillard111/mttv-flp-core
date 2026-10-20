---
tags:
  - mttv-flp
  - b-gate
  - experience
  - dose-reponse
  - biais-contrastif
license: CC-BY-NC-SA-4.0
language: fr
---

# Compte-rendu d'expérience — B-Gate : dose-réponse et biais contrastif

**Date :** 3 octobre 2026
**Machine :** Intel i3-3110M (CPU), 7,9 Go RAM, `torch 2.12.1+cpu`, `transformers 5.12.1`
**Modèle :** `gpt2` (local, `W_emb` de forme `[50257, 768]`)
**Objet :** mesurer, sans tricherie, si l'opérateur de décodage B-Gate (Direction 2 de la spec V1) réoriente réellement le classement des tokens, et à partir de quel seuil.

**Scripts :** [`experiments/smoke_test_bgate_direction2.py`](../experiments/smoke_test_bgate_direction2.py) · [`experiments/bgate_dose_reponse.py`](../experiments/bgate_dose_reponse.py) · [`experiments/bgate_dose_reponse_contrastif.py`](../experiments/bgate_dose_reponse_contrastif.py)

---

## 1. Ce qui a été fait

1. **Smoke test** : exécution de `BGateLogitsProcessor` sur `gpt2` — forme préservée, biais fini, 41 ms (CPU). ✅
2. **Courbe dose-réponse (métrique `max`)** : balayage de `α` (0.05 → 5.0) et de `N_ref` (4 → 64).
3. **Courbe dose-réponse (métrique contrastive)** : même balayage, avec le biais `cos(token, µ_ref) − cos(token, µ_vocab)`.

---

## 2. Résultats mesurés

### 2.1 Métrique `max` (version initiale) — sature

| N_ref | α | Jaccard top-5 | Réorientation top-1 | biais/logits |
|---|---|---|---|---|
| 4 | 0.5 | 1.000 | non | 0.72 % |
| 4 | 5.0 | 0.111 | **oui** | 7.23 % |
| 16 | 5.0 | 0.429 | non | 6.65 % |
| 64 | 5.0 | 0.429 | non | 6.65 % |

**Lecture :** le top-1 ne bouge qu'à `α = 5.0` (biais ~7 % de la norme), et **seulement** à `N_ref = 4`. Dès que la source s'enrichit, l'effet se **dilue** : le `max` sature (chaque token trouve toujours un fragment quasi-aligned), et un biais quasi-uniforme ne change pas l'`argmax`.

### 2.2 Métrique contrastive — ne sature pas

| N_ref | α | Jaccard top-5 | Réorientation top-1 | biais/logits |
|---|---|---|---|---|
| 4 | 0.5 | 1.000 | **oui** | 0.05 % |
| 4 | 1.0 | 0.667 | oui | 0.10 % |
| 16 | 0.5 | 0.667 | **oui** | 0.06 % |
| 64 | 0.5 | 0.667 | **oui** | 0.06 % |
| 64 | 5.0 | 0.250 | oui | 0.55 % |

**Lecture :** la réorientation apparaît dès `α = 0.5`, avec ~0.05 % d'énergie injectée — soit **~100× moins** que le `max`. L'effet est **stable** quand `N_ref` croît de 4 à 64 (Jaccard constant à 0.667 puis 0.250).

---

## 3. Conclusion

1. **Le mécanisme est réel** : un opérateur de décodage, sans toucher aux poids, modifie effectivement le classement des tokens à des niveaux d'énergie minimes.
2. **La métrique `max` est inadaptée** : elle sature et son effet se dilue avec l'enrichissement de la source. Elle est remplacée par la métrique **contrastive** dans la spec V1 (§3).
3. **Le contraste est le bon opérateur** : `cos(token, µ_ref) − cos(token, µ_vocab)` mesure la *penchée* d'un token vers la source relativement au fond du vocabulaire — contrastif par construction, il ne peut pas saturer.

---

## 4. Limites assumées (à ne pas masquer)

- **Réorienter ≠ améliorer.** L'expérience prouve que l'opérateur *agit* sur le classement ; elle ne prouve pas que la réorientation *réduit un biais*. La qualité exige des benchmarks standardisés (BOLD, Winobias, CrowS-Pairs, StereoSet, BBQ) — étape suivante, non réalisée ici.
- **`µ_ref` est un choix humain.** La direction moyenne de la source dépend des fragments choisis ; ce choix reste traçable et révisable (conforme à l'anti-Goodhart du dépôt).
- **`gpt2` est un modèle de démonstration**, pas le modèle cible ; les seuils d'`α` sont indicatifs et non transférables tels quels.

---

*Formulation opératoire, non vérité définitive. Résultats reproductibles via les scripts cités, sur la machine locale.*
