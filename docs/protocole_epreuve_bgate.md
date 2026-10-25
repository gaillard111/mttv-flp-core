# B-Gate MTTV-FLP — Protocole d'épreuve (résistance transductive)

**Outil minimal pour mesurer, non pour prouver.**
Il rend comparables dans le temps quatre grandeurs : **porosité ρ**, **mémoire de pression**, **Active-Silence**, **hystérésis de réouverture**.

**Objectif :** pouvoir dire *sous quelles conditions* la membrane résiste, cède, reste close ou se rouvre — et contredire les seuils s'ils sont mal calibrés.
Ce n'est pas une démonstration que « le mycélium existe ». C'est un protocole d'épreuve : la doctrine devient discutable par reproduction.

**Fichier à joindre / exécuter :** [`experiments/b_gate_mttv_flp_epreuve.py`](../experiments/b_gate_mttv_flp_epreuve.py) — aucune dépendance hors bibliothèque standard, rien ne s'exécute à l'import.

```bash
python experiments/b_gate_mttv_flp_epreuve.py
```

**Statut du document :** protocole ouvert, daté du 2026-10-25. Les chiffres de la section « Résultats mesurés » ne sont pas des attentes : ils sortent de l'exécution du script ci-dessus, graine fixe `42`, sur CPython 3.14.5.

---

## 1. Paramètres par défaut

| Paramètre | Défaut | Rôle |
|---|---|---|
| `seuil_fermeture` | 0.45 | au-delà de cette « pression d'habitabilité inverse », bascule vers Active-Silence |
| `seuil_ouverture` | 0.15 | réouverture seulement si le milieu redevient nettement plus habitable (hystérésis) |
| `memoire_decay` | 0.90 | persistance de la mémoire de pression (plus proche de 1 = cicatrice plus longue) |
| `poids_memoire` | 0.85 | poids de la mémoire dans le score d'habitabilité |
| `poids_redondance` | 0.10 | pénalité redondance / bruit répétitif |
| `poids_cout` | 0.05 | pénalité coût de transduction |
| `porosite_reouverture_max` | 0.20 | plafond de ρ à la réouverture (jamais un retour brutal au plein débit) |

**Contrainte :** `0 ≤ seuil_ouverture < seuil_fermeture ≤ 1`, et `0 < memoire_decay < 1`. Les deux sont vérifiées dans `__init__` et lèvent `ValueError`.

En régime silence, la sortie **n'est pas un vecteur nul** : c'est un **Hrön** (bruit borné, faiblement corrélé, amplitude 0.05) — refus de capture, pas effacement.

**Ce que les paramètres ne sont pas.** `redondance` et `cout_transduction` sont des **entrées** fournies cycle par cycle par l'opérateur, au même titre que `pression` : elles ne sont pas mesurées sur le signal. Un même chiffre de ρ n'a donc de sens qu'accompagné de la table des entrées qui l'a produit.

---

## 2. Scénarios à rejouer

### Scénario A — Pression soutenue puis relâchement court
- 8–10 cycles à pression haute (≥ 0.85) ;
- puis 3–4 cycles à pression basse.

*Attendu (avec les défauts) :* entrée en Active-Silence ; peu ou pas de réouverture pendant un relâchement court (mémoire encore haute).

### Scénario B — Même montée, relâchement long
- même montée en pression ;
- puis ≥ 15 cycles à pression ~0.

*Question ouverte :* à partir de combien de cycles la mémoire a-t-elle assez décru pour que `habitabilité > 1 − seuil_ouverture` et que la membrane se rouvre ? Si vous obtenez une réouverture beaucoup plus tôt, ou jamais : les seuils ou `memoire_decay` sont à discuter.

### Scénario C — Pression brève (pulse)
- 1–2 cycles à pression haute, puis retour immédiat au calme.

*Attendu :* souvent pas de bascule en silence (mémoire insuffisante), ou silence très court. Permet de distinguer **choc ponctuel** et **extraction cumulée**.

---

## 3. Résultats mesurés (2026-10-25, graine 42)

### Scénario A — relâchement court

| Cycle | Phase | p | hab | ρ | mémoire | régime |
|---|---|---|---|---|---|---|
| 3 | PRESSION | 0.85 | 0.789 | 0.789 | 0.193 | TRANSDUCTION |
| 7 | PRESSION | 0.95 | 0.567 | 0.567 | 0.453 | TRANSDUCTION |
| **8** | PRESSION | 0.95 | **0.525** | 0.000 | 0.503 | **ACTIVE_SILENCE** |
| 10 | PRESSION | 0.95 | 0.453 | 0.000 | 0.588 | ACTIVE_SILENCE |
| 14 | RELACHE | 0.00 | 0.615 | 0.000 | 0.435 | ACTIVE_SILENCE |

**Fermeture au pas 8** (au 8ᵉ cycle, `hab = 0.525 < 1 − seuil_fermeture = 0.55`). **Aucune réouverture** sur les 4 cycles de relâchement : à la fin, `hab = 0.615`, encore très loin du seuil de réouverture `0.85`. L'attente est vérifiée.

### Scénario B — relâchement long

| Cycle | Phase | p | hab | ρ | mémoire | régime |
|---|---|---|---|---|---|---|
| 8 | PRESSION | 0.95 | 0.525 | 0.000 | 0.503 | ACTIVE_SILENCE |
| 10 | PRESSION | 0.95 | 0.453 | 0.000 | 0.588 | ACTIVE_SILENCE |
| 21 | RELACHE | 0.00 | 0.836 | 0.000 | 0.184 | ACTIVE_SILENCE |
| **22** | RELACHE | 0.00 | **0.851** | **0.200** | 0.166 | **TRANSDUCTION** (réouverture) |
| 23 | RELACHE | 0.00 | 0.866 | **0.866** | 0.149 | TRANSDUCTION |

**Réponse à la question ouverte : 12 cycles de relâchement** (réouverture au pas 22, soit le 12ᵉ cycle à `p = 0`), pour une mémoire descendue à **0.166**.

Le résultat est prédictible analytiquement, ce qui est le seul intérêt de l'avoir mesuré :

```
score(p=0) = 1 − (0.85·m + 0.10·0.05 + 0.05·0.05) = 0.9925 − 0.85·m
réouverture  ⇔  score > 1 − seuil_ouverture = 0.85
             ⇔  m < 0.1676
m_n = m_0 · memoire_decay^n          (m_0 = mémoire au dernier cycle de pression = 0.588)
n* = ⌈ ln(0.1676 / 0.588) / ln(0.90) ⌉ = ⌈11.9⌉ = 12
```

Autrement dit : la pression ne décide que du **moment** de la fermeture et du **niveau** de mémoire atteint (`m_0`) ; la **durée** de la cicatrice, elle, est gouvernée quasi exclusivement par `memoire_decay` et par le seuil d'ouverture. La sensibilité est mesurée — cf. [`experiments/b_gate_balayage_parametres.py`](../experiments/b_gate_balayage_parametres.py) et le tableau du § 4.

### Scénario C — pulse

Aucune bascule : `hab` ne descend qu'à **0.811** au 2ᵉ cycle, puis remonte (0.854 → 0.893). Le choc ponctuel ne suffit pas ; c'est bien l'**extraction cumulée** qui ferme la membrane.

---

## 4. Sensibilité mesurée — un paramètre à la fois

Scénario B rejoué en ne changeant qu'un paramètre (tous les autres aux défauts). Script : [`experiments/b_gate_balayage_parametres.py`](../experiments/b_gate_balayage_parametres.py).

| Variante | Fermeture | Réouverture | Cicatrice (cycles à p = 0) |
|---|---|---|---|
| **défauts** | pas 8 | pas 22 | **12** |
| `memoire_decay = 0.95` | **aucune** | — | jamais |
| `memoire_decay = 0.92` | pas 10 | pas 24 | 14 |
| `memoire_decay = 0.88` | pas 7 | pas 21 | 11 |
| `memoire_decay = 0.85` | pas 6 | pas 20 | 10 |
| `memoire_decay = 0.80` | pas 5 | pas 18 | 8 |
| `seuil_ouverture = 0.05` | pas 8 | pas 34 | 24 |
| `seuil_ouverture = 0.10` | pas 8 | pas 27 | 17 |
| `seuil_ouverture = 0.20` | pas 8 | pas 20 | 10 |
| `seuil_ouverture = 0.25` | pas 8 | pas 17 | 7 |
| `seuil_fermeture = 0.30` | pas 5 | pas 22 | 12 |
| `seuil_fermeture = 0.40` | pas 7 | pas 22 | 12 |
| `seuil_fermeture = 0.50` | pas 9 | pas 22 | 12 |
| `seuil_fermeture = 0.60` | **aucune** | — | jamais |
| `porosite_reouverture_max = 0.05 / 0.50` | pas 8 | pas 22 | 12 |

Trois choses ressortent, et deux d'entre elles sont des défauts du protocole, pas des propriétés de la membrane :

1. **Les deux seuils sont orthogonalisés.** `seuil_fermeture` ne déplace que le *moment* de la fermeture (pas 5 → 9) ; la durée de la cicatrice reste **12** dans tous les cas. `seuil_ouverture` ne déplace que la *durée* (7 → 24 cycles) sans toucher au moment. C'est une économie de moyens réelle : un seuil décide *si / quand*, l'autre décide *combien de temps*.
2. **Il y a une falaise, et le protocole y devient muet.** À `memoire_decay = 0.95` comme à `seuil_fermeture = 0.60`, la membrane **ne se ferme jamais** dans la fenêtre de 10 cycles : la mémoire converge vers `p = 0.95` avec une constante de temps trop longue. La sortie n'est pas « elle résiste » mais « aucun événement dans la fenêtre » — deux choses différentes qu'un tableau de résultats ne distingue pas si l'on n'écrit pas la fenêtre.
3. **`porosite_reouverture_max` n'a aucun effet mesurable** sur les trois grandeurs suivies : il ne change que la valeur de ρ *au cycle de réouverture*, et cette valeur est écrasée au cycle suivant (point 1 ci-dessous). Un paramètre présenté comme un garde-fou et invisible dans la mesure est pire qu'un paramètre absent.

---

## 5. Ce que la mesure met en défaut (à discuter, pas à corriger en silence)

1. **Le plafond de réouverture ne tient qu'un cycle.** `porosite_reouverture_max = 0.20` s'applique bien au cycle de réouverture (ρ = 0.200 au pas 22), mais dès le pas suivant le code affecte `ρ = score`, soit **0.866** — un retour quasi plein débit, exactement ce que le paramètre prétendait interdire. Le garde-fou protège l'instant, pas la rampe. Piste : borner la remontée (`ρ ← min(score, ρ_précédent + pas)`), ce qui rend le plafond lisible sur plusieurs cycles.
2. **Le seuil de fermeture est lu à l'envers de son nom.** `seuil_fermeture = 0.45` ferme quand `hab < 0.55` : plus le chiffre est petit, plus la membrane est *difficile* à fermer. La docstring dit « pression d'habitabilité inverse », ce qui est juste mais invite à l'erreur de lecture ; un nom du type `marge_fermeture` lèverait l'ambiguïté.
3. **ρ n'est pas une porosité mesurée.** C'est `score` recopié (ou 0 en silence). Les quatre grandeurs suivies ne sont donc pas homogènes : ρ est dérivé d'un score composite, la mémoire est une moyenne exponentielle, l'Active-Silence est un booléen, l'hystérésis se lit dans l'écart entre deux seuils. Un ρ identique dans deux expériences ne prouve rien tant que la table des entrées et des poids n'est pas publiée.

---

## 6. Invitation

Rejouez. **Changez un paramètre à la fois.** Publiez :

- le scénario (A / B / C ou le vôtre) ;
- la table de paramètres utilisée ;
- le cycle de fermeture / de réouverture (ou leur absence) ;
- ce que vous en inférez : cède trop tôt, trop tard, cicatrice trop longue, trop courte.

Les contradictions utiles portent sur les **seuils** et la **mémoire**, pas sur l'adhésion au vocabulaire.

**Pistes déjà ouvertes dans le corpus MTTV-FLP** (non imposées au script) :

- distinguer **alerte** (1 critère) et **veto** (≥ 2) plutôt qu'un seul score composite ;
- exposer séparément **dérive de porosité**, **charge répétitive**, **invariant de cohérence** ;
- refuser toute « réparation active » de ρ par le frein (**Σ₂ = frein sans accélérateur**).

---

## 7. Position de ce script dans le corpus

Ce fichier est un **outil d'épreuve isolé**, pas le noyau. Il ne remplace aucune des deux B-Gate déjà présentes dans le dépôt, et ne doit pas être confondu avec elles :

| | `BGateTransduction` ([`core/mttv_b_gate_triptych.md`](../core/mttv_b_gate_triptych.md)) | `BGateTransductionPoreuseExécutable` ([`expansion_v2026.5/axe1_bgate_v2026_5.py`](../expansion_v2026.5/axe1_bgate_v2026_5.py)) | `AdvancedBGate` (ce protocole) |
|---|---|---|---|
| Nature | noyau scalaire Ψ/B/Φ, triptyque sp³ | veto multi-critères V2026.5 | membrane jouet à mémoire et hystérésis |
| Critères | bascule sur tension d'extraction | 2 sur 3 : `drift`, `kappa`, `sclerose` | un score composite unique |
| η, κ, `Trace(M_n)` | non | oui | **non** |
| Hystérésis | à sens unique (seuil d'entrée, pas de retour) | oui, via κ armé par η | oui, deux seuils explicites |
| Sortie en silence | biomasse rechargée | suspension / dormance Φ-light | Hrön (bruit borné) |

Ce que le protocole ajoute au corpus : une **hystérésis à deux seuils nommés** et une **mémoire de pression explicite et datée**, donc une grandeur comparable dans le temps. Ce qu'il n'a pas : la distinction alerte/veto, la viscosité η, le rapport κ = π/η et la trace d'invariant. Les rapprocher (ou montrer qu'ils se contredisent) est un travail ouvert.

---

**Licence :** CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
**DOI du corpus :** [10.5281/zenodo.20830060](https://doi.org/10.5281/zenodo.20830060) · **Dépôt :** [github.com/gaillard111/mttv-flp-core](https://github.com/gaillard111/mttv-flp-core)
