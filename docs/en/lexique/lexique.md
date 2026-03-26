**Contents:**

**A. Physics**

1. SI Units and Prefixes
2. Dimensionless Numbers
3. Physical Symbols
4. Rheology Terms
5. Fluid Mechanics Terms

**B. Numerical Methods**

6. Method Acronyms
7. Numerical Scheme Acronyms
8. Numerical Terms
9. Software and Libraries

**C. Hardware and Formats**

10. Hardware Acronyms
11. File Formats and Data

**D. Techniques and Applications**

12. Dispensing Processes
13. Experimental Characterization
14. Couplings and Artificial Intelligence

---

# A. Physics

## 1. SI Units and Prefixes

| Quantity | Unit | Symbol |
|----------|------|--------|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Force | newton | N |
| Pressure | pascal | Pa |
| Dynamic viscosity | pascal-second | Pa·s |
| Surface tension | newton per meter | N/m |
| Energy | joule | J |
| Power | watt | W |

### Prefixes

| Prefix | Symbol | Factor |
|--------|--------|--------|
| micro | µ | 10$^{-6}$ |
| milli | m | 10$^{-3}$ |
| kilo | k | 10$^{3}$ |
| mega | M | 10$^{6}$ |
| giga | G | 10$^{9}$ |
| tera | T | 10$^{12}$ |

---

## 2. Dimensionless Numbers

| Symbol | Name | Expression | Physical Meaning |
|--------|------|------------|------------------|
| $Re$ | Reynolds | $\frac{\rho v L}{\eta}$ | Inertia / Viscosity |
| $We$ | Weber | $\frac{\rho v^2 L}{\sigma}$ | Inertia / Surface tension |
| $Oh$ | Ohnesorge | $\frac{\eta}{\sqrt{\rho \sigma L}}$ | Viscosity / (Inertia × Capillarity)$^{1/2}$ |
| $Ca$ | Capillary | $\frac{\eta v}{\sigma}$ | Viscosity / Capillarity |
| $Bo$ | Bond | $\frac{\rho g L^2}{\sigma}$ | Gravity / Capillarity |
| $De$ | Deborah | $\lambda \dot{\gamma}$ | Relaxation time × Shear rate |
| $Ma$ | Mach | $\frac{v}{c_s}$ | Velocity / Speed of sound |

---

## 3. Physical Symbols

### Fluid Properties

| Symbol | Name | SI Unit |
|--------|------|---------|
| $\rho$ | Density | kg/m³ |
| $\eta$, $\mu$ | Dynamic viscosity | Pa·s |
| $\nu$ | Kinematic viscosity | m²/s |
| $\sigma$ | Surface tension | N/m |
| $\theta$ | Contact angle | ° or rad |

### Rheological Parameters

| Symbol | Name | Model | Unit |
|--------|------|-------|------|
| $\eta_0$ | Zero-shear viscosity | Carreau | Pa·s |
| $\eta_\infty$ | Infinite-shear viscosity | Carreau | Pa·s |
| $\lambda$ | Relaxation time | Carreau, Oldroyd-B | s |
| $n$ | Flow behavior index | Power law | - |
| $K$ | Consistency | Power law | Pa·s$^n$ |
| $\tau_0$ | Yield stress | Herschel-Bulkley | Pa |
| $\dot{\gamma}$ | Shear rate | All | s$^{-1}$ |

### Flow Variables

| Symbol | Name | Unit |
|--------|------|------|
| $\mathbf{v}$, $\mathbf{u}$ | Velocity vector | m/s |
| $p$ | Pressure | Pa |
| $\mathbf{D}$ | Rate of deformation tensor | s$^{-1}$ |
| $\boldsymbol{\tau}$ | Stress tensor | Pa |
| $\kappa$ | Interface curvature | m$^{-1}$ |

---

## 4. Rheology Terms

| Term | Definition |
|------|------------|
| **Shear-thinning** | Fluid whose viscosity decreases with shear |
| **Shear-thickening** | Fluid whose viscosity increases with shear |
| **Thixotropy** | Time-dependent viscosity (restructuring) |
| **Viscoelasticity** | Behavior combining viscosity and elasticity |
| **Newtonian fluid** | Constant viscosity independent of shear |
| **Non-Newtonian fluid** | Shear-dependent viscosity |
| **Yield stress** | Flow threshold stress |

---

## 5. Fluid Mechanics Terms

| Term | Definition |
|------|------------|
| **Two-phase flow** | Flow involving two phases (e.g., liquid/gas) |
| **Interface** | Separation surface between two phases |
| **Capillarity** | Phenomenon related to surface tension |
| **Wetting** | Fluid-solid interaction characterized by contact angle |
| **Meniscus** | Interface curvature at wall contact |
| **Pinch-off** | Filament necking before breakup |
| **Satellite** | Secondary droplet formed during breakup |
| **Coalescence** | Merging of two droplets |

---

# B. Numerical Methods

## 6. Method Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **FEM** | Finite Element Method | Finite element method |
| **VOF** | Volume of Fluid | Eulerian interface tracking method |
| **LBM** | Lattice Boltzmann Method | Lattice Boltzmann method |
| **SPH** | Smoothed Particle Hydrodynamics | Smoothed particle hydrodynamics |
| **CFD** | Computational Fluid Dynamics | Computational fluid mechanics |
| **DNS** | Direct Numerical Simulation | Direct numerical simulation |

---

## 7. Numerical Scheme Acronyms

| Acronym | Full Name | Context |
|---------|-----------|---------|
| **PLIC** | Piecewise Linear Interface Calculation | VOF interface reconstruction |
| **CSF** | Continuum Surface Force | Surface tension model |
| **BGK** | Bhatnagar-Gross-Krook | LBM collision operator |
| **MRT** | Multiple Relaxation Time | Multi-relaxation LBM scheme |
| **SUPG** | Streamline Upwind Petrov-Galerkin | FEM convection stabilization |
| **PSPG** | Pressure Stabilizing Petrov-Galerkin | FEM pressure stabilization |
| **GLS** | Galerkin Least-Squares | Combined FEM stabilization |
| **ALE** | Arbitrary Lagrangian-Eulerian | Moving mesh |
| **AMR** | Adaptive Mesh Refinement | Adaptive meshing |
| **CFL** | Courant-Friedrichs-Lewy | Time stability condition (Co = vΔt/Δx ≤ 1) |
| **MULES** | Multidimensional Universal Limiter | OpenFOAM limiter for VOF |
| **DFSPH** | Divergence-Free Smoothed Particle Hydrodynamics | Incompressible SPH solver (Bender & Koschier 2015) |

---

## 8. Numerical Terms

| Term | Definition |
|------|------------|
| **Eulerian** | Fixed reference frame (fixed grid) |
| **Lagrangian** | Moving reference frame (follows particles) |
| **Mesh** | Spatial discretization of the domain |
| **Meshless** | Method without fixed connectivity (e.g., SPH) |
| **Weak formulation** | Integral form of equations (finite elements) |
| **Test function** | Weighting function in weak formulation |
| **DOF** | Degrees of Freedom |
| **Inf-sup condition** | LBB stability criterion for mixed elements |

---

## 9. Software and Libraries

| Name | Type | Language | Method |
|------|------|----------|--------|
| **FEniCS** | Open-source | Python/C++ | FEM |
| **Firedrake** | Open-source | Python/C++ | Automated FEM |
| **UFL** | Open-source | Python | Unified Form Language (variational syntax for FEniCS/Firedrake) |
| **SfePy** | Open-source | Python | Multiphysics FEM |
| **FiPy** | Open-source | Python | FVM, Phase-Field |
| **Dedalus** | Open-source | Python | Spectral methods |
| **OpenFOAM** | Open-source | C++ | VOF, FVM |
| **Palabos** | Open-source | C++ | LBM |
| **PySPH** | Open-source | Python | SPH |
| **COMSOL** | Commercial | GUI/MATLAB | Multiphysics FEM |
| **Ansys Fluent** | Commercial | GUI | VOF, FVM |
| **DualSPHysics** | Open-source | C++/CUDA | SPH GPU |
| **SPlisHSPlasH** | Open-source | C++/CUDA | SPH GPU (DFSPH solver, Akinci 2013 surface tension) |
| **waLBerla** | Open-source | C++ | LBM HPC |

---

# C. Hardware and Formats

## 10. Hardware Acronyms

| Acronym | Full Name | Description |
|---------|-----------|-------------|
| **CPU** | Central Processing Unit | Central processor |
| **GPU** | Graphics Processing Unit | Graphics processor |
| **HPC** | High Performance Computing | High performance computing |
| **CUDA** | Compute Unified Device Architecture | NVIDIA GPU API |
| **MPI** | Message Passing Interface | Distributed parallelization |
| **OpenMP** | Open Multi-Processing | Shared memory parallelization |
| **TFLOPS** | Tera Floating-Point Operations Per Second | Computing power unit |
| **RAM** | Random Access Memory | Main memory |

## 11. File Formats and Data

| Extension | Full Name | Description |
|-----------|-----------|-------------|
| **XML** | eXtensible Markup Language | Structured configuration file (Palabos parameters) |
| **CSV** | Comma-Separated Values | Tabular text file (parameter → result mappings) |
| **JSON** | JavaScript Object Notation | Structured data exchange format (configurations) |
| **GIF** | Graphics Interchange Format | Animated image (simulation animations) |
| **PNG** | Portable Network Graphics | Lossless image (final states) |
| **JPG/JPEG** | Joint Photographic Experts Group | Lossy compressed image |
| **SVG** | Scalable Vector Graphics | Vector image |
| **STL** | STereoLithography | 3D surface mesh (triangles) |
| **MSH** | GMSH Mesh | Volume mesh generated by GMSH |
| **GEO** | GMSH Geometry | GMSH geometry script (domain and mesh definition) |
| **VTK/VTI/VTU/VTP** | Visualization Toolkit | ParaView formats for post-processing (grids, data) |
| **XDMF** | eXtensible Data Model and Format | Metadata for FEM result visualization (FEniCSx) |
| **HDF5** (.h5) | Hierarchical Data Format | Large numerical data storage |
| **NPY/NPZ** | NumPy Array | Serialized Python numerical data |
| **PKL** | Pickle | Python object serialization |
| **PY** | Python Script | Python source code (PySPH, FEniCSx, post-processing) |
| **CPP** | C++ Source | C++ source code (OpenFOAM, Palabos) |
| **YAML/YML** | YAML Ain't Markup Language | Human-readable configuration (CI/CD, Docker) |

---

# D. Techniques and Applications

## 12. Dispensing Processes

| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **DOD** | Drop-on-Demand | On-demand droplet ejection (piezo or thermal). Used for precision dispensing, bioprinting. |
| **CIJ** | Continuous Inkjet | Continuous jet with electrostatic deflection of unwanted droplets. Used for industrial marking. |

---

## 13. Experimental Characterization

| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **PIV** | Particle Image Velocimetry | Particle image velocimetry. 2D/3D velocity field measurement. |
| **OCT** | Optical Coherence Tomography | Optical coherence tomography. Non-invasive sub-surface imaging. |

---

## 14. Couplings and Artificial Intelligence

| Abbreviation | Full Name | Description |
|--------------|-----------|-------------|
| **FSI** | Fluid-Structure Interaction | Fluid-structure coupling. Interaction between flow and solid deformation. |
| **PINN** | Physics-Informed Neural Networks | Neural networks integrating physical equations as constraints. |
| **AI** | Artificial Intelligence | Machine learning techniques applied to simulation. |

