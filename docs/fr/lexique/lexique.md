**Sommaire :**

**A. Physique**

1. Unités SI et préfixes
2. Nombres adimensionnels
3. Symboles physiques
4. Termes de rhéologie
5. Termes de mécanique des fluides

**B. Méthodes numériques**

6. Acronymes des méthodes
7. Acronymes des schémas numériques
8. Termes numériques
9. Logiciels et bibliothèques

**C. Hardware et formats**

10. Acronymes hardware
11. Formats de fichiers et données

**D. Techniques et applications**

12. Procédés de dispense
13. Caractérisation expérimentale
14. Couplages et intelligence artificielle

---

# A. Physique

## 1. Unités SI et préfixes

| Grandeur | Unité | Symbole |
|----------|-------|---------|
| Longueur | mètre | m |
| Masse | kilogramme | kg |
| Temps | seconde | s |
| Force | newton | N |
| Pression | pascal | Pa |
| Viscosité dynamique | pascal-seconde | Pa·s |
| Tension superficielle | newton par mètre | N/m |
| Énergie | joule | J |
| Puissance | watt | W |

### Préfixes

| Préfixe | Symbole | Facteur |
|---------|---------|---------|
| micro | µ | 10$^{-6}$ |
| milli | m | 10$^{-3}$ |
| kilo | k | 10$^{3}$ |
| méga | M | 10$^{6}$ |
| giga | G | 10$^{9}$ |
| téra | T | 10$^{12}$ |

---

## 2. Nombres adimensionnels

| Symbole | Nom | Expression | Signification physique |
|---------|-----|------------|------------------------|
| $Re$ | Reynolds | $\frac{\rho v L}{\eta}$ | Inertie / Viscosité |
| $We$ | Weber | $\frac{\rho v^2 L}{\sigma}$ | Inertie / Tension superficielle |
| $Oh$ | Ohnesorge | $\frac{\eta}{\sqrt{\rho \sigma L}}$ | Viscosité / (Inertie × Capillarité)$^{1/2}$ |
| $Ca$ | Capillaire | $\frac{\eta v}{\sigma}$ | Viscosité / Capillarité |
| $Bo$ | Bond | $\frac{\rho g L^2}{\sigma}$ | Gravité / Capillarité |
| $De$ | Deborah | $\lambda \dot{\gamma}$ | Temps de relaxation × Taux de cisaillement |
| $Ma$ | Mach | $\frac{v}{c_s}$ | Vitesse / Vitesse du son |

---

## 3. Symboles physiques

### Propriétés des fluides

| Symbole | Nom | Unité SI |
|---------|-----|----------|
| $\rho$ | Masse volumique | kg/m³ |
| $\eta$, $\mu$ | Viscosité dynamique | Pa·s |
| $\nu$ | Viscosité cinématique | m²/s |
| $\sigma$ | Tension superficielle | N/m |
| $\theta$ | Angle de contact | ° ou rad |

### Paramètres rhéologiques

| Symbole | Nom | Modèle | Unité |
|---------|-----|--------|-------|
| $\eta_0$ | Viscosité au repos | Carreau | Pa·s |
| $\eta_\infty$ | Viscosité à cisaillement infini | Carreau | Pa·s |
| $\lambda$ | Temps de relaxation | Carreau, Oldroyd-B | s |
| $n$ | Indice de comportement | Loi de puissance | - |
| $K$ | Consistance | Loi de puissance | Pa·s$^n$ |
| $\tau_0$ | Contrainte seuil | Herschel-Bulkley | Pa |
| $\dot{\gamma}$ | Taux de cisaillement | Tous | s$^{-1}$ |

### Variables d'écoulement

| Symbole | Nom | Unité |
|---------|-----|-------|
| $\mathbf{v}$, $\mathbf{u}$ | Vecteur vitesse | m/s |
| $p$ | Pression | Pa |
| $\mathbf{D}$ | Tenseur des taux de déformation | s$^{-1}$ |
| $\boldsymbol{\tau}$ | Tenseur des contraintes | Pa |
| $\kappa$ | Courbure de l'interface | m$^{-1}$ |

---

## 4. Termes de rhéologie

| Terme | Définition |
|-------|------------|
| **Rhéofluidifiant** | Fluide dont la viscosité diminue avec le cisaillement (shear-thinning) |
| **Rhéoépaississant** | Fluide dont la viscosité augmente avec le cisaillement (shear-thickening) |
| **Thixotropie** | Dépendance temporelle de la viscosité (restructuration) |
| **Viscoélasticité** | Comportement combinant viscosité et élasticité |
| **Fluide newtonien** | Viscosité constante indépendante du cisaillement |
| **Fluide non-newtonien** | Viscosité dépendante du cisaillement |
| **Yield stress** | Contrainte seuil d'écoulement |

---

## 5. Termes de mécanique des fluides

| Terme | Définition |
|-------|------------|
| **Écoulement diphasique** | Écoulement impliquant deux phases (ex: liquide/gaz) |
| **Interface** | Surface de séparation entre deux phases |
| **Capillarité** | Phénomène lié à la tension superficielle |
| **Mouillage** | Interaction fluide-solide caractérisée par l'angle de contact |
| **Ménisque** | Courbure de l'interface au contact d'une paroi |
| **Pincement** | Rétrécissement du filament avant rupture |
| **Satellite** | Goutte secondaire formée lors de la rupture |
| **Coalescence** | Fusion de deux gouttes |

---

# B. Méthodes numériques

## 6. Acronymes des méthodes

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **FEM** | Finite Element Method | Méthode des éléments finis |
| **VOF** | Volume of Fluid | Méthode de suivi d'interface eulérienne |
| **LBM** | Lattice Boltzmann Method | Méthode de Boltzmann sur réseau |
| **SPH** | Smoothed Particle Hydrodynamics | Hydrodynamique des particules lissées |
| **CFD** | Computational Fluid Dynamics | Mécanique des fluides numérique |
| **DNS** | Direct Numerical Simulation | Simulation numérique directe |

---

## 7. Acronymes des schémas numériques

| Acronyme | Signification | Contexte |
|----------|---------------|----------|
| **PLIC** | Piecewise Linear Interface Calculation | Reconstruction d'interface VOF |
| **CSF** | Continuum Surface Force | Modèle de tension superficielle |
| **BGK** | Bhatnagar-Gross-Krook | Opérateur de collision LBM |
| **MRT** | Multiple Relaxation Time | Schéma LBM multi-relaxation |
| **SUPG** | Streamline Upwind Petrov-Galerkin | Stabilisation FEM convection |
| **PSPG** | Pressure Stabilizing Petrov-Galerkin | Stabilisation FEM pression |
| **GLS** | Galerkin Least-Squares | Stabilisation FEM combinée |
| **ALE** | Arbitrary Lagrangian-Eulerian | Maillage mobile |
| **AMR** | Adaptive Mesh Refinement | Maillage adaptatif |
| **CFL** | Courant-Friedrichs-Lewy | Condition de stabilité temporelle (Co = vΔt/Δx ≤ 1) |
| **MULES** | Multidimensional Universal Limiter | Limiteur OpenFOAM pour VOF |
| **DFSPH** | Divergence-Free Smoothed Particle Hydrodynamics | Solveur SPH incompressible (Bender & Koschier 2015) |

---

## 8. Termes numériques

| Terme | Définition |
|-------|------------|
| **Eulérien** | Référentiel fixe (grille fixe) |
| **Lagrangien** | Référentiel mobile (suit les particules) |
| **Maillage** | Discrétisation spatiale du domaine |
| **Sans maillage (meshless)** | Méthode sans connectivité fixe (ex: SPH) |
| **Formulation faible** | Forme intégrale des équations (éléments finis) |
| **Fonction test** | Fonction de pondération en formulation faible |
| **DOF** | Degrees of Freedom (degrés de liberté) |
| **Condition inf-sup** | Critère de stabilité LBB pour éléments mixtes |

---

## 9. Logiciels et bibliothèques

| Nom | Type | Langage | Méthode |
|-----|------|---------|---------|
| **FEniCS** | Open-source | Python/C++ | FEM |
| **Firedrake** | Open-source | Python/C++ | FEM automatisé |
| **UFL** | Open-source | Python | Unified Form Language (syntaxe variationnelle FEniCS/Firedrake) |
| **SfePy** | Open-source | Python | FEM multiphysique |
| **FiPy** | Open-source | Python | FVM, Phase-Field |
| **Dedalus** | Open-source | Python | Méthodes spectrales |
| **OpenFOAM** | Open-source | C++ | VOF, FVM |
| **Palabos** | Open-source | C++ | LBM |
| **PySPH** | Open-source | Python | SPH |
| **COMSOL** | Commercial | GUI/MATLAB | FEM multiphysique |
| **Ansys Fluent** | Commercial | GUI | VOF, FVM |
| **DualSPHysics** | Open-source | C++/CUDA | SPH GPU |
| **SPlisHSPlasH** | Open-source | C++/CUDA | SPH GPU (solveur DFSPH, tension de surface Akinci 2013) |
| **waLBerla** | Open-source | C++ | LBM HPC |

---

# C. Hardware et formats

## 10. Acronymes hardware

| Acronyme | Signification | Description |
|----------|---------------|-------------|
| **CPU** | Central Processing Unit | Processeur central |
| **GPU** | Graphics Processing Unit | Processeur graphique |
| **HPC** | High Performance Computing | Calcul haute performance |
| **CUDA** | Compute Unified Device Architecture | API GPU NVIDIA |
| **MPI** | Message Passing Interface | Parallélisation distribuée |
| **OpenMP** | Open Multi-Processing | Parallélisation mémoire partagée |
| **TFLOPS** | Tera Floating-Point Operations Per Second | Unité de puissance de calcul |
| **RAM** | Random Access Memory | Mémoire vive |

## 11. Formats de fichiers et données

| Extension | Signification | Description |
|-----------|---------------|-------------|
| **XML** | eXtensible Markup Language | Fichier de configuration structuré (paramètres Palabos) |
| **CSV** | Comma-Separated Values | Fichier tabulaire texte (mappings paramètres → résultats) |
| **JSON** | JavaScript Object Notation | Format d'échange de données structurées (configurations) |
| **GIF** | Graphics Interchange Format | Image animée (animations de simulation) |
| **PNG** | Portable Network Graphics | Image sans perte (états finaux) |
| **JPG/JPEG** | Joint Photographic Experts Group | Image compressée avec perte |
| **SVG** | Scalable Vector Graphics | Image vectorielle |
| **STL** | STereoLithography | Maillage surfacique 3D (triangles) |
| **MSH** | GMSH Mesh | Maillage volumique généré par GMSH |
| **GEO** | GMSH Geometry | Script de géométrie GMSH (définition du domaine et du maillage) |
| **VTK/VTI/VTU/VTP** | Visualization Toolkit | Formats ParaView pour post-traitement (grilles, données) |
| **XDMF** | eXtensible Data Model and Format | Métadonnées pour visualisation de résultats FEM (FEniCSx) |
| **HDF5** (.h5) | Hierarchical Data Format | Stockage de données numériques volumineuses |
| **NPY/NPZ** | NumPy Array | Données numériques Python sérialisées |
| **PKL** | Pickle | Sérialisation d'objets Python |
| **PY** | Python Script | Code source Python (PySPH, FEniCSx, post-traitement) |
| **CPP** | C++ Source | Code source C++ (OpenFOAM, Palabos) |
| **YAML/YML** | YAML Ain't Markup Language | Configuration lisible (CI/CD, Docker) |

---

# D. Techniques et applications

## 12. Procédés de dispense

| Abréviation | Signification | Description |
|-------------|---------------|-------------|
| **DOD** | Drop-on-Demand | Éjection de gouttes à la demande (piézo ou thermique). Utilisé pour la dispense de précision, bio-impression. |
| **CIJ** | Continuous Inkjet | Jet continu avec déviation électrostatique des gouttes non désirées. Utilisé pour le marquage industriel. |

---

## 13. Caractérisation expérimentale

| Abréviation | Signification | Description |
|-------------|---------------|-------------|
| **PIV** | Particle Image Velocimetry | Vélocimétrie par images de particules. Mesure de champs de vitesse 2D/3D. |
| **OCT** | Optical Coherence Tomography | Tomographie par cohérence optique. Imagerie sub-surfacique non invasive. |

---

## 14. Couplages et intelligence artificielle

| Abréviation | Signification | Description |
|-------------|---------------|-------------|
| **FSI** | Fluid-Structure Interaction | Couplage fluide-structure. Interaction entre écoulement et déformation solide. |
| **PINN** | Physics-Informed Neural Networks | Réseaux de neurones intégrant des équations physiques comme contraintes. |
| **IA** | Intelligence Artificielle | Ensemble des techniques d'apprentissage automatique appliquées à la simulation. |

