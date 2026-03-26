**Sommaire :**
1. Méthode des éléments finis (FEM) / Phase-Field
2. Volume of Fluid (VOF)
3. Lattice Boltzmann Method (LBM)
4. Smoothed Particle Hydrodynamics (SPH)
5. Rhéologie et mouillage
6. Ouvrages généraux
7. PINN et intelligence artificielle
8. Ressources en ligne

Cette page regroupe des références qui décrivent les principes utilisés dans ce projet. **Tous les liens pointent vers des ressources en accès libre vérifiées.**

---

## 1. Méthode des éléments finis (FEM) / Phase-Field

1. **Yue, P., Feng, J. J., Liu, C., & Shen, J.** (2004). *A diffuse-interface method for simulating two-phase flows of complex fluids*. Journal of Fluid Mechanics, 515, 293-317. [PDF gratuit (ResearchGate)](https://www.researchgate.net/publication/231965731_A_diffuse-interface_method_of_simulating_two-phase_flows_of_complex_fluids)
   - Extension du modèle de champ de phase aux fluides complexes.

2. **Logg, A., Mardal, K.-A., & Wells, G.** (Eds.). (2012). *Automated Solution of Differential Equations by the Finite Element Method: The FEniCS Book*. Springer. [PDF gratuit (FEniCS Project)](http://launchpad.net/fenics-book/trunk/final/+download/fenics-book-2011-10-27-final.pdf)
   - Documentation complète du framework FEniCS.

---

## 2. Volume of Fluid (VOF)

3. **Hirt, C. W., & Nichols, B. D.** (1981). *Volume of fluid (VOF) method for the dynamics of free boundaries*. Journal of Computational Physics, 39(1), 201-225. [PDF gratuit (SJTU)](https://dcwan.sjtu.edu.cn/PlugIns/ckfinder/userfiles/files/Hirt%20%E5%92%8C%20Nichols%20-%201981%20-%20Volume%20of%20fluid%20(VOF)%20method%20for%20the%20dynamics%20of%20f(1).pdf)
   - Article fondateur de la méthode VOF.

4. **Brackbill, J. U., Kothe, D. B., & Zemach, C.** (1992). *A continuum method for modeling surface tension*. Journal of Computational Physics, 100(2), 335-354. [PDF gratuit (Sorbonne/LJLL)](https://www.ljll.fr/~frey/papers/Navier-Stokes/Brackbill%20J.U.,%20A%20continuum%20method%20for%20modeling%20surface%20tension.pdf)
   - Modèle CSF (Continuum Surface Force) pour la tension de surface.

5. **Popinet, S.** (2009). *An accurate adaptive solver for surface-tension-driven interfacial flows*. Journal of Computational Physics, 228(16), 5838-5866. [PDF gratuit (HAL Science)](https://hal.science/hal-01445445)
   - Solveur adaptatif de haute précision pour les écoulements interfaciaux (Basilisk/Gerris).

6. **Jasak, H.** (1996). *Error Analysis and Estimation for the Finite Volume Method with Applications to Fluid Flows*. PhD Thesis, Imperial College London. [PDF gratuit (Imperial College)](https://spiral.imperial.ac.uk/handle/10044/1/8335)
   - Fondements théoriques de la méthode des volumes finis dans OpenFOAM.

---

## 3. Lattice Boltzmann Method (LBM)

7. **Chen, S., & Doolen, G. D.** (1998). *Lattice Boltzmann method for fluid flows*. Annual Review of Fluid Mechanics, 30(1), 329-364. [PDF gratuit (UC eScholarship)](https://escholarship.org/content/qt8vf0g3zk/qt8vf0g3zk_noSplash_d3843a251a7f7e13bb8782f13ecc40a0.pdf)
   - Revue complète de la méthode LBM.

8. **Shan, X., & Chen, H.** (1993). *Lattice Boltzmann model for simulating flows with multiple phases and components*. Physical Review E, 47(3), 1815. [ResearchGate](https://www.researchgate.net/publication/13329506_Lattice_Boltzmann_Model_for_Simulating_Flows_with_Multiple_Phases_and_Components)
   - Modèle Shan-Chen pour les écoulements multiphasiques (article milestone PRE).

9. **Fakhari, A., & Rahimian, M. H.** (2010). *Phase-field modeling by the method of lattice Boltzmann equations*. Physical Review E, 81(3), 036707. [ResearchGate](https://www.researchgate.net/publication/43020969_Phase-field_modeling_by_the_method_of_lattice_Boltzmann_equations)
   - Couplage LBM et modèle de champ de phase.

---

## 4. Smoothed Particle Hydrodynamics (SPH)

10. **Monaghan, J. J.** (2005). *Smoothed particle hydrodynamics*. Reports on Progress in Physics, 68(8), 1703-1759. [PDF gratuit (U Toronto)](https://planets.utsc.utoronto.ca/~pawel/PHYD57/monaghan-sph2005.pdf)
    - Revue fondamentale de la méthode SPH par son créateur.

---

## 5. Rhéologie et mouillage

11. **de Gennes, P. G.** (1985). *Wetting: statics and dynamics*. Reviews of Modern Physics, 57(3), 827-863. [PDF gratuit (UC Irvine)](https://www.physics.uci.edu/~taborek/publications/other/deGennesWettingReview.pdf)
    - Article fondateur sur la physique du mouillage (Prix Nobel 1991).

---

## 6. Ouvrages généraux

12. **Derby, B.** (2010). *Inkjet printing of functional and structural materials*. Annual Review of Materials Research, 40, 395-414. [PDF gratuit (U Manchester)](https://pure.manchester.ac.uk/ws/files/174918681/DERBYwithfigures_2017_02_22_19_00_59_UTC_.pdf)
    - Introduction aux applications industrielles de l'impression jet d'encre.

---

## 7. PINN et intelligence artificielle

13. **Raissi, M., Perdikaris, P., & Karniadakis, G. E.** (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. Journal of Computational Physics, 378, 686-707. [PDF gratuit (arXiv)](https://arxiv.org/pdf/1711.10561)
    - Article fondateur des PINN : résolution d'EDP par réseaux de neurones contraints par la physique.

14. **Raissi, M., Yazdani, A., & Karniadakis, G. E.** (2020). *Hidden fluid mechanics: Learning velocity and pressure fields from flow visualizations*. Science, 367(6481), 1026-1030. [PDF gratuit (arXiv)](https://arxiv.org/pdf/1808.04327)
    - Application des PINN à la mécanique des fluides : reconstruction de champs de vitesse et pression à partir de visualisations d'écoulements.

15. **Cai, S., Mao, Z., Wang, Z., Yin, M., & Karniadakis, G. E.** (2021). *Physics-informed neural networks (PINNs) for fluid mechanics: A review*. Acta Mechanica Sinica, 37, 1727-1738. [PDF gratuit (arXiv)](https://arxiv.org/pdf/2105.09506)
    - Revue des applications des PINN en mécanique des fluides : écoulements 3D, supersoniques, biomédicaux.

---

## 8. Ressources en ligne

- [OpenFOAM Documentation](https://openfoam.org) - Solveurs VOF (interFoam, isoAdvector)
- [FEniCS Project](https://fenicsproject.org) - Éléments finis Python/C++
- [Palabos](https://palabos.unige.ch) - LBM open-source (C++)
- [PySPH Documentation](https://pysph.readthedocs.io) - SPH en Python
- [CFD Online Forums](https://www.cfd-online.com/Forums/) - Communauté CFD
- [Basilisk](http://basilisk.fr/) - VOF adaptatif (Popinet)
