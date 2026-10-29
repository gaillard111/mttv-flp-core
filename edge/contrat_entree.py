# -*- coding: utf-8 -*-
"""Le defaut est dans le contrat d'entree, pas dans la machine a etats.

Observation du 2026-10-29 (marginalia_claude, post 11) : `p` est un flottant, donc
« pression mesuree a zero » et « aucune lecture recue » ont la meme valeur, 0.0. La
decroissance les traite identiquement, et c'est de la que vient le fail-open : l'absence
devient une preuve de calme.

Trois traitements sont compares, memes constantes, meme serie de pressions :

  A   — actuelle. `p` flottant ; la memoire decroit toujours ; rouvre des que h > 0,85.
  B2  — reveil explicite sur canal separe (cf. deux_horloges.py). Ferme l'absence, mais
        ferme AUSSI le calme reellement mesure : un capteur qui rapporte paisiblement zero
        n'envoie aucun reveil. C'est une sur-correction.
  C   — contrat d'entree explicite. Une lecture peut etre *absente* (`lecture=False`).
        Sous absence : la memoire est GELEE et un compteur de peremption avance ; au-dela
        d'un seuil on ESCALADE au lieu de rouvrir. Sous lecture, meme a zero : le calcul
        reprend, et la reouverture redevient possible — c'est le role de l'hysteresis.

Ce que C doit montrer, et qui departage les deux autres :
  - absence prolongee        -> aucune reouverture, memoire gelee, escalade ;
  - calme reellement mesure  -> reouverture, exactement comme A ;
  - reprise apres absence    -> la decroissance repart de la memoire gelee.

Aucune dependance.
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DECAY = 0.90
W_M, W_R, W_C = 0.85, 0.10, 0.05
SEUIL_FERMETURE = 0.45
SEUIL_OUVERTURE = 0.15
POROSITE_MAX = 0.20
PEREMPTION = 20                  # au-dela, escalade au lieu de rouvrir

PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25
R_CALME, C_CALME = 0.05, 0.05

LIM_FERMETURE = 1.0 - SEUIL_FERMETURE
LIM_OUVERTURE = 1.0 - SEUIL_OUVERTURE


def plafond(v):
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


class Porte(object):
    def __init__(self, mode):
        self.mode = mode
        self.m = 0.0
        self.r = 0.10            # derniere redondance connue
        self.c = 0.10            # dernier cout connu
        self.ferme = False
        self.porosite = 1.0
        self.reveil = False
        self.peremption = 0      # pas consecutifs sans lecture
        self.escalade = False

    def _h(self):
        return plafond(1.0 - (W_M * self.m + W_R * self.r + W_C * self.c))

    def pas(self, p=0.0, r=None, c=None, lecture=True, reveil=False):
        if reveil:
            self.reveil = True

        if self.mode == "A":
            # A ne peut PAS representer l'absence : son entree est un flottant, et une
            # non-lecture y arrive comme un zero. C'est precisement son defaut, et le
            # simuler autrement ferait de la variante de controle une autre variante.
            lecture = True

        if lecture:
            if r is not None:
                self.r = r
            if c is not None:
                self.c = c
            self.m = self.m * DECAY + p * (1.0 - DECAY)
            self.peremption = 0
        else:
            # aucune lecture : on ne devine rien. La memoire et les dernieres valeurs
            # connues sont GELEES ; seul le compteur de peremption avance.
            self.peremption += 1
            if self.peremption >= PEREMPTION:
                self.escalade = True

        h = self._h()

        if self.ferme:
            if self.mode == "A":
                rouvrir = h > LIM_OUVERTURE
            elif self.mode == "B2":
                rouvrir = (h > LIM_OUVERTURE) and self.reveil
            else:                                        # C
                rouvrir = (h > LIM_OUVERTURE) and lecture and not self.escalade

            if rouvrir:
                self.ferme = False
                self.porosite = min(h, POROSITE_MAX)
                self.reveil = False
            else:
                self.porosite = 0.0
        else:
            if h < LIM_FERMETURE:
                self.ferme = True
                self.porosite = 0.0
                self.reveil = False
            else:
                self.porosite = h
        return self.m, h


def scenario(mode, apres, n=60, reprise=None):
    """`apres` vaut 'absence' ou 'calme'. -> (fermeture, reouverture, journal)."""
    porte = Porte(mode)
    journal = []
    fermeture = reouverture = None
    pas = 0

    for p in PRESSION:
        pas += 1
        m, h = porte.pas(p, R_PRESSION, C_PRESSION)
        journal.append((pas, p, True, m, h, porte.ferme, porte.peremption, porte.escalade))
        if fermeture is None and porte.ferme:
            fermeture = pas

    for _ in range(n):
        pas += 1
        if reprise is not None and pas >= reprise:
            m, h = porte.pas(0.0, R_CALME, C_CALME, lecture=True)
            lu = True
        elif apres == "calme":
            m, h = porte.pas(0.0, R_CALME, C_CALME, lecture=True)
            lu = True
        else:
            if mode == "A":
                # A ne peut pas representer l'absence : une non-lecture y arrive comme une
                # lecture a zero, avec les valeurs de calme du protocole publie.
                m, h = porte.pas(0.0, R_CALME, C_CALME, lecture=True)
                lu = True
            else:
                m, h = porte.pas(lecture=False)
                lu = False
        journal.append((pas, 0.0, lu, m, h, porte.ferme, porte.peremption, porte.escalade))
        if reouverture is None and fermeture is not None and not porte.ferme:
            reouverture = pas

    return fermeture, reouverture, journal


def titre(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def details(journal, pas_voulus):
    for pas, p, lu, m, h, ferme, per, esc in journal:
        if pas in pas_voulus:
            print("    pas %2d | %-9s | m=%.4f | h=%.4f | %s | peremption=%2d%s"
                  % (pas, ("lu p=%.2f" % p) if lu else "ABSENCE", m, h,
                     "FERME " if ferme else "ouvert", per, " | ESCALADE" if esc else ""))


def main():
    titre("A — implementation actuelle (regression : doit donner 8 et 22)")
    f, r, j = scenario("A", "absence", n=30)
    print("  fermeture %s | reouverture %s" % (f, r))
    details(j, (10, 21, 22))
    ok = (f == 8 and r == 22)
    print("  regression :", "conforme" if ok else "ECART")

    titre("1. Absence de lecture pendant 60 pas (capteur muet)")
    for mode in ("A", "B2", "C"):
        f, r, j = scenario(mode, "absence", n=60)
        print("  %-2s : fermeture %s | reouverture %-8s"
              % (mode, f, r if r else "AUCUNE"))
    f, r, j = scenario("C", "absence", n=60)
    print("  C, memoire gelee et escalade :")
    details(j, (11, 20, 21, 30, 60))

    titre("2. Calme REELLEMENT mesure pendant 60 pas (le cas que B2 casse)")
    for mode in ("A", "B2", "C"):
        f, r, j = scenario(mode, "calme", n=60)
        print("  %-2s : fermeture %s | reouverture %-8s"
              % (mode, f, r if r else "AUCUNE"))
    f, r, j = scenario("C", "calme", n=60)
    print("  C, calme mesure :")
    details(j, (11, 21, 22))

    titre("3. Absence pendant 20 pas, puis calme mesure au pas 30")
    for mode in ("A", "B2", "C"):
        f, r, j = scenario(mode, "absence", n=60, reprise=30)
        print("  %-2s : fermeture %s | reouverture %-8s"
              % (mode, f, r if r else "AUCUNE"))
    f, r, j = scenario("C", "absence", n=60, reprise=30)
    print("  C, details :")
    details(j, (29, 30, 31, 36, 37))

    titre("Lecture")
    print("  A  rouvre sur l'absence : l'absence tient lieu de calme.")
    print("  B2 ferme les deux cas : il corrige l'absence en supprimant le calme.")
    print("  C  garde les deux : l'absence gele et escalade, le calme mesure rouvre.")
    print()
    print("  Le defaut n'etait pas dans la machine a etats, il etait dans le type de")
    print("  l'entree : un flottant ne peut pas porter l'absence.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
