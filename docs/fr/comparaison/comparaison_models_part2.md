---

## 3. Analyse critique par modèle

### 3.1 VOF (Volume of Fluid)

Méthode eulérienne où chaque cellule contient une fraction volumique $\alpha \in [0,1]$. L'interface est reconstruite géométriquement via l'algorithme PLIC (Piecewise Linear Interface Construction).

| Avantages | Limitations |
|-----------|-------------|
| Conservation de masse rigoureuse | Diffusion numérique aux interfaces fines |
| Standard industriel depuis 30 ans | Coût mémoire pour maillages fins |
| Documentation et communauté étendues | Coalescence de gouttes difficile |
| Logiciels : OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.2 LBM (Lattice Boltzmann Method)

Méthode mésoscopique résolvant l'équation de Boltzmann discrétisée sur grille régulière (D2Q9, D3Q19). Les grandeurs macroscopiques (vitesse, pression) sont obtenues par calcul des moments statistiques.

| Avantages | Limitations |
|-----------|-------------|
| Parallélisation GPU exceptionnelle (facteur ×10-20) | Compressibilité artificielle (contrainte Ma < 0.1) |
| Algorithme local (chaque nœud indépendant) | Précision sub-micronique difficile |
| Pas de maillage complexe à générer | Calibration rhéologique délicate |
| Logiciels : Palabos, waLBerla (open-source) | Documentation moins fournie que VOF |

---

### 3.3 SPH (Smoothed Particle Hydrodynamics)

Méthode lagrangienne sans maillage. Le fluide est discrétisé en particules dont les propriétés sont interpolées via des noyaux de lissage (cubic spline, Wendland). Il est optimisé pour le calcul GPU et principalement conçu pour les écoulements à surface libre (interactions fluide-structure, ingénierie côtière, vagues).

| Avantages | Limitations |
|-----------|-------------|
| Pas de maillage : pas de problème de distorsion | Bruit numérique dans les champs de pression |
| Coalescence et fragmentation naturelles | Instabilités tensorielles à haute vitesse |
| Adapté aux grandes déformations | Maturité industrielle moindre |
| Logiciels : PySPH (Python), DualSPHysics (C++/CUDA)| Coût mémoire élevé en 3D |

---

## 4. Besoins hardware

### 4.1 Temps de calcul (simulations de ce projet)

Les temps ci-dessous correspondent au cas de référence : dispense d'une goutte dans un micro-via (domaine 1.2×0.5 mm, 100-200 ms de temps physique), PC standard 8 cœurs.

| Modèle | Discrétisation | Résolution | Temps | Remarques |
|--------|----------------|------------|-------|-----------|
| **VOF** | ~50k cellules | ~5 µm | **0.5-2 h** | OpenFOAM optimisé C++ |
| **LBM** | 240×100 nœuds | 5 µm | **~10 min** | Parallélisation efficace (GPU) |
| **SPH** | ~1k particules | 15-20 µm | **1-2 h** | PySPH |

### 4.2 Configurations indicatives

| Gamme | Configuration type | Budget indicatif | Utilisation |
|-------|-------------------|------------------|-------------|
| **PC standard** | 6-12 cœurs, 16-32 Go RAM | 800-1 500 € | VOF/LBM simples, SPH 2D, FEM 2D|
| **PC dopé** | 12-16 cœurs, 32-64 Go RAM, GPU 8 Go | 1 500-3 000 € | VOF 3D, études paramétriques |
| **Serveur** | 32+ cœurs, 128+ Go RAM | 5 000-15 000 € | grandes séries d'études |
| **Cloud** | AWS, Google Cloud, Azure | 1-5 €/h | Pour calculs ponctuels intensifs |

### 4.3 Remarques pratiques

- **LBM** exploite efficacement les GPU : une carte graphique grand public accélère significativement les calculs.
- **VOF** tourne sur des PC standards pour des cas 2D
- Le cloud peut être utile pour des études 3D ou des grandes séries paramétriques.

---

## 5. Tableau de synthèse

| Critère | VOF | LBM | SPH |
|---------|-----|-----|-----|
| **Précision interface** | 0.1-1 µm | 0.2-2 µm | 0.5-5 µm |
| **Temps par simulation unitaire (ce projet)** | 0.5-2 h | ~10 min | 1-2 h |
| **Conservation masse** | Rigoureuse | Approximative | Par sommation |
| **Rhéologie Carreau** | Natif | Implémentable | Implémentable |
| **Courbe d'apprentissage** | Élevée (C++, CLI) | Élevée (physique spécifique) | Moyenne (Python) |
| **Maturité industrielle** | Très haute | Moyenne | En développement |
| **Coût logiciel** | OpenFOAM gratuit | Palabos gratuit | PySPH gratuit |

### Recommandations selon le contexte applicatif

| Contexte | Méthode recommandée | Justification |
|----------|---------------------|---------------|
| Industrie | VOF (OpenFOAM) | Robustesse éprouvée, large communauté |
| Études paramétriques intensives | LBM (Palabos) | Performance GPU optimale |
| Recherche fondamentale | SPH (PySPH) | Flexibilité pour nouvelles physiques |

---

## 6. Références bibliographiques

> Pour la liste complète des références scientifiques, consulter la section **Références bibliographiques** dans le menu Annexes.
