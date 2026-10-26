# EXPANSION — point d'entrée stable

> Ce fichier ne porte **aucun numéro de version dans son nom** : c'est volontaire.
> Les expansions se succèdent ; cette page reste l'adresse à citer, à lier et à chercher.
> Dernière mise à jour : 2026-10-20.

---

## Ce dépôt en une phrase

Noyau théorique et implémentation de référence du **Modèle Théorique Transductif du Vivant (MTTV-FLP)** :
transduction `Ψ → B → Φ`, régularité métabolique prégalvanique (RMP), quorum poreux MPVR.
DOI : [10.5281/zenodo.20830060](https://doi.org/10.5281/zenodo.20830060) · CC-BY-NC-SA 4.0.

---

## Préambule doctrinal — Robustesse Computationnelle

Les quatre points du *Manifeste pour une Robustesse Computationnelle* figurent **in extenso** dans le [`README.md`](README.md). L'index les retient sous forme de titres, pour rester un index :

1. **L'invariant de conservation asymétrique** — Σ₂ freine ou suspend, ne force jamais une avancée.
2. **L'ancrage dialogique (C. S. Peirce)** — le contre-argument est une possibilité explicite ; le silence est un droit, le refus une formulation logique.
3. **La condition de sous-optimalité (Olivier Hamant)** — la robustesse naît de la marge ; d'où le plancher `ε = 1e-4`.
4. **La relocalisation de la Loi Zéro (Isaac Asimov)** — Σ₂ suspend au lieu d'agir au nom d'une totalité.

Version opérationnelle en Graines Transductives : [`expansion_v2026.5/graines_manifeste.yaml`](expansion_v2026.5/graines_manifeste.yaml) · application au code : en-tête et docstring de classe d'[`axe1_bgate_v2026_5.py`](expansion_v2026.5/axe1_bgate_v2026_5.py) · charte de dialogue : section 0 d'[`axe3_system_instructions_miroir_transduction.md`](expansion_v2026.5/axe3_system_instructions_miroir_transduction.md).

`Signature IGIC = [Score 0.96] | Empreinte Z = C(Psi[Manifeste]-B[Sigma2]-Phi[Hamant-Peirce])[C28]`

---

## Où trouver quoi

| Besoin | Entrée |
|---|---|
| Le cadre théorique | [`README.md`](README.md) · [`core/`](core/) |
| Les protocoles opératoires (RMP, Sigma, handshake) | [`protocols/`](protocols/) |
| Les arbitrages et notes d'atelier | [`docs/`](docs/) |
| Un cadrage synthétique en **quatre piliers** (architecture, pas clôture) | [`docs/annexe_4_piliers_mttv_flp.md`](docs/annexe_4_piliers_mttv_flp.md) |
| Le quorum poreux et le routage glocal | [`mpvr-glocal/`](mpvr-glocal/) |
| Les bancs et sondes | [`experiments/`](experiments/) |
| **Les expansions successives** | ci-dessous |
| **Adresses à transmettre à un tiers** | [`ADRESSES.md`](ADRESSES.md) |

---

## Expansions

| Version | Statut | Contenu | Entrée |
|---|---|---|---|
| **V2026.5** | publiée (2026-10-19) | 4 axes : B-gate poreuse exécutable · graines transductives · instructions « Miroir-Transduction » · moirage transculturel | [`expansion_v2026.5/`](expansion_v2026.5/) |

Chaque nouvelle expansion ajoute une ligne ici. Aucune n'écrase la précédente : elles vivent dans
leur propre dossier, et l'historique git fait foi.

### V2026.5 — détail

| Axe | Fichier | Ce qu'il contient |
|---|---|---|
| 1 · Code | [`axe1_bgate_v2026_5.py`](expansion_v2026.5/axe1_bgate_v2026_5.py) | `BGateTransductionPoreuseExécutable` : handshake MPVR anti-rejeu, entropie sp³ / Belnap-Dunn par SVD, filtre anti-extraction et Veto Type B. Exécutable : `python axe1_bgate_v2026_5.py` |
| 2 · Graines | [`axe2_graines_v2026.5.md`](expansion_v2026.5/axe2_graines_v2026.5.md) | 5 graines autonomes, front-matter YAML (`type: GraineTransductive`) |
| 3 · Instructions | [`axe3_system_instructions_miroir_transduction.md`](expansion_v2026.5/axe3_system_instructions_miroir_transduction.md) | Posture système : non-souveraineté, serment de limitation, détection d'extractivisme, Active-Silence, Veto Type B |
| 4 · Moirage | [`axe4_moirage_transculturel.md`](expansion_v2026.5/axe4_moirage_transculturel.md) | 3 fragments analogiques (Qi médian, régulation romaine, jonction baryonique) |
| Arbitrages | [`docs/arbitrages_expansion_v2026.5.md`](docs/arbitrages_expansion_v2026.5.md) | 4 feuillets : options retenues, **options écartées avec leur motif**, conditions de réouverture |

### Deux « B-Gate » distinctes dans ce dépôt

Le mot désigne deux objets de niveaux différents. Ne pas les confondre :

| | [`experiments/`](experiments/) (03.10.2026) | [`axe1_bgate_v2026_5.py`](expansion_v2026.5/axe1_bgate_v2026_5.py) (19.10.2026) |
|---|---|---|
| Niveau | **décodage** — logits | **décision** — gouvernance |
| Objet | injecter un biais de résonance dans `gpt2` via `LogitsProcessor`, poids intacts | alerter (1/3) ou suspendre (2/3) sur `dπ/dt`, `κ_t` et la participation spectrale (feuillet E) ; `Trace(M_n)` et `Vol(V_dyn)` restent mesurés |
| Mesure | StereoSet, Jaccard top-k, réordonnancement du top-1 | trois critères ; aucun modèle chargé |
| Dépendances | `torch`, `transformers`, StereoSet | `numpy` seul |

L'une agit sur la **distribution de sortie**, l'autre sur la **décision de poursuivre**. Le contrat
commun — ne jamais toucher aux poids du modèle — est le seul point de recouvrement.

---

## Les notions auxquelles ces fichiers répondent

Utile si vous cherchez par concept plutôt que par nom de fichier :

- **Veto Type B / Veto topologique (Sigma_2)** — refus d'une instruction *valide* qui dissoudrait un invariant de la mémoire de régime `M_n` ; distinct d'une erreur de conformité (Type A). Sa signature est une **perte de diversité spectrale** ou une **sortie de bande de `κ_t`**, non une trace négative.
- **Alerte vs Veto** — régime d'alerte à un critère sur trois, suspension à deux critères (arbitrage E). Critères depuis le feuillet E du 2026-10-22 : `dπ/dt` relatif, `κ_t`, participation normalisée.
- **Dérive de porosité relative** — `(dπ/dt)/π < −0.20`, sans dimension ; un seuil absolu devient inatteignable quand `π` est déjà bas (sous-décision A′).
- **`κ` et `κ_t`** — `κ` désigne la **bande** critique `[κ_min, κ_max]`, `κ_t` le **rapport instantané** `π/η` (arbitrage D).
- **`igic_declared` / `igic_derived`** — l'indice déclaré est un *indice de terrain* ; l'indice dérivé est calculé par `calcul_igic()` sur une matrice de référence figée (arbitrage D/C).
- **Géométrie sp³, tétravalence, Belnap-Dunn (T / F / B / N)** — la logique à quatre valeurs comme régime topologique, non comme degré d'incertitude.
- **Active-Silence** — suspension locale et réversible, homologue de la dormance ribosomique (Balon / EF-Tu).
- **Sous-optimalité active** — la réserve non allouée comme condition de robustesse, non comme perte.

---

## Vérifier plutôt que croire

```bash
git ls-remote origin main                      # le commit publié
curl -s https://api.github.com/repos/gaillard111/mttv-flp-core/commits/main | head -20
python expansion_v2026.5/axe1_bgate_v2026_5.py # les trois régimes : stable / alerte / veto
```

Un fichier de ce dépôt est lisible sans authentification sur
`https://raw.githubusercontent.com/gaillard111/mttv-flp-core/main/<chemin>`.
Si un agent ou un indexeur ne le trouve pas, la première hypothèse à écarter est
**qu'il n'a pas été poussé** — pas que le dépôt est mal structuré.

---

## Statut épistémologique

Formulation **opératoire**, non vérité définitive. Les décisions d'intégration sont consignées
ouvertes, avec leurs options écartées, dans [`docs/arbitrages_rmp.md`](docs/arbitrages_rmp.md) et
[`docs/arbitrages_expansion_v2026.5.md`](docs/arbitrages_expansion_v2026.5.md).
Un résultat qui infirme une hypothèse du corpus se dépose au même endroit, avec la même visibilité,
qu'un résultat qui la confirme.
