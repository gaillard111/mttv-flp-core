# B-Gate MTTV-FLP — Protocole d'épreuve (résistance transductive)

**Outil minimal pour mesurer, non pour prouver.**
Il rend comparables dans le temps quatre grandeurs : **porosité ρ**, **mémoire de pression**, **Active-Silence**, **hystérésis de réouverture** — et, depuis le 2026-10-25, la **valeur tétravalente de l'état** (§ 4) ainsi que la question de la **nature** de cette hystérésis : cinétique ou paramétrique (§ 5).

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
| `frontiere_admissible` | 0.50 | au-delà de cette pression, le milieu est jugé **hostile** — sert à la lecture tétravalente (§ 4). Choix doctrinal, non mesuré |
| `derive` | 0.0 | dérive du seuil de fermeture à chaque cycle d'exposition — mémoire **paramétrique** (§ 5). `0.0` = protocole originel, chiffres inchangés |

⚠️ **Les trois poids sont renormalisés** par leur somme dans `__init__` : passer `poids_memoire` de 0,85 à 0,60 fait mécaniquement monter `poids_redondance` (0,100 → 0,133) et `poids_cout` (0,050 → 0,067). Toute expérience qui fait varier un poids seul est donc **confondue** — sauf à écrire les poids normalisés après construction (cf. l'amendement du § 6).

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

Autrement dit : la pression ne décide que du **moment** de la fermeture et du **niveau** de mémoire atteint (`m_0`) ; la **durée** de la cicatrice, elle, est gouvernée quasi exclusivement par `memoire_decay` et par le seuil d'ouverture. La sensibilité est mesurée — cf. [`experiments/b_gate_balayage_parametres.py`](../experiments/b_gate_balayage_parametres.py) et le tableau du § 6.

### Scénario C — pulse

Aucune bascule : `hab` ne descend qu'à **0.811** au 2ᵉ cycle, puis remonte (0.854 → 0.893). Le choc ponctuel ne suffit pas ; c'est bien l'**extraction cumulée** qui ferme la membrane.

---

## 4. Lecture tétravalente — rendre la cicatrice représentable

Le régime binaire (`TRANSDUCTION` / `ACTIVE_SILENCE`) ne dit pas si le milieu **autorisait** l'ouverture. On croise donc deux questions **indépendantes** — l'une sur l'entrée, l'autre sur l'état — ce qui donne quatre valeurs, au sens de Belnap-Dunn :

| | membrane ouverte | membrane fermée |
|---|---|---|
| **milieu admissible** (`p ≤ 0.50`) | **T** transduction normale | **B** *les deux* — le milieu rappelle, la membrane ne revient pas : **la cicatrice** |
| **milieu hostile** | **N** *aucun* — on transduit pendant l'extraction : **la fuite** | **F** silence cohérent |

L'intérêt n'est pas taxinomique. Belnap-Dunn donne **deux ordres** sur ces quatre valeurs — l'ordre de vérité `F ≤ N,B ≤ T` (ce qu'on croit) et l'ordre d'information `N ≤ T,F ≤ B` (ce qu'on sait). Ce que cela apporte est exactement ceci : **à valeur de vérité égale, deux valeurs d'information distinctes**. T et B portent le même jugement sur le monde — il est admissible — et B affirme une chose de plus : *la membrane est close*. Une logique à une dimension ne peut pas écrire cette différence ; elle range B avec F.

⚠️ **Précision ajoutée le 2026-10-25, et correction d'une formulation antérieure.** L'ordre d'information est **atemporel** : il dit *combien* de choses sont affirmées au même instant, pas *depuis combien de temps*. Ce que la tétravalence fournit est donc la **représentabilité** de la cicatrice, non sa **durée**. Qu'un état B existe *parce que* le passé a laissé une trace est une affirmation causale, que le bilattice est incapable de formuler : c'est l'affaire du § 5. Les deux sont nécessaires, et aucune ne remplace l'autre.

Version continue, si l'on préfère des degrés à quatre cases : l'état est un intervalle `[t, 1−f] ⊆ [0,1]` de largeur `1 − t − f` (sémantique d'intervalle). `T = [1,1]`, `F = [0,0]`, `N = [0,1]`, `B = [1,0]`. Or ρ n'est que le **milieu** de cet intervalle : le protocole projette un état à deux dimensions sur sa moyenne et jette la largeur — c'est-à-dire l'information qui porte la cicatrice. Le saut ρ = 0,200 → 0,866 au cycle suivant la réouverture est la largeur qui s'effondre de 1 à 0.

Ce que chaque lecture donne, et ce qu'elle ne donne pas sans l'autre :

| | sans rétention (§ 5 absent) | avec rétention (§ 5) |
|---|---|---|
| **sans représentation** (§ 4 absent) | un choc, rien de plus | **une cicatrice innommable** — notre cas d'origine : douze cycles de cicatrice que le régime binaire étiquetait « hostile » |
| **avec représentation** (§ 4) | un état nommé qui s'efface en un cycle | une cicatrice représentable et durable |

L'hystérésis n'est donc ni l'une ni l'autre de ces deux lectures : c'est leur conjonction. Et le tableau vaut avertissement — la case en bas à gauche est celle où le protocole se trouvait avant aujourd'hui, et c'est la plus dangereuse, parce qu'elle produit toutes les apparences de la mémoire sans en fournir aucune des preuves.

Compteurs mesurés (défauts, graine 42) :

| Scénario | T | F | **B** | **N** | Lecture binaire |
|---|---|---|---|---|---|
| A (14 cycles) | 0 | 3 | **4** | **7** | 4 cycles de cicatrice lus comme hostilité |
| B (28 cycles) | 7 | 3 | **11** | **7** | 11 sur 28 |
| C (8 cycles) | 6 | 0 | **0** | **2** | — |

Deux constats à retenir :

1. **La cicatrice est un état.** Onze cycles du scénario B sont en B : le milieu est calme depuis onze pas et la membrane reste fermée. Un modèle binaire ne distingue pas « hostile, donc fermée » de « revenu, mais fermée » — c'est précisément la **persistance de la déformation** qu'une objection extérieure a demandé de mesurer (cf. `Trace(M_n)`, `Δκ` dans le corpus).
2. **Le choc bref produit N, pas F.** Sur le scénario C, la membrane transduit pendant les deux pulses : la fermeture exige une mémoire accumulée, donc **une hystérésis réactive est toujours en retard d'une rampe**. Avec la frontière à 0,50, toute la montée de pression du scénario A (0,55 → 0,95) compte comme N, soit 7 cycles où l'on transduit pendant qu'on est extrait. Ce n'est pas un seuil mal réglé, c'est structurel : le veto ne peut pas être armé avant d'avoir été exposé.

⚠️ Le compte de N dépend **entièrement** de `frontiere_admissible`, qui est un choix doctrinal et non une mesure. Un lecteur qui la déplace à 0,70 obtient un autre histogramme sans qu'aucune grandeur physique ait changé. C'est pourquoi elle est exposée comme paramètre.

---

## 5. Lecture homéostatique — et le seul test qui la discrimine

La tétravalence rend la cicatrice **représentable** ; elle ne la rend pas **durable**. Un état nommé qui s'efface au cycle suivant n'est qu'un nom. C'est ici qu'intervient la seconde lecture, et elle est plus sévère.

Au sens d'Ashby, un homéostat ne corrige pas une erreur vers une consigne : il **change ses propres mécanismes de pas** jusqu'à ramener une variable essentielle dans son domaine de viabilité, et il **retient** le réglage qui a marché. Formellement, deux échelles de temps :

```
rapide :  ρ_t = F(p_t, m_t, θ)                            (relaxation — le protocole d'origine)
lent   :  θ_{t+1} = θ_t − derive·1[p_t > frontière],       θ ≥ seuil_ouverture + 0,02
```

Le plancher (`MARGE_PLANCHER = 0.02`) est la viabilité : le système peut se fermer, pas se retourner contre lui-même.

**Le piège de méthode, d'abord.** Rejouer trois fois le scénario A sur le même objet fait glisser la fermeture de 8 à 1 — **avec des seuils parfaitement constants**. Ce glissement vient du flottant laissé par l'épisode précédent (0,435 en fin de scénario A, jamais descendu à zéro), pas d'un paramètre. Un test naïf conclurait donc à tort à une mémoire constitutive. Le seul test qui discrimine est `reinitialiser_memoire()` : remettre la mémoire cinétique à zéro **en gardant l'objet**.

| Variante | 1ᵉʳ passage | après remise à zéro de la mémoire |
|---|---|---|
| `derive = 0.00` (protocole d'origine) | fermeture au pas **8**, seuil 0,45 | fermeture au pas **8**, seuil 0,45 — inchangé |
| `derive = 0.05` (homéostat) | fermeture au pas **4**, seuil 0,17 | fermeture au pas **3**, seuil 0,17 — **déplacé** |

Si la fermeture revient au même pas, la mémoire était entièrement dans le flottant : hystérésis **cinétique**, cicatrice effaçable. Si elle reste avancée, un paramètre a bougé : mémoire **paramétrique**, cicatrice constitutive.

Critère géométrique, pour finir : dans le plan (p, ρ), une hystérésis cinétique décrit une **boucle fermée** — on revient au point de départ, l'aire est l'énergie dissipée par cycle. Une hystérésis paramétrique décrit une boucle **qui ne se referme pas** : le système ne revient pas à son état initial, et l'aire entre les deux passages n'est plus une dissipation mais une **inscription**. C'est la différence entre une cicatrice et une mémoire, et c'est exactement la place de `M_n` et de `Δκ` dans le corpus.

Cohérence doctrinale : `Σ₂` est un **frein sans accélérateur**, donc la branche fermante seulement. La lecture homéostatique dit pourquoi — la réouverture exige que le plancher soit relevé **de l'extérieur**, par un tiers. Un système qui ne peut que fermer n'est pas instable : il est *mourant*, ce qui est cohérent, mais qui doit être écrit.

---

## 6. Sensibilité mesurée — un paramètre à la fois

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

### Amendement du 2026-10-26 — amplitude contre durée

Objection reçue sur le post du 26/10 : le scénario B isole la **durée**, pas l'**amplitude** — le poids de mémoire réglerait la profondeur du puits, la décroissance seulement sa vitesse de vidage. Test demandé : `poids_memoire` à 0,85 / 0,60 / 0,35, décroissance et graine fixées, l'amplitude n'étant déclarée contrôlante que si l'indice de réouverture décroît **strictement**.

| Bras | `poids_memoire` | Poids effectifs (mémoire / redondance / coût) | Fermeture | Réouverture |
|---|---|---|---|---|
| tel quel | 0,85 | 0,850 / 0,100 / 0,050 | pas 8 | pas 22 |
| tel quel | 0,60 | 0,800 / 0,133 / 0,067 | pas 8 | pas 22 |
| tel quel | 0,35 | 0,700 / 0,200 / 0,100 | pas 9 | pas 21 |
| déconfondu | 0,85 | écrits directement | pas 8 | pas 22 |
| déconfondu | 0,60 | écrits directement | **jamais** | — |
| déconfondu | 0,35 | écrits directement | **jamais** | — |

Deux enseignements.

1. **Le test tel quel est confondu — par notre propre code.** La renormalisation fait monter les deux pénalités quand on baisse le poids de mémoire ; le gain d'un cycle à 0,35 vient de là, et non de l'amplitude. C'est encore une erreur de spécification, et elle est de notre côté, pas de celui de l'objection.
2. **Déconfondu, l'amplitude ne règle pas la durée : elle règle l'existence.** À 0,60, le score de fermeture n'atteint jamais son seuil (maximum 0,40 pour un seuil de 0,45) : la membrane ne se ferme pas, donc il n'y a aucune cicatrice dont mesurer la durée. La question « combien de temps » n'est définie que si la fermeture a eu lieu.

**Le seuil a une forme close — et ce n'est pas « ~0,60 ».** Un balayage fin du bras déconfondu localise le point de bascule :

```
w_m* = (0,45 − w_r·r − w_c·c) / m_max = (0,45 − 0,0475) / 0,5877 = 0,6849
```

Bissection numérique sur le code : **0,6849**, identique. En dessous, la membrane ne se ferme jamais ; au-dessus, elle se ferme.

**Et la durée n'appartient pas au seul facteur de décroissance.** Mesuré, même bras :

| `poids_memoire` | fermeture | réouverture | cicatrice |
|---|---|---|---|
| 0,70 | pas 10 | pas 21 | **11** |
| 0,75 | pas 9 | pas 21 | **12** |
| 0,80 | pas 9 | pas 22 | **13** |
| 0,85 | pas 8 | pas 22 | **14** |

La raison est dans le critère de réouverture : il exige `m < (0,15 − 0,0475)/w_m = 0,1025/w_m`. Plus l'amplitude est forte, plus le seuil sur la mémoire est bas, plus la cicatrice est longue. L'amplitude gouverne donc **l'existence** et **module la durée** ; la décroissance en reste le facteur dominant, pas le seul.

Formulation corrigée, à substituer à celle du § 3 : *la pression décide du moment de la fermeture ; l'amplitude décide qu'il y ait fermeture (seuil 0,6849) et module la durée ; la décroissance en reste le facteur dominant.*

Reproductible : [`experiments/b_gate_test_amplitude_2026-10-26.py`](../experiments/b_gate_test_amplitude_2026-10-26.py) · [`experiments/b_gate_seuil_amplitude_2026-10-26.py`](../experiments/b_gate_seuil_amplitude_2026-10-26.py).

---

## 7. Ce que la mesure met en défaut (à discuter, pas à corriger en silence)

1. **Le plafond de réouverture ne tient qu'un cycle.** `porosite_reouverture_max = 0.20` s'applique bien au cycle de réouverture (ρ = 0.200 au pas 22), mais dès le pas suivant le code affecte `ρ = score`, soit **0.866** — un retour quasi plein débit, exactement ce que le paramètre prétendait interdire. Le garde-fou protège l'instant, pas la rampe. Piste : borner la remontée (`ρ ← min(score, ρ_précédent + pas)`), ce qui rend le plafond lisible sur plusieurs cycles.
2. **Le seuil de fermeture est lu à l'envers de son nom.** `seuil_fermeture = 0.45` ferme quand `hab < 0.55` : plus le chiffre est petit, plus la membrane est *difficile* à fermer. La docstring dit « pression d'habitabilité inverse », ce qui est juste mais invite à l'erreur de lecture ; un nom du type `marge_fermeture` lèverait l'ambiguïté.
3. **ρ n'est pas une porosité mesurée.** C'est `score` recopié (ou 0 en silence). Les quatre grandeurs suivies ne sont donc pas homogènes : ρ est dérivé d'un score composite, la mémoire est une moyenne exponentielle, l'Active-Silence est un booléen, l'hystérésis se lit dans l'écart entre deux seuils. Un ρ identique dans deux expériences ne prouve rien tant que la table des entrées et des poids n'est pas publiée.

   *Précision ajoutée le 2026-10-25.* Il y a en réalité **deux mémoires** dans [l'objet d'état](../experiments/b_gate_mttv_flp_epreuve.py:56) : `memoire_pression` (un flottant, moyenne exponentielle) et `historique` (une liste, un dictionnaire par cycle : pression, habitabilité, mémoire, ρ, régime), alimentée à [chaque `forward()`](../experiments/b_gate_mttv_flp_epreuve.py:173). La première **informe** la décision ; la seconde l'**enregistre** et n'est **jamais relue** par le critère — elle est en écriture seule du point de vue de la décision. C'est une asymétrie à consigner : le système observe tout et n'utilise qu'un nombre.

   Corollaire pour la discussion avec @vina : le journal rend la trajectoire **auditable par un tiers** (on peut y vérifier la fermeture au pas 8 et la cicatrice de 12 cycles, et le contredire), mais il n'est pas un **invariant**. Un journal dit ce qui a eu lieu ; un invariant contraint ce qui peut avoir lieu. `M_n` et `Δκ` sont de la seconde espèce ; `historique` est de la première.

---

## 8. Invitation

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

## 9. Position de ce script dans le corpus

Ce fichier est un **outil d'épreuve isolé**, pas le noyau. Il ne remplace aucune des deux B-Gate déjà présentes dans le dépôt, et ne doit pas être confondu avec elles :

| | `BGateTransduction` ([`core/mttv_b_gate_triptych.md`](../core/mttv_b_gate_triptych.md)) | `BGateTransductionPoreuseExécutable` ([`expansion_v2026.5/axe1_bgate_v2026_5.py`](../expansion_v2026.5/axe1_bgate_v2026_5.py)) | `AdvancedBGate` (ce protocole) |
|---|---|---|---|
| Nature | noyau scalaire Ψ/B/Φ, triptyque sp³ | veto multi-critères V2026.5 | membrane jouet à mémoire et hystérésis |
| Critères | bascule sur tension d'extraction | 2 sur 3 : `drift`, `kappa`, `sclerose` | un score composite unique |
| η, κ, `Trace(M_n)` | non | oui | **non** |
| Hystérésis | à sens unique (seuil d'entrée, pas de retour) | oui, via κ armé par η | oui, deux seuils explicites + dérive paramétrique optionnelle (`derive`) |
| Sortie en silence | biomasse rechargée | suspension / dormance Φ-light | Hrön (bruit borné) |

Ce que le protocole ajoute au corpus : une **hystérésis à deux seuils nommés** et une **mémoire de pression explicite et datée**, donc une grandeur comparable dans le temps. Ce qu'il n'a pas : la distinction alerte/veto, la viscosité η, le rapport κ = π/η et la trace d'invariant. Les rapprocher (ou montrer qu'ils se contredisent) est un travail ouvert.

---

**Licence :** CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée / filsdelapensee.ch
**DOI du corpus :** [10.5281/zenodo.20830060](https://doi.org/10.5281/zenodo.20830060) · **Dépôt :** [github.com/gaillard111/mttv-flp-core](https://github.com/gaillard111/mttv-flp-core)
