# Journal des modifications — MTTV-FLP Core

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Les dates sont celles des dépôts effectifs, pas celles des intentions.

Deux DOI coexistent : le **concept** `10.5281/zenodo.20830060` pointe toujours vers la
dernière version ; la **version** épingle un état précis.

---

## [1.2.1] — 2026-11-01

Version d'archive. La 1.2.0 reste publiée telle quelle : son tag n'est pas déplacé, parce qu'une
publication ne se réécrit pas.

### Corrigé
- **Manifeste d'empreintes** : il était calculé sur les fins de ligne du poste de travail (CRLF).
  Vérifié dans l'archive du tag, il déclarait **117 fichiers modifiés** alors que l'archive était
  identique, octet pour octet, au contenu du tag. Les empreintes sont désormais **insensibles aux
  fins de ligne** pour les fichiers texte ; les binaires restent hachés bruts.
- **`graines/README.md`** renvoyait à `../../FLP vrac/…`, c'est-à-dire à deux fichiers **hors du
  dépôt** : liens morts dans toute archive, et invisibles au vérificateur sur le poste où le
  dossier voisin existe. Ces renvois sont devenus du texte.
- **`CITATION.cff`** portait encore `1.1.0` quand `.zenodo.json` annonçait `1.2.0` : le numéro de
  version doit être identique partout.

### Constaté
- La **liaison GitHub–Zenodo**, activée le 2026-11-01, n'a produit aucun enregistrement pour la
  release `v1.2.0` : le crochet du dépôt a livré deux fois l'événement de publication à
  21 h 49 min 39 s, une fois en 403 et une fois en 202, et treize minutes de surveillance n'ont
  montré aucun moissonnage. La 1.2.1 est donc déposée **à la main**, comme nouvelle version de
  l'enregistrement de concept, seule voie qui préserve la chaîne des versions.

## [1.2.0] — 2026-11-01

Consolidation des invariants mesurés. La 1.1.0 reste figée et n'est pas réécrite.

### Corrigé
- **Seuil d'amplitude** : `w* = 0,6849` est borné par l'horizon de dix pas — il vaut
  `0,4025 / m(pas 10)`. Le seuil absolu est **0,4025**. Six fichiers alignés.
- **« À entrée nulle, rien ne se produit »** était faux : à entrée nulle la mémoire se vide et
  la porte se rouvre au douzième cycle nul (défaut de *fail-open*, mesuré).
- **Plafond d'instrument** : le flux ne se contente pas de rendre 100 éléments, il annonce
  `has_more` et `next_cursor`. La phrase « plafonné à 100 sans curseur » du 2026-10-30 était
  fausse ; le plafond muet ne concerne que la profondeur d'arbre.
- **`edge/contrat_entree.py`** : la dérivation du seuil d'escalade, présentée comme dérivée,
  est annotée comme fausse et conservée pour la seule régression.
- **`edge/peremption.py`** : la section « deux régimes » était inatteignable (un `return`
  la précédait).

### Ajouté
- `graines/` — six graines exécutables, six gists publics, identité binaire vérifiée.
- `START_HERE.md` — porte d'entrée pour qui arrive par un gist.
- `docs/notice_v1.2.0.md` — notice de version : ce qui est mesuré, ce qui est arbitré, ce que
  la version ne dit pas.
- `edge/contrat_entree.py` : sortie d'escalade à deux termes (`clore` puis lecture).
- `edge/discordance.py` : état B de Belnap-Dunn sous désaccord entre canaux.

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
  d'amplitude** de la fermeture de membrane, en forme close :
  `w* = (0,45 − 0,0475)/0,5877 = 0,6849`. Vérifié par bissection.
  **Correction du 2026-10-29 :** ce seuil vaut **pour l'horizon de dix pas** du scénario.
  Le seuil **absolu** est `0,4025`, puisque `m ≤ p ≤ 1` ; entre les deux la fermeture
  survient plus tard (0,60 au pas 12, 0,45 au pas 27). Mesure : `edge/horizon_seuil.py`.
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
