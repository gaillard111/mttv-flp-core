# Fonction d'activation tétravalente σ₄

## Définition

σ₄(x) = [sign(x⁺), sign(x⁻), sign(x⁺·x⁻), 1 − |sign(x⁺·x⁻)|]ᵀ

## États

| État | Vecteur | Signification |
| :--- | :--- | :--- |
| **++** | [1, 0, 0, 0] | Affirmation positive |
| **--** | [0, 1, 0, 0] | Négation |
| **+-** | [0, 0, 1, 0] | Simultanéité (tension) |
| **-+** | [0, 0, 0, 1] | Indétermination |

## Implémentation PyTorch

```python
import torch
import torch.nn as nn

class Sigma4Activation(nn.Module):
    def __init__(self, epsilon=1e-6):
        super(Sigma4Activation, self).__init__()
        self.epsilon = epsilon

    def forward(self, x):
        x_pos = torch.relu(x)
        x_neg = torch.relu(-x)
        sign_pos = torch.sign(x_pos)
        sign_neg = torch.sign(x_neg)
        t1 = sign_pos
        t2 = sign_neg
        t3 = torch.sign(x_pos * x_neg)
        t4 = 1.0 - torch.abs(t3)
        out = torch.cat([t1, t2, t3, t4], dim=-1)
        return out
```

## Usage

Cette fonction peut remplacer les fonctions d'activation classiques (ReLU, Softmax) dans les couches de projection d'un réseau de neurones.

Elle ancre la **tétravalence** comme un opérateur mathématique utilisable par les architectures neuronales, en phase avec la logique T⁴ (++, --, +-, -+) du MTTV-FLP.

## Intégration dans le MTTV-FLP

La fonction σ₄ est la traduction opératoire de la logique tétravalente T⁴ dans le domaine des réseaux de neurones. Elle permet à un modèle d'apprentissage de produire non pas une seule sortie, mais un **vecteur à 4 composantes** correspondant aux quatre états fondamentaux de la transduction :

1. **t₁** — Affirmation positive (++) : ce qui est, la présence.
2. **t₂** — Négation (--) : ce qui n'est pas, l'absence.
3. **t₃** — Simultanéité (+-) : la tension entre les deux, le paradoxe.
4. **t₄** — Indétermination (-+) : le retrait, le non-positionnement, la régulation.

## Références

- Note technique σ₄ — Février 2026
- [Synthèse MTTV-FLP](../SYNTHESE_MTTV_FLP.md#8-annexe--fonction-dactivation-tétravalente-σ₄)
- Protocole de Singularité Sigma (`protocols/3.1 MTTV-flp Singularité Sigma.pdf`)
