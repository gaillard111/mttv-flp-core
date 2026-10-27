/*
 * bgate.h — filtre gâté à mémoire d'hystérésis, portage C de référence.
 *
 * État BORNÉ, taille fixe, aucune allocation dynamique, aucun pointeur possédé.
 * `bgate_t` peut vivre en statique, sur la pile, ou dans une section dédiée.
 *
 * Licence : CC-BY-NC-SA 4.0 — Collectif Les Fils de la Pensée.
 */
#ifndef BGATE_H
#define BGATE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Profondeur du journal d'état (tampon circulaire). Mettre 0 supprime le journal :
 * la décision est inchangée, seule la trace disparaît. */
#ifndef BGATE_RING
#define BGATE_RING 8u
#endif

/* Type de calcul. `double` reproduit le prototype Python à la 4e décimale ;
 * `float` divise l'empreinte par deux au prix d'un écart mesurable (voir README). */
#ifndef BGATE_REAL
#define BGATE_REAL double
#endif

#define BGATE_PLANCHER 0.02   /* marge : le seuil de fermeture ne rejoint jamais celui d'ouverture */

typedef enum { BGATE_TRANSDUCTION = 0, BGATE_SILENCE = 1 } bgate_regime_t;
typedef enum { BGATE_T = 0, BGATE_F = 1, BGATE_B = 2, BGATE_N = 3 } bgate_valeur_t;

typedef struct {
    BGATE_REAL p, h, m, rho;      /* entrée, habitabilité, mémoire d'état, gain */
    uint8_t regime, valeur;       /* régime binaire + lecture à 4 états */
} bgate_trace_t;

typedef struct {
    /* paramètres */
    BGATE_REAL seuil_fermeture;   /* 0,45 : ferme quand h < 1 - seuil (0,55) */
    BGATE_REAL seuil_ouverture;   /* 0,15 : rouvre seulement quand h > 1 - seuil (0,85) */
    BGATE_REAL memoire_decay;     /* 0,90 : décroissance par cycle */
    BGATE_REAL w_memoire, w_redondance, w_cout;  /* 0,85 / 0,10 / 0,05 (somme = 1) */
    BGATE_REAL porosite_max;      /* 0,20 : plafond du gain à la réouverture */
    BGATE_REAL frontiere;         /* 0,50 : admissibilité du milieu — choix doctrinal */
    BGATE_REAL derive;            /* 0,00 : >0 rend la mémoire paramétrique */

    /* état — tout est de taille fixe */
    BGATE_REAL memoire, porosite, seuil_courant;
    uint32_t cycles_silence;
    uint8_t ferme, valeur, tete, nb;
#if BGATE_RING > 0
    bgate_trace_t hist[BGATE_RING];
#endif
} bgate_t;

void            bgate_init(bgate_t *g);
void            bgate_reset_memoire(bgate_t *g);   /* mémoire cinétique seule */
bgate_regime_t  bgate_step(bgate_t *g, BGATE_REAL pression, BGATE_REAL redondance,
                           BGATE_REAL cout, BGATE_REAL *habitabilite);
size_t          bgate_taille(void);

#ifdef __cplusplus
}
#endif
#endif /* BGATE_H */
