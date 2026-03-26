**Contents:**
1. Scientific and Industrial Context
2. Properties of Shear-Thinning Fluids
3. Numerical Modeling Challenges
4. Physical System Studied
5. Multi-Model Approach
6. Bibliographical References

---

# Modeling of Shear-Thinning Fluid Dispensing

## 1. Scientific and Industrial Context

### 1.1 Microfluidic Dispensing Technologies

Microfluidic dispensing encompasses a set of techniques for controlled deposition of volumes ranging from nanoliters to microliters. These processes find applications in numerous industrial fields:

- Electrochemical sensor fabrication: ink deposition for reference electrode, conductive electrode, chemical or biochemical functionalization...
- Printed electronics: conductive circuits, RFID antennas, module packaging...
- Functional coatings and thin films.
- Precision pharmaceutical dosing.

### 1.2 Physical Mechanisms

Fluid dispensing involves several coupled physical phenomena:
- **Two-phase flow**: fluid/air interaction at the interface.
- **Capillarity**: surface tension and wall wetting.
- **Rheology**: non-Newtonian behavior of complex fluids.
- **Interface dynamics**: deformation, spreading, pinch-off.

---

## 2. Properties of Shear-Thinning Fluids

### 2.1 Non-Newtonian Behavior

Shear-thinning fluids are **non-Newtonian fluids** whose apparent viscosity decreases under shear stress. This behavior is essential for dispensing: the fluid flows easily under pressure but maintains its shape at rest.

**Power law (Ostwald-de Waele):**

$$\tau = K\dot{\gamma}^n \quad \text{with } n < 1$$

where $\tau$ is the shear stress, $K$ the consistency index, $\dot{\gamma}$ the shear rate, and $n$ the behavior index.

### 2.2 Carreau-Yasuda Model

$$\eta(\dot{\gamma}) = \eta_\infty + \frac{\eta_0 - \eta_\infty}{[1 + (k\dot{\gamma})^a]^{(1-n)/a}}$$

where $\eta_0$ and $\eta_\infty$ are the zero-shear and infinite-shear viscosities, and $k$, $a$ are fitting parameters.

**Example:** A shear-thinning ink can exhibit $\eta_0 = 0.5$-$15$ Pa·s (at rest) and $\eta_\infty = 0.05$ Pa·s under high shear.

---

## 3. Numerical Modeling Challenges

### 3.1 Technical Issues

| Challenge | Description | Approach |
|-----------|-------------|----------|
| **Interface tracking** | Capture fluid/air interface deformation | VOF, Phase-Field, Level-Set |
| **Complex rheology** | Model non-Newtonian behavior | Constitutive laws (Carreau, Herschel-Bulkley) |
| **Wetting** | Handle dynamic contact angles | Specific boundary conditions |
| **Multi-scale** | From micron (interface) to millimeter (well) | Adaptive meshes, meshless methods |
| **Computational cost** | Expensive 2D or 3D transient simulations | GPU, parallelization, hybrid methods |

---

## 4. Physical System Studied

### 4.1 Geometric Configuration

The modeled system consists of:
- **Dispensing nozzle**: diameter 200-350 µm, positioned above the micro-via.
- **Micro-via**: diameter 800-1500 µm, depth ~130 µm.
- **Fluid**: shear-thinning ink ($\rho$ = 3000 kg/m³).
- **Environment**: ambient temperature (~20°C) and atmospheric pressure.

### 4.2 Simulation Parameters

| Parameter | Range | Unit |
|-----------|-------|------|
| Micro-via diameter | 800 - 1500 | µm |
| Nozzle diameter | 200 - 350 | µm |
| Horizontal offset (nozzle vs well center) | 0, -75, -150 | µm |
| Vertical offset (nozzle vs well top) | -30, 0, 30, 60 | µm |
| Zero-shear viscosity $\eta_0$ | 0.5, 1.5, 5 | Pa·s |
| Viscosity $\eta_\infty$ | 0.05 - 0.5 | Pa·s |
| Wall contact angle | 15 - 120 | ° |
| Micro-via bottom contact angle | 15 - 65 | ° |
| Substrate contact angle (plateau) | 15 - 120 | ° |
| Dispensing time | 20 - 40 | ms |

---

## 5. Multi-Model Approach

This project compares three complementary numerical methods:

| Model | Approach | Main Advantage |
|-------|----------|----------------|
| **VOF** | Eulerian, finite volumes | Robustness, industrial reference (used by Airbus, Danone, Volkswagen, Siemens...) |
| **LBM** | Mesoscopic, lattice | GPU performance, complex geometries |
| **SPH** | Lagrangian, meshless | Free surfaces, large deformations |

---

## 6. Bibliographical References

> **Note**: For the complete list of references, see the **Bibliographical References** section in the Appendices menu.
