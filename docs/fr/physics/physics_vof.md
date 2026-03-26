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

La méthode **VOF (Volume of Fluid)** est une approche eulérienne pour le suivi d'interfaces dans les écoulements diphasiques. Elle représente le standard industriel pour les simulations à surface libre, notamment avec le solveur `interFoam` d'OpenFOAM.

### Variable principale : fraction volumique α

| Valeur | Signification |
|--------|---------------|
| α = 1 | Encre (fluide 1) |
| α = 0 | Air (fluide 2) |
| 0 < α < 1 | Zone d'interface |

**Avantage clé :** Conservation de masse parfaite, propriété intrinsèque de la formulation.

---

## 2. Équations fondamentales

### 2.1 Équations de Navier-Stokes

**Conservation de la masse :**
$$\nabla \cdot \mathbf{v} = 0$$

**Conservation de la quantité de mouvement :**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho\mathbf{g} + \mathbf{f}_\sigma$$

où :
- $\mathbf{v}$ = vecteur vitesse (m/s)
- $\rho$ = masse volumique du mélange (kg/m³)
- $p$ = pression (Pa)
- $\boldsymbol{\tau}$ = tenseur des contraintes visqueuses (Pa)
- $\mathbf{g}$ = accélération gravitationnelle (m/s²)
- $\mathbf{f}_\sigma$ = force de tension superficielle volumique (N/m³)

### 2.2 Équation de transport de α

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

où :
- $\alpha$ = fraction volumique (0 = air, 1 = encre)
- $\mathbf{v}$ = vecteur vitesse

**Avec compression artificielle (MULES - OpenFOAM) :**
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

où :
- $\mathbf{v}_r$ = $c_\alpha |\mathbf{v}| \mathbf{n}$, vitesse de compression artificielle
- $c_\alpha$ = coefficient de compression (typiquement 1 dans OpenFOAM)
- $\mathbf{n}$ = normale à l'interface ($\nabla \alpha / |\nabla \alpha|$)
- Le terme $\alpha(1-\alpha)$ garantit que la compression n'agit qu'à l'interface

### 2.3 Force de tension de surface (CSF)

Le modèle **Continuum Surface Force** de Brackbill :

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

où :
- $\sigma$ = coefficient de tension superficielle (N/m)
- $\kappa$ = $-\nabla \cdot (\nabla \alpha / |\nabla \alpha|)$, courbure de l'interface (m$^{-1}$)
- $\nabla \alpha$ = gradient de la fraction volumique (localise l'interface)

---

## 3. Formulation mathématique

### 3.1 Propriétés du mélange

Les propriétés physiques sont interpolées linéairement :

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

où :
- $\alpha$ = fraction volumique (0 = air, 1 = encre)
- $\rho_1$, $\rho_2$ = masses volumiques de l'encre et de l'air (kg/m³)
- $\eta_1$, $\eta_2$ = viscosités dynamiques de l'encre et de l'air (Pa·s)

### 3.2 Modèle de Carreau (fluides non-newtoniens)

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

| Paramètre | Symbole | Valeur | Unité |
|-----------|---------|--------|-------|
| Masse volumique | ρ | 3000 | kg/m³ |
| Viscosité au repos | η₀ | 0.5 - 5 | Pa·s |
| Viscosité à cisaillement infini | η∞ | 0.05 - 0.15 | Pa·s |
| Temps de relaxation | λ | 0.15 | s |
| Indice de pseudoplasticité | n | 0.7 | - |
| Tension de surface | σ | 0.04 | N/m |

### 3.3 Configuration OpenFOAM (`transportProperties`)

```cpp
transportModel Carreau;

CarreauCoeffs {
    nu0   nu0 [0 2 -1 0 0 0 0] 1.667e-4;  // η₀/ρ
    nuInf nuInf [0 2 -1 0 0 0 0] 1.667e-5; // η∞/ρ
    k     k [0 0 1 0 0 0 0] 0.15;          // λ
    n     n [0 0 0 0 0 0 0] 0.7;           // n
}

sigma sigma [1 0 -2 0 0 0 0] 0.04;
```

---

## 4. Avantages et limitations

| Avantages | Limitations |
|-----------|-------------|
| Robustesse éprouvée (>25 ans) | Diffusion numérique de l'interface |
| Conservation de masse parfaite | Maillages fins requis près de l'interface |
| Standard industriel (OpenFOAM) | Coalescences multiples difficiles |
| Précision interfaciale 0.1-1 µm (avec PLIC) | Rhéologie complexe (thixotropie) difficile |
| Support GPU depuis OpenFOAM 10 (non réussi dans ce projet)| Coût mémoire pour AMR |

---

## 5. Coût computationnel

**Domaine de référence :** 1.2 mm × 0.5 mm (dispense dans micro-via)

| Configuration | Cellules | Résolution | Temps | Hardware |
|---------------|----------|------------|-------|----------|
| **Ce projet** | ~50k | ~5 µm | **0.5-2 h** | 6 cœurs |
| Haute résolution | ~500k | ~1.5 µm | 4-8 h | 16 cœurs |
| Avec AMR | 50k-500k | 1-10 µm (adaptatif) | 2-4 h | 16 cœurs |

> **Interprétation :** 50k cellules hexaédriques sur 1.2×0.5 mm correspondent à une résolution de ~5 µm, compatible avec la reconstruction PLIC de l'interface.

**Accélération GPU :** x5-x10 pour les opérations matricielles (OpenFOAM ≥ v10 avec CUDA).

---

## 6. Bibliothèques open-source

| Bibliothèque | Langage | Focus | Parallélisation |
|--------------|---------|-------|-----------------|
| **OpenFOAM** | C++ | Standard industriel, VOF/interFoam | MPI, CUDA |
| **Basilisk** | C | Recherche, AMR natif | MPI |
| **Gerris** | C | Précurseur de Basilisk | MPI |

---

## 7. Références bibliographiques

> **Note** : Pour la liste complète des références, consultez la section **Références bibliographiques** dans le menu Annexes.

