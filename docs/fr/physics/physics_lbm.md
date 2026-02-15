**Sommaire :**
1. Principe de la méthode
2. Équations fondamentales
3. Formulation mathématique
4. Avantages et limitations
5. Coût computationnel
6. Bibliothèques open-source
7. Références bibliographiques

---

## 1. Principe de la méthode

La méthode **LBM (Lattice Boltzmann Method)** est une approche **mésoscopique** qui ne résout pas directement les équations de Navier-Stokes, mais l'**équation de Boltzmann discrétisée** sur un réseau régulier (lattice).

### Variable principale : fonctions de distribution f_i

On suit l'évolution de fonctions de distribution f_i(**x**, t) représentant la probabilité de trouver des particules à la position **x** se déplaçant selon des directions discrètes **c**_i.

Les grandeurs macroscopiques sont obtenues par **moments statistiques** :

$$\rho = \sum_i f_i \quad \text{et} \quad \rho \mathbf{u} = \sum_i f_i \mathbf{c}_i$$

où :
- $f_i$ = fonction de distribution dans la direction $i$
- $\rho$ = masse volumique macroscopique (kg/m³)
- $\mathbf{u}$ = vitesse macroscopique (m/s)
- $\mathbf{c}_i$ = vecteur vitesse discrète de la direction $i$

**Avantage clé :** Parallélisation massive sur GPU (chaque nœud est indépendant).

---

## 2. Équations fondamentales

### 2.1 Équation de Boltzmann discrète (BGK)

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau}(f_i - f_i^{eq}) + F_i$$

où :
- $f_i(\mathbf{x}, t)$ = fonction de distribution au nœud $\mathbf{x}$, direction $i$, temps $t$
- $\mathbf{c}_i$ = vecteur vitesse discrète de la direction $i$
- $\Delta t$ = pas de temps
- $\tau$ = temps de relaxation (contrôle la viscosité)
- $f_i^{eq}$ = distribution d'équilibre de Maxwell-Boltzmann
- $F_i$ = terme de force externe (gravité, Shan-Chen)

### 2.2 Distribution d'équilibre

$$f_i^{eq} = w_i \rho \left[1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}^2}{2c_s^2}\right]$$

où :
- $w_i$ = poids de quadrature de la direction $i$
- $\rho$ = masse volumique
- $\mathbf{c}_i$ = vecteur vitesse discrète
- $\mathbf{u}$ = vitesse macroscopique
- $c_s$ = $1/\sqrt{3}$, vitesse du son sur le réseau (en unités lattice)

### 2.3 Lien viscosité - temps de relaxation

$$\nu = c_s^2 \left(\tau - \frac{1}{2}\right) \Delta t$$

où :
- $\nu$ = viscosité cinématique (m²/s)
- $c_s$ = vitesse du son sur le réseau
- $\tau$ = temps de relaxation (doit être > 0.5 pour la stabilité)
- $\Delta t$ = pas de temps

Cette relation permet de modéliser des fluides de viscosités différentes en ajustant τ.

---

## 3. Formulation mathématique

### 3.1 Grilles de discrétisation (DdQq)

La notation **DdQq** désigne une grille à **d** dimensions spatiales avec **q** vitesses discrètes de propagation. Ces vitesses définissent les directions dans lesquelles les populations de particules se déplacent à chaque pas de temps.

| Grille | Dimensions | Vitesses | Application |
|--------|------------|----------|-------------|
| **D2Q9** | 2D | 9 | Standard 2D |
| **D3Q19** | 3D | 19 | Standard 3D (bon compromis) |
| **D3Q27** | 3D | 27 | Haute précision |

**Choix de ce projet :** D2Q9 avec Δx = 5 µm

### 3.2 Modèle multiphasique Shan-Chen

La force interparticulaire modélise les interactions entre fluides :

$$\mathbf{F}_{int}(\mathbf{x}) = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i$$

où :
- $G$ = constante de couplage (contrôle la tension superficielle)
- $\psi(\mathbf{x})$ = pseudopotentiel (fonction de la densité locale)
- $w_i$ = poids de quadrature
- $\mathbf{c}_i$ = vecteur vitesse discrète

**Tension superficielle :** σ ∝ G(ψ_max - ψ_min)²

### 3.3 Fluides non-newtoniens

Pour les fluides rhéofluidifiants, τ dépend localement du taux de cisaillement :

$$\tau(\dot{\gamma}) = \frac{1}{2} + \frac{\nu(\dot{\gamma})}{c_s^2 \Delta t}$$

où :
- $\tau$ = temps de relaxation local (variable spatialement)
- $\dot{\gamma}$ = taux de cisaillement local (s$^{-1}$)
- $\nu(\dot{\gamma})$ = viscosité cinématique dépendante du cisaillement (modèle Carreau)

### 3.4 Gestion du mouillage

Les angles de contact sont gérés par une **densité fictive** aux nœuds solides :

$$\rho_{solid} = \rho_0 + \Delta \rho \cdot \cos(\theta_{eq})$$

où :
- $\rho_{solid}$ = densité fictive assignée aux nœuds solides
- $\rho_0$ = densité de référence du fluide
- $\Delta \rho$ = amplitude de modulation
- $\theta_{eq}$ = angle de contact d'équilibre souhaité

Le mouillage est géré naturellement sans conditions aux limites explicites.

---

## 4. Avantages et limitations

| Avantages | Limitations |
|-----------|-------------|
| Scalabilité GPU exceptionnelle (x20) | Compressibilité artificielle (Ma < 0.1) |
| Parallélisation intrinsèque | Courants parasites aux interfaces |
| Mouillage naturel (géométries complexes) | Calibration rhéologique délicate |
| Coalescence/rupture automatiques | Mémoire GPU limitante en 3D |
| Précision interfaciale ~1 µm | Rapport de densité limité (~1000, encre/air réel = 2500) |

---

## 5. Coût computationnel

**Domaine de référence :** 1.2 mm × 0.5 mm (dispense dans micro-via)

| Configuration | Grille | Δx | Temps | Hardware |
|---------------|--------|-----|-------|----------|
| **Ce projet** | 240×100 | 5 µm | **~10 min** | 6 cœurs |
| Haute résolution | 1200×500 | 1 µm | 1–2 h | GPU |
| 3D (D3Q19) | 300³ | 4 µm | 1–2 h | 1× GPU |

> **Interprétation :** Une grille 240×100 avec Δx = 5 µm couvre exactement le domaine 1.2×0.5 mm. Le LBM est particulièrement rapide grâce à sa structure régulière optimisée pour le parallélisme.

**Scalabilité GPU :** Quasi-linéaire jusqu'à 16 GPUs. ~16 GB pour 300³ nœuds en D3Q19.

---

## 6. Bibliothèques open-source

| Bibliothèque | Langage | GPU | Focus |
|--------------|---------|-----|-------|
| **Palabos** | C++ | Non | Référence open-source, tutoriels |
| **OpenLB** | C++ | CUDA/OpenMP | Applications industrielles |
| **waLBerla** | C++ | CUDA | HPC extrême, millions de cœurs |
| **Sailfish** | Python/CUDA | CUDA natif | Interface Python |

---

## 7. Références bibliographiques

> **Note** : Pour la liste complète des références, consultez la section **Références bibliographiques** dans le menu Annexes.

