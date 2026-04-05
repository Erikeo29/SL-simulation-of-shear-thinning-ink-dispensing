**Sommaire :**
1. Contexte applicatif
2. Géométrie du domaine
3. Rhéologie : modèle de Bird-Carreau
4. Tension de surface et mouillabilité
5. Analyse dimensionnelle
6. Équations fondamentales
7. Méthode numérique VOF
8. Matrice de l'étude
9. Enseignements physiques

---

## 1. Contexte applicatif

Ce projet modélise l'**encapsulation par glob top** d'un composant Chip-On-Board (COB). Le procédé consiste à dispenser une résine époxy rhéofluidifiante sur un die silicium et ses fils de connexion (*wire bonds*) pour les protéger mécaniquement et thermiquement.

**Application :** Packaging semiconducteur : biosenseurs, circuits intégrés bas coût.

**Procédé dam-and-fill :**
1. Die collé sur PCB (substrat FR-4)
2. Fils de connexion soudés (Au, Ø 25 µm, boucle ~500 µm)
3. Barrage (*dam*) en résine époxy posé autour du die
4. Dispensing du glob top (résine) depuis une buse mobile (Ø 0.6 mm)
5. Repos (*settling*) pour auto-nivellement capillaire
6. Cuisson (150°C, 1-2 h) → polymérisation

**Objectif de la simulation :** Prédire la couverture du die et le risque de débordement (*spillage*) du barrage en fonction des paramètres procédé.

---

## 2. Géométrie du domaine

Coupe 2D dans le plan XY (1 cellule en Z).

```
       INLET (buse, Ø 0.6 mm)
          ↓
    ╔═══════════╗  y = 2.35 mm
    ║   BUSE    ║
    ║  (mobile) ║
    ╠═══════════╣  y = 1.1 mm (bas buse = haut dam)
    ║           ║
  ╔═╩═══════════╩═╗
  ║ DAM    DIE    DAM ║  y = 0.8 mm (haut dam)
  ║ 0.5mm  1.0mm  0.5mm║
  ║        0.3mm      ║  y = 0.3 mm (haut die)
  ║  PCB    ║DIE║  PCB  ║
  ║  (Au)   ║   ║  (Au) ║
  ╚═════════╩═══╩═══════╝  y = 0
  x=-1.5                x=1.5 mm
```

| Élément | Dimensions | Matériau |
|---------|-----------|----------|
| Die | 1.0 × 0.3 mm | SiN (passivation). |
| Pads Au | 0.4 mm (×2, de chaque côté) | Or |
| Dam (barrage) | 0.5 × 1.04 mm (×2) | Résine époxy |
| Buse | Ø 0.6 mm, mobile (4 phases) | Acier + PTFE (extérieur). |
| PCB | Largeur totale 3.0 mm | FR-4 + solder mask |
| Maillage | ~28 500 cellules hex | 15 µm résolution (10 µm en production). |

---

## 3. Rhéologie : modèle de Bird-Carreau

La résine glob top est un fluide **rhéofluidifiant** (shear-thinning) : sa viscosité diminue sous cisaillement. Le modèle de Bird-Carreau capture les deux plateaux de viscosité :

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[1 + (\lambda \dot{\gamma})^2\right]^{(n-1)/2}$$

| Paramètre | Symbole | Valeur de référence | Unité |
|-----------|---------|-------------------|-------|
| Viscosité au repos | η₀ | 15 | Pa·s |
| Viscosité à cisaillement infini | η∞ | 1.0 | Pa·s |
| Temps de relaxation | λ | 10 | s |
| Indice rhéofluidifiant | n | 0.4 | - |
| Masse volumique | ρ | 1600 | kg/m³ |

**Note :** η₀ = 15 Pa·s correspond à la température de process (70-80°C). A 25°C, η₀ ≈ 50 Pa·s (datasheet). La simulation utilise la valeur à température de process.

**Interprétation physique :**
- **Au repos** (γ̇ → 0) : η → η₀ = 15 Pa·s → la résine reste en place (pas de drainage gravitaire).
- **Sous la buse** (γ̇ ~ 100 s⁻¹) : η → η∞ = 1 Pa·s → la résine s'écoule facilement.
- **Après dispensing** (γ̇ → 0) : η remonte → auto-nivellement capillaire lent, contrôlé.

Le rapport de viscosité résine/air est extrême : **1.5×10⁶**. Ce contraste impose un traitement numérique soigneux (solveur implicite pour la diffusion visqueuse).

---

## 4. Tension de surface et mouillabilité

### 4.1 Tension de surface

$\sigma$ = 0.035 N/m (35 mN/m, résine époxy / air à température de process, non polymérisée)

### 4.2 Angles de contact dynamiques

Les angles de contact varient selon le matériau de surface. Un modèle dynamique (hystérésis ±5°) est utilisé pour les surfaces critiques :

| Surface | Matériau | θ₀ (°) | Modèle | Caractère |
|---------|----------|--------|--------|-----------|
| PCB | Solder mask (FR-4) | 35 | Dynamique (±5°) | Hydrophile |
| Pads Au | Or (zone de soudure) | 25 | Dynamique (±5°) | Très hydrophile |
| Die | SiN (passivation chip) | 25 | Dynamique (±5°) | Très hydrophile |
| Dam | Résine époxy (barrage) | 70 | Dynamique (±5°) | Mouillage partiel |
| Buse intérieur | Acier inox | 90 | Constant | Neutre |
| Buse extérieur | PTFE | 150 | Constant | Anti-mouillage |

**Rôle physique :**
- θ(pads) = 25° et θ(die) = 25° : la résine *mouille* spontanément le die et les pads → bonne couverture.
- θ(dam) = 70° : le barrage freine l'avancée de la résine → prévention du débordement.
- θ(buse ext) = 150° : empêche la résine de remonter sur l'extérieur de la buse (coating PTFE).

### 4.3 Équation de Young

$$\cos\theta = \frac{\gamma_{SG} - \gamma_{SL}}{\sigma}$$

L'angle de contact traduit l'équilibre des énergies de surface à la ligne triple (solide-liquide-gaz).

---

## 5. Analyse dimensionnelle

**Conditions de référence :** U = 3.5 mm/s (v_disp, vitesse de dispensing), L = 0.6 mm (Ø buse), η₀ = 15 Pa·s (T_process).

| Nombre | Expression | Valeur | Interprétation |
|--------|-----------|--------|----------------|
| **Re** | ρUL/η₀ | 2×10⁻⁴ | Stokes pur : inertie totalement négligeable. |
| **Ca** | η₀U/σ | 1.5 | Visqueux ≈ capillaire pendant la dispense. |
| **Bo** | ρgL²/σ | 0.16 | Gravité négligeable. |
| **Oh** | η₀/√(ρσL) | 82 | Très visqueux (pas d'oscillations). |

**Régime biphasique (4 phases) :**
- **Phases 1-3 : dispensing** (Ca ~ 1.5) : les forces visqueuses et capillaires sont comparables → la forme de l'écoulement dépend de la rhéologie ET de la mouillabilité.
- **Phase 4 : settling** (Ca → 0) : la capillarité domine → auto-nivellement, la résine s'étale et mouille les surfaces hydrophiles.

Ce caractère biphasique (dispensing visqueux → repos capillaire) est la signature physique clé du procédé.

**Séquence temporelle de la buse mobile (2.8 s total) :**
1. Phase 1 [0 - 0.05 s] : dépôt stationnaire à x = -1.1 mm (côté gauche).
2. Phase 2 [0.05 - 0.49 s] : translation de -1.1 à +1.1 mm à v_lat = 5 mm/s.
3. Phase 3 [0.49 - 1.29 s] : dépôt stationnaire à x = +1.1 mm (0.8 s).
4. Phase 4 [1.29 - 2.8 s] : buse retirée, relaxation capillaire (1.5 s).

---

## 6. Équations fondamentales

### 6.1 Navier-Stokes incompressible

$$\rho\left[\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v}\right] = -\nabla p_{rgh} + \nabla \cdot [\mu(\nabla \mathbf{v} + \nabla \mathbf{v}^T)] + \sigma\kappa\nabla\alpha + \rho\mathbf{g}$$

### 6.2 Transport VOF

$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) + \nabla \cdot [\alpha(1-\alpha)\mathbf{v}_r] = 0$$

| α | Phase |
|---|-------|
| 1 | Résine époxy |
| 0 | Air |

### 6.3 Propriétés du mélange

$$\rho = \alpha \rho_{resine} + (1-\alpha) \rho_{air}$$
$$\mu = \alpha \mu_{resine}(\dot{\gamma}) + (1-\alpha) \mu_{air}$$

> La viscosité de la résine dépend du cisaillement local via Bird-Carreau.

---

## 7. Méthode numérique VOF

### 7.1 Solveur

**OpenFOAM v2406**, solveur `interFoam` (VOF avec tension de surface CSF).

### 7.2 Choix critique : cAlpha = 0

Le coefficient de compression artificielle **cAlpha** est fixé à **0** (désactivé). C'est un choix critique :

| cAlpha | Effet sur l'interface | Effet sur les angles de contact |
|--------|----------------------|-------------------------------|
| 1 (défaut) | Interface nette (~3 cellules) | **Inopérants.** La compression écrase les gradients capillaires. |
| **0 (ce projet)** | Interface diffuse (~5-7 cellules) | **Fonctionnels.** La physique pilote le mouillage. |

**Conséquence :** l'interface est plus diffuse, mais les angles de contact imposent correctement la physique de mouillage. Ce compromis est essentiel pour prédire la couverture du die.

### 7.3 Algorithme PIMPLE

| Paramètre | Valeur | Note |
|-----------|--------|------|
| nOuterCorrectors | 2 | Plus élevé que standard (1). Nécessaire pour le couplage haute viscosité. |
| nCorrectors | 3 | Corrections pression-vitesse internes. |
| momentumPredictor | no | Standard VOF |

### 7.4 Pas de temps adaptatif

- deltaT initial : 0.1 µs
- maxCo = 0.3, maxAlphaCo = 0.3
- maxDeltaT : 500 µs
- endTime : 2.8 s (1.29 s dispensing + 1.51 s settling).

---

## 8. Étude paramétrique (3 axes)

L'étude paramétrique porte sur 7 cas (039-045), organisés autour de 3 axes avec le cas 039 comme référence.

**Cas de référence (039) :** v_disp = 3.5 mm/s, v_lat = 5.0 mm/s, η₀ = 15 Pa·s. Résultat : remplissage optimal, dôme ~1.4 mm, volume dispensé 2.71 mm².

| ID | Axe | Paramètre varié | V_disp (mm²) | Delta vol. | Verdict |
|----|-----|-----------------|-------------|-----------|---------|
| **039** | **Référence** | - | **2.71** | - | Optimal. |
| 040 | v_disp | 2.0 mm/s (-43%) | 1.55 | -43% | Sous-remplissage, die exposé. |
| 041 | v_disp | 5.0 mm/s (+43%) | 3.87 | +43% | Sur-remplissage, dôme massif. |
| 042 | v_lat | 3.5 mm/s (lent) | 3.11 | +15% | Bonne symétrie, léger surplus. |
| 043 | v_lat | 7.5 mm/s (rapide) | 2.40 | -11% | Légère asymétrie droite. |
| 044 | η₀ | 5 Pa·s (fluide) | 2.71 | 0% | Résultat final identique. |
| 045 | η₀ | 25 Pa·s (visqueux) | 2.71 | 0% | Résultat final identique. |

---

## 9. Enseignements physiques

1. **Le débit de dispense (v_disp) est le levier principal.** Le volume dispensé est strictement proportionnel à v_disp (V = v_disp × Ø_buse × t_dispense). Un écart de ±43% en débit produit ±43% en volume. Fenêtre de process : 3.0-4.0 mm/s.

2. **La vitesse latérale (v_lat) a un effet indirect via le temps de traversée.** Une buse plus lente (v_lat = 3.5 mm/s) met plus longtemps à traverser le die → temps de dispense total plus long → plus de volume (+15%). Ce n'est pas la distribution latérale qui change, c'est le volume total.

3. **La viscosité (η₀) n'affecte pas le résultat final** dans la plage 5-25 Pa·s. Le settling (1.5 s) est suffisamment long pour que la capillarité homogénéise la forme finale quelle que soit la viscosité. Conséquence favorable : la température de process n'a pas besoin d'être très précise.

4. **Le régime est biphasique.** Pendant le dispensing (Ca ~ 1.5), la rhéologie pilote ; pendant le settling (Ca → 0), la capillarité prend le relais. Les deux phases doivent être simulées.

5. **cAlpha = 0 est non négociable.** Activer la compression artificielle (cAlpha = 1) rend les angles de contact inopérants. L'interface diffuse (~5-7 cellules) est le prix à payer pour une physique correcte.

6. **Hiérarchie de sensibilité :** v_disp (±43%) >> v_lat (±15%) >> η₀ (0%).
