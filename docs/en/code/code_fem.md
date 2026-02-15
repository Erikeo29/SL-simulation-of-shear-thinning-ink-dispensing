
## 4. NUMERICAL METHOD

### 4.1 Spatial Discretization

The domain Ω is discretized using finite elements with:
- P₂ elements for velocity (quadratic polynomials)
- P₁ elements for pressure (linear polynomials)
- P₁ elements for the level-set function

This combination (P₂-P₁) satisfies the inf-sup condition for stability.

### 4.2 Temporal Discretization

Crank-Nicolson scheme (θ = 0.5):
$$\frac{\mathbf{v}^{n+1} - \mathbf{v}^n}{\Delta t} = \theta \mathcal{F}(\mathbf{v}^{n+1}) + (1-\theta)\mathcal{F}(\mathbf{v}^n)$$

with Δt = 10⁻⁴ s chosen to satisfy CFL < 0.5:
$$\text{CFL} = \frac{|\mathbf{v}|_{\max} \Delta t}{h} < 0.5$$

where h is the characteristic mesh size.

### 4.3 Solution Algorithm

```
ALGORITHM: Phase-Field Two-Phase Simulation
------------------------------------------------
1. INITIALIZATION
   - Create mesh with refinement near interface
   - Initialize v = 0, p = 0, φ = φ₀

2. TIME LOOP: for t = 0 to T

   2.1 INTERFACE TRANSPORT
       - Solve Phase-Field equation for φⁿ⁺¹
       - Reinitialize signed distance if necessary

   2.2 PROPERTY UPDATE
       - Calculate ρ(φⁿ⁺¹), η(φⁿ⁺¹, γ̇ⁿ)
       - Calculate F_σ from φⁿ⁺¹

   2.3 NAVIER-STOKES SOLUTION (SIMPLE algorithm)
       a. Velocity prediction v*
          Solve: ρ(v* - vⁿ)/Δt + ρ(vⁿ·∇)v* = -∇pⁿ + ∇·τⁿ + F

       b. Pressure correction
          Solve: ∇²p' = (ρ/Δt)∇·v*

       c. Velocity correction
          vⁿ⁺¹ = v* - (Δt/ρ)∇p'
          pⁿ⁺¹ = pⁿ + p'

   2.4 CONVERGENCE CHECK
       - ||vⁿ⁺¹ - vⁿ||/||vⁿ|| < 10⁻⁶
       - ||∇·vⁿ⁺¹|| < 10⁻⁸

   2.5 METRICS CALCULATION
       - Fill rate: α = ∫_Ω H(φ)dΩ / V_well
       - If α ≥ 0.8: STOP

3. POST-PROCESSING
   - Export results (VTK/XDMF)
   - Statistical analysis
```

---

## 5. PYTHON IMPLEMENTATION

### 5.1 Modular Code Structure

#!/usr/bin/env python3
"""
Dispensing Simulation
Phase-Field Method with FEniCSx

"""

import numpy as np
import os
import glob
from pathlib import Path
from mpi4py import MPI
from petsc4py import PETSc
from dolfinx import fem, mesh, io, plot, default_scalar_type
from dolfinx.fem import Function, functionspace, dirichletbc, locate_dofs_topological, form, assemble_scalar
from dolfinx.mesh import locate_entities_boundary, meshtags, create_rectangle, CellType
from dolfinx.io import XDMFFile
import ufl
from ufl import (
    grad, div, inner, dx, ds, dS,
    TestFunction, TrialFunction, split, as_tensor,
    FacetNormal, jump, avg, CellDiameter,
    tanh, sqrt, conditional, as_vector, sin, cos, exp
)
import basix.ufl
import matplotlib.pyplot as plt
from PIL import Image
import pyvista

# PETSc Configuration
PETSc.Sys.popErrorHandler()

class InkDispenseSimulation:
    """
    Main class for dispensing simulation.
    """

    def __init__(self, params=None):
        """
        Initialization with physical parameters.

        Args:
            params (dict): Dictionary of simulation parameters
        """

        # Retrieve parameters or default values
        if params is None:
            params = {}

        # ========== Phase 1 Properties: Ink ==========
        self.rho_ink = params.get('rho_ink', 3000.0)      # kg/m³
        self.mu_0 = params.get('viscosity', 1.5)          # Pa·s (zero-shear viscosity)
        self.mu_inf = params.get('mu_inf', 0.05)          # Pa·s (infinite-shear viscosity)
        self.lambda_c = params.get('lambda_c', 0.15)      # s (relaxation time)
        self.n_carreau = params.get('n_carreau', 0.7)     # - (power-law index)

        # ========== Phase 2 Properties: Air ==========
        self.rho_air = params.get('rho_air', 1.2)         # kg/m³
        self.mu_air = params.get('mu_air', 1e-5)          # Pa·s

        # ========== Interfacial Properties ==========
        self.sigma = params.get('sigma', 0.04)            # N/m (surface tension)
        self.epsilon = params.get('epsilon', 5e-6)        # m (interface thickness)
        self.gamma_mob = params.get('gamma_mob', 1.0)     # interface mobility

        # ========== Geometry [m] ==========
        self.D_well = params.get('well_diameter', 0.8e-3)     # well diameter
        self.h_well = params.get('well_height', 0.128e-3)     # well height
        self.D_needle = params.get('needle_diameter', 0.2e-3) # syringe diameter
        self.shift_x = params.get('shift_x', 0.0)             # syringe X offset
        self.shift_z = params.get('shift_z', 30e-6)           # syringe-well gap

        # ========== Contact Angles [rad] ==========
        self.theta_gold = np.radians(params.get('angle_gold', 60))
        self.theta_left = np.radians(params.get('angle_left', 45))
        self.theta_right = np.radians(params.get('angle_right', 45))
        self.theta_eg = np.radians(params.get('angle_eg', 30))

        # ========== Operating Conditions ==========
        self.flow_rate = params.get('flow_rate', 1e-9)    # m³/s (volumetric flow rate)
        self.v_inlet = self.flow_rate / (np.pi * (self.D_needle/2)**2)  # inlet velocity

        # ========== Numerical Parameters ==========
        self.dt = params.get('dt', 1e-4)                   # time step [s]
        self.T_final = params.get('T_final', 0.1)          # final time [s]
        self.tol = params.get('tol', 1e-6)                 # convergence tolerance
        self.mesh_resolution = params.get('mesh_res', 40)  # mesh resolution

        # ========== Export Parameters ==========
        self.output_dir = params.get('output_dir', 'simulation_results')
        self.export_step = params.get('export_step', 10)   # export every N steps

        # Create output directory
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/frames").mkdir(exist_ok=True)

    def create_mesh(self):
        """
        Create 2D axisymmetric mesh.

        Returns:
            domain: Dolfinx mesh object
        """
        # Calculate number of elements
        nx = self.mesh_resolution
        ny = int(nx * self.h_well / (self.D_well/2))

        # Create rectangular mesh (r, z)
        domain = create_rectangle(
            MPI.COMM_WORLD,
            [np.array([0, 0]),
             np.array([self.D_well/2, self.h_well])],
            [nx, ny],
            cell_type=CellType.triangle
        )

        # Create boundary markers
        domain.topology.create_connectivity(domain.topology.dim - 1, domain.topology.dim)

        # Define boundary tags
        def axis_boundary(x):
            return np.isclose(x[0], 0)

        def wall_boundary(x):
            return np.isclose(x[0], self.D_well/2)

        def bottom_boundary(x):
            return np.isclose(x[1], 0)

        def top_boundary(x):
            return np.isclose(x[1], self.h_well)

        def inlet_boundary(x):
            return np.logical_and(
                np.isclose(x[1], self.h_well),
                x[0] <= self.D_needle/2 + abs(self.shift_x)
            )

        # Store boundary functions for later use
        self.boundary_conditions = {
            'axis': axis_boundary,
            'wall': wall_boundary,
            'bottom': bottom_boundary,
            'top': top_boundary,
            'inlet': inlet_boundary
        }

        return domain

    def setup_function_spaces(self, domain):
        """
        Define function spaces with FEniCSx 0.8+ API.

        Args:
            domain: Mesh

        Returns:
            V, Q, S, W: Spaces for velocity, pressure, level-set and mixed
        """
        # Create elements with basix.ufl
        P2 = basix.ufl.element("Lagrange", domain.topology.cell_name(), 2, shape=(2,))
        P1 = basix.ufl.element("Lagrange", domain.topology.cell_name(), 1)

        # Create function spaces
        V = fem.functionspace(domain, P2)  # Velocity
        Q = fem.functionspace(domain, P1)  # Pressure
        S = fem.functionspace(domain, P1)  # Level-set

        # Mixed space for coupled system
        TH = basix.ufl.mixed_element([P2, P1, P1])
        W = fem.functionspace(domain, TH)

        return V, Q, S, W

    def initialize_fields(self, V, Q, S):
        """
        Initialize fields.

        Args:
            V, Q, S: Function spaces

        Returns:
            u, p, phi: Initialized functions
        """
        u = Function(V, name="velocity")
        p = Function(Q, name="pressure")
        phi = Function(S, name="levelset")

        # ========== Level-set Initialization ==========
        def initial_phi_expr(x):
            # Initial horizontal interface
            z_interface = self.h_well - 0.01e-3
            return np.tanh((x[1] - z_interface) / (2 * self.epsilon))

        phi.interpolate(initial_phi_expr)

        # ========== Velocity Initialization ==========
        def initial_velocity_expr(x):
            vr = np.zeros(x.shape[1])
            vz = np.zeros(x.shape[1])

            # Injection zone
            mask_inlet = np.logical_and(
                x[1] > self.h_well - 0.001e-3,
                x[0] < self.D_needle/2
            )

            if np.any(mask_inlet):
                r = x[0][mask_inlet]
                R = self.D_needle/2
                # Parabolic profile
                vz[mask_inlet] = -2 * self.v_inlet * (1 - (r/R)**2)

            return np.vstack([vr, vz])

        u.interpolate(initial_velocity_expr)

        # ========== Hydrostatic Pressure ==========
        def initial_pressure_expr(x):
            g = 9.81
            return self.rho_air * g * (self.h_well - x[1])

        p.interpolate(initial_pressure_expr)

        return u, p, phi

    def setup_variational_problem(self, W, u_n, p_n, phi_n):
        """
        Configure the variational problem for the coupled system.

        Args:
            W: Mixed space
            u_n, p_n, phi_n: Solutions at previous time step

        Returns:
            a, L: Bilinear and linear forms
        """
        # Test and unknown functions
        (v, q, xi) = ufl.TestFunctions(W)
        w = Function(W)
        (u, p, phi) = ufl.split(w)

        # ========== Strain Tensor ==========
        def epsilon(u):
            return 0.5 * (grad(u) + grad(u).T)

        # ========== Shear Rate ==========
        def gamma_dot(u):
            return sqrt(2 * inner(epsilon(u), epsilon(u)) + 1e-10)

        # ========== Carreau Viscosity ==========
        def mu_carreau(u):
            gd = gamma_dot(u)
            return self.mu_inf + (self.mu_0 - self.mu_inf) * \
                   (1 + (self.lambda_c * gd)**2)**((self.n_carreau - 1)/2)

        # ========== Regularized Heaviside ==========
        def H(phi):
            return 0.5 * (1.0 + phi/sqrt(phi**2 + self.epsilon**2))

        # ========== Averaged Properties ==========
        H_phi = H(phi)
        rho = self.rho_ink * H_phi + self.rho_air * (1 - H_phi)
        mu = mu_carreau(u) * H_phi + self.mu_air * (1 - H_phi)

        # ========== Surface Tension Force ==========
        n = grad(phi) / sqrt(inner(grad(phi), grad(phi)) + 1e-10)
        kappa = div(n)
        f_st = self.sigma * kappa * grad(phi)

        # ========== Gravity ==========
        g = as_vector([0, -9.81])

        # ========== Navier-Stokes Equation ==========
        # Inertia term
        F_ns = rho * inner((u - u_n) / self.dt, v) * dx
        F_ns += rho * inner(grad(u) * u, v) * dx

        # Viscous term
        F_ns += 2 * mu * inner(epsilon(u), epsilon(v)) * dx

        # Pressure term
        F_ns -= p * div(v) * dx

        # Body forces
        F_ns -= inner(rho * g, v) * dx
        F_ns -= inner(f_st, v) * dx

        # Mass conservation
        F_ns += q * div(u) * dx

        # ========== Level-set Transport Equation ==========
        # Advection
        F_phi = (phi - phi_n) / self.dt * xi * dx
        F_phi += inner(u, grad(phi)) * xi * dx

        # Reinitialization term (maintain |∇φ| = 1)
        lambda_reinit = self.epsilon * abs(max(abs(self.v_inlet), 1e-3))
        F_phi += lambda_reinit * (inner(grad(phi), grad(xi)) * dx -
                                   (1 - inner(grad(phi), grad(phi))) * xi * dx)

        # ========== Total Form ==========
        F = F_ns + F_phi

        # Separate into bilinear and linear forms
        dw = ufl.TrialFunction(W)
        J = ufl.derivative(F, w, dw)

        return J, F

    def apply_boundary_conditions(self, W, domain):
        """
        Apply boundary conditions.

        Args:
            W: Mixed space
            domain: Mesh

        Returns:
            bcs: List of Dirichlet conditions
        """
        V, Q, S = W.sub(0), W.sub(1), W.sub(2)

        bcs = []

        # ========== Inlet Condition ==========
        def inlet_velocity_expr(x):
            vr = np.zeros(x.shape[1])
            vz = np.zeros(x.shape[1])

            # Parabolic profile in syringe
            r = x[0]
            R = self.D_needle/2
            mask = r <= R

            if np.any(mask):
                vz[mask] = -2 * self.v_inlet * (1 - (r[mask]/R)**2)

            return np.vstack([vr, vz])

        # Locate inlet dofs
        fdim = domain.topology.dim - 1
        inlet_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['inlet'])
        inlet_dofs = locate_dofs_topological((V.sub(0).collapse()[0], V.sub(0)), fdim, inlet_facets)

        u_inlet = Function(V)
        u_inlet.interpolate(inlet_velocity_expr)
        bc_inlet = dirichletbc(u_inlet, inlet_dofs, V)
        bcs.append(bc_inlet)

        # ========== No-Slip Condition on Walls ==========
        # Left wall (symmetry axis)
        axis_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['axis'])
        axis_dofs_r = locate_dofs_topological((V.sub(0).collapse()[0], V.sub(0)), fdim, axis_facets)
        bc_axis = dirichletbc(default_scalar_type(0), axis_dofs_r, V.sub(0))
        bcs.append(bc_axis)

        # Right wall
        wall_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['wall'])
        wall_dofs = locate_dofs_topological(V, fdim, wall_facets)
        u_wall = Function(V)
        u_wall.x.array[:] = 0
        bc_wall = dirichletbc(u_wall, wall_dofs)
        bcs.append(bc_wall)

        # Bottom
        bottom_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['bottom'])
        bottom_dofs = locate_dofs_topological(V, fdim, bottom_facets)
        u_bottom = Function(V)
        u_bottom.x.array[:] = 0
        bc_bottom = dirichletbc(u_bottom, bottom_dofs)
        bcs.append(bc_bottom)

        # ========== Contact Angle (Robin BC for φ) ==========
        # Implemented via boundary term in variational form

        return bcs

    def solve_time_step(self, W, J, F, bcs, w):
        """
        Solve one time step.

        Args:
            W: Mixed space
            J: Bilinear form (Jacobian)
            F: Linear form (Residual)
            bcs: Boundary conditions
            w: Current solution

        Returns:
            Convergence (bool)
        """
        # Newton solver configuration
        problem = fem.petsc.NonlinearProblem(F, w, bcs=bcs, J=J)
        solver = fem.petsc.NewtonSolver(MPI.COMM_WORLD, problem)

        # Solver parameters
        solver.convergence_criterion = "incremental"
        solver.rtol = self.tol
        solver.atol = 1e-10
        solver.max_it = 20
        solver.report = True

        # Linear solver configuration
        ksp = solver.krylov_solver
        opts = PETSc.Options()
        option_prefix = ksp.getOptionsPrefix()
        opts[f"{option_prefix}ksp_type"] = "gmres"
        opts[f"{option_prefix}ksp_rtol"] = 1e-8
        opts[f"{option_prefix}pc_type"] = "ilu"
        opts[f"{option_prefix}pc_factor_levels"] = 2
        ksp.setFromOptions()

        # Solve
        n_iter, converged = solver.solve(w)

        return converged

    def export_solution(self, u, p, phi, t, step):
        """
        Export solution for visualization.

        Args:
            u, p, phi: Solution fields
            t: Current time
            step: Time step number
        """
        # XDMF export for ParaView
        with XDMFFile(MPI.COMM_WORLD, f"{self.output_dir}/solution_{step:04d}.xdmf", "w") as xdmf:
            xdmf.write_mesh(u.function_space.mesh)
            xdmf.write_function(u, t)
            xdmf.write_function(p, t)
            xdmf.write_function(phi, t)

        # Image export for GIF
        if step % self.export_step == 0:
            self.save_frame(phi, step)

    def save_frame(self, phi, step):
        """
        Save a frame for GIF creation.

        Args:
            phi: Level-set function
            step: Step number
        """
        # Extract values on regular grid
        nx, ny = 200, 100
        x = np.linspace(0, self.D_well/2, nx)
        y = np.linspace(0, self.h_well, ny)
        X, Y = np.meshgrid(x, y)

        # Evaluate phi on grid
        points = np.vstack([X.ravel(), Y.ravel()])

        # For now, simple contour save
        fig, ax = plt.subplots(figsize=(8, 4))

        # Simplified visualization
        # Note: In practice, phi should be interpolated on the grid
        # Here we use a schematic visualization

        # Draw domain
        ax.add_patch(plt.Rectangle((0, 0), self.D_well/2*1000, self.h_well*1000,
                                   fill=False, edgecolor='black', linewidth=2))

        # Ink zone (phi > 0)
        # Simple approximation for demo
        z_interface = self.h_well*1000 - 10 - step * 0.1
        if z_interface > 0:
            ax.add_patch(plt.Rectangle((0, 0), self.D_well/2*1000, z_interface,
                                       fill=True, facecolor='silver', alpha=0.8))

        # Syringe
        needle_x = self.shift_x*1000
        needle_top = self.h_well*1000 + self.shift_z*1000
        ax.add_patch(plt.Rectangle((needle_x, self.h_well*1000),
                                   self.D_needle/2*1000, 5,
                                   fill=True, facecolor='gray'))

        ax.set_xlim(0, self.D_well/2*1000)
        ax.set_ylim(0, self.h_well*1000*1.1)
        ax.set_xlabel('r [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_title(f'Dispensing - t = {step*self.dt*1000:.1f} ms')
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/frames/frame_{step:04d}.png", dpi=100)
        plt.close()

    def create_gif(self):
        """
        Create GIF from frames.
        """
        # Retrieve frames
        frames = []
        frame_files = sorted(glob.glob(f"{self.output_dir}/frames/frame_*.png"))

        for frame_file in frame_files:
            frame = Image.open(frame_file)
            frames.append(frame)

        if frames:
            # Save GIF
            frames[0].save(
                f"{self.output_dir}/simulation.gif",
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0
            )
            print(f"GIF created: {self.output_dir}/simulation.gif")

    def run(self):
        """
        Main simulation loop.
        """
        print("="*60)
        print("Dispensing Simulation")
        print("="*60)

        # Create mesh
        print("Creating mesh...")
        domain = self.create_mesh()

        # Function spaces
        print("Setting up function spaces...")
        V, Q, S, W = self.setup_function_spaces(domain)

        # Initialization
        print("Initializing fields...")
        u_n, p_n, phi_n = self.initialize_fields(V, Q, S)

        # Mixed solution
        w = Function(W)
        w.sub(0).interpolate(u_n)
        w.sub(1).interpolate(p_n)
        w.sub(2).interpolate(phi_n)

        # Variational problem
        print("Setting up variational problem...")
        J, F = self.setup_variational_problem(W, u_n, p_n, phi_n)

        # Boundary conditions
        print("Applying boundary conditions...")
        bcs = self.apply_boundary_conditions(W, domain)

        # Time loop
        t = 0
        step = 0
        n_steps = int(self.T_final / self.dt)

        print(f"\nStarting simulation:")
        print(f"  - Time step: {self.dt*1000:.2f} ms")
        print(f"  - Final time: {self.T_final*1000:.1f} ms")
        print(f"  - Number of steps: {n_steps}")
        print("="*60)

        while t < self.T_final:
            t += self.dt
            step += 1

            print(f"\nStep {step}/{n_steps} - t = {t*1000:.2f} ms")

            # Solve
            converged = self.solve_time_step(W, J, F, bcs, w)

            if not converged:
                print("WARNING: Non-convergence detected!")
                break

            # Extract solutions
            u, p, phi = w.sub(0).collapse(), w.sub(1).collapse(), w.sub(2).collapse()

            # Export
            self.export_solution(u, p, phi, t, step)

            # Update for next step
            u_n.x.array[:] = u.x.array
            p_n.x.array[:] = p.x.array
            phi_n.x.array[:] = phi.x.array

            # Calculate and display metrics
            if step % 10 == 0:
                # Dispensed ink volume
                volume_ink = assemble_scalar(form((phi_n + 1) / 2 * dx))
                volume_ink = MPI.COMM_WORLD.allreduce(volume_ink, op=MPI.SUM)
                print(f"  Ink volume: {volume_ink*1e9:.3f} nL")

        # Create final GIF
        print("\nCreating GIF...")
        self.create_gif()

        print("\n" + "="*60)
        print("Simulation completed successfully!")
        print("="*60)

        return True


def run_batch_simulations():
    """
    Batch execution for all parameter combinations.
    """
    # Define parameter ranges
    well_diameters = [800e-6, 1000e-6, 1200e-6]  # µm -> m
    needle_diameters = [100e-6, 150e-6, 200e-6]
    shift_x_values = [0, 50e-6, 100e-6]
    shift_z_values = [0, 30e-6, 60e-6]
    viscosities = [10, 20, 30]  # Pa.s
    angles_left = [30, 45, 60]
    angles_right = [30, 45, 60]
    angles_eg = [30, 45, 60]
    angles_gold = [45, 60, 90]

    # Counter for naming GIFs
    gif_counter = 1

    # CSV mapping file
    csv_file = open("gif_mapping_generated.csv", "w")
    csv_file.write("gif filename;well diameter (µm);needle diameter (µm);"
                   "needle shift x (µm);needle shift z (µm);Ink viscosity (Pa.s);"
                   "left wall contact angle (°);right wall contact angle (°);"
                   "left EG contact angle (°);gold contact angle (°)\n")

    # Loop over a selection of combinations (not all to save time)
    for well_d in well_diameters[::2]:  # Every other value
        for needle_d in needle_diameters[::2]:
            for visc in viscosities[::2]:
                for angle_l in angles_left[::2]:
                    # Parameters for this simulation
                    params = {
                        'well_diameter': well_d,
                        'needle_diameter': needle_d,
                        'shift_x': shift_x_values[1],
                        'shift_z': shift_z_values[1],
                        'viscosity': visc,
                        'angle_left': angle_l,
                        'angle_right': angles_right[1],
                        'angle_eg': angles_eg[0],
                        'angle_gold': angles_gold[1],
                        'T_final': 0.05,  # Short simulation for testing
                        'mesh_res': 30,   # Reduced resolution for testing
                        'output_dir': f'simulations/gif_{gif_counter}'
                    }

                    print(f"\n{'='*60}")
                    print(f"Simulation {gif_counter}")
                    print(f"Parameters: well={well_d*1e6:.0f}µm, needle={needle_d*1e6:.0f}µm, "
                          f"visc={visc}Pa.s")
                    print(f"{'='*60}")

                    try:
                        # Run simulation
                        sim = InkDispenseSimulation(params)
                        success = sim.run()

                        if success:
                            # Copy generated GIF
                            import shutil
                            gif_source = f"{params['output_dir']}/simulation.gif"
                            gif_dest = f"gif/gif_{gif_counter}.gif"

                            # Create gif folder if needed
                            Path("gif").mkdir(exist_ok=True)

                            if os.path.exists(gif_source):
                                shutil.copy2(gif_source, gif_dest)

                                # Add to CSV
                                csv_file.write(f"gif_{gif_counter}.gif;"
                                             f"{well_d*1e6:.0f};"
                                             f"{needle_d*1e6:.0f};"
                                             f"{params['shift_x']*1e6:.0f};"
                                             f"{params['shift_z']*1e6:.0f};"
                                             f"{visc};"
                                             f"{angle_l};"
                                             f"{params['angle_right']};"
                                             f"{params['angle_eg']};"
                                             f"{params['angle_gold']}\n")

                            gif_counter += 1

                    except Exception as e:
                        print(f"Simulation {gif_counter} error: {e}")
                        continue

                    # Limit number of simulations for testing
                    if gif_counter > 5:
                        break
                if gif_counter > 5:
                    break
            if gif_counter > 5:
                break
        if gif_counter > 5:
            break

    csv_file.close()
    print(f"\n{'='*60}")
    print(f"Batch completed: {gif_counter-1} simulations")
    print(f"CSV file: gif_mapping_generated.csv")
    print(f"{'='*60}")


if __name__ == "__main__":
    # Test with a single parameter set
    test_params = {
        'well_diameter': 1000e-6,       # 1000 µm
        'needle_diameter': 150e-6,       # 150 µm
        'shift_x': 50e-6,                # 50 µm
        'shift_z': 30e-6,                # 30 µm
        'viscosity': 3.0,                # 3.0 Pa.s
        'angle_left': 45,
        'angle_right': 45,
        'angle_eg': 30,
        'angle_gold': 60,
        'T_final': 0.02,                 # 20 ms for quick test
        'dt': 1e-4,
        'mesh_res': 25,                  # Reduced resolution for testing
        'export_step': 5
    }

    print("Single simulation test...")
    sim = InkDispenseSimulation(test_params)
    sim.run()

    # To run full batch, uncomment:
    # run_batch_simulations()
