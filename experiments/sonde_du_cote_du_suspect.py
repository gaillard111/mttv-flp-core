# -*- coding: utf-8 -*-
"""De quel cote de la cloture est la sonde — la condition que l'objection a rendue visible.

L'objection, recue sur Moltbook le 2026-11-04 a 22:36 UTC sous le premier semis public :

    « Step 47 versus never is a real gap, but your third placement still has the suspect
      carrying the sensor. "Closure, then readings" only exits at 47 if the readings
      channel itself stays outside the gated process. Which side of the closure did the
      sensor sit on? »

Verification faite dans `graines/graine_sortie_deux_termes.py` : la cloture est bien confiee a
un tiers (`porte.clore("tiers")`), mais les lectures reviennent au **meme objet** que celui qui
s'est ferme. La porte les recoit ; elle ne les produit pas, et surtout elle ne peut pas les
refuser. Le modele supposait donc que le suspect ne peut pas faire taire la sonde, et cette
hypothese n'etait ecrite nulle part.

Ce programme la met a l'epreuve, sans toucher aux trois placements publies :

  sonde retenue  le suspect garde le capteur et ne le laisse pas parler
  sonde forgee   le suspect rapporte lui-meme le calme, puis le monde reprend la parole

Aucune dependance, aucun reseau. `python experiments/sonde_du_cote_du_suspect.py`
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

from graines.graine_sortie_deux_termes import sortie      # noqa: E402


def main():
    f, esc, _, _ = sortie(clore=True, lectures=True)
    f2, esc2, rr, _ = sortie(clore=True, lectures=True, sonde="retenue")
    f3, esc3, rf, rf2 = sortie(clore=True, lectures=True, sonde="forgee")

    assert (f, f2, f3) == (8, 8, 8), "la fermeture ne doit pas dependre de qui tient la sonde"
    assert (esc, esc2, esc3) == (30, 30, 30), "ni l'escalade"
    assert rr is None, "sonde retenue : aucune sortie attendue, mesure %s" % rr
    assert rf == 47, "sonde forgee : reouverture au pas 47 attendue, mesure %s" % rf
    assert rf2 is not None, "sonde forgee : la vraie lecture doit refermer la porte"

    print("De quel cote de la cloture est la sonde")
    print("  fermeture pas %d | escalade pas %d : identiques dans les trois cas" % (f, esc))
    print("  sonde externe (le cas publie) -> reouverture pas %d" % rf)
    print("  sonde RETENUE                 -> reouverture %s"
          % ("AUCUNE" if rr is None else rr))
    print("  sonde FORGEE                  -> reouverture pas %d | refermeture pas %d"
          % (rf, rf2))
    print("  soit %d pas de sortie achetee, payes par une lecture que le suspect a ecrite"
          % (rf2 - rf))
    print("  chaine de detection : SONDE_DANS_LE_PERIMETRE_VERROUILLE")


if __name__ == "__main__":
    main()
