# CP_002 — Intégration encapsulation COB (temporaire)

**Date** : 2026-04-04 18:45
**Projet** : 03_SL_dispense_encre (Streamlit)
**Statut** : TERMINÉ

---

## Actions réalisées

- Ajout page "Encapsulation (COB)" dans section "Autres modélisations fluidiques"
- 3 tabs : Physique (Bird-Carreau, COB, nombres sans dimension), Code (OpenFOAM v2406), Résultats (9 cas)
- Contenu bilingue FR/EN complet
- Géométrie + photo glob top en haut de l'onglet Physique
- Comparaison 2-à-2 avec selectbox + rendu GIF base64

## Architecture sidebar mise à jour

```
Résultats de modélisation
  ├── 1. VOF (OpenFOAM)
  ├── 2. LBM (Palabos)
  └── 3. SPH (PySPH)
Autres modélisations fluidiques
  ├── ► Micro-canal (SSD)
  └── ► Encapsulation (COB)      ← NOUVEAU
Annexes
  └── ...
```

## Notes

- Source : `~/17_RD_Ag_AgCl/70_Encapsulation/` (38 cas, 9 sélectionnés)
- Intégration temporaire, même principe que le micro-canal
