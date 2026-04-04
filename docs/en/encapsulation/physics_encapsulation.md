**Contents:**
1. Application Context
2. Domain Geometry
3. Rheology: Bird-Carreau Model
4. Surface Tension and Wettability
5. Dimensional Analysis
6. Fundamental Equations
7. VOF Numerical Method
8. Study Matrix
9. Physical Insights

---

## 1. Application Context

This project models **glob top encapsulation** of a Chip-On-Board (COB) component. The process consists of dispensing a shear-thinning epoxy resin over a silicon die and its wire bonds to provide mechanical and thermal protection.

**Application:** Semiconductor packaging : biosensors, low-cost integrated circuits.

**Dam-and-fill process:**
1. Die bonded to PCB (FR-4 substrate)
2. Wire bonds formed (Au, Ø 25 µm, ~500 µm loop height)
3. Dam (epoxy compound barrier) placed around the die
4. Glob top (resin) dispensed from a mobile nozzle (Ø 0.6 mm)
5. Settling phase for capillary self-leveling
6. Cure (150°C, 1-2 h) → polymerization

**Simulation objective:** Predict die coverage and dam overflow (spillage) risk as a function of process parameters.

---

## 2. Domain Geometry

2D cross-section in the XY plane (1 cell in Z).

```
       INLET (nozzle, Ø 0.6 mm)
          ↓
    ╔═══════════╗  y = 2.35 mm
    ║  NOZZLE   ║
    ║  (mobile) ║
    ╠═══════════╣  y = 1.1 mm (nozzle bottom = dam top)
    ║           ║
  ╔═╩═══════════╩═╗
  ║ DAM    DIE    DAM ║  y = 0.8 mm (dam top)
  ║ 0.5mm  1.0mm  0.5mm║
  ║        0.3mm      ║  y = 0.3 mm (die top)
  ║  PCB    ║DIE║  PCB  ║
  ║  (Au)   ║   ║  (Au) ║
  ╚═════════╩═══╩═══════╝  y = 0
  x=-1.5                x=1.5 mm
```

| Element | Dimensions | Material |
|---------|-----------|----------|
| Die | 1.0 × 0.3 mm | SiN (passivation). |
| Au pads | 0.4 mm (×2, each side) | Gold |
| Dam (barrier) | 0.5 × 0.5-1.0 mm (×2) | Epoxy compound |
| Nozzle | Ø 0.6 mm, height 1.5 mm | Steel + PTFE (exterior). |
| PCB | Total width 3.0 mm | FR-4 + solder mask |
| Mesh | ~100k hex cells | 10-20 µm resolution. |

---

## 3. Rheology: Bird-Carreau Model

The glob top resin is a **shear-thinning** fluid: its viscosity decreases under shear. The Bird-Carreau model captures both viscosity plateaus:

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[1 + (\lambda \dot{\gamma})^2\right]^{(n-1)/2}$$

| Parameter | Symbol | Reference value | Unit |
|-----------|--------|----------------|------|
| Zero-shear viscosity | η₀ | 15-50 | Pa·s |
| Infinite-shear viscosity | η∞ | 1.0 | Pa·s |
| Relaxation time | λ | 10 | s |
| Shear-thinning index | n | 0.4 | - |
| Density | ρ | 1200 | kg/m³ |

**Physical interpretation:**
- **At rest** (γ̇ → 0): η → η₀ = 50 Pa·s → resin stays in place (no gravity drainage).
- **Under the nozzle** (γ̇ ~ 100 s⁻¹): η → η∞ = 1 Pa·s → resin flows easily.
- **After dispensing** (γ̇ → 0): η rises → slow, controlled capillary self-leveling.

The resin/air viscosity ratio is extreme: **5×10⁶**. This contrast requires careful numerical treatment (implicit solver for viscous diffusion).

---

## 4. Surface Tension and Wettability

### 4.1 Surface tension

$\sigma$ = 0.038 N/m (38 mN/m, epoxy resin / air at 25°C, uncured)

### 4.2 Dynamic contact angles

Contact angles vary by surface material. A dynamic model (hysteresis ±5°) is used for critical surfaces:

| Surface | Material | θ₀ (°) | Model | Character |
|---------|----------|--------|-------|-----------|
| PCB | Solder mask (FR-4) | 35 | Dynamic (±5°) | Hydrophilic |
| Au pads | Gold (bond zone) | 25 | Dynamic (±5°) | Very hydrophilic |
| Die | SiN (chip passivation) | 25 | Dynamic (±5°) | Very hydrophilic |
| Dam | Epoxy compound (barrier) | 70 | Dynamic (±5°) | Partial wetting |
| Nozzle interior | Stainless steel | 90 | Constant | Neutral |
| Nozzle exterior | PTFE | 150 | Constant | Anti-wetting |

**Physical role:**
- θ(pads) = 25° and θ(die) = 25°: resin *wets* spontaneously the die and pads → good coverage.
- θ(dam) = 70°: the barrier slows resin advancement → prevents overflow.
- θ(nozzle ext) = 150°: prevents resin from creeping up the nozzle exterior (PTFE coating).

### 4.3 Young's equation

$$\cos\theta = \frac{\gamma_{SG} - \gamma_{SL}}{\sigma}$$

The contact angle reflects the surface energy balance at the triple line (solid-liquid-gas).

---

## 5. Dimensional Analysis

**Reference conditions:** U = 1 mm/s (dispensing velocity), L = 0.6 mm (nozzle Ø)

| Number | Expression | Value | Interpretation |
|--------|-----------|-------|----------------|
| **Re** | ρUL/μ | 0.012 | Stokes : inertia negligible. |
| **Ca** | μU/σ | 1.3 | Viscoelastic ≈ capillary. |
| **Bo** | ρgL²/σ | 0.077 | Gravity negligible. |
| **Oh** | μ/√(ρσL) | 330 | Extremely viscous (no oscillations). |

**Two-phase regime:**
- **During dispensing** (Ca ~ 1): viscous and capillary forces are comparable → flow shape depends on rheology AND wettability.
- **During settling** (Ca → 0.1): capillarity dominates → self-leveling, resin spreads on hydrophilic surfaces.

This two-phase character (viscous dispensing → capillary settling) is the key physical signature of the process.

---

## 6. Fundamental Equations

### 6.1 Incompressible Navier-Stokes

$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p_{rgh} + \nabla \cdot [\mu(\nabla \mathbf{v} + \nabla \mathbf{v}^T)] + \sigma\kappa\nabla\alpha + \rho\mathbf{g}$$

### 6.2 VOF Transport

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) + \nabla \cdot [\alpha(1-\alpha)\mathbf{v}_r] = 0$$

| α | Phase |
|---|-------|
| 1 | Epoxy resin |
| 0 | Air |

### 6.3 Mixture properties

$$\rho = \alpha \rho_{resin} + (1-\alpha) \rho_{air}$$
$$\mu = \alpha \mu_{resin}(\dot{\gamma}) + (1-\alpha) \mu_{air}$$

> Resin viscosity depends on local shear rate via Bird-Carreau.

---

## 7. VOF Numerical Method

### 7.1 Solver

**OpenFOAM v2406**, `interFoam` solver (VOF with CSF surface tension).

### 7.2 Critical choice: cAlpha = 0

The artificial compression coefficient **cAlpha** is set to **0** (disabled). This is a critical choice:

| cAlpha | Interface effect | Contact angle effect |
|--------|-----------------|---------------------|
| 1 (default) | Sharp interface (~3 cells) | **Inoperable.** Compression crushes capillary gradients. |
| **0 (this project)** | Diffuse interface (~5-7 cells) | **Functional.** Physics drives wetting. |

**Consequence:** the interface is more diffuse, but contact angles correctly impose wetting physics. This trade-off is essential for predicting die coverage.

### 7.3 PIMPLE Algorithm

| Parameter | Value | Note |
|-----------|-------|------|
| nOuterCorrectors | 2 | Higher than standard (1). Required for high-viscosity coupling. |
| nCorrectors | 3 | Inner pressure-velocity corrections. |
| momentumPredictor | no | Standard VOF |

### 7.4 Adaptive time stepping

- Initial deltaT: 0.1 µs
- maxCo = 0.3, maxAlphaCo = 0.3
- maxDeltaT: 500 µs
- endTime: 1.0 s (0.5 s dispensing + 0.5 s settling).

---

## 8. Study Matrix

38 cases were simulated. Here are the representative cases available in this tool:

| ID | Description | Key parameter | Die (%) | Dam spillage | Verdict |
|----|-------------|--------------|---------|--------------|---------|
| **025** | **Best case (offset die)** | x_start = −0.5 mm | **96%** | **0%** | ✅ Validated |
| 026 | Corrected physics baseline | Reference | ~90% | Low | ✅ |
| 028 | 10 µm mesh | cell = 10 µm | 95% | 0% | ✅ |
| 033 | Symmetric dispensing | v_lat symmetric | 100% | L/R asymmetry | ⚠️ |
| 034 | 10 µm + nozzle | cell = 10 µm, nozzle | 100% | 0% | ✅ |
| 035 | Extended settling | t₁_end = 0.8 s | 100% | 0% | ✅ |
| 036 | Low viscosity | η₀ = 7.5 Pa·s | 55% | Drainage | ❌ |
| 037 | Reduced surface tension | σ = 35 mN/m | 100% | 0% | ✅ |
| 038 | Fast nozzle | v_lat = 5 mm/s | 90% | Dam symmetry | ⚠️ |

---

## 9. Physical Insights

1. **Nozzle positioning dominates.** L/R asymmetry is kinematic (dispensing timing), not due to material properties. Offsetting the nozzle (case 025) corrects the asymmetry.

2. **Mesh resolution is critical.** 10 µm resolves capillary details (die edge, 25-30 µm Au pads). At 15-20 µm, the interface is pixelated and asymmetries are numerical artifacts.

3. **Dam height matters more than contact angle.** A physical barrier (0.8-1.0 mm) is more effective than a high contact angle for preventing overflow.

4. **Viscosity tolerates a wide range.** Between 7.5 and 50 Pa·s, encapsulation works. Below 7.5 Pa·s, gravity drainage becomes problematic (case 036).

5. **The regime is two-phase.** During dispensing (Ca ~ 1), rheology drives the flow; during settling (Ca → 0.1), capillarity takes over. Both phases must be simulated.

6. **cAlpha = 0 is non-negotiable.** Enabling artificial compression (cAlpha = 1) renders contact angles inoperable. The diffuse interface (~5-7 cells) is the price for correct physics.
