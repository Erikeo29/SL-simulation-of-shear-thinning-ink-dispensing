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
        nu0     nu0  [0 2 -1 0 0 0 0] 9.375e-3;  // η₀/ρ = 15/1600 m²/s
        nuInf   nuInf [0 2 -1 0 0 0 0] 6.25e-4;   // η∞/ρ = 1.0/1600 m²/s
        k       k    [0 0 1 0 0 0 0] 10;           // λ = 10 s
        n       n    [0 0 0 0 0 0 0] 0.4;          // indice rhéofluidifiant
    }

    rho     1600;    // kg/m³ — résine époxy chargée silice
}

air
{
    transportModel  Newtonian;
    nu              8.33e-6;  // m²/s
    rho             1.2;      // kg/m³
}

sigma   0.035;    // N/m — tension de surface résine/air (35 mN/m)
```

**Points clés :**
- **BirdCarreau** (et non Carreau) : OpenFOAM v2406 utilise ce nom pour le modèle complet avec les deux plateaux.
- Le rapport ν₀/ν∞ = 15 → forte rhéofluidification.
- Conversion : ν = η / ρ (OpenFOAM attend la viscosité cinématique).

---

## 3. Contrôle de la simulation (`controlDict`)

```cpp
// system/controlDict

application     interFoam;

startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         2.8;              // 2.8 s total (1.29 s dispensing + 1.51 s settling)

deltaT          1e-7;             // Pas de temps initial (0.1 µs)

writeControl    adjustableRunTime;
writeInterval   0.010;            // Écriture toutes les 10 ms → 100 frames

adjustTimeStep  yes;
maxCo           0.3;
maxAlphaCo      0.3;
maxDeltaT       5e-4;             // Max 500 µs
```

**Points clés :**
- **endTime = 2.8 s** : simulation longue pour capturer le dispensing (4 phases) ET le settling (1.5 s).
- **writeInterval = 10 ms** : compromis entre résolution temporelle et volume de données (~280 frames).
- La buse est mobile : une `codedFunctionObject` dans le controlDict calcule la position x de la buse en fonction du temps (4 phases : dépôt stationnaire, translation, dépôt final, retrait).
- La phase de settling (1.5 s) est essentielle : la résine continue de s'écouler par capillarité après le retrait de la buse.

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

## 7. Profil d'injection (`U`) et buse mobile

La vitesse d'entrée et la position de la buse sont gérées par une `codedFunctionObject` dans le controlDict. La buse est mobile en x et la dispense est active pendant les phases 1-3.

```cpp
// Séquence temporelle (codedFunctionObject dans controlDict) :
//
// Phase 1 [0, 0.05 s]      : stationnaire à x = -1.1 mm, dispense ON
// Phase 2 [0.05, 0.49 s]   : translation -1.1 → +1.1 mm à v_lat = 5 mm/s
// Phase 3 [0.49, 1.29 s]   : stationnaire à x = +1.1 mm, dispense ON
// Phase 4 [1.29, 2.8 s]    : buse retirée, settling (capillarité)
//
// v_disp = 3.5 mm/s (vitesse de dispensing, constante phases 1-3)
// V_total = v_disp × Ø_buse × t_disp = 3.5 × 0.6 × 1.29 = 2.71 mm²
```

**Phases de la simulation :**
1. **t = 0 → 0.05 s** : dépôt stationnaire côté gauche (x = -1.1 mm).
2. **t = 0.05 → 0.49 s** : translation de la buse (-1.1 → +1.1 mm).
3. **t = 0.49 → 1.29 s** : dépôt stationnaire côté droit (0.8 s).
4. **t = 1.29 → 2.8 s** : settling, la résine s'étale par capillarité.

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

| Paramètre | Min | Réf. (039) | Max | Unité |
|-----------|-----|-----------|-----|-------|
| v_disp (débit buse) | 2.0 | 3.5 | 5.0 | mm/s |
| v_lat (vitesse latérale) | 3.5 | 5.0 | 7.5 | mm/s |
| η₀ (viscosité repos) | 5 | 15 | 25 | Pa·s |
| σ (tension surface) | - | 0.035 | - | N/m |
| θ_chip (angle die) | - | 25 | - | ° |
| θ_dam (angle barrage) | - | 70 | - | ° |
| Taille maille | - | 15 | - | µm |

**Étude paramétrique structurée : 7 cas (039-045), 3 axes.**
