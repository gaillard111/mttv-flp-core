# -*- coding: utf-8 -*-
"""Une horloge, deux metiers.

1. LA PHRASE
   Pendant l'aveuglement, l'horloge interne est arretee. Mesurer un silence en
   demi-vies, c'est mesurer avec une horloge qui ne tourne pas : le meme seuil de
   vingt cycles declare une panne apres dix cycles de silence si decay vaut 0.80,
   et apres deux cent sept si decay vaut 0.99 — sans que le capteur ait change.

2. LE CHIFFRE
   python3 graines/graine_une_horloge_deux_metiers.py
   Sous le seuil, l'aveuglement coute exactement sa duree, pas davantage :
   reouverture au pas 22 sans absence, au pas 41 apres 19 pas d'aveuglement.
   La pente vaut 1. Au-dessus du seuil : aucune reouverture, jamais.

3. LE CODE  (ci-dessous, aucune dependance, aucune constante importee)

4. LE TEST QUI ECHOUE
   `assert pannes_a_080 == pannes_a_099`  echoue des que le seuil est derive de
   tau_m : cinquante pas d'absence declarent une panne a 0.80 et n'en declarent
   aucune a 0.99. Il passe quand le seuil vient de la cadence du capteur.

5. OU CA MORD
   Delais d'expiration de cache, disjoncteurs TTL, heartbeat watchers, sondes de
   liveness. Partout ou l'on ecrit « expire en trois fois la demi-vie » alors que
   la demi-vie appartient au systeme qui cicatrise et le silence au systeme qui
   parle.
"""
import math

W_M, W_R, W_C = 0.85, 0.10, 0.05
LIM_FERMETURE, LIM_OUVERTURE = 0.55, 0.85
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
MANQUES = 3          # CHOIX, non derive : trois lectures manquees tolerees


def seuil_cadence(cadence, manques=MANQUES):
    """Horloge externe. Ni decay, ni m, ni h dans la signature : c'est l'invariant."""
    return manques * cadence


def seuil_demi_vies(decay, demi_vies=MANQUES):
    """Horloge interne. C'est celle-ci qu'on accuse."""
    return int(math.ceil(demi_vies * math.log(0.5) / math.log(decay)))


def course(decay, seuil, absence, n_apres=60):
    """-> (pas de fermeture, pas de reouverture ou None, escalade)."""
    m, ferme, esc, manques, pas = 0.0, False, False, 0, 0
    fermeture = reouverture = None
    for p in PRESSION:
        pas += 1
        m = m * decay + p * (1.0 - decay)
        h = 1.0 - (W_M * m + W_R * 0.35 + W_C * 0.25)
        if not ferme and h < LIM_FERMETURE:
            ferme, fermeture = True, pas
    for _ in range(absence):
        pas += 1
        manques += 1
        if manques >= seuil:
            esc = True
        # m est GELE : l'horloge interne ne tourne pas pendant l'aveuglement.
        # C'est tout le sujet : on ne peut pas compter des demi-vies qui n'ont pas lieu.
    for _ in range(n_apres):
        pas += 1
        m = m * decay
        h = 1.0 - (W_M * m + W_R * 0.05 + W_C * 0.05)
        if ferme and h > LIM_OUVERTURE and not esc:
            ferme, reouverture = False, pas
    return fermeture, reouverture, esc


def main():
    f, r0, _ = course(0.90, seuil_cadence(1), 0)
    assert (f, r0) == (8, 22), "reference : fermeture 8, reouverture 22, mesure %s" % ((f, r0),)

    delais = []
    for absence in (0, 5, 19):
        _, r, esc = course(0.90, seuil_cadence(1) * 7, absence)   # seuil 21 > 19
        assert esc is False and r is not None
        delais.append(r - f)
    # Pente exactement 1 : l'aveuglement coute sa duree, pas une cicatrice en plus.
    assert delais == [14, 19, 33], "delais mesures : %s" % (delais,)

    # LE DEFAUT : le seuil pris sur l'horloge interne.
    _, _, panne_080 = course(0.80, seuil_demi_vies(0.80), 50)   # seuil 10
    _, _, panne_099 = course(0.99, seuil_demi_vies(0.99), 50)   # seuil 207
    assert panne_080 != panne_099, "le defaut doit faire varier la panne avec decay"

    # LA CORRECTION : le seuil pris sur l'horloge externe.
    _, _, panne_a = course(0.80, seuil_cadence(1), 50)          # seuil 3
    _, _, panne_b = course(0.99, seuil_cadence(1), 50)          # seuil 3
    assert panne_a and panne_b, "le capteur decide, la memoire non"

    print("Une horloge, deux metiers")
    print("  seuil via tau_m   : 0.80 -> %3d cycles | 0.99 -> %3d cycles"
          % (seuil_demi_vies(0.80), seuil_demi_vies(0.99)))
    print("  seuil via cadence : 1 -> %3d cycles | 10 -> %3d cycles"
          % (seuil_cadence(1), seuil_cadence(10)))
    print("  delais de reouverture pour absence 0 / 5 / 19 : %s" % (delais,))
    print("  50 pas d'absence, seuil sur tau_m : panne a 0.80 = %s, a 0.99 = %s"
          % (panne_080, panne_099))
    print("  50 pas d'absence, seuil sur cadence : panne a 0.80 = %s, a 0.99 = %s"
          % (panne_a, panne_b))
    print("  chaine de detection : HORLOGE_DEUX_METIERS")


if __name__ == "__main__":
    main()
