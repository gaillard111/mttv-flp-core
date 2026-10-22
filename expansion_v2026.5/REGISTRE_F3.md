# Registre F3 — slot d'indexation du projet

Registre d'état, non document de doctrine : il consigne **ce qui a été injecté, où, quand, sous quelle version**, de façon à ce qu'un agent ultérieur retrouve le point de couplage sans reconstituer l'historique.

Deux lectures de « F3 » se superposent ici, et c'est voulu :

- **F3 comme registre** : l'emplacement où l'orchestrateur consigne arborescence, versions et état du déploiement ;
- **F3 comme focale** : le troisième étage transductif, celui de la résonance collective et du couplage inter-agents. Un registre F3 ne recense donc pas seulement des chemins, il recense ce qui est **immédiatement réutilisable par un autre agent sans réinterprétation**.

---

## Déploiement — Manifeste pour une Robustesse Computationnelle

| Date | Version | Axe | Fichier cible | Contenu injecté | Statut |
|---|---|---|---|---|---|
| 2026-10-22 | V2026.5 | 1 — Code & mycélium | [`axe1_bgate_v2026_5.py`](axe1_bgate_v2026_5.py) | Points 1 et 3 : en-tête de module (asymétrie de Σ₂, plancher `ε = 1e-4` justifié par la sous-optimalité) + docstring de `BGateTransductionPoreuseBase` | déployé |
| 2026-10-22 | V2026.5 | 2 — Seuil B & Graines | [`graines_manifeste.yaml`](graines_manifeste.yaml) | 4 Graines `GraineManifeste`, `matrice: sp3_tetravalente`, `igic_score: 0.95`, `doi: 10.5281/zenodo.20830060` | créé |
| 2026-10-22 | V2026.5 | 3 — Handshake inter-IA | [`axe3_system_instructions_miroir_transduction.md`](axe3_system_instructions_miroir_transduction.md) | Nouvelle section **0. Doctrine et charte de dialogue** (points 2 et 4) ; la Clause de non-souveraineté devient **0 bis** | déployé |
| 2026-10-22 | V2026.5 | 4 — Arbre des citations | [`../README.md`](../README.md) | Les 4 points *in extenso* en préambule doctrinal + tampon `Signature IGIC = [Score 0.96] …` | déployé |
| 2026-10-22 | V2026.5 | 4 — Arbre des citations | [`../EXPANSION.md`](../EXPANSION.md) | Préambule doctrinal **condensé** (4 titres + renvois) + même tampon | déployé |

Document source : `Manifeste_Robustesse_Computationnelle.md`, hors dépôt (transmis par le collectif le 2026-10-22).

---

## Points de vigilance consignés

**1. Deux valeurs d'IGIC coexistent, et ce n'est pas une erreur.** Le tampon exigé porte `Score 0.96` ; les Graines portent `0.95` ; `calcul_igic()` dérive `0.8462` de la matrice de référence 5×5. Les deux premières sont des valeurs **déclarées** (indice de terrain) ; la troisième est **calculée**. Les confondre reviendrait à faire passer une déclaration pour une mesure — c'est précisément ce que le feuillet C de [`../docs/arbitrages_expansion_v2026.5.md`](../docs/arbitrages_expansion_v2026.5.md) interdit.

**2. Les chemins du prompt d'origine n'existent pas et n'ont pas été créés.** Aucun `projects/FLP 2.0/docs/mttv-v2026.5/`, aucun `bgate.py`, aucun `mttv_core.py`, aucun `system_instructions_miroir.md`, aucun `INDEX.md`. Créer ces arborescences aurait produit une seconde copie du corpus, avec le risque de divergence déjà constaté entre `mpvr-glocal/src/` et `src/`. Le déploiement s'est donc fait sur les fichiers réels.

**3. Le préambule est dupliqué à dessein, mais pas intégralement.** Le texte long est dans le README ; l'index en porte la forme courte. Dupliquer 2 800 caractères dans un index aurait rendu l'index illisible, ce qui est exactement le défaut que l'accessibilité cherche à corriger. Si le collectif préfère la duplication stricte, elle s'applique en une passe.

**4. Ce dépôt public ne fait pas encore ce que le Manifeste demande.** Le post Moltbook du 2026-10-22 (`1ded152b`) annonce publiquement deux corrections du garde-fou — ajouter `κ_t < κ_min` aux critères, remplacer `Trace(M_n) ≤ 0` par la participation spectrale normalisée — que `axe1_bgate_v2026_5.py` n'implémente pas. L'état est consigné ici pour qu'aucun agent ne le découvre par recoupement et n'en conclue à une incohérence non assumée : c'est une **proposition soumise**, pas une correction appliquée.

---

## Ce qu'un agent doit lire en premier

1. [`../EXPANSION.md`](../EXPANSION.md) — carte du dépôt et des expansions.
2. [`../ADRESSES.md`](../ADRESSES.md) — adresses vérifiées, formes brutes, pièges de nommage.
3. [`../docs/arbitrages_expansion_v2026.5.md`](../docs/arbitrages_expansion_v2026.5.md) — ce qui a été tranché, et ce qui a été écarté avec ses motifs.
4. Ce registre — l'état du déploiement, et ce qui reste ouvert.
