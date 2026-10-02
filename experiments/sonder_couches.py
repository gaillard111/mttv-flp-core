#!/usr/bin/env python3
"""
Sonde des couches internes — examen PASSIF.

Question : que peut-on voir, sans rien modifier et sans rien appeler, dans les
couches d'un modèle exécuté en local ?

Quatre grandeurs sont mesurées, chacune candidate à incarner une variable de la
RMP — **proposition, non doctrine**. Aucune n'est adoptée ; elles sont nommées
pour être discutées :

    entropie d'attention          -> dispersion de l'attention
    CKA entre couches voisines    -> rétention vs réécriture  (candidat : eta)
    rang effectif des états       -> dimensions ouvertes      (candidat : pi)
    profondeur de cristallisation -> profondeur à laquelle la réponse se fige
                                     (candidat : kappa, mesuré en COUCHES)

Aucun appel réseau, aucun coût : le modèle est exécuté sur la machine.
Instrument par défaut : SmolLM2-135M-Instruct, déjà présent en cache.

Licence : CC0 — domaine public.
"""

from __future__ import annotations

import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

try:  # Console Windows en cp1252 : même idiome que src/mttv_bgate_system.py
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

MODELE = "HuggingFaceTB/SmolLM2-135M-Instruct"
QUESTION = "En une phrase : qu'est-ce qui distingue retenir un flux de le figer ?"


def cka_lineaire(x: torch.Tensor, y: torch.Tensor) -> float:
    """Similarité de représentation entre deux couches (CKA linéaire).

    Proche de 1 : la couche a conservé la représentation précédente.
    Proche de 0 : elle l'a réécrite.
    """
    xc = x - x.mean(dim=0, keepdim=True)
    yc = y - y.mean(dim=0, keepdim=True)
    numerateur = torch.norm(xc.t() @ yc, p="fro") ** 2
    denominateur = torch.norm(xc.t() @ xc, p="fro") * torch.norm(yc.t() @ yc, p="fro")
    if denominateur == 0:
        return float("nan")
    return float(numerateur / denominateur)


def rang_effectif(x: torch.Tensor) -> float:
    """Rang effectif (rapport de participation) : nombre de dimensions réellement occupées."""
    xc = x - x.mean(dim=0, keepdim=True)
    valeurs = torch.linalg.svdvals(xc)
    somme = valeurs.sum()
    if somme == 0:
        return float("nan")
    return float((somme ** 2) / (valeurs ** 2).sum())


def entropie_attention(attentions) -> list[float]:
    """Entropie (bits) de l'attention, moyenne sur têtes et positions, par couche."""
    resultats = []
    epsilon = 1e-9
    for couche in attentions:
        # couche : [1, tetes, positions_requete, positions_cle]
        p = couche[0]
        e = -(p * torch.log2(p + epsilon)).sum(dim=-1)  # par (tete, requete)
        resultats.append(float(e.mean()))
    return resultats


def main() -> int:
    print("SONDE DES COUCHES INTERNES — examen passif")
    print("=" * 74)
    print(f"  instrument : {MODELE}")
    print(f"  question   : {QUESTION}")
    print()

    tokenizer = AutoTokenizer.from_pretrained(MODELE)
    # attn_implementation="eager" est requis pour que les matrices d'attention
    # soient réellement renvoyées (l'implémentation optimisée ne les expose pas).
    try:
        modele = AutoModelForCausalLM.from_pretrained(
            MODELE, dtype=torch.float32, attn_implementation="eager"
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  ÉCHEC du chargement en mode eager ({type(exc).__name__}) : "
              "les attentions ne seront pas disponibles.")
        modele = AutoModelForCausalLM.from_pretrained(MODELE, dtype=torch.float32)
    modele.eval()

    ids = tokenizer.apply_chat_template(
        [{"role": "user", "content": QUESTION}],
        add_generation_prompt=True,
        return_tensors=None,
    )
    if not isinstance(ids, list):
        ids = ids["input_ids"]
    entree = torch.tensor([ids])
    n_jetons = entree.shape[1]
    print(f"  entrée : {n_jetons} jetons")

    with torch.no_grad():
        sorties = modele(entree, output_hidden_states=True, output_attentions=True)

    etats = sorties.hidden_states          # n_couches + 1 tenseurs [1, seq, d]
    n_couches = len(etats) - 1
    print(f"  couches : {n_couches}   |   dimension cachée : {etats[0].shape[-1]}")
    print()

    # --- 1. Entropie d'attention -------------------------------------------
    print("1. ENTROPIE D'ATTENTION (bits) — dispersion de l'attention")
    if getattr(sorties, "attentions", None):
        entropies = entropie_attention(sorties.attentions)
        for i, e in enumerate(entropies):
            barre = "=" * max(1, int(e * 4))
            print(f"   couche {i:>2} : {e:5.2f}  {barre}")
        mini, maxi = min(entropies), max(entropies)
        print(f"   -> minimum {mini:.2f} (couche {entropies.index(mini)}) · "
              f"maximum {maxi:.2f} (couche {entropies.index(maxi)})")
    else:
        print("   indisponible : le modèle n'a pas renvoyé les matrices d'attention.")
    print()

    # --- 2. CKA entre couches voisines -------------------------------------
    print("2. CKA ENTRE COUCHES VOISINES — rétention (proche de 1) vs réécriture (proche de 0)")
    ckas = []
    for i in range(n_couches):
        x = etats[i][0]
        y = etats[i + 1][0]
        ckas.append(cka_lineaire(x, y))
    for i, c in enumerate(ckas):
        barre = "#" * max(1, int((1.0 - c) * 40))
        print(f"   couche {i:>2} -> {i + 1:>2} : CKA {c:5.3f}  {barre}")
    if ckas:
        indice = min(range(len(ckas)), key=lambda k: ckas[k])
        print(f"   -> réécriture la plus forte : couche {indice} -> {indice + 1} "
              f"(CKA {ckas[indice]:.3f})")
    print()

    # --- 3. Rang effectif des états cachés ---------------------------------
    print("3. RANG EFFECTIF DES ÉTATS — nombre de dimensions réellement ouvertes")
    for i, etat in enumerate(etats):
        r = rang_effectif(etat[0])
        barre = "=" * max(1, int(r / 2))
        print(f"   couche {i:>2} : rang {r:6.1f}  {barre}")
    print()

    # --- 4. Profondeur de cristallisation (logit lens) ---------------------
    print("4. PROFONDEUR DE CRISTALLISATION — à quelle couche la réponse se fige")
    norme = getattr(modele, "model", modele).norm
    tete = modele.lm_head
    with torch.no_grad():
        jeton_final = int(sorties.logits[0, -1].argmax())
        figee_a = None
        for i in range(n_couches):
            logits = tete(norme(etats[i][0, -1]))
            if int(logits.argmax()) == jeton_final and figee_a is None:
                figee_a = i
    mot_final = tokenizer.decode([jeton_final])
    print(f"   prédiction finale : {mot_final!r}")
    if figee_a is None:
        print("   -> la prédiction ne converge jamais avant la dernière couche")
    else:
        print(f"   -> stabilisée dès la couche {figee_a} sur {n_couches} "
              f"({100 * figee_a / n_couches:.0f} % de la profondeur)")
        print("      (une cristallisation précoce signale une clôture hâtive —")
        print("       analogue en profondeur de l'effet de seuil définitif de la B-gate)")
    print()
    print("Aucun appel réseau, aucune modification du modèle. Examen passif terminé.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
