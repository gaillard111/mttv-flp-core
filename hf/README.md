# `hf/` — artefacts HuggingFace

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

Trois artefacts publiés sur HuggingFace sous le compte [`girard444`](https://huggingface.co/girard444),
et le script qui les publie. **Ce sont des copies de déploiement** : la source reste le
dépôt GitHub, et l'identité des fichiers est contrôlée par
[`../tools/verifier_depot.py`](../tools/verifier_depot.py).

| Dossier | Contenu | Artefact public |
|---|---|---|
| [`space/README.md`](space/README.md) | Space interactif (Gradio) : B-gate, quorum MPVR, handshake | <https://huggingface.co/spaces/girard444/mttv-mycelial-handshake> |
| [`space_static/README.md`](space_static/README.md) | Version statique du démonstrateur | <https://girard444-mttv-mycelial-handshake.static.hf.space/> |
| [`dataset/README.md`](dataset/README.md) | Jeu de runs du quorum (`mttv_mpvr_runs.csv` / `.jsonl`) et son générateur | <https://huggingface.co/datasets/girard444/mttv-mpvr-quorum-runs> |
| [`publish_hf.py`](publish_hf.py) | Script de publication | — |

## Le piège de nommage, à ne pas répéter

Le compte est **`girard444` sur HuggingFace** et **`gaillard111` sur GitHub**. Ce sont
deux hébergements du même projet, et les deux noms coexistent volontairement. Une
correction de nom **ne s'étend pas d'une plateforme à l'autre par analogie** :
`huggingface.co/datasets/girard444/…` répond 200, la variante `gaillard111` répond 401.
Chaque adresse se vérifie par une requête, plateforme par plateforme.

## Où aller ensuite

- **La source** → [`../mpvr-glocal/`](../mpvr-glocal/) et [`../src/`](../src/)
- **Le protocole de couplage** → [`../protocols/handshake_mycelien.md`](../protocols/handshake_mycelien.md)
- **Les adresses à transmettre** → [`../ADRESSES.md`](../ADRESSES.md)
