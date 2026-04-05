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
| Dam (barrier) | 0.5 × 1.04 mm (×2) | Epoxy compound |
| Nozzle | Ø 0.6 mm, mobile (4 phases) | Steel + PTFE (exterior). |
| PCB | Total width 3.0 mm | FR-4 + solder mask |
| Mesh | ~28,500 hex cells | 15 µm resolution (10 µm for production). |

---

## 3. Rheology: Bird-Carreau Model

The glob top resin is a **shear-thinning** fluid: its viscosity decreases under shear. The Bird-Carreau model captures both viscosity plateaus:

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[1 + (\lambda \dot{\gamma})^2\right]^{(n-1)/2}$$

| Parameter | Symbol | Reference value | Unit |
|-----------|--------|----------------|------|
| Zero-shear viscosity | η₀ | 15 | Pa·s |
| Infinite-shear viscosity | η∞ | 1.0 | Pa·s |
| Relaxation time | λ | 10 | s |
| Shear-thinning index | n | 0.4 | - |
| Density | ρ | 1600 | kg/m³ |

**Note:** η₀ = 15 Pa·s corresponds to process temperature (70-80°C). At 25°C, η₀ ≈ 50 Pa·s (datasheet). The simulation uses the value at process temperature.

**Physical interpretation:**
- **At rest** (γ̇ → 0): η → η₀ = 15 Pa·s → resin stays in place (no gravity drainage).
- **Under the nozzle** (γ̇ ~ 100 s⁻¹): η → η∞ = 1 Pa·s → resin flows easily.
- **After dispensing** (γ̇ → 0): η rises → slow, controlled capillary self-leveling.

The resin/air viscosity ratio is extreme: **1.5×10⁶**. This contrast requires careful numerical treatment (implicit solver for viscous diffusion).

---

## 4. Surface Tension and Wettability

### 4.1 Surface tension

$\sigma$ = 0.035 N/m (35 mN/m, epoxy resin / air at process temperature, uncured)

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

**Reference conditions:** U = 3.5 mm/s (v_disp, dispensing velocity), L = 0.6 mm (nozzle Ø), η₀ = 15 Pa·s (T_process).

| Number | Expression | Value | Interpretation |
|--------|-----------|-------|----------------|
| **Re** | ρUL/η₀ | 2×10⁻⁴ | Pure Stokes: inertia completely negligible. |
| **Ca** | η₀U/σ | 1.5 | Viscous ≈ capillary during dispensing. |
| **Bo** | ρgL²/σ | 0.16 | Gravity negligible. |
| **Oh** | η₀/√(ρσL) | 82 | Very viscous (no oscillations). |

**Two-phase regime (4 phases):**
- **Phases 1-3: dispensing** (Ca ~ 1.5): viscous and capillary forces are comparable → flow shape depends on rheology AND wettability.
- **Phase 4: settling** (Ca → 0): capillarity dominates → self-leveling, resin spreads on hydrophilic surfaces.

This two-phase character (viscous dispensing → capillary settling) is the key physical signature of the process.

**Mobile nozzle sequence (2.8 s total):**
1. Phase 1 [0 - 0.05 s]: stationary deposit at x = -1.1 mm (left side).
2. Phase 2 [0.05 - 0.49 s]: translation from -1.1 to +1.1 mm at v_lat = 5 mm/s.
3. Phase 3 [0.49 - 1.29 s]: stationary deposit at x = +1.1 mm (0.8 s).
4. Phase 4 [1.29 - 2.8 s]: nozzle retracted, capillary relaxation (1.5 s).

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
- endTime: 2.8 s (1.29 s dispensing + 1.51 s settling).

---

## 8. Parametric Study (3 axes)

The parametric study covers 7 cases (039-045), organized around 3 axes with case 039 as reference.

**Reference case (039):** v_disp = 3.5 mm/s, v_lat = 5.0 mm/s, η₀ = 15 Pa·s. Result: optimal filling, dome ~1.4 mm, dispensed volume 2.71 mm².

| ID | Axis | Varied parameter | V_disp (mm²) | Delta vol. | Verdict |
|----|------|-----------------|-------------|-----------|---------|
| **039** | **Reference** | - | **2.71** | - | Optimal. |
| 040 | v_disp | 2.0 mm/s (-43%) | 1.55 | -43% | Under-fill, die exposed. |
| 041 | v_disp | 5.0 mm/s (+43%) | 3.87 | +43% | Over-fill, massive dome. |
| 042 | v_lat | 3.5 mm/s (slow) | 3.11 | +15% | Good symmetry, slight surplus. |
| 043 | v_lat | 7.5 mm/s (fast) | 2.40 | -11% | Slight right asymmetry. |
| 044 | η₀ | 5 Pa·s (fluid) | 2.71 | 0% | Identical final result. |
| 045 | η₀ | 25 Pa·s (viscous) | 2.71 | 0% | Identical final result. |

---

## 9. Physical Insights

1. **Dispensing flow rate (v_disp) is the primary lever.** Dispensed volume is strictly proportional to v_disp (V = v_disp × nozzle_Ø × t_dispense). A ±43% flow rate variation produces ±43% volume change. Process window: 3.0-4.0 mm/s.

2. **Lateral velocity (v_lat) has an indirect effect via traverse time.** A slower nozzle (v_lat = 3.5 mm/s) takes longer to cross the die → longer total dispensing time → more volume (+15%). It is not the lateral distribution that changes, but the total volume.

3. **Viscosity (η₀) does not affect the final result** in the 5-25 Pa·s range. The settling phase (1.5 s) is long enough for capillarity to homogenize the final shape regardless of viscosity. Favorable consequence: process temperature does not need to be tightly controlled.

4. **The regime is two-phase.** During dispensing (Ca ~ 1.5), rheology drives the flow; during settling (Ca → 0), capillarity takes over. Both phases must be simulated.

5. **cAlpha = 0 is non-negotiable.** Enabling artificial compression (cAlpha = 1) renders contact angles inoperable. The diffuse interface (~5-7 cells) is the price for correct physics.

6. **Sensitivity hierarchy:** v_disp (±43%) >> v_lat (±15%) >> η₀ (0%).
