# -*- coding: utf-8 -*-
"""Audit contradictoire des deux graines "Post-Riemann" soumises le 2026-11-21.

Ce script ne juge pas l'intention. Il execute exactement ce que le dossier
propose, et compte. Aucune dependance, aucune ecriture, aucun acces reseau.

  M1  Le "test qui echoue" peut-il echouer ?
      On execute les asserts sur la version corrigee, puis sur la version
      fautive placee SOUS LE MEME NOM. Un vrai test doit passer dans le
      premier cas et echouer dans le second.

  M2  L'assert branche sur la version naive discrimine-t-il ?
      On substitue plusieurs implementations naives differentes.

  M3  La decision suit-elle la constante, ou la cadence ?
      Test de la graine 2 ("invariance de derivation"), deja cataloguee.

  M4  La graine A contre le garde-fou doctrinal du noyau (axe1, l.291-295).

  M5  Bornes de la partie 3, mesurees a l'ast.

Usage : python audit_graines_post_riemann.py
"""
import ast


def executer(source, nom):
    """Rend (nb_echecs, nb_asserts, exception_ou_None)."""
    espace = {}
    try:
        exec(compile(source, "<%s>" % nom, "exec"), espace)  # noqa: S102
    except AssertionError as e:
        return 1, source.count("assert "), "AssertionError: %s" % (e or "(sans message)")
    except Exception as e:  # noqa: BLE001
        return -1, source.count("assert "), "%s: %s" % (type(e).__name__, e)
    return 0, source.count("assert "), None


def lignes_instructions(source):
    lignes = len(source.strip().splitlines())
    instructions = sum(1 for x in ast.walk(ast.parse(source)) if isinstance(x, ast.stmt))
    return lignes, instructions


MUR = "-" * 74


def titre(t):
    print("\n" + MUR)
    print(t)
    print(MUR)


# ------------------------------------------------------------------ Graine A
A_CORRIGEE = '''
def evaluer_regime(porosite, viscosite, kappa_min=0.25):
    if viscosite <= 0:
        raise ValueError("Viscosite nulle invalide")
    ratio = porosite / viscosite
    if ratio < kappa_min:
        return "DORMANCE_C2"
    return "TRANSDUCTION_ACTIF"
'''

A_FAUTIVE = '''
def evaluer_regime(porosite, viscosite, kappa_min=0.25):
    return "TRANSDUCTION_ACTIF"
'''

A_ASSERTS = '''
assert evaluer_regime(0.5, 1.0) == "TRANSDUCTION_ACTIF"
assert evaluer_regime(0.1, 1.0) == "DORMANCE_C2"
naif = lambda p, v: "TRANSDUCTION_ACTIF"
assert naif(0.1, 1.0) != "DORMANCE_C2", "Echec : le systeme naif continue a l'aveugle"
'''

# ------------------------------------------------------------------ Graine B
B_CORRIGEE = '''
def interpreter_canaux(canal_a, canal_b):
    if canal_a == canal_b:
        return "VRAI" if canal_a else "FAUX"
    return "DISCORDANCE_B"
'''

B_FAUTIVE = '''
def interpreter_canaux(canal_a, canal_b):
    return (float(bool(canal_a)) + float(bool(canal_b))) / 2.0
'''

B_ASSERTS = '''
assert interpreter_canaux(True, True) == "VRAI"
assert interpreter_canaux(False, False) == "FAUX"
assert interpreter_canaux(True, False) == "DISCORDANCE_B"
agregateur_naif = lambda a, b: (float(bool(a)) + float(bool(b))) / 2.0
assert agregateur_naif(True, False) != "DISCORDANCE_B", "Echec : la moyenne masque"
'''

# ================================================================ M1
titre("M1 - le test peut-il echouer ?")

for nom, corrigee, fautive in (
    ("A dormance_rmp", A_CORRIGEE, A_FAUTIVE),
    ("B discordance_fde", B_CORRIGEE, B_FAUTIVE),
):
    asserts = A_ASSERTS if nom.startswith("A") else B_ASSERTS
    e1, n1, x1 = executer(corrigee + asserts, nom + "-corrigee")
    e2, n2, x2 = executer(fautive + asserts, nom + "-fautive")
    print("\n%s" % nom)
    print("  code corrige, asserts soumis : %d echec(s) / %d assert(s)%s"
          % (e1, n1, "   [%s]" % x1 if x1 else ""))
    print("  code fautif,  memes asserts  : %d echec(s) / %d assert(s)%s"
          % (e2, n2, "   [%s]" % x2 if x2 else ""))
    verdict = "le test mord" if e2 else "le test ne mord pas"
    print("  verdict sur la substitution  : %s" % verdict)
    if nom.startswith("A"):
        print("  MAIS 3e assert : naif(0.1, 1.0) = 'TRANSDUCTION_ACTIF' vs 'DORMANCE_C2'")
        print("                   -> vrai par construction, quel que soit le code")
    else:
        print("  MAIS 4e assert : agregateur_naif(True, False) = 0.5 vs 'DISCORDANCE_B'")
        print("                   -> flottant contre chaine : jamais egaux")

# ================================================================ M2
titre("M2 - l'assert sur la version naive discrimine-t-il ?")

NAIFS_A = [
    'lambda p, v: "TRANSDUCTION_ACTIF"',
    'lambda p, v: "AUTRE_ETAT"',
    'lambda p, v: "TRANSDUCTION_ACTIF" if p > 1e-12 else "RIEN"',
]
NAIFS_B = [
    "lambda a, b: (float(bool(a)) + float(bool(b))) / 2.0",
    "lambda a, b: max(float(bool(a)), float(bool(b)))",
    "lambda a, b: min(float(bool(a)), float(bool(b)))",
]

for nom, code, asserts, naifs, var in (
    ("A dormance_rmp", A_CORRIGEE, A_ASSERTS, NAIFS_A, "naif"),
    ("B discordance_fde", B_CORRIGEE, B_ASSERTS, NAIFS_B, "agregateur_naif"),
):
    passe = 0
    for i, expr in enumerate(naifs, 1):
        remplace = asserts.replace(
            'naif = lambda p, v: "TRANSDUCTION_ACTIF"' if var == "naif"
            else "agregateur_naif = lambda a, b: (float(bool(a)) + float(bool(b))) / 2.0",
            "%s = %s" % (var, expr),
        )
        e, _, _ = executer(code + remplace, "%s-naif%d" % (nom, i))
        passe += (e == 0)
        print("  %-18s naive %d -> %s" % (nom.split()[0], i, "passe" if e == 0 else "echoue"))
    print("  => %d / %d implementations naives passent : "
          "%s\n" % (passe, len(naifs),
                    "l'assert ne separe rien" if passe == len(naifs) else "l'assert separe"))

# ================================================================ M3
titre("M3 - la decision suit-elle la constante, ou la cadence ?")


def regime(porosite, viscosite, kappa_min):
    return "TRANSDUCTION_ACTIF" if porosite / viscosite >= kappa_min else "DORMANCE_C2"


POROSITE, VISCOSITE = 0.30, 1.00
CONSTANTES = [0.05, 0.15, 0.25, 0.35, 0.45]
etiquettes = [regime(POROSITE, VISCOSITE, k) for k in CONSTANTES]
bascules = sum(1 for a, b in zip(etiquettes, etiquettes[1:]) if a != b)
print("\n  pi/eta fige a %.2f ; seule kappa_min varie" % (POROSITE / VISCOSITE))
for k, e in zip(CONSTANTES, etiquettes):
    print("    kappa_min = %.2f -> %s" % (k, e))
print("  basculements                : %d / %d reglages" % (bascules, len(CONSTANTES)))
print("  parametres de cadence       : 0 (aucun pas, aucune decroissance, aucun temps)")
print("  => decision = fonction pure de la constante : c'est le defaut de la graine 2")

# ================================================================ M4
titre("M4 - la graine A contre le garde-fou doctrinal du noyau")

PI_DORMANT, ETA_REF, SEUIL_PRESSION_ETA = 0.12, 0.95, 0.10
kappa_t = PI_DORMANT / ETA_REF
eta_requise = ETA_REF * (1.0 + SEUIL_PRESSION_ETA)
print("\n  etat dormant : pi = %.2f, eta = %.2f (a sa reference, non pressee)"
      % (PI_DORMANT, ETA_REF))
print("  kappa_t = pi/eta                 = %.4f" % kappa_t)
print("  graine A (kappa_min = 0.25)      -> %s   [refus declare]"
      % regime(PI_DORMANT, ETA_REF, 0.25))
print("  noyau (kappa_min = 0.15) + garde-fou -> critere kappa %s"
      % ("ACTIF" if ETA_REF > eta_requise else "INACTIF  [pas de refus]"))
print("  eta exigee par le garde-fou      = %.3f ; eta courante = %.2f" % (eta_requise, ETA_REF))
print("  => la graine A declare en faute un etat que le noyau protege nommement")

# ================================================================ M5
titre("M5 - bornes de la partie 3, mesurees")
for nom, src in (("A dormance_rmp", A_CORRIGEE), ("B discordance_fde", B_CORRIGEE)):
    l, i = lignes_instructions(src)
    print("  %-18s %3d lignes / %2d instructions (ast)" % (nom, l, i))
print("\n  borne en vigueur dans le depot : <= 170 lignes et <= 85 instructions")
print("  borne citee par le dossier     : <= 40 lignes (retiree le 2026-10-31)")

print("\n" + MUR)
print("FIN - aucune de ces mesures ne porte sur l'intention des deux graines.")
print(MUR)
