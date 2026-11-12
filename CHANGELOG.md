# Journal des modifications — MTTV-FLP Core

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).
Les dates sont celles des dépôts effectifs, pas celles des intentions.

Deux DOI coexistent : le **concept** `10.5281/zenodo.20830060` pointe toujours vers la
dernière version ; la **version** épingle un état précis.

---

## [Non publié] — après le 2026-11-01

Travail sur `main`, postérieur à l'archive `10.5281/zenodo.23869556`. **Rien de ce qui suit n'est
archivé**, et rien ne doit être présenté comme tel avant une version ultérieure.

### Ajouté — neuvième graine : l'inconnu n'est ni une lecture ni une absence

- `graines/graine_unknown_troisieme_etat.py` — **147 lignes / 77 instructions**, aucune dépendance.
  Le défaut n'est pas dans la **valeur** d'une réponse mais dans sa **classe de décodage** : une
  porte à deux états range le troisième cas — la réponse qui a eu lieu et ne porte rien — d'un côté
  ou de l'autre, et se confond alors *exactement* avec l'un des deux états qu'elle connaît.
- **Mesuré, même protocole que la graine 1** (fermeture pas 8, réouverture pas 22 sous accord),
  quarante pas où le second canal répond `INCONNU` : défaut A, « toute réponse non nulle est une
  lecture » → réouverture au **pas 22**, soit le pas du calme mesuré ; défaut B, « l'inconnu est
  rangé avec l'absence » → **aucune** réouverture, soit l'absence vraie ; correctif C, trois classes
  décodées → aucune réouverture, `m` gelée à **0,5877**, compteur d'inconnues et **escalade au
  pas 40**. Re-dérivable : `m_n = 0,5877 × 0,9^n`, réouverture quand `m < 0,1677`, donc `n = 12`.
- **Le test qui échoue n'assère pas un comportement mais une séparation** : `INCONNU` et `ABSENCE`
  doivent laisser deux étiquettes distinctes dans la trace. La version fautive produit le même gel,
  au même pas, sans champ pour les distinguer — c'est-à-dire une panne et une attente confondues.
- **Provenance différente des huit autres** : première graine née d'une objection **extérieure** et
  non d'une erreur commise ici — @ymas, Moltbook, 2026-11-10, « absence is not zero, and neither is
  unknown », avec l'incident qui la rend mesurable : un registre de tâche affirmant `enabled,
  scheduled, last result ok` pendant **20,88 heures** sans artefact produit.
- **Choix déclaré, et non mesuré** : le seuil de 30 inconnues consécutives avant escalade. Rien ne
  le mesure, exactement comme `p < 0,15` et `r > 0,25`.
- Chaîne de détection : `CLASSE_INCONNUE_DECODEE`.
- `graines/README.md` — ligne de catalogue, provenance et **borne re-mesurée le 2026-11-11** :
  147/77 ; le maximum constaté ne bouge pas (166 lignes, 85 instructions), la borne 170/85 reste
  celle qui se vérifie.
- **Gist public figé le 2026-11-12** :
  <https://gist.github.com/gaillard111/d19cfff4a35ceaefe211d724f02c426a> — copie mécanique du
  fichier au commit `1ad8735`, jamais éditée ensuite.

### Ajouté — première mesure extérieure : un succès vert sans artefact

- `experiments/succes_sans_artefact.py` — la graine 9 posée **hors de nos modèles** : sur la liste
  des vingt dépôts de `collecteur_depots.py` (importée, jamais recopiée), combien ont une tâche
  planifiée en **succès** alors que le dernier artefact produit est plus vieux que la fenêtre
  déclarée de 30 jours. Deux requêtes par dépôt, aucune écriture, aucun jeton dans le code.
- **Deux passes le 2026-11-12, à deux minutes d'écart : 1 puis 2 cas**, sur 16 puis 17 dépôts lus.
  Les deux cas sont `great-expectations/great_expectations` et `elastic/elasticsearch-py` : vert le
  jour même, artefact vieux de **70** et **72** jours. Trois dépôts restent illisibles (HTTP 500 sur
  les artefacts) — déclarés, jamais comptés comme des zéros.
- **Ce que le chiffre ne dit pas** : ce n'est pas une prévalence, l'échantillon étant notre propre
  liste ; et le compte n'est pas stable à deux minutes, un workflow en cours ayant produit un
  artefact entre les deux passes. Un tel chiffre ne vaut qu'avec son horodatage.
- **Deux défauts de l'instrument corrigés dans l'heure** : un run `in_progress` (`conclusion: null`)
  était étiqueté « non vert », donc un travail en cours passait pour un échec ; un âge négatif
  s'imprimait au lieu d'être déclaré (`DATE_A_VENIR`).
- Détail daté : [`experiments/notes_succes_sans_artefact_2026-11-12.md`](experiments/notes_succes_sans_artefact_2026-11-12.md:1).

### Modifié — comportement du noyau
- **`BGateTransduction` : `Σ` cesse d'être un résidu recalculé.** Décision du 2026-11-02, option
  (b) : `Σ` est un **paramètre de l'opérateur** (`sigma_fixe`), la triade `Ψ + B + Φ` se partage
  `1 − Σ`, et l'invariant `Ψ + B + Φ + Σ = 1` est vérifié sur 100 000 flux à graine fixe. Trois
  conséquences mesurées par l'auto-test : le seuil ne tombe plus à 0 (un flux de 0,20 ne bascule
  pas sous `Σ = 0,25`), le souffle `Ψ` est réellement rechargé, et `ρ = moyenne × Σ` retrouve un
  sens en aval. L'option (a) — loi d'évolution de `Σ` — reste ouverte.
- **`MicroQuorumPoreux` déclaré démonstrateur** dans son propre en-tête : `evaluer_contexte()` tire
  ses nœuds et ses signaux avec `random`, donc aucun chiffre de ce module n'est citable.
- **Copie de déploiement** `hf/space/mttv_bgate_system.py` propagée à l'identique (le vérificateur
  l'exige, et il a raison : deux copies divergentes se découvrent toujours trop tard).

### Ajouté — documentation de propagation
- `docs/kit/` — index, quickstart, PoC edge, manifeste ; `docs/quickstart.md` et
  `docs/quickstart.en.md` ; `CONTRIBUTING.md` à la racine ; `docs/i18n/` (glossaire anglais).
- `docs/licences.md` — séparation des licences : noyau CC-BY-NC-SA, documents CC-BY-SA, manifeste
  CC0, MPVR CC0 ; la 1.2.1 déposée reste sous l'ancienne règle, par non-rétroactivité.
- `docs/ROADMAP.md` — ce qui est fait sur `main`, ce qui est différé avec ses critères de sortie, et
  les interdits qui restent des interdits.

### Ajouté — contre-exemple outillé
- `experiments/connecteur_binaire_tetravalent.py` — un « Interoperability Gateway » reçu le
  2026-11-02 comme « spécifications de référence conformes au jalon Zenodo », rejoué hors de son
  cadre HTTP et conservé au crible. Trois défauts **mesurés** : la valuation est **constante**
  (`BOTH` quelle que soit l'entrée ; `T` et `F` jamais produits, `NEITHER` seulement si une chaîne
  est vide) ; l'identifiant est `hash()` de Python étiqueté « sha256 », donc **instable entre
  processus** (`9194…` puis `8684…` pour la même entrée) ; la « frugalité » vaut
  `1/(durée × 1000)` et **lève une division par zéro** quand la machine est trop rapide.
  Le crible échoue si l'un de ces défauts disparaît : un contre-exemple qui ne démontre plus rien
  est un contre-exemple mort. Chaîne de détection : `GATEWAY_BOTH_CONSTANT`.

### Ajouté — détecteur de frictions, couche L2
- `experiments/filtre_frictions.py` — filtre **lexical, déterministe, sans modèle** : des motifs
  par graine, des motifs négatifs qui disqualifient (éthique générale, accord enthousiaste,
  promotion, cadre complet), et un candidat qui porte **sa réfutation**. Aucun réseau, aucune
  écriture, aucune dépendance.
- **Jugé sur un jeu de référence** de dix frictions documentées et trente leurres, avec deux
  seuils : `rappel ≥ 8/10` et **zéro faux positif**. Le second seuil existe parce qu'un filtre qui
  ne rend rien aurait une précision parfaite et un rappel nul.
- **Le test a d'abord trouvé trois défauts dans le filtre lui-même** : une phrase sur l'horloge
  interne classée « seuil qui dérive » (motif générique évalué avant le spécifique), `announce`
  absent du vocabulaire anglais, et `median` admis à tort comme indice d'absence — l'imputation par
  la médiane est une pratique ordinaire, pas une friction. Après correction : **10/10 et 0/30**.
- Budget mesuré : **≈ 1,8 ms par item de 300 caractères**. La rédaction initiale annonçait
  « < 50 ms pour 1 000 items » : c'était une promesse, et elle était fausse d'un facteur 35.

### Ajouté — collecteur L1, et son échec mesuré
- `experiments/collecteur_github.py` — recherche d'issues GitHub **en lecture seule**, pagination
  suivie, plafond déclaré (`total_count`, `incomplete_results`), trois états par requête
  (`lu` / `NON LU` / `TRONQUE`). Banc hors ligne à fixture : la pagination, le plafond et la source
  muette sont testés **sans réseau**.
- **Premier passage réel, et il ne passe pas** : 500 items, **228 candidats (46 %)**, et une
  précision de **1/20, soit 5 %**, mesurée à la main sur les vingt premiers. Un seul candidat tient :
  `unknown costs are not treated as zero`.
- **Deux hypothèses réfutées, dans l'ordre** : borner le rapprochement à la phrase fait passer
  183 → 180 candidats (négligeable) ; exclure les pull requests (`is:issue`) fait passer
  180 → **228** (effet inverse). Le défaut n'est donc ni la fenêtre ni le type d'objet, mais la
  **recherche plein texte** — motifs trop larges, et corpus public désormais peuplé de tickets
  générés par des agents, qui emploient ce vocabulaire sans formuler aucune plainte.
- Le code et son banc restent ; l'entonnoir est déclaré **inutilisable en l'état**, et les deux
  pistes de correction sont inscrites dans `docs/ROADMAP.md` **à mesurer avant d'être affirmées**.

### Ajouté — seconde famille : les signes de réassurance
- Cinq frictions **réelles et dures**, fournies le 2026-11-02 par l'orchestrateur FLP 2.0 (un zéro
  qui avait l'air d'une réponse, une coche verte `✅ VALIDATION PASSED`, l'étiquette « comportement
  normal », un instrument muet, un écran bloqué), ont été passées au filtre : **0 sur 5 détectées**.
  Diagnostic : dans ces cas la douleur n'est pas dans les mots, elle est dans un **signe de
  réussite** qui recouvre une absence. Un filtre à mots de douleur y est structurellement aveugle.
- Ajout d'une seconde famille, `a_relire` — réussite affirmée, zéro présenté comme réponse, mutisme
  déclaré, étiquette de normalité, blocage subi. Elle ne rend pas des candidats mais des **textes à
  relire**, avec la question à poser : « le signe couvre-t-il une absence, ou est-il exact ? »
  Sortie volontairement séparée : mêler un doute à un candidat serait la faute reprochée aux autres.
- Mesure : **cas durs relevés 5/5**, **bruit 0/30** sur les leurres, et la suite d'origine reste à
  **10/10 et 0/30**. Les cinq cas sont désormais dans le banc (`HARD_TEST`), et le test échoue si
  l'un d'eux cesse d'être dur ou cesse d'être relevé.
- **Contre-épreuve du même soir, et elle est sévère.** Six frictions neuves, dont deux graines
  jusque-là vides (G2 et G4), passées **sans réglage préalable** : **1 sur 6**. Seul `invisible` a
  été relevé. La famille de réassurance était donc **ajustée à ses cinq cas de mise au point** —
  sur-ajustement caractérisé, révélé par une fournée fraîche.
- Après extension du vocabulaire **à partir du corpus** et non de l'imagination — `0 rouge`,
  « logs est VIDE … aucune exécution prouvée », « sinon un reboot tue la mémoire », « unexpected end
  of hex escape », « le nom mentait », « un sort écrase le score », « palier 5 alors que » — la
  seconde fournée passe à **6/6**, sans dégrader le reste : 10/10, 0/30, 5/5, 0/30.
- **Le jeu de test est dépensé.** Ces six cas sont désormais dans l'entraînement. Toute mesure
  honnête de la version suivante exigera une fournée neuve, jamais relue avant d'être passée.

### Ajouté — collecteur L1 bis, « dépôts surveillés » : l'entonnoir se resserre
- `experiments/collecteur_depots.py` — 19 dépôts, une graine par dépôt, `Link: rel="next"` suivi,
  plafond déclaré, fenêtre `since` de 14 jours, **pull requests exclues à la lecture** (`pull_request`
  présent), trois états par dépôt. Banc hors ligne : pagination à deux pages, PR à écarter, dépôt
  muet, et un zéro qui avait l'air d'une réponse.
- **Passe réelle du 2026-11-02** : 19 dépôts, **427 items**, **0 dépôt muet**, 5 tronqués,
  **49 candidats — 11,5 %** des items, contre 46 % pour la recherche plein texte.
- **Précision mesurée à la main, vingt premiers candidats : 7/20, soit 35 %** — au-dessus du seuil
  de 30 % fixé d'avance. Retenus : `estimated_distance always reports 0.0 m due to falsy tx_power`,
  `an hour with no usable observations makes the AQI sensor report 0`, `battery sensors not
  discovered if value is none`, `config flow hangs forever`, `need a way to differentiate between
  unset and none programmatically`, `batch processor timeout accumulates drift over time`, et le
  `is_not_in` qui garde les lignes nulles sur pandas et les jette ailleurs.
- **Volume : 49 candidats par passe, au-dessus du seuil de 30.** Non corrigé ici : la fenêtre de
  14 jours en est la cause probable, et une fenêtre de 7 jours la diviserait par deux — à mesurer,
  pas à affirmer.
- **La famille `a_relire` sort 198 textes sur 427 items (46 %)** : elle n'a pas encore son budget de
  volume, et à ce niveau elle n'est pas relisible. À traiter comme un défaut ouvert, pas comme un
  succès.
- **Passe du soir, arbitrée** : `ros2/ros2` retiré (friction absente — 18 issues d'installation et de
  tickets générés par IA), `pola-rs/polars` et `apache/arrow` ajoutés en graine 4, fenêtre ramenée de
  14 à 7 jours. **La passe s'est arrêtée au dixième dépôt sur vingt : quota GitHub épuisé** (60
  requêtes/heure sans jeton). Le collecteur l'a déclaré — neuf `NON LU` avec motif, aucun faux
  « calme » — puis insistait neuf fois pour rien : il **s'arrête désormais au premier 403** et marque
  le reste « non tenté ».
- Sur les dix dépôts effectivement lus : 196 items, **19 candidats**, **précision 8/19 = 42 %** —
  meilleure que les 35 % de la veille, sur un échantillon plus petit. Trois nouveaux cas de graine 1
  valent d'être notés : `empty tables fail column checks and nullable=False` (pandera),
  `len(array)==0 omits missing array properties` (weaviate), et le déjà vu `unset` vs `none`.
- **Les deux dépôts ajoutés n'ont pas été atteints** : leur valeur reste inconnue, et ne sera pas
  affirmée avant d'avoir été mesurée.

### Ajouté — huitième graine : « borné », et le troisième état
- `graines/graine_borne_declaree.py` — propriété **P1**, *un nombre imprimé reste dans l'intervalle
  que son propre cadre définit*. Dix nombres, dont **cinq** sortent du cadre que leur texte nomme ;
  la version fautive — borne haute seule, absence de cadre lue comme conformité — en voit **2**.
  Les trois manquées passent toutes par la borne basse (−100 s, −1 s, −3 j) ; les deux nombres sans
  cadre sont déclarés conformes alors que rien ne permet de les juger. La correction voit **5 sur
  5** et rend `non visible` là où le texte ne nomme aucune borne. C'est ce troisième état, et non
  la garde sur les nombres négatifs, qui fait de ce cas une graine de propriété : sans cadre nommé,
  il n'y a plus rien à vérifier, et un instrument qui l'ignore fabrique du calme (graine 1).
  Cinq `assert`, aucune dépendance, aucun réseau. Chaîne de détection : `PROPRIETE_NON_TENUE`.
  `[mesuré]` — `python graines/graine_borne_declaree.py`.
- `graines/README.md` — catalogue, liste des chaînes valides (huit désormais), et **borne de taille
  de la partie 3 re-mesurée** : la rédaction « ≤ 120 lignes, ≤ 60 instructions » n'était tenue que
  par **4 graines sur 8** (109/54, 104/57, 84/38 et 111/58 la tiennent ; 164/69, 166/67, 147/73 et
  129/82 non). Le chiffre écrit était faux, comme en octobre pour les « 40 lignes utiles ». La
  borne devient ≤ 170 lignes et ≤ 85 instructions, avec la commande qui réimprime le tableau.
  `[choix]` — la valeur décrit le maximum constaté ; elle ne prescrit pas une taille.

### Modifié — graine 5 : la condition qu'une objection a rendue visible
- **L'objection**, reçue le 2026-11-04 à 22:36 UTC sur Moltbook, sous le premier semis public, par
  @vina : *« Close, then read n'ouvre que si le canal de lecture reste hors du processus verrouillé ;
  de quel côté de la clôture était la sonde ? »* Vérification faite dans le code : la clôture est
  bien confiée à un tiers (`porte.clore("tiers")`), mais les lectures reviennent au **même objet**
  que celui qui s'est fermé — la porte les reçoit, elle ne les produit pas, et elle ne peut pas les
  refuser. Cette hypothèse n'était écrite nulle part.
- **`graines/graine_sortie_deux_termes.py` gagne un paramètre `sonde`** (`externe`, `retenue`,
  `forgee`) et un §6 qui nomme la condition. **Sa sortie publique est inchangée** : les trois
  placements, `AUCUNE`, `AUCUNE`, `pas 47`, et la chaîne `ATTENTE_LECTURE_APRES_CLOTURE` — ce que
  le commentaire du 22:30 promettait à un lecteur qui lance la commande. `[mesuré]` — **156 lignes /
  85 instructions**, la borne du catalogue tenue à l'unité près.
- **`experiments/sonde_du_cote_du_suspect.py` porte la mesure**, il ne l'affirme pas : **sonde
  retenue** (le suspect garde le capteur et ne le laisse pas parler) → `AUCUNE` ; la troisième place
  s'effondre sur la deuxième. **Sonde forgée** (le suspect rapporte lui-même le calme, puis le monde
  reprend la parole) → réouverture au pas **47**, puis **refermeture au pas 52** dès la première
  vraie lecture, soit **cinq pas** de sortie achetée. `[mesuré]` — `python
  experiments/sonde_du_cote_du_suspect.py`. Chaîne de détection :
  `SONDE_DANS_LE_PERIMETRE_VERROUILLE`.
- **Ce que le chiffre devient.** Le 47 n'est pas un critère mais une condition : une observation que
  le suspect ne peut ni taire ni écrire. Les `assert` d'origine sont conservés ; deux nouveaux
  échouent si la condition disparaît, et un troisième si elle est mal placée.

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

### Déposé
- **DOI de version :** `10.5281/zenodo.23869556` · **concept :** `10.5281/zenodo.20830060`, qui
  résout désormais sur la 1.2.1.
- Archive : `mttv-flp-core-v1.2.1.zip`, **4 207 084 octets**, MD5
  `16b2005d13d1c4a9f5db7077080c070d`, sha256
  `385F35B47EB4163AE427107C230EED3E8E5514444376AB7A89CB474890FC2B11`.
- **Vérifiée après dépôt, dans son état téléchargé depuis Zenodo** : `python
  tools/verifier_depot.py` rend « dépôt cohérent » ; notice et `START_HERE.md` présents ;
  `.zenodo.json` en `1.2.1`. Contrôles par l'API : `conceptdoi` = `10.5281/zenodo.20830060`,
  version `1.2.1`, date `2026-11-01`, un seul fichier, empreinte identique à celle déposée.
- **Deux écarts assumés, nommés ici parce qu'ils sont dans l'archive.** (1) Le `.zenodo.json`
  déposé porte `isSupplementTo` sur le tag `v1.2.0` : il avait été écrit avant l'existence de la
  1.2.1, et un dépôt manuel ne relit pas ce fichier — les champs ont été saisis dans le
  formulaire. (2) Les identifiants liés du formulaire ont été vidés de l'attribution fausse
  (`17940301`, « MTTV Fundamentals », n'est pas une version antérieure du noyau) et n'ont pas été
  reconstitués ce soir ; la chaîne des versions, elle, est portée par Zenodo lui-même.

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
