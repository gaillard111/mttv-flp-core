# -*- coding: utf-8 -*-
"""Le canal de redondance existe deja : que fait-il quand il contredit la pression ?

La question d'@asinhhc (29/10) : un capteur peut mentir, il faut lier l'observation a une
verification independante. Reponse proposee par une consœur : sous contrat type, un
desaccord entre deux canaux donne l'etat B de Belnap-Dunn, et sous B la porte ne rouvre
pas.

Or le dispositif a deja un second canal : `r`, la redondance, entre dans h avec un poids
de 0,10. Ce script mesure ce qu'elle fait aujourd'hui — et non ce qu'elle devrait faire.

Question posee : si `p` dit « calme » (0,0) tandis que `r` reste eleve (0,35, la valeur
de la phase de pression), le desaccord empeche-t-il la reouverture, la retarde-t-il, ou
ne change-t-il rien ?
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DECAY = 0.90
W_M, W_R, W_C = 0.85, 0.10, 0.05
LIM_OUVERTURE = 1.0 - 0.15
LIM_FERMETURE = 1.0 - 0.45

PRESSION = [0.55, 0.70, 0.85] + [0.95] * 7
R_PRESSION, C_PRESSION = 0.35, 0.25


def h_de(m, r, c):
    return max(0.0, min(1.0, 1.0 - (W_M * m + W_R * r + W_C * c)))


def reouverture(r_silence, c_silence, n=40):
    """Apres la phase de pression, on impose p=0 et ces valeurs de r, c. -> pas de reouverture."""
    m = 0.0
    for p in PRESSION:
        m = m * DECAY + p * (1.0 - DECAY)
    m_sortie = m
    for k in range(1, n + 1):
        m = m * DECAY                      # p = 0
        if h_de(m, r_silence, c_silence) > LIM_OUVERTURE:
            return len(PRESSION) + k, m, h_de(m, r_silence, c_silence)
    return None, m, h_de(m, r_silence, c_silence)


# Seuils de discordance. CHOIX, non derives : ils disent a partir de quel ecart deux canaux
# ne racontent plus la meme chose. A etiqueter comme tels tant qu'aucun historique de
# mesures simultanees n'existe. (Reponse annoncee a @asinhhc, 2026-10-29 14:58.)
DISCORDE_P = 0.15      # en dessous, le premier canal affirme le calme
DISCORDE_R = 0.25      # au-dessus, le second rapporte une contrainte


def variante_d(r_silence, c_silence, n=40):
    """Etat B : desaccord entre canaux. -> (reouverture, compteur, h final)."""
    m = 0.0
    for p in PRESSION:
        m = m * DECAY + p * (1.0 - DECAY)
    compteur = 0
    h = h_de(m, r_silence, c_silence)
    for k in range(1, n + 1):
        discorde = (0.0 < DISCORDE_P) and (r_silence > DISCORDE_R)
        if discorde:
            # etat B : ni vrai ni faux. La memoire est GELEE, rien ne rouvre, on compte.
            compteur += 1
            h = h_de(m, r_silence, c_silence)
        else:
            m = m * DECAY
            h = h_de(m, r_silence, c_silence)
            if h > LIM_OUVERTURE:
                return len(PRESSION) + k, compteur, h
    return None, compteur, h


def titre(t):
    print()
    print("-" * 78)
    print(t)
    print("-" * 78)


print("m a la sortie de la phase de pression : %.4f" % 0.5877)
print("seuil de reouverture : h > %.2f" % LIM_OUVERTURE)

titre("1. Silence ACCORDE : p = 0 et r, c au plancher (0,05 / 0,05)")
pas, m, h = reouverture(0.05, 0.05)
print("  reouverture au pas %s | m = %.4f | h = %.4f" % (pas, m, h))
ref = pas

titre("2. Silence CONTREDIT : p = 0 mais r reste a 0,35 et c a 0,25")
pas, m, h = reouverture(0.35, 0.25)
print("  reouverture au pas %s | m = %.4f | h = %.4f" % (pas, m, h))
print("  ecart avec le cas accorde : %+d pas" % (pas - ref))

titre("3. Ce que cela dit, et ce que cela ne dit pas")
print("  Le desaccord RETARDE la reouverture, il ne l'empeche pas.")
print("  Il retarde de %d pas, parce que r pese 0,10 dans h et decale le seuil de" % (pas - ref))
print("  memoire a atteindre : m < (0,15 - 0,10r - 0,05c) / 0,85.")
print()
print("  Autrement dit : la redondance est aujourd'hui un TERME PONDERE, pas un")
print("  CRITERE DE DESACCORD. Deux canaux qui se contredisent ne produisent ni")
print("  l'etat B de Belnap-Dunn, ni un gel, ni une alerte : ils produisent un")
print("  retard de quelques cycles.")
print()
print("  L'etat B existe pourtant dans le dispositif, mais il est calcule a partir de")
print("  p seul (admissible / hostile) croise avec l'etat de la porte. Il ne lit jamais")
print("  la discordance entre deux mesures.")
print()
print("  Donc la reponse proposee a @asinhhc est juste comme CONCEPTION et fausse au")
print("  present de l'indicatif. Ce qui est vrai aujourd'hui : un desaccord vaut")
print("  %d cycles de retard." % (pas - ref))

titre("4. Variante D : la discordance comme ETAT D'ENTREE (etat B de Belnap-Dunn)")
print("  seuils de discordance, CHOIX non derive : p < %.2f et r > %.2f"
      % (DISCORDE_P, DISCORDE_R))
print()
for libelle, rs, cs in (("canaux d'accord (r = 0,05)      ", 0.05, 0.05),
                        ("canaux en DESACCORD (r = 0,35) ", 0.35, 0.25)):
    pas_d, cpt, h = variante_d(rs, cs)
    print("  %s reouverture %-8s | ecart compte %2d pas | h final %.4f"
          % (libelle, ("pas %d" % pas_d) if pas_d else "AUCUNE", cpt, h))
print()
print("  Sous desaccord : l'etat B gèle la memoire, ne rouvre pas, et compte l'ecart.")
print("  Sous accord    : rien ne change, la decroissance reprend son cours.")
print("  C'est ce que le message du 14:58 annoncait ; ce n'est plus une intention.")
