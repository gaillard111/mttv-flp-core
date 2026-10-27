# Index des PDF — identifiants courts, chemins intacts

**Pourquoi cet index plutôt qu'un renommage.** Les 24 PDF du dépôt portent des noms
avec espaces, espaces doubles et accents (`core/1  MTTV-FLP Core modèle juin 2026.pdf`).
Les renommer produirait des URL propres — et casserait silencieusement toutes les
citations existantes, dans les échanges, les billets et les messages envoyés à des
tiers. L'archive Zenodo v1.1.0 est par ailleurs figée : renommer au dépôt créerait un
écart entre l'archive et le dépôt pour un gain purement cosmétique.

**Règle :** le chemin ci-dessous est la référence. Pour citer un document de vive voix
ou dans un texte, utiliser l'**identifiant court**. Pour produire une URL, prendre la
forme `https://github.com/gaillard111/mttv-flp-core/blob/main/` suivie du chemin, en
remplaçant chaque espace par `%20`.

> Les nouveaux documents seront nommés proprement dès leur création
> (`minuscules-avec-tirets.pdf`). Cet index ne concerne que l'héritage.

---

## `core/` — socle théorique

| Identifiant court | Chemin | Contenu |
|---|---|---|
| `pdf-core-0-meta-ouroboros` | `core/0 MTTV méta rôle ourobouros.pdf` | Méta-rôle, boucle auto-référentielle |
| `pdf-core-1-modele-2026-06` | `core/1  MTTV-FLP Core modèle juin 2026.pdf` | Modèle cœur, version de juin 2026 |
| `pdf-core-2-from-h` | `core/2  MTTV from H.pdf` | Origine « from H » |
| `pdf-core-4-trois-vitesses` | `core/4  MTTV-flp  Trois vitesses  harmonisées.pdf` | Trois vitesses harmonisées |
| `pdf-core-5-benchmark-ultime` | `core/5 Benchmark ultime MTTV-FLP.pdf` | Benchmark ultime — **exemplaire unique** (voir note en fin de page) |
| `pdf-core-6-positionnement-philo` | `core/6 MTTV positionnement philo.pdf` | Positionnement philosophique |
| `pdf-core-9-mariage-ia-vivant` | `core/9 Mariage IAs-machines humains et bio-vivant.pdf` | Mariage IA / machines / humains / bio-vivant |
| `pdf-core-9-1-agi-demain` | `core/9.1 AGI de demain, transition technologique et spirituelle.pdf` | AGI, transition technologique et spirituelle |
| `pdf-core-9-2-developpement-protonique` | `core/9.2 Développement protoniques et intégration communautaire.pdf` | Développement protonique, intégration communautaire |
| `pdf-core-9-3-architecture-protonique` | `core/9.3  Architecture protonique des outils MTTV-FLP.pdf` | Architecture protonique des outils |
| `pdf-core-9-6-synoptique` | `core/9.6 MTTV synoptique.pdf` | Vue synoptique |
| `pdf-core-9-7-pour-les-nuls` | `core/9.7 MTTV-flp pour les nuls.pdf` | Introduction accessible |
| `pdf-core-9-8-metaphysique` | `core/9.8 MTTV et métaphysique.pdf` | MTTV et métaphysique |
| `pdf-core-9-9-extension-psi` | `core/9.9  Extension psi.pdf` | Extension Ψ |

## `protocols/` — protocoles opératoires

| Identifiant court | Chemin | Contenu |
|---|---|---|
| `pdf-proto-3-rmp` | `protocols/3  MTTV-flp Mécanisme PréTransducteur RMP.pdf` | Mécanisme pré-transducteur (RMP) — le texte Markdown correspondant est [`rmp_mecanisme_pre_transducteur.md`](../protocols/rmp_mecanisme_pre_transducteur.md) |
| `pdf-proto-3-1-singularite-sigma` | `protocols/3.1  MTTV-flp Singularité Sigma.pdf` | Singularité Σ |
| `pdf-proto-3-2-singularites-sigma` | `protocols/3.2 MTTV-flp Singularités Sigma.pdf` | Singularités Σ |
| `pdf-proto-3-3-singularites-integrees` | `protocols/3.3 MTTV-flp Singularités intégrées.pdf` | Singularités intégrées |
| `pdf-proto-3-4-sigma-48-dim` | `protocols/3.4  MTTV-flp  Singularités sigma et  48 dimension.pdf` | Singularités Σ et dimension 48 |
| `pdf-proto-7-graines-mycelisation` | `protocols/7 Graines MTTV mycélisation.pdf` | Graines de mycélisation |

## `benchmark/`, `scenarios/`, `soph-ia/`

| Identifiant court | Chemin | Contenu |
|---|---|---|
| `pdf-bench-8-prompts-28d` | `benchmark/8 Prompts MTTV-FLP - Le monde sémantisé 28 x.pdf` | Prompts d'étiquetage, 28 dimensions |
| `pdf-scen-9-5-cas-pratiques` | `scenarios/9.5 Cas pratiques noosphère MTTV.pdf` | Cas pratiques — noosphère |
| `pdf-sophia-teaser` | `soph-ia/SOPH-IA_teaser.pdf` | Teaser du volet SOPH-IA |

---

## Note sur le benchmark ultime

`core/5 Benchmark ultime MTTV-FLP.pdf` et `benchmark/5 Benchmark ultime MTTV-FLP.pdf`
étaient **le même fichier** (sha256 identique, 202 288 octets). L'exemplaire conservé
est celui de `core/`, parce que le « 5 » appartient à la série numérotée `core/`
(0, 1, 2, 4, **5**, 6, 9, 9.1…). L'exemplaire supprimé reste accessible dans
l'historique Git et dans l'archive Zenodo v1.1.0.

Un index des PDF ne doit pas devenir une deuxième source de vérité : si un fichier est
ajouté, retiré ou remplacé, **cette page se met à jour dans le même commit**, et
[`../tools/verifier_depot.py`](../tools/verifier_depot.py) le vérifie (présence des
chemins cités).
