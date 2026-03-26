**Sommaire :**
1. Équations de Navier-Stokes
2. Modèles rhéologiques
3. Suivi d'interface
4. Tension superficielle
5. Conditions aux limites
6. Nombres adimensionnels fondamentaux
   - 6.1 Reynolds - Régimes d'écoulement
   - 6.2 Weber - Stabilité des gouttes
   - 6.3 Ohnesorge - Éjection et filaments
   - 6.4 Deborah - Effets viscoélastiques
   - 6.5 Capillaire - Étalement et mouillage
   - 6.6 Bond - Gravité vs Capillarité
7. Tableau comparatif des modèles
8. Synthèse

Ce chapitre présente les équations fondamentales utilisées dans les modèles numériques. L'objectif est de comparer les points communs (équations de Navier-Stokes, rhéologie) et les différences (discrétisation, suivi d'interface).

---

## 1. Équations de Navier-Stokes

### 1.1 Conservation de la masse (continuité)

$$\nabla \cdot \mathbf{v} = 0$$

| Terme | Signification | Unité |
|-------|---------------|-------|
| $\nabla \cdot$ | Opérateur divergence | m$^{-1}$ |
| $\mathbf{v}$ | Vecteur vitesse $(v_x, v_y, v_z)$ | m/s |

**Interprétation :** Le flux de masse entrant dans un volume élémentaire est égal au flux sortant. Cette équation impose l'**incompressibilité** du fluide.

**Forme développée (2D) :**
$$\frac{\partial v_x}{\partial x} + \frac{\partial v_y}{\partial y} = 0$$

---

### 1.2 Conservation de la quantité de mouvement

$$\rho \left[ \frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla) \mathbf{v} \right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \mathbf{g} + \mathbf{F}_\sigma$$

| Terme | Nom | Signification physique |
|-------|-----|------------------------|
| $\rho \frac{\partial \mathbf{v}}{\partial t}$ | **Inertie locale** | Variation temporelle de la quantité de mouvement |
| $\rho (\mathbf{v} \cdot \nabla) \mathbf{v}$ | **Convection** | Transport de quantité de mouvement par l'écoulement |
| $-\nabla p$ | **Gradient de pression** | Force motrice due aux différences de pression |
| $\nabla \cdot \boldsymbol{\tau}$ | **Diffusion visqueuse** | Dissipation par frottement interne |
| $\rho \mathbf{g}$ | **Gravité** | Force volumique gravitationnelle |
| $\mathbf{F}_\sigma$ | **Tension superficielle** | Force capillaire à l'interface |

**Opérateurs :**

| Opérateur | Notation | Définition |
|-----------|----------|------------|
| Gradient | $\nabla p$ | $\left( \frac{\partial p}{\partial x}, \frac{\partial p}{\partial y}, \frac{\partial p}{\partial z} \right)$ |
| Divergence | $\nabla \cdot \boldsymbol{\tau}$ | $\frac{\partial \tau_{ij}}{\partial x_j}$ (sommation sur $j$) |
| Convection | $(\mathbf{v} \cdot \nabla)$ | $v_x \frac{\partial}{\partial x} + v_y \frac{\partial}{\partial y} + v_z \frac{\partial}{\partial z}$ |

---

### 1.3 Tenseur des contraintes visqueuses

Pour un fluide newtonien incompressible :

$$\boldsymbol{\tau} = 2 \eta \mathbf{D}$$

où le **tenseur des taux de déformation** est :

$$\mathbf{D} = \frac{1}{2} \left[ \nabla \mathbf{v} + (\nabla \mathbf{v})^T \right]$$

**Composantes (2D) :**

$$\mathbf{D} = \begin{pmatrix} \frac{\partial v_x}{\partial x} & \frac{1}{2}\left(\frac{\partial v_x}{\partial y} + \frac{\partial v_y}{\partial x}\right) \\ \frac{1}{2}\left(\frac{\partial v_x}{\partial y} + \frac{\partial v_y}{\partial x}\right) & \frac{\partial v_y}{\partial y} \end{pmatrix}$$

**Taux de cisaillement :**

$$\dot{\gamma} = \sqrt{2 \mathbf{D} : \mathbf{D}} = \sqrt{2 \sum_{i,j} D_{ij} D_{ij}}$$

---

## 2. Modèles rhéologiques

### 2.1 Loi de Newton (fluide newtonien)

$$\boldsymbol{\tau} = 2 \eta \mathbf{D}$$

La viscosité $\eta$ est **constante**. Exemples : eau, air, huiles minérales.

---

### 2.2 Loi de puissance (Ostwald-de Waele)

$$\eta(\dot{\gamma}) = K \dot{\gamma}^{n-1}$$

| Paramètre | Signification | Valeur typique |
|-----------|---------------|----------------|
| $K$ | Consistance | 0.01 - 10 Pa·s$^n$ |
| $n$ | Indice de comportement | 0.3 - 0.9 (rhéofluidifiant) |
| $\dot{\gamma}$ | Taux de cisaillement | 1 - 10$^5$ s$^{-1}$ |

**Comportement :**
- $n < 1$ : **Rhéofluidifiant** (viscosité ↓ quand cisaillement ↑)
- $n = 1$ : Newtonien
- $n > 1$ : Rhéoépaississant

**Limitation :** Singularité à $\dot{\gamma} = 0$ (viscosité → ∞).

---

### 2.3 Modèle de Carreau

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[ 1 + (\lambda \dot{\gamma})^2 \right]^{\frac{n-1}{2}}$$

| Paramètre | Signification | Valeur typique (encre rhéofluidifiante) |
|-----------|---------------|-------------------------------|
| $\eta_0$ | Viscosité au repos | 0.5 - 5 Pa·s |
| $\eta_\infty$ | Viscosité à fort cisaillement | 0.05 Pa·s |
| $\lambda$ | Temps de relaxation | 0.1 - 0.2 s |
| $n$ | Indice de comportement | 0.6 - 0.8 |

**Avantage :** Évite la singularité de la loi de puissance grâce aux plateaux $\eta_0$ et $\eta_\infty$.

**Forme graphique :**
```
η
│
η₀ ─────┐
│       ╲
│        ╲
η∞ ───────────────
│
└───────────────── log(γ̇)
     λ⁻¹
```

---

### 2.4 Modèle de Herschel-Bulkley (fluide à seuil)

| Condition | Comportement |
|-----------|--------------|
| $\|\boldsymbol{\tau}\| \leq \tau_0$ | Solide (pas d'écoulement) |
| $\|\boldsymbol{\tau}\| > \tau_0$ | $\boldsymbol{\tau} = \left( \frac{\tau_0}{\dot{\gamma}} + K \dot{\gamma}^{n-1} \right) \dot{\boldsymbol{\gamma}}$ |

| Paramètre | Signification |
|-----------|---------------|
| $\tau_0$ | Contrainte seuil (yield stress) |
| $K$ | Consistance |
| $n$ | Indice de comportement |

**Application :** Encres avec charge solide élevée, pâtes, gels.

---

## 3. Suivi d'interface

### 3.1 VOF : transport de la fraction volumique

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

| Terme | Signification |
|-------|---------------|
| $\alpha$ | Fraction volumique (0 = air, 1 = encre) |
| $\frac{\partial \alpha}{\partial t}$ | Variation temporelle de la fraction |
| $\nabla \cdot (\alpha \mathbf{v})$ | Advection de l'interface par l'écoulement |

**Propriétés du mélange :**
$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

**Reconstruction PLIC :** L'interface est approximée par un plan dans chaque cellule :
$$\mathbf{n} \cdot \mathbf{x} = d$$
où $\mathbf{n} = \nabla \alpha / |\nabla \alpha|$ est la normale.

---

### 3.2 Phase-Field : équation de Cahn-Hilliard

$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[ \varepsilon \nabla \phi - \phi (1 - \phi^2) \mathbf{n} \right]$$

| Terme | Signification |
|-------|---------------|
| $\phi$ | Paramètre d'ordre ($-1$ = air, $+1$ = encre) |
| $\mathbf{v} \cdot \nabla \phi$ | Advection de l'interface |
| $\gamma$ | Mobilité de l'interface |
| $\varepsilon$ | Épaisseur de l'interface diffuse |
| $\phi (1 - \phi^2)$ | Terme de double puits (maintient $\phi = \pm 1$) |

**Énergie libre de Ginzburg-Landau :**
$$\mathcal{F}[\phi] = \int_\Omega \left[ \frac{\varepsilon}{2} |\nabla \phi|^2 + \frac{1}{4\varepsilon} (1 - \phi^2)^2 \right] d\Omega$$

---

### 3.3 LBM : équation de Boltzmann discrète

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = \Omega_i$$

| Terme | Signification |
|-------|---------------|
| $f_i$ | Fonction de distribution dans la direction $i$ |
| $\mathbf{c}_i$ | Vitesse discrète de la direction $i$ |
| $\Omega_i$ | Opérateur de collision |

**Opérateur BGK :**
$$\Omega_i = -\frac{1}{\tau} (f_i - f_i^{eq})$$

où $\tau$ est le temps de relaxation et $f_i^{eq}$ la distribution d'équilibre de Maxwell-Boltzmann.

**Récupération des grandeurs macroscopiques :**
$$\rho = \sum_i f_i \qquad \rho \mathbf{v} = \sum_i f_i \mathbf{c}_i$$

**Lien viscosité-relaxation :**
$$\nu = c_s^2 \left( \tau - \frac{1}{2} \right) \Delta t$$

avec $c_s = 1/\sqrt{3}$ la vitesse du son sur réseau.

---

### 3.4 SPH : interpolation par noyau

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

| Terme | Signification |
|-------|---------------|
| $A(\mathbf{r})$ | Valeur interpolée au point $\mathbf{r}$ |
| $m_b, \rho_b$ | Masse et densité de la particule $b$ |
| $A_b$ | Valeur de $A$ portée par la particule $b$ |
| $W$ | Noyau de lissage (kernel) |
| $h$ | Longueur de lissage |

**Équation du mouvement SPH :**
$$\frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left( \frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab} \right) \nabla_a W_{ab} + \mathbf{g} + \frac{\mathbf{F}_\sigma}{m_a}$$

| Terme | Signification |
|-------|---------------|
| $p_a / \rho_a^2$ | Contribution de pression (formulation symétrique) |
| $\Pi_{ab}$ | Viscosité artificielle |
| $\nabla_a W_{ab}$ | Gradient du noyau |

---

## 4. Tension superficielle

### 4.1 Modèle CSF (Continuum Surface Force)

$$\mathbf{F}_\sigma = \sigma \kappa \mathbf{n} \delta_s$$

| Terme | Signification | Calcul |
|-------|---------------|--------|
| $\sigma$ | Tension superficielle | 0.04 N/m (encre) |
| $\kappa$ | Courbure de l'interface | $\kappa = -\nabla \cdot \mathbf{n}$ |
| $\mathbf{n}$ | Normale à l'interface | $\mathbf{n} = \nabla \alpha / |\nabla \alpha|$ (VOF) |
| $\delta_s$ | Delta de surface | $\delta_s = |\nabla \alpha|$ (VOF) |

**Implémentation par méthode :**

| Méthode | Formulation |
|---------|-------------|
| **VOF** | $\mathbf{F}_\sigma = \sigma \kappa \nabla \alpha$ |
| **Phase-Field** | $\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$ avec $\delta(\phi) = \frac{3}{2\varepsilon}|\nabla \phi|$ |
| **LBM** | Force Shan-Chen : $\mathbf{F} = -G \psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i) \mathbf{c}_i$ |
| **SPH** | Force pairée : $\mathbf{F}_\sigma = -\sigma \sum_b s_{ab} \frac{\mathbf{r}_{ab}}{|\mathbf{r}_{ab}|} W_{ab}$ |

---

### 4.2 Courbure de l'interface

$$\kappa = -\nabla \cdot \mathbf{n} = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$$

**Forme développée (2D) :**

$$\kappa = -\frac{\alpha_{xx} \alpha_y^2 - 2 \alpha_x \alpha_y \alpha_{xy} + \alpha_{yy} \alpha_x^2}{(\alpha_x^2 + \alpha_y^2)^{3/2}}$$

où $\alpha_x = \partial \alpha / \partial x$, etc.

---

## 5. Conditions aux limites

### 5.1 Condition de mouillage (angle de contact)

$$\mathbf{n} \cdot \mathbf{n}_w = \cos \theta$$

| Variable | Signification |
|----------|---------------|
| $\mathbf{n}$ | Normale à l'interface fluide |
| $\mathbf{n}_w$ | Normale à la paroi |
| $\theta$ | Angle de contact statique |

**Valeurs typiques :**
- $\theta < 90°$ : Surface hydrophile (mouillante)
- $\theta > 90°$ : Surface hydrophobe (non-mouillante)
- $\theta = 90°$ : Neutre

---

## 6. Nombres adimensionnels fondamentaux

La modélisation de la dispense de fluides implique plusieurs phénomènes physiques interdépendants, caractérisés par les nombres adimensionnels suivants :

| Nombre | Expression | Signification | Valeur typique | Interprétation physique |
|--------|------------|---------------|----------------|-------------------------|
| **Reynolds** | $Re = \frac{\rho v D}{\eta}$ | Effets inertiels vs visqueux | 10 - 100 | Rapport entre forces d'inertie et forces visqueuses. Détermine le régime d'écoulement. |
| **Weber** | $We = \frac{\rho v^2 L}{\sigma}$ | Forces inertielles vs tension superficielle | $We < 10$ | Rapport entre énergie cinétique et énergie de surface. Contrôle la déformation des gouttes. |
| **Ohnesorge** | $Oh = \frac{\eta}{\sqrt{\rho \sigma D}}$ | Viscosité, tension superficielle et taille | $Oh < 0.5$ | Combine viscosité, capillarité et inertie. Prédit la stabilité des jets et filaments. |
| **Deborah** | $De = \lambda \dot{\gamma}$ | Effets viscoélastiques | Variable | Rapport entre temps de relaxation du fluide et temps caractéristique de l'écoulement. |
| **Capillaire** | $Ca = \frac{\eta v}{\sigma}$ | Viscosité vs capillarité | $Ca \ll 1$ | Rapport entre forces visqueuses et tension superficielle. Contrôle l'étalement. |
| **Bond** | $Bo = \frac{\rho g L^2}{\sigma}$ | Gravité vs tension superficielle | $Bo \ll 1$ | Rapport entre forces gravitationnelles et capillaires. Détermine la forme des gouttes. |

---

### 6.1 Nombre de Reynolds ($Re$) - Régimes d'écoulement

| Plage de $Re$ | Régime | Description physique |
|---------------|--------|----------------------|
| $Re < 1$ | **Stokes (rampant)** | Forces visqueuses dominantes, écoulement très lent, réversible. Typique des microcanaux. |
| $1 < Re < 10$ | **Laminaire visqueux** | Écoulement ordonné, les effets inertiels commencent à apparaître mais restent faibles. |
| $10 < Re < 100$ | **Laminaire inertiel** | Régime typique de la dispense d'encre. Écoulement stable mais avec effets inertiels significatifs. |
| $100 < Re < 2000$ | **Laminaire transitionnel** | Écoulement laminaire mais sensible aux perturbations. Début d'instabilités possibles. |
| $Re > 2000$ | **Turbulent** | Écoulement chaotique avec tourbillons. Rare en microfluidique (diamètres trop petits). |

**Application dispense :** Avec $\rho \approx 1000$ kg/m³, $v \approx 0.1$ m/s, $D \approx 300$ µm, $\eta \approx 0.5$ Pa·s → $Re \approx 60$ (laminaire inertiel).

---

### 6.2 Nombre de Weber ($We$) - Stabilité des gouttes

| Plage de $We$ | Comportement | Description physique |
|---------------|--------------|----------------------|
| $We < 1$ | **Capillaire dominant** | La tension superficielle maintient les gouttes sphériques. Pas de déformation significative. |
| $1 < We < 10$ | **Équilibre inertie-capillarité** | Déformation modérée des gouttes. Régime optimal pour la dispense contrôlée. |
| $10 < We < 50$ | **Déformation importante** | Gouttes fortement déformées, risque de rupture en gouttelettes satellites. |
| $We > 50$ | **Atomisation** | Fragmentation en fines gouttelettes. Phénomène de splash à l'impact. |

**Application dispense :** $We < 10$ garantit une dispense propre sans satellites excessifs.

---

### 6.3 Nombre d'Ohnesorge ($Oh$) - Éjection et formation de filaments

| Plage de $Oh$ | Comportement | Description physique |
|---------------|--------------|----------------------|
| $Oh < 0.1$ | **Inertio-capillaire** | Faible amortissement visqueux. Oscillations de gouttes, satellites fréquents, filaments fins qui se brisent. |
| $0.1 < Oh < 0.5$ | **Régime optimal** | Équilibre viscosité/capillarité. Formation de gouttes stables, filaments contrôlés. Zone optimale pour l'inkjet. |
| $0.5 < Oh < 1$ | **Visqueux modéré** | Amortissement des oscillations. Filaments plus épais, moins de satellites mais éjection plus lente. |
| $Oh > 1$ | **Visqueux dominant** | Difficile d'éjecter des gouttes. Étirement de longs filaments visqueux ("stringing"). |

**Critère de Fromm :** Zone d'imprimabilité inkjet : $0.1 < Oh < 1$ et $We > 4$.

---

### 6.4 Nombre de Deborah ($De$) - Effets viscoélastiques

| Plage de $De$ | Comportement | Description physique |
|---------------|--------------|----------------------|
| $De \ll 1$ | **Fluide newtonien équivalent** | Le fluide a le temps de relaxer. Comportement quasi-visqueux, pas de mémoire élastique. |
| $De \approx 1$ | **Viscoélastique** | Couplage entre relaxation et écoulement. Effets élastiques significatifs (die swell, normal stresses). |
| $De \gg 1$ | **Élastique dominant** | Le fluide se comporte comme un solide élastique. Stockage d'énergie, réponse différée. |

**Application encres :** Les encres rhéofluidifiantes ont souvent $\lambda \approx 0.1$ s et $\dot{\gamma} \approx 100$ s⁻¹ → $De \approx 10$ (effets élastiques notables).

---

### 6.5 Nombre Capillaire ($Ca$) - Étalement et mouillage

| Plage de $Ca$ | Comportement | Description physique |
|---------------|--------------|----------------------|
| $Ca \ll 0.01$ | **Capillaire pur** | L'interface se déforme uniquement sous l'effet de la tension superficielle. Forme d'équilibre rapide. |
| $0.01 < Ca < 0.1$ | **Visco-capillaire** | Compétition entre étalement visqueux et tension superficielle. Dynamique de mouillage contrôlée. |
| $Ca > 0.1$ | **Visqueux dominant** | L'écoulement visqueux déforme l'interface. Entraînement de film, déformation importante de la ligne de contact. |

**Application dispense :** $Ca \approx 0.01$ - l'étalement est contrôlé par la capillarité avec influence visqueuse modérée.

---

### 6.6 Nombre de Bond ($Bo$) - Gravité vs Capillarité

| Plage de $Bo$ | Comportement | Description physique |
|---------------|--------------|----------------------|
| $Bo \ll 0.1$ | **Capillaire dominant** | La gravité est négligeable. Gouttes quasi-sphériques, montée capillaire possible. |
| $0.1 < Bo < 1$ | **Transition** | Gravité et capillarité comparables. Gouttes légèrement aplaties, forme intermédiaire. |
| $Bo > 1$ | **Gravité dominante** | Les gouttes s'aplatissent sous leur poids. Forme de "flaque", drainage gravitaire. |

**Application micro-via :** Avec $L \approx 500$ µm → $Bo \approx 0.01$ - la gravité est négligeable, le remplissage est dominé par la capillarité et le mouillage.

---

## 7. Tableau comparatif des modèles

### 7.1 Équations résolues

| Équation | FEM | VOF | LBM | SPH |
|----------|:---:|:---:|:---:|:---:|
| **Navier-Stokes** | Directe (forme faible) | Directe (volumes finis) | Indirecte (moments de $f_i$) | Directe (particules) |
| **Continuité** | Contrainte | Contrainte | Automatique | Équation d'état |
| **Transport interface** | Cahn-Hilliard | Advection $\alpha$ | Shan-Chen / Free Energy | Mouvement particules |
| **Rhéologie** | $\eta(\dot{\gamma})$ local | $\eta(\dot{\gamma})$ local | $\tau(\dot{\gamma})$ local | $\eta(\dot{\gamma})$ par particule |
| **Tension superficielle** | Phase-Field + CSF | CSF | Force Shan-Chen | CSF adapté / Pairwise |

---

### 7.2 Discrétisation

| Aspect | FEM | VOF | LBM | SPH |
|--------|-----|-----|-----|-----|
| **Référentiel** | Eulérien | Eulérien | Eulérien | Lagrangien |
| **Maillage** | Éléments (triangles, tétraèdres) | Volumes finis (hexaèdres) | Réseau régulier (D2Q9, D3Q19) | Sans maillage |
| **Interface** | Diffuse ($\varepsilon \sim \mu$m) | Reconstruite (PLIC) | Diffuse (pseudopotentiel) | Implicite (couleur) |
| **Couplage $\mathbf{v}$-$p$** | Éléments mixtes (Taylor-Hood) | PIMPLE/SIMPLE | Équation d'état | Équation d'état |

---

### 7.3 Avantages et limitations

| Critère | FEM | VOF | LBM | SPH |
|---------|-----|-----|-----|-----|
| **Précision interface** | Excellente (0.05 µm) | Très bonne (0.1 µm) | Bonne (0.2 µm) | Moyenne (0.5 µm) |
| **Rhéologie complexe** | Excellente | Bonne | Limitée | Excellente (thixotropie) |
| **Scalabilité GPU** | Faible | Moyenne | Excellente (×20) | Bonne (×10) |
| **Grandes déformations** | Difficile (remaillage) | Moyenne | Bonne | Excellente |
| **Conservation masse** | Très bonne | Parfaite | Bonne | Très bonne |

---

### 7.4 Quand utiliser chaque méthode

| Situation | Méthode Recommandée | Justification |
|-----------|---------------------|---------------|
| Validation industrielle | **VOF** | Robustesse, standard établi |
| Étude rhéologie fine | **FEM** | Lois constitutives avancées |
| Exploration paramétrique rapide | **LBM** | Performance GPU |
| Rupture de jet, éclaboussures | **SPH** | Surfaces libres complexes |
| Couplage fluide-structure | **FEM** | Formulation variationnelle |
| Encres thixotropes | **SPH** | Approche lagrangienne |
| Géométries complexes (rugosité) | **LBM** | Mouillage naturel |

---

## 8. Synthèse : de Navier-Stokes aux méthodes

```
                    ÉQUATIONS PHYSIQUES
                           │
           ┌───────────────┴───────────────┐
           │                               │
    Navier-Stokes                    Interface
    (conservation)                   (suivi)
           │                               │
    ┌──────┴──────┐              ┌─────────┴─────────┐
    │             │              │         │         │
  FEM/VOF       LBM            VOF    Phase-Field   SPH
 (direct)    (Boltzmann)     (α)        (φ)      (couleur)
    │             │              │         │         │
    └──────┬──────┘              └────┬────┘         │
           │                          │              │
      Discrétisation              Tension        Lagrangien
           │                    superficielle        │
    ┌──────┴──────┐                  │              │
    │      │      │                 CSF          Noyaux
   Maillé Réseau Particules          │             SPH
   (FEM)  (LBM)   (SPH)              │              │
           │                         │              │
           └─────────────────────────┴──────────────┘
                           │
                    SIMULATION NUMÉRIQUE
```

