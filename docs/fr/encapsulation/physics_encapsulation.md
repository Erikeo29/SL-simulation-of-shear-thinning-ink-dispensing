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
| Dam (barrage) | 0.5 × 0.5-1.0 mm (×2) | Résine époxy |
| Buse | Ø 0.6 mm, hauteur 1.5 mm | Acier + PTFE (extérieur). |
| PCB | Largeur totale 3.0 mm | FR-4 + solder mask |
| Maillage | ~100k cellules hex | 10-20 µm résolution. |

---

## 3. Rhéologie : modèle de Bird-Carreau

La résine glob top est un fluide **rhéofluidifiant** (shear-thinning) : sa viscosité diminue sous cisaillement. Le modèle de Bird-Carreau capture les deux plateaux de viscosité :

$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty) \left[1 + (\lambda \dot{\gamma})^2\right]^{(n-1)/2}$$

| Paramètre | Symbole | Valeur de référence | Unité |
|-----------|---------|-------------------|-------|
| Viscosité au repos | η₀ | 15-50 | Pa·s |
| Viscosité à cisaillement infini | η∞ | 1.0 | Pa·s |
| Temps de relaxation | λ | 10 | s |
| Indice rhéofluidifiant | n | 0.4 | - |
| Masse volumique | ρ | 1200 | kg/m³ |

**Interprétation physique :**
- **Au repos** (γ̇ → 0) : η → η₀ = 50 Pa·s → la résine reste en place (pas de drainage gravitaire).
- **Sous la buse** (γ̇ ~ 100 s⁻¹) : η → η∞ = 1 Pa·s → la résine s'écoule facilement.
- **Après dispensing** (γ̇ → 0) : η remonte → auto-nivellement capillaire lent, contrôlé.

Le rapport de viscosité résine/air est extrême : **5×10⁶**. Ce contraste impose un traitement numérique soigneux (solveur implicite pour la diffusion visqueuse).

---

## 4. Tension de surface et mouillabilité

### 4.1 Tension de surface

$\sigma$ = 0.038 N/m (38 mN/m, résine époxy / air à 25°C, non polymérisée)

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

**Conditions de référence :** U = 1 mm/s (vitesse de dispensing), L = 0.6 mm (Ø buse)

| Nombre | Expression | Valeur | Interprétation |
|--------|-----------|--------|----------------|
| **Re** | ρUL/μ | 0.012 | Stokes : inertie négligeable. |
| **Ca** | μU/σ | 1.3 | Viscoélastique ≈ capillaire. |
| **Bo** | ρgL²/σ | 0.077 | Gravité négligeable. |
| **Oh** | μ/√(ρσL) | 330 | Extrêmement visqueux (pas d'oscillations). |

**Régime biphasique :**
- **Pendant le dispensing** (Ca ~ 1) : les forces visqueuses et capillaires sont comparables → la forme de l'écoulement dépend de la rhéologie ET de la mouillabilité.
- **Pendant le repos** (Ca → 0.1) : la capillarité domine → auto-nivellement, le résine s'étale et mouille les surfaces hydrophiles.

Ce caractère biphasique (dispensing visqueux → repos capillaire) est la signature physique clé du procédé.

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
- endTime : 1.0 s (0.5 s dispensing + 0.5 s repos).

---

## 8. Matrice de l'étude

38 cas ont été simulés. Voici les cas représentatifs disponibles dans cet outil :

| ID | Description | Paramètre clé | Die (%) | Dam spillage | Verdict |
|----|-------------|---------------|---------|--------------|---------|
| **025** | **Meilleur cas (offset die)** | x_start = −0.5 mm | **96%** | **0%** | ✅ Validé |
| 026 | Baseline physique corrigée | Référence | ~90% | Faible | ✅ |
| 028 | Maillage 10 µm | cell = 10 µm | 95% | 0% | ✅ |
| 033 | Dispensing symétrique | v_lat symétrique | 100% | Asymétrie L/R | ⚠️ |
| 034 | 10 µm + nozzle | cell = 10 µm, nozzle | 100% | 0% | ✅ |
| 035 | Settling étendu | t₁_end = 0.8 s | 100% | 0% | ✅ |
| 036 | Viscosité faible | η₀ = 7.5 Pa·s | 55% | Drainage | ❌ |
| 037 | Tension de surface réduite | σ = 35 mN/m | 100% | 0% | ✅ |
| 038 | Buse rapide | v_lat = 5 mm/s | 90% | Symétrie dam | ⚠️ |

---

## 9. Enseignements physiques

1. **La position de la buse domine.** L'asymétrie L/R est cinématique (timing du dispensing), pas due aux propriétés matériaux. Décaler la buse (cas 025) corrige l'asymétrie.

2. **La résolution du maillage est critique.** 10 µm résout les détails capillaires (bord du die, pads Au de 25-30 µm). À 15-20 µm, l'interface est pixellisée et les asymétries sont des artefacts numériques.

3. **La hauteur du barrage (dam) compte plus que l'angle de contact.** Un barrage physique (0.8-1.0 mm) est plus efficace qu'un angle de contact élevé pour empêcher le débordement.

4. **La viscosité tolère une large gamme.** Entre 7.5 et 50 Pa·s, l'encapsulation fonctionne. En dessous de 7.5 Pa·s, le drainage gravitaire devient problématique (cas 036).

5. **Le régime est biphasique.** Pendant le dispensing (Ca ~ 1), la rhéologie pilote ; pendant le repos (Ca → 0.1), la capillarité prend le relais. Les deux phases doivent être simulées.

6. **cAlpha = 0 est non négociable.** Activer la compression artificielle (cAlpha = 1) rend les angles de contact inopérants. L'interface diffuse (~5-7 cellules) est le prix à payer pour une physique correcte.
