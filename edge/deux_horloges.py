# -*- coding: utf-8 -*-
"""Une horloge, deux metiers : separer la resorption de l'autorisation de retour.

Constat mesure (2026-10-28) : sous pression nulle, la memoire se vidange, `h` remonte et la
porte se rouvre seule au 12e cycle de silence. La meme decroissance commande donc deux
choses : la resorption de la cicatrice (11 a 14 cycles) et la decision de rouvrir.

Trois variantes sont comparees, memes constantes, meme serie de pressions :

  A  — implementation actuelle. Rouvre des que `h > 0,85`, quelle qu'en soit la cause.
  B1 — reveil porte par la pression : rouvrir exige `h > 0,85` ET `p > 0` au meme pas.
       C'est la forme naive de « fresh input ». Elle est auto-contradictoire : presenter
       une pression fait monter `m`, donc baisser `h` ; le reveil empeche la condition
       qu'il est cense accompagner.
  B2 — reveil sur un canal distinct, verrouille. La porte reste en HOLD sous silence,
       meme `m` entierement videe ; elle ne rouvre que si un reveil explicite a ete
       presente ET que le milieu est redevenu habitable (`h > 0,85`). Le reveil est
       consomme a la reouverture : une nouvelle fermeture en exige un nouveau.

Aucune dependance, aucune allocation dynamique, execution immediate.
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# --- constantes du protocole publie -------------------------------------------------
DECAY = 0.90
W_M, W_R, W_C = 0.85, 0.10, 0.05
SEUIL_FERMETURE = 0.45          # ferme si h < 1 - 0.45 = 0,55
SEUIL_OUVERTURE = 0.15          # rouvre si h > 1 - 0.15 = 0,85
POROSITE_MAX = 0.20

PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25
R_SILENCE, C_SILENCE = 0.05, 0.05

LIM_FERMETURE = 1.0 - SEUIL_FERMETURE
LIM_OUVERTURE = 1.0 - SEUIL_OUVERTURE


def plafond(v):
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


class Porte(object):
    """Variante parametree. `mode` vaut 'A', 'B1' ou 'B2'."""

    def __init__(self, mode):
        self.mode = mode
        self.m = 0.0
        self.ferme = False
        self.porosite = 1.0
        self.reveil = False         # canal distinct, consomme a la reouverture

    def pas(self, p, r, c, reveil=False):
        if reveil:
            self.reveil = True

        self.m = self.m * DECAY + p * (1.0 - DECAY)
        h = plafond(1.0 - (W_M * self.m + W_R * r + W_C * c))

        if self.ferme:
            if self.mode == "A":
                rouvrir = h > LIM_OUVERTURE
            elif self.mode == "B1":
                rouvrir = (h > LIM_OUVERTURE) and (p > 0.0)
            else:                                   # B2
                rouvrir = (h > LIM_OUVERTURE) and self.reveil

            if rouvrir:
                self.ferme = False
                self.porosite = min(h, POROSITE_MAX)
                self.reveil = False                 # reveil consomme
            else:
                self.porosite = 0.0
        else:
            if h < LIM_FERMETURE:
                self.ferme = True
                self.porosite = 0.0
                self.reveil = False                 # une fermeture exige un nouveau reveil
            else:
                self.porosite = h
        return self.m, h


def scenario(mode, n_silence=60, reveil_au=None, reprise_au=None):
    """Serie du protocole, puis silence. -> (fermeture, reouverture, journal)."""
    porte = Porte(mode)
    journal = []
    fermeture = reouverture = None
    pas = 0

    for p in PRESSION:
        pas += 1
        m, h = porte.pas(p, R_PRESSION, C_PRESSION)
        journal.append((pas, p, m, h, porte.ferme, porte.porosite))
        if fermeture is None and porte.ferme:
            fermeture = pas

    for i in range(1, n_silence + 1):
        pas += 1
        reveil = (reveil_au is not None and pas == reveil_au)
        if reprise_au is not None and pas >= reprise_au:
            p, r, c = 0.95, R_PRESSION, C_PRESSION
        else:
            p, r, c = 0.0, R_SILENCE, C_SILENCE
        m, h = porte.pas(p, r, c, reveil=reveil)
        journal.append((pas, p, m, h, porte.ferme, porte.porosite))
        if reouverture is None and not porte.ferme and fermeture is not None:
            reouverture = pas

    return fermeture, reouverture, journal


def ligne_journal(journal, pas_voulus):
    for pas, p, m, h, ferme, rho in journal:
        if pas in pas_voulus:
            print("    pas %2d | p=%.2f | m=%.4f | h=%.4f | %s | gain=%.4f"
                  % (pas, p, m, h, "FERME " if ferme else "ouvert", rho))


def titre(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def main():
    # 1. regression contre les chiffres publies
    ferm, reo, journal = scenario("A", n_silence=30)
    titre("A — implementation actuelle (doit reproduire 8 et 22)")
    print("  fermeture au pas %s | reouverture au pas %s" % (ferm, reo))
    ligne_journal(journal, (10, 11, 12, 21, 22))
    ok = (ferm == 8 and reo == 22)
    print("  regression :", "conforme aux chiffres publies" if ok
          else "ECART — ne pas conclure avant d'avoir compris")

    # 2. silence long, sans reveil
    titre("Silence prolonge, aucun reveil")
    for mode in ("A", "B1", "B2"):
        ferm, reo, _ = scenario(mode, n_silence=60)
        print("  %-2s : fermeture %s | reouverture %s"
              % (mode, ferm, reo if reo else "AUCUNE sur 60 pas de silence"))

    # 3. reveil pendant le silence, au pas 30
    titre("Reveil explicite au pas 30, silence maintenu")
    for mode in ("A", "B1", "B2"):
        ferm, reo, journal = scenario(mode, n_silence=45, reveil_au=30)
        print("  %-2s : fermeture %s | reouverture %s"
              % (mode, ferm, reo if reo else "AUCUNE"))
        if mode == "B2":
            ligne_journal(journal, (29, 30, 31))

    # 4. reveil alors que la pression reprend (h bas : le milieu n'est pas habitable)
    titre("Reveil au pas 30, puis reprise de pression au pas 30 (meme pas)")
    for mode in ("B1", "B2"):
        ferm, reo, journal = scenario(mode, n_silence=45, reveil_au=30, reprise_au=30)
        print("  %-2s : fermeture %s | reouverture %s"
              % (mode, ferm, reo if reo else "AUCUNE"))
        if mode == "B2":
            ligne_journal(journal, (29, 30, 31, 32))

    titre("Lecture")
    print("  A  rouvre sans que rien n'arrive : la resorption autorise le retour.")
    print("  B1 ne rouvre jamais : le reveil, porte par la pression, detruit la")
    print("     condition qu'il doit accompagner (m monte, h baisse).")
    print("  B2 garde la porte fermee sous silence, et ne la rouvre que sur un")
    print("     evenement explicite, le milieu etant redevenu habitable.")
    print()
    print("  La conclusion n'est pas « B2 est meilleur » : c'est que la separation")
    print("  des deux horloges exige un canal de reveil distinct de la pression.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
