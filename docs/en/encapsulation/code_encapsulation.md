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
        nu0     nu0  [0 2 -1 0 0 0 0] 9.375e-3;  // η₀/ρ = 15/1600 m²/s
        nuInf   nuInf [0 2 -1 0 0 0 0] 6.25e-4;   // η∞/ρ = 1.0/1600 m²/s
        k       k    [0 0 1 0 0 0 0] 10;           // λ = 10 s
        n       n    [0 0 0 0 0 0 0] 0.4;          // shear-thinning index
    }

    rho     1600;    // kg/m³ — silica-filled epoxy resin
}

air
{
    transportModel  Newtonian;
    nu              8.33e-6;  // m²/s
    rho             1.2;      // kg/m³
}

sigma   0.035;    // N/m — resin/air surface tension (35 mN/m)
```

**Key points:**
- **BirdCarreau** (not Carreau): OpenFOAM v2406 uses this name for the full model with both plateaus.
- The ν₀/ν∞ ratio = 15 → strong shear-thinning.
- Conversion: ν = η / ρ (OpenFOAM expects kinematic viscosity).

---

## 3. Simulation Control (`controlDict`)

```cpp
// system/controlDict

application     interFoam;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         2.8;              // 2.8 s total (1.29 s dispensing + 1.51 s settling)

deltaT          1e-7;             // Initial time step (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.010;            // Write every 10 ms → 100 frames

adjustTimeStep  yes;
maxCo           0.3;
maxAlphaCo      0.3;
maxDeltaT       5e-4;             // Max 500 µs
```

**Key points:**
- **endTime = 2.8 s**: long simulation to capture dispensing (4 phases) AND settling (1.5 s).
- **writeInterval = 10 ms**: compromise between temporal resolution and data volume (~280 frames).
- The nozzle is mobile: a `codedFunctionObject` in the controlDict computes the nozzle x-position as a function of time (4 phases: stationary deposit, translation, final deposit, retraction).
- The settling phase (1.5 s) is essential: resin continues flowing by capillarity after nozzle retraction.

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

## 7. Injection Profile (`U`) and Mobile Nozzle

The inlet velocity and nozzle position are managed by a `codedFunctionObject` in the controlDict. The nozzle is mobile in x and dispensing is active during phases 1-3.

```cpp
// Temporal sequence (codedFunctionObject in controlDict):
//
// Phase 1 [0, 0.05 s]      : stationary at x = -1.1 mm, dispense ON
// Phase 2 [0.05, 0.49 s]   : translation -1.1 → +1.1 mm at v_lat = 5 mm/s
// Phase 3 [0.49, 1.29 s]   : stationary at x = +1.1 mm, dispense ON
// Phase 4 [1.29, 2.8 s]    : nozzle retracted, settling (capillarity)
//
// v_disp = 3.5 mm/s (dispensing velocity, constant phases 1-3)
// V_total = v_disp × nozzle_Ø × t_disp = 3.5 × 0.6 × 1.29 = 2.71 mm²
```

**Simulation phases:**
1. **t = 0 → 0.05 s**: stationary deposit on left side (x = -1.1 mm).
2. **t = 0.05 → 0.49 s**: nozzle translation (-1.1 → +1.1 mm).
3. **t = 0.49 → 1.29 s**: stationary deposit on right side (0.8 s).
4. **t = 1.29 → 2.8 s**: settling, resin spreads by capillarity.

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

| Parameter | Min | Ref. (039) | Max | Unit |
|-----------|-----|-----------|-----|------|
| v_disp (nozzle flow rate) | 2.0 | 3.5 | 5.0 | mm/s |
| v_lat (lateral velocity) | 3.5 | 5.0 | 7.5 | mm/s |
| η₀ (zero-shear viscosity) | 5 | 15 | 25 | Pa·s |
| σ (surface tension) | - | 0.035 | - | N/m |
| θ_chip (die angle) | - | 25 | - | ° |
| θ_dam (dam angle) | - | 70 | - | ° |
| Cell size | - | 15 | - | µm |

**Structured parametric study: 7 cases (039-045), 3 axes.**
