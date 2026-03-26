**Sommaire :**
1. Contexte scientifique et industriel
2. Propriétés des fluides rhéofluidifiants
3. Défis de la modélisation numérique
4. Système physique étudié
5. Approche multi-modèles
6. Références bibliographiques

---

# Modélisation de la dispense de fluides rhéofluidifiants

## 1. Contexte scientifique et industriel

### 1.1 Technologies de dispense microfluidique

La dispense de fluides en microfluidique englobe un ensemble de techniques permettant le dépôt contrôlé de volumes de l'ordre du nanolitre au microlitre. Ces procédés trouvent des applications dans de nombreux domaines industriels :

- Fabrication de capteurs électrochimiques: dépôt d'encre pour électrode de référence, pour électrode conductrice, pour fonctionnalisation chimique ou biochimique...
- Électronique imprimée: circuits conducteurs, antennes RFID, module packaging...
- Revêtements fonctionnels et couches minces.
- Dosage pharmaceutique de précision.

### 1.2 Mécanismes physiques

La dispense de fluides implique plusieurs phénomènes physiques couplés :
- **Écoulement diphasique** : interaction fluide/air à l'interface.
- **Capillarité** : tension superficielle et mouillage sur les parois.
- **Rhéologie** : comportement non-newtonien des fluides complexes.
- **Dynamique interfaciale** : déformation, étalement, pincement.

---

## 2. Propriétés des fluides rhéofluidifiants

### 2.1 Comportement non-newtonien

Les fluides rhéofluidifiants sont des fluides **non-newtoniens** dont la viscosité apparente diminue sous l'effet d'un cisaillement. Ce comportement est essentiel pour la dispense : le fluide s'écoule facilement sous pression mais conserve sa forme au repos.

**Loi de puissance (Ostwald-de Waele) :**

$$\tau = K\dot{\gamma}^n \quad \text{avec } n < 1$$

où $\tau$ est la contrainte de cisaillement, $K$ l'indice de consistance, $\dot{\gamma}$ le taux de cisaillement, et $n$ l'indice de comportement.

### 2.2 Modèle de Carreau-Yasuda

$$\eta(\dot{\gamma}) = \eta_\infty + \frac{\eta_0 - \eta_\infty}{[1 + (k\dot{\gamma})^a]^{(1-n)/a}}$$

où $\eta_0$ et $\eta_\infty$ sont les viscosités à cisaillement nul et infini, et $k$, $a$ des paramètres d'ajustement.

**Exemple :** Une encre rhéofluidifiante peut présenter un  $\eta_0 = 0.5$-$15$ Pa·s (au repos) et $\eta_\infty = 0.05$ Pa·s sous fort cisaillement.

---

## 3. Défis de la modélisation numérique

### 3.1 Enjeux techniques

| Défi | Description | Approche |
|------|-------------|----------|
| **Suivi d'interface** | Capturer la déformation de l'interface fluide/air | VOF, Phase-Field, Level-Set |
| **Rhéologie complexe** | Modéliser le comportement non-newtonien | Lois constitutives (Carreau, Herschel-Bulkley) |
| **Mouillage** | Gérer les angles de contact dynamiques | Conditions aux limites spécifiques |
| **Multi-échelles** | Du micron (interface) au millimètre (puit) | Maillages adaptatifs, méthodes sans maillage |
| **Coût calcul** | Simulations 2D ou 3D transitoires coûteuses | GPU, parallélisation, méthodes hybrides |

---

## 4. Système physique étudié

### 4.1 Configuration géométrique

Le système modélisé consiste en :
- **Buse de dispense** : diamètre 200-350 µm, positionnée au-dessus du micro-via.
- **Micro-via** : diamètre 800-1500 µm, profondeur ~130 µm.
- **Fluide** : encre rhéofluidifiante ($\rho$ = 3000 kg/m³).
- **Environnement** : température ambiante (~20°C) et pression atmosphérique.

### 4.2 Paramètres de simulation

| Paramètre | Plage | Unité |
|-----------|-------|-------|
| Diamètre micro-via | 800 - 1500 | µm |
| Diamètre buse | 200 - 350 | µm |
| Décalage horizontal (buse vs centre puit) | 0, -75, -150 | µm |
| Décalage vertical (buse vs haut du puit) | -30, 0, 30, 60 | µm |
| Viscosité zéro cisaillement $\eta_0$ | 0.5, 1.5, 5 | Pa·s |
| Viscosité $\eta_\infty$ | 0.05 - 0.5 | Pa·s |
| Angle de contact paroi | 15 - 120 | ° |
| Angle de contact fond du micro-via | 15 - 65 | ° |
| Angle de contact substrat (plateau) | 15 - 120 | ° |
| Temps de dispense | 20 - 40 | ms |

---

## 5. Approche multi-modèles

Ce projet compare trois méthodes numériques complémentaires :

| Modèle | Approche | Avantage principal |
|--------|----------|-------------------|
| **VOF** | Eulérienne, volumes finis | Robustesse, référence industrielle (utilisé par Airbus, Danone, Volkswagen, Siemens...) |
| **LBM** | Mésoscopique, réseau | Performance GPU, géométries complexes |
| **SPH** | Lagrangienne, sans maillage | Surfaces libres, grandes déformations |

---

## 6. Références bibliographiques

> **Note** : Pour la liste complète des références, consultez la section **Références bibliographiques** dans le menu Annexes.

