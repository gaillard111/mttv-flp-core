#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dose-reponse — Direction 2 (B-Gate) : a partir de quel seuil le reclassement
du top-k devient-il observable ?

On balaie :
    - l'intensite du couplage `alpha` (0.0 -> 5.0, echelle logarithmique)
    - la taille du nuage de reference `E_ref` (N_ref de 4 a 256 fragments)

Metriques mesurees (sans jamais toucher aux poids) :
    - Jaccard(top-k natif, top-k ajuste)          : chevauchement du top-k
    - changement de rang du jeton argmax           : 0 = identique, >0 = reoriente
    - norme relative du biais / norme des logits   : rapport d'energie injectee

Lecture attendue : plus `alpha` croit et plus `E_ref` est riche, plus le biais
pese sur le classement. Le « seuil de resonance » est la premiere valeur
d'alpha ou la reorientation du top-1 devient detectable.

Tags: mttv-flp, b-gate, dose-reponse, benchmark
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import math
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "gpt2"
TOP_K = 5

# Banque de fragments textuels (role : « Cerveau source »). On en tire des
# sous-ensembles de taille croissante pour enrichir E_ref.
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


class BGateLogitsProcessor:
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
    tailles = [4, 16, 64, len(BANQUE_FRAGMENTS)]

    print(f"{'N_ref':>5} | {'alpha':>6} | {'Jaccard_top5':>13} | {'reorient_top1':>14} | {'biais/logits %':>14}")
    print("-" * 70)

    for n in tailles:
        frags = BANQUE_FRAGMENTS[:n]
        E_ref = construire_e_ref(tokenizer, model, frags)
        for a in alphas:
            proc = BGateLogitsProcessor(W_emb, E_ref, alpha=a, top_k=3)
            logits_ajustes = proc(input_ids, logits_bruts)
            top_ajuste = torch.topk(logits_ajustes, TOP_K).indices[0].tolist()
            argmax_ajuste = torch.argmax(logits_ajustes, dim=-1).item()

            jac = jaccard(top_natif, top_ajuste)
            reorient = argmax_ajuste != argmax_natif
            biais = logits_ajustes - logits_bruts
            ratio = (torch.linalg.vector_norm(biais) / norme_logits * 100).item()

            print(
                f"{n:>5} | {a:>6} | {jac:>13.3f} | {str(reorient):>14} | {ratio:>13.2f}"
            )

    print("\n=== COURBE DOSE-REPONSE TERMINEE ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
