# Journal des modifications — MTTV-FLP Core

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Les dates sont celles des dépôts effectifs, pas celles des intentions.

Deux DOI coexistent : le **concept** `10.5281/zenodo.20830060` pointe toujours vers la
dernière version ; la **version** épingle un état précis.

---

## [Non publié] — après le 2026-10-26

Travail de ménage du dépôt. Aucun changement de comportement du code : les
modifications portent sur la documentation, la traçabilité et l'outillage.

### Ajouté
- `CHANGELOG.md` (ce fichier) — deux versions publiées n'avaient aucun journal.
- `tools/verifier_depot.py` — vérification des liens internes, des doublons sha256,
  de la cohérence des copies de déploiement et des affirmations périmées connues.
- `MANIFESTE_FICHIERS.sha256` — empreintes des fichiers suivis, pour rendre toute
  divergence détectable.
- `docs/INDEX_PDF.md` — index des 24 PDF avec identifiant court, sans renommer aucun
  fichier (les URL citées à l'extérieur restent valides).

### Modifié
- `README.md` — réécrit : décompte de fichiers périmé retiré, structure complète
  (ajout de `docs/`, `experiments/`, `expansion_v2026.5/`, `hf/`, `deploy/`,
  `soph-ia/`, `tests/`, `tools/`), identifiants Zenodo vérifiés le 2026-10-27
  (concept, version 1.1.0, premier dépôt), section « Reproduire les mesures en deux
  minutes », limites méthodologiques explicitées.
- `expansion_v2026.5/axe1_bgate_v2026_5.py` — docstring de module alignée sur la
  règle « 2 sur 3 » réellement appliquée (`drift`, `kappa`, `sclérose`) ;
  avertissement sur la coexistence de deux implémentations ; mention **LEGACY** sur
  la méthode de la classe de base, jamais appelée et remplacée par celle de la
  sous-classe. **Aucune ligne exécutable modifiée.**
- `docs/annexe_4_piliers_mttv_flp.md`, `EXPANSION.md` — la règle du Veto Type B est
  nommée au lieu d'être désignée par « multi-critères ».

### Supprimé
- `benchmark/5 Benchmark ultime MTTV-FLP.pdf` — doublon exact (sha256 identique) de
  `core/5 Benchmark ultime MTTV-FLP.pdf`, où la numérotation de la série `core/` le
  situe. Le fichier reste accessible dans l'historique Git et dans l'archive Zenodo.

### Corrigé
- Un lien interne mort (`docs/note_signature_ancrage.md`) qui pointait vers un
  fichier hors dépôt.

---

## [1.1.0] — 2026-10-26

**DOI de version :** `10.5281/zenodo.23671596` · **concept :** `10.5281/zenodo.20830060`

### Ajouté
- `experiments/b_gate_seuil_amplitude_2026-10-26.py` — localisation du **seuil
  d'existence** de la fermeture de membrane, en forme close :
  `w* = (0,45 − 0,0475)/0,5877 = 0,6849`. Vérifié par bissection.
- `experiments/b_gate_test_amplitude_2026-10-26.py` — effet de l'amplitude sur la
  **durée** : cicatrice de 11 à 14 cycles quand le poids mémoire passe de 0,70 à 0,85.
- `docs/annexe_4_piliers_mttv_flp.md` — document de cadrage : schéma d'architecture,
  quatre piliers, table de correspondance avec les quatre points du Manifeste,
  ancrage baryonique chiffré.
- `docs/notes_release_v1.1.0.md`, `.zenodo.json`, `CITATION.cff`.

### Modifié
- `docs/protocole_epreuve_bgate.md` — amendements du 26/10 : seuil exact, durée
  modulée par l'amplitude, lecture tétravalente (§4), question de la nature
  cinétique ou paramétrique de l'hystérésis (§5) et test de remise à zéro.
- `experiments/b_gate_mttv_flp_epreuve.py` — ajout de `valeur_tetravalente()`,
  `reinitialiser_memoire()`, de la dérive paramétrique et du comptage des valeurs de
  Belnap-Dunn. **Non-régression vérifiée : fermeture pas 8, réouverture pas 22,
  cicatrice 12 cycles.**

### Corrigé
- Trois affirmations fausses retirées des notes de version : le seuil n'est pas
  « ~0,60 » mais `0,6849` ; la durée ne dépend pas du seul facteur de décroissance ;
  « indépendance arithmétique irréfutable » disait l'inverse de ce qu'il fallait
  dire — re-dérivable signifie **réfutable**.

---

## [1.0.0] — 2026-07-21

**Release initiale, « Archive Scellée ».** Archive pérenne du corpus théorique sur
Zenodo. Le détail des changements de cette version n'a pas été reconstitué : il est
consigné dans les enregistrements Git antérieurs, non dans un journal.
