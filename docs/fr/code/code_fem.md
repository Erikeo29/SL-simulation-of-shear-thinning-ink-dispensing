
## 4. MÉTHODE NUMÉRIQUE

### 4.1 Discrétisation spatiale

Le domaine Ω est discrétisé par éléments finis avec :
- Éléments P₂ pour la vitesse (polynômes quadratiques)
- Éléments P₁ pour la pression (polynômes linéaires)
- Éléments P₁ pour la fonction level-set

Cette combinaison (P₂-P₁) satisfait la condition inf-sup pour la stabilité.

### 4.2 Discrétisation temporelle

Schéma de Crank-Nicolson (θ = 0.5) :
$$\frac{\mathbf{v}^{n+1} - \mathbf{v}^n}{\Delta t} = \theta \mathcal{F}(\mathbf{v}^{n+1}) + (1-\theta)\mathcal{F}(\mathbf{v}^n)$$

avec Δt = 10⁻⁴ s choisi pour satisfaire CFL < 0.5 :
$$\text{CFL} = \frac{|\mathbf{v}|_{\max} \Delta t}{h} < 0.5$$

où h est la taille caractéristique de maille.

### 4.3 Algorithme de résolution

```
ALGORITHME : Simulation diphasique Phase-Field
------------------------------------------------
1. INITIALISATION
   - Créer maillage avec raffinement près de l'interface
   - Initialiser v = 0, p = 0, φ = φ₀
   
2. BOUCLE TEMPORELLE : pour t = 0 à T
   
   2.1 TRANSPORT INTERFACE
       - Résoudre équation Phase-Field pour φⁿ⁺¹
       - Réinitialiser distance signée si nécessaire
   
   2.2 MISE À JOUR PROPRIÉTÉS
       - Calculer ρ(φⁿ⁺¹), η(φⁿ⁺¹, γ̇ⁿ)
       - Calculer F_σ depuis φⁿ⁺¹
   
   2.3 RÉSOLUTION NAVIER-STOKES (algorithme SIMPLE)
       a. Prédiction vitesse v*
          Résoudre : ρ(v* - vⁿ)/Δt + ρ(vⁿ·∇)v* = -∇pⁿ + ∇·τⁿ + F
       
       b. Correction pression
          Résoudre : ∇²p' = (ρ/Δt)∇·v*
       
       c. Correction vitesse
          vⁿ⁺¹ = v* - (Δt/ρ)∇p'
          pⁿ⁺¹ = pⁿ + p'
   
   2.4 VÉRIFICATION CONVERGENCE
       - ||vⁿ⁺¹ - vⁿ||/||vⁿ|| < 10⁻⁶
       - ||∇·vⁿ⁺¹|| < 10⁻⁸
   
   2.5 CALCUL MÉTRIQUES
       - Taux de remplissage : α = ∫_Ω H(φ)dΩ / V_puit
       - Si α ≥ 0.8 : STOP
   
3. POST-TRAITEMENT
   - Export résultats (VTK/XDMF)
   - Analyse statistique
```

---

## 5. IMPLÉMENTATION PYTHON

### 5.1 Structure modulaire du code

#!/usr/bin/env python3
"""
Simulation de dispense
Méthode Phase-Field avec FEniCSx

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

# Configuration PETSc
PETSc.Sys.popErrorHandler()

class InkDispenseSimulation:
    """
    Classe principale pour la simulation de dispense.
    """

    def __init__(self, params=None):
        """
        Initialisation avec paramètres physiques.

        Args:
            params (dict): Dictionnaire des paramètres de simulation
        """

        # Récupération des paramètres ou valeurs par défaut
        if params is None:
            params = {}

        # ========== Propriétés Phase 1 : Encre ==========
        self.rho_ink = params.get('rho_ink', 3000.0)      # kg/m³
        self.mu_0 = params.get('viscosity', 1.5)          # Pa·s (viscosité au repos)
        self.mu_inf = params.get('mu_inf', 0.05)          # Pa·s (viscosité infinie)
        self.lambda_c = params.get('lambda_c', 0.15)      # s (temps de relaxation)
        self.n_carreau = params.get('n_carreau', 0.7)     # - (indice pseudoplasticité)

        # ========== Propriétés Phase 2 : Air ==========
        self.rho_air = params.get('rho_air', 1.2)         # kg/m³
        self.mu_air = params.get('mu_air', 1e-5)          # Pa·s

        # ========== Propriétés interfaciales ==========
        self.sigma = params.get('sigma', 0.04)            # N/m (tension surface)
        self.epsilon = params.get('epsilon', 5e-6)        # m (épaisseur interface)
        self.gamma_mob = params.get('gamma_mob', 1.0)     # mobilité interface

        # ========== Géométrie [m] ==========
        self.D_well = params.get('well_diameter', 0.8e-3)     # diamètre puit
        self.h_well = params.get('well_height', 0.128e-3)     # hauteur puit
        self.D_needle = params.get('needle_diameter', 0.2e-3) # diamètre seringue
        self.shift_x = params.get('shift_x', 0.0)             # décalage X seringue
        self.shift_z = params.get('shift_z', 30e-6)           # gap seringue-puit

        # ========== Angles de contact [rad] ==========
        self.theta_gold = np.radians(params.get('angle_gold', 60))
        self.theta_left = np.radians(params.get('angle_left', 45))
        self.theta_right = np.radians(params.get('angle_right', 45))
        self.theta_eg = np.radians(params.get('angle_eg', 30))

        # ========== Conditions opératoires ==========
        self.flow_rate = params.get('flow_rate', 1e-9)    # m³/s (débit volumique)
        self.v_inlet = self.flow_rate / (np.pi * (self.D_needle/2)**2)  # vitesse entrée

        # ========== Paramètres numériques ==========
        self.dt = params.get('dt', 1e-4)                   # pas de temps [s]
        self.T_final = params.get('T_final', 0.1)          # temps final [s]
        self.tol = params.get('tol', 1e-6)                 # tolérance convergence
        self.mesh_resolution = params.get('mesh_res', 40)  # résolution maillage

        # ========== Paramètres export ==========
        self.output_dir = params.get('output_dir', 'simulation_results')
        self.export_step = params.get('export_step', 10)   # export tous les N pas

        # Créer dossier de sortie
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{self.output_dir}/frames").mkdir(exist_ok=True)

    def create_mesh(self):
        """
        Création du maillage 2D axisymétrique.

        Returns:
            domain: Objet maillage Dolfinx
        """
        # Calcul du nombre d'éléments
        nx = self.mesh_resolution
        ny = int(nx * self.h_well / (self.D_well/2))

        # Création du maillage rectangulaire (r, z)
        domain = create_rectangle(
            MPI.COMM_WORLD,
            [np.array([0, 0]),
             np.array([self.D_well/2, self.h_well])],
            [nx, ny],
            cell_type=CellType.triangle
        )

        # Créer les marqueurs de frontières
        domain.topology.create_connectivity(domain.topology.dim - 1, domain.topology.dim)

        # Définir les tags pour les frontières
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

        # Stocker les fonctions de frontière pour usage ultérieur
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
        Définition des espaces fonctionnels avec API FEniCSx 0.8+.

        Args:
            domain: Maillage

        Returns:
            V, Q, S, W: Espaces pour vitesse, pression, level-set et mixte
        """
        # Créer les éléments avec basix.ufl
        P2 = basix.ufl.element("Lagrange", domain.topology.cell_name(), 2, shape=(2,))
        P1 = basix.ufl.element("Lagrange", domain.topology.cell_name(), 1)

        # Créer les espaces fonctionnels
        V = fem.functionspace(domain, P2)  # Vitesse
        Q = fem.functionspace(domain, P1)  # Pression
        S = fem.functionspace(domain, P1)  # Level-set

        # Espace mixte pour le système couplé
        TH = basix.ufl.mixed_element([P2, P1, P1])
        W = fem.functionspace(domain, TH)

        return V, Q, S, W

    def initialize_fields(self, V, Q, S):
        """
        Initialisation des champs.

        Args:
            V, Q, S: Espaces fonctionnels

        Returns:
            u, p, phi: Fonctions initialisées
        """
        u = Function(V, name="velocity")
        p = Function(Q, name="pressure")
        phi = Function(S, name="levelset")

        # ========== Initialisation level-set ==========
        def initial_phi_expr(x):
            # Interface initiale horizontale
            z_interface = self.h_well - 0.01e-3
            return np.tanh((x[1] - z_interface) / (2 * self.epsilon))

        phi.interpolate(initial_phi_expr)

        # ========== Initialisation vitesse ==========
        def initial_velocity_expr(x):
            vr = np.zeros(x.shape[1])
            vz = np.zeros(x.shape[1])

            # Zone d'injection
            mask_inlet = np.logical_and(
                x[1] > self.h_well - 0.001e-3,
                x[0] < self.D_needle/2
            )

            if np.any(mask_inlet):
                r = x[0][mask_inlet]
                R = self.D_needle/2
                # Profil parabolique
                vz[mask_inlet] = -2 * self.v_inlet * (1 - (r/R)**2)

            return np.vstack([vr, vz])

        u.interpolate(initial_velocity_expr)

        # ========== Pression hydrostatique ==========
        def initial_pressure_expr(x):
            g = 9.81
            return self.rho_air * g * (self.h_well - x[1])

        p.interpolate(initial_pressure_expr)

        return u, p, phi

    def setup_variational_problem(self, W, u_n, p_n, phi_n):
        """
        Configuration du problème variationnel pour le système couplé.

        Args:
            W: Espace mixte
            u_n, p_n, phi_n: Solutions au pas de temps précédent

        Returns:
            a, L: Formes bilinéaire et linéaire
        """
        # Fonctions test et inconnues
        (v, q, xi) = ufl.TestFunctions(W)
        w = Function(W)
        (u, p, phi) = ufl.split(w)

        # ========== Tenseur des déformations ==========
        def epsilon(u):
            return 0.5 * (grad(u) + grad(u).T)

        # ========== Taux de cisaillement ==========
        def gamma_dot(u):
            return sqrt(2 * inner(epsilon(u), epsilon(u)) + 1e-10)

        # ========== Viscosité Carreau ==========
        def mu_carreau(u):
            gd = gamma_dot(u)
            return self.mu_inf + (self.mu_0 - self.mu_inf) * \
                   (1 + (self.lambda_c * gd)**2)**((self.n_carreau - 1)/2)

        # ========== Heaviside régularisée ==========
        def H(phi):
            return 0.5 * (1.0 + phi/sqrt(phi**2 + self.epsilon**2))

        # ========== Propriétés moyennées ==========
        H_phi = H(phi)
        rho = self.rho_ink * H_phi + self.rho_air * (1 - H_phi)
        mu = mu_carreau(u) * H_phi + self.mu_air * (1 - H_phi)

        # ========== Force de tension de surface ==========
        n = grad(phi) / sqrt(inner(grad(phi), grad(phi)) + 1e-10)
        kappa = div(n)
        f_st = self.sigma * kappa * grad(phi)

        # ========== Gravité ==========
        g = as_vector([0, -9.81])

        # ========== Equation de Navier-Stokes ==========
        # Terme d'inertie
        F_ns = rho * inner((u - u_n) / self.dt, v) * dx
        F_ns += rho * inner(grad(u) * u, v) * dx

        # Terme visqueux
        F_ns += 2 * mu * inner(epsilon(u), epsilon(v)) * dx

        # Terme de pression
        F_ns -= p * div(v) * dx

        # Forces volumiques
        F_ns -= inner(rho * g, v) * dx
        F_ns -= inner(f_st, v) * dx

        # Conservation de la masse
        F_ns += q * div(u) * dx

        # ========== Equation de transport level-set ==========
        # Advection
        F_phi = (phi - phi_n) / self.dt * xi * dx
        F_phi += inner(u, grad(phi)) * xi * dx

        # Terme de réinitialisation (maintien |∇φ| = 1)
        lambda_reinit = self.epsilon * abs(max(abs(self.v_inlet), 1e-3))
        F_phi += lambda_reinit * (inner(grad(phi), grad(xi)) * dx -
                                   (1 - inner(grad(phi), grad(phi))) * xi * dx)

        # ========== Forme totale ==========
        F = F_ns + F_phi

        # Séparation en formes bilinéaire et linéaire
        dw = ufl.TrialFunction(W)
        J = ufl.derivative(F, w, dw)

        return J, F

    def apply_boundary_conditions(self, W, domain):
        """
        Application des conditions aux limites.

        Args:
            W: Espace mixte
            domain: Maillage

        Returns:
            bcs: Liste des conditions de Dirichlet
        """
        V, Q, S = W.sub(0), W.sub(1), W.sub(2)

        bcs = []

        # ========== Condition d'entrée (inlet) ==========
        def inlet_velocity_expr(x):
            vr = np.zeros(x.shape[1])
            vz = np.zeros(x.shape[1])

            # Profil parabolique dans la seringue
            r = x[0]
            R = self.D_needle/2
            mask = r <= R

            if np.any(mask):
                vz[mask] = -2 * self.v_inlet * (1 - (r[mask]/R)**2)

            return np.vstack([vr, vz])

        # Localiser les dofs d'entrée
        fdim = domain.topology.dim - 1
        inlet_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['inlet'])
        inlet_dofs = locate_dofs_topological((V.sub(0).collapse()[0], V.sub(0)), fdim, inlet_facets)

        u_inlet = Function(V)
        u_inlet.interpolate(inlet_velocity_expr)
        bc_inlet = dirichletbc(u_inlet, inlet_dofs, V)
        bcs.append(bc_inlet)

        # ========== Condition de non-glissement sur les parois ==========
        # Paroi gauche (axe de symétrie)
        axis_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['axis'])
        axis_dofs_r = locate_dofs_topological((V.sub(0).collapse()[0], V.sub(0)), fdim, axis_facets)
        bc_axis = dirichletbc(default_scalar_type(0), axis_dofs_r, V.sub(0))
        bcs.append(bc_axis)

        # Paroi droite
        wall_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['wall'])
        wall_dofs = locate_dofs_topological(V, fdim, wall_facets)
        u_wall = Function(V)
        u_wall.x.array[:] = 0
        bc_wall = dirichletbc(u_wall, wall_dofs)
        bcs.append(bc_wall)

        # Fond
        bottom_facets = locate_entities_boundary(domain, fdim, self.boundary_conditions['bottom'])
        bottom_dofs = locate_dofs_topological(V, fdim, bottom_facets)
        u_bottom = Function(V)
        u_bottom.x.array[:] = 0
        bc_bottom = dirichletbc(u_bottom, bottom_dofs)
        bcs.append(bc_bottom)

        # ========== Angle de contact (Robin BC pour φ) ==========
        # Implémenté via terme de bord dans la forme variationnelle

        return bcs

    def solve_time_step(self, W, J, F, bcs, w):
        """
        Résolution d'un pas de temps.

        Args:
            W: Espace mixte
            J: Forme bilinéaire (Jacobien)
            F: Forme linéaire (Résidu)
            bcs: Conditions aux limites
            w: Solution courante

        Returns:
            Convergence (bool)
        """
        # Configuration du solveur Newton
        problem = fem.petsc.NonlinearProblem(F, w, bcs=bcs, J=J)
        solver = fem.petsc.NewtonSolver(MPI.COMM_WORLD, problem)

        # Paramètres du solveur
        solver.convergence_criterion = "incremental"
        solver.rtol = self.tol
        solver.atol = 1e-10
        solver.max_it = 20
        solver.report = True

        # Configuration du solveur linéaire
        ksp = solver.krylov_solver
        opts = PETSc.Options()
        option_prefix = ksp.getOptionsPrefix()
        opts[f"{option_prefix}ksp_type"] = "gmres"
        opts[f"{option_prefix}ksp_rtol"] = 1e-8
        opts[f"{option_prefix}pc_type"] = "ilu"
        opts[f"{option_prefix}pc_factor_levels"] = 2
        ksp.setFromOptions()

        # Résolution
        n_iter, converged = solver.solve(w)

        return converged

    def export_solution(self, u, p, phi, t, step):
        """
        Export de la solution pour visualisation.

        Args:
            u, p, phi: Champs de solution
            t: Temps actuel
            step: Numéro de pas de temps
        """
        # Export XDMF pour ParaView
        with XDMFFile(MPI.COMM_WORLD, f"{self.output_dir}/solution_{step:04d}.xdmf", "w") as xdmf:
            xdmf.write_mesh(u.function_space.mesh)
            xdmf.write_function(u, t)
            xdmf.write_function(p, t)
            xdmf.write_function(phi, t)

        # Export image pour GIF
        if step % self.export_step == 0:
            self.save_frame(phi, step)

    def save_frame(self, phi, step):
        """
        Sauvegarde d'une frame pour création de GIF.

        Args:
            phi: Fonction level-set
            step: Numéro de pas
        """
        # Extraction des valeurs sur une grille régulière
        nx, ny = 200, 100
        x = np.linspace(0, self.D_well/2, nx)
        y = np.linspace(0, self.h_well, ny)
        X, Y = np.meshgrid(x, y)

        # Évaluation de phi sur la grille
        points = np.vstack([X.ravel(), Y.ravel()])

        # Pour l'instant, sauvegarde simple des contours
        fig, ax = plt.subplots(figsize=(8, 4))

        # Visualisation simplifiée
        # Note: En pratique, il faudrait interpoler phi sur la grille
        # Ici on fait une visualisation schématique

        # Dessin du domaine
        ax.add_patch(plt.Rectangle((0, 0), self.D_well/2*1000, self.h_well*1000,
                                   fill=False, edgecolor='black', linewidth=2))

        # Zone d'encre (phi > 0)
        # Approximation simple pour la démo
        z_interface = self.h_well*1000 - 10 - step * 0.1
        if z_interface > 0:
            ax.add_patch(plt.Rectangle((0, 0), self.D_well/2*1000, z_interface,
                                       fill=True, facecolor='silver', alpha=0.8))

        # Seringue
        needle_x = self.shift_x*1000
        needle_top = self.h_well*1000 + self.shift_z*1000
        ax.add_patch(plt.Rectangle((needle_x, self.h_well*1000),
                                   self.D_needle/2*1000, 5,
                                   fill=True, facecolor='gray'))

        ax.set_xlim(0, self.D_well/2*1000)
        ax.set_ylim(0, self.h_well*1000*1.1)
        ax.set_xlabel('r [mm]')
        ax.set_ylabel('z [mm]')
        ax.set_title(f'Dispense - t = {step*self.dt*1000:.1f} ms')
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/frames/frame_{step:04d}.png", dpi=100)
        plt.close()

    def create_gif(self):
        """
        Création du GIF à partir des frames.
        """
        # Récupération des frames
        frames = []
        frame_files = sorted(glob.glob(f"{self.output_dir}/frames/frame_*.png"))

        for frame_file in frame_files:
            frame = Image.open(frame_file)
            frames.append(frame)

        if frames:
            # Sauvegarde du GIF
            frames[0].save(
                f"{self.output_dir}/simulation.gif",
                save_all=True,
                append_images=frames[1:],
                duration=100,
                loop=0
            )
            print(f"GIF créé: {self.output_dir}/simulation.gif")

    def run(self):
        """
        Boucle principale de simulation.
        """
        print("="*60)
        print("Simulation de Dispense")
        print("="*60)

        # Création du maillage
        print("Création du maillage...")
        domain = self.create_mesh()

        # Espaces fonctionnels
        print("Configuration des espaces fonctionnels...")
        V, Q, S, W = self.setup_function_spaces(domain)

        # Initialisation
        print("Initialisation des champs...")
        u_n, p_n, phi_n = self.initialize_fields(V, Q, S)

        # Solution mixte
        w = Function(W)
        w.sub(0).interpolate(u_n)
        w.sub(1).interpolate(p_n)
        w.sub(2).interpolate(phi_n)

        # Problème variationnel
        print("Configuration du problème variationnel...")
        J, F = self.setup_variational_problem(W, u_n, p_n, phi_n)

        # Conditions aux limites
        print("Application des conditions aux limites...")
        bcs = self.apply_boundary_conditions(W, domain)

        # Boucle temporelle
        t = 0
        step = 0
        n_steps = int(self.T_final / self.dt)

        print(f"\nDémarrage de la simulation:")
        print(f"  - Pas de temps: {self.dt*1000:.2f} ms")
        print(f"  - Temps final: {self.T_final*1000:.1f} ms")
        print(f"  - Nombre de pas: {n_steps}")
        print("="*60)

        while t < self.T_final:
            t += self.dt
            step += 1

            print(f"\nPas {step}/{n_steps} - t = {t*1000:.2f} ms")

            # Résolution
            converged = self.solve_time_step(W, J, F, bcs, w)

            if not converged:
                print("ATTENTION: Non-convergence détectée!")
                break

            # Extraction des solutions
            u, p, phi = w.sub(0).collapse(), w.sub(1).collapse(), w.sub(2).collapse()

            # Export
            self.export_solution(u, p, phi, t, step)

            # Mise à jour pour le prochain pas
            u_n.x.array[:] = u.x.array
            p_n.x.array[:] = p.x.array
            phi_n.x.array[:] = phi.x.array

            # Calcul et affichage de métriques
            if step % 10 == 0:
                # Volume d'encre dispensée
                volume_ink = assemble_scalar(form((phi_n + 1) / 2 * dx))
                volume_ink = MPI.COMM_WORLD.allreduce(volume_ink, op=MPI.SUM)
                print(f"  Volume encre: {volume_ink*1e9:.3f} nL")

        # Création du GIF final
        print("\nCréation du GIF...")
        self.create_gif()

        print("\n" + "="*60)
        print("Simulation terminée avec succès!")
        print("="*60)

        return True


def run_batch_simulations():
    """
    Exécution en batch pour toutes les combinaisons de paramètres.
    """
    # Définition des plages de paramètres
    well_diameters = [800e-6, 1000e-6, 1200e-6]  # µm -> m
    needle_diameters = [100e-6, 150e-6, 200e-6]
    shift_x_values = [0, 50e-6, 100e-6]
    shift_z_values = [0, 30e-6, 60e-6]
    viscosities = [10, 20, 30]  # Pa.s
    angles_left = [30, 45, 60]
    angles_right = [30, 45, 60]
    angles_eg = [30, 45, 60]
    angles_gold = [45, 60, 90]

    # Compteur pour nommer les GIFs
    gif_counter = 1

    # Fichier CSV de mapping
    csv_file = open("gif_mapping_generated.csv", "w")
    csv_file.write("nom fichier gif;diamètre du puit (µm);diamètre de la buse (µm);"
                   "shift buse en x (µm);shift buse en z (µm);Viscosité de l'encre (Pa.s);"
                   "angle de contact paroi gauche (°);angle de contact paroi droite (°);"
                   "angle de contact EG gauche (°);angle de contact or (°)\n")

    # Boucle sur une sélection de combinaisons (pas toutes pour économiser le temps)
    for well_d in well_diameters[::2]:  # Une valeur sur deux
        for needle_d in needle_diameters[::2]:
            for visc in viscosities[::2]:
                for angle_l in angles_left[::2]:
                    # Paramètres pour cette simulation
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
                        'T_final': 0.05,  # Simulation courte pour test
                        'mesh_res': 30,   # Résolution réduite pour test
                        'output_dir': f'simulations/gif_{gif_counter}'
                    }

                    print(f"\n{'='*60}")
                    print(f"Simulation {gif_counter}")
                    print(f"Paramètres: well={well_d*1e6:.0f}µm, needle={needle_d*1e6:.0f}µm, "
                          f"visc={visc}Pa.s")
                    print(f"{'='*60}")

                    try:
                        # Lancer la simulation
                        sim = InkDispenseSimulation(params)
                        success = sim.run()

                        if success:
                            # Copier le GIF généré
                            import shutil
                            gif_source = f"{params['output_dir']}/simulation.gif"
                            gif_dest = f"gif/gif_{gif_counter}.gif"

                            # Créer le dossier gif si nécessaire
                            Path("gif").mkdir(exist_ok=True)

                            if os.path.exists(gif_source):
                                shutil.copy2(gif_source, gif_dest)

                                # Ajouter au CSV
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
                        print(f"Erreur simulation {gif_counter}: {e}")
                        continue

                    # Limiter le nombre de simulations pour test
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
    print(f"Batch terminé: {gif_counter-1} simulations")
    print(f"Fichier CSV: gif_mapping_generated.csv")
    print(f"{'='*60}")


if __name__ == "__main__":
    # Test avec un seul jeu de paramètres
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
        'T_final': 0.02,                 # 20 ms pour test rapide
        'dt': 1e-4,
        'mesh_res': 25,                  # Résolution réduite pour test
        'export_step': 5
    }

    print("Test de simulation unique...")
    sim = InkDispenseSimulation(test_params)
    sim.run()

    # Pour lancer le batch complet, décommenter:
    # run_batch_simulations()
