**Contents:**
1. Conclusion
2. Perspectives
   - 2.1 Open Source Python Alternatives
   - 2.2 Artificial Intelligence and Hybrid Modeling
   - 2.3 4D Printing and Smart Inks
   - 2.4 Research Opportunities
   - 2.5 Quantum Computing
3. Bibliographical References

---

## 1. Conclusion

This study enabled the modeling of shear-thinning ink dispensing into micro-via using three distinct numerical methods: VOF, LBM, and SPH.

The most realistic results were obtained using the VOF method (OpenFOAM), close to what can be expected from physics and from what commercial modeling tools can produce. Notably, the impact of nozzle position along the X-axis on overflow phenomena and filling uniformity was demonstrated. Similarly, expected physicochemical phenomena were reproduced: the influence of viscosity and contact angles (surface energy) on ink spreading corresponds to anticipated physical behaviors.

Differences in results nevertheless appear depending on the models used, which is expected given their very different numerical formulations (Eulerian vs Lagrangian, mesh-based vs meshless, macroscopic vs mesoscopic).

To go further, it would be necessary to continue improving the codes, refine the physicochemical models (particularly rheology and dynamic wetting) and optimize numerical parameters to improve result accuracy compared to experimental expectations.

---

## 2. Perspectives

### 2.1 Open Source Python Alternatives

The failure of the initial FEM/Phase-Field implementation (based on an attempt to reproduce commercial models) highlighted the need for robust Python tools for advanced fluid mechanics modeling. The following packages could help create modeling codes in Python, which remains a simpler tool to evolve than the OpenFOAM C++ environment:

- **Firedrake**: an automated system for solving partial differential equations using the finite element method. High performance for computational fluid dynamics (CFD), it offers a syntax close to mathematics (UFL).
- **SfePy (Simple Finite Elements in Python)**: a flexible library for solving coupled partial differential equation systems (mechanical, thermal, fluids) using finite elements. Ideal for complex multiphysics problems.
- **Hybrid FEM/SPH Systems**: a promising approach consists of coupling the precision of finite elements (FEM) near solid walls with the flexibility of SPH (Smoothed Particle Hydrodynamics) for free surfaces.

### 2.2 Artificial Intelligence and Hybrid Modeling

### PINN (Physics-Informed Neural Networks)

**PINNs** allow combining physical equations with neural networks to accelerate simulations:

- **Principle:** the network learns to solve Navier-Stokes equations by minimizing both data error and physical equation violation.
- **Inkjet application:** Raissi et al. (2020) used PINNs to solve Navier-Stokes with precision comparable to FEM but 100× faster.
- **Current limitation:** limited generalization outside the training domain (no reliable extrapolation).

### Surrogate Models

**Surrogate models** involve training a "simplified AI" (like a neural network) to instantly predict the outcome of a complex simulation:

- **Principle:** a few hundred real simulations (VOF, LBM...) are performed to "show" the model how the fluid reacts.
- **Advantage:** once trained, the model can predict the dispensing shape in milliseconds, without having to run a multi-hour OpenFOAM calculation.
- **Potential:** real-time optimization of parameters on a production line.

### Reinforcement Learning

- **Principle:** it involves training a computer program, called an **"agent"**, to make the best possible decisions to achieve a goal. The agent learns through trial and error, being "rewarded" for good actions (e.g., a successful dispense) and "punished" for bad ones (an overflow).
- **Application:** an agent could learn to dynamically adjust the nozzle's pressure or speed to ensure an optimal fill, even if the ink's properties change slightly.
- **Tools:** open-source libraries like `Stable-Baselines3` (based on PyTorch) or `Ray RLlib` (for large-scale systems) are used to implement these algorithms.
- **Potential:** enable machines to self-correct in real-time and adapt to variations in ink or the environment without human intervention.

---

### 2.3 4D Printing and Smart Inks

Shear-thinning inks are increasingly used for **4D printing** (materials that change shape after printing):

### Shape-Memory Inks

- Polymers that deform under temperature or light.
- **Modeling:** FEM coupling with thermomechanical models.


---

### 2.4 Research Opportunities

### Rheology-Interface Coupling

**Problem:** no model in the literature simultaneously handles non-Newtonian rheology (thixotropy) and free interfaces with sub-micron precision.

**Research directions:**
- **VOF-SPH hybridization:** VOF for interface tracking, SPH for rheology.
- **LBM with advanced rheology:** implement thixotropy and viscoelasticity models in LBM.
- **Adaptive FEM:** dynamic meshes that adapt to high-shear zones.

### Sub-Micron Scales

**Problem:** droplets < 5 µm are difficult to model due to dominant surface tension effects and prohibitive computation times.

**Research directions:**
- **Multi-scale models:** couple a macroscopic model (VOF, FEM) with a mesoscopic model (LBM).
- **Atomistic simulations:** use molecular dynamics (MD) for droplets < 1 µm.

---

### 2.5 Quantum Computing

Quantum computing could revolutionize complex flow modeling:

### Quantum Algorithms for SPH

- quantum computers could simulate 10⁹ SPH particles in real-time.
- **Example:** IBM demonstrated (2023) a quantum algorithm for molecular dynamics, applicable to SPH.

### Mesh Optimization

- Quantum algorithms could reduce the cost of 3D adaptive meshes.

---

## 3. Bibliographical References

> **Note**: For references discussing the resources used in this project, see the **Bibliographical References** section in the Appendices menu.
