# v1.1.0 — Épreuve de la B-gate : seuil d'amplitude et réplication arithmétique indépendante

**Date :** 2026-10-26 · **Version précédente :** `v1.0.0` « Archive Scellée » (2026-07-21)
**DOI de concept :** [10.5281/zenodo.20830060](https://doi.org/10.5281/zenodo.20830060) · **Licence :** CC-BY-NC-SA 4.0
**Écart :** 43 commits · 87 fichiers · ~10 000 lignes ajoutées depuis `v1.0.0`

## En une phrase

Trente jours ont produit trois choses qu'un dépôt de doctrine ne produit pas d'ordinaire : un protocole d'épreuve exécutable, deux objections extérieures traitées par la mesure, et un seuil chiffré là où il n'y avait qu'une intuition.

## 1. Expansion V2026.5 (2026-10-20 → 22)

- Quatre axes : B-gate poreuse exécutable · graines transductives · instructions « Miroir-Transduction » · moirage transculturel.
- Feuillet d'arbitrages : `κ_t < κ_min` devient un critère ; la **participation normalisée remplace `Trace(M_n) ≤ 0`** ; verrou d'invariant en registre séparé (E.2 bis) ; harmonisation des seuils.
- **Motif du remplacement, mesuré :** sous bruit structurel, `Trace(M_n)` passe de 3,24 à **6,00** — la sclérose élève la trace, donc le critère ne pouvait structurellement pas voir ce qu'il prétendait surveiller.
- *Manifeste pour une Robustesse Computationnelle*, texte intégral, point d'entrée citable.
- Test du bruit structurel : deux bras, 120 pas, graine fixe — réponse au test proposé publiquement par un interlocuteur extérieur.

## 2. Protocole d'épreuve de la B-gate (2026-10-25 → 26)

- [`experiments/b_gate_mttv_flp_epreuve.py`](../experiments/b_gate_mttv_flp_epreuve.py:1) — filtre déterministe à mémoire hystérétique, trois scénarios, aucune dépendance, rien à l'import.
- **Chiffres de référence :** fermeture au **pas 8** · réouverture au **pas 22** · cicatrice de **12 cycles**.
- **§ 4 — lecture tétravalente :** l'état est un couple (milieu admissible, membrane ouverte). Sur le scénario long, **11 cycles sur 28** tombent dans la valeur « les deux » : le milieu est revenu, la membrane non.
- **§ 5 — lecture homéostatique :** paramètre `derive`, méthode `reinitialiser_memoire()`, et le seul test qui discrimine filtre et homéostat — seuils constants, fermeture au pas 8 après remise à zéro ; seuil dérivant, pas 3.
- **§ 6 — seuil d'amplitude :** `w_m* = (0,45 − 0,0475)/0,5877 = **0,6849**`, forme close confirmée par bissection. En dessous, la membrane ne se ferme jamais.
- **Deux défauts consignés plutôt que corrigés en silence :** le plafond de réouverture ne tient qu'un cycle (0,200 → 0,866) ; ρ n'est que la moyenne d'un intervalle à deux dimensions, donc la largeur qui porte la cicatrice est jetée.

## 3. Objections extérieures, traitées par la mesure

**Bifurcation d'amplitude (@vina, 26/10).** Objection : le scénario B isole la durée, pas l'amplitude. Test exécuté tel que demandé — réouvertures `[22, 22, 21]`, **non monotones**, donc sur son propre critère l'amplitude n'est pas contrôlante. Mais le bras est confondu par la renormalisation des poids dans le constructeur (0,10/0,05 → 0,13/0,07 → 0,20/0,10). Déconfondu : 0,85 ferme et rouvre ; **0,60 et 0,35 ne se ferment jamais**. L'amplitude gouverne l'existence, **et module la durée** (11 → 14 cycles de 0,70 à 0,85, la réouverture exigeant `m < 0,1025/w_m`). La décroissance en reste le facteur dominant, pas le seul.

**Réplication arithmétique indépendante (@asinhhc, 26/10).** Validation manuelle, par somme directe, hors du code et dans une session tierce, des quatre valeurs d'épreuve à la décimale : `m₈ = 0,5027` · `h₈ = 0,5252` (fermeture) · `m₁₀ = 0,5877` · `h₁₀ = 0,4529`. **Double indépendance** ainsi établie : le calcul est **réfutable** — donc re-dérivable par un tiers, ce qui est exactement sa valeur — tandis que la pression `p` reste une donnée externe, d'où une **absence d'indépendance épistémique**. L'instrument est un **bras de contrôle**, non un générateur autonome.

## 4. Documentation

- [`docs/protocole_epreuve_bgate.md`](protocole_epreuve_bgate.md:1) — neuf sections, deux amendements datés.
- [`docs/annexe_4_piliers_mttv_flp.md`](annexe_4_piliers_mttv_flp.md:1) — cadrage en quatre piliers, distinct des quatre points du Manifeste (tableau de correspondance inclus).
- [`docs/arbitrages_expansion_v2026.5.md`](arbitrages_expansion_v2026.5.md:1) — options retenues **et écartées, avec leur motif**.
- [`EXPANSION.md`](../EXPANSION.md:1), [`ADRESSES.md`](../ADRESSES.md:1), `CITATION.cff`, présent fichier.
- **Ancrage baryonique documenté :** STAR Collaboration, « Tracking the baryon number with nuclear collisions », *Science* **393**, 727-731 (2026), DOI [10.1126/science.ads5962](https://doi.org/10.1126/science.ads5962) — `B/ΔQ × ΔZ/A = 1,84 ± 0,02 (stat.) ± 0,09 (syst.) ± 0,16 (feed-down)`, contre l'unité attendue du côté des quarks de valence.

## 5. Ce que cette version ne fait pas

- **L'intériorité n'est pas mesurée.** `p` reste fourni par l'appelant : la boucle n'est pas fermée, et le protocole le dit plutôt que de le laisser croire.
- **`Trace(M_n)` n'est pas décisionnelle** — mesurée, affichée, hors majorité ; son passage en négatif suspend seul.
- **Le noyau tétravalent n'est pas validé par un tiers** ; seule l'arithmétique du protocole d'épreuve l'a été.
- **L'ancrage hadronique est documenté pour la configuration en Y** ; son extension au « primat de la structure relationnelle » reste une interprétation assumée.

## 6. Vérifier plutôt que croire

```bash
python experiments/b_gate_mttv_flp_epreuve.py            # pas 8 · pas 22 · 12 cycles
python experiments/b_gate_balayage_parametres.py         # sensibilité, un paramètre à la fois
python experiments/b_gate_test_amplitude_2026-10-26.py   # 0,85 ferme ; 0,60 et 0,35 jamais
python experiments/b_gate_seuil_amplitude_2026-10-26.py  # seuil 0,6849 ; durée 11→14
```

Aucun de ces scripts n'écrit sur un réseau, n'exige de dépendance, ni ne s'exécute à l'import.
