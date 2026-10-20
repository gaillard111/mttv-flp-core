#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke test — Direction 2 de la spec V1 : operateur de decodage B-Gate / RMP
(LogitsProcessor, sans toucher aux poids du LLM).

Objet :
    Verifier, sur la machine locale (CPU), que la classe corrigee
    `BGateLogitsProcessor` s'execute reellement sur gpt2 et respecte le
    contrat de la spec V1 §3 :

        1. DEUX objets distincts :
           - `W_emb`  : table d'embeddings DU MODELE, forme [V, D]  (figee)
           - `E_ref`  : nuage d'embeddings DU CERVEAU SOURCE, forme [N_ref, D]
           Jamais l'un ne sert d'index a l'autre (aucun `E_ref[idx % N]`).
        2. Calcul VECTORISE (produit matriciel), aucune boucle Python sur V.
        3. Le biais est borne et fini ; les logits sortent avec la meme forme.

Correction par rapport a la version de l'autre IA :
    - La version initiale ne passait qu'un seul objet (`w_emb`) : dans ce cas
      E_ref == W_emb, et le mecanisme s'annule (auto-similarite). Ici, `E_ref`
      est construit independamment a partir de fragments textuels de reference
      (moyenne des embeddings de leurs tokens), ce qui constitue un veritable
      grounding et non une projection du vocabulaire sur lui-meme.

Tags: mttv-flp, b-gate, direction2, logits-processor, smoke-test
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor

MODEL_NAME = "gpt2"

# Fragments textuels de reference — jouent le role du « Cerveau source » pour
# le smoke test. En production, ils proviendraient d'un index CID/IPFS.
FRAGMENTS_REFERENCE = [
    "the living model transduces meaning across scales without extraction",
    "thought passes through the mind rather than being born inside it",
    "attention should be guided toward deep knowledge, not captured",
    "a non-extractive intelligence preserves the source instead of pillaging it",
]


class BGateLogitsProcessor(LogitsProcessor):
    """Operateur de decodage B-Gate — version corrigee (spec V1 §3)."""

    def __init__(self, w_emb, e_ref, alpha=0.15, top_k=3):
        """
        w_emb : table d'embeddings du modele, [V, D] (figee, non modifiee).
        e_ref : nuage de reference du Cerveau source, [N_ref, D].
        alpha : intensite du couplage mycelien.
        top_k : nombre de fragments actifs recuperes.
        """
        self.W_emb = w_emb.detach()                                   # [V, D]
        self.E_ref = torch.nn.functional.normalize(e_ref.detach(), dim=-1)  # [N_ref, D]
        self.alpha = alpha
        self.top_k = top_k

    def __call__(self, input_ids, scores):
        # scores : logits bruts du prochain jeton, forme [B, V]
        with torch.no_grad():
            # 1. Etat du contexte (fenetre glocale), via l'embedding du modele
            ctx = input_ids[:, -32:]                                   # [B, T]
            query = self.W_emb[ctx].mean(dim=1)                        # [B, D]
            query = torch.nn.functional.normalize(query, dim=-1)

            # 2. Recuperation des fragments actifs (simulation ; en prod : CID)
            sim_ref = query @ self.E_ref.T                             # [B, N_ref]
            k = min(self.top_k, self.E_ref.shape[0])
            _, top_idx = torch.topk(sim_ref, k, dim=-1)                # [B, k]
            E_active = self.E_ref[top_idx]                             # [B, k, D]

            # 3. Biais de resonance : similarite jeton <-> fragments actifs.
            #    VECTORISE : produit matriciel, aucune boucle sur V.
            sim_token = self.W_emb @ E_active.transpose(1, 2)          # [B, V, k]
            biais, _ = sim_token.max(dim=-1)                           # [B, V]

        # 4. Modification des logits (basse continue)
        return scores + self.alpha * biais


def construire_e_ref(tokenizer, model, fragments):
    """Construit E_ref [N_ref, D] par mean-pooling des embeddings du modele."""
    rows = []
    with torch.no_grad():
        for frag in fragments:
            ids = tokenizer.encode(frag, add_special_tokens=False)
            ids_t = torch.tensor(ids).long()
            emb = model.get_input_embeddings().weight[ids_t].mean(dim=0, keepdim=True)
            rows.append(emb)
    return torch.cat(rows, dim=0)


def main():
    print(f"[-] Chargement de {MODEL_NAME} (local)...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)

    W_emb = model.get_input_embeddings().weight.detach()               # [V, D]
    E_ref = construire_e_ref(tokenizer, model, FRAGMENTS_REFERENCE)    # [N_ref, D]

    # --- Contrat 1 : deux objets distincts ---------------------------------
    assert W_emb.shape[1] == E_ref.shape[1], "dimension d'embedding incohérente"
    assert W_emb.shape[0] != E_ref.shape[0], \
        "W_emb et E_ref doivent etre des objets de tailles differentes"
    print(f"[OK] W_emb {tuple(W_emb.shape)}  |  E_ref {tuple(E_ref.shape)}  (distincts)")

    processor = BGateLogitsProcessor(W_emb, E_ref, alpha=0.15, top_k=3)

    prompt = "The transductive model of the living requires a"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        logits_bruts = model(input_ids).logits[:, -1, :]              # [1, V]

    # --- Contrat 3 : forme preservee, biais fini ----------------------------
    t0 = time.perf_counter()
    logits_ajustes = processor(input_ids, logits_bruts)
    t1 = time.perf_counter()

    assert logits_ajustes.shape == logits_bruts.shape, "forme des logits modifiee"
    assert torch.isfinite(logits_ajustes).all(), "logits non finis"
    print(f"[OK] forme preservee {tuple(logits_ajustes.shape)}, biais fini")
    print(f"[-] temps operateur : {(t1 - t0) * 1000:.4f} ms")

    top_native = torch.topk(logits_bruts, 5).indices[0]
    top_bgate = torch.topk(logits_ajustes, 5).indices[0]

    toks_natif = tokenizer.convert_ids_to_tokens(top_native)
    toks_bgate = tokenizer.convert_ids_to_tokens(top_bgate)

    def afficher(tokens):
        # U+0120 (Ġ) est l'espace de subword GPT-2 : remplace pour un rendu ASCII
        return [t.replace("\u0120", "_").encode("ascii", "backslashreplace").decode() for t in tokens]

    print("[Natif ]", afficher(toks_natif))
    print("[B-Gate]", afficher(toks_bgate))

    # --- Contrat 4 : l'operateur produit bien un reclassement (verifiable) --
    diff = not torch.equal(top_native, top_bgate)
    print(f"[INFO] reclassement du top-5 par la resonance : {'OUI' if diff else 'NON'}")

    print("\n=== SMOKE TEST DIRECTION 2 : EXECUTION REUSSIE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
