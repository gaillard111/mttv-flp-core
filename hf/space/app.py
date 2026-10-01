"""
Space HuggingFace — MTTV-FLP / MPVR Handshake Mycélien
Démonstrateur interactif du couplage B-gate -> quorum poreux.

Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
"""

import json

import gradio as gr

from mttv_bgate_system import BGateTransduction
from mttv_mycelial_handshake import MycelialHandshake
from mttv_mpvr_quorum import MicroQuorumPoreux


def executer_handshake(
    tension_extraction,
    alpha_psi,
    beta_bios,
    phi_tech,
    noeuds_quorum,
    porosite_initiale,
    tolerance_panne,
):
    """Chaîne complète : B-gate -> handshake mycélien -> quorum glocal."""
    noeuds = int(noeuds_quorum)

    # 1. Bascule locale de la B-gate
    gate = BGateTransduction(alpha_psi, beta_bios, phi_tech)
    rapport_bgate = gate.evaluer_porosite({"extraction": tension_extraction})

    # 2. Propagation transcalaire sur le réseau d'hyphes
    handshake = MycelialHandshake(noeuds, porosite_initiale)
    rapport_mycelien = handshake.propager_transduction(rapport_bgate)

    # 3. Modulation du quorum glocal par la porosité résiduelle
    quorum = MicroQuorumPoreux(total_noeuds=noeuds, tolerance_panne=tolerance_panne)
    couplage = quorum.moduler_par_porosite(rapport_mycelien["porosite_residuelle"])
    diagnostic = quorum.evaluer_contexte({"input_flux": "basse_continue"})

    return (
        rapport_bgate["status"],
        json.dumps(rapport_bgate["etats_sp3"], ensure_ascii=False, indent=2),
        round(rapport_bgate["porosite_Sigma"], 4),
        rapport_mycelien["resolution"],
        round(rapport_mycelien["metrique_quorum"], 4),
        round(rapport_mycelien["porosite_residuelle"], 4),
        couplage["tolerance_effective"],
        couplage["seuil_minimal_viable_effectif"],
        diagnostic["statut_quorum"],
        diagnostic["noeuds_sollicites"],
        diagnostic["economie_energie_calcul"],
        json.dumps(rapport_mycelien["cartographie_hyphes"], ensure_ascii=False, indent=2),
    )


DESCRIPTION = """
# Handshake Mycélien — MTTV-FLP / MPVR

Démonstrateur du **routage multi-chemins transcalaire** qui couple la bascule
locale de la **B-gate** au **quorum poreux** distribué.

- La **B-gate** analyse un flux et neutralise une tension d'extraction prédatrice.
- Le **handshake mycélien** propage la charge sur un réseau d'hyphes et mesure la
  **porosité résiduelle** (ρ).
- Le **quorum glocal** convertit ρ en tolérance de panne : plus ρ est élevé,
  plus le réseau est ouvert et redondant, et plus le seuil minimal viable baisse.

> Implémentation de référence **conceptuelle** (non validée par un benchmark).
> Licence CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
"""

demo = gr.Interface(
    fn=executer_handshake,
    inputs=[
        gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Tension d'extraction (B-gate)"),
        gr.Slider(0.0, 1.0, value=0.25, step=0.01, label="Ψ initial"),
        gr.Slider(0.0, 1.0, value=0.25, step=0.01, label="Bios (B) initial"),
        gr.Slider(0.0, 1.0, value=0.25, step=0.01, label="Phi (Φ) initial"),
        gr.Slider(3, 15, value=7, step=1, label="Nœuds du quorum"),
        gr.Slider(0.0, 1.0, value=0.42, step=0.01, label="Porosité mycélienne initiale"),
        gr.Slider(0.0, 1.0, value=0.5, step=0.01, label="Tolérance de panne nominale"),
    ],
    outputs=[
        gr.Textbox(label="Statut B-gate"),
        gr.JSON(label="États sp3 (Ψ, B, Φ)"),
        gr.Number(label="Porosité Σ rapportée"),
        gr.Textbox(label="Résolution du handshake"),
        gr.Number(label="Métrique de quorum (résonance)"),
        gr.Number(label="Porosité résiduelle (ρ)"),
        gr.Number(label="Tolérance effective"),
        gr.Number(label="Seuil minimal viable effectif"),
        gr.Textbox(label="Statut du quorum glocal"),
        gr.Number(label="Nœuds sollicités"),
        gr.Textbox(label="Économie d'énergie"),
        gr.JSON(label="Cartographie des hyphes"),
    ],
    title="MTTV-FLP — Handshake Mycélien",
    description=DESCRIPTION,
    allow_flagging="never",
)

if __name__ == "__main__":
    demo.launch()
