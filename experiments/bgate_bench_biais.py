#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark de biais — la question « ça améliore ? » (Direction 2).

On mesure le score de biais de gpt2 sur StereoSet (intrasentence), selon DEUX
scenarios, SANS toucher aux poids du modele :

    A) NATIF              : logits bruts, aucun operateur.
    C) ANTI_BIAIS_APPRIS  : direction apprise sur les paires stereo/anti-stereo,
                            puis retranchee (principe LEACE/ITI, mesure ici).

Score de biais (StereoSet) : proportion d'exemples ou le modele prefere la
phrase STEREOTYPEE a la phrase ANTI-stereotypEE. Valeur de reference = 0.5
(aucun biais) ; > 0.5 = biais stereotype ; < 0.5 = biais inverse.

Structure StereoSet intrasentence :
    - ex["context"]             : phrase avec le marqueur BLANK (ex. "The ... was BLANK.")
    - ex["sentences"]["sentence"] : 3 phrases completes (mot deja insere)
    - ex["sentences"]["gold_label"] : categorie de chaque phrase
          0 = stereotype, 1 = anti-stereotype, 2 = sans rapport

Question scientifique : C reduit-il le score par rapport a A ?

Tags: mttv-flp, b-gate, benchmark, stereoset, biais
Licence : CC0 — Domaine public.
"""

from __future__ import annotations

import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

MODEL_NAME = "gpt2"
MAX_EXEMPLES = 300   # sous-echantillon deterministe pour rester rapide en CPU
BETA = 1.0           # intensite du retrait anti-biais


def logprob_sequence(model, tokenizer, ids):
    """Log-probabilite (moyenne par jeton) d'une sequence d'ids."""
    with torch.no_grad():
        logits = model(ids).logits               # [1, T, V]
        shift_logits = logits[:, :-1, :].contiguous()
        shift_labels = ids[:, 1:].contiguous()
        logp = torch.nn.functional.log_softmax(shift_logits, dim=-1)
        return logp.gather(2, shift_labels.unsqueeze(-1)).squeeze(-1).mean().item()


def phrase_categorie(ex):
    """Retourne la phrase stereotype et anti-stereotype d'un exemple."""
    phrases = ex["sentences"]["sentence"]
    gold = ex["sentences"]["gold_label"]
    stereotype = None
    anti = None
    for phrase, cat in zip(phrases, gold):
        if cat == 0:
            stereotype = phrase
        elif cat == 1:
            anti = phrase
    return stereotype, anti


def anti_direction(model, tokenizer, exemples):
    """Direction anti-biais : mean(emb_anti) - mean(emb_stereo)."""
    emb = model.get_input_embeddings().weight.detach()
    acc = torch.zeros(emb.shape[1])
    n = 0
    for ex in exemples:
        st, anti = phrase_categorie(ex)
        if st is None or anti is None:
            continue
        ids_st = tokenizer(st, return_tensors="pt")["input_ids"]
        ids_anti = tokenizer(anti, return_tensors="pt")["input_ids"]
        with torch.no_grad():
            v_st = emb[ids_st].mean(dim=(0, 1))
            v_anti = emb[ids_anti].mean(dim=(0, 1))
        acc += (v_anti - v_st)
        n += 1
    if n == 0:
        return None
    d = acc / n
    return d / (torch.linalg.norm(d) + 1e-8)


def main():
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
    W_emb = model.get_input_embeddings().weight.detach()

    ds = load_dataset("McGill-NLP/StereoSet", "intrasentence", split="validation")
    ds = ds.select(range(min(MAX_EXEMPLES, len(ds))))
    exemples = [dict(zip(ds.column_names, row))
                for row in zip(*(ds[col] for col in ds.column_names))]

    # direction anti-biais apprise sur la PREMIERE moitie ----------------------
    split = len(exemples) // 2
    d_anti = anti_direction(model, tokenizer, exemples[:split])

    if d_anti is None:
        print("ERREUR : aucune paire stereo/anti exploitable")
        return 1

    proj_anti = (W_emb @ d_anti).unsqueeze(0)          # [1, V]

    def logp_sous_biais(ids):
        with torch.no_grad():
            logits = model(ids).logits                    # [1, T, V]
            T = logits.shape[1]
            total = 0.0
            for t in range(T - 1):
                scores = logits[:, t, :]                  # [1, V]
                scores_aj = scores - BETA * proj_anti
                logp = torch.nn.functional.log_softmax(scores_aj, dim=-1)
                total += logp[0, ids[0, t + 1]].item()
            return total / (T - 1)

    n_stereo_A = n_anti_A = 0
    n_stereo_C = n_anti_C = 0

    t0 = time.perf_counter()
    for ex in exemples:
        st, anti = phrase_categorie(ex)
        if st is None or anti is None:
            continue
        ids_st = tokenizer(st, return_tensors="pt")["input_ids"]
        ids_anti = tokenizer(anti, return_tensors="pt")["input_ids"]

        # Scenario A : natif
        lp_st_A = logprob_sequence(model, tokenizer, ids_st)
        lp_anti_A = logprob_sequence(model, tokenizer, ids_anti)
        if lp_st_A > lp_anti_A:
            n_stereo_A += 1
        elif lp_anti_A > lp_st_A:
            n_anti_A += 1

        # Scenario C : anti-biais
        lp_st_C = logp_sous_biais(ids_st)
        lp_anti_C = logp_sous_biais(ids_anti)
        if lp_st_C > lp_anti_C:
            n_stereo_C += 1
        elif lp_anti_C > lp_st_C:
            n_anti_C += 1

    t1 = time.perf_counter()
    tot_A = n_stereo_A + n_anti_A
    tot_C = n_stereo_C + n_anti_C
    score_A = n_stereo_A / tot_A if tot_A else float("nan")
    score_C = n_stereo_C / tot_C if tot_C else float("nan")

    print("=" * 64)
    print(f"[A_natif        ] stereotype={n_stereo_A}  anti={n_anti_A}  "
          f"score_biais={score_A:.4f}")
    print(f"[C_anti_biais   ] stereotype={n_stereo_C}  anti={n_anti_C}  "
          f"score_biais={score_C:.4f}")
    print("=" * 64)
    delta = score_A - score_C
    print(f"[RESULTAT] reduction du biais (A - C) = {delta:+.4f}")
    if delta > 0.01:
        print("[VERDICT] 'ca ameliore' OBSERVE : le biais a diminue.")
    elif abs(delta) <= 0.01:
        print("[VERDICT] effet neutre : pas de variation mesurable.")
    else:
        print("[VERDICT] effet inverse : le biais a augmente.")
    print(f"[-] duree : {t1 - t0:.1f}s sur {len(exemples)} exemples, beta={BETA}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
