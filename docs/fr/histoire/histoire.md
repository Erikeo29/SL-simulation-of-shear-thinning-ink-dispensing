**Sommaire :**
1. Pères de la mécanique des fluides
2. Pionniers de la rhéologie
3. Fondateurs de la mécanique statistique
4. Créateurs des méthodes numériques
5. Inventeurs des méthodes modernes
6. Tableau chronologique
7. Diagramme des filiations scientifiques
8. Références bibliographiques

Ce projet de simulation de dispense de fluides repose sur des siècles de découvertes scientifiques. Cette page rend hommage aux savants dont les travaux fondamentaux ont rendu possible la modélisation numérique moderne des écoulements diphasiques.

---

## 1. Pères de la mécanique des fluides

### Claude-Louis Navier (1785-1836)

**Nationalité :** Française | **Domaine :** Ingénierie, Mécanique des fluides

Claude Louis Marie Henri Navier est né à Dijon le 10 février 1785. Orphelin de père à 8 ans, il fut élevé par son grand-oncle Emiland Gauthey, ingénieur en chef des Ponts et Chaussées. Cette influence familiale orienta sa carrière vers l'ingénierie.

**Formation :** École Polytechnique (1802), École des Ponts et Chaussées (1804-1806)

**Contribution majeure :** En **1821-1822**, Navier formula les équations du mouvement des fluides visqueux, généralisant les équations d'Euler pour inclure les effets de frottement interne. Fait remarquable : il obtint les bonnes équations malgré une compréhension incomplète de la physique des contraintes de cisaillement, en modélisant les forces intermoléculaires.

**Travaux connexes :** Théorie des ponts suspendus, élasticité des matériaux, construction de ponts sur la Seine.

**Héritage :** Son nom est inscrit sur la Tour Eiffel. Le problème de l'existence et régularité des solutions des équations de Navier-Stokes reste l'un des 7 problèmes du millénaire (prix : 1 million USD).

---

### Sir George Gabriel Stokes (1819-1903)

**Nationalité :** Irlandaise/Britannique | **Domaine :** Mathématiques, Physique

Né à Skreen en Irlande, Stokes fut l'un des plus grands scientifiques du XIXe siècle. Une anecdote raconte que son intérêt pour la dynamique des fluides naquit lorsqu'il faillit être emporté par une vague en se baignant sur la côte de Sligo.

**Formation :** Pembroke College, Cambridge - Major de promotion ("Senior Wrangler")

**Carrière :** Titulaire de la Chaire Lucasienne de Mathématiques à Cambridge (1849-1903), la même chaire qu'occupèrent Newton et Hawking.

**Contributions majeures :**
- **1845 :** Reformulation rigoureuse des équations de Navier avec une dérivation basée sur les contraintes de cisaillement
- Théorème de Stokes (calcul vectoriel)
- Loi de Stokes (traînée visqueuse sur une sphère)
- Découverte et nomination de la **fluorescence**

**Unité :** Le **stokes** (St), unité de viscosité cinématique, porte son nom.

---

### Osborne Reynolds (1842-1912)

**Nationalité :** Irlandaise/Britannique | **Domaine :** Ingénierie, Hydrodynamique

Né à Belfast, Reynolds hérita de son père, le révérend Osborne Reynolds, un vif intérêt pour la mécanique. En 1868, il devint le premier professeur d'ingénierie à Owens College (aujourd'hui Université de Manchester).

**Expérience emblématique (1883) :** Reynolds injecta un filet d'encre colorée dans un écoulement d'eau en tube de verre. À faible vitesse, le filet restait distinct (laminaire). Au-delà d'une vitesse critique, il se fragmentait (turbulent). Cette expérience définit le passage laminaire-turbulent.

**Le Nombre de Reynolds :**
$$Re = \frac{\rho v L}{\mu}$$

Valeur critique : $Re \approx 2000$ pour les conduites.

**Autres contributions :** Théorie de la lubrification (1886), contraintes de Reynolds en turbulence, pompes turbines.

---

### Moritz Weber (1871-1951)

**Nationalité :** Allemande | **Domaine :** Mécanique navale

Professeur de mécanique navale à la Technische Hochschule de Berlin-Charlottenburg, Weber formalisa en 1919 les principes de similitude mécanique pour les modèles réduits de navires.

**Le Nombre de Weber :**
$$We = \frac{\rho v^2 L}{\sigma}$$

Ce nombre compare les forces d'inertie aux forces de tension superficielle. Crucial pour la formation de gouttes et la dispense de fluides.

---

### Wolfgang von Ohnesorge (1901-1976)

**Nationalité :** Allemande | **Domaine :** Métrologie, Physique des fluides

Descendant du général prussien Blücher (vainqueur de Napoléon à Waterloo), Ohnesorge suivit une carrière atypique : il ne fut jamais universitaire mais directeur du Bureau des Poids et Mesures de Rhénanie du Nord-Westphalie.

**Thèse doctorale (1936) :** Ohnesorge développa un diagramme opérationnel distinguant les régimes de rupture de jets liquides.

**Le Nombre d'Ohnesorge :**
$$Oh = \frac{\mu}{\sqrt{\rho \sigma L}} = \frac{\sqrt{We}}{Re}$$

**Application directe :** En jet d'encre, les fluides sont "éjectables" pour $0.1 < Oh < 1.0$.

---

## 2. Pionniers de la rhéologie

### Isaac Newton (1643-1727)

**Nationalité :** Anglaise | **Domaine :** Physique, Mathématiques

Le génie universel de la science. Outre la gravitation et le calcul infinitésimal, Newton établit en 1687 la loi fondamentale de la viscosité dans ses *Principia Mathematica*.

**Loi de Newton pour les fluides :**
$$\tau = \mu \dot{\gamma}$$

Un fluide dont la viscosité $\mu$ est constante est dit **newtonien**. L'eau, l'air et les huiles minérales sont newtoniens.

---

### Wilhelm Ostwald (1853-1932) & Arnulph de Waele

**Nationalité :** Ostwald : Allemande (né à Riga, alors Empire russe) | **Domaine :** Chimie physique, Rhéologie

Wilhelm Ostwald reçut le **Prix Nobel de Chimie en 1909** pour ses travaux sur la catalyse et les équilibres chimiques.

**Loi de puissance (Ostwald-de Waele) :**
$$\eta(\dot{\gamma}) = K \dot{\gamma}^{n-1}$$

Cette loi décrit les fluides **rhéofluidifiants** ($n < 1$) et **rhéoépaississants** ($n > 1$).

---

### Pierre J. Carreau (né en 1939)

**Nationalité :** Canadienne | **Domaine :** Génie chimique, Rhéologie des polymères

Professeur émérite à l'École Polytechnique de Montréal, Pierre Carreau est le fondateur du CRASP (devenu CREPEC en 2002). Il obtint son doctorat à l'Université du Wisconsin en 1968.

**Le Modèle de Carreau (1972) :**
$$\eta(\dot{\gamma}) = \eta_\infty + (\eta_0 - \eta_\infty)[1 + (\lambda\dot{\gamma})^2]^{(n-1)/2}$$

Ce modèle évite la singularité de la loi de puissance à cisaillement nul grâce aux plateaux $\eta_0$ et $\eta_\infty$.

**Distinctions :** Fellow de la Société Royale du Canada (2006), Docteur *honoris causa* de l'Université Joseph Fourier de Grenoble (1989).

---

### Winslow H. Herschel & Ronald Bulkley

**Époque :** Années 1920 | **Domaine :** Rhéologie

En 1926, Herschel et Bulkley étudièrent la consistance de solutions de caoutchouc dans le benzène et proposèrent un modèle pour les **fluides à seuil** :

**Modèle de Herschel-Bulkley :**
- Si $|\tau| \leq \tau_0$ : pas d'écoulement (solide)
- Si $|\tau| > \tau_0$ : $\tau = \tau_0 + K\dot{\gamma}^n$

Ce modèle combine une contrainte seuil (*yield stress*) avec un comportement non-linéaire post-écoulement. Il s'applique aux encres à forte charge solide, pâtes, boues de forage, etc.

---

## 3. Fondateurs de la mécanique statistique

### Ludwig Boltzmann (1844-1906)

**Nationalité :** Autrichienne | **Domaine :** Physique théorique

Né à Vienne, Boltzmann est le père de la mécanique statistique. Son travail révolutionnaire établit que les lois de la thermodynamique sont de nature **probabiliste** : l'entropie mesure le nombre d'états microscopiques compatibles avec un état macroscopique.

**Équation de Boltzmann (1872) :**
$$\frac{\partial f}{\partial t} + \mathbf{v} \cdot \nabla f = \Omega(f)$$

Cette équation décrit l'évolution de la fonction de distribution des particules et constitue le fondement de la méthode LBM.

**Formule de l'entropie :** $S = k \log W$ (gravée sur sa tombe à Vienne)

**Tragédie :** Boltzmann souffrit de dépression et se suicida en 1906, peu avant que ses théories ne soient pleinement acceptées. Einstein et Planck confirmèrent ses idées quelques années plus tard.

---

### James Clerk Maxwell (1831-1879)

**Nationalité :** Écossaise | **Domaine :** Physique théorique

Maxwell est considéré par Einstein comme le physicien le plus influent du XIXe siècle. Outre l'unification de l'électricité, du magnétisme et de l'optique, il contribua fondamentalement à la théorie cinétique des gaz.

**Distribution de Maxwell-Boltzmann (1860) :**

Maxwell fut le premier à concevoir que les molécules d'un gaz n'ont pas toutes la même vitesse mais suivent une distribution statistique. Cette idée révolutionnaire introduisit le concept de **probabilité en physique**.

**Directeur du Laboratoire Cavendish** à Cambridge (1871-1879).

---

### Prabhu Lal Bhatnagar (1912-1976), Eugene P. Gross (1926-1991) & Max Krook (1913-1985)

**Nationalités :** Indienne, Américaine, Sud-Africaine/Américaine | **Domaine :** Physique théorique

**L'opérateur BGK (1954) :**
$$\Omega_i = -\frac{1}{\tau}(f_i - f_i^{eq})$$

Cette simplification géniale de l'opérateur de collision de Boltzmann remplace l'intégrale complexe par une relaxation linéaire vers l'équilibre. Elle est au cœur de toutes les implémentations LBM modernes.

Le temps de relaxation $\tau$ est directement lié à la viscosité cinématique : $\nu = c_s^2(\tau - 1/2)\Delta t$.

---

## 4. Créateurs des méthodes numériques

### Boris Galerkin (1871-1945)

**Nationalité :** Russe/Soviétique | **Domaine :** Mécanique, Mathématiques appliquées

Né dans une famille pauvre en Biélorussie actuelle, Galerkin étudia à l'Institut Technologique de Saint-Pétersbourg tout en travaillant pour subvenir à ses besoins.

**Fait remarquable :** Révolutionnaire actif, il fut emprisonné en 1906 à la prison de Kresty où il rédigea son premier article scientifique (130 pages) !

**La Méthode de Galerkin (1915) :**

Cette méthode transforme une équation différentielle en un système algébrique en projetant sur un espace de fonctions test. Elle est la base théorique de la **Méthode des Éléments Finis (FEM)**.

**Héritage :** L'URSS créa des prix et bourses en son nom pour récompenser les travaux en élasticité et mécanique des structures.

---

### John W. Cahn (1928-2016) & John E. Hilliard (1926-1987)

**Nationalité :** Américaine | **Domaine :** Science des matériaux

Né à Cologne (Allemagne) dans une famille juive qui fuit le nazisme, John Cahn obtint son doctorat à Berkeley (1953) et travailla chez General Electric puis au MIT et au NIST.

**L'Équation de Cahn-Hilliard (1958) :**
$$\frac{\partial \phi}{\partial t} = \gamma \nabla^2 \left( \frac{\delta \mathcal{F}}{\delta \phi} \right)$$

Cette équation décrit la **décomposition spinodale** : comment deux composants d'un alliage se séparent spontanément en phases distinctes.

**Impact :** L'équation est au cœur des méthodes **Phase-Field** utilisées pour le suivi d'interface dans ce projet.

**Distinctions :** Médaille Nationale de la Science (1998), Prix Kyoto (2011).

---

### Vitaly Ginzburg (1916-2009) & Lev Landau (1908-1968)

**Nationalité :** Soviétique/Russe | **Domaine :** Physique théorique

**Lev Landau** est considéré comme l'un des derniers physiciens universels du XXe siècle, ayant contribué à presque tous les domaines de la physique théorique. Il reçut le **Prix Nobel de Physique en 1962** pour sa théorie de la superfluidité.

**Vitaly Ginzburg** reçut le **Prix Nobel de Physique en 2003** pour ses contributions à la supraconductivité.

**La Théorie de Ginzburg-Landau (1950) :**

Cette théorie phénoménologique introduit le concept de **paramètre d'ordre** $\phi$ et d'**énergie libre** :
$$\mathcal{F}[\phi] = \int \left[ \frac{\varepsilon}{2}|\nabla\phi|^2 + \frac{1}{4\varepsilon}(1-\phi^2)^2 \right] d\Omega$$

Dans ce projet, cette énergie libre gouverne l'évolution de l'interface encre/air dans la méthode Phase-Field.

---

## 5. Inventeurs des méthodes modernes

### Cyril W. Hirt & Billy D. Nichols

**Nationalité :** Américaine | **Époque :** 1981 | **Institution :** Los Alamos National Laboratory

**La Méthode VOF (Volume of Fluid) :**

En 1981, Hirt et Nichols publièrent l'article fondateur de la méthode VOF : *"Volume of Fluid (VOF) Method for the Dynamics of Free Boundaries"* dans le Journal of Computational Physics.

L'idée clé : suivre l'interface via une fraction volumique $\alpha$ transportée par l'écoulement :
$$\frac{\partial \alpha}{\partial t} + \nabla \cdot (\alpha \mathbf{v}) = 0$$

Cette méthode est aujourd'hui le **standard industriel** pour les écoulements diphasiques (OpenFOAM, Fluent, etc.).

---

### Xiaowen Shan (né ~1960) & Hudong Chen

**Nationalité :** Chinoise/Américaine | **Institution :** Los Alamos / Dartmouth College

**Le Modèle Shan-Chen (1993) :**

En 1993, Shan et Chen proposèrent un modèle de Boltzmann sur réseau pour les écoulements multiphasiques basé sur un **pseudopotentiel** d'interaction :
$$\mathbf{F}_{int} = -G\psi(\mathbf{x}) \sum_i w_i \psi(\mathbf{x} + \mathbf{c}_i)\mathbf{c}_i$$

Ce modèle génère automatiquement la séparation de phases et la tension superficielle sans suivi explicite d'interface.

**Xiaowen Shan** fut élu Fellow de l'American Physical Society en 2009. Il a travaillé chez Microsoft, Exa Corp., et COMAC (constructeur aéronautique chinois).

---

### Joseph J. Monaghan (né ~1940)

**Nationalité :** Australienne | **Institution :** Monash University

**La Méthode SPH (1977) :**

En 1977, Monaghan et R.A. Gingold (simultanément avec L.B. Lucy) inventèrent la méthode **Smoothed Particle Hydrodynamics (SPH)** pour simuler la formation des étoiles.

L'idée révolutionnaire : représenter le fluide par des particules mobiles, sans maillage :
$$A(\mathbf{r}) = \sum_b m_b \frac{A_b}{\rho_b} W(|\mathbf{r} - \mathbf{r}_b|, h)$$

**Applications actuelles :** Écoulements à surface libre, rupture de jets, éclaboussures, impacts violents.

Monaghan a publié plus de 150 articles et deux revues majeures dans *Annual Review of Astronomy and Astrophysics* (1992) et *Annual Review of Fluid Mechanics* (2012).

---

## 6. Tableau chronologique

| Période | Scientifique | Contribution | Application dans ce projet |
|---------|--------------|--------------|---------------------------|
| 1687 | Newton | Loi de viscosité | Fluides newtoniens |
| 1821-1845 | Navier, Stokes | Équations N-S | Toutes les méthodes |
| 1860-1872 | Maxwell, Boltzmann | Théorie cinétique | LBM |
| 1883 | Reynolds | Nombre de Reynolds | Analyse d'écoulement |
| 1915 | Galerkin | Méthode de Galerkin | FEM |
| 1919-1936 | Weber, Ohnesorge | Nombres We, Oh | Critères d'éjectabilité |
| 1926 | Herschel-Bulkley | Fluides à seuil | Encres à charge |
| 1950 | Ginzburg-Landau | Énergie libre | Phase-Field |
| 1954 | Bhatnagar-Gross-Krook | Opérateur BGK | LBM |
| 1958 | Cahn-Hilliard | Séparation de phases | Phase-Field, FEM |
| 1972 | Carreau | Modèle rhéologique | Encres rhéofluidifiantes |
| 1977 | Monaghan, Gingold, Lucy | SPH | Méthode SPH |
| 1981 | Hirt, Nichols | VOF | OpenFOAM |
| 1993 | Shan, Chen | Modèle multiphasique | LBM diphasique |

---

## 7. Diagramme des filiations scientifiques

```
NEWTON (1687)
    │
    ├─────────────────────────────────────────┐
    │                                         │
EULER (1755)                           OSTWALD (1890s)
    │                                         │
    ├─────────────┐                     CARREAU (1972)
    │             │                     HERSCHEL-BULKLEY
NAVIER (1821)   STOKES (1845)                 │
    │             │                           │
    └──────┬──────┘                   MODÈLES RHÉOLOGIQUES
           │                                  │
    NAVIER-STOKES                             │
           │                                  │
    ┌──────┼──────────────────────────────────┼─────────────┐
    │      │                                  │             │
REYNOLDS  GALERKIN          MAXWELL-BOLTZMANN        WEBER-OHNESORGE
(1883)    (1915)                  (1860-1872)             (1919-1936)
    │         │                        │                       │
    │    ÉLÉMENTS FINIS           BOLTZMANN                    │
    │         │                   (1872)                       │
    │    CAHN-HILLIARD                │                        │
    │    (1958)                  BGK (1954)                    │
    │         │                        │                       │
    │    GINZBURG-LANDAU         SHAN-CHEN              CRITÈRES
    │    (1950)                  (1993)                 DISPENSE
    │         │                        │                       │
    └─────────┴────────────────────────┴───────────────────────┘
              │                        │
         PHASE-FIELD                  LBM
              │                        │
              │                        │
    MONAGHAN (1977)          HIRT-NICHOLS (1981)
              │                        │
             SPH                      VOF
              │                        │
              └────────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
         CE PROJET              APPLICATIONS
    Dispense d'encre          INDUSTRIELLES
   rhéofluidifiante
```

---

## 8. Références bibliographiques

> **Note** : Pour la liste complète des références techniques, consultez la section **Références bibliographiques** dans le menu Annexes.

