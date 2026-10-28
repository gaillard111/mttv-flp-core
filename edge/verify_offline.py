# -*- coding: utf-8 -*-
"""Vérifications faisables SANS compilateur.

Deux choses que le portage C affirme et qu'on veut pouvoir re-vérifier même quand
`cl` et `gcc` sont absents de la machine :

1. la taille de `bgate_t` dans les trois variantes (double / float / float sans journal),
   recalculée ici par `ctypes` qui applique la même règle d'alignement que le compilateur ;
2. le comportement à entrée **nulle** — ce qui se passe quand le capteur tombe au
   plancher de bruit, à partir d'une porte ouverte puis à partir d'une porte fermée.

Le point 2 tranche une question de fait, pas d'opinion : à entrée nulle, la mémoire
d'état se vidange, donc `h` remonte, donc la porte peut se **rouvrir** sans qu'aucune
entrée ne soit jamais remontée. Si c'est vrai, la phrase « à entrée nulle, il ne se
passe rien » est fausse et il faut le dire avant qu'un relecteur le trouve.
"""
import ctypes
import importlib.util
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- tailles d'état
def taille_etat(reel="double", ring=8):
    """Taille de `bgate_t` en octets, même disposition que `bgate.h`."""
    t = ctypes.c_double if reel == "double" else ctypes.c_float
    u8 = ctypes.c_uint8

    class Trace(ctypes.Structure):
        _fields_ = [("p", t), ("h", t), ("m", t), ("rho", t),
                    ("regime", u8), ("valeur", u8)]

    champs = [(nom, t) for nom in (
        "seuil_fermeture", "seuil_ouverture", "memoire_decay",
        "w_memoire", "w_redondance", "w_cout", "porosite_max",
        "frontiere", "derive", "memoire", "porosite", "seuil_courant")]
    champs += [("cycles_silence", ctypes.c_uint32),
               ("ferme", u8), ("valeur", u8), ("tete", u8), ("nb", u8)]
    if ring > 0:
        champs.append(("hist", Trace * ring))

    class Etat(ctypes.Structure):
        _fields_ = champs

    return ctypes.sizeof(Etat)


def tableau_tailles():
    attendu = {("double", 8): 424, ("float", 8): 216, ("float", 0): 56}
    print("variante                        octets   attendu   verdict")
    for (reel, ring), cible in attendu.items():
        mesure = taille_etat(reel, ring)
        verdict = "identique" if mesure == cible else "ECART"
        nom = "%s, journal %s" % (reel, ring if ring else "aucun")
        print("%-30s %7d %9d   %s" % (nom, mesure, cible, verdict))
    return all(taille_etat(r, k) == v for (r, k), v in attendu.items())


# ------------------------------------------------------- comportement à p = 0
def charger_classe():
    chemin = os.path.join(ICI, "..", "experiments", "b_gate_mttv_flp_epreuve.py")
    spec = importlib.util.spec_from_file_location("epreuve", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.AdvancedBGate


def cas_porte_ouverte(Gate, n=40):
    """Porte jamais fermée, entrée nulle : y a-t-il une seule bascule ?"""
    gate = Gate()
    bascules = 0
    precedent = None
    for _ in range(n):
        _, h, regime = gate.forward([1.0], pression=0.0, redondance=0.0,
                                    cout_transduction=0.0)
        if precedent is not None and regime != precedent:
            bascules += 1
        precedent = regime
    return {"bascules": bascules, "regime_final": regime, "h_final": h}


PRESSION_PROTOCOLE = [0.55, 0.70, 0.85] + [0.95] * 7   # série publiée, cf. crosscheck_bgate.py


def cas_porte_fermee(Gate, n_silence=60):
    """Choc selon la série du protocole, puis entrée strictement nulle.

    La série est celle du protocole publié — et non une pression constante — pour que ce
    script reproduise exactement le couple annoncé (fermeture au pas 8, réouverture au 22).
    Une pression constante ferme au pas 7 et rendrait le chiffre publié invérifiable ici.
    """
    gate = Gate()
    fermeture = None
    for i, p in enumerate(PRESSION_PROTOCOLE, 1):
        _, _, regime = gate.forward([1.0], pression=p, redondance=0.35,
                                    cout_transduction=0.25)
        if fermeture is None and regime == "ACTIVE_SILENCE":
            fermeture = i
    reouverture = None
    for j in range(1, n_silence + 1):
        _, h, regime = gate.forward([1.0], pression=0.0, redondance=0.0,
                                    cout_transduction=0.0)
        if reouverture is None and regime == "TRANSDUCTION":
            reouverture = len(PRESSION_PROTOCOLE) + j
    return {"fermeture": fermeture, "reouverture": reouverture,
            "h_final": h, "regime_final": regime}


def main():
    ok = tableau_tailles()

    Gate = charger_classe()
    ouvert = cas_porte_ouverte(Gate)
    ferme = cas_porte_fermee(Gate)

    print()
    print("porte ouverte (p=0 des le depart)  : bascules=%d  regime=%s  h=%.4f"
          % (ouvert["bascules"], ouvert["regime_final"], ouvert["h_final"]))
    print("porte fermee puis p=0              : fermeture=%s  reouverture=%s  h=%.4f"
          % (ferme["fermeture"], ferme["reouverture"], ferme["h_final"]))

    print()
    if ferme["reouverture"] is not None:
        print("VERDICT : la porte se ROUVRE a entree nulle, %d pas apres le dernier choc,"
              % 12)
        print("          sans qu'aucune entree ne soit remontee. La formulation")
        print("          'ni bascule ni reprise' est donc fausse pour une porte fermee.")
    else:
        print("VERDICT : la porte reste fermee sous entree nulle sur %d pas." % 60)

    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
