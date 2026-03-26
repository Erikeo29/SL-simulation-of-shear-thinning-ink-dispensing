# PySPH Code - Smoothed Particle Hydrodynamics (SPH)

This page presents the SPH implementation using the **PySPH** library (code written in Python).

---

## 1. Code Structure

The project uses PySPH to define equations and the solver. Configuration is managed via YAML files.

```
project_directory/
├── templates/
│   └── pysph/
│       └── droplet_spreading.py   # Main simulation script
├── config/
│   └── base_parameters.yaml       # Default parameters
├── scripts/                       # Visualization utilities
└── results/                       # Output files (.npz)
```

---

## 2. Configuration (`base_parameters.yaml`)

This file centralizes physical and numerical parameters. It is shared between VOF and SPH simulations to ensure consistency.

```yaml
# config/base_parameters.yaml

sph:
  dx: 1.0e-5              # Particle spacing (10 µm)
  hdx: 1.3                # Smoothing/spacing ratio
  c0: 10.0                # Artificial speed of sound

surface:
  sigma: 0.040            # Surface tension (N/m)

rheology:
  eta0: 1.5               # Zero-shear viscosity
  n: 0.5                  # Shear-thinning index

contact_angles:
  substrate: 35           # Bottom (hydrophilic)
  wall_isolant_left: 15   # Left wall
```

**Key points:**
- **dx**: Defines spatial resolution (characteristic particle size).
- **c0**: Numerical speed of sound for the WCSPH (Weakly Compressible SPH) scheme.
- **sigma**: Physical surface tension.

---

## 3. Main Class (`DropletSpreading`)

The simulation is encapsulated in a class derived from PySPH's `Application`. It configures the solver, particles, and equations.

```python
# templates/pysph/droplet_spreading.py

class DropletSpreading(Application):
    def initialize(self):
        # Default parameters
        self.dx = 1e-5
        self.rho_ink = 3000.0
        self.scheme_name = 'morris'  # Surface tension scheme

    def create_particles(self):
        # Creation of fluid and solid particles
        # ...
        return [fluid, solid]

    def create_equations(self):
        # Definition of forces and interactions
        # ...
        return equations
```

**Key points:**
- **Application**: Manages the PySPH simulation lifecycle (particle creation, equation configuration, solver execution, result saving).
- **Morris Scheme**: Used for surface tension (robust for high density ratios).

---

## 4. Contact Angle Management (`CavityAdhesionForce`)

Unlike classical methods, we use an explicit adhesion force to impose the contact angle on complex cavity walls.

```python
class CavityAdhesionForce(Equation):
    """Applies an adhesion force to impose the contact angle."""

    def initialize(self, d_idx, d_x, d_y, d_h, d_au, d_av, d_scolor):
        # Apply only at interface (scolor ~ 0.5)
        if 0.05 <= d_scolor[d_idx] <= 0.95:
            # Calculate distance to wall
            dist_to_bottom = d_y[d_idx] - self.y_bottom
            
            if dist_to_bottom < self.delta * h:
                # Force proportional to cosine of contact angle
                F_mag = self.alpha * self.sigma * abs(self.cos_theta) / h
                
                # Direction: spread or retract based on hydrophilicity
                if self.cos_theta > 0: # Hydrophilic
                    d_au[d_idx] += direction * F_mag
                else: # Hydrophobic
                    d_au[d_idx] -= direction * F_mag
```

**Key points:**
- **Adhesion Force**: Simulates the triple line tension.
- **Complex Geometry**: Handles bottom, vertical walls, and platforms distinctly.
- **cos_theta**: Determines if the force favors spreading (>0) or retraction (<0).

---

## 5. Rheology (Carreau Model)

Similar to LBM, each particle's viscosity is dynamically updated based on the local strain rate.

```python
class CarreauViscosity(Equation):
    def loop(self, d_idx, d_nu, d_strain_rate):
        gamma_dot = d_strain_rate[d_idx]

        # Carreau Model
        factor = 1.0 + (self.lam * gamma_dot)**2
        exponent = 0.5 * (self.n - 1.0)
        
        # Local dynamic viscosity
        eta = self.eta_inf + (self.eta0 - self.eta_inf) * (factor ** exponent)

        # Convert to kinematic viscosity
        d_nu[d_idx] = eta / self.rho0
```

**Key points:**
- **Particle-based**: Each particle carries its own viscosity.
- **ComputeStrainRate**: Prerequisite equation that estimates the strain tensor $\dot{\gamma}$ via SPH gradients.

---

## 6. Equation Assembly (`create_equations`)

The `create_equations` method assembles all physical models into sequential groups.

```python
def create_equations(self):
    equations = [
        # Group 1: Density
        Group(equations=[SummationDensity(dest='fluid', sources=['fluid', 'solid'])]),

        # Rheology Group (optional)
        Group(equations=[
            ComputeStrainRate(...),
            CarreauViscosity(...)
        ]) if self.use_carreau else Group(),

        # Surface Tension & Adhesion Group
        Group(equations=[
            MorrisColorGradient(...),
            ShadlooYildizSurfaceTensionForce(...),
            CavityAdhesionForce(...)
        ]),

        # Momentum Group
        Group(equations=[
            MomentumEquationPressureGradient(...),
            MomentumEquationViscosity(...),
        ])
    ]
    return equations
```

**Key points:**
- **Groups**: Define the execution order of forces.
- **Modularity**: Allows toggling rheology or cavity geometry on/off.

---

## 7. Solver Configuration and Time Step

The solver is configured to use an adaptive or fixed time step based on CFL (Courant-Friedrichs-Lewy), viscous, and capillary criteria.

```python
# templates/pysph/droplet_spreading.py

def consume_user_options(self):
    # Time step criteria calculation
    dt_cfl = 0.25 * self.h0 / (1.1 * self.c0)
    dt_viscous = 0.125 * self.h0**2 / max(self.nu, 1e-10)
    dt_surface = np.sqrt(self.rho0 * self.h0**3 / (2 * np.pi * max(self.sigma, 1e-10)))
    
    # Choose most restrictive step
    self.dt = 0.5 * min(dt_cfl, dt_viscous, dt_surface)

def create_solver(self):
    # Predictor-corrector integrator
    integrator = PECIntegrator(fluid=TransportVelocityStep())

    solver = Solver(
        kernel=QuinticSpline(dim=2),
        integrator=integrator,
        dt=self.dt,
        tf=self.tf,
        pfreq=100  # Save frequency
    )
    return solver
```

**Key points:**
- **Stability**: The time step must satisfy multiple physical conditions simultaneously.
- **Integrator**: Uses an efficient explicit scheme (PEC).

---

## 8. Post-processing and Metrics

The script includes an automatic post-processing step to calculate the spreading diameter over time.

```python
# Spreading metrics calculation
def _compute_spreading_metrics(self):
    times = []
    spreading_diameters = []

    for sd, arrays in iter_output(self.output_files, 'fluid'):
        # Filter droplet particles (color > 0.5)
        mask = pa.color > 0.5
        x_drop = pa.x[mask]
        
        # Diameter = Xmax - Xmin
        spread = x_drop.max() - x_drop.min()
        
        times.append(t)
        spreading_diameters.append(spread)

    # Save results
    np.savez('spreading_metrics.npz', time=times, spreading=spreading_diameters)
```

**Key points:**
- **Automatic Metrics**: Facilitates quantitative comparison with other models (VOF, FEM).
- **Masking**: Distinguishes the droplet from the surrounding air.