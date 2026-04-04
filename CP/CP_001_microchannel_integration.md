# CP_001 — Intégration micro-canal SSD (temporaire)

**Date** : 2026-04-04 17:30
**Projet** : 03_SL_dispense_encre (Streamlit)
**Statut** : TERMINÉ

---

## Actions réalisées

- Ajout d'une section sidebar "Autres modélisations fluidiques" avec page "Micro-canal (SSD)"
- 3 tabs : Physique (capillarité, VOF/PLIC), Code (OpenFOAM 13), Résultats (7 simulations)
- Contenu bilingue FR/EN complet
- Comparaison 2-à-2 avec selectbox + GIF combiné + courbes de remplissage
- Rendu GIF en base64 (contournement bug `st.image()` dans colonnes)

## Fichiers ajoutés

- `docs/{fr,en}/microchannel/physics_microchannel.md`
- `docs/{fr,en}/microchannel/code_microchannel.md`
- `assets/microchannel/gif/` — 8 GIFs (7 cas + 1 combiné, 1.0-1.4 MB chacun)
- `assets/microchannel/png/` — 2 courbes comparatives
- `app.py` modifié (~100 lignes ajoutées)

## Architecture sidebar

```
Résultats de modélisation
  ├── 1. VOF (OpenFOAM)
  ├── 2. LBM (Palabos)
  └── 3. SPH (PySPH)
Autres modélisations fluidiques    ← NOUVEAU
  └── ► Micro-canal (SSD)          ← NOUVEAU
Annexes
  └── ...
```

## Notes

- Intégration **temporaire** : un projet Streamlit dédié sera créé quand plus de matière
- Source des données : `~/18_Fluidic/01_Micro_channel/01_SSD_2D_coupe_xz/02_Param_Study/`
- Pas de CSV mapping (simple selectbox 7 cas) — adapté au caractère temporaire
- GIFs originaux full-res conservés dans `assets/microchannel/gif/*_full.gif`
