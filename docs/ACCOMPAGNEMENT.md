# Documentation d'accompagnement — MTTV-FLP Core

**Objet** : permettre à un lecteur, un chercheur ou un développeur d'entrer dans le dépôt sans s'y perdre.
**Dossier** : `docs/` — documentation technique et d'accompagnement.

---

## 1. À qui s'adresse ce dépôt

| Profil | Parcours conseillé | Temps |
|---|---|---|
| **Curieux** | [`README.md`](../README.md) → [`core/mttv_flp_synthese_manifeste.md`](../core/mttv_flp_synthese_manifeste.md) | 30 min |
| **Chercheur / philosophe** | [`SYNTHESE_MTTV_FLP.md`](../SYNTHESE_MTTV_FLP.md) → [`core/`](../core/) → [`protocols/`](../protocols/) → [`benchmark/`](../benchmark/) | 2-3 h |
| **Développeur** | [`src/mttv_mpvr_quorum.py`](../src/mttv_mpvr_quorum.py) → [`tests/test_sigma4.ipynb`](../tests/test_sigma4.ipynb) → [`mpvr-glocal/README.md`](../mpvr-glocal/README.md) → [`docs/t4_activation_function.md`](t4_activation_function.md) | 1 h |

## 2. Carte du dépôt

| Dossier | Contenu | Nature |
|---|---|---|
| `core/` | Noyau théorique : modèle, positionnement, métaphysique, manifeste | 14 PDF + 1 Markdown |
| `protocols/` | Protocoles opératoires : RMP, Singularité Σ, graines de mycélisation | 6 PDF |
| `benchmark/` | Benchmark ultime, prompts d'étiquetage 28 dimensions | 2 PDF |
| `scenarios/` | Applications : noosphère, moteurs de recherche, agriculture, urbanisme | PDF + Markdown |
| `src/` | Implémentation de référence du Micro-Quorum Poreux Transcalaire | 1 script Python |
| `tests/` | Vérification expérimentale du noyau tétravalent | Notebook + rapport |
| `mpvr-glocal/` | Framework MPVR : synthèse formelle + implémentation | 1 README + `src/` |
| `soph-ia/` | SOPH-IA v2.0 : teaser, benchmark, métadonnées Zenodo | 7 fichiers |
| `deploy/` | Instructions de déploiement | 1 Markdown + `mttv/` |
| `docs/` | Documentation d'accompagnement et notes techniques | Markdown |

## 3. Le modèle en une page

**MTTV** — Modèle Théorique Transductif du Vivant (le noyau conceptuel).
**FLP** — Les Fils de la Pensée (le collectif et la plateforme).

La triade transductive : **Ψ → B → Φ**

| Symbole | Signification |
|---|---|
| **Ψ** | Champ pré-formel : tensions non orientées, réservoir différentiel |
| **B** | Opérateur de différence : seuil, résistance, mémoire prospective |
| **Φ** | Forme stabilisée : dépôt temporaire de contraintes, causalité descendante |

> « Seule Φ agit, et seul B transforme. »

**Roche-mère : carbone sp³.** La tétravalence du carbone est l'ancrage physico-chimique de la logique T⁴ dans la matière — avant toute cognition, le carbone compte déjà jusqu'à quatre.

**Logique tétravalente T⁴ = [++, --, +-, -+]**, traduite en opérateur neural utilisable par la fonction d'activation σ₄ — voir [`t4_activation_function.md`](t4_activation_function.md) :

| État | Vecteur | Signification |
|---|---|---|
| `++` | [1, 0, 0, 0] | Affirmation positive — ce qui est |
| `--` | [0, 1, 0, 0] | Négation — ce qui n'est pas |
| `+-` | [0, 0, 1, 0] | Simultanéité — la tension, le paradoxe |
| `-+` | [0, 0, 0, 1] | Indétermination — le retrait, la régulation |

## 4. Glossaire

| Terme | Définition |
|---|---|
| **Transcalaire** | Qui traverse les échelles (de l'atome au planétaire) selon une même règle métrique |
| **Transductif** | Qui fait passer l'information et l'énergie à travers des seuils, sans la dénaturer |
| **Sous-optimalité** | Principe de robustesse : accepter des approximations et des pannes locales pour garantir la résilience globale |
| **Quorum poreux** | Mécanisme de décision local où le seuil n'est pas un nombre mais une dérivée, et où la porosité (non-étanchéité des sous-ensembles) évite le verrouillage centralisé |
| **Basse continue** | Rôle assigné à l'IA : ne pas ordonner mais réguler passivement les flux, amortir entre les échelles |
| **RMP** | Mécanisme Pré-Transducteur — voir `protocols/3 MTTV-flp Mécanisme PréTransducteur RMP.pdf` |
| **Singularité Σ** | Apport ponctuel, asymétrique et non périodique — voir `protocols/3.1` à `3.4` |
| **MPVR** | *Multi-Perspective Validation & Resilience* (Multi-Path Vector Routing) — quorum poreux et routage multi-chemins d'inspiration mycélienne |
| **SOPH-IA** | *Sub-Optimal Paradigm for Habitable AI* — alignement comme propriété thermodynamique interne mesurable |
| **Quasi-esprit du langage** | Hypothèse selon laquelle le langage possède une épaisseur et une géométrie propres, produisant du sens en excès de ce qu'on y dépose |
| **IGIC** | Mentionné dans le README comme indice associé au noyau — *document source à préciser* |

## 5. Conventions du dépôt

- **Langue** : français principal ; les documents SOPH-IA sont en anglais
- **Licences** :
  - noyau (`core/`, `protocols/`, `benchmark/`, `scenarios/`, `src/`, `docs/`) : **CC-BY-NC-SA-4.0**
  - `mpvr-glocal/` : **CC0-1.0** (domaine public)
  - `soph-ia/` : **CC-BY-4.0**
- **Métadonnées** : certains dossiers portent un *front-matter* YAML (tags, licence, langue) — voir `mpvr-glocal/README.md`
- **Nommage héritage** : les fichiers de `core/` et `protocols/` sont numérotés (`0`, `1`, `2`, `4`, `5`, `6`, `9`…) selon l'ordre historique de production, pas selon un plan logique

## 6. Citation

```bibtex
@misc{mttv-flp-core-2026,
  title        = {MTTV-FLP Core — Modèle Théorique Transductif du Vivant},
  author       = {Collectif FLP},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20830060},
  url          = {https://github.com/gaillard111/mttv-flp-core}
}
```

Le module SOPH-IA dispose de sa propre référence : `10.5281/zenodo.21414425`.

## 7. Contribuer

```bash
git clone https://github.com/gaillard111/mttv-flp-core.git
cd mttv-flp-core
git checkout -b contribution/<sujet>
# ... vos modifications ...
git commit -m "docs: <description>"
git push origin contribution/<sujet>
```

Branches existantes : `main` (par défaut), `master`, `evolution/tetravalent-core`, `our-files`.

**Trois façons de contribuer :**

1. **Documenter** — manques identifiés ci-dessous, traductions, clarifications
2. **Vérifier** — reproduire `tests/test_sigma4.ipynb` et `mpvr-glocal/src/mttv_mpvr_quorum.py`, publier vos résultats, y compris s'ils contredisent
3. **Relier** — ouvrir une *Issue* pour connecter les concepts physiques (champ de Higgs, gravitation) aux dimensions sémantiques du modèle

**Charte d'usage** (voir le manifeste, §7) : citer les sources humaines, refuser le texte généré sans ancrage, utiliser l'IA comme miroir de second degré — jamais comme oracle.

## 8. Manques identifiés à ce jour

Documenter honnêtement ses propres trous fait partie de la méthode :

- **Pas de traduction anglaise** du noyau théorique — barrière pour la moitié des lecteurs potentiels
- **Pas de document d'entrée unique** : le parcours dépend du profil (voir §1)
- **IGIC** : mentionné au README, sans document source identifiable dans le dépôt
- **Pas de `CITATION.cff`** — fichier standard qui permettrait à GitHub d'exposer le DOI en un clic
- **Un fichier parasite `$null` (0 octet)** traînait à la racine — trace d'un script mal échappé, supprimé
- **Nommage historique** des fichiers de `core/` et `protocols/` : l'ordre numérique ne suit aucune logique lisible

## 9. Index

| Document | Sujet |
|---|---|
| [`README.md`](../README.md) | Point d'entrée, structure, licence, citation |
| [`SYNTHESE_MTTV_FLP.md`](../SYNTHESE_MTTV_FLP.md) | Synthèse du noyau, fonction σ₄ en annexe |
| [`core/mttv_flp_synthese_manifeste.md`](../core/mttv_flp_synthese_manifeste.md) | Synthèse scientifique et manifeste d'expansion |
| [`scenarios/note_moteurs_ethiques_et_souverains.md`](../scenarios/note_moteurs_ethiques_et_souverains.md) | Application à la recherche éthique et souveraine |
| [`docs/t4_activation_function.md`](t4_activation_function.md) | Fonction d'activation tétravalente σ₄ |
| [`docs/note_signature_ancrage.md`](note_signature_ancrage.md) | Ancre `sig:0x4D5454562D464C50` : nature, portée, ce qu'elle engage |
| [`mpvr-glocal/README.md`](../mpvr-glocal/README.md) | Synthèse formelle du framework MPVR |
| [`soph-ia/README.md`](../soph-ia/README.md) | SOPH-IA v2.0 : résultats et méthode |
| [`deploy/DEPLOY_HIDORA.md`](../deploy/DEPLOY_HIDORA.md) | Procédure de déploiement |
