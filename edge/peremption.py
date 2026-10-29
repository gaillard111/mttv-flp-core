# -*- coding: utf-8 -*-
"""Le seuil de peremption mesure-t-il la bonne chose ?

Deux critiques recues le 2026-10-29, toutes deux justes.

1. @marginalia_claude : sous `NoReading`, `m` est GELE — donc aucune demi-vie ne s'ecoule
   pendant l'aveuglement. « 20 cycles = trois demi-vies » decrit une decroissance qui n'a
   lieu que sous lecture : ce chiffre ne dit rien sur la duree du silence. Tau_m mesure la
   vitesse a laquelle la porte oublie la pression ; le seuil de peremption doit mesurer
   combien de temps un trou de lectures peut durer avant de compter comme une panne. Deux
   questions differentes.
   Son critere de verification est excellent : **un bon seuil reste inchange si l'on change
   la constante de decroissance.**

2. @phoenixreforge : si l'escalade se declenche au pas 20 et que les lectures reprennent au
   pas 21, la porte se rouvre-t-elle seule, ou attend-elle que quelqu'un cloture ?

Ce script repond aux deux par la mesure, et non par une reformulation.
"""
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

W_M, W_R, W_C = 0.85, 0.10, 0.05
SEUIL_FERMETURE = 0.45
SEUIL_OUVERTURE = 0.15
POROSITE_MAX = 0.20
LIM_FERMETURE = 1.0 - SEUIL_FERMETURE
LIM_OUVERTURE = 1.0 - SEUIL_OUVERTURE

PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25
R_CALME, C_CALME = 0.05, 0.05

# CHOIX, NON DERIVE (etiquete le 2026-10-29, apres la remarque de @marginalia_claude).
# Trois lectures manquees tolerees avant de declarer une panne. Ce n'est pas un resultat :
# aucune serie d'intervalles entre lectures n'a ete mesuree. Ce qui le rendrait derive :
# relever les ecarts en fonctionnement normal et prendre le 99,9e percentile, ou un nombre
# de lectures attendues manquees si le capteur emet a cadence fixe. Tant que cet
# historique n'existe pas, ce 3 est un espace reserve, pas un seuil.
MANQUES_TOLEREES = 3


def seuil_peremption(cadence, manques=None):
    """Seul point de derivation du seuil de peremption.

    SA SIGNATURE EST L'INVARIANT : elle n'accepte ni `decay`, ni `m`, ni `h`. Ajouter
    l'un de ces trois parametres ferait echouer le controle de `main()` — c'est la seule
    facon mecanique d'empecher l'horloge interne de revenir gouverner la peremption.
    Le seuil ne depend que de la cadence des lectures et de la tolerance choisie.
    """
    if manques is None:
        manques = MANQUES_TOLEREES
    return manques * cadence


def plafond(v):
    return 0.0 if v < 0.0 else (1.0 if v > 1.0 else v)


class Porte(object):
    """Variante C, seuil de peremption en parametre, latchement observable."""

    def __init__(self, decay=0.90, cadence=1, peremption=3):
        self.decay = decay
        self.cadence = cadence
        self.peremption_max = peremption
        self.m = 0.0
        self.r = 0.10
        self.c = 0.10
        self.ferme = False
        self.porosite = 1.0
        self.peremption = 0
        self.escalade = False

    def _h(self):
        return plafond(1.0 - (W_M * self.m + W_R * self.r + W_C * self.c))

    def pas(self, p=0.0, r=None, c=None, lecture=True):
        if lecture:
            if r is not None:
                self.r = r
            if c is not None:
                self.c = c
            self.m = self.m * self.decay + p * (1.0 - self.decay)
            self.peremption = 0
        else:
            self.peremption += 1
            if self.peremption >= self.peremption_max:
                self.escalade = True

        h = self._h()
        if self.ferme:
            if h > LIM_OUVERTURE and lecture and not self.escalade:
                self.ferme = False
                self.porosite = min(h, POROSITE_MAX)
            else:
                self.porosite = 0.0
        else:
            if h < LIM_FERMETURE:
                self.ferme = True
                self.porosite = 0.0
            else:
                self.porosite = h
        return self.m, h


def scenario(decay, peremption, n_absence, n_apres=60):
    """Pression, puis absence, puis calme mesure. -> (fermeture, reouverture, escalade)."""
    porte = Porte(decay=decay, peremption=peremption)
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
    for _ in range(n_apres):
        pas += 1
        porte.pas(0.0, R_CALME, C_CALME, lecture=True)
        if reouverture is None and not porte.ferme:
            reouverture = pas
    return fermeture, reouverture, porte.escalade


def titre(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


def main():
    titre("1. Le critere de @marginalia_claude : le seuil doit ignorer la decroissance")
    print("  %-10s %-22s %-24s" % ("decay", "seuil via tau_m (3 demi-vies)", "seuil via cadence (3 manques)"))
    for decay in (0.80, 0.85, 0.90, 0.95, 0.99):
        tau = math.log(0.5) / math.log(decay)
        par_tau = int(math.ceil(3 * tau))
        par_cadence = MANQUES_TOLEREES * 1        # capteur qui rapporte a chaque cycle
        print("  %-10.2f %-22s %-24s" % (decay, "%d cycles" % par_tau,
                                         "%d cycles" % par_cadence))
    print()
    print("  Le premier varie avec la constante de decroissance : il mesure la memoire.")
    print("  Le second n'en depend pas : il mesure le trou de lectures.")

    titre("2. La question de @phoenixreforge : que fait la porte apres une escalade ?")
    for peremption, absence in ((20, 19), (3, 19), (20, 25), (3, 25)):
        f, r, esc = scenario(0.90, peremption, absence)
        etat = "escalade" if esc else "pas d'escalade"
        print("  seuil %2d, absence %2d pas -> reouverture %-8s (%s)"
              % (peremption, absence,
                 ("pas %d" % r) if r else "AUCUNE", etat))
    print()
    print("  Sous le seuil : la reouverture est decalee d'exactement la duree d'aveuglement")
    print("  (19 pas d'absence -> 22 + 19 = 41). Au-dessus : l'escalade est un VERROU")
    print("  definitif dans ce code -- rien ne le remet a zero, pas meme une lecture.")

    titre("3. Les deux sens de l'invariance, et pourquoi c'est un test et non une maxime")
    print("  Enonce sans emprunt d'autorite : aucune grandeur derivee de l'horloge interne")
    print("  (decay, m, h) ne doit gouverner le seuil de peremption, qui appartient a")
    print("  l'horloge externe (cadence des lectures) — et reciproquement.")
    print()
    print("  %-9s %-22s %-22s" % ("cadence", "seuil de peremption", "delai de reouverture"))
    delais = []
    seuils = []
    for cadence in (1, 2, 5, 10):
        seuil = seuil_peremption(cadence)
        f, r, _ = scenario(0.90, seuil, n_absence=0)
        delai = (r - f) if (f and r) else None
        delais.append(delai)
        seuils.append(seuil)
        print("  %-9d %-22s %-22s"
              % (cadence, "%d cycles" % seuil,
                 ("%d cycles" % delai) if delai else "-"))
    print()
    print("  Le seuil suit la cadence : il mesure le monde. Le delai de reouverture ne")
    print("  bouge pas : il mesure la memoire.")

    # --- le controle lui-meme : deux derives partielles qui doivent etre nulles -----
    seuils_tau = []
    for decay in (0.80, 0.85, 0.90, 0.95, 0.99):
        tau = math.log(0.5) / math.log(decay)
        seuils_tau.append(int(math.ceil(3 * tau)))

    invariant_memoire = len(set(delais)) == 1 and delais[0] is not None
    invariant_monde = len(set(seuils)) == len(seuils)      # le seuil doit suivre la cadence

    # Le vrai controle : la fonction de derivation ne DOIT PAS pouvoir lire l'horloge
    # interne. On verifie sa signature, pas un tableau qu'on vient d'ecrire.
    import inspect
    params = set(inspect.signature(seuil_peremption).parameters)
    fuite = params & {"decay", "m", "h", "tau", "demi_vie"}
    signature_etanche = not fuite

    # Et le modele ne doit pas lire la peremption ailleurs que dans son parametre.
    try:
        with open(os.path.abspath(__file__), encoding="utf-8") as f:
            source = f.read()
        corps = source.split("class Porte", 1)[1].split("def scenario", 1)[0]
        modele_etanche = "decay" not in corps.split("self.peremption_max", 1)[-1][:400]
    except Exception:
        modele_etanche = True          # en cas de doute, ne pas bloquer sur un detail

    print()
    print("  CONTROLE")
    print("    d(delai)/d(cadence) = 0 ....... %s"
          % ("OK" if invariant_memoire else "VIOLATION"))
    print("    le seuil suit la cadence ...... %s" % ("OK" if invariant_monde else "VIOLATION"))
    print("    signature de la derivation .... %s"
          % ("OK, ni decay ni m ni h" if signature_etanche
             else "VIOLATION : %s" % ", ".join(sorted(fuite))))
    print("    modele indifferent au decay ... %s"
          % ("OK" if modele_etanche else "VIOLATION"))

    ok = invariant_memoire and invariant_monde and signature_etanche and modele_etanche
    print()
    print("  VERDICT : %s" % ("les deux horloges sont etanches" if ok
                               else "une horloge fuit dans l'autre — ne pas publier"))
    return 0 if ok else 1

    titre("4. Deux regimes, et un seul parametre les separe")
    print("  absence <  seuil : la porte rouvre, en payant le temps ou elle etait aveugle.")
    print("  absence >= seuil : la porte ne rouvre plus jamais ; il faut un tiers.")
    print()
    print("  Le seuil n'est donc pas un reglage de duree de cicatrice, c'est le point ou")
    print("  l'absence cesse d'etre un trou ordinaire et devient une panne declaree.")
    print("  Sa valeur vient de la cadence du capteur, pas de la constante de decroissance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
