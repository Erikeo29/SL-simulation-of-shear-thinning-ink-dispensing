**Contents:**
1. Application Context
2. Micro-channel Geometry
3. Capillary Filling Physics
4. Fundamental Equations
5. VOF Numerical Method
6. Study Parameters
7. Computational Cost

---

## 1. Application Context

This project models the **capillary filling** of a micro-channel designed for a microfluidic sensor (µTAS - Micro Total Analysis System: a miniaturized analysis system integrating sampling, transport and detection of a liquid sample on a single chip). The objective is to understand how the physicochemical properties of the channel influence the capillary filling speed, a critical parameter for sensor response time.

**Application:** Micro-electrodes for biosensors (physiological fluid analysis (blood, sweat, etc.)).

---

## 2. Micro-channel Geometry

The domain is a **2D cross-section in the xz plane** of a 125 µm deep channel with two protruding electrodes.

```
y (µm)
125  |________________________________________________|  Cover plate (θ_top)
     |          ___       ___                          |
     |  inlet  |e1 |     |e2 |                        |
  22 |_________|   |_____|   |_________________________|  Electrodes (θ_elec)
   0 |________________________________________________|  Substrate (θ_bottom)
     ↑         ↑0.4 ↑0.9 ↑1.3 ↑1.8                  ↑
   inlet                                            outlet
   x = -0.2 mm                                     x = 3.8 mm
```

| Element | Dimension | Detail |
|---------|-----------|--------|
| Channel length | 4.0 mm | From x = −0.2 to x = 3.8 mm. |
| Depth (height) | 125 µm | Substrate-to-cover-plate distance. |
| Electrodes (×2) | 500 µm × 22 µm | Protruding from substrate. |
| Electrode chamfer | R = 3 µm | Prevents Gibbs pinning at corners. |
| Mesh | ~100k quad cells | 5 µm resolution, 2.5 µm refinement at corners. |

---

## 3. Capillary Filling Physics

### 3.1 Filling driving force: capillary pressure

Filling is driven by two forces:
- **Inlet pressure**: ΔP = 300 Pa (hydrostatic liquid pressure).
- **Capillary pressure (Young-Laplace):**

$$\Delta P_{cap} = \sigma \left(\frac{\cos\theta_{top} + \cos\theta_{bottom}}{h}\right)$$

where:
- $\sigma$ = surface tension (N/m)
- $\theta_{top}$, $\theta_{bottom}$ = contact angles on the cover plate and substrate (°)
- $h$ = channel height (m)

**Physical interpretation:** If $\theta < 90°$ (hydrophilic), the meniscus is concave and capillary pressure *pushes* the liquid forward. If $\theta > 90°$ (hydrophobic), the meniscus is convex and capillary pressure *opposes* advancement.

### 3.2 Contact angles

The contact angle $\theta$ reflects surface wettability. It is defined by Young's equation:

$$\cos\theta = \frac{\gamma_{SG} - \gamma_{SL}}{\gamma_{LG}}$$

where:
- $\gamma_{SG}$ = solid-gas surface energy
- $\gamma_{SL}$ = solid-liquid surface energy
- $\gamma_{LG}$ = liquid-gas surface tension ($= \sigma$)

| Surface | Material | θ baseline | Character |
|---------|----------|-----------|-----------|
| Cover plate | Treated PET | 22° | Very hydrophilic. |
| Substrate (bottom) | Raw PET | 121° | Hydrophobic. |
| Electrodes | Ni/Au | 96° | Slightly hydrophobic. |

### 3.3 Viscous resistance

The channel being very thin (125 µm), the flow is viscosity-dominated (Re << 1). The viscous resistance for Poiseuille flow between parallel plates:

$$\Delta P_{visc} = \frac{12 \mu L v}{h^2}$$

where:
- $\mu$ = dynamic viscosity (Pa·s)
- $L$ = wetted length (m)
- $v$ = average front velocity (m/s)
- $h$ = channel height (m)

### 3.4 Reynolds number

$$Re = \frac{\rho v h}{\mu} \approx \frac{1005 \times 0.3 \times 125 \times 10^{-6}}{9 \times 10^{-4}} \approx 0.04$$

The regime is **laminar** ($Re \ll 1$): inertial forces are negligible compared to viscous forces.

### 3.5 Capillary number

$$Ca = \frac{\mu v}{\sigma} \approx \frac{9 \times 10^{-4} \times 0.3}{0.072} \approx 3.8 \times 10^{-3}$$

$Ca \ll 1$: surface tension dominates viscous forces at the interface. The meniscus adopts a quasi-static shape (low dynamic deformation).

---

## 4. Fundamental Equations

### 4.1 Incompressible Navier-Stokes

**Mass conservation:**
$$\nabla \cdot \mathbf{v} = 0$$

**Momentum conservation:**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot (\mu \nabla \mathbf{v}) + \rho\mathbf{g} + \mathbf{f}_\sigma$$

### 4.2 Volume fraction transport (VOF)

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

| α value | Meaning |
|---------|---------|
| α = 1 | Liquid (water). |
| α = 0 | Air. |
| 0 < α < 1 | Interface zone. |

### 4.3 Mixture properties

$$\rho = \alpha \rho_{water} + (1-\alpha) \rho_{air}$$
$$\mu = \alpha \mu_{water} + (1-\alpha) \mu_{air}$$

### 4.4 Surface tension force (CSF)

Brackbill's *Continuum Surface Force* model:

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

where $\kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right)$ is the interface curvature.

---

## 5. VOF Numerical Method

### 5.1 Solver

**OpenFOAM 13** with the `incompressibleVoF` solver (successor of `interFoam`).

### 5.2 PLIC interface reconstruction

Unlike the ink dispensing project (which uses MULES with artificial compression), this project uses **PLIC** (*Piecewise Linear Interface Calculation*) reconstruction:

- The interface is geometrically reconstructed as a line segment in each cell.
- No numerical interface diffusion (unlike MULES).
- Requires a **structured mesh** (quadrilaterals) for optimal reconstruction.
- **cAlpha = 0**: artificial compression is disabled to let contact angle boundary conditions drive the physics.

### 5.3 Boundary conditions

| Boundary | U type | α type | Detail |
|----------|--------|--------|--------|
| Inlet | fixedValue (ΔP=300 Pa) | inletOutlet | Driving pressure. |
| Outlet | inletOutlet | inletOutlet | Reference pressure 0 Pa. |
| Cover plate | noSlip | contactAngle (θ_top) | Top wall. |
| Substrate | noSlip | contactAngle (θ_bottom) | Bottom wall. |
| Electrodes | noSlip | contactAngle (θ_elec) | Ni/Au surfaces. |
| Front/Back | empty | empty | 2D symmetry. |

### 5.4 Fluid properties

| Property | Liquid (water) | Air |
|----------|---------------|-----|
| ρ (kg/m³) | 1005 | 1.2 |
| ν (m²/s) | 8.96×10⁻⁷ | 1.48×10⁻⁵ |
| μ (mPa·s) | 0.90 | 0.018 |
| σ (mN/m) | 72 | — |

> **Note:** The fluid is Newtonian (no Carreau model here), unlike the ink dispensing project.

---

## 6. Study Parameters

The parametric study covers **7 configurations** varying one parameter at a time from the reference case (baseline).

| ID | Description | Varied parameter | Value | t_fill (ms) | Δ vs baseline |
|----|-------------|-----------------|-------|-------------|---------------|
| **001** | **Baseline (reference)** | — | — | **13.7** | — |
| 002 | Neutral substrate | θ_bottom | 90° (vs 121°) | 11.9 | −13% |
| 003 | Hydrophilic substrate | θ_bottom | 60° (vs 121°) | 10.6 | −23% |
| 004 | Viscosity ×1.5 | μ | 1.35 mPa·s (vs 0.90) | 20.2 | +47% |
| 005 | Surfactant (σ×0.5) | σ | 36 mN/m (vs 72) | 16.2 | +18% |
| 006 | Hydrophilic electrodes | θ_elec | 45° (vs 96°) | 10.8 | −21% |
| 007 | Less hydrophilic cover plate | θ_top | 45° (vs 22°) | 16.3 | +19% |

**Ranking by filling speed (fastest first):**

003 (10.6 ms) > 006 (10.8 ms) > 002 (11.9 ms) > 001 (13.7 ms) > 005 (16.2 ms) ≈ 007 (16.3 ms) > 004 (20.2 ms)

### Physical insights

1. **Substrate contact angle**: dominant effect. Changing θ from 121° (hydrophobic) to 60° (hydrophilic) reduces filling time by 23%. The substrate is the largest wetted surface, so its wettability drives the net capillary pressure.

2. **Viscosity**: strongest effect. +50% viscosity → +47% filling time. In a thin channel, viscous resistance ($\propto \mu / h^2$) is the dominant brake.

3. **Surfactant (σ÷2)**: counter-intuitive effect. Reducing σ *slows* filling (+18%) because the capillary driving force (∝ σ·cos θ / h) decreases more than interfacial resistance.

4. **Cover plate wettability**: θ_top = 45° vs 22° → +19%. The cover plate contributes significantly to capillary pressure as it represents half the wetted perimeter.

5. **Electrode wettability**: modest effect (−21% apparent but electrodes occupy only ~0.6% of the total wetted surface).

---

## 7. Computational Cost

| Configuration | Cells | Resolution | Time/case | Hardware |
|---------------|-------|------------|-----------|----------|
| **This project** | ~100k | 5 µm (2.5 µm corners) | **5-15 min** | 6 cores |

**Stability parameters:**
- maxCo = 0.2, maxAlphaCo = 0.2
- Adaptive time stepping (Euler, 1st order)
- Initial deltaT = 0.1 µs, maxDeltaT = 50 µs

> **Comparison:** This case is ~10× faster than the ink dispensing project (50k cells, 0.5-2h) because the channel is geometrically simpler and the fluid is Newtonian.
