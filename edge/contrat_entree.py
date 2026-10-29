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
import math
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

# Seuil de peremption : il n'est pas choisi, il se derive. La demi-vie de la cicatrice est
# le temps au bout duquel la memoire a perdu la moitie de son ecart au milieu :
#     tau_m = ln(0,5) / ln(0,90) = 6,5788 cycles
# On escalade apres trois demi-vies — au-dela, il ne reste que 12,5 % de l'ecart initial,
# donc l'information portee par la memoire est trop degradee pour distinguer encore
# « calme qui dure » et « silence qui s'installe ».
DEMI_VIE = math.log(0.5) / math.log(DECAY)
N_DEMI_VIES = 3
PEREMPTION = int(math.ceil(N_DEMI_VIES * DEMI_VIE))    # -> 20

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
        # SORTIE D'ESCALADE (2026-10-29). Le verrou n'est plus terminal : il se leve par
        # `clore()`, mais la levee ne suffit pas. `attente_lecture` exige qu'au moins une
        # lecture arrive APRES la cloture — sans quoi la cloture serait une autorisation
        # sans observation, ce que toute la discussion du 29/10 refuse.
        self.attente_lecture = False
        self.clos_par = None     # qui a leve le verrou : trace, non condition

    def clore(self, par):
        """Leve le verrou d'escalade. Ne rouvre rien : exige une lecture posterieure."""
        if self.escalade:
            self.escalade = False
            self.attente_lecture = True
            self.clos_par = par
            return True
        return False

    def _h(self):
        return plafond(1.0 - (W_M * self.m + W_R * self.r + W_C * self.c))

    def pas(self, p=0.0, r=None, c=None, lecture=True, reveil=False):
        if reveil:
            self.reveil = True

        # une lecture apres une cloture satisfait la condition d'observation
        if lecture and self.attente_lecture:
            self.attente_lecture = False

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
                rouvrir = ((h > LIM_OUVERTURE) and lecture
                           and not self.escalade and not self.attente_lecture)

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


def scenario_escalade(faire_clore, lectures_apres, n_absence=25, n_apres=60):
    """Escalade declenchee, puis cloture eventuelle, puis lectures eventuelles.

    -> (fermeture, reouverture, escalade encore active, qui a clos).
    """
    porte = Porte("C")
    fermeture = reouverture = None
    pas = 0

    for p in PRESSION:
        pas += 1
        porte.pas(p, R_PRESSION, C_PRESSION)
        if fermeture is None and porte.ferme:
            fermeture = pas

    for _ in range(n_absence):
        pas += 1
        porte.pas(lecture=False)

    if faire_clore:
        porte.clore("tiers")

    for _ in range(n_apres):
        pas += 1
        if lectures_apres:
            porte.pas(0.0, R_CALME, C_CALME, lecture=True)
        else:
            porte.pas(lecture=False)
        if reouverture is None and not porte.ferme:
            reouverture = pas

    return fermeture, reouverture, porte.escalade, porte.clos_par


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
    titre("Le seuil d'escalade n'est pas choisi, il est derive")
    print("  demi-vie de la cicatrice : tau_m = ln(0,5)/ln(0,90) = %.4f cycles" % DEMI_VIE)
    print("  seuil d'escalade         : %d demi-vies -> %d cycles (%.2f tau_m)"
          % (N_DEMI_VIES, PEREMPTION, PEREMPTION / DEMI_VIE))
    print("  memoire restante au seuil : %.1f %% de l'ecart initial"
          % (100.0 * DECAY ** PEREMPTION))

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

    titre("5. La sortie d'escalade : deux termes, pas un bouton")
    print("  absence de 25 pas -> escalade au 20e, verrou pose.")
    print()
    print("  %-38s %-14s %-12s" % ("situation", "reouverture", "verrou"))
    cas = [
        ("aucune cloture, lectures revenues", False, True),
        ("cloture, puis lectures revenues", True, True),
        ("cloture, aucune lecture ensuite", True, False),
    ]
    for libelle, clore, lectures in cas:
        f, r, esc, par = scenario_escalade(clore, lectures)
        print("  %-38s %-14s %-12s"
              % (libelle, ("pas %d" % r) if r else "AUCUNE",
                 "leve par %s" % par if par else "toujours pose"))
    print()
    print("  Ni l'un ni l'autre des deux premiers cas ne suffit seul :")
    print("    - lectures sans cloture  -> rien ne leve le verrou (etat terminal) ;")
    print("    - cloture sans lecture   -> la cloture ne vaut pas observation.")
    print("  La porte ne se rouvre que si les DEUX termes sont satisfaits, dans cet ordre.")

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
