# OpenFOAM Code : Glob Top Encapsulation (COB)

This page presents the OpenFOAM v2406 configuration files used for VOF simulations of Chip-On-Board component encapsulation.

---

## 1. OpenFOAM Case Structure

```
case_directory/
├── 0/                        # Initial conditions
│   ├── U                     # Velocity field (inlet table + mobile nozzle)
│   ├── p_rgh                 # Hydrostatic pressure
│   └── alpha.water           # Volume fraction (resin/air)
├── constant/
│   └── transportProperties   # Bird-Carreau + air properties
├── system/
│   ├── controlDict           # Time control + nozzle codedFO
│   ├── fvSchemes             # Discretization schemes
│   ├── fvSolution            # PIMPLE + solvers
│   ├── blockMeshDict         # Structured mesh (29 blocks)
│   └── setFieldsDict         # Initial resin position in nozzle
└── templates/                # Parametric template files
    └── system/parameters     # Parameter dictionary (geometry + physics)
```

---

## 2. Transport Properties (`transportProperties`)

```cpp
// constant/transportProperties — OpenFOAM v2406

phases (water air);

water  // Epoxy resin phase (glob top)
{
    transportModel  BirdCarreau;

    BirdCarreauCoeffs
    {
        nu0     nu0  [0 2 -1 0 0 0 0] 4.167e-2;  // η₀/ρ = 50/1200 m²/s
        nuInf   nuInf [0 2 -1 0 0 0 0] 8.33e-4;   // η∞/ρ = 1.0/1200 m²/s
        k       k    [0 0 1 0 0 0 0] 10;           // λ = 10 s
        n       n    [0 0 0 0 0 0 0] 0.4;          // shear-thinning index
    }

    rho     1200;    // kg/m³ — silica-filled epoxy resin
}

air
{
    transportModel  Newtonian;
    nu              8.33e-6;  // m²/s
    rho             1.2;      // kg/m³
}

sigma   0.038;    // N/m — resin/air surface tension (38 mN/m)
```

**Key points:**
- **BirdCarreau** (not Carreau): OpenFOAM v2406 uses this name for the full model with both plateaus.
- The ν₀/ν∞ ratio = 50 → strong shear-thinning.
- Conversion: ν = η / ρ (OpenFOAM expects kinematic viscosity).

---

## 3. Simulation Control (`controlDict`)

```cpp
// system/controlDict

application     interFoam;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         1.0;              // 1 s total (0.5 s dispensing + 0.5 s settling)

deltaT          1e-7;             // Initial time step (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.010;            // Write every 10 ms → 100 frames

adjustTimeStep  yes;
maxCo           0.3;
maxAlphaCo      0.3;
maxDeltaT       5e-4;             // Max 500 µs
```

**Key points:**
- **endTime = 1.0 s**: long simulation to capture both dispensing AND settling.
- **writeInterval = 10 ms**: compromise between temporal resolution and data volume.
- The settling phase (0.5 s) is essential : resin continues flowing by capillarity after dispensing stops.

---

## 4. Discretization Schemes (`fvSchemes`)

```cpp
// system/fvSchemes

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default                             none;

    div(rhoPhi,U)                       Gauss linearUpwind grad(U);
    div(phi,alpha)                      Gauss vanLeer;
    div(phirb,alpha)                    Gauss linear;
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

**Difference from micro-channel project:**
- **No PLIC**: `Gauss vanLeer` (algebraic) instead of `Gauss PLIC` (geometric).
- Reason: the blockMesh with 29 non-conformal blocks makes PLIC unstable at junctions.
- Artificial compression is managed by `cAlpha = 0` in fvSolution (not by the scheme).

---

## 5. Solver Configuration (`fvSolution`)

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      3;
        nAlphaSubCycles 2;

        cAlpha          0;       // CRITICAL: no artificial compression

        MULESCorr       no;
        nLimiterIter    3;

        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-9;
        relTol          0;
    }

    pcorr
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-5;
        relTol          0;
    }

    p_rgh
    {
        solver          PCG;
        preconditioner  DIC;
        tolerance       1e-8;
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
    momentumPredictor   no;
    nOuterCorrectors    2;       // 2 outer corrections (high viscosity)
    nCorrectors         3;
    nNonOrthogonalCorrectors 0;

    pRefCell            0;
    pRefValue           0;
}
```

**Critical point: nOuterCorrectors = 2**

Standard pressure-velocity coupling (nOuterCorrectors = 1) is insufficient when the viscosity ratio is extreme (5×10⁶). With 2 outer corrections, the solver converges stably. This is a key learning from this project.

---

## 6. Contact Angles (`alpha.water`)

```cpp
// 0/alpha.water — boundary conditions (excerpt)

boundaryField
{
    pcb_left
    {
        type            dynamicAlphaContactAngle;
        theta0          35;           // PCB contact angle (°)
        thetaA          40;           // Advancing angle
        thetaR          30;           // Receding angle
        uTheta          0.001;        // Threshold velocity (m/s)
        limit           gradient;
        value           uniform 0;
    }

    pad_au_left
    {
        type            dynamicAlphaContactAngle;
        theta0          25;           // Gold — very hydrophilic
        thetaA          30;
        thetaR          20;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    die_top
    {
        type            dynamicAlphaContactAngle;
        theta0          25;           // SiN — very hydrophilic
        thetaA          30;
        thetaR          20;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    dam_left
    {
        type            dynamicAlphaContactAngle;
        theta0          70;           // Barrier — partial wetting
        thetaA          75;
        thetaR          65;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    buse_left_ext
    {
        type            constantAlphaContactAngle;
        theta0          150;          // PTFE — anti-wetting
        limit           gradient;
        value           uniform 0;
    }

    inlet
    {
        type            fixedValue;
        value           uniform 0;    // Air enters through inlet
    }
}
```

**Key points:**
- **dynamicAlphaContactAngle**: model with hysteresis (θ_advancing ≠ θ_receding).
- **uTheta**: threshold velocity for advancing/receding transition (0.001 m/s = 1 mm/s).
- The PTFE nozzle exterior (θ = 150°) is essential to prevent resin from creeping up the nozzle.

---

## 7. Injection Profile (`U`)

```cpp
// 0/U — inlet boundary condition

inlet
{
    type            uniformFixedValue;
    uniformValue    table
    (
        (0.000    (0 -0.002 0))     // Start dispensing: 2 mm/s downward
        (0.500    (0 -0.002 0))     // End dispensing at t = 0.5 s
        (0.501    (0  0     0))     // Abrupt stop
        (1.000    (0  0     0))     // Settling (rest)
    );
}
```

**Simulation phases:**
1. **t = 0 → 0.5 s**: active dispensing (v = 2 mm/s, flow rate Q ≈ 0.56 µL/s)
2. **t = 0.5 → 1.0 s**: settling : resin spreads by capillarity + gravity.

---

## 8. Mesh Generation (`generate_blockMeshDict.py`)

```python
#!/usr/bin/env python3
"""
Generate parametric blockMeshDict for COB encapsulation.
29 structured blocks, 18 named patches.
"""

# Geometric parameters (mm → m via scale 0.001)
PARAMS = {
    "die_width":    1.0,    # mm — die width
    "die_height":   0.3,    # mm — die height
    "pad_width":    0.4,    # mm — Au pad width (×2)
    "dam_width":    0.5,    # mm — dam width (×2)
    "dam_height":   0.8,    # mm — dam height
    "nozzle_width": 0.6,    # mm — nozzle diameter
    "nozzle_height": 1.5,   # mm — nozzle height
    "cell_size":    0.015,  # mm — cell size (15 µm)
}


def generate_vertices(p: dict) -> list:
    """
    Generate 60+ vertices for the 2D domain.
    Topology: PCB (bottom) + die (obstacle) + dam (sides) + nozzle (top).
    """
    # ... 29 blocks with controlled aspect ratios ...


def generate_blocks(p: dict) -> list:
    """
    Generate hex blocks with uniform resolution.
    Each block: (n_cells_x, n_cells_y, 1) for 2D.
    """
    nx = int(p["die_width"] / p["cell_size"])
    ny = int(p["die_height"] / p["cell_size"])
    # ... 29 block definitions ...


def generate_patches() -> dict:
    """
    18 named patches:
    - 2 pcb (L/R), 2 pad_au (L/R), 3 die (top/L/R)
    - 2 dam (L/R), 2 dam_top (L/R)
    - 2 buse_int (L/R), 2 buse_ext (L/R)
    - 1 inlet, 1 atmosphere, 2 outlet (L/R)
    - front/back (empty for 2D)
    """
```

**Key points:**
- The mesh is **parametric**: changing `cell_size` or `dam_height` regenerates the entire blockMeshDict.
- **29 blocks**: topology handles the die obstacle (not meshed) + lateral dams + nozzle.
- **18 patches**: each physical surface has its own patch for different contact angles.

---

## 9. Summary of Studied Parameters

| Parameter | Min | Ref. | Max | Unit |
|-----------|-----|------|-----|------|
| Cell size | 10 | 15 | 20 | µm |
| η₀ (zero-shear viscosity) | 5 | 15 | 50 | Pa·s |
| σ (surface tension) | 0.030 | 0.038 | 0.040 | N/m |
| θ_chip (die angle) | 15 | 25 | 60 | ° |
| θ_dam (dam angle) | 40 | 70 | 120 | ° |
| y_dam (dam height) | 0.5 | 0.8 | 1.04 | mm |
| v_lateral (nozzle) | 1.7 | 2.5 | 5.0 | mm/s |
| t₁_end (end dispensing) | 0.2 | 0.5 | 0.8 | s |

**Total: 38 simulated cases** (unstructured exploration, no formal DoE).
