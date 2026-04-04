# Code OpenFOAM : remplissage capillaire en micro-canal

Cette page présente les fichiers de configuration OpenFOAM 13 utilisés pour les simulations VOF de remplissage capillaire dans un micro-canal µTAS.

---

## 1. Structure du cas OpenFOAM

```
case_directory/
├── 0/                        # Conditions initiales
│   ├── U                     # Champ de vitesse
│   ├── p_rgh                 # Pression hydrostatique
│   └── alpha.water           # Fraction volumique (eau/air)
├── constant/
│   └── transportProperties   # Propriétés physiques
├── system/
│   ├── controlDict           # Contrôle temporel
│   ├── fvSchemes             # Schémas de discrétisation
│   └── fvSolution            # Solveurs linéaires
└── polyMesh_ref/             # Maillage GMSH (partagé entre les 7 cas)
```

---

## 2. Propriétés de transport (`transportProperties`)

```cpp
// constant/transportProperties — OpenFOAM 13

phases (water air);

water
{
    transportModel  Newtonian;    // Sueur = fluide newtonien
    nu              8.96e-7;      // m²/s (viscosité cinématique)
    rho             1005;         // kg/m³
}

air
{
    transportModel  Newtonian;
    nu              1.48e-5;      // m²/s
    rho             1.2;          // kg/m³
}

sigma           0.072;            // N/m — tension de surface eau/air (72 mN/m)
```

**Différence clé avec le projet de dispense :** pas de modèle de Carreau. Le liquide est un fluide newtonien simple.

---

## 3. Contrôle de la simulation (`controlDict`)

```cpp
// system/controlDict

application     foamRun;
solver          incompressibleVoF;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         0.030;            // 30 ms de simulation

deltaT          1e-7;             // Pas de temps initial (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.0001;           // Écriture toutes les 0.1 ms (100 µs)

// Contrôle adaptatif du pas de temps
adjustTimeStep  yes;
maxCo           0.2;              // Courant max global (conservateur)
maxAlphaCo      0.2;              // Courant max à l'interface
maxDeltaT       5e-5;             // Pas de temps max (50 µs)
```

**Points clés :**
- **maxCo = 0.2** : plus conservateur que le projet de dispense (0.3), nécessaire pour la stabilité des angles de contact.
- **writeInterval = 0.1 ms** : fréquence élevée pour visualiser l'avancée du front capillaire.
- **maxDeltaT = 50 µs** : limite stricte pour éviter les oscillations CFL avec PLIC.

---

## 4. Schémas de discrétisation (`fvSchemes`)

```cpp
// system/fvSchemes

ddtSchemes
{
    default         Euler;            // Temporel 1er ordre (stable pour VOF)
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;

    // Transport de l'interface — PLIC géométrique
    div(phi,alpha.water) Gauss PLIC interfaceCompression vanLeer 1;

    // Convection de la quantité de mouvement
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

**Différence majeure : reconstruction PLIC**

| Méthode | Projet dispense | Ce projet (micro-canal) |
|---------|-----------------|------------------------|
| Transport α | MULES (algébrique). | **PLIC** (géométrique). |
| Interface | Diffuse (~2-3 cellules). | **Nette** (~1 cellule). |
| cAlpha | 1 (compression active). | **0** (compression désactivée). |
| Maillage requis | Hexa ou poly | **Quad structuré obligatoire.** |

La reconstruction **PLIC** est préférable ici car :
1. L'interface est un front simple (pas de coalescence).
2. Le maillage est structuré (quads).
3. Les angles de contact doivent piloter la physique, pas la compression numérique.

---

## 5. Configuration des solveurs (`fvSolution`)

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      1;
        nAlphaSubCycles polynomial (0 4);  // Sous-cyclage adaptatif

        cAlpha          0;                  // Pas de compression artificielle
    }

    pcorr
    {
        solver          GAMG;
        tolerance       1e-5;
        relTol          0;
    }

    p_rgh
    {
        solver          GAMG;              // Solveur par défaut
        // OU : solver PCG + preconditioner DIC  (si θ_sub < 90°)
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
    nCorrectors     3;                     // 3 corrections pression-vitesse
    nNonOrthogonalCorrectors 0;
    momentumPredictor no;
}
```

**Point critique : choix du solveur de pression**

Lors de l'étude paramétrique, le solveur **GAMG** (Geometric Algebraic Multigrid) s'est avéré instable pour les cas avec θ_substrat < 90° (cas 002 et 003). La raison : les forts gradients de pression capillaire provoquent une singularité au niveau le plus grossier de la hiérarchie multigrid.

```
Sélection automatique dans le script d'étude :

if θ_substrat < 90° :
    → PCG + DIC   (évite l'agrégation multigrid)
else :
    → GAMG        (plus rapide pour gradients modérés)
```

---

## 6. Angles de contact (`alpha.water`)

```cpp
// 0/alpha.water (conditions aux limites)

boundaryField
{
    lid
    {
        type            constantAlphaContactAngle;
        theta0          22;               // Angle de contact lid (°)
        limit           gradient;
        value           uniform 0;
    }

    substrate
    {
        type            constantAlphaContactAngle;
        theta0          121;              // Angle de contact substrat (°)
        limit           gradient;
        value           uniform 0;
    }

    electrode_1
    {
        type            constantAlphaContactAngle;
        theta0          96;               // Angle de contact électrode (°)
        limit           gradient;
        value           uniform 0;
    }

    inlet
    {
        type            inletOutlet;
        inletValue      uniform 1;        // Entrée d'eau (α = 1)
        value           uniform 1;
    }

    outlet
    {
        type            inletOutlet;
        inletValue      uniform 0;        // Sortie air (α = 0)
        value           uniform 0;
    }
}
```

---

## 7. Script d'étude paramétrique (`run_study.py`)

```python
#!/usr/bin/env python3
"""
Étude paramétrique : remplissage capillaire en micro-canal µTAS.
7 cas, 1 paramètre varié par cas.
"""

# Matrice de l'étude
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
    Prépare un cas OpenFOAM à partir du template.

    1. Copie polyMesh_ref/ → runs/<case>/constant/polyMesh/
    2. Modifie transportProperties (sigma, nu)
    3. Modifie alpha.water (theta0 pour chaque patch)
    4. Adapte fvSolution si theta_sub < 90° (PCG au lieu de GAMG)
    """
    run_dir = base_dir / "runs" / case_name
    # ... copie template + modification paramètres ...

    # Choix du solveur de pression (stabilité)
    if params["theta_sub"] < 90:
        set_pressure_solver(run_dir, solver="PCG", preconditioner="DIC")
    else:
        set_pressure_solver(run_dir, solver="GAMG")


def run_all():
    """Lance les 7 simulations séquentiellement."""
    for name, params in STUDY_MATRIX.items():
        setup_case(name, params, BASE_DIR)

        # Commande OpenFOAM
        cmd = f"foamRun -solver incompressibleVoF"
        subprocess.run(cmd, shell=True, cwd=run_dir)
```

**Points clés :**
- **1 paramètre varié par cas** : permet d'isoler l'effet de chaque variable.
- **Sélection automatique PCG/GAMG** : évite les crashes SIGFPE sur les cas fortement capillaires.
- **Pipeline** : le maillage est généré une seule fois (GMSH puis `gmshToFoam`) et partagé via `polyMesh_ref/`.
