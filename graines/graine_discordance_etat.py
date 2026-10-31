# -*- coding: utf-8 -*-
"""Discordance = etat.

1. LA PHRASE
   Un desaccord entre deux canaux n'est pas un veto, c'est un tarif : le second canal
   pese 0,10 dans h, donc une contradiction franche ne fait que retarder la reouverture
   de quelques cycles — et ce nombre de cycles depend du poids qu'on a bien voulu lui
   donner. Un tarif n'est pas une mesure : il ne signale rien, il facture.

2. LE CHIFFRE
   python3 graines/graine_discordance_etat.py
   canaux d'accord  (r = 0,05) -> reouverture au pas 22
   desaccord modere (r = 0,35) -> pas 26    (+4)
   desaccord franc  (r = 0,95) -> pas 34    (+12)
   Jamais AUCUNE : le desaccord ne bloque pas, il decale. Et l'ecart suit le poids,
   ce qui est la marque d'un reglage, non d'un constat.

3. LE CODE  (ci-dessous, aucune dependance)

4. LE TEST QUI ECHOUE
   `assert reouverture(0.35, 0.25) is None` echoue : la porte rouvre au pas 26. La
   phrase « un desaccord produit l'etat B et sous B la porte ne rouvre pas » decrit
   une intention, pas le comportement. La correction n'est pas d'augmenter le poids
   de r — ce serait acheter plus cher le meme silence — mais de faire du desaccord
   un ETAT qui gele la memoire au lieu de la ponderer.

5. OU CA MORD
   Fusion de capteurs redondants, caches a verification secondaire, quorums avec poids
   d'arbitrage, sondes de liveness croisees : partout ou l'on croit detecter une
   contradiction et ou l'on ne fait qu'en fixer le prix en cycles.
"""
DECAY = 0.90
W_M, W_R, W_C = 0.85, 0.10, 0.05
LIM_OUVERTURE = 0.85
PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25
DISCORDE_R = 0.25            # CHOIX, non derive : au-dela, les canaux se contredisent


def h_de(m, r, c):
    return 1.0 - (W_M * m + W_R * r + W_C * c)


def m_de_sortie():
    m = 0.0
    for p in PRESSION:
        m = m * DECAY + p * (1.0 - DECAY)
    return m


def reouverture(r, c, n=40):
    """Etat actuel : le desaccord entre comme un terme pondere. -> pas de reouverture."""
    m = m_de_sortie()
    for k in range(1, n + 1):
        m = m * DECAY
        if h_de(m, r, c) > LIM_OUVERTURE:
            return len(PRESSION) + k
    return None


def etat_b(r, c, n=40):
    """Correction : sous desaccord, la memoire est GELEE. -> (pas, compteur, h)."""
    m = m_de_sortie()
    compteur = 0
    h = h_de(m, r, c)
    for k in range(1, n + 1):
        if r > DISCORDE_R:
            compteur += 1
            continue                       # rien ne decroit, rien ne rouvre, on compte
        m = m * DECAY
        h = h_de(m, r, c)
        if h > LIM_OUVERTURE:
            return len(PRESSION) + k, compteur, h
    return None, compteur, h


def main():
    accord = reouverture(0.05, 0.05)
    modere = reouverture(0.35, 0.25)
    franc = reouverture(0.95, 0.25)
    assert accord == 22, "reference : reouverture au pas 22, mesure %s" % accord
    assert (modere, franc) == (26, 34), "tarifs mesures : %s, %s" % (modere, franc)
    assert modere is not None and franc is not None, "un desaccord ne bloque jamais"

    pas_b, cpt_b, h_b = etat_b(0.35, 0.25)
    assert pas_b is None and cpt_b == 40, "etat B : aucune reouverture, 40 pas comptes"
    assert abs(h_b - 0.4529) < 1e-4, "h gele : 0.4529, mesure %.4f" % h_b

    pas_c, cpt_c, _ = etat_b(0.05, 0.05)
    assert (pas_c, cpt_c) == (22, 0), "sous accord, rien ne change : %s / %s" % (pas_c, cpt_c)

    print("Discordance = etat")
    print("  canaux d'accord  (r = 0.05) -> reouverture pas %d" % accord)
    print("  desaccord modere (r = 0.35) -> pas %d  (%+d)" % (modere, modere - accord))
    print("  desaccord franc  (r = 0.95) -> pas %d  (%+d)" % (franc, franc - accord))
    print("  etat B (r = 0.35)           -> reouverture %s | ecart compte %d | h %.4f"
          % ("AUCUNE" if pas_b is None else pas_b, cpt_b, h_b))
    print("  etat B (r = 0.05)           -> reouverture pas %d | ecart compte %d"
          % (pas_c, cpt_c))
    print("  chaine de detection : DISCORDE_R_EGAL_0_25")


if __name__ == "__main__":
    main()
