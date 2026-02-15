# Shear-Thinning Ink Dispensing Simulation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dispense-encre.streamlit.app/)

Streamlit application for visualization and comparison of numerical simulations of shear-thinning fluid dispensing into micro-wells.

## Compared Models

| Model | Method | Implementation | Physical Focus |
|-------|--------|----------------|----------------|
| **FEM** | Finite Elements / Phase-Field | Python (FEniCS) | Interface thermodynamics, capillarity |
| **VOF** | Volume of Fluid | C++ (OpenFOAM) | Industrial standard, mass conservation |
| **LBM** | Lattice Boltzmann | C++ (Palabos) | GPU performance, complex geometries |
| **SPH** | Smoothed Particle Hydrodynamics | Python (PySPH) | Free surfaces, large deformations |

## Features

- **Home page**: Overview of 4 models with animated examples
- **Scientific documentation**: LaTeX equations, dimensionless numbers, references
- **Detailed comparison**: Hardware tables, accuracy, computational cost
- **Interactive viewer**: Parameter selection for FEM model
- **Smooth navigation**: Back-to-top/bottom buttons, visible tabs
- **Bilingual support**: Full FR/EN interface

## Project Structure

```
app.py              # Streamlit application (~660 lines)
assets/             # Visual resources (GIFs, PNGs)
  fem/, vof/, lbm/, sph/
data/               # CSV mappings parameters → files
docs/               # Markdown documentation
  fr/, en/          # Bilingual content
  physics/          # Theory per model
  comparaison/      # Comparison tables
  biblio/           # Centralized bibliography
```

## Installation

```bash
git clone https://github.com/Erikeo29/dispense-encre.git
cd dispense-encre
pip install -r requirements.txt
streamlit run app.py
```

## Technical Documentation

Documentation includes:
- Dimensionless numbers (Re, We, Oh, De, Ca, Bo)
- Navier-Stokes equations and rheological models (Carreau, Herschel-Bulkley)
- Detailed numerical methods (VOF-PLIC, LBM-BGK, SPH-CSF, FEM-SUPG)
- Experimental validation results
- Hardware recommendations and computational costs

## Version

**Version 3.5.0 (January 2026)**
- Full bilingual FR/EN support
- Centralized bibliography with verified DOIs
- Up/down navigation buttons
- Compact sidebar (optimized spacing)
- Improved labels for GIF/PNG viewers
- Bordered containers for parameters

**Version 3.4.0 (December 2025)**
- Home page with 4 models overview
- Appendix pages: Key Equations, Glossary, History
- Improved interface (visible tabs)
- LaTeX fixes for KaTeX compatibility

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
