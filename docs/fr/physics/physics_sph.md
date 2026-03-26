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

La méthode **SPH (Smoothed Particle Hydrodynamics)** est une approche **lagrangienne** et **sans maillage (meshless)** où le fluide est représenté par un ensemble de particules mobiles transportant les propriétés physiques.

### Variable principale : particules

Contrairement aux méthodes sur grille (VOF, FEM, LBM), il n'y a pas de connexions fixes entre les points. La valeur d'une propriété A en position **r** est calculée par **interpolation** :

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

où b désigne chaque particule **voisine** dans le rayon d'influence :
- $m_b$ = masse de la particule voisine b
- $A_b$ = valeur de la propriété A portée par la particule b
- $\rho_b$ = masse volumique de la particule b
- $\mathbf{r}_b$ = position de la particule b
- $W$ = **noyau de lissage** (fonction poids)
- $h$ = **longueur de lissage** (rayon d'influence)

**Avantage clé :** Gestion naturelle des surfaces libres complexes (ruptures, éclaboussures) sans maillage à déformer.

---

## 2. Équations fondamentales

### 2.1 Équation de quantité de mouvement

$$m_a \frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left(\frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab}\right) \nabla_a W_{ab} + \mathbf{f}_\sigma$$

où a est la particule **cible** et b ses particules **voisines** :
- $m_a$, $m_b$ = masses des particules cible a et voisine b
- $\mathbf{v}_a$ = vitesse de la particule a
- $p_a$, $p_b$ = pressions des particules a et b
- $\rho_a$, $\rho_b$ = masses volumiques des particules a et b
- $\Pi_{ab}$ = terme de viscosité artificielle
- $\nabla_a W_{ab}$ = gradient du noyau de lissage entre les particules a et b
- $\mathbf{f}_\sigma$ = force de tension superficielle

### 2.2 Équation d'état (faiblement compressible)

$$p = c_0^2 (\rho - \rho_0) \quad \text{ou} \quad p = B\left[\left(\frac{\rho}{\rho_0}\right)^\gamma - 1\right]$$

où :
- $p$ = pression
- $\rho$ = masse volumique locale
- $\rho_0$ = masse volumique de référence
- $c_0$ = 10·$v_{max}$ (vitesse du son numérique)
- $B$ = constante de pression
- $\gamma$ = 7 pour les liquides

### 2.3 Tension superficielle (CSF adapté)

$$\mathbf{F}_{st} = -\sigma \kappa \mathbf{n}$$

où :
- $\sigma$ = coefficient de tension superficielle
- $\kappa$ = courbure de l'interface
- $\mathbf{n}$ = ∇c, normale calculée par le gradient du champ de couleur c

---

## 3. Formulation mathématique

### 3.1 Noyau de lissage cubic spline

| Domaine | Expression |
|---------|------------|
| 0 ≤ q < 1 | W(q) = σ_d/h^d · (1 - 3q²/2 + 3q³/4) |
| 1 ≤ q < 2 | W(q) = σ_d/h^d · (2-q)³/4 |
| q ≥ 2 | W(q) = 0 |

où :
- $q$ = $r/h$, distance normalisée entre deux particules
- $\sigma_d$ = facteur de normalisation (dépend de la dimension $d$)
- $h$ = longueur de lissage
- $d$ = nombre de dimensions spatiales (2 ou 3)

### 3.2 Viscosité artificielle (Monaghan)

| Condition | Π_ab |
|-----------|------|
| **v**_ab · **r**_ab < 0 | Π_ab = (-α c̄_ab μ_ab + β μ_ab²) / ρ̄_ab |
| sinon | Π_ab = 0 |

où :
- $\mathbf{v}_{ab}$ = $\mathbf{v}_a - \mathbf{v}_b$, vitesse relative
- $\mathbf{r}_{ab}$ = $\mathbf{r}_a - \mathbf{r}_b$, position relative
- $\bar{c}_{ab}$ = vitesse du son moyenne entre a et b
- $\mu_{ab}$ = $h \mathbf{v}_{ab} \cdot \mathbf{r}_{ab} / (|\mathbf{r}_{ab}|^2 + \epsilon h^2)$
- $\bar{\rho}_{ab}$ = masse volumique moyenne entre a et b
- $\alpha$, $\beta$ = coefficients de viscosité artificielle

**Paramètres typiques :** α = 0.1, β = 0

### 3.3 Conditions aux limites (particules fantômes)

Les parois sont constituées de couches de **particules fantômes** fixes qui :
- Exercent une pression répulsive
- Imposent la condition de non-glissement
- Extrapolent les propriétés depuis le fluide

### 3.4 Fluides non-newtoniens

Le tenseur des contraintes dépend du taux de cisaillement :

$$\boldsymbol{\tau}_a = K|\dot{\gamma}_a|^{n-1} \dot{\gamma}_a$$

où :
- $\boldsymbol{\tau}_a$ = tenseur des contraintes de la particule a
- $K$ = indice de consistance (Pa·s$^n$)
- $\dot{\gamma}_a$ = taux de cisaillement local
- $n$ = indice de comportement ($n < 1$ : rhéofluidifiant)

**Avantage SPH :** Gestion naturelle de la **thixotropie** (viscosité dépendante du temps) grâce à l'approche lagrangienne.

---

## 4. Avantages et limitations

| Avantages | Limitations |
|-----------|-------------|
| Surfaces libres complexes (ruptures, éclaboussures) | Bruit numérique (oscillations de pression) |
| Advection exacte (pas de diffusion numérique) | Conditions aux limites difficiles |
| Coalescence naturelle | Coût mémoire élevé (10⁶ particules) |
| Thixotropie native (lagrangien) | Instabilités à haute vitesse (> 20 m/s) |
| Scalabilité GPU (x10-x15) | Calibration délicate (h, α) |

---

## 5. Coût computationnel

**Domaine de référence :** 1.2 mm × 0.5 mm (dispense dans micro-via)

| Configuration | Particules | Espacement | Temps | Hardware |
|---------------|------------|------------|-------|----------|
| **Ce projet** | ~1k | 15-20 µm | **1-2 h** | 6 cœurs |
| Haute résolution | ~10k | 5-10 µm | 4-8 h | 8 cœurs |
| 3D standard | ~1M | 5 µm | 5-10 h | GPU |

> **Interprétation :** ~1000 particules sur 1.2×0.5 mm donnent un espacement moyen de 15-20 µm. La longueur de lissage $h$ est typiquement 1.3× cet espacement. Code PySPH non optimisé.

**Accélération GPU :** x10-x15 vs CPU pour simulations > 100k particules.

---

## 6. Bibliothèques open-source

| Bibliothèque | Langage | GPU | Focus |
|--------------|---------|-----|-------|
| **PySPH** | Python/Cython | CUDA, OpenCL | Flexibilité, prototypage |
| **DualSPHysics** | C++/CUDA | CUDA natif | Performance, applications côtières |
| **GPUSPH** | C++/CUDA | CUDA | Écoulements géophysiques |
| **SPHinXsys** | C++ | OpenMP | Couplages multiphysiques |

---

## 7. Références bibliographiques

> **Note** : Pour la liste complète des références, consultez la section **Références bibliographiques** dans le menu Annexes.

