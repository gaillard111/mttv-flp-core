/* test_bgate.c — rejoue les scénarios A et B du protocole et imprime les grandeurs
 * publiées : pas de fermeture, pas de réouverture, m8/h8/m10/h10, taille de l'état.
 * Sortie comparable ligne à ligne avec edge/crosscheck_bgate.py. */
#include <stdio.h>
#include "bgate.h"

#define PRESSION_N 10

static const BGATE_REAL pris_p[PRESSION_N] = {0.55, 0.70, 0.85, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95};

int main(void)
{
    bgate_t g;
    int i, fermeture = 0, reouverture = 0;
    /* BGATE_REAL et non double : en variante `float`, passer un double* à
     * bgate_step() ecrirait 4 octets dans un double et lirait du vide.
     * C'est le piege que la premiere execution a revele (h8 = 0.0000). */
    BGATE_REAL m8 = 0.0, h8 = 0.0, m10 = 0.0, h10 = 0.0;

    bgate_init(&g);
    for (i = 1; i <= PRESSION_N; i++) {
        BGATE_REAL h = 0.0;
        bgate_step(&g, pris_p[i - 1], 0.35, 0.25, &h);
        /* g.memoire est l'état APRES le pas : lisible meme si BGATE_RING = 0,
         * ce qui permet de mesurer l'empreinte sans journal. */
        if (i == 8) { m8 = g.memoire; h8 = h; }
        if (i == 10) { m10 = g.memoire; h10 = h; }
        if (!fermeture && g.ferme) fermeture = i;
    }
    for (i = 1; i <= 18; i++) {
        bgate_step(&g, 0.0, 0.05, 0.05, NULL);
        if (!reouverture && !g.ferme) reouverture = PRESSION_N + i;
    }

    printf("fermeture=%d\n", fermeture);
    printf("reouverture=%d\n", reouverture);
    printf("m8=%.4f\n", m8);
    printf("h8=%.4f\n", h8);
    printf("m10=%.4f\n", m10);
    printf("h10=%.4f\n", h10);
    printf("cycles_silence=%u\n", (unsigned)g.cycles_silence);
    printf("valeur_B=%u\n", (unsigned)g.valeur);
    printf("taille_etat=%u\n", (unsigned)bgate_taille());
    return 0;
}
