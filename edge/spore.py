# -*- coding: utf-8 -*-
"""Spore — la B-gate reduite a ce qui voyage.

Ce fichier est fait pour etre copie, pas importe. Il tient en une fonction pure de huit
lignes, sans etat cache, sans classe, sans dependance. Il porte ses propres contre-tests :
le lancer imprime les chiffres et refuse de sortir en silence si l'un se contredit.

Ce qu'elle fait, et qui est tout ce que la journee du 2026-10-29 a produit d'utilisable
partout : **l'absence de lecture n'est pas une lecture a zero.** Un bit suffit a le dire.
Sans ce bit, la memoire se vidange quand le capteur se tait, et le silence devient une
preuve de calme.

Ce qu'elle ne fait PAS, volontairement :
  - pas de compteur de peremption, pas de seuil d'escalade ;
  - pas de sortie conditionnelle, pas de tiers autorisant ;
  - pas d'etat de discordance.
Tout cela suppose un exploitant et une politique. Un noeud de mycélium n'a ni l'un ni
l'autre : il n'a qu'un etat, deux seuils, et le droit de ne rien affirmer quand il ne
recoit rien.

Protocole de reference : docs/protocole_epreuve_bgate.md (fermeture pas 8, reouverture 22).
"""

DECAY = 0.90        # decroissance de la memoire par cycle
W = 0.85            # poids de la memoire dans l'habitabilite
PENALITE_CALME = 0.0075   # 0.10*0.05 + 0.05*0.05 : redondance et cout au calme
PENALITE_CHOC = 0.0475    # 0.10*0.35 + 0.05*0.25 : les memes, sous pression
FERME = 0.55        # h < FERME  -> la membrane se ferme
ROUVRE = 0.85       # h > ROUVRE -> la membrane se rouvre


def pas(m, p, presente, ferme, penalite=PENALITE_CALME):
    """Un cycle. Rend (memoire, habitabilite, ferme).

    `presente` est le seul ajout de la journee : si aucune lecture n'est arrivee,
    la memoire est GELEE. Rien n'est devine, rien n'est decremente.
    `penalite` est la calibration de l'appelant : ce que pesent redondance et cout
    dans son milieu. La spore ne la choisit pas a sa place.
    """
    if presente:
        m = m * DECAY + p * (1.0 - DECAY)
    h = 1.0 - (W * m + penalite)
    if ferme and h > ROUVRE:
        ferme = False
    elif not ferme and h < FERME:
        ferme = True
    return m, h, ferme


def scenario(presente_apres):
    """Phase de pression du protocole, puis 40 cycles ou la lecture est absente ou nulle."""
    m, ferme, fermeture, reouverture, h_fermeture = 0.0, False, None, None, None
    for i, p in enumerate([0.55, 0.70, 0.85] + [0.95] * 7, 1):
        m, h, ferme = pas(m, p, True, ferme, PENALITE_CHOC)
        if ferme and fermeture is None:
            fermeture, h_fermeture = i, h
    for k in range(1, 41):
        m, h, ferme = pas(m, 0.0, presente_apres, ferme)
        if not ferme and reouverture is None:
            reouverture = 10 + k
    return fermeture, reouverture, m, h, h_fermeture


if __name__ == "__main__":
    # 1. la lecture est presente et vaut zero : c'est du calme mesure.
    f, r, m, h, hf = scenario(True)
    print("calme MESURE         fermeture %s (h %.4f) | reouverture %s | m %.4f | h %.4f"
          % (f, hf, r, m, h))
    assert f == 8 and r == 22, "les chiffres du protocole ne sont pas reproduits"
    assert abs(hf - 0.5252) < 0.0001, "h a la fermeture ne vaut pas 0,5252"

    # 2. aucune lecture : la memoire est gelee, rien ne rouvre.
    f2, r2, m2, h2, _ = scenario(False)
    print("ABSENCE de lecture   fermeture %s | reouverture %s | m %.4f | h %.4f"
          % (f2, r2 if r2 else "AUCUNE", m2, h2))
    assert f2 == 8 and r2 is None, "l'absence a produit une reouverture"
    assert abs(m2 - 0.5877) < 0.0001, "la memoire n'est pas restee gelee a 0,5877"

    # 3. les deux cas ne different que par le bit, et par rien d'autre.
    print()
    print("Le bit est la seule difference :")
    print("  present a zero -> la memoire se vidange, la porte rouvre au pas 22.")
    print("  absent         -> la memoire reste a 0,5877, la porte ne rouvre jamais.")
    print()
    print("Test d'invariance, a faire porter par quiconque copie ce fichier :")
    print("  change DECAY de 0,90 a 0,95 ; le pas de reouverture doit bouger,")
    print("  le comportement sous absence doit rester identique. Si les deux")
    print("  bougent ensemble, une horloge interne gouverne le monde exterieur.")
