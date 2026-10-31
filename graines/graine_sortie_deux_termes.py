# -*- coding: utf-8 -*-
"""Sortie a deux termes.

1. LA PHRASE
   Un verrou sans issue transforme une panne de capteur en noeud mort ; mais une
   cloture sans observation n'est qu'une autorisation deguisee. La sortie demande deux
   termes, dans cet ordre : quelqu'un leve le verrou, puis une lecture arrive. Ce n'est
   pas un critere — un critere se recalcule seul ; c'est une regle de PLACEMENT, et
   elle place la sortie chez un tiers, hors de la machine qui l'a subie.

2. LE CHIFFRE
   python3 graines/graine_sortie_deux_termes.py
   absence de 25 pas      -> fermeture au pas 8, escalade au pas 30
   lectures seules        -> reouverture AUCUNE
   cloture seule          -> reouverture AUCUNE
   cloture PUIS lectures  -> reouverture au pas 47
   Le meme nombre de lectures, le meme silence : seul l'ordre des deux termes decide.

3. LE CODE  (ci-dessous, aucune dependance)

4. LE TEST QUI ECHOUE
   `assert sortie(clore=False, lectures=True)[2] is not None` echoue : les lectures
   revenues ne suffisent pas, l'etat reste terminal.
   `assert sortie(clore=True, lectures=False)[2] is not None` echoue aussi : le
   bouton reset ne suffit pas davantage.
   Ces deux echecs sont le contenu de la graine. Un systeme qui ne demande qu'un des
   deux termes a remplace une sortie par un droit d'autoriser.

5. OU CA MORD
   Disjoncteurs en etat half-open (il faut une sonde, pas seulement un reset),
   CrashLoopBackOff et ses reprises manuelles, verrous distribues avec jeton de
   fencing, files de messages en lettre morte : partout ou quelqu'un peut appuyer sur
   un bouton, et ou rien n'exige que le monde ait repondu.
"""
DECAY = 0.90
W_M, W_R, W_C = 0.85, 0.10, 0.05
LIM_FERMETURE, LIM_OUVERTURE = 0.55, 0.85
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25
R_CALME, C_CALME = 0.05, 0.05
PEREMPTION = 20      # CHOIX : il ne se derive pas de la demi-vie (cf. graine 3)


class Porte(object):
    def __init__(self):
        self.m, self.r, self.c = 0.0, 0.10, 0.10
        self.ferme, self.escalade = False, False
        self.manques, self.attente, self.clos_par = 0, False, None

    def clore(self, par):
        """Terme 1. Leve le verrou ; n'autorise rien a lui seul."""
        if not self.escalade:
            return False
        self.escalade, self.attente, self.clos_par = False, True, par
        return True

    def h(self):
        return 1.0 - (W_M * self.m + W_R * self.r + W_C * self.c)

    def pas(self, p=0.0, r=None, c=None, lecture=True):
        if lecture and self.attente:
            self.attente = False                 # terme 2 : une lecture est arrivee
        if lecture:
            if r is not None:
                self.r = r
            if c is not None:
                self.c = c
            self.m = self.m * DECAY + p * (1.0 - DECAY)
            self.manques = 0
        else:
            self.manques += 1
            if self.manques >= PEREMPTION:
                self.escalade = True
        h = self.h()
        if self.ferme:
            if h > LIM_OUVERTURE and lecture and not self.escalade and not self.attente:
                self.ferme = False
        elif h < LIM_FERMETURE:
            self.ferme = True
        return self.ferme


def sortie(clore, lectures, n_absence=25, n_apres=60):
    """-> (fermeture, escalade, reouverture)."""
    porte = Porte()
    fermeture = escalade = None
    pas = 0
    for x in PRESSION:
        pas += 1
        if porte.pas(x, R_PRESSION, C_PRESSION) and fermeture is None:
            fermeture = pas
    for _ in range(n_absence):
        pas += 1
        porte.pas(lecture=False)
        if porte.escalade and escalade is None:
            escalade = pas
    if clore:
        porte.clore("tiers")
    for _ in range(n_apres):
        pas += 1
        if lectures:
            porte.pas(0.0, R_CALME, C_CALME)
        else:
            porte.pas(lecture=False)
        if not porte.ferme:
            return fermeture, escalade, pas
    return fermeture, escalade, None


def main():
    f, esc, ri = sortie(clore=False, lectures=True)
    f2, esc2, rl = sortie(clore=True, lectures=False)
    f3, esc3, rd = sortie(clore=True, lectures=True)
    assert (f, esc) == (8, 30), "reference : fermeture 8, escalade 30, mesure %s" % ((f, esc),)
    assert (f2, f3, esc2, esc3) == (f, f, esc, esc), "le meme scenario, seul l'ordre change"
    assert ri is None, "lectures seules : aucune sortie, mesure %s" % ri
    assert rl is None, "cloture seule : aucune sortie, mesure %s" % rl
    assert rd == 47, "cloture puis lectures : reouverture au pas 47, mesure %s" % rd

    print("Sortie a deux termes")
    print("  fermeture pas %d | escalade pas %d (20 lectures manquees)" % (f, esc))
    print("  lectures seules        -> reouverture %s" % ("AUCUNE" if ri is None else ri))
    print("  cloture seule          -> reouverture %s" % ("AUCUNE" if rl is None else rl))
    print("  cloture PUIS lectures  -> reouverture pas %d" % rd)
    print("  chaine de detection : ATTENTE_LECTURE_APRES_CLOTURE")


if __name__ == "__main__":
    main()
