# Code OpenFOAM : encapsulation glob top (COB)

Cette page présente les fichiers de configuration OpenFOAM v2406 utilisés pour les simulations VOF d'encapsulation de composants Chip-On-Board.

---

## 1. Structure du cas OpenFOAM

```
case_directory/
├── 0/                        # Conditions initiales
│   ├── U                     # Champ de vitesse (inlet table + nozzle mobile)
│   ├── p_rgh                 # Pression hydrostatique
│   └── alpha.water           # Fraction volumique (résine/air)
├── constant/
│   └── transportProperties   # Bird-Carreau + propriétés air
├── system/
│   ├── controlDict           # Contrôle temporel + nozzle codedFO
│   ├── fvSchemes             # Schémas de discrétisation
│   ├── fvSolution            # PIMPLE + solveurs
│   ├── blockMeshDict         # Maillage structuré 29 blocs
│   └── setFieldsDict         # Initialisation résine dans la buse
└── templates/                # Fichiers de base paramétriques
    └── system/parameters     # Dictionnaire paramètres (géométrie + physique)
```

---

## 2. Propriétés de transport (`transportProperties`)

```cpp
// constant/transportProperties — OpenFOAM v2406

phases (water air);

water  // Phase résine époxy (glob top)
{
    transportModel  BirdCarreau;

    BirdCarreauCoeffs
    {
        nu0     nu0  [0 2 -1 0 0 0 0] 4.167e-2;  // η₀/ρ = 50/1200 m²/s
        nuInf   nuInf [0 2 -1 0 0 0 0] 8.33e-4;   // η∞/ρ = 1.0/1200 m²/s
        k       k    [0 0 1 0 0 0 0] 10;           // λ = 10 s
        n       n    [0 0 0 0 0 0 0] 0.4;          // indice rhéofluidifiant
    }

    rho     1200;    // kg/m³ — résine époxy chargée silice
}

air
{
    transportModel  Newtonian;
    nu              8.33e-6;  // m²/s
    rho             1.2;      // kg/m³
}

sigma   0.038;    // N/m — tension de surface résine/air (38 mN/m)
```

**Points clés :**
- **BirdCarreau** (et non Carreau) : OpenFOAM v2406 utilise ce nom pour le modèle complet avec les deux plateaux.
- Le rapport ν₀/ν∞ = 50 → forte rhéofluidification.
- Conversion : ν = η / ρ (OpenFOAM attend la viscosité cinématique).

---

## 3. Contrôle de la simulation (`controlDict`)

```cpp
// system/controlDict

application     interFoam;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         1.0;              // 1 s total (0.5 s dispensing + 0.5 s settling)

deltaT          1e-7;             // Pas de temps initial (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.010;            // Écriture toutes les 10 ms → 100 frames

adjustTimeStep  yes;
maxCo           0.3;
maxAlphaCo      0.3;
maxDeltaT       5e-4;             // Max 500 µs
```

**Points clés :**
- **endTime = 1.0 s** : simulation longue pour capturer le dispensing ET le repos (settling).
- **writeInterval = 10 ms** : compromis entre résolution temporelle et volume de données.
- La phase de settling (0.5 s) est essentielle : la résine continue de s'écouler par capillarité après l'arrêt du dispensing.

---

## 4. Schémas de discrétisation (`fvSchemes`)

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

**Différence avec le projet micro-canal :**
- **Pas de PLIC** : `Gauss vanLeer` (algébrique) au lieu de `Gauss PLIC` (géométrique).
- Raison : le maillage blockMesh avec 29 blocs non-conformes rend PLIC instable aux jonctions.
- La compression artificielle est gérée par `cAlpha = 0` dans fvSolution (pas par le schéma).

---

## 5. Configuration des solveurs (`fvSolution`)

```cpp
// system/fvSolution

solvers
{
    "alpha.water.*"
    {
        nAlphaCorr      3;
        nAlphaSubCycles 2;

        cAlpha          0;       // CRITIQUE : pas de compression artificielle

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
    nOuterCorrectors    2;       // 2 corrections externes (haute viscosité)
    nCorrectors         3;
    nNonOrthogonalCorrectors 0;

    pRefCell            0;
    pRefValue           0;
}
```

**Point critique : nOuterCorrectors = 2**

Le couplage pression-vitesse standard (nOuterCorrectors = 1) est insuffisant quand le rapport de viscosité est extrême (5×10⁶). Avec 2 corrections externes, le solveur converge de manière stable. C'est un apprentissage clé de ce projet.

---

## 6. Angles de contact (`alpha.water`)

```cpp
// 0/alpha.water — conditions aux limites (extrait)

boundaryField
{
    pcb_left
    {
        type            dynamicAlphaContactAngle;
        theta0          35;           // Angle de contact PCB (°)
        thetaA          40;           // Angle d'avancée
        thetaR          30;           // Angle de recul
        uTheta          0.001;        // Vitesse seuil (m/s)
        limit           gradient;
        value           uniform 0;
    }

    pad_au_left
    {
        type            dynamicAlphaContactAngle;
        theta0          25;           // Or — très hydrophile
        thetaA          30;
        thetaR          20;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    die_top
    {
        type            dynamicAlphaContactAngle;
        theta0          25;           // SiN — très hydrophile
        thetaA          30;
        thetaR          20;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    dam_left
    {
        type            dynamicAlphaContactAngle;
        theta0          70;           // Barrage — mouillage partiel
        thetaA          75;
        thetaR          65;
        uTheta          0.001;
        limit           gradient;
        value           uniform 0;
    }

    buse_left_ext
    {
        type            constantAlphaContactAngle;
        theta0          150;          // PTFE — anti-mouillage
        limit           gradient;
        value           uniform 0;
    }

    inlet
    {
        type            fixedValue;
        value           uniform 0;    // Air entre par l'inlet
    }
}
```

**Points clés :**
- **dynamicAlphaContactAngle** : modèle avec hystérésis (θ_avancée ≠ θ_recul).
- **uTheta** : vitesse seuil pour la transition avancée/recul (0.001 m/s = 1 mm/s).
- Le PTFE de la buse extérieure (θ = 150°) est essentiel pour éviter que la résine ne remonte le long de la buse.

---

## 7. Profil d'injection (`U`)

```cpp
// 0/U — condition d'entrée (inlet)

inlet
{
    type            uniformFixedValue;
    uniformValue    table
    (
        (0.000    (0 -0.002 0))     // Début dispensing : 2 mm/s vers le bas
        (0.500    (0 -0.002 0))     // Fin dispensing à t = 0.5 s
        (0.501    (0  0     0))     // Arrêt brutal
        (1.000    (0  0     0))     // Settling (repos)
    );
}
```

**Phases de la simulation :**
1. **t = 0 → 0.5 s** : dispensing actif (v = 2 mm/s, débit Q ≈ 0.56 µL/s)
2. **t = 0.5 → 1.0 s** : repos : la résine s'étale par capillarité + gravité.

---

## 8. Génération de maillage (`generate_blockMeshDict.py`)

```python
#!/usr/bin/env python3
"""
Génère un blockMeshDict paramétrique pour l'encapsulation COB.
29 blocs structurés, 18 patches nommées.
"""

# Paramètres géométriques (mm → m via scale 0.001)
PARAMS = {
    "die_width":    1.0,    # mm — largeur du die
    "die_height":   0.3,    # mm — hauteur du die
    "pad_width":    0.4,    # mm — largeur pad Au (×2)
    "dam_width":    0.5,    # mm — largeur barrage (×2)
    "dam_height":   0.8,    # mm — hauteur barrage
    "nozzle_width": 0.6,    # mm — diamètre buse
    "nozzle_height": 1.5,   # mm — hauteur buse
    "cell_size":    0.015,  # mm — taille de maille (15 µm)
}


def generate_vertices(p: dict) -> list:
    """
    Génère les 60+ sommets du domaine 2D.
    Topologie : PCB (bas) + die (obstacle) + dam (côtés) + buse (haut).
    """
    # ... 29 blocs avec ratios d'aspect contrôlés ...


def generate_blocks(p: dict) -> list:
    """
    Génère les blocs hex avec résolution uniforme.
    Chaque bloc : (n_cells_x, n_cells_y, 1) pour le 2D.
    """
    nx = int(p["die_width"] / p["cell_size"])
    ny = int(p["die_height"] / p["cell_size"])
    # ... 29 définitions de blocs ...


def generate_patches() -> dict:
    """
    18 patches nommées :
    - 2 pcb (L/R), 2 pad_au (L/R), 3 die (top/L/R)
    - 2 dam (L/R), 2 dam_top (L/R)
    - 2 buse_int (L/R), 2 buse_ext (L/R)
    - 1 inlet, 1 atmosphere, 2 outlet (L/R)
    - front/back (empty pour 2D)
    """
```

**Points clés :**
- Le maillage est **paramétrique** : changer `cell_size` ou `dam_height` régénère tout le blockMeshDict.
- **29 blocs** : la topologie gère l'obstacle du die (non maillé) + les barrages latéraux + la buse.
- **18 patches** : chaque surface physique a son propre patch pour imposer des angles de contact différents.

---

## 9. Résumé des paramètres étudiés

| Paramètre | Min | Réf. | Max | Unité |
|-----------|-----|------|-----|-------|
| Taille maille | 10 | 15 | 20 | µm |
| η₀ (viscosité repos) | 5 | 15 | 50 | Pa·s |
| σ (tension surface) | 0.030 | 0.038 | 0.040 | N/m |
| θ_chip (angle die) | 15 | 25 | 60 | ° |
| θ_dam (angle barrage) | 40 | 70 | 120 | ° |
| y_dam (hauteur barrage) | 0.5 | 0.8 | 1.04 | mm |
| v_latérale (buse) | 1.7 | 2.5 | 5.0 | mm/s |
| t₁_end (fin dispensing) | 0.2 | 0.5 | 0.8 | s |

**Total : 38 cas simulés** (exploration non structurée, pas de DoE formel).
