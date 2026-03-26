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

La méthode **Phase-Field** couplée aux **Éléments Finis (FEM)** est une approche eulérienne pour la simulation d'écoulements diphasiques. L'interface entre les deux fluides est représentée comme une **zone de transition diffuse** d'épaisseur finie ε.

### Variable principale : fonction de phase φ

| Valeur | Signification |
|--------|---------------|
| φ = +1 | Encre (fluide 1) |
| φ = -1 | Air (fluide 2) |
| -1 < φ < +1 | Zone d'interface |

**Avantage clé :** Les changements topologiques (coalescence, rupture) sont gérés automatiquement sans intervention numérique.

---

## 2. Équations fondamentales

### 2.1 Équations de Navier-Stokes

**Conservation de la masse (incompressible) :**
$$\nabla \cdot \mathbf{v} = 0$$

**Conservation de la quantité de mouvement :**
$$\rho(\phi)\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot [2\eta(\phi,\dot{\gamma})\mathbf{D}] + \mathbf{F}_\sigma$$

où **D** est le tenseur des taux de déformation et **F**_σ la force de tension de surface.

### 2.2 Équation de transport Phase-Field

$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[\varepsilon \nabla \phi - \phi(1-\phi^2)\mathbf{n}\right]$$

avec γ = mobilité de l'interface, ε = épaisseur de l'interface, **n** = normale à l'interface.

### 2.3 Force de tension de surface

$$\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$$

où σ = tension de surface, κ = courbure, δ(φ) = fonction delta localisée à l'interface.

---

## 3. Formulation mathématique

### 3.1 Modèle rhéologique de Carreau

La viscosité de l'encre rhéofluidifiante suit :

$$\eta(\dot{\gamma}) = \eta_{\infty} + (\eta_0 - \eta_{\infty})\left[1 + (\lambda\dot{\gamma})^2\right]^{\frac{n-1}{2}}$$

| Paramètre | Symbole | Valeur | Unité |
|-----------|---------|--------|-------|
| Viscosité au repos | η₀ | 1.5 - 5 | Pa·s |
| Viscosité à cisaillement infini | η∞ | 0.05 | Pa·s |
| Temps de relaxation | λ | 0.15 | s |
| Indice de pseudoplasticité | n | 0.7 | - |

### 3.2 Propriétés du mélange

$$\rho(\phi) = \rho_1 H(\phi) + \rho_2 [1-H(\phi)]$$
$$\eta(\phi) = \eta_1 H(\phi) + \eta_2 [1-H(\phi)]$$

où H(φ) est une fonction de Heaviside régularisée.

### 3.3 Conditions aux limites

| Surface | Condition |
|---------|-----------|
| Parois | Non-glissement : **v** = **0** |
| Électrode or | Angle de contact : θ = 35-75° |
| Parois micro-via | Angle de contact : θ = 35-90° |
| Entrée (buse) | Vitesse imposée : v = 0.1 m/s |
| Sortie | Pression atmosphérique : p = 0 |

### 3.4 Éléments finis Taylor-Hood (P2-P1)

| Variable | Élément | Degré |
|----------|---------|-------|
| Vitesse **v** | Lagrange quadratique (P2) | 2 |
| Pression p | Lagrange linéaire (P1) | 1 |

Cette combinaison garantit la stabilité inf-sup et évite les oscillations de pression.

---

## 4. Avantages et limitations

| Avantages | Limitations |
|-----------|-------------|
| Consistance thermodynamique | Coût mémoire élevé (maillage fin requis) |
| Coalescence/rupture automatiques | Scalabilité GPU limitée |
| Couplage multiphysique natif (FSI) | Résolution interface dépend de ε |
| Précision élevée (erreur < 2%) | Temps de calcul important en 3D |
| Support rhéologie complexe | Calibration de γ et ε délicate |

---

## 5. Coût computationnel

**Domaine de référence :** 1.2 mm × 0.5 mm (dispense dans micro-via)

| Configuration | Éléments | Taille maille | Temps | Hardware |
|---------------|----------|---------------|-------|----------|
| **Ce projet** | ~20k | 5-10 µm | **1-2 h** | 8 cœurs |
| Haute résolution | ~100k | 1-2 µm | 4-8 h | 16 cœurs |
| 3D complet | ~500k | 5 µm | 30-50 h | Cluster |

> **Interprétation :** 20k éléments triangulaires sur un domaine 1.2×0.5 mm donnent une taille de maille moyenne de 5-10 µm, suffisante pour capturer l'interface diffuse (ε ~ 2-5 µm).

**Note :** La FEM classique (assemblage matriciel) bénéficie peu de l'accélération GPU, contrairement à LBM.

---

## 6. Bibliothèques open-source

| Bibliothèque | Langage | Focus | Parallélisation |
|--------------|---------|-------|-----------------|
| **FEniCS** | Python/C++ | Flexibilité, prototypage | MPI, PETSc |
| **Firedrake** | Python | Automatisation, GPU | MPI, PETSc |
| **deal.II** | C++ | Performance, adaptativité | MPI, Trilinos |
| **FreeFEM** | DSL | Rapidité d'implémentation | MPI, MUMPS |

---

## 7. Références bibliographiques

> **Note** : Pour la liste complète des références, consultez la section **Références bibliographiques** dans le menu Annexes.

