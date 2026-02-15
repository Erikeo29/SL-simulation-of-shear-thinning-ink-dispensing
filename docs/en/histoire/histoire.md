**Contents:**
1. Fathers of Fluid Mechanics
2. Rheology Pioneers
3. Founders of Statistical Mechanics
4. Creators of Numerical Methods
5. Inventors of Modern Methods
6. Chronological Table
7. Scientific Lineage Diagram
8. Bibliographical References

This fluid dispensing simulation project builds upon centuries of scientific discoveries. This page pays tribute to the scientists whose foundational work made modern numerical modeling of two-phase flows possible.

---

## 1. Fathers of Fluid Mechanics

### Claude-Louis Navier (1785-1836)

**Nationality:** French | **Field:** Engineering, Fluid Mechanics

Claude Louis Marie Henri Navier was born in Dijon on February 10, 1785. Orphaned at 8, he was raised by his great-uncle Emiland Gauthey, chief engineer of Ponts et Chaussées. This family influence directed his career toward engineering.

**Education:** École Polytechnique (1802), École des Ponts et Chaussées (1804-1806)

**Major contribution:** In **1821-1822**, Navier formulated the equations of motion for viscous fluids, generalizing Euler's equations to include internal friction effects. Remarkably, he obtained the correct equations despite incomplete understanding of shear stress physics, by modeling intermolecular forces.

**Related works:** Suspension bridge theory, material elasticity, Seine bridge construction.

**Legacy:** His name is inscribed on the Eiffel Tower. The existence and regularity problem for Navier-Stokes solutions remains one of the 7 Millennium Prize Problems (prize: 1 million USD).

---

### Sir George Gabriel Stokes (1819-1903)

**Nationality:** Irish/British | **Field:** Mathematics, Physics

Born in Skreen, Ireland, Stokes was one of the greatest scientists of the 19th century. An anecdote tells that his interest in fluid dynamics arose when he nearly got swept away by a wave while swimming off the Sligo coast.

**Education:** Pembroke College, Cambridge - Senior Wrangler (top of class)

**Career:** Lucasian Chair of Mathematics at Cambridge (1849-1903), the same chair held by Newton and Hawking.

**Major contributions:**
- **1845:** Rigorous reformulation of Navier's equations with derivation based on shear stresses
- Stokes' theorem (vector calculus)
- Stokes' law (viscous drag on a sphere)
- Discovery and naming of **fluorescence**

**Unit:** The **stokes** (St), unit of kinematic viscosity, bears his name.

---

### Osborne Reynolds (1842-1912)

**Nationality:** Irish/British | **Field:** Engineering, Hydrodynamics

Born in Belfast, Reynolds inherited a keen interest in mechanics from his father, Reverend Osborne Reynolds. In 1868, he became the first professor of engineering at Owens College (now University of Manchester).

**Landmark experiment (1883):** Reynolds injected a stream of colored dye into water flowing through a glass tube. At low velocity, the stream remained distinct (laminar). Beyond a critical velocity, it fragmented (turbulent). This experiment defined the laminar-turbulent transition.

**The Reynolds Number:**
$$Re = \frac{\rho v L}{\mu}$$

Critical value: $Re \approx 2000$ for pipes.

**Other contributions:** Lubrication theory (1886), Reynolds stresses in turbulence, turbine pumps.

---

### Moritz Weber (1871-1951)

**Nationality:** German | **Field:** Naval mechanics

Professor of naval mechanics at Technische Hochschule Berlin-Charlottenburg, Weber formalized in 1919 the principles of mechanical similitude for scale ship models.

**The Weber Number:**
$$We = \frac{\rho v^2 L}{\sigma}$$

This number compares inertial forces to surface tension forces. Crucial for droplet formation and fluid dispensing.

---

### Wolfgang von Ohnesorge (1901-1976)

**Nationality:** German | **Field:** Metrology, Fluid Physics

Descended from Prussian General Blücher (victor over Napoleon at Waterloo), Ohnesorge followed an unusual career: he was never a university professor but rather director of the Weights and Measures Bureau of North Rhine-Westphalia.

**Doctoral thesis (1936):** Ohnesorge developed an operational diagram distinguishing liquid jet breakup regimes.

**The Ohnesorge Number:**
$$Oh = \frac{\mu}{\sqrt{\rho \sigma L}} = \frac{\sqrt{We}}{Re}$$

**Direct application:** In inkjet, fluids are "ejectable" for $0.1 < Oh < 1.0$.

---

## 2. Rheology Pioneers

### Isaac Newton (1643-1727)

**Nationality:** English | **Field:** Physics, Mathematics

The universal genius of science. Besides gravitation and calculus, Newton established in 1687 the fundamental law of viscosity in his *Principia Mathematica*.

**Newton's law for fluids:**
$$\tau = \mu \dot{\gamma}$$

A fluid whose viscosity $\mu$ is constant is called **Newtonian**. Water, air, and mineral oils are Newtonian.

---

### Wilhelm Ostwald (1853-1932) & Arnulph de Waele

**Nationality:** Ostwald: German (born in Riga, then Russian Empire) | **Field:** Physical chemistry, Rheology

Wilhelm Ostwald received the **Nobel Prize in Chemistry in 1909** for his work on catalysis and chemical equilibria.

**Power law (Ostwald-de Waele):**
$$\eta(\dot{\gamma}) = K \dot{\gamma}^{n-1}$$

This law describes **shear-thinning** ($n < 1$) and **shear-thickening** ($n > 1$) fluids.

---

### Pierre J. Carreau (born 1939)

**Nationality:** Canadian | **Field:** Chemical engineering, Polymer rheology

Professor emeritus at École Polytechnique de Montréal, Pierre Carreau founded CRASP (later merged into CREPEC in 2002). He earned his doctorate from the University of Wisconsin in 1968.

**The Carreau Model (1972):**
$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty)[1 + (\lambda\dot{\gamma})^2]^{(n-1)/2}$$

This model avoids the power law singularity at zero shear thanks to the $\eta_0$ and $\eta_\infty$ plateaus.

**Distinctions:** Fellow of the Royal Society of Canada (2006), Honorary Doctorate from Université Joseph Fourier de Grenoble (1989).

---

### Winslow H. Herschel & Ronald Bulkley

**Era:** 1920s | **Field:** Rheology

In 1926, Herschel and Bulkley studied the consistency of rubber solutions in benzene and proposed a model for **yield stress fluids**:

**Herschel-Bulkley Model:**
- If $|\tau| \leq \tau_0$: no flow (solid)
- If $|\tau| > \tau_0$: $\tau = \tau_0 + K\dot{\gamma}^n$

This model combines a yield stress with nonlinear post-flow behavior. It applies to high solid-loading inks, pastes, drilling muds, etc.

---

## 3. Founders of Statistical Mechanics

### Ludwig Boltzmann (1844-1906)

**Nationality:** Austrian | **Field:** Theoretical physics

Born in Vienna, Boltzmann is the father of statistical mechanics. His revolutionary work established that thermodynamic laws are **probabilistic** in nature: entropy measures the number of microscopic states compatible with a macroscopic state.

**Boltzmann Equation (1872):**
$$\frac{\partial f}{\partial t} + \mathbf{v} \cdot \nabla f = \Omega(f)$$

This equation describes the evolution of the particle distribution function and forms the foundation of the LBM method.

**Entropy formula:** $S = k \log W$ (engraved on his tombstone in Vienna)

**Tragedy:** Boltzmann suffered from depression and committed suicide in 1906, shortly before his theories were fully accepted. Einstein and Planck confirmed his ideas a few years later.

---

### James Clerk Maxwell (1831-1879)

**Nationality:** Scottish | **Field:** Theoretical physics

Maxwell is considered by Einstein as the most influential physicist of the 19th century. Beyond unifying electricity, magnetism, and optics, he fundamentally contributed to the kinetic theory of gases.

**Maxwell-Boltzmann Distribution (1860):**

Maxwell was the first to conceive that gas molecules don't all have the same velocity but follow a statistical distribution. This revolutionary idea introduced the concept of **probability in physics**.

**Director of the Cavendish Laboratory** at Cambridge (1871-1879).

---

### Prabhu Lal Bhatnagar (1912-1976), Eugene P. Gross (1926-1991) & Max Krook (1913-1985)

**Nationalities:** Indian, American, South African/American | **Field:** Theoretical physics

**The BGK operator (1954):**
$$\Omega_i = -\frac{1}{\tau}(f_i - f_i^{eq})$$

This brilliant simplification of the Boltzmann collision operator replaces the complex integral with linear relaxation toward equilibrium. It is at the heart of all modern LBM implementations.

The relaxation time $\tau$ is directly related to kinematic viscosity: $\nu = c_s^2(\tau - 1/2)\Delta t$.

---

## 4. Creators of Numerical Methods

### Boris Galerkin (1871-1945)

**Nationality:** Russian/Soviet | **Field:** Mechanics, Applied mathematics

Born into a poor family in present-day Belarus, Galerkin studied at the St. Petersburg Technological Institute while working to support himself.

**Remarkable fact:** An active revolutionary, he was imprisoned in 1906 at Kresty prison where he wrote his first scientific paper (130 pages)!

**The Galerkin Method (1915):**

This method transforms a differential equation into an algebraic system by projecting onto a space of test functions. It is the theoretical basis of the **Finite Element Method (FEM)**.

**Legacy:** The USSR created prizes and scholarships in his name for work in elasticity and structural mechanics.

---

### John W. Cahn (1928-2016) & John E. Hilliard (1926-1987)

**Nationality:** American | **Field:** Materials science

Born in Cologne (Germany) in a Jewish family that fled Nazism, John Cahn earned his doctorate at Berkeley (1953) and worked at General Electric, then MIT and NIST.

**The Cahn-Hilliard Equation (1958):**
$$\frac{\partial \phi}{\partial t} = \gamma \nabla^2 \left( \frac{\delta \mathcal{F}}{\delta \phi} \right)$$

This equation describes **spinodal decomposition**: how two alloy components spontaneously separate into distinct phases.

**Impact:** The equation is at the core of **Phase-Field** methods used for interface tracking in this project.

**Distinctions:** National Medal of Science (1998), Kyoto Prize (2011).

---

### Vitaly Ginzburg (1916-2009) & Lev Landau (1908-1968)

**Nationality:** Soviet/Russian | **Field:** Theoretical physics

**Lev Landau** is considered one of the last universal physicists of the 20th century, having contributed to almost every domain of theoretical physics. He received the **Nobel Prize in Physics in 1962** for his theory of superfluidity.

**Vitaly Ginzburg** received the **Nobel Prize in Physics in 2003** for his contributions to superconductivity.

**Ginzburg-Landau Theory (1950):**

This phenomenological theory introduces the concept of **order parameter** $\phi$ and **free energy**:
$$\mathcal{F}[\phi] = \int \left[ \frac{\varepsilon}{2}|\nabla\phi|^2 + \frac{1}{4\varepsilon}(1-\phi^2)^2 \right] d\Omega$$

In this project, this free energy governs the evolution of the ink/air interface in the Phase-Field method.

---

## 5. Inventors of Modern Methods

### Cyril W. Hirt & Billy D. Nichols

**Nationality:** American | **Era:** 1981 | **Institution:** Los Alamos National Laboratory

**The VOF (Volume of Fluid) Method:**

In 1981, Hirt and Nichols published the foundational VOF method paper: *"Volume of Fluid (VOF) Method for the Dynamics of Free Boundaries"* in the Journal of Computational Physics.

The key idea: track the interface via a volume fraction $\alpha$ transported by the flow:
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

This method is today the **industry standard** for two-phase flows (OpenFOAM, Fluent, etc.).

---

### Xiaowen Shan (born ~1960) & Hudong Chen

**Nationality:** Chinese/American | **Institution:** Los Alamos / Dartmouth College

**The Shan-Chen Model (1993):**

In 1993, Shan and Chen proposed a lattice Boltzmann model for multiphase flows based on an interaction **pseudopotential**:
$$\mathbf{F}_{int} = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i)\mathbf{c}_i$$

This model automatically generates phase separation and surface tension without explicit interface tracking.

**Xiaowen Shan** was elected Fellow of the American Physical Society in 2009. He has worked at Microsoft, Exa Corp., and COMAC (Chinese aircraft manufacturer).

---

### Joseph J. Monaghan (born ~1940)

**Nationality:** Australian | **Institution:** Monash University

**The SPH Method (1977):**

In 1977, Monaghan and R.A. Gingold (simultaneously with L.B. Lucy) invented the **Smoothed Particle Hydrodynamics (SPH)** method to simulate star formation.

The revolutionary idea: represent the fluid with mobile particles, without mesh:
$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

**Current applications:** Free surface flows, jet breakup, splashes, violent impacts.

Monaghan has published over 150 papers and two major reviews in *Annual Review of Astronomy and Astrophysics* (1992) and *Annual Review of Fluid Mechanics* (2012).

---

## 6. Chronological Table

| Period | Scientist | Contribution | Application in this project |
|--------|-----------|--------------|----------------------------|
| 1687 | Newton | Viscosity law | Newtonian fluids |
| 1821-1845 | Navier, Stokes | N-S equations | All methods |
| 1860-1872 | Maxwell, Boltzmann | Kinetic theory | LBM |
| 1883 | Reynolds | Reynolds number | Flow analysis |
| 1915 | Galerkin | Galerkin method | FEM |
| 1919-1936 | Weber, Ohnesorge | We, Oh numbers | Ejectability criteria |
| 1926 | Herschel-Bulkley | Yield stress fluids | High-loading inks |
| 1950 | Ginzburg-Landau | Free energy | Phase-Field |
| 1954 | Bhatnagar-Gross-Krook | BGK operator | LBM |
| 1958 | Cahn-Hilliard | Phase separation | Phase-Field, FEM |
| 1972 | Carreau | Rheological model | Shear-thinning inks |
| 1977 | Monaghan, Gingold, Lucy | SPH | SPH method |
| 1981 | Hirt, Nichols | VOF | OpenFOAM |
| 1993 | Shan, Chen | Multiphase model | Two-phase LBM |

---

## 7. Scientific Lineage Diagram

```
NEWTON (1687)
    │
    ├─────────────────────────────────────────┐
    │                                         │
EULER (1755)                           OSTWALD (1890s)
    │                                         │
    ├─────────────┐                     CARREAU (1972)
    │             │                     HERSCHEL-BULKLEY
NAVIER (1821)   STOKES (1845)                 │
    │             │                           │
    └──────┬──────┘                   RHEOLOGICAL MODELS
           │                                  │
    NAVIER-STOKES                             │
           │                                  │
    ┌──────┼──────────────────────────────────┼─────────────┐
    │      │                                  │             │
REYNOLDS  GALERKIN          MAXWELL-BOLTZMANN        WEBER-OHNESORGE
(1883)    (1915)                  (1860-1872)             (1919-1936)
    │         │                        │                       │
    │    FINITE ELEMENTS          BOLTZMANN                    │
    │         │                   (1872)                       │
    │    CAHN-HILLIARD                │                        │
    │    (1958)                  BGK (1954)                    │
    │         │                        │                       │
    │    GINZBURG-LANDAU         SHAN-CHEN               DISPENSING
    │    (1950)                  (1993)                  CRITERIA
    │         │                        │                       │
    └─────────┴────────────────────────┴───────────────────────┘
              │                        │
         PHASE-FIELD                  LBM
              │                        │
              │                        │
    MONAGHAN (1977)          HIRT-NICHOLS (1981)
              │                        │
             SPH                      VOF
              │                        │
              └────────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         THIS PROJECT              INDUSTRIAL
    Shear-Thinning Ink              APPLICATIONS
         Dispensing
```

---

## 8. Bibliographical References

> **Note**: For the complete list of technical references, see the **Bibliographical References** section in the Appendices menu.
