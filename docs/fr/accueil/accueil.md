&nbsp;

**À propos de ce projet** — *Ce projet de modélisation physique a été conçu intégralement par l'auteur, depuis une page blanche jusqu'à sa mise en ligne sur ce site. Le contenu a été élaboré sur la base de ses connaissances complétées par une veille documentaire sur les concepts physiques et les outils numériques.*

*L'objectif est de permettre la réalisation de modélisations multiphysiques avancées au moyen d'outils open-source gratuits.*

*Pour les sujets - nombreux - dépassant son domaine de compétence initial, des outils d'intelligence artificielle et d'automatisation (LLM, agents de recherche) ont été utilisés pour réaliser des recherches internet approfondies (paramétrage des modèles physiques, utilisation des bibliothèques numériques), la rédaction et la restructuration des codes (Python, C++), l'interface de cette application, la traduction automatique français / anglais.*

*Tous les résultats présentés dans ce projet sont issus de modèles physiques analytiques et déterministes résolus par des solveurs numériques reconnus et validés.*

*Les données utilisées pour alimenter le projet (équations, constantes et données physicochimiques...) sont disponibles en accès libres sur internet. Les codes sont originaux et s'appuient exclusivement sur des bibliothèques open-source. De fait, ce travail est mis à disposition sous licence MIT pour être utilisé, reproduit et amélioré à des fins d'apprentissage ou d'exploitation des modèles physiques et numériques présentés.*

&nbsp;

---

**Sommaire :**
1. Objectif du projet
2. Application cible
3. Navigation
4. Note méthodologique
5. Aperçu des résultats des 3 modèles

---

## 1. Objectif du projet

Le but de cette application est de modéliser, visualiser et comparer les résultats de **trois méthodes numériques** pour la simulation de la dispense de fluides rhéofluidifiants dans des micro-via. L'application permet d'explorer les résultats de simulations diphasiques réalisées avec différentes approches :

- **VOF (Volume of Fluid)** : Méthode eulérienne (OpenFOAM)
- **LBM (Lattice Boltzmann)** : Approche mésoscopique optimisée GPU (Palabos)
- **SPH (Smoothed Particle Hydrodynamics)** : Méthode lagrangienne sans maillage (PySPH)
- La méthode **FEM (Méthode des éléments finis)** sous Python avec environnements FEniCSx et Firedrake est en cours de développement et n'est pas présentée dans cette version.
---

## 2. Application cible

Les simulations modélisent la **dispense d'une encre rhéofluidifiante** dans des micro-via.

**Paramètres clés étudiés :**
- Géométrie : diamètre micro-via, diamètre buse.
- Position de la buse : décalage en X et Y (décalage vertical et horizontal par rapport au via).
- Rhéologie : viscosité (modèle de Carreau).
- Mouillage : angles de contact sur le fond du micro-via, sur les parois verticales du puit, sur la surface horizontale du substrat.

---

## 3. Navigation

La navigation dans les différentes pages de cette application est structurée avec les outils suivants :

1.  **Menu latéral (à gauche)** : outil de navigation entre les différentes sections du projet :
    *   **Introduction** : Contexte scientifique, propriétés des fluides rhéofluidifiants et présentation du système physique étudié.
    *   **Comparaison des modèles** : analyses synthétiques pour comparaison des différentes approches.
    *   **Résultats de modélisation** : Chaque page de modèle (VOF, LBM, SPH) contient des onglets pour explorer la physique sous-jacente, le code source utilisé et les **résultats des simulations** (animations GIF et images PNG).
    *   **Annexes** : Conclusion, perspectives, lexique technique, équations clés et bibliographie thématique.


2.  **Boutons de navigation flottants (à droite)** : Deux flèches permettent de se déplacer rapidement en haut ou en bas des pages.

3.  **Assistant IA (dans le menu latéral)** : Un pop-up s'ouvre pour répondre à vos questions sur la physique, les méthodes numériques ou le projet en général.

---

## 4. Note méthodologique

Les animations et images présentées dans cette application proviennent de simulations **pré-calculées**. Le projet a été réalisé sur un PC portable standard: environnement Linux via WSL2, processeur 1.5-3.5 GHz, 6 CPU / 12 threads, 32 Go de RAM, 8 Go de GPU (quand utilisable : LBM, SPH DualSPHysics). Les modélisations en 2D ont été réalisées avec différentes combinaisons de facteurs (géométrie, viscosité, angles de contact, temps de dispense...) sous forme d'étude paramétrique. Les résultats ont ensuite été exportés sous format GIF (animations) et PNG (images état final) pour alimenter cette application.

Cette application est donc un **visualiseur de résultats**, non un simulateur en temps réel. En effet, la réalisation de ces simulations nécessite des configurations spécifiques d'environnements et de packages Python ou OpenFOAM ; le temps de modélisation est également conséquent, de 10 minutes à 2 heures par simulation unitaire suivant le type de modèle numérique et de paramètres étudiés. Les codes sont fournis dans les onglets "Code" des 3 modèles afin d'être copiés et pouvoir reproduire ces modélisations sur d'autres machines.
