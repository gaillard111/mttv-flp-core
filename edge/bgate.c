/* bgate.c — filtre gâté à mémoire d'hystérésis. C89-compatible, sans allocation. */
#include "bgate.h"

#define BGATE_PLAFOND(v) ((v) < 0.0 ? 0.0 : ((v) > 1.0 ? 1.0 : (v)))

void bgate_reset_memoire(bgate_t *g)
{
    g->memoire = 0.0;
    g->porosite = 1.0;
    g->cycles_silence = 0;
    g->ferme = 0;
    g->valeur = (uint8_t)BGATE_T;
}

void bgate_init(bgate_t *g)
{
    g->seuil_fermeture = 0.45;
    g->seuil_ouverture = 0.15;
    g->memoire_decay = 0.90;
    g->w_memoire = 0.85;
    g->w_redondance = 0.10;
    g->w_cout = 0.05;
    g->porosite_max = 0.20;
    g->frontiere = 0.50;
    g->derive = 0.0;
    g->seuil_courant = g->seuil_fermeture;
    g->tete = 0;
    g->nb = 0;
    bgate_reset_memoire(g);
}

bgate_regime_t bgate_step(bgate_t *g, BGATE_REAL p, BGATE_REAL r, BGATE_REAL c,
                          BGATE_REAL *h_out)
{
    BGATE_REAL h, limite_fermeture, limite_ouverture;
    int admissible, ouverte;

    p = BGATE_PLAFOND(p);
    r = BGATE_PLAFOND(r);
    c = BGATE_PLAFOND(c);

    /* mémoire paramétrique facultative : le seuil dérive avec l'exposition */
    if (g->derive > 0.0 && p > g->frontiere) {
        BGATE_REAL candidat = g->seuil_courant - g->derive;
        BGATE_REAL plancher = g->seuil_ouverture + (BGATE_REAL)BGATE_PLANCHER;
        g->seuil_courant = (candidat < plancher) ? plancher : candidat;
    }

    /* mémoire d'état : un seul flottant, décroissance exponentielle */
    g->memoire = g->memoire * g->memoire_decay + p * (1.0 - g->memoire_decay);

    h = 1.0 - (g->w_memoire * g->memoire + g->w_redondance * r + g->w_cout * c);
    h = BGATE_PLAFOND(h);

    limite_fermeture = 1.0 - g->seuil_courant;
    limite_ouverture = 1.0 - g->seuil_ouverture;

    if (g->ferme) {
        if (h > limite_ouverture) {          /* réouverture : le gain repart timidement */
            g->ferme = 0;
            g->cycles_silence = 0;
            g->porosite = (h < g->porosite_max) ? h : g->porosite_max;
        } else {                             /* période réfractaire */
            g->cycles_silence++;
            g->porosite = 0.0;
        }
    } else {
        if (h < limite_fermeture) {          /* fermeture */
            g->ferme = 1;
            g->porosite = 0.0;
            g->cycles_silence = 1;
        } else {
            g->porosite = h;                 /* le gain d'ouverture EST l'habitabilité */
        }
    }

    /* lecture à 4 états : deux questions indépendantes (milieu, membrane) */
    admissible = (p <= g->frontiere);
    ouverte = !g->ferme;
    g->valeur = admissible ? (ouverte ? BGATE_T : BGATE_B)
                           : (ouverte ? BGATE_N : BGATE_F);

#if BGATE_RING > 0
    {
        bgate_trace_t *e = &g->hist[g->tete];
        e->p = p; e->h = h; e->m = g->memoire; e->rho = g->porosite;
        e->regime = g->ferme; e->valeur = g->valeur;
        g->tete = (uint8_t)((g->tete + 1u) % BGATE_RING);
        if (g->nb < BGATE_RING) g->nb++;
    }
#endif

    if (h_out) *h_out = h;
    return g->ferme ? BGATE_SILENCE : BGATE_TRANSDUCTION;
}

size_t bgate_taille(void) { return sizeof(bgate_t); }
