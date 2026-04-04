# OpenFOAM Code: Capillary Filling in Micro-channel

This page presents the OpenFOAM 13 configuration files used for VOF simulations of capillary filling in a µTAS micro-channel.

---

## 1. OpenFOAM Case Structure

```
case_directory/
├── 0/                        # Initial conditions
│   ├── U                     # Velocity field
│   ├── p_rgh                 # Hydrostatic pressure
│   └── alpha.water           # Volume fraction (water/air)
├── constant/
│   └── transportProperties   # Physical properties
├── system/
│   ├── controlDict           # Time control
│   ├── fvSchemes             # Discretization schemes
│   └── fvSolution            # Linear solvers
└── polyMesh_ref/             # GMSH mesh (shared across all 7 cases)
```

---

## 2. Transport Properties (`transportProperties`)

```cpp
// constant/transportProperties — OpenFOAM 13

phases (water air);

water
{
    transportModel  Newtonian;    // Sweat = Newtonian fluid
    nu              8.96e-7;      // m²/s (kinematic viscosity)
    rho             1005;         // kg/m³
}

air
{
    transportModel  Newtonian;
    nu              1.48e-5;      // m²/s
    rho             1.2;          // kg/m³
}

sigma           0.072;            // N/m — water/air surface tension (72 mN/m)
```

**Key difference from the dispensing project:** No Carreau model. The liquid is a simple Newtonian fluid.

---

## 3. Simulation Control (`controlDict`)

```cpp
// system/controlDict

application     foamRun;
solver          incompressibleVoF;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         0.030;            // 30 ms simulation

deltaT          1e-7;             // Initial time step (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.0001;           // Write every 0.1 ms (100 µs)

// Adaptive time stepping
adjustTimeStep  yes;
maxCo           0.2;              // Max global Courant (conservative)
maxAlphaCo      0.2;              // Max interface Courant
maxDeltaT       5e-5;             // Max time step (50 µs)
```

**Key points:**
- **maxCo = 0.2**: more conservative than the dispensing project (0.3), required for contact angle stability.
- **writeInterval = 0.1 ms**: high frequency to visualize capillary front advancement.
- **maxDeltaT = 50 µs**: strict limit to avoid CFL oscillations with PLIC.

---

## 4. Discretization Schemes (`fvSchemes`)

```cpp
// system/fvSchemes

ddtSchemes
{
    default         Euler;            // 1st order temporal (stable for VOF)
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;

    // Interface transport — geometric PLIC
    div(phi,alpha.water) Gauss PLIC interfaceCompression vanLeer 1;

    // Momentum convection
    div(rhoPhi,U)   Gauss linearUpwind grad(U);

    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}
```

**Major difference: PLIC reconstruction**

| Method | Dispensing project | This project (micro-channel) |
|--------|-------------------|------------------------------|
| α transport | MULES (algebraic). | **PLIC** (geometric). |
| Interface | Diffuse (~2-3 cells). | **Sharp** (~1 cell). |
| cAlpha | 1 (compression active). | **0** (compression disabled). |
| Required mesh | Hexa or poly. | **Structured quad mandatory.** |

**PLIC** reconstruction is preferred here because:
1. The interface is a simple front (no coalescence).
2. The mesh is structured (quads).
3. Contact angles must drive the physics, not numerical compression.

---

## 5. Solver Configuration (`fvSolution`)

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      1;
        nAlphaSubCycles polynomial (0 4);  // Adaptive sub-cycling

        cAlpha          0;                  // No artificial compression
    }

    pcorr
    {
        solver          GAMG;
        tolerance       1e-5;
        relTol          0;
    }

    p_rgh
    {
        solver          GAMG;              // Default solver
        // OR: solver PCG + preconditioner DIC  (if θ_sub < 90°)
        tolerance       1e-7;
        relTol          0.01;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-6;
        relTol          0;
    }
}

PIMPLE
{
    nCorrectors     3;                     // 3 pressure-velocity corrections
    nNonOrthogonalCorrectors 0;
    momentumPredictor no;
}
```

**Critical point: pressure solver selection**

During the parametric study, the **GAMG** (Geometric Algebraic Multigrid) solver proved unstable for cases with θ_substrate < 90° (cases 002 and 003). The reason: strong capillary pressure gradients cause a singularity at the coarsest multigrid level.

```
Automatic selection in the study script:

if θ_substrate < 90°:
    → PCG + DIC   (avoids multigrid aggregation)
else:
    → GAMG        (faster for moderate gradients)
```

---

## 6. Contact Angles (`alpha.water`)

```cpp
// 0/alpha.water (boundary conditions)

boundaryField
{
    lid
    {
        type            constantAlphaContactAngle;
        theta0          22;               // Lid contact angle (°)
        limit           gradient;
        value           uniform 0;
    }

    substrate
    {
        type            constantAlphaContactAngle;
        theta0          121;              // Substrate contact angle (°)
        limit           gradient;
        value           uniform 0;
    }

    electrode_1
    {
        type            constantAlphaContactAngle;
        theta0          96;               // Electrode contact angle (°)
        limit           gradient;
        value           uniform 0;
    }

    inlet
    {
        type            inletOutlet;
        inletValue      uniform 1;        // Water inlet (α = 1)
        value           uniform 1;
    }

    outlet
    {
        type            inletOutlet;
        inletValue      uniform 0;        // Air outlet (α = 0)
        value           uniform 0;
    }
}
```

---

## 7. Parametric Study Script (`run_study.py`)

```python
#!/usr/bin/env python3
"""
Parametric study: capillary filling in µTAS micro-channel.
7 cases, 1 parameter varied per case.
"""

# Study matrix
STUDY_MATRIX = {
    "001_baseline":  {"theta_sub": 121, "theta_top": 22, "theta_elec": 96,
                      "sigma": 0.072, "mu": 0.90e-3},
    "002_theta90":   {"theta_sub":  90, "theta_top": 22, "theta_elec": 96,
                      "sigma": 0.072, "mu": 0.90e-3},
    "003_theta60":   {"theta_sub":  60, "theta_top": 22, "theta_elec": 96,
                      "sigma": 0.072, "mu": 0.90e-3},
    "004_visco15x":  {"theta_sub": 121, "theta_top": 22, "theta_elec": 96,
                      "sigma": 0.072, "mu": 1.35e-3},
    "005_sigma05x":  {"theta_sub": 121, "theta_top": 22, "theta_elec": 96,
                      "sigma": 0.036, "mu": 0.90e-3},
    "006_step45":    {"theta_sub": 121, "theta_top": 22, "theta_elec": 45,
                      "sigma": 0.072, "mu": 0.90e-3},
    "007_top45":     {"theta_sub": 121, "theta_top": 45, "theta_elec": 96,
                      "sigma": 0.072, "mu": 0.90e-3},
}


def setup_case(case_name: str, params: dict, base_dir: Path):
    """
    Prepare an OpenFOAM case from the template.

    1. Copy polyMesh_ref/ → runs/<case>/constant/polyMesh/
    2. Modify transportProperties (sigma, nu)
    3. Modify alpha.water (theta0 for each patch)
    4. Adapt fvSolution if theta_sub < 90° (PCG instead of GAMG)
    """
    run_dir = base_dir / "runs" / case_name
    # ... copy template + modify parameters ...

    # Pressure solver selection (stability)
    if params["theta_sub"] < 90:
        set_pressure_solver(run_dir, solver="PCG", preconditioner="DIC")
    else:
        set_pressure_solver(run_dir, solver="GAMG")


def run_all():
    """Run all 7 simulations sequentially."""
    for name, params in STUDY_MATRIX.items():
        setup_case(name, params, BASE_DIR)

        # OpenFOAM command
        cmd = f"foamRun -solver incompressibleVoF"
        subprocess.run(cmd, shell=True, cwd=run_dir)
```

**Key points:**
- **1 parameter varied per case**: isolates the effect of each variable.
- **Automatic PCG/GAMG selection**: prevents SIGFPE crashes on strongly capillary cases.
- **Pipeline**: the mesh is generated once (GMSH → `gmshToFoam`) and shared via `polyMesh_ref/`.
