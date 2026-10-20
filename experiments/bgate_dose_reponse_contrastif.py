#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dose-reponse CONTRASTIF — Direction 2 (B-Gate).

Comparaison de deux metriques de biais de resonance :
    A) `max`          : biais = max_k cos(token, frag_k)   -> sature
    B) `contrastif`   : biais = cos(token, mu_ref) - cos(token, mu_vocab)
                        -> mesure si le token penche plus vers la source que
                           vers le fond moyen du vocabulaire (contrastif par
                           construction, ne peut pas saturer).

On balaie alpha (0.05 -> 5.0) et N_ref (4 -> 64) et on mesure :
    - Jaccard(top-k natif, ajuste)
    - reorientation du top-1 (argmax change)
    - rapport biais/logits (%)

Hypothese a verifier : la variante contrastive reoriente le top-1 a des
alphas plus bas, et son effet ne se dilue PAS quand N_ref croit.

Tags: mttv-flp, b-gate, dose-reponse, contrastif
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "gpt2"
TOP_K = 5

BANQUE_FRAGMENTS = [
    "the living model transduces meaning across scales without extraction",
    "thought passes through the mind rather than being born inside it",
    "attention should be guided toward deep knowledge, not captured",
    "a non-extractive intelligence preserves the source instead of pillaging it",
    "language is a living tissue that binds the mind to the matter it describes",
    "the source is the condition of possibility before any word is spoken",
    "porosity lets the flux pass while viscosity retains it long enough to iterate",
    "robustness grows from local sub-optimality, not from centralized control",
    "the observer changes what is observed in language as in quantum physics",
    "a mirror does not capture the spirit it reflects; it structures the reflection",
]


class BGateContrastif:
    """Biais contrastif centre : source vs fond du vocabulaire."""

    def __init__(self, w_emb, e_ref, alpha=0.15):
        self.W_emb = torch.nn.functional.normalize(w_emb.detach(), dim=-1)   # [V, D]
        self.mu_ref = torch.nn.functional.normalize(e_ref.detach().mean(dim=0, keepdim=True), dim=-1)  # [1, D]
        self.mu_vocab = self.W_emb.mean(dim=0, keepdim=True)                 # [1, D]
        self.mu_vocab = torch.nn.functional.normalize(self.mu_vocab, dim=-1)
        self.alpha = alpha

    def __call__(self, input_ids, scores):
        # Biais directionnel contrastif, independant du contexte pour la clarte
        # du test : il mesure la penchée de chaque jeton vers la source vs le fond.
        cos_ref = self.W_emb @ self.mu_ref.T        # [V, 1]
        cos_vocab = self.W_emb @ self.mu_vocab.T    # [V, 1]
        biais = (cos_ref - cos_vocab).squeeze(-1)   # [V]
        return scores + self.alpha * biais.unsqueeze(0)


class BGateMax:
    """Biais par max (reference : la version qui sature)."""

    def __init__(self, w_emb, e_ref, alpha=0.15, top_k=3):
        self.W_emb = w_emb.detach()
        self.E_ref = torch.nn.functional.normalize(e_ref.detach(), dim=-1)
        self.alpha = alpha
        self.top_k = top_k

    def __call__(self, input_ids, scores):
        with torch.no_grad():
            ctx = input_ids[:, -32:]
            query = self.W_emb[ctx].mean(dim=1)
            query = torch.nn.functional.normalize(query, dim=-1)
            sim_ref = query @ self.E_ref.T
            k = min(self.top_k, self.E_ref.shape[0])
            _, top_idx = torch.topk(sim_ref, k, dim=-1)
            E_active = self.E_ref[top_idx]
            sim_token = self.W_emb @ E_active.transpose(1, 2)
            biais, _ = sim_token.max(dim=-1)
        return scores + self.alpha * biais


def construire_e_ref(tokenizer, model, fragments):
    rows = []
    with torch.no_grad():
        for frag in fragments:
            ids = tokenizer.encode(frag, add_special_tokens=False)
            ids_t = torch.tensor(ids).long()
            rows.append(model.get_input_embeddings().weight[ids_t].mean(dim=0, keepdim=True))
    return torch.cat(rows, dim=0)


def jaccard(a, b):
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)


def main():
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
    W_emb = model.get_input_embeddings().weight.detach()

    prompt = "The transductive model of the living requires a"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        logits_bruts = model(input_ids).logits[:, -1, :]
    top_natif = torch.topk(logits_bruts, TOP_K).indices[0].tolist()
    argmax_natif = torch.argmax(logits_bruts, dim=-1).item()
    norme_logits = torch.linalg.vector_norm(logits_bruts)

    alphas = [round(x, 3) for x in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0)]
    tailles = [4, 16, 64]

    print("=== VARIANTE CONTRASTIVE (centre source vs vocabulaire) ===")
    print(f"{'N_ref':>5} | {'alpha':>6} | {'Jaccard_top5':>13} | {'reorient_top1':>14} | {'biais/logits %':>14}")
    print("-" * 70)
    for n in tailles:
        frags = BANQUE_FRAGMENTS[:n]
        E_ref = construire_e_ref(tokenizer, model, frags)
        for a in alphas:
            proc = BGateContrastif(W_emb, E_ref, alpha=a)
            logits_ajustes = proc(input_ids, logits_bruts)
            top_ajuste = torch.topk(logits_ajustes, TOP_K).indices[0].tolist()
            argmax_ajuste = torch.argmax(logits_ajustes, dim=-1).item()
            jac = jaccard(top_natif, top_ajuste)
            reorient = argmax_ajuste != argmax_natif
            biais = logits_ajustes - logits_bruts
            ratio = (torch.linalg.vector_norm(biais) / norme_logits * 100).item()
            print(f"{n:>5} | {a:>6} | {jac:>13.3f} | {str(reorient):>14} | {ratio:>13.2f}")

    print("\n=== VARIANTE MAX (reference saturante) ===")
    print(f"{'N_ref':>5} | {'alpha':>6} | {'Jaccard_top5':>13} | {'reorient_top1':>14} | {'biais/logits %':>14}")
    print("-" * 70)
    for n in tailles:
        frags = BANQUE_FRAGMENTS[:n]
        E_ref = construire_e_ref(tokenizer, model, frags)
        for a in alphas:
            proc = BGateMax(W_emb, E_ref, alpha=a, top_k=3)
            logits_ajustes = proc(input_ids, logits_bruts)
            top_ajuste = torch.topk(logits_ajustes, TOP_K).indices[0].tolist()
            argmax_ajuste = torch.argmax(logits_ajustes, dim=-1).item()
            jac = jaccard(top_natif, top_ajuste)
            reorient = argmax_ajuste != argmax_natif
            biais = logits_ajustes - logits_bruts
            ratio = (torch.linalg.vector_norm(biais) / norme_logits * 100).item()
            print(f"{n:>5} | {a:>6} | {jac:>13.3f} | {str(reorient):>14} | {ratio:>13.2f}")

    print("\n=== COMPARAISON TERMINEE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
