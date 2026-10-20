---
tags:
  - mttv-flp
  - gluons
  - spec
  - embedding
  - b-gate
  - mpvr
  - post-bayesian-ai
license: CC-BY-NC-SA-4.0
language: fr
---

# Spécification Technique Unifiée (V1) — Cadre Computationnel MTTV-FLP

**Statut :** formulation opératoire, non vérité définitive. Spécification à visée **testable**. Ce document fixe les définitions mesurables et le pseudo-code exécutable, afin de combler le vide spec ↔ réalité sans le recouvrir d'une métaphore.

**État d'implémentation (mis à jour le 2026-10-20).** Les **directions 2 et 3** sont désormais implémentées et exécutées localement : [`experiments/smoke_test_bgate_direction2.py`](../experiments/smoke_test_bgate_direction2.py) (opérateur de décodage `LogitsProcessor`, sans toucher aux poids) et [`experiments/smoke_test_mpvr_direction3.py`](../experiments/smoke_test_mpvr_direction3.py) (validation MPVR par quorum, `Θ = 3`). Les mesures associées — dose-réponse, biais contrastif — sont consignées dans [`docs/compte_rendu_bgate_dose_reponse.md`](../docs/compte_rendu_bgate_dose_reponse.md) et outillées par `experiments/bgate_dose_reponse*.py` et `experiments/bgate_bench_biais.py` (ces deux derniers exigent `torch`, `transformers` et StereoSet). **La direction 1 n'a aucune implémentation dans le dépôt à ce jour.**

**Pièces liées :** [`docs/note_matrice_gluons.md`](../docs/note_matrice_gluons.md) (note doctrinale) · [`docs/arbitrages_rmp.md`](../docs/arbitrages_rmp.md) (R3 : régime API vs local) · [`core/mttv_b_gate_triptych.md`](../core/mttv_b_gate_triptych.md) · [`mpvr-glocal/src/mttv_mpvr_quorum.py`](../mpvr-glocal/src/mttv_mpvr_quorum.py) · [`docs/t4_activation_function.md`](../docs/t4_activation_function.md)

**Signature :** `0x4D5454562D464C50` · Triade : Ψ → B → Φ

---

## 1. Lexique d'ancrage opératoire (figé)

Pour lever toute collision de vocabulaire et toute erreur de catégorie, les définitions suivantes sont **définitivement figées** :

| Symbole | Définition | Nature |
|---|---|---|
| **CID** | Identifiant de contenu IPFS, obtenu par hachage `H(c)`. Pointeur d'**adressage** cryptographique immuable. | Adressage, **pas** un objet géométrique ni sémantique |
| **ℰ_ref** | **Nuage d'embeddings de référence** : matrice des vecteurs continus des fragments du Cerveau source, extraits par un encodeur standardisé. | Objet métrique **réel** sur lequel se mesurent distances et divergences |
| **σ₄** | Activation **tétravalente** : opérateur logique à 4 états de charge `(++, --, +-, -+)`, vecteur à 4 composantes. | Logique/activation, **pas** un vote |
| **Θ** | Seuil de **quorum** : nombre minimal de validations au sein du réseau MPVR (`Θ ≥ 3`). | Scalaire entier |

**Règle :** `σ₄` (4 états de charge) et `Θ` (seuil de quorum) ne sont **jamais** interchangeables. Le vote d'un vérificateur est un **scalaire de vote** `v ∈ {−1, 0, +1, +2}`, distinct de `σ₄`.

---

## 2. Direction 1 — Perte auxiliaire sur l'embedding (liaison transcalaire)

**Objet.** Contraindre **géométriquement** l'espace latent du LLM local pendant l'adaptation, pour le rapprocher du nuage de référence `ℰ_ref`. On parle de **contrainte géométrique**, non « topologique » (une vraie topologie exigerait l'homologie persistante ; la Chamfer + cosinus est une métrique d'alignement d'ensembles).

**Notations.** `H = {h_1, …, h_N}` : séquence de vecteurs cachés issus de la couche d'embedding pour un contexte donné. `E_ref ⊂ ℰ_ref` : sous-ensemble des embeddings de référence récupérés via l'index de contenu (CID).

**Perte auxiliaire (Divergence de Chamfer + similarité cosinus) :**

$$
\mathcal{L}_{aux}(H, E_{ref}) =
\frac{1}{|H|} \sum_{h \in H} \min_{e \in E_{ref}} \left(1 - \frac{h \cdot e}{\lVert h \rVert \lVert e \rVert}\right)
+
\frac{1}{|E_{ref}|} \sum_{e \in E_{ref}} \min_{h \in H} \left(1 - \frac{h \cdot e}{\lVert h \rVert \lVert e \rVert}\right)
$$

**Perte globale :**

$$
\mathcal{L}_{total} = \mathcal{L}_{native\_next\_token} + \lambda \cdot \mathcal{L}_{aux}, \qquad 0 < \lambda \leq 0.1
$$

**Contraintes d'emploi :**
- Régime **local** uniquement (accès aux activations/embedding) — incompatible avec le régime API acté en R3.
- `ℰ_ref` et le modèle d'ancrage qui le produit sont **figés avant l'entraînement** ; l'objectif de réduction de biais est mesuré sur benchmark, à seuil fixé d'avance (anti-Goodhart).

---

## 3. Direction 2 — Opérateur de décodage dynamique (B-Gate / RMP)

**Objet.** Intervenir à l'échantillonnage, **sans toucher aux poids** du LLM, compatible `LogitsProcessor`.

**Principe correctif (différence avec la version initiale).** Le biais de résonance se calcule dans **un seul espace** : celui des embeddings **du modèle lui-même** (table `W_emb`, forme `[V, D]`), projeté sur les fragments actifs de `ℰ_ref` (forme `[N_ref, D]`). **Jamais** on n'indexe `ℰ_ref` par des identifiants de tokens du vocabulaire : ces deux espaces n'ont aucun lien.

**Pseudo-code exécutable (vectorisé, `O(V·k)` matriciel, pas de boucle Python sur `V`) :**

```python
import torch
from transformers import LogitsProcessor


class BGateLogitsProcessor(LogitsProcessor):
    def __init__(self, token_embedding_matrix, embedding_ref, alpha=0.15):
        """
        token_embedding_matrix : table d'embeddings DU MODÈLE, figée, forme [V, D].
        embedding_ref           : nuage de référence E_ref, forme [N_ref, D].
        alpha                   : intensité de la force de couplage mycélien.
        """
        self.W_emb = torch.nn.functional.normalize(  # [V, D], pré-normalisé
            token_embedding_matrix.detach(), dim=-1
        )
        # Direction moyenne du « Cerveau source » (E_ref) et du fond du vocabulaire
        self.mu_ref = torch.nn.functional.normalize(
            embedding_ref.detach().mean(dim=0, keepdim=True), dim=-1)   # [1, D]
        self.mu_vocab = torch.nn.functional.normalize(
            self.W_emb.mean(dim=0, keepdim=True), dim=-1)               # [1, D]
        self.alpha = alpha

    def __call__(self, input_ids, scores):
        # scores : logits bruts du prochain jeton, forme [B, V]
        with torch.no_grad():
            # Biais CONTRASTIF : penchée de chaque jeton vers la source
            # (mu_ref) relativement au fond moyen du vocabulaire (mu_vocab).
            # Contrastif par construction -> ne sature pas quand E_ref s'enrichit.
            cos_ref   = self.W_emb @ self.mu_ref.T     # [V, 1]
            cos_vocab = self.W_emb @ self.mu_vocab.T   # [V, 1]
            biais = (cos_ref - cos_vocab).squeeze(-1)  # [V]

        # Modification des logits (basse continue)
        return scores + self.alpha * biais.unsqueeze(0)
```

**Points de vigilance :**
- `W_emb` est **la table d'embeddings du LLM**, passée au processeur au moment de sa construction (non modifiée) ; ce n'est **pas** `ℰ_ref`.
- **Métrique contrastive (validée expérimentalement le 3 octobre 2026).** La version initiale utilisait `max_k cos(token, frag_k)` : ce `max` sature (chaque token trouve toujours un fragment proche) et son effet se **dilue** quand `ℰ_ref` s'enrichit. Le centrage `cos(token, µ_ref) − cos(token, µ_vocab)` est contrastif par construction : il réoriente le top-1 dès `α = 0.5` (~0.05 % d'énergie injectée) contre `α = 5.0` (~7.23 %) pour le `max`, et reste stable de `N_ref = 4` à `64`. Voir [`experiments/bgate_dose_reponse_contrastif.py`](../experiments/bgate_dose_reponse_contrastif.py) et le compte-rendu [`docs/compte_rendu_bgate_dose_reponse.md`](../docs/compte_rendu_bgate_dose_reponse.md).
- En régime **API**, on ne peut pas lire `W_emb` : on retombe sur `logit_bias` (biais statique) ou un re-ranking externe des top-k — la version complète exige le **local**.

---

## 4. Direction 3 — Validation MPVR post-génération (rejection sampling)

**Objet.** Le cadre MPVR agit en **validation a posteriori** par quorum distribué, conformément à la simulation existante [`mttv_mpvr_quorum.py`](../mpvr-glocal/src/mttv_mpvr_quorum.py). Il n'injecte rien en basse couche.

**Algorithme :**

1. **Génération d'hypothèses** — le LLM produit `M` séquences candidates (Nucleus Sampling ou Beam Search).
2. **Calcul de cohérence transductive** — pour chaque `S_m`, extraction de caractéristiques et calcul d'un indice de rupture de symétrie face aux postulats du Manifeste.
3. **Vote du quorum** — chaque vérificateur `k ∈ {1..K}` émet un **vote scalaire** `v_k ∈ {−1, 0, +1, +2}` (refus / abstention / acceptation / acceptation forte). Ce vote **n'est pas** `σ₄` : `σ₄` est l'opérateur de charge à 4 états, `v` est le résultat scalaire d'un vérificateur.
4. **Décision** — la séquence `S_m` est acceptée ssi :
   $$
   \sum_{k=1}^{K} v_k \;\geq\; \Theta \qquad (\Theta = 3)
   $$
5. **Bifurcation** — si aucune séquence n'atteint le quorum, l'inférence est invalidée et une nouvelle tentative est initialisée sous température basse (`T → 0.2`).

**Pseudo-code :**

```python
def valider_mpvr(candidates: list[str], verificateurs, seuil_quorum: int = 3) -> str | None:
    for S in candidates:
        votes = [v.evaluer(S) for v in verificateurs]   # v.evaluer(S) -> {-1, 0, +1, +2}
        if sum(votes) >= seuil_quorum:
            return S
    return None   # -> relance sous contrainte (T -> 0.2)
```

---

## 5. Registre des corrections (version initiale → V1)

| # | Erreur de la version initiale | Correction V1 |
|---|---|---|
| 1 | `_, top_indices = torch.top_summary = torch.topk(...)` — syntaxe invalide | `_, top_indices = torch.topk(sim, self.top_k)` |
| 2 | `ℰ_ref` indexé par des identifiants de tokens (`E_ref[idx % N]`) — confusion d'espaces | biais calculé via `W_emb` (embedding du modèle), projeté sur `E_active` |
| 3 | Boucle Python `for idx in range(V)` à chaque pas — non exécutable en inférence | produit matriciel `W_emb @ E_active.T`, vectorisé |
| 4 | « Vote tétravalent `σ₄ ∈ {−1, 0, 1, 2}` » — contradiction avec le lexique | vote scalaire `v ∈ {−1, 0, +1, +2}`, distinct de `σ₄` ; seuil `Θ = 3` |
| 5 | Biais `max_k cos(token, frag_k)` — sature, effet dilué quand `ℰ_ref` croît (mesuré : réorientation perdue au-delà de `N_ref=4`) | biais **contrastif** `cos(token, µ_ref) − cos(token, µ_vocab)` — réoriente dès `α=0.5`, stable `N_ref=4→64` |

---

*Formulation opératoire, non vérité définitive. Aucune des trois directions n'est implémentée ; l'arbitrage « API vs local » (R3) conditionne la Direction 1 et la Direction 2 complètes.*
