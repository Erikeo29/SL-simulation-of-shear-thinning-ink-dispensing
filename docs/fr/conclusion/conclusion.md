**Sommaire :**
1. Conclusion
2. Perspectives
   - 2.1 Alternatives Open Source en Python
   - 2.2 Intelligence artificielle et modélisation hybride
   - 2.3 Impression 4D et encres intelligentes
   - 2.4 Opportunités de recherche
   - 2.5 Calcul quantique
3. Références bibliographiques

---

## 1. Conclusion

Cette étude a permis de modéliser la dispense d'une encre rhéofluidifiante dans des micro-via en utilisant trois méthodes numériques distinctes : VOF, LBM et SPH.

Les résultats les plus réalistes ont été obtenus par la méthode VOF (OpenFOAM) et proches de ce qui peut être attendu d'après la physique et de ce que des outils commerciaux de modélisation peuvent produire. Notamment, l'impact de la position de la buse en X sur le phénomène d'overflow et sur l'uniformité du remplissage a pu être mis en évidence. De même, les phénomènes physicochimiques attendus ont été reproduits : l'influence de la viscosité et des angles de contact (énergie de surface) sur l'étalement de l'encre correspond aux comportements physiques anticipés.

Des différences de résultats apparaissent néanmoins selon les modèles utilisés, ce qui est attendu compte tenu de leurs formulations numériques très différentes (eulérien vs lagrangien, maillé vs sans maillage, macroscopique vs mésoscopique). 

Pour aller plus loin, il serait nécessaire de poursuivre l'amélioration des codes, d'affiner les modèles physicochimiques (notamment la rhéologie et le mouillage dynamique) et d'optimiser les paramètres numériques pour améliorer la justesse des résultats par rapport aux attentes  expérimentales.

---

## 2. Perspectives

### 2.1 Alternatives Open Source en Python

L'échec de l'implémentation initiale FEM/Phase-Field (basée sur une tentative de reproduction de modèles commerciaux) a mis en lumière la nécessité d'outils Python robustes pour la modélisation avancée de la mécanique des fluides. Les packages suivant pourraient aider à crééer des codes de modélisation sous Python qui reste un outil plus simple à faire évoluer que l'environnement Openfoam en C++ :

- **Firedrake** : un système automatisé pour la résolution d'équations aux dérivées partielles par la méthode des éléments finis. Très performant pour la mécanique des fluides computationnelle (CFD), il offre une syntaxe proche des mathématiques (UFL).
- **SfePy (Simple Finite Elements in Python)** : une bibliothèque flexible pour résoudre des systèmes d'équations aux dérivées partielles couplées (mécanique, thermiques, fluides) par éléments finis. Idéal pour des problèmes multiphysiques complexes.
- **Systèmes Hybrides FEM/SPH** : une voie prometteuse consiste à coupler la précision des éléments finis (FEM) près des parois solides avec la flexibilité du SPH (Smoothed Particle Hydrodynamics) pour l'interface libre.

---

### 2.2 Intelligence artificielle et modélisation hybride

### PINN (Physics-Informed Neural Networks)

Les **PINN** permettent de combiner les équations physiques avec des réseaux de neurones pour accélérer les simulations :

- **Principe :** le réseau apprend à résoudre les équations de Navier-Stokes en minimisant à la fois l'erreur de données et la violation des équations physiques.
- **Application inkjet :** Raissi et al. (2020) ont utilisé des PINN pour résoudre Navier-Stokes avec une précision comparable à FEM mais 100× plus rapidement.
- **Limitation actuelle :** généralisation limitée hors du domaine d'entraînement (pas d'extrapolation fiable).

### Modèles de substitution (Surrogate Models)

Les **modèles de substitution** consistent à entraîner une "IA simplifiée" (comme un réseau de neurones) pour prédire instantanément le résultat d'une simulation complexe :

- **Principe :** on réalise quelques centaines de simulations réelles (VOF, LBM...) pour "montrer" au modèle comment le fluide réagit.
- **Avantage :** une fois entraîné, le modèle peut prédire la forme de la dispense et ce en quelques millisecondes, sans avoir à relancer un calcul OpenFOAM de plusieurs heures.
- **Potentiel :** optimisation en temps réel des paramètres sur une ligne de production.

### Apprentissage par renforcement

- **Principe :** il s'agit d'entraîner un programme informatique, appelé **"agent"**, à prendre les meilleures décisions possibles pour atteindre un objectif. L'agent apprend par essais-erreurs, en étant "récompensé" pour les bonnes actions (par exemple, une dispense réussie) et "puni" pour les mauvaises (un débordement).
- **Application :** un agent pourrait apprendre à ajuster dynamiquement la pression ou la vitesse de la buse pour garantir un remplissage optimal, même si les propriétés de l'encre changent légèrement.
- **Outils :** des bibliothèques open-source comme `Stable-Baselines3` (basée sur PyTorch) ou `Ray RLlib` (pour les systèmes à grande échelle) permettent de mettre en œuvre ces algorithmes.
- **Potentiel :** permettre aux machines de s'auto-corriger en temps réel et de s'adapter aux variations de l'encre ou de l'environnement, sans intervention humaine.

---

### 2.3 Impression 4D et encres intelligentes

Les encres rhéofluidifiantes sont de plus en plus utilisées pour l'**impression 4D** (matériaux qui changent de forme après impression) :

### Encres à mémoire de forme

- Polymères qui se déforment sous l'effet de la température ou de la lumière.
- **Modélisation :** Couplage FEM avec des modèles thermomécaniques.


---

### 2.4 Opportunités de recherche

### Couplage rhéologie-interface

**Problématique :** il n'existe pas dans la littérature de modèle qui gère simultanément la rhéologie non-newtonienne (thixotropie) et les interfaces libres avec une précision sub-micronique.

**Pistes de recherche :**
- **Hybridation VOF-SPH** : VOF pour le suivi d'interface, SPH pour la rhéologie.
- **LBM avec rhéologie avancée** : implémenter des modèles de thixotropie et de viscoélasticité dans LBM.
- **FEM adaptatif** : maillages dynamiques qui s'adaptent aux zones de fort cisaillement.

### Échelles sub-microniques

**Problématique :** les gouttes < 5 µm sont difficiles à modéliser en raison des effets de tension superficielle dominants et des temps de calcul prohibitifs.

**Pistes de recherche :**
- **Modèles multi-échelles** : coupler un modèle macroscopique (VOF, FEM) avec un modèle mésoscopique (LBM).
- **Simulations atomistiques** : utiliser la dynamique moléculaire (MD) pour les gouttes < 1 µm.


---

### 2.5 Calcul quantique

Le calcul quantique pourrait révolutionner la modélisation des écoulements complexes :

### Algorithmes quantiques pour SPH

- les ordinateurs quantiques pourraient simuler 10⁹ particules SPH en temps réel.
- **Exemple :** IBM a démontré (2023) un algorithme quantique pour la dynamique moléculaire, applicable à SPH.

### Optimisation des maillages

- Les algorithmes quantiques pourraient réduire le coût des maillages 3D adaptatifs.

---

## 3. Références bibliographiques

> **Note** : Pour des références qui traitent des ressources utilisées dans ce projet, consultez la section **Références bibliographiques** dans le menu Annexes.
