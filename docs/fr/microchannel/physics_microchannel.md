**Sommaire :**
1. Contexte applicatif
2. Géométrie du micro-canal
3. Physique du remplissage capillaire
4. Équations fondamentales
5. Méthode numérique VOF
6. Paramètres de l'étude
7. Coût computationnel

---

## 1. Contexte applicatif

Ce projet modélise le **remplissage capillaire** d'un micro-canal destiné à un capteur microfluidique (µTAS - Micro Total Analysis System : système d'analyse miniaturisé intégrant sur une seule puce les étapes de prélèvement, transport et détection d'un échantillon liquide). L'objectif est de comprendre comment les propriétés physicochimiques du canal influencent la vitesse de remplissage par capillarité, paramètre critique pour le temps de réponse du capteur.

**Application :** Micro-électrodes pour biosenseurs (détection d'analytes dans le liquide).

---

## 2. Géométrie du micro-canal

Le domaine est une **coupe 2D dans le plan xz** d'un canal de 125 µm de profondeur, avec deux électrodes protubérantes.

```
y (µm)
125  |________________________________________________|  Paroi sup. (θ_top)
     |          ___       ___                          |
     |  inlet  |e1 |     |e2 |                        |
  22 |_________|   |_____|   |_________________________|  Électrodes (θ_elec)
   0 |________________________________________________|  Substrat (θ_bottom)
     ↑         ↑0.4 ↑0.9 ↑1.3 ↑1.8                  ↑
   inlet                                            outlet
   x = -0.2 mm                                     x = 3.8 mm
```

| Élément | Dimension | Détail |
|---------|-----------|--------|
| Longueur du canal | 4.0 mm | De x = −0.2 à x = 3.8 mm. |
| Profondeur (hauteur) | 125 µm | Distance substrat-paroi supérieure. |
| Électrodes (×2) | 500 µm × 22 µm | Protubérantes depuis le substrat. |
| Chamfrein électrodes | R = 3 µm | Évite le piégeage de Gibbs aux coins. |
| Maillage | ~100k cellules quad | Résolution 5 µm, raffinement 2.5 µm aux coins. |

---

## 3. Physique du remplissage capillaire

### 3.1 Moteur du remplissage : pression capillaire

Le remplissage est piloté par deux forces :
- **Pression d'entrée** : ΔP = 300 Pa (pression hydrostatique du liquide).
- **Pression capillaire (Young-Laplace)** :

$$\Delta P_{cap} = \sigma \left(\frac{\cos\theta_{top} + \cos\theta_{bottom}}{h}\right)$$

où :
- $\sigma$ = tension de surface (N/m)
- $\theta_{top}$, $\theta_{bottom}$ = angles de contact sur la paroi supérieure et le substrat (°).
- $h$ = hauteur du canal (m)

**Interprétation physique :** Si $\theta < 90°$ (hydrophile), le ménisque est concave et la pression capillaire *pousse* le liquide vers l'avant. Si $\theta > 90°$ (hydrophobe), le ménisque est convexe et la pression capillaire *freine* l'avancée.

### 3.2 Angles de contact

L'angle de contact $\theta$ traduit la mouillabilité d'une surface. Il est défini par l'équation de Young :

$$\cos\theta = \frac{\gamma_{SG} - \gamma_{SL}}{\gamma_{LG}}$$

où :
- $\gamma_{SG}$ = énergie de surface solide-gaz
- $\gamma_{SL}$ = énergie de surface solide-liquide
- $\gamma_{LG}$ = tension de surface liquide-gaz ($= \sigma$)

| Surface | Matériau | θ baseline | Caractère |
|---------|----------|-----------|-----------|
| Paroi supérieure | PET traité | 22° | Très hydrophile. |
| Substrat (bas) | PET brut | 121° | Hydrophobe. |
| Électrodes | Ni/Au | 96° | Légèrement hydrophobe. |

### 3.3 Résistance visqueuse

Le canal étant très fin (125 µm), l'écoulement est dominé par la viscosité (Re << 1). La résistance visqueuse pour un écoulement de Poiseuille entre plaques parallèles :

$$\Delta P_{visc} = \frac{12 \mu L v}{h^2}$$

où :
- $\mu$ = viscosité dynamique (Pa·s)
- $L$ = longueur mouillée (m)
- $v$ = vitesse moyenne du front (m/s)
- $h$ = hauteur du canal (m)

### 3.4 Nombre de Reynolds

$$Re = \frac{\rho v h}{\mu} \approx \frac{1005 \times 0.3 \times 125 \times 10^{-6}}{9 \times 10^{-4}} \approx 0.04$$

Le régime est **laminaire** ($Re \ll 1$) : les forces d'inertie sont négligeables devant les forces visqueuses.

### 3.5 Nombre capillaire

$$Ca = \frac{\mu v}{\sigma} \approx \frac{9 \times 10^{-4} \times 0.3}{0.072} \approx 3.8 \times 10^{-3}$$

$Ca \ll 1$ : la tension de surface domine les forces visqueuses à l'interface. Le ménisque adopte une forme quasi-statique (faible déformation dynamique).

---

## 4. Équations fondamentales

### 4.1 Navier-Stokes incompressible

**Conservation de la masse :**
$$\nabla \cdot \mathbf{v} = 0$$

**Conservation de la quantité de mouvement :**
$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p + \nabla \cdot (\mu \nabla \mathbf{v}) + \rho\mathbf{g} + \mathbf{f}_\sigma$$

### 4.2 Transport de la fraction volumique (VOF)

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

| Valeur de α | Signification |
|-------------|---------------|
| α = 1 | Liquide (eau). |
| α = 0 | Air. |
| 0 < α < 1 | Zone d'interface. |

### 4.3 Propriétés du mélange

$$\rho = \alpha \rho_{eau} + (1-\alpha) \rho_{air}$$
$$\mu = \alpha \mu_{eau} + (1-\alpha) \mu_{air}$$

### 4.4 Force de tension de surface (CSF)

Modèle de Brackbill (*Continuum Surface Force*) :

$$\mathbf{f}_\sigma = \sigma \kappa \nabla \alpha$$

où $\kappa = -\nabla \cdot \left(\frac{\nabla \alpha}{|\nabla \alpha|}\right)$ est la courbure de l'interface.

---

## 5. Méthode numérique VOF

### 5.1 Solveur

**OpenFOAM 13** avec le solveur `incompressibleVoF` (successeur de `interFoam`).

### 5.2 Reconstruction d'interface PLIC

À la différence du projet de dispense d'encre (qui utilise MULES avec compression artificielle), ce projet utilise la reconstruction **PLIC** (*Piecewise Linear Interface Calculation*) :

- L'interface est reconstruite géométriquement comme un segment de droite dans chaque cellule.
- Pas de diffusion numérique de l'interface (contrairement à MULES).
- Nécessite un **maillage structuré** (quadrilatères) pour une reconstruction optimale.
- **cAlpha = 0** : la compression artificielle est désactivée pour permettre aux conditions d'angle de contact de piloter la physique.

### 5.3 Conditions aux limites

| Frontière | Type U | Type α | Détail |
|-----------|--------|--------|--------|
| Inlet | fixedValue (ΔP=300 Pa) | inletOutlet | Pression motrice. |
| Outlet | inletOutlet | inletOutlet | Pression de référence 0 Pa. |
| Paroi supérieure | noSlip | contactAngle (θ_top) | Paroi supérieure. |
| Substrat | noSlip | contactAngle (θ_bottom) | Paroi inférieure. |
| Électrodes | noSlip | contactAngle (θ_elec) | Surfaces Ni/Au. |
| Front/Back | empty | empty | Symétrie 2D. |

### 5.4 Propriétés des fluides

| Propriété | Liquide (eau) | Air |
|-----------|-------------|-----|
| ρ (kg/m³) | 1005 | 1.2 |
| ν (m²/s) | 8.96×10⁻⁷ | 1.48×10⁻⁵ |
| μ (mPa·s) | 0.90 | 0.018 |
| σ (mN/m) | 72 | - |

> **Note :** Le fluide est newtonien (pas de modèle de Carreau ici), contrairement au projet de dispense d'encre.

---

## 6. Paramètres de l'étude

L'étude paramétrique couvre **7 configurations** en faisant varier un paramètre à la fois par rapport au cas de référence (baseline).

| ID | Description | Paramètre varié | Valeur | t_fill (ms) | Δ vs baseline |
|----|-------------|-----------------|--------|-------------|---------------|
| **001** | **Baseline (référence)** | - | – | **13.7** | - |
| 002 | Substrat neutre | θ_bottom | 90° (vs 121°) | 11.9 | −13% |
| 003 | Substrat hydrophile | θ_bottom | 60° (vs 121°) | 10.6 | −23% |
| 004 | Viscosité ×1.5 | μ | 1.35 mPa·s (vs 0.90) | 20.2 | +47% |
| 005 | Surfactant (σ×0.5) | σ | 36 mN/m (vs 72) | 16.2 | +18% |
| 006 | Électrodes hydrophiles | θ_elec | 45° (vs 96°) | 10.8 | −21% |
| 007 | Paroi supérieure moins hydrophile | θ_top | 45° (vs 22°) | 16.3 | +19% |

**Classement par vitesse de remplissage (le plus rapide en premier) :**

003 (10.6 ms) > 006 (10.8 ms) > 002 (11.9 ms) > 001 (13.7 ms) > 005 (16.2 ms) ≈ 007 (16.3 ms) > 004 (20.2 ms)

### Enseignements physiques

1. **Angle de contact substrat** : effet dominant. Passer de θ = 121° (hydrophobe) à 60° (hydrophile) réduit le temps de remplissage de 23 %. Le substrat est la plus grande surface mouillée, donc son mouillabilité pilote la pression capillaire nette.

2. **Viscosité** : effet le plus fort. +50 % de viscosité donne +47 % de temps de remplissage. Dans un canal fin, la résistance visqueuse ($\propto \mu / h^2$) est le frein dominant.

3. **Surfactant (σ÷2)** : effet contre-intuitif. Réduire σ *ralentit* le remplissage (+18 %) car la force motrice capillaire (∝ σ·cos θ / h) diminue plus que la résistance interfaciale.

4. **Mouillabilité de la paroi supérieure** : θ_top = 45° vs 22° donne +19 %. La paroi supérieure contribue significativement à la pression capillaire car elle représente la moitié du périmètre mouillé.

5. **Mouillabilité des électrodes** : effet modeste (−21 % apparent mais les électrodes n'occupent que ~0.6 % de la surface mouillée totale).

---

## 7. Coût computationnel

| Configuration | Cellules | Résolution | Temps/cas | Hardware |
|---------------|----------|------------|-----------|----------|
| **Ce projet** | ~100k | 5 µm (2.5 µm coins) | **5-15 min** | 6 cœurs |

**Paramètres de stabilité :**
- maxCo = 0.2, maxAlphaCo = 0.2
- Pas de temps adaptatif (Euler, 1er ordre).
- deltaT initial = 0.1 µs, maxDeltaT = 50 µs.

> **Comparaison :** Ce cas est ~10× plus rapide que le projet de dispense d'encre (50k cellules, 0.5-2h) car le canal est plus simple géométriquement et le fluide est newtonien.
