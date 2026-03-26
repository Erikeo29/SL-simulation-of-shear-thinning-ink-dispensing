**Contents:**
1. Navier-Stokes Equations
2. Rheological Models
3. Interface Tracking
4. Surface Tension
5. Boundary Conditions
6. Fundamental Dimensionless Numbers
   - 6.1 Reynolds - Flow Regimes
   - 6.2 Weber - Droplet Stability
   - 6.3 Ohnesorge - Ejection and Filaments
   - 6.4 Deborah - Viscoelastic Effects
   - 6.5 Capillary - Spreading and Wetting
   - 6.6 Bond - Gravity vs Capillarity
7. Model Comparison Table
8. Summary

This chapter presents the fundamental equations used in the numerical models. The goal is to understand the commonalities (Navier-Stokes equations, rheology) and differences (discretization, interface tracking).

---

## 1. Navier-Stokes Equations

### 1.1 Mass Conservation (Continuity)

$$\nabla \cdot \mathbf{v} = 0$$

| Term | Meaning | Unit |
|------|---------|------|
| $\nabla \cdot$ | Divergence operator | m$^{-1}$ |
| $\mathbf{v}$ | Velocity vector $(v_x, v_y, v_z)$ | m/s |

**Interpretation:** The mass flux entering an elementary volume equals the outgoing flux. This equation enforces **incompressibility** of the fluid.

**Expanded form (2D):**
$$\frac{\partial v_x}{\partial x} + \frac{\partial v_y}{\partial y} = 0$$

---

### 1.2 Momentum Conservation

$$\rho \left[ \frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla) \mathbf{v} \right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho \mathbf{g} + \mathbf{F}_\sigma$$

| Term | Name | Physical meaning |
|------|------|------------------|
| $\rho \frac{\partial \mathbf{v}}{\partial t}$ | **Local inertia** | Temporal variation of momentum |
| $\rho (\mathbf{v} \cdot \nabla) \mathbf{v}$ | **Convection** | Momentum transport by the flow |
| $-\nabla p$ | **Pressure gradient** | Driving force from pressure differences |
| $\nabla \cdot \boldsymbol{\tau}$ | **Viscous diffusion** | Dissipation by internal friction |
| $\rho \mathbf{g}$ | **Gravity** | Gravitational body force |
| $\mathbf{F}_\sigma$ | **Surface tension** | Capillary force at interface |

**Operators:**

| Operator | Notation | Definition |
|----------|----------|------------|
| Gradient | $\nabla p$ | $\left( \frac{\partial p}{\partial x}, \frac{\partial p}{\partial y}, \frac{\partial p}{\partial z} \right)$ |
| Divergence | $\nabla \cdot \boldsymbol{\tau}$ | $\frac{\partial \tau_{ij}}{\partial x_j}$ (summation over $j$) |
| Convection | $(\mathbf{v} \cdot \nabla)$ | $v_x \frac{\partial}{\partial x} + v_y \frac{\partial}{\partial y} + v_z \frac{\partial}{\partial z}$ |

---

### 1.3 Viscous Stress Tensor

For an incompressible Newtonian fluid:

$$\boldsymbol{\tau} = 2 \eta \mathbf{D}$$

where the **rate of deformation tensor** is:

$$\mathbf{D} = \frac{1}{2} \left[ \nabla \mathbf{v} + (\nabla \mathbf{v})^T \right]$$

**Components (2D):**

$$\mathbf{D} = \begin{pmatrix} \frac{\partial v_x}{\partial x} & \frac{1}{2}\left(\frac{\partial v_x}{\partial y} + \frac{\partial v_y}{\partial x}\right) \\ \frac{1}{2}\left(\frac{\partial v_x}{\partial y} + \frac{\partial v_y}{\partial x}\right) & \frac{\partial v_y}{\partial y} \end{pmatrix}$$

**Shear rate:**

$$\dot{\gamma} = \sqrt{2 \mathbf{D} : \mathbf{D}} = \sqrt{2 \sum_{i,j} D_{ij} D_{ij}}$$

---

## 2. Rheological Models

### 2.1 Newton's Law (Newtonian Fluid)

$$\boldsymbol{\tau} = 2 \eta \mathbf{D}$$

Viscosity $\eta$ is **constant**. Examples: water, air, mineral oils.

---

### 2.2 Power Law (Ostwald-de Waele)

$$\eta(\dot{\gamma}) = K \dot{\gamma}^{n-1}$$

| Parameter | Meaning | Typical value |
|-----------|---------|---------------|
| $K$ | Consistency | 0.01 - 10 Pa·s$^n$ |
| $n$ | Flow behavior index | 0.3 - 0.9 (shear-thinning) |
| $\dot{\gamma}$ | Shear rate | 1 - 10$^5$ s$^{-1}$ |

**Behavior:**
- $n < 1$: **Shear-thinning** (viscosity ↓ when shear ↑)
- $n = 1$: Newtonian
- $n > 1$: Shear-thickening

**Limitation:** Singularity at $\dot{\gamma} = 0$ (viscosity → ∞).

---

### 2.3 Carreau Model

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[ 1 + (\lambda \dot{\gamma})^2 \right]^{\frac{n-1}{2}}$$

| Parameter | Meaning | Typical value (shear-thinning ink) |
|-----------|---------|----------------------------|
| $\eta_0$ | Zero-shear viscosity | 0.5 - 5 Pa·s |
| $\eta_\infty$ | Infinite-shear viscosity | 0.05 Pa·s |
| $\lambda$ | Relaxation time | 0.1 - 0.2 s |
| $n$ | Flow behavior index | 0.6 - 0.8 |

**Advantage:** Avoids power law singularity thanks to $\eta_0$ and $\eta_\infty$ plateaus.

**Graphical form:**
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

### 2.4 Herschel-Bulkley Model (Yield Stress Fluid)

| Condition | Behavior |
|-----------|----------|
| $\|\boldsymbol{\tau}\| \leq \tau_0$ | Solid (no flow) |
| $\|\boldsymbol{\tau}\| > \tau_0$ | $\boldsymbol{\tau} = \left( \frac{\tau_0}{\dot{\gamma}} + K \dot{\gamma}^{n-1} \right) \dot{\boldsymbol{\gamma}}$ |

| Parameter | Meaning |
|-----------|---------|
| $\tau_0$ | Yield stress |
| $K$ | Consistency |
| $n$ | Flow behavior index |

**Application:** High solid-loading inks, pastes, gels.

---

## 3. Interface Tracking

### 3.1 VOF: Volume Fraction Transport

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

| Term | Meaning |
|------|---------|
| $\alpha$ | Volume fraction (0 = air, 1 = ink) |
| $\frac{\partial \alpha}{\partial t}$ | Temporal variation of the fraction |
| $\nabla \cdot (\alpha \mathbf{v})$ | Interface advection by flow |

**Mixture properties:**
$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

**PLIC reconstruction:** Interface is approximated by a plane in each cell:
$$\mathbf{n} \cdot \mathbf{x} = d$$
where $\mathbf{n} = \nabla \alpha / |\nabla \alpha|$ is the normal.

---

### 3.2 Phase-Field: Cahn-Hilliard Equation

$$\frac{\partial \phi}{\partial t} + \mathbf{v} \cdot \nabla \phi = \gamma \nabla \cdot \left[ \varepsilon \nabla \phi - \phi (1 - \phi^2) \mathbf{n} \right]$$

| Term | Meaning |
|------|---------|
| $\phi$ | Order parameter ($-1$ = air, $+1$ = ink) |
| $\mathbf{v} \cdot \nabla \phi$ | Interface advection |
| $\gamma$ | Interface mobility |
| $\varepsilon$ | Diffuse interface thickness |
| $\phi (1 - \phi^2)$ | Double-well term (maintains $\phi = \pm 1$) |

**Ginzburg-Landau free energy:**
$$\mathcal{F}[\phi] = \int_\Omega \left[ \frac{\varepsilon}{2} |\nabla \phi|^2 + \frac{1}{4\varepsilon} (1 - \phi^2)^2 \right] d\Omega$$

---

### 3.3 LBM: Discrete Boltzmann Equation

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = \Omega_i$$

| Term | Meaning |
|------|---------|
| $f_i$ | Distribution function in direction $i$ |
| $\mathbf{c}_i$ | Discrete velocity of direction $i$ |
| $\Omega_i$ | Collision operator |

**BGK operator:**
$$\Omega_i = -\frac{1}{\tau} (f_i - f_i^{eq})$$

where $\tau$ is the relaxation time and $f_i^{eq}$ is the Maxwell-Boltzmann equilibrium distribution.

**Recovery of macroscopic quantities:**
$$\rho = \sum_i f_i \qquad \rho \mathbf{v} = \sum_i f_i \mathbf{c}_i$$

**Viscosity-relaxation relation:**
$$\nu = c_s^2 \left( \tau - \frac{1}{2} \right) \Delta t$$

with $c_s = 1/\sqrt{3}$ the lattice speed of sound.

---

### 3.4 SPH: Kernel Interpolation

$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

| Term | Meaning |
|------|---------|
| $A(\mathbf{r})$ | Interpolated value at point $\mathbf{r}$ |
| $m_b, \rho_b$ | Mass and density of particle $b$ |
| $A_b$ | Value of $A$ carried by particle $b$ |
| $W$ | Smoothing kernel |
| $h$ | Smoothing length |

**SPH momentum equation:**
$$\frac{d\mathbf{v}_a}{dt} = -\sum_b m_b \left( \frac{p_a}{\rho_a^2} + \frac{p_b}{\rho_b^2} + \Pi_{ab} \right) \nabla_a W_{ab} + \mathbf{g} + \frac{\mathbf{F}_\sigma}{m_a}$$

| Term | Meaning |
|------|---------|
| $p_a / \rho_a^2$ | Pressure contribution (symmetric formulation) |
| $\Pi_{ab}$ | Artificial viscosity |
| $\nabla_a W_{ab}$ | Kernel gradient |

---

## 4. Surface Tension

### 4.1 CSF Model (Continuum Surface Force)

$$\mathbf{F}_\sigma = \sigma \kappa \mathbf{n} \delta_s$$

| Term | Meaning | Calculation |
|------|---------|-------------|
| $\sigma$ | Surface tension | 0.04 N/m (ink) |
| $\kappa$ | Interface curvature | $\kappa = -\nabla \cdot \mathbf{n}$ |
| $\mathbf{n}$ | Interface normal | $\mathbf{n} = \nabla \alpha / |\nabla \alpha|$ (VOF) |
| $\delta_s$ | Surface delta | $\delta_s = |\nabla \alpha|$ (VOF) |

**Implementation by method:**

| Method | Formulation |
|--------|-------------|
| **VOF** | $\mathbf{F}_\sigma = \sigma \kappa \nabla \alpha$ |
| **Phase-Field** | $\mathbf{F}_\sigma = \sigma \kappa \delta(\phi) \mathbf{n}$ with $\delta(\phi) = \frac{3}{2\varepsilon}|\nabla \phi|$ |
| **LBM** | Shan-Chen force: $\mathbf{F} = -G \psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i) \mathbf{c}_i$ |
| **SPH** | Pairwise force: $\mathbf{F}_\sigma = -\sigma \sum_b s_{ab} \frac{\mathbf{r}_{ab}}{|\mathbf{r}_{ab}|} W_{ab}$ |

---

### 4.2 Interface Curvature

$$\kappa = -\nabla \cdot \mathbf{n} = -\nabla \cdot \left( \frac{\nabla \alpha}{|\nabla \alpha|} \right)$$

**Expanded form (2D):**

$$\kappa = -\frac{\alpha_{xx} \alpha_y^2 - 2 \alpha_x \alpha_y \alpha_{xy} + \alpha_{yy} \alpha_x^2}{(\alpha_x^2 + \alpha_y^2)^{3/2}}$$

where $\alpha_x = \partial \alpha / \partial x$, etc.

---

## 5. Boundary Conditions

### 5.1 Wetting Condition (Contact Angle)

$$\mathbf{n} \cdot \mathbf{n}_w = \cos \theta$$

| Variable | Meaning |
|----------|---------|
| $\mathbf{n}$ | Fluid interface normal |
| $\mathbf{n}_w$ | Wall normal |
| $\theta$ | Static contact angle |

**Typical values:**
- $\theta < 90°$: Hydrophilic surface (wetting)
- $\theta > 90°$: Hydrophobic surface (non-wetting)
- $\theta = 90°$: Neutral

---

## 6. Fundamental Dimensionless Numbers

Fluid dispensing modeling involves several interdependent physical phenomena, characterized by the following dimensionless numbers:

| Number | Expression | Meaning | Typical Value | Physical Interpretation |
|--------|------------|---------|---------------|-------------------------|
| **Reynolds** | $Re = \frac{\rho v D}{\eta}$ | Inertial vs viscous effects | 10 - 100 | Ratio of inertial to viscous forces. Determines flow regime. |
| **Weber** | $We = \frac{\rho v^2 L}{\sigma}$ | Inertial forces vs surface tension | $We < 10$ | Ratio of kinetic energy to surface energy. Controls droplet deformation. |
| **Ohnesorge** | $Oh = \frac{\eta}{\sqrt{\rho \sigma D}}$ | Viscosity, surface tension, and size | $Oh < 0.5$ | Combines viscosity, capillarity, and inertia. Predicts jet and filament stability. |
| **Deborah** | $De = \lambda \dot{\gamma}$ | Viscoelastic effects | Variable | Ratio of fluid relaxation time to characteristic flow time. |
| **Capillary** | $Ca = \frac{\eta v}{\sigma}$ | Viscosity vs capillarity | $Ca \ll 1$ | Ratio of viscous forces to surface tension. Controls spreading. |
| **Bond** | $Bo = \frac{\rho g L^2}{\sigma}$ | Gravity vs surface tension | $Bo \ll 1$ | Ratio of gravitational to capillary forces. Determines droplet shape. |

---

### 6.1 Reynolds Number ($Re$) - Flow Regimes

| $Re$ Range | Regime | Physical Description |
|------------|--------|----------------------|
| $Re < 1$ | **Stokes (creeping)** | Viscous forces dominate, very slow flow, reversible. Typical of microchannels. |
| $1 < Re < 10$ | **Viscous laminar** | Ordered flow, inertial effects begin to appear but remain weak. |
| $10 < Re < 100$ | **Inertial laminar** | Typical regime for ink dispensing. Stable flow with significant inertial effects. |
| $100 < Re < 2000$ | **Transitional laminar** | Laminar flow but sensitive to perturbations. Possible onset of instabilities. |
| $Re > 2000$ | **Turbulent** | Chaotic flow with vortices. Rare in microfluidics (diameters too small). |

**Dispensing application:** With $\rho \approx 1000$ kg/m³, $v \approx 0.1$ m/s, $D \approx 300$ µm, $\eta \approx 0.5$ Pa·s → $Re \approx 60$ (inertial laminar).

---

### 6.2 Weber Number ($We$) - Droplet Stability

| $We$ Range | Behavior | Physical Description |
|------------|----------|----------------------|
| $We < 1$ | **Capillary dominant** | Surface tension maintains spherical droplets. No significant deformation. |
| $1 < We < 10$ | **Inertia-capillarity balance** | Moderate droplet deformation. Optimal regime for controlled dispensing. |
| $10 < We < 50$ | **Significant deformation** | Highly deformed droplets, risk of satellite droplet breakup. |
| $We > 50$ | **Atomization** | Fragmentation into fine droplets. Splash phenomenon upon impact. |

**Dispensing application:** $We < 10$ ensures clean dispensing without excessive satellites.

---

### 6.3 Ohnesorge Number ($Oh$) - Ejection and Filament Formation

| $Oh$ Range | Behavior | Physical Description |
|------------|----------|----------------------|
| $Oh < 0.1$ | **Inertio-capillary** | Low viscous damping. Droplet oscillations, frequent satellites, thin filaments that break up. |
| $0.1 < Oh < 0.5$ | **Optimal regime** | Viscosity/capillarity balance. Stable droplet formation, controlled filaments. Optimal zone for inkjet. |
| $0.5 < Oh < 1$ | **Moderate viscous** | Oscillation damping. Thicker filaments, fewer satellites but slower ejection. |
| $Oh > 1$ | **Viscous dominant** | Difficult to eject droplets. Stretching of long viscous filaments ("stringing"). |

**Fromm criterion:** Inkjet printability zone: $0.1 < Oh < 1$ and $We > 4$.

---

### 6.4 Deborah Number ($De$) - Viscoelastic Effects

| $De$ Range | Behavior | Physical Description |
|------------|----------|----------------------|
| $De \ll 1$ | **Equivalent Newtonian fluid** | Fluid has time to relax. Quasi-viscous behavior, no elastic memory. |
| $De \approx 1$ | **Viscoelastic** | Coupling between relaxation and flow. Significant elastic effects (die swell, normal stresses). |
| $De \gg 1$ | **Elastic dominant** | Fluid behaves like an elastic solid. Energy storage, delayed response. |

**Ink application:** Shear-thinning inks often have $\lambda \approx 0.1$ s and $\dot{\gamma} \approx 100$ s⁻¹ → $De \approx 10$ (notable elastic effects).

---

### 6.5 Capillary Number ($Ca$) - Spreading and Wetting

| $Ca$ Range | Behavior | Physical Description |
|------------|----------|----------------------|
| $Ca \ll 0.01$ | **Pure capillary** | Interface deforms only under surface tension. Rapid equilibrium shape. |
| $0.01 < Ca < 0.1$ | **Visco-capillary** | Competition between viscous spreading and surface tension. Controlled wetting dynamics. |
| $Ca > 0.1$ | **Viscous dominant** | Viscous flow deforms the interface. Film entrainment, significant contact line deformation. |

**Dispensing application:** $Ca \approx 0.01$ - spreading is controlled by capillarity with moderate viscous influence.

---

### 6.6 Bond Number ($Bo$) - Gravity vs Capillarity

| $Bo$ Range | Behavior | Physical Description |
|------------|----------|----------------------|
| $Bo \ll 0.1$ | **Capillary dominant** | Gravity is negligible. Quasi-spherical droplets, capillary rise possible. |
| $0.1 < Bo < 1$ | **Transition** | Gravity and capillarity comparable. Slightly flattened droplets, intermediate shape. |
| $Bo > 1$ | **Gravity dominant** | Droplets flatten under their weight. "Puddle" shape, gravitational drainage. |

**Micro-via application:** With $L \approx 500$ µm → $Bo \approx 0.01$ - gravity is negligible, filling is dominated by capillarity and wetting.

---

## 7. Model Comparison Table

### 7.1 Equations Solved

| Equation | FEM | VOF | LBM | SPH |
|----------|:---:|:---:|:---:|:---:|
| **Navier-Stokes** | Direct (weak form) | Direct (finite volumes) | Indirect ($f_i$ moments) | Direct (particles) |
| **Continuity** | Constraint | Constraint | Automatic | Equation of state |
| **Interface transport** | Cahn-Hilliard | $\alpha$ advection | Shan-Chen / Free Energy | Particle motion |
| **Rheology** | Local $\eta(\dot{\gamma})$ | Local $\eta(\dot{\gamma})$ | Local $\tau(\dot{\gamma})$ | Per-particle $\eta(\dot{\gamma})$ |
| **Surface tension** | Phase-Field + CSF | CSF | Shan-Chen force | Adapted CSF / Pairwise |

---

### 7.2 Discretization

| Aspect | FEM | VOF | LBM | SPH |
|--------|-----|-----|-----|-----|
| **Reference frame** | Eulerian | Eulerian | Eulerian | Lagrangian |
| **Mesh** | Elements (triangles, tetrahedra) | Finite volumes (hexahedra) | Regular lattice (D2Q9, D3Q19) | Meshless |
| **Interface** | Diffuse ($\varepsilon \sim \mu$m) | Reconstructed (PLIC) | Diffuse (pseudopotential) | Implicit (color) |
| **$\mathbf{v}$-$p$ coupling** | Mixed elements (Taylor-Hood) | PIMPLE/SIMPLE | Equation of state | Equation of state |

---

### 7.3 Advantages and Limitations

| Criterion | FEM | VOF | LBM | SPH |
|-----------|-----|-----|-----|-----|
| **Interface precision** | Excellent (0.05 µm) | Very good (0.1 µm) | Good (0.2 µm) | Medium (0.5 µm) |
| **Complex rheology** | Excellent | Good | Limited | Excellent (thixotropy) |
| **GPU scalability** | Low | Medium | Excellent (×20) | Good (×10) |
| **Large deformations** | Difficult (remeshing) | Medium | Good | Excellent |
| **Mass conservation** | Very good | Perfect | Good | Very good |

---

### 7.4 When to Use Each Method

| Situation | Recommended Method | Justification |
|-----------|---------------------|---------------|
| Industrial validation | **VOF** | Robustness, established standard |
| Fine rheology study | **FEM** | Advanced constitutive laws |
| Rapid parametric exploration | **LBM** | GPU performance |
| Jet breakup, splashes | **SPH** | Complex free surfaces |
| Fluid-structure coupling | **FEM** | Variational formulation |
| Thixotropic inks | **SPH** | Lagrangian approach |
| Complex geometries (roughness) | **LBM** | Natural wetting |

---

## 8. Summary: From Navier-Stokes to Methods

```
                    PHYSICAL EQUATIONS
                           │
           ┌───────────────┴───────────────┐
           │                               │
    Navier-Stokes                    Interface
    (conservation)                   (tracking)
           │                               │
    ┌──────┴──────┐              ┌─────────┴─────────┐
    │             │              │         │         │
  FEM/VOF       LBM            VOF    Phase-Field   SPH
 (direct)    (Boltzmann)     (α)        (φ)      (color)
    │             │              │         │         │
    └──────┬──────┘              └────┬────┘         │
           │                          │              │
      Discretization              Surface        Lagrangian
           │                      tension            │
    ┌──────┴──────┐                  │              │
    │      │      │                 CSF          SPH
   Meshed Lattice Particles          │          kernels
   (FEM)  (LBM)   (SPH)              │              │
           │                         │              │
           └─────────────────────────┴──────────────┘
                           │
                    NUMERICAL SIMULATION
```

