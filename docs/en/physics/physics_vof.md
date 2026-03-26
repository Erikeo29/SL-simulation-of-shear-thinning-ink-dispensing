**Contents:**
1. Method Principle
2. Fundamental Equations
3. Mathematical Formulation
4. Advantages and Limitations
5. Computational Cost
6. Open-Source Libraries
7. Bibliographical References

---

## 1. Method Principle

The **VOF (Volume of Fluid)** method is an Eulerian approach for interface tracking in two-phase flows. It represents the industrial standard for free surface simulations, particularly with OpenFOAM's `interFoam` solver.

### Main Variable: Volume Fraction α

| Value | Meaning |
|-------|---------|
| α = 1 | Ink (fluid 1) |
| α = 0 | Air (fluid 2) |
| 0 < α < 1 | Interface zone |

**Key Advantage:** Perfect mass conservation, intrinsic property of the formulation.

---

## 2. Fundamental Equations

### 2.1 Navier-Stokes Equations

**Mass conservation:**
$$\nabla \cdot \mathbf{v} = 0$$

**Momentum conservation:**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot \boldsymbol{\tau} + \rho\mathbf{g} + \mathbf{f}_\sigma$$

where:
- $\mathbf{v}$ = velocity vector (m/s)
- $\rho$ = mixture density (kg/m³)
- $p$ = pressure (Pa)
- $\boldsymbol{\tau}$ = viscous stress tensor (Pa)
- $\mathbf{g}$ = gravitational acceleration (m/s²)
- $\mathbf{f}_\sigma$ = volumetric surface tension force (N/m³)

### 2.2 α Transport Equation

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

where:
- $\alpha$ = volume fraction (0 = air, 1 = ink)
- $\mathbf{v}$ = velocity vector

**With artificial compression (MULES - OpenFOAM):**
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\mathbf{v} \alpha) + \nabla \cdot [\mathbf{v}_r \alpha (1-\alpha)] = 0$$

where:
- $\mathbf{v}_r$ = $c_\alpha |\mathbf{v}| \mathbf{n}$, artificial compression velocity
- $c_\alpha$ = compression coefficient (typically 1 in OpenFOAM)
- $\mathbf{n}$ = interface normal ($\nabla \alpha / |\nabla \alpha|$)
- The $\alpha(1-\alpha)$ term ensures compression acts only at the interface

### 2.3 Surface Tension Force (CSF)

The **Continuum Surface Force** model by Brackbill:

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

where:
- $\sigma$ = surface tension coefficient (N/m)
- $\kappa$ = $-\nabla \cdot (\nabla \alpha / |\nabla \alpha|)$, interface curvature (m$^{-1}$)
- $\nabla \alpha$ = volume fraction gradient (localizes the interface)

---

## 3. Mathematical Formulation

### 3.1 Mixture Properties

Physical properties are linearly interpolated:

$$\rho = \alpha \rho_1 + (1-\alpha) \rho_2$$
$$\eta = \alpha \eta_1 + (1-\alpha) \eta_2$$

where:
- $\alpha$ = volume fraction (0 = air, 1 = ink)
- $\rho_1$, $\rho_2$ = densities of ink and air (kg/m³)
- $\eta_1$, $\eta_2$ = dynamic viscosities of ink and air (Pa·s)

### 3.2 Carreau Model (Non-Newtonian Fluids)

$$\eta_{eff}(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) [1 + (\lambda \dot{\gamma})^2]^{(n-1)/2}$$

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Density | ρ | 3000 | kg/m³ |
| Zero-shear viscosity | η₀ | 0.5 - 5 | Pa·s |
| Infinite-shear viscosity | η∞ | 0.05 - 0.15 | Pa·s |
| Relaxation time | λ | 0.15 | s |
| Power-law index | n | 0.7 | - |
| Surface tension | σ | 0.04 | N/m |

### 3.3 OpenFOAM Configuration (`transportProperties`)

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

## 4. Advantages and Limitations

| Advantages | Limitations |
|------------|-------------|
| Proven robustness (>25 years) | Numerical interface diffusion |
| Perfect mass conservation | Fine meshes required near interface |
| Industrial standard (OpenFOAM) | Multiple coalescences difficult |
| Interface precision 0.1-1 µm (with PLIC) | Complex rheology (thixotropy) difficult |
| GPU support since OpenFOAM 10 (not achieved in this project)| Memory cost for AMR |

---

## 5. Computational Cost

**Reference domain:** 1.2 mm × 0.5 mm (micro-via dispensing)

| Configuration | Cells | Resolution | Time | Hardware |
|---------------|-------|------------|------|----------|
| **This project** | ~50k | ~5 µm | **0.5-2 h** | 6 cores |
| High resolution | ~500k | ~1.5 µm | 4-8 h | 16 cores |
| With AMR | 50k-500k | 1-10 µm (adaptive) | 2-4 h | 16 cores |

> **Interpretation:** 50k hexahedral cells on 1.2×0.5 mm correspond to ~5 µm resolution, compatible with PLIC interface reconstruction.

**GPU Acceleration:** x5-x10 for matrix operations (OpenFOAM ≥ v10 with CUDA).

---

## 6. Open-Source Libraries

| Library | Language | Focus | Parallelization |
|---------|----------|-------|-----------------|
| **OpenFOAM** | C++ | Industrial standard, VOF/interFoam | MPI, CUDA |
| **Basilisk** | C | Research, native AMR | MPI |
| **Gerris** | C | Basilisk precursor | MPI |

---

## 7. Bibliographical References

> **Note**: For the complete list of references, see the **Bibliographical References** section in the Appendices menu.
