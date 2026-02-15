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

The **LBM (Lattice Boltzmann Method)** is a **mesoscopic** approach that does not directly solve the Navier-Stokes equations, but rather the **discretized Boltzmann equation** on a regular lattice.

### Main Variable: Distribution Functions f_i

We track the evolution of distribution functions f_i(**x**, t) representing the probability of finding particles at position **x** moving along discrete directions **c**_i.

Macroscopic quantities are obtained through **statistical moments**:

$$\rho = \sum_i f_i \quad \text{and} \quad \rho \mathbf{u} = \sum_i f_i \mathbf{c}_i$$

where:
- $f_i$ = distribution function in direction $i$
- $\rho$ = macroscopic density (kg/m³)
- $\mathbf{u}$ = macroscopic velocity (m/s)
- $\mathbf{c}_i$ = discrete velocity vector in direction $i$

**Key Advantage:** Massive GPU parallelization (each node is independent).

---

## 2. Fundamental Equations

### 2.1 Discrete Boltzmann Equation (BGK)

$$f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = -\frac{1}{\tau}(f_i - f_i^{eq}) + F_i$$

where:
- $f_i(\mathbf{x}, t)$ = distribution function at node $\mathbf{x}$, direction $i$, time $t$
- $\mathbf{c}_i$ = discrete velocity vector in direction $i$
- $\Delta t$ = time step
- $\tau$ = relaxation time (controls viscosity)
- $f_i^{eq}$ = Maxwell-Boltzmann equilibrium distribution
- $F_i$ = external force term (gravity, Shan-Chen)

### 2.2 Equilibrium Distribution

$$f_i^{eq} = w_i \rho \left[1 + \frac{\mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{(\mathbf{c}_i \cdot \mathbf{u})^2}{2c_s^4} - \frac{\mathbf{u}^2}{2c_s^2}\right]$$

where:
- $w_i$ = quadrature weight for direction $i$
- $\rho$ = density
- $\mathbf{c}_i$ = discrete velocity vector
- $\mathbf{u}$ = macroscopic velocity
- $c_s$ = $1/\sqrt{3}$, lattice speed of sound (in lattice units)

### 2.3 Viscosity - Relaxation Time Relationship

$$\nu = c_s^2 \left(\tau - \frac{1}{2}\right) \Delta t$$

where:
- $\nu$ = kinematic viscosity (m²/s)
- $c_s$ = lattice speed of sound
- $\tau$ = relaxation time (must be > 0.5 for stability)
- $\Delta t$ = time step

This relationship allows modeling fluids of different viscosities by adjusting τ.

---

## 3. Mathematical Formulation

### 3.1 Discretization Grids (DdQq)

The **DdQq** notation denotes a grid with **d** spatial dimensions and **q** discrete propagation velocities. These velocities define the directions in which particle populations move at each time step.

| Grid | Dimensions | Velocities | Application |
|------|------------|------------|-------------|
| **D2Q9** | 2D | 9 | 2D standard |
| **D3Q19** | 3D | 19 | 3D standard (good compromise) |
| **D3Q27** | 3D | 27 | High precision |

**This project's choice:** D2Q9 with Δx = 5 µm

### 3.2 Shan-Chen Multiphase Model

The interparticle force models interactions between fluids:

$$\mathbf{F}_{int}(\mathbf{x}) = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i \Delta t) \mathbf{c}_i$$

where:
- $G$ = coupling constant (controls surface tension)
- $\psi(\mathbf{x})$ = pseudopotential (function of local density)
- $w_i$ = quadrature weights
- $\mathbf{c}_i$ = discrete velocity vector

**Surface tension:** σ ∝ G(ψ_max - ψ_min)²

### 3.3 Non-Newtonian Fluids

For shear-thinning fluids, τ depends locally on the shear rate:

$$\tau(\dot{\gamma}) = \frac{1}{2} + \frac{\nu(\dot{\gamma})}{c_s^2 \Delta t}$$

where:
- $\tau$ = local relaxation time (spatially variable)
- $\dot{\gamma}$ = local shear rate (s$^{-1}$)
- $\nu(\dot{\gamma})$ = shear-dependent kinematic viscosity (Carreau model)

### 3.4 Wetting Management

Contact angles are managed through a **fictitious density** at solid nodes:

$$\rho_{solid} = \rho_0 + \Delta \rho \cdot \cos(\theta_{eq})$$

where:
- $\rho_{solid}$ = fictitious density assigned to solid nodes
- $\rho_0$ = reference fluid density
- $\Delta \rho$ = modulation amplitude
- $\theta_{eq}$ = desired equilibrium contact angle

Wetting is handled naturally without explicit boundary conditions.

---

## 4. Advantages and Limitations

| Advantages | Limitations |
|------------|-------------|
| Exceptional GPU scalability (x20) | Artificial compressibility (Ma < 0.1) |
| Intrinsic parallelization | Spurious currents at interfaces |
| Natural wetting (complex geometries) | Delicate rheological calibration |
| Automatic coalescence/breakup | GPU memory limiting in 3D |
| Interface precision ~1 µm | Limited density ratio (~1000, actual ink/air = 2500) |

---

## 5. Computational Cost

**Reference domain:** 1.2 mm × 0.5 mm (micro-via dispensing)

| Configuration | Grid | Δx | Time | Hardware |
|---------------|------|-----|------|----------|
| **This project** | 240×100 | 5 µm | **~10 min** | 6 cores |
| High resolution | 1200×500 | 1 µm | 1–2 h | GPU |
| 3D (D3Q19) | 300³ | 4 µm | 1–2 h | 1× GPU |

> **Interpretation:** A 240×100 grid with Δx = 5 µm exactly covers the 1.2×0.5 mm domain. LBM is particularly fast due to its regular structure optimized for parallelism.

**GPU Scalability:** Near-linear up to 16 GPUs. ~16 GB for 300³ nodes in D3Q19.

---

## 6. Open-Source Libraries

| Library | Language | GPU | Focus |
|---------|----------|-----|-------|
| **Palabos** | C++ | None | Open-source reference, tutorials |
| **OpenLB** | C++ | CUDA/OpenMP | Industrial applications |
| **waLBerla** | C++ | CUDA | Extreme HPC, millions of cores |
| **Sailfish** | Python/CUDA | Native CUDA | Python interface |

---

## 7. Bibliographical References

> **Note**: For the complete list of references, see the **Bibliographical References** section in the Appendices menu.
