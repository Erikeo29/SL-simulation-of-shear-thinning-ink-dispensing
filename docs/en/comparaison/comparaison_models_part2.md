---

## 3. Critical Analysis by Model

### 3.1 VOF (Volume of Fluid)

Eulerian method where each cell contains a volume fraction $\alpha \in [0,1]$. The interface is geometrically reconstructed via the PLIC algorithm (Piecewise Linear Interface Construction).

| Advantages | Limitations |
|------------|-------------|
| Rigorous mass conservation | Numerical diffusion at fine interfaces |
| Industry standard for 30 years | Memory cost for fine meshes |
| Extensive documentation and community | Droplet coalescence difficult |
| Software: OpenFOAM (open-source), Fluent (commercial) | |

---

### 3.2 LBM (Lattice Boltzmann Method)

Mesoscopic method solving the discretized Boltzmann equation on a regular grid (D2Q9, D3Q19). Macroscopic quantities (velocity, pressure) are obtained through statistical moment computation.

| Advantages | Limitations |
|------------|-------------|
| Exceptional GPU parallelization (factor ×10-20) | Artificial compressibility (constraint Ma < 0.1) |
| Local algorithm (each node independent) | Sub-micron precision difficult |
| No complex mesh generation required | Delicate rheological calibration |
| Software: Palabos (open-source), waLBerla | Less extensive documentation than VOF |

---

### 3.3 SPH (Smoothed Particle Hydrodynamics)

Meshless Lagrangian method. The fluid is discretized into particles whose properties are interpolated via smoothing kernels (cubic spline, Wendland). It is optimized for GPU computing and primarily designed for free-surface flows (fluid-structure interactions, coastal engineering, waves).

| Advantages | Limitations |
|------------|-------------|
| No mesh: no distortion issues | Numerical noise in pressure fields |
| Natural coalescence and fragmentation | Tensorial instabilities at high velocity |
| Suited for large deformations | Lower industrial maturity |
| Software: PySPH (Python), DualSPHysics (C++/CUDA) | High memory cost in 3D |

---

## 4. Hardware Requirements

### 4.1 Computation times (this project's simulations)

Times below correspond to the reference case: droplet dispensing into a micro-via (1.2×0.5 mm domain, 100-200 ms physical time), standard 8-core PC.

| Model | Discretization | Resolution | Time | Notes |
|-------|----------------|------------|------|-------|
| **VOF** | ~50k cells | ~5 µm | **0.5-2 h** | Optimized C++ OpenFOAM |
| **LBM** | 240×100 nodes | 5 µm | **~10 min** | Efficient parallelization (GPU) |
| **SPH** | ~1k particles | 15-20 µm | **1-2 h** | PySPH |

### 4.2 Indicative configurations

| Range | Typical configuration | Indicative budget | Usage |
|-------|----------------------|-------------------|-------|
| **Standard PC** | 6-12 cores, 16-32 GB RAM | €800-1,500 | Simple VOF/LBM, 2D SPH, 2D FEM |
| **Upgraded PC** | 12-16 cores, 32-64 GB RAM, GPU 8 GB | €1,500-3,000 | 3D VOF, parametric studies |
| **Server** | 32+ cores, 128+ GB RAM | €5,000-15,000 | Large study series |
| **Cloud** | AWS, Google Cloud, Azure | €1-5/h | Intensive one-off calculations |

### 4.3 Practical remarks

- **LBM** efficiently exploits GPUs: a consumer graphics card significantly accelerates computations.
- **VOF** runs on standard PCs for 2D cases.
- Cloud can be useful for 3D studies or large parametric series.

---

## 5. Summary Table

| Criterion | VOF | LBM | SPH |
|-----------|-----|-----|-----|
| **Interface precision** | 0.1-1 µm | 0.2-2 µm | 0.5-5 µm |
| **Time per unit simulation (this project)** | 0.5-2 h | ~10 min | 1-2 h |
| **Mass conservation** | Rigorous | Approximate | By summation |
| **Carreau rheology** | Native | Implementable | Implementable |
| **Learning curve** | Steep (C++, CLI) | Steep (specific physics) | Medium (Python) |
| **Industrial maturity** | Very high | Medium | Developing |
| **Software cost** | OpenFOAM free | Palabos free | PySPH free |

### Recommendations by application context

| Context | Recommended method | Justification |
|---------|-------------------|---------------|
| Industrial production | VOF (OpenFOAM) | Proven robustness, large community |
| Intensive parametric studies | LBM (Palabos) | Optimal GPU performance |
| Fundamental research | SPH (PySPH) | Flexibility for new physics |

---

## 6. Bibliographical References

> For the complete list of scientific references, see the **Bibliographical References** section in the Appendices menu.
