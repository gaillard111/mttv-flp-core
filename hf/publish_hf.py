#!/usr/bin/env python3
"""
Publication des artefacts MTTV-FLP sur HuggingFace.

Crée (ou met à jour) deux dépôts sous le compte authentifié :
  - un Space statique  : mttv-mycelial-handshake  (HTML/JS, gratuit)
  - un Dataset         : mttv-mpvr-quorum-runs

Note : un Space Gradio/Docker exigerait un abonnement PRO (cpu-basic). On
publie donc la variante **statique**, gratuite pour tous, dans `hf/space_static/`.

L'authentification est lue depuis le cache HuggingFace (`hf auth login`).

Usage :
    python publish_hf.py            # publie Space statique + Dataset
    python publish_hf.py --dry-run  # n'envoie rien, affiche le plan
"""

import argparse
import os
import sys

from huggingface_hub import HfApi

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_SPACE = os.path.join(ICI, "space_static")
DOSSIER_DATASET = os.path.join(ICI, "dataset")

NOM_SPACE = "mttv-mycelial-handshake"
NOM_DATASET = "mttv-mpvr-quorum-runs"

# Artefacts non publiables : caches Python et fichiers compiles.
EXCLUSIONS = ["__pycache__/*", "**/__pycache__/*", "*.pyc", "*.pyo"]


def publier(dry_run=False):
    api = HfApi()
    utilisateur = api.whoami()["name"]

    id_space = f"{utilisateur}/{NOM_SPACE}"
    id_dataset = f"{utilisateur}/{NOM_DATASET}"

    print(f"Utilisateur HuggingFace : {utilisateur}")
    print(f"Space statique cible    : {id_space}")
    print(f"Dataset cible           : {id_dataset}")

    if dry_run:
        print("\n[dry-run] Aucune écriture effectuée.")
        return id_space, id_dataset

    api.create_repo(
        repo_id=id_space, repo_type="space", space_sdk="static", exist_ok=True
    )
    api.upload_folder(
        folder_path=DOSSIER_SPACE,
        repo_id=id_space,
        repo_type="space",
        commit_message="feat: Space statique — handshake mycélien MTTV-FLP/MPVR",
        ignore_patterns=EXCLUSIONS,
    )
    print(f"Space publié   : https://huggingface.co/spaces/{id_space}")

    api.create_repo(repo_id=id_dataset, repo_type="dataset", exist_ok=True)
    api.upload_folder(
        folder_path=DOSSIER_DATASET,
        repo_id=id_dataset,
        repo_type="dataset",
        commit_message="feat: dataset couplage quorum MPVR (runs synthétiques)",
        ignore_patterns=EXCLUSIONS,
    )
    print(f"Dataset publié : https://huggingface.co/datasets/{id_dataset}")

    return id_space, id_dataset


if __name__ == "__main__":
    parseur = argparse.ArgumentParser()
    parseur.add_argument("--dry-run", action="store_true")
    args = parseur.parse_args()
    try:
        publier(dry_run=args.dry_run)
    except Exception as erreur:  # noqa: BLE001
        print(f"Échec de la publication : {erreur}", file=sys.stderr)
        sys.exit(1)
