import streamlit as st
import base64
import os
import pandas as pd
from groq import Groq

# --- Configuration de la page ---
st.set_page_config(page_title="Simulation Dispense", layout="wide", initial_sidebar_state="expanded")


# --- Dictionnaire de Traduction UI ---
TRANSLATIONS = {
    "fr": {
        "title": "Simulation de Dispense d'Encre Rhéofluidifiante",
        "hero_subtitle": "Comparaison VOF, LBM, SPH - rhéologie et dispense en micro-puits",
        "sidebar_title": "Modélisation de la dispense d'encre",
        "nav_header": "Navigation",
        "gen_header": "Général",
        "models_header": "Résultats de modélisation",
        "annex_header": "Annexes",
        "gen_pages": ["Accueil", "Introduction", "Comparaison des modèles"],
        "model_pages": ["1. VOF (OpenFOAM)", "2. LBM (Palabos)", "3. SPH (PySPH)"],
        "annex_pages": ["Conclusion et perspectives", "Lexique", "Équations clés", "Un peu d'histoire", "Références bibliographiques"],
        "tabs_dual": ["Physique", "Code", "▸ Résultats de modélisation (GIF)", "▸ Résultats de modélisation (PNG)"],
        "tabs_other": ["Physique", "Code", "▸ Résultats de modélisation"],
        "overview_title": "5. Aperçu des résultats des 3 modèles",
        "overview_subtitle": "voir les pages 'Résultats de modélisation' pour l'ensemble des modélisations",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_launch": "LANCER LES SIMULATIONS",
        "btn_reset": "RÉINITIALISER",
        "btn_show": "AFFICHER LES IMAGES",
        "combo_unavailable": "Combinaison non disponible",
        "image_unavailable": "Image non disponible",
        "gif_viewer": "Visualisation dynamique (GIF)",
        "png_viewer": "Visualisation état final (PNG)",
        "lbl_avail_sims": "📋 Simulations disponibles",
        # Titres Modèles
        "title_model_1": "Modèle 1 : Méthode Volume of Fluid (OpenFOAM)",
        "title_model_2": "Modèle 2 : Méthode Lattice Boltzmann (Palabos C++)",
        "title_model_3": "Modèle 3 : Méthode Smoothed Particle Hydrodynamics (PySPH)",
        # Labels GIF
        "lbl_well": "Ø Puit (µm)",
        "lbl_nozzle": "Ø Buse (µm)",
        "lbl_shift_x": "Décalage X (µm)",
        "lbl_viscosity": "η₀ (Pa·s)",
        "lbl_ca_wall": "θ paroi (°)",
        "lbl_ca_gold": "θ substrat (°)",
        # Labels PNG
        "lbl_time": "Temps (ms)",
        "lbl_shift_z": "Décalage Z (µm)",
        "lbl_ratio": "Ratio buse/puit",
        # Labels LBM avancés
        "lbl_adv_params": "Paramètres avancés",
        "lbl_ca_wall_l": "CA Mur Gauche (°)",
        "lbl_ca_wall_r": "CA Mur Droit (°)",
        "lbl_ca_plateau": "CA Plateau (°)",
        "lbl_gap": "Gap Buse (µm)",
        "lbl_ratio_drop": "Ratio goutte/puit",
        "version_info": """**Version 3.5.0** - Jan 2026

**Nouveautés :**
- Support bilingue FR/EN
- Références bibliographiques
- Assistant IA
- Navigation améliorée""",
        "caption_fem": "Méthode des éléments finis - Python/FEniCS",
        "caption_vof": "Volume of Fluid - C++/OpenFOAM",
        "caption_lbm": "Lattice Boltzmann - C++/Palabos",
        "caption_sph": "Smoothed Particle Hydrodynamics - Python/PySPH",
        # Chatbot
        "chat_title": "Assistant IA",
        "chat_welcome": "Bonjour ! Je suis votre assistant pour comprendre les simulations de dispense d'encre rhéofluidifiante. Posez-moi vos questions sur FEM, VOF, LBM, SPH, ou la physique des fluides !",
        "chat_placeholder": "Posez votre question...",
        "chat_error": "Erreur de connexion à l'API. Vérifiez votre clé API.",
        "chat_close": "Fermer",
        "chat_clear": "Effacer",
        "chat_api_missing": "⚠️ Clé API manquante. Configurez GROQ_API_KEY.",
        "chat_disclaimer": "⚠️ Réponse générée par IA - peut contenir des erreurs ou omissions. Vérifiez toujours les informations auprès des sources scientifiques reconnues.",
        "chat_toggle": "Assistant IA",
        # Comparison page
        "lbl_empty_mesh": "Maillage vide",
        "lbl_with_droplet": "Avec goutte (état final)",
        # SPH
        "sph_example_title": "Résultats de Simulation SPH",
        "sph_preliminary": "🔴 **Résultats non concluants à ce jour** - La méthode SPH s'est avérée inadaptée pour ce problème.",
        "sph_failure_title": "Pourquoi SPH ne fonctionne pas ici ?",
        "sph_failure_details": """
La méthode SPH a été testée de manière exhaustive (~115 versions de codes différentes) avec deux solveurs (**PySPH** et **SPlisHSPlasH**) et s'est avérée **inadaptée** pour la simulation de dépôt d'encre rhéofluidifiante en micro-cavité. Les principales raisons sont :

**1. Tension de surface mal prise en compte**
- Le modèle CSF (*Continuum Surface Force*) utilisé dans PySPH crée des **artefacts de splitting** : la goutte se scinde artificiellement au milieu pendant l'étalement, ce qui est non physique.
- La contrainte CFL (Courant-Friedrichs-Lewy) capillaire impose un pas de temps extrêmement petit : $\\Delta t \\propto \\sqrt{\\rho h^3 / \\sigma} \\approx 10^{-8}$ s à la résolution de 10 µm, rendant les calculs prohibitifs (~2h pour 30 ms de temps physique).

**2. Résolution insuffisante**
- Avec 700 à 1200 particules (résolution typique de 10-20 µm), les dynamiques fines d'étalement et de mouillage ne sont pas capturées correctement.
- Augmenter la résolution aggrave encore le problème du pas de temps.

**3. Modèles d'adhésion limités**
- Les angles de contact sont imposés via des forces d'adhésion explicites, une approche moins robuste que les conditions aux limites de mouillabilité utilisées en VOF ou Phase Field.
- La calibration du paramètre d'adhésion α reste empirique et sensible à la résolution.

**4. Solveur alternatif (SPlisHSPlasH)**
- Le solveur SPlisHSPlasH (DFSPH - Divergence-Free SPH + Akinci 2013) est beaucoup plus rapide (~1000× avec la GPU) mais ne fonctionne qu'à **échelle macroscopique** (échelle ×1000).
- Pas de contrôle des angles de contact par paroi.
- Résultats visuellement "spectaculaires" (éclaboussures et vagues réalistes : voir dernière image ci-dessous) mais **physiquement faux** pour le dépôt d'une encre visqueuse à l'échelle du µm.

**Conclusion** : Pour ce type de problème (goutte µm, tension de surface élevée, angles de contact variables), les méthodes **VOF** (OpenFOAM) et **Phase Field** (FEM) sont plus adaptées.
""",
        "sph_nok_caption_1": "PySPH - Splitting de la goutte (artefact CSF)",
        "sph_nok_caption_2": "PySPH - Splitting de la goutte (artefact CSF)",
        "sph_nok_caption_3": "PySPH - Angle contact 60°: OK. Particules s'échappant de la cavité",
        "sph_geyser_caption": "SPlisHSPlasH (échelle ×1000, non réaliste pour une encre visqueuse ! )",
        # Errors
        "mapping_missing": "Données de mapping manquantes.",
        "data_not_found": "Données non trouvées",
    },
    "en": {
        "title": "Shear-Thinning Ink Dispensing Simulation",
        "hero_subtitle": "VOF, LBM, SPH comparison - rheology and micro-well dispensing",
        "sidebar_title": "Ink Dispensing Modeling",
        "nav_header": "Navigation",
        "gen_header": "General",
        "models_header": "Modeling Results",
        "annex_header": "Appendices",
        "gen_pages": ["Home", "Introduction", "Model Comparison"],
        "model_pages": ["1. VOF (OpenFOAM)", "2. LBM (Palabos)", "3. SPH (PySPH)"],
        "annex_pages": ["Conclusion and Perspectives", "Glossary", "Key Equations", "A Bit of History", "Bibliographical References"],
        "tabs_dual": ["Physics", "Code", "▸ Modeling Results (GIF)", "▸ Modeling Results (PNG)"],
        "tabs_other": ["Physics", "Code", "▸ Modeling Results"],
        "overview_title": "5. Overview of the 3 Simulation Models",
        "overview_subtitle": "see the 'Modeling Results' pages for all simulations",
        "sim_1": "Simulation 1",
        "sim_2": "Simulation 2",
        "btn_launch": "LAUNCH SIMULATIONS",
        "btn_reset": "RESET",
        "btn_show": "SHOW IMAGES",
        "combo_unavailable": "Combination not available",
        "image_unavailable": "Image not available",
        "gif_viewer": "Dynamic Visualization (GIF)",
        "png_viewer": "Final State Visualization (PNG)",
        "lbl_avail_sims": "📋 Available Simulations",
        # Model Titles
        "title_model_1": "Model 1 : Volume of Fluid Method (OpenFOAM)",
        "title_model_2": "Model 2 : Lattice Boltzmann Method (Palabos C++)",
        "title_model_3": "Model 3 : Smoothed Particle Hydrodynamics (PySPH)",
        # Labels GIF
        "lbl_well": "Ø Well (µm)",
        "lbl_nozzle": "Ø Nozzle (µm)",
        "lbl_shift_x": "Offset X (µm)",
        "lbl_viscosity": "η₀ (Pa·s)",
        "lbl_ca_wall": "θ wall (°)",
        "lbl_ca_gold": "θ substrate (°)",
        # Labels PNG
        "lbl_time": "Time (ms)",
        "lbl_shift_z": "Offset Z (µm)",
        "lbl_ratio": "Nozzle/well ratio",
        # Labels LBM advanced
        "lbl_adv_params": "Advanced Parameters",
        "lbl_ca_wall_l": "CA Wall Left (°)",
        "lbl_ca_wall_r": "CA Wall Right (°)",
        "lbl_ca_plateau": "CA Plateau (°)",
        "lbl_gap": "Nozzle Gap (µm)",
        "lbl_ratio_drop": "Drop/Well Ratio",
        "version_info": """**Version 3.5.0** - Jan 2026

**New Features:**
- Bilingual support FR/EN
- Bibliographical References
- AI Assistant
- Improved navigation""",
        "caption_fem": "Finite Element Method - Python/FEniCS",
        "caption_vof": "Volume of Fluid - C++/OpenFOAM",
        "caption_lbm": "Lattice Boltzmann - C++/Palabos",
        "caption_sph": "Smoothed Particle Hydrodynamics - Python/PySPH",
        # Chatbot
        "chat_title": "AI Assistant",
        "chat_welcome": "Hello! I'm your assistant to help you understand shear-thinning ink dispensing simulations. Ask me about FEM, VOF, LBM, SPH, or fluid physics!",
        "chat_placeholder": "Ask your question...",
        "chat_error": "API connection error. Check your API key.",
        "chat_close": "Close",
        "chat_clear": "Clear",
        "chat_api_missing": "⚠️ API key missing. Configure GROQ_API_KEY.",
        "chat_disclaimer": "⚠️ AI-generated response - may contain errors or omissions. Always verify information against recognized scientific sources.",
        "chat_toggle": "AI Assistant",
        # Comparison page
        "lbl_empty_mesh": "Empty Mesh",
        "lbl_with_droplet": "With Droplet (final state)",
        # SPH
        "sph_example_title": "SPH Simulation Results",
        "sph_preliminary": "🔴 **Inconclusive results to date** - The SPH method proved unsuitable for this problem.",
        "sph_failure_title": "Why SPH does not work here?",
        "sph_failure_details": """
The SPH method was extensively tested (~115 different code versions) with two solvers (**PySPH** and **SPlisHSPlasH**) and proved **unsuitable** for simulating shear-thinning ink deposition in micro-cavities. The main reasons are:

**1. Poor surface tension handling**
- The CSF (*Continuum Surface Force*) model used in PySPH creates **splitting artifacts**: the droplet artificially splits in the middle during spreading, which is non-physical.
- The capillary CFL (Courant-Friedrichs-Lewy) constraint imposes an extremely small time step: $\\Delta t \\propto \\sqrt{\\rho h^3 / \\sigma} \\approx 10^{-8}$ s at 10 µm resolution, making computations prohibitive (~2h for 30 ms of physical time).

**2. Insufficient resolution**
- With 700 to 1,200 particles (typical 10-20 µm resolution), the fine dynamics of spreading and wetting are not captured correctly.
- Increasing resolution further worsens the time step problem.

**3. Limited adhesion models**
- Contact angles are imposed via explicit adhesion forces, a less robust approach than the wettability boundary conditions used in VOF or Phase Field methods.
- Calibration of the adhesion parameter α remains empirical and resolution-dependent.

**4. Alternative solver (SPlisHSPlasH)**
- The SPlisHSPlasH solver (DFSPH - Divergence-Free SPH + Akinci 2013) is much faster (~1,000× with the GPU) but only works at **macroscopic scale** (×1000 simulation).
- No per-wall contact angle control.
- Visually "spectacular" results (realistic splashing and waves: see last image below) but **physically wrong** for viscous ink deposition at the µm scale.

**Conclusion**: For this type of problem (µm droplet, high surface tension, variable contact angles), **VOF** (OpenFOAM) and **Phase Field** (FEM) methods are more suitable.
""",
        "sph_nok_caption_1": "PySPH - Droplet splitting (CSF artifact)",
        "sph_nok_caption_2": "PySPH - Droplet splitting (CSF artifact)",
        "sph_nok_caption_3": "PySPH - Contact angle 60°: OK. Particles escaping the cavity",
        "sph_geyser_caption": "SPlisHSPlasH (×1000 scale, not realistic for a viscous ink!)",
        # Errors
        "mapping_missing": "Mapping data missing.",
        "data_not_found": "Data not found",
    }
}

# --- Fonctions de Langue ---
def get_language():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'fr'
    return st.session_state.lang

def t(key):
    """Retourne la traduction pour la clé donnée."""
    lang = get_language()
    return TRANSLATIONS[lang].get(key, key)

# --- Styles CSS personnalisés (chargés depuis fichier externe) ---
def load_custom_css():
    """Charge le CSS depuis assets/style.css et retourne le HTML complet."""
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "style.css")
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except FileNotFoundError:
        css_content = ""  # Fallback si fichier non trouvé

    # HTML des boutons de navigation (reste ici car c'est du balisage)
    nav_buttons_html = """
<!-- Bouton retour en haut - SVG avec flèche vers le haut -->
<a href="#top" class="nav-button back-to-top" title="Retour en haut / Back to top">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 4l-8 8h5v8h6v-8h5z"/>
    </svg>
</a>
<!-- Bouton descendre en bas - SVG avec flèche vers le bas -->
<a href="#bottom" class="nav-button scroll-to-bottom" title="Aller en bas / Go to bottom">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12 20l8-8h-5V4h-6v8H4z"/>
    </svg>
</a>
<div id="top"></div>
"""
    return f"<style>{css_content}</style>{nav_buttons_html}"

st.markdown(load_custom_css(), unsafe_allow_html=True)

# --- Chemins Absolus Robustes (Compatible Cloud) ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DOC_PATH = os.path.join(ROOT_DIR, "docs")
DATA_PATH = os.path.join(ROOT_DIR, "data")
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# Chemins vers les codes sources (dans fr/ car identiques)
LBM_SRC = os.path.join(DOC_PATH, "fr/code/code_lbm.cpp")
SPH_SRC = os.path.join(DOC_PATH, "fr/code/code_sph.py")

# Chemins vers les exemples visuels
FEM_GIF_EX = os.path.join(ASSETS_PATH, "fem/gif/gif_a01.gif")
VOF_GIF_EX = os.path.join(ASSETS_PATH, "vof/gif/run_039_y_gap_buse0.03_x_gap_buse0_eta01.5_ratio_surface0.8.gif")
LBM_GIF_EX = os.path.join(ASSETS_PATH, "lbm/gif/lbm_020.gif")
SPH_GIF_EX = os.path.join(ASSETS_PATH, "sph/gif/NOK_2.gif")

# --- Fonctions Utilitaires ---

@st.cache_data(ttl=600)
def load_fem_gif_mapping():
    """Charge le mapping FEM GIF et retourne (mapping_dict, DataFrame)."""
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'fem_gif_mapping.csv'), sep=';', encoding='utf-8')
        # Convertir les virgules en points pour les floats
        df['viscosity'] = df["Viscosité de l'encre (Pa.s)"].apply(lambda x: float(str(x).replace(',', '.')))
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['diamètre du puit (µm)']), int(row['diamètre de la buse (µm)']),
                int(row['shift buse en x (µm)']), row['viscosity'],
                int(row['CA wall right']), int(row['CA gold'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "fem/gif", row['nom fichier gif'])
        return mapping, df
    except Exception:
        return {}, pd.DataFrame()

@st.cache_data(ttl=600)
def load_fem_png_mapping():
    """Charge le mapping FEM PNG et retourne (mapping_dict, DataFrame)."""
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'fem_png_mapping.csv'), sep=';', encoding='utf-8')
        # Convertir les virgules en points pour les floats
        df['viscosity'] = df["Viscosité de l'encre (Pa.s)"].apply(lambda x: float(str(x).replace(',', '.')))
        df['remplissage_f'] = df['remplissage'].apply(lambda x: float(str(x).replace(',', '.')))
        mapping = {}
        for _, row in df.iterrows():
            key = (
                int(row['temps dispense (ms)']), row['viscosity'],
                int(row['shift buse en x (µm)']), int(row['shift buse en z (µm)']),
                int(row['CA gold']), row['remplissage_f']
            )
            filename = row['nom fichier gif'].replace('.png', '.jpg')
            mapping[key] = os.path.join(ASSETS_PATH, "fem/png", filename)
        return mapping, df
    except Exception:
        return {}, pd.DataFrame()

@st.cache_data(ttl=600)
def load_vof_gif_mapping():
    """Charge le mapping VOF GIF et retourne (mapping_dict, DataFrame)."""
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'vof_gif_mapping.csv'), sep=';', encoding='utf-8')
        # Convertir les virgules en points pour les floats
        df['ratio'] = df['ratio surface goutte/puit'].apply(lambda x: float(str(x).replace(',', '.')))
        df['viscosity'] = df['Viscosite eta0 (Pa.s)'].apply(lambda x: float(str(x).replace(',', '.')))
        # Assurer que les entiers sont bien des entiers
        df['gap'] = df['gap buse (µm)'].astype(int)
        df['shift'] = df['shift buse (µm)'].astype(int)

        mapping = {}
        for _, row in df.iterrows():
            key = (
                row['ratio'], row['viscosity'],
                row['gap'], row['shift'],
                int(row['CA substrat (deg)']), int(row['CA mur gauche (deg)']),
                int(row['CA mur droit (deg)'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "vof/gif", row['nom fichier gif'])
        return mapping, df
    except Exception:
        return {}, pd.DataFrame()

@st.cache_data(ttl=600)
def load_vof_png_mapping():
    """Charge le mapping VOF PNG et retourne (mapping_dict, DataFrame)."""
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'vof_png_mapping.csv'), sep=';', encoding='utf-8')
        df['ratio'] = df['ratio surface goutte/puit'].apply(lambda x: float(str(x).replace(',', '.')))
        df['viscosity'] = df['Viscosite eta0 (Pa.s)'].apply(lambda x: float(str(x).replace(',', '.')))
        df['gap'] = df['gap buse (µm)'].astype(int)
        df['shift'] = df['shift buse (µm)'].astype(int)

        mapping = {}
        for _, row in df.iterrows():
            key = (
                row['ratio'], row['viscosity'],
                row['gap'], row['shift'],
                int(row['CA substrat (deg)']), int(row['CA mur gauche (deg)']),
                int(row['CA mur droit (deg)'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "vof/png", row['nom fichier png'])
        return mapping, df
    except Exception:
        return {}, pd.DataFrame()

@st.cache_data(ttl=600)
def load_lbm_gif_mapping():
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'lbm_gif_mapping.csv'), sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            # Clé : (ratio, ca_sub, ca_wall_l, ca_wall_r, ca_plat_l, visc, shift)
            key = (
                float(str(row['ratio surface goutte/puit']).replace(',', '.')),
                int(row['CA substrat (deg)']),
                int(row['CA mur gauche (deg)']),
                int(row['CA mur droit (deg)']),
                int(row['CA plateau gauche (deg)']),
                float(str(row['Viscosite eta0 (Pa.s)']).replace(',', '.')),
                int(row['shift X (um)'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "lbm/gif", row['nom fichier gif'])
        return mapping, df
    except Exception: return {}, pd.DataFrame()

@st.cache_data(ttl=600)
def load_lbm_png_mapping():
    try:
        df = pd.read_csv(os.path.join(DATA_PATH, 'lbm_png_mapping.csv'), sep=';', encoding='utf-8')
        mapping = {}
        for _, row in df.iterrows():
            key = (
                float(str(row['ratio surface goutte/puit']).replace(',', '.')),
                int(row['CA substrat (deg)']),
                int(row['CA mur gauche (deg)']),
                int(row['CA mur droit (deg)']),
                int(row['CA plateau gauche (deg)']),
                float(str(row['Viscosite eta0 (Pa.s)']).replace(',', '.')),
                int(row['shift X (um)'])
            )
            mapping[key] = os.path.join(ASSETS_PATH, "lbm/png", row['nom fichier png'])
        return mapping, df
    except Exception: return {}, pd.DataFrame()

def load_file_content(relative_path):
    """Charge un fichier depuis docs/<lang>/relative_path"""
    lang = get_language()
    full_path = os.path.join(DOC_PATH, lang, relative_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f: return f.read()
    except Exception:
        return f"Document not found / Document non trouvé : {os.path.join(lang, relative_path)}"

def display_smart_markdown(content):
    if "```python" in content:
        parts = content.split("```python")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='python', line_numbers=False)
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='python', line_numbers=False)
            elif part.strip():
                st.markdown(part)
    elif "```cpp" in content:
        parts = content.split("```cpp")
        for i, part in enumerate(parts):
            if i > 0:
                if "```" in part:
                    code, text = part.split("```", 1)
                    st.code(code.strip(), language='cpp', line_numbers=False)
                    if text.strip(): st.markdown(text)
                else:
                    st.code(part.strip(), language='cpp', line_numbers=False)
            elif part.strip():
                st.markdown(part)
    else:
        st.markdown(content)

def render_lbm_cascading_filters(df_origin: pd.DataFrame, key_prefix: str,
                                  sim_num: int, file_type: str = "gif") -> str | None:
    """
    Génère les filtres en cascade pour LBM (7 paramètres sur une ligne).

    Args:
        df_origin: DataFrame source avec toutes les combinaisons
        key_prefix: Préfixe pour les clés des widgets (ex: "lg" pour LBM GIF)
        sim_num: 1 ou 2 (pour l'index par défaut différent)
        file_type: "gif" ou "png"

    Returns:
        Chemin complet du fichier ou None si non trouvé
    """
    df = df_origin.copy()
    default_idx = 0 if sim_num == 1 else (1 if len(df) > 1 else 0)

    # Colonnes pour les filtres
    col_ratio = 'ratio surface goutte/puit'
    col_visc = 'Viscosite eta0 (Pa.s)'
    col_shift = 'shift X (um)'
    col_ca_sub = 'CA substrat (deg)'
    col_ca_wl = 'CA mur gauche (deg)'
    col_ca_wr = 'CA mur droit (deg)'
    col_ca_pl = 'CA plateau gauche (deg)'
    col_file = 'nom fichier gif' if file_type == "gif" else 'nom fichier png'

    st.markdown(f"**{t('sim_1') if sim_num == 1 else t('sim_2')}**")

    # 7 paramètres sur une seule ligne
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c1:
        opts = sorted(df[col_ratio].unique())
        idx = min(default_idx, len(opts) - 1)
        val_ratio = st.selectbox(t("lbl_ratio_drop"), opts, key=f"{key_prefix}_r{sim_num}", index=idx)
        df = df[df[col_ratio] == val_ratio]

    with c2:
        opts = sorted(df[col_visc].unique())
        val_visc = st.selectbox(t("lbl_viscosity"), opts, key=f"{key_prefix}_v{sim_num}")
        df = df[df[col_visc] == val_visc]

    with c3:
        opts = sorted(df[col_shift].unique())
        val_shift = st.selectbox(t("lbl_shift_x"), opts, key=f"{key_prefix}_s{sim_num}")
        df = df[df[col_shift] == val_shift]

    with c4:
        opts = sorted(df[col_ca_sub].unique())
        val_ca_sub = st.selectbox(t("lbl_ca_gold"), opts, key=f"{key_prefix}_c{sim_num}")
        df = df[df[col_ca_sub] == val_ca_sub]

    with c5:
        opts = sorted(df[col_ca_wl].unique())
        val_wl = st.selectbox(t("lbl_ca_wall_l"), opts, key=f"{key_prefix}_wl{sim_num}")
        df = df[df[col_ca_wl] == val_wl]

    with c6:
        opts = sorted(df[col_ca_wr].unique())
        val_wr = st.selectbox(t("lbl_ca_wall_r"), opts, key=f"{key_prefix}_wr{sim_num}")
        df = df[df[col_ca_wr] == val_wr]

    with c7:
        opts = sorted(df[col_ca_pl].unique())
        val_pl = st.selectbox(t("lbl_ca_plateau"), opts, key=f"{key_prefix}_pl{sim_num}")
        df = df[df[col_ca_pl] == val_pl]

    # Retourner le chemin du fichier
    if not df.empty:
        subdir = f"lbm/{file_type}"
        return os.path.join(ASSETS_PATH, subdir, df.iloc[0][col_file])
    return None


def render_fem_gif_cascading_filters(df_origin: pd.DataFrame, key_prefix: str,
                                      sim_num: int) -> str | None:
    """
    Génère les filtres en cascade pour FEM GIF (6 paramètres sur une ligne).

    Args:
        df_origin: DataFrame source avec toutes les combinaisons
        key_prefix: Préfixe pour les clés des widgets (ex: "fg" pour FEM GIF)
        sim_num: 1 ou 2 (pour l'index par défaut différent)

    Returns:
        Chemin complet du fichier ou None si non trouvé
    """
    df = df_origin.copy()
    default_idx = 0 if sim_num == 1 else (1 if len(df) > 1 else 0)

    # Colonnes pour les filtres
    col_well = 'diamètre du puit (µm)'
    col_nozzle = 'diamètre de la buse (µm)'
    col_shift = 'shift buse en x (µm)'
    col_visc = 'viscosity'  # Colonne convertie en float
    col_ca_wall = 'CA wall right'
    col_ca_gold = 'CA gold'
    col_file = 'nom fichier gif'

    st.markdown(f"**{t('sim_1') if sim_num == 1 else t('sim_2')}**")

    # 6 paramètres sur une seule ligne (avec espaceurs)
    _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])

    with c1:
        opts = sorted(df[col_well].unique())
        idx = min(default_idx, len(opts) - 1)
        val_well = st.selectbox(t("lbl_well"), opts, key=f"{key_prefix}_w{sim_num}", index=idx)
        df = df[df[col_well] == val_well]

    with c2:
        opts = sorted(df[col_nozzle].unique())
        val_nozzle = st.selectbox(t("lbl_nozzle"), opts, key=f"{key_prefix}_n{sim_num}")
        df = df[df[col_nozzle] == val_nozzle]

    with c3:
        opts = sorted(df[col_shift].unique(), reverse=True)  # 0, -75, -150
        val_shift = st.selectbox(t("lbl_shift_x"), opts, key=f"{key_prefix}_s{sim_num}")
        df = df[df[col_shift] == val_shift]

    with c4:
        opts = sorted(df[col_visc].unique(), reverse=True)  # 5.0, 1.5
        val_visc = st.selectbox(t("lbl_viscosity"), opts, key=f"{key_prefix}_v{sim_num}")
        df = df[df[col_visc] == val_visc]

    with c5:
        opts = sorted(df[col_ca_wall].unique(), reverse=True)  # 90, 35
        val_ca_wall = st.selectbox(t("lbl_ca_wall"), opts, key=f"{key_prefix}_cw{sim_num}")
        df = df[df[col_ca_wall] == val_ca_wall]

    with c6:
        opts = sorted(df[col_ca_gold].unique())
        val_ca_gold = st.selectbox(t("lbl_ca_gold"), opts, key=f"{key_prefix}_cg{sim_num}")
        df = df[df[col_ca_gold] == val_ca_gold]

    # Retourner le chemin du fichier
    if not df.empty:
        return os.path.join(ASSETS_PATH, "fem/gif", df.iloc[0][col_file])
    return None


def render_vof_cascading_filters(df_origin: pd.DataFrame, key_prefix: str,
                                  sim_num: int, file_type: str = "gif") -> str | None:
    """
    Génère les filtres en cascade pour VOF (7 paramètres sur une ligne).

    Args:
        df_origin: DataFrame source avec toutes les combinaisons
        key_prefix: Préfixe pour les clés des widgets (ex: "vg" pour VOF GIF)
        sim_num: 1 ou 2 (pour l'index par défaut différent)
        file_type: "gif" ou "png"

    Returns:
        Chemin complet du fichier ou None si non trouvé
    """
    df = df_origin.copy()
    default_idx = 0 if sim_num == 1 else (1 if len(df) > 1 else 0)

    # Colonnes pour les filtres
    col_ratio = 'ratio'
    col_visc = 'viscosity'
    col_gap = 'gap'
    col_shift = 'shift'
    col_ca_sub = 'CA substrat (deg)'
    col_ca_wl = 'CA mur gauche (deg)'
    col_ca_wr = 'CA mur droit (deg)'
    col_file = 'nom fichier gif' if file_type == "gif" else 'nom fichier png'

    st.markdown(f"**{t('sim_1') if sim_num == 1 else t('sim_2')}**")

    # 7 paramètres sur une seule ligne
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c1:
        opts = sorted(df[col_ratio].unique())
        idx = min(default_idx, len(opts) - 1)
        val_ratio = st.selectbox(t("lbl_ratio_drop"), opts, key=f"{key_prefix}_r{sim_num}", index=idx)
        df = df[df[col_ratio] == val_ratio]

    with c2:
        opts = sorted(df[col_visc].unique())
        val_visc = st.selectbox(t("lbl_viscosity"), opts, key=f"{key_prefix}_v{sim_num}")
        df = df[df[col_visc] == val_visc]

    with c3:
        opts = sorted(df[col_gap].unique())
        val_gap = st.selectbox(t("lbl_gap"), opts, key=f"{key_prefix}_g{sim_num}")
        df = df[df[col_gap] == val_gap]

    with c4:
        opts = sorted(df[col_shift].unique())
        val_shift = st.selectbox(t("lbl_shift_x"), opts, key=f"{key_prefix}_s{sim_num}")
        df = df[df[col_shift] == val_shift]

    with c5:
        opts = sorted(df[col_ca_sub].unique())
        val_ca_sub = st.selectbox(t("lbl_ca_gold"), opts, key=f"{key_prefix}_cs{sim_num}")
        df = df[df[col_ca_sub] == val_ca_sub]

    with c6:
        opts = sorted(df[col_ca_wl].unique())
        val_wl = st.selectbox(t("lbl_ca_wall_l"), opts, key=f"{key_prefix}_wl{sim_num}")
        df = df[df[col_ca_wl] == val_wl]

    with c7:
        opts = sorted(df[col_ca_wr].unique())
        val_wr = st.selectbox(t("lbl_ca_wall_r"), opts, key=f"{key_prefix}_wr{sim_num}")
        df = df[df[col_ca_wr] == val_wr]

    # Retourner le chemin du fichier
    if not df.empty:
        subdir = f"vof/{file_type}"
        return os.path.join(ASSETS_PATH, subdir, df.iloc[0][col_file])
    return None


def render_fem_png_cascading_filters(df_origin: pd.DataFrame, key_prefix: str,
                                      sim_num: int) -> str | None:
    """
    Génère les filtres en cascade pour FEM PNG (6 paramètres sur une ligne).

    Args:
        df_origin: DataFrame source avec toutes les combinaisons
        key_prefix: Préfixe pour les clés des widgets (ex: "fp" pour FEM PNG)
        sim_num: 1 ou 2 (pour l'index par défaut différent)

    Returns:
        Chemin complet du fichier ou None si non trouvé
    """
    df = df_origin.copy()
    default_idx = 0 if sim_num == 1 else (1 if len(df) > 1 else 0)

    # Colonnes pour les filtres
    col_time = 'temps dispense (ms)'
    col_visc = 'viscosity'
    col_shift_x = 'shift buse en x (µm)'
    col_shift_z = 'shift buse en z (µm)'
    col_ca_gold = 'CA gold'
    col_ratio = 'remplissage_f'
    col_file = 'nom fichier gif'

    st.markdown(f"**{t('sim_1') if sim_num == 1 else t('sim_2')}**")

    # 6 paramètres sur une seule ligne (avec espaceurs)
    _, c1, c2, c3, c4, c5, c6, _ = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])

    with c1:
        opts = sorted(df[col_time].unique())
        idx = min(default_idx, len(opts) - 1)
        val_time = st.selectbox(t("lbl_time"), opts, key=f"{key_prefix}_t{sim_num}", index=idx)
        df = df[df[col_time] == val_time]

    with c2:
        opts = sorted(df[col_visc].unique())
        val_visc = st.selectbox(t("lbl_viscosity"), opts, key=f"{key_prefix}_v{sim_num}")
        df = df[df[col_visc] == val_visc]

    with c3:
        opts = sorted(df[col_shift_x].unique(), reverse=True)
        val_shift_x = st.selectbox(t("lbl_shift_x"), opts, key=f"{key_prefix}_sx{sim_num}")
        df = df[df[col_shift_x] == val_shift_x]

    with c4:
        opts = sorted(df[col_shift_z].unique(), reverse=True)
        val_shift_z = st.selectbox(t("lbl_shift_z"), opts, key=f"{key_prefix}_sz{sim_num}")
        df = df[df[col_shift_z] == val_shift_z]

    with c5:
        opts = sorted(df[col_ca_gold].unique())
        val_ca_gold = st.selectbox(t("lbl_ca_gold"), opts, key=f"{key_prefix}_cg{sim_num}")
        df = df[df[col_ca_gold] == val_ca_gold]

    with c6:
        opts = sorted(df[col_ratio].unique())
        val_ratio = st.selectbox(t("lbl_ratio"), opts, key=f"{key_prefix}_r{sim_num}")
        df = df[df[col_ratio] == val_ratio]

    # Retourner le chemin du fichier
    if not df.empty:
        filename = df.iloc[0][col_file].replace('.png', '.jpg')
        return os.path.join(ASSETS_PATH, "fem/png", filename)
    return None


# --- Initialisation Centralisée des États ---
DEFAULT_SESSION_STATES = {
    # FEM Visualization
    'run_g': False,           # GIF viewer actif
    'run_p': False,           # PNG viewer actif
    'files_fem_g': (None, None),  # Fichiers GIF (sim1, sim2)
    'files_fem_p': (None, None),  # Fichiers PNG (sim1, sim2)
    # LBM Visualization
    'run_lbm_g': False,
    'run_lbm_p': False,
    'files_lbm_g': (None, None),
    'files_lbm_p': (None, None),
    # VOF Visualization
    'run_vof_g': False,
    'run_vof_p': False,
    'files_vof_g': (None, None),
    'files_vof_p': (None, None),
    # Chatbot
    'chat_messages': [],
}

for key, default in DEFAULT_SESSION_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Chatbot ---

def is_chatbot_enabled():
    """Vérifie si le chatbot doit être affiché."""
    # 1. Vérifier si la clé API existe
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass
    if not api_key:
        return False  # Pas de clé = pas de chatbot

    # 2. Vérifier si explicitement désactivé dans secrets
    try:
        enabled = st.secrets.get("CHATBOT_ENABLED", True)
        if isinstance(enabled, str):
            enabled = enabled.lower() in ("true", "1", "yes", "oui")
        return enabled
    except Exception:
        return True  # Par défaut activé si clé présente

# System prompt contextuel pour l'assistant
SYSTEM_PROMPT = """Tu es un assistant expert en simulation numérique de la dispense d'encre rhéofluidifiante dans des micro-puits.

Tu connais parfaitement les 4 méthodes numériques comparées dans cette application :
1. **FEM / Phase-Field** (FEniCS/Python) : Méthode des éléments finis avec approche champ de phase pour le suivi d'interface diffuse
2. **VOF** (OpenFOAM/C++) : Volume of Fluid avec suivi d'interface nette (α ∈ [0,1])
3. **LBM** (Palabos/C++) : Lattice Boltzmann avec modèle Shan-Chen pour le multiphasique
4. **SPH** (PySPH/Python) : Smoothed Particle Hydrodynamics, méthode particulaire lagrangienne

Tu maîtrises :
- La rhéologie des fluides non-newtoniens (modèle Carreau pour les encres rhéofluidifiantes)
- Les phénomènes capillaires (tension de surface σ, angles de contact θ)
- Les nombres adimensionnels (Reynolds Re, Capillaire Ca, Weber We, Ohnesorge Oh)
- Les équations de Navier-Stokes incompressibles
- Les conditions aux limites (mouillabilité, non-glissement)

Réponds de manière concise, pédagogique et scientifiquement rigoureuse.
Utilise des équations LaTeX quand c'est pertinent (format $equation$ pour inline).
Si tu ne connais pas la réponse, dis-le honnêtement.
Réponds dans la langue de l'utilisateur (français ou anglais).
"""

def get_groq_client():
    """Retourne le client Groq si la clé API est disponible."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", None)
        except Exception:
            pass
    if api_key:
        return Groq(api_key=api_key)
    return None

def stream_groq_response(user_message: str):
    """Génère la réponse de Groq (Llama 3) en streaming."""
    client = get_groq_client()
    if not client:
        yield t("chat_api_missing")
        return

    st.session_state.chat_messages.append({"role": "user", "content": user_message})

    try:
        # Préparer les messages avec le system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(st.session_state.chat_messages)

        # Générer la réponse en streaming
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                full_response += text
                yield text

        # Sauvegarder la réponse complète dans l'historique
        st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        error_msg = f"{t('chat_error')} ({str(e)[:50]}...)"
        yield error_msg

def render_chatbot():
    """Affiche le chatbot dans un popover sidebar."""
    with st.sidebar.popover(f"{t('chat_title')}", use_container_width=True):
        # Bouton effacer
        if st.button(t("chat_clear"), use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

        st.markdown("---")

        # Message de bienvenue
        if not st.session_state.chat_messages:
            st.info(t("chat_welcome"))

        # Historique des messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Disclaimer après les réponses
        if st.session_state.chat_messages:
            st.caption(t("chat_disclaimer"))

        # Zone de saisie
        if prompt := st.chat_input(t("chat_placeholder")):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                # Streaming : affichage progressif mot par mot !
                st.write_stream(stream_groq_response(prompt))
            st.caption(t("chat_disclaimer"))


# =====================================================================
# Page functions
# =====================================================================

def page_home():
    st.markdown(f"""
    <div class="hero-banner">
        <h1>{t("title")}</h1>
        <p>{t("hero_subtitle")}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Layout côte-à-côte : note auteur (gauche) + GIF VOF (droite) ---
    accueil_content = load_file_content("accueil/accueil.md")
    parts = accueil_content.split("---", 1)

    col_text, col_img = st.columns([3, 1])
    with col_text:
        st.markdown(parts[0])
    with col_img:
        vof_gif = os.path.join(ASSETS_PATH, "vof", "gif", "run_057_y_gap_buse0.12_x_gap_buse0_eta01.5_ratio_surface0.8.gif")
        if os.path.exists(vof_gif):
            st.image(vof_gif, use_container_width=True)
            st.caption("VOF - OpenFOAM")

    # --- Reste du contenu en pleine largeur ---
    if len(parts) > 1:
        st.markdown("---" + parts[1])

    st.markdown("---")
    st.header(t("overview_title"))
    st.markdown(f'<p style="font-size:18px; color:#1E90FF; font-weight:bold; margin-top:-10px;"><em>({t("overview_subtitle")})</em></p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 1. VOF (OpenFOAM)")
        if os.path.exists(VOF_GIF_EX):
            st.image(VOF_GIF_EX, use_container_width=True)
        st.caption(t("caption_vof"))

    with col2:
        st.markdown("#### 2. LBM (Palabos)")
        if os.path.exists(LBM_GIF_EX):
            st.image(LBM_GIF_EX, use_container_width=True)
        st.caption(t("caption_lbm"))

    with col3:
        st.markdown("#### 3. SPH (PySPH)")
        if os.path.exists(SPH_GIF_EX):
            with open(SPH_GIF_EX, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            st.markdown(f'<img src="data:image/gif;base64,{data}" style="width:100%">', unsafe_allow_html=True)
        st.caption(t("caption_sph"))


def page_introduction():
    st.title("Introduction")
    st.markdown("---")
    st.markdown(load_file_content("intro/intro_project.md"))


def page_comparison():
    gen_pages = t("gen_pages")
    st.title(gen_pages[2])
    st.markdown("---")
    # Partie 1: Sections 1-3.3
    st.markdown(load_file_content("comparaison/comparaison_models.md"))

    # --- Section visuelle: Visualisation des maillages (après section 2) ---
    # Espacement avant les onglets
    st.markdown("<br><br>", unsafe_allow_html=True)

    current_lang = st.session_state.get('lang', 'fr')

    # Onglets pour les 3 méthodes (ordre cohérent: VOF, LBM, SPH)
    mesh_tabs = st.tabs(["VOF", "LBM", "SPH"])

    mesh_images = {
        "VOF": os.path.join(ASSETS_PATH, "comparaison", "mesh_vof.png"),
        "LBM": os.path.join(ASSETS_PATH, "comparaison", "mesh_lbm.png"),
        "SPH": os.path.join(ASSETS_PATH, "comparaison", "mesh_sph.png"),
    }

    droplet_images = {
        "VOF": os.path.join(ASSETS_PATH, "comparaison", "droplet_vof.png"),
        "LBM": os.path.join(ASSETS_PATH, "comparaison", "droplet_lbm.png"),
        "SPH": os.path.join(ASSETS_PATH, "comparaison", "droplet_sph.png"),
    }

    mesh_captions = {
        "fr": {
            "VOF": "Maillage hexaédrique avec raffinement AMR (Eulérien)",
            "LBM": "Grille uniforme 5 µm = 1 l.u. (Eulérien)",
            "SPH": "Particules discrètes avec rayon d'influence h (Lagrangien)",
        },
        "en": {
            "VOF": "Hexahedral mesh with AMR refinement (Eulerian)",
            "LBM": "Uniform grid 5 µm = 1 l.u. (Eulerian)",
            "SPH": "Discrete particles with influence radius h (Lagrangian)",
        }
    }

    droplet_captions = {
        "fr": {
            "VOF": "Fraction volumique α : encre (1) / air (0)",
            "LBM": "Densité ρ : liquide (~458 l.u.) / air (~90 l.u.)",
            "SPH": "Particules d'encre étalées dans le puits",
        },
        "en": {
            "VOF": "Volume fraction α: ink (1) / air (0)",
            "LBM": "Density ρ: liquid (~458 l.u.) / air (~90 l.u.)",
            "SPH": "Ink particles spread in the well",
        }
    }

    for i, method in enumerate(["VOF", "LBM", "SPH"]):
        with mesh_tabs[i]:
            col_mesh, col_droplet = st.columns(2)

            with col_mesh:
                st.markdown(f"**{t('lbl_empty_mesh')}**")
                img_path = mesh_images[method]
                if os.path.exists(img_path):
                    st.image(img_path, caption=mesh_captions[current_lang][method], use_container_width=True)
                else:
                    st.warning(f"Image non disponible: {img_path}")

            with col_droplet:
                st.markdown(f"**{t('lbl_with_droplet')}**")
                droplet_path = droplet_images[method]
                if os.path.exists(droplet_path):
                    st.image(droplet_path, caption=droplet_captions[current_lang][method], use_container_width=True)
                else:
                    st.warning(f"Image non disponible: {droplet_path}")

    # Partie 2: Sections 4-9 (après les images)
    st.markdown(load_file_content("comparaison/comparaison_models_part2.md"))


def page_vof():
    st.title(t("title_model_1"))
    tabs = st.tabs(t("tabs_dual"))

    with tabs[0]:  # Physique
        st.markdown(load_file_content("physics/physics_vof.md"))

    with tabs[1]:  # Code
        display_smart_markdown(load_file_content("code/code_vof.md"))

    with tabs[2]:  # GIF
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("gif_viewer"))

        _, df_vof_gif = load_vof_gif_mapping()

        with c_pop:
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                if not df_vof_gif.empty:
                    st.dataframe(df_vof_gif, use_container_width=True, hide_index=True)
                else:
                    st.error(t("data_not_found"))

        if not df_vof_gif.empty:
            with st.container(border=True):
                # Simulation 1 - Filtres en cascade
                file_1 = render_vof_cascading_filters(df_vof_gif, "vg", 1, "gif")
                st.divider()
                # Simulation 2 - Filtres en cascade
                file_2 = render_vof_cascading_filters(df_vof_gif, "vg", 2, "gif")

                # Boutons
                _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
                with btn_col1:
                    if st.button(t("btn_launch"), type="primary", use_container_width=True, key="btn_vof_g"):
                        st.session_state.run_vof_g = True
                        st.session_state.files_vof_g = (file_1, file_2)
                with btn_col2:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_vof_g"):
                        st.session_state.run_vof_g = False
                        st.rerun()

            if st.session_state.get('run_vof_g', False):
                with st.container(border=True):
                    res_cols = st.columns(2)
                    files = st.session_state.files_vof_g

                    # Sim 1
                    with res_cols[0]:
                        st.subheader(t("sim_1"))
                        if files[0] and os.path.exists(files[0]):
                            st.image(files[0], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))

                    # Sim 2
                    with res_cols[1]:
                        st.subheader(t("sim_2"))
                        if files[1] and os.path.exists(files[1]):
                            st.image(files[1], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))
        else:
            st.warning(t("mapping_missing"))

    with tabs[3]:  # PNG
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("png_viewer"))

        _, df_vof_png = load_vof_png_mapping()

        with c_pop:
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                if not df_vof_png.empty:
                    st.dataframe(df_vof_png, use_container_width=True, hide_index=True)
                else:
                    st.error(t("data_not_found"))

        if not df_vof_png.empty:
            with st.container(border=True):
                # Simulation 1 - Filtres en cascade
                file_p1 = render_vof_cascading_filters(df_vof_png, "vp", 1, "png")
                st.divider()
                # Simulation 2 - Filtres en cascade
                file_p2 = render_vof_cascading_filters(df_vof_png, "vp", 2, "png")

                # Boutons
                _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
                with btn_col1:
                    if st.button(t("btn_show"), type="primary", use_container_width=True, key="btn_vof_p"):
                        st.session_state.run_vof_p = True
                        st.session_state.files_vof_p = (file_p1, file_p2)
                with btn_col2:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_vof_p"):
                        st.session_state.run_vof_p = False
                        st.rerun()

            if st.session_state.get('run_vof_p', False):
                with st.container(border=True):
                    res_cols = st.columns(2)
                    files_p = st.session_state.files_vof_p

                    with res_cols[0]:
                        st.subheader(t("sim_1"))
                        if files_p[0] and os.path.exists(files_p[0]):
                            st.image(files_p[0], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))

                    with res_cols[1]:
                        st.subheader(t("sim_2"))
                        if files_p[1] and os.path.exists(files_p[1]):
                            st.image(files_p[1], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))
        else:
            st.warning(t("mapping_missing"))


def page_lbm():
    st.title(t("title_model_2"))
    tabs = st.tabs(t("tabs_dual"))

    with tabs[0]:
        st.markdown(load_file_content("physics/physics_lbm.md"))

    with tabs[1]:
        display_smart_markdown(load_file_content("code/code_lbm.md"))

    with tabs[2]:  # GIF
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("gif_viewer"))

        _, df_g_origin = load_lbm_gif_mapping()

        with c_pop:
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                if not df_g_origin.empty:
                    st.dataframe(df_g_origin, use_container_width=True, hide_index=True)
                else:
                    st.error(t("data_not_found"))

        if not df_g_origin.empty:
            with st.container(border=True):
                # Simulation 1 - Filtres en cascade
                file_1 = render_lbm_cascading_filters(df_g_origin, "lg", 1, "gif")
                st.divider()
                # Simulation 2 - Filtres en cascade
                file_2 = render_lbm_cascading_filters(df_g_origin, "lg", 2, "gif")

                # Boutons
                _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
                with btn_col1:
                    if st.button(t("btn_launch"), type="primary", use_container_width=True, key="btn_lbm_g"):
                        st.session_state.run_lbm_g = True
                        st.session_state.files_lbm_g = (file_1, file_2)
                with btn_col2:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_lbm_g"):
                        st.session_state.run_lbm_g = False
                        st.rerun()

            if st.session_state.get('run_lbm_g', False):
                with st.container(border=True):
                    res_cols = st.columns(2)
                    files = st.session_state.files_lbm_g

                    # Sim 1
                    with res_cols[0]:
                        st.subheader(t("sim_1"))
                        if files[0] and os.path.exists(files[0]):
                            st.image(files[0], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))

                    # Sim 2
                    with res_cols[1]:
                        st.subheader(t("sim_2"))
                        if files[1] and os.path.exists(files[1]):
                            st.image(files[1], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))
        else:
            st.warning(t("mapping_missing"))

    with tabs[3]:  # PNG
        c_title, c_pop = st.columns([0.7, 0.3])
        with c_title:
            st.subheader(t("png_viewer"))

        _, df_p_origin = load_lbm_png_mapping()

        with c_pop:
            with st.popover(t("lbl_avail_sims"), use_container_width=True):
                if not df_p_origin.empty:
                    st.dataframe(df_p_origin, use_container_width=True, hide_index=True)
                else:
                    st.error(t("data_not_found"))

        if not df_p_origin.empty:
            with st.container(border=True):
                # Simulation 1 - Filtres en cascade
                file_p1 = render_lbm_cascading_filters(df_p_origin, "lp", 1, "png")
                st.divider()
                # Simulation 2 - Filtres en cascade
                file_p2 = render_lbm_cascading_filters(df_p_origin, "lp", 2, "png")

                # Boutons
                _, btn_col1, btn_col2, _ = st.columns([1, 1, 1, 1])
                with btn_col1:
                    if st.button(t("btn_show"), type="primary", use_container_width=True, key="btn_lbm_p"):
                        st.session_state.run_lbm_p = True
                        st.session_state.files_lbm_p = (file_p1, file_p2)
                with btn_col2:
                    if st.button(t("btn_reset"), type="secondary", use_container_width=True, key="rst_lbm_p"):
                        st.session_state.run_lbm_p = False
                        st.rerun()

            if st.session_state.get('run_lbm_p', False):
                with st.container(border=True):
                    res_cols = st.columns(2)
                    files_p = st.session_state.files_lbm_p

                    with res_cols[0]:
                        st.subheader(t("sim_1"))
                        if files_p[0] and os.path.exists(files_p[0]):
                            st.image(files_p[0], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))

                    with res_cols[1]:
                        st.subheader(t("sim_2"))
                        if files_p[1] and os.path.exists(files_p[1]):
                            st.image(files_p[1], use_container_width=True)
                        else:
                            st.warning(t("image_unavailable"))
        else:
            st.warning(t("mapping_missing"))


def page_sph():
    st.title(t("title_model_3"))
    tabs = st.tabs(t("tabs_other"))

    with tabs[0]:
        st.markdown(load_file_content("physics/physics_sph.md"))

    with tabs[1]:
        display_smart_markdown(load_file_content("code/code_sph.md"))

    with tabs[2]:
        st.subheader(t("sph_example_title"))
        st.error(t("sph_preliminary"))

        # Detailed explanation first
        with st.expander(t('sph_failure_title'), expanded=True):
            st.markdown(t("sph_failure_details"))

        # GIFs with red border (NOK results) - below explanation
        st.markdown("---")
        sph_gifs = {
            "NOK_1": os.path.join(ASSETS_PATH, "sph/gif/NOK_1.gif"),
            "NOK_2": os.path.join(ASSETS_PATH, "sph/gif/NOK_2.gif"),
            "NOK_3": os.path.join(ASSETS_PATH, "sph/gif/NOK_3.gif"),
            "geyser": os.path.join(ASSETS_PATH, "sph/gif/geyser.gif"),
        }
        sph_captions = {
            "NOK_1": t("sph_nok_caption_1"),
            "NOK_2": t("sph_nok_caption_2"),
            "NOK_3": t("sph_nok_caption_3"),
            "geyser": t("sph_geyser_caption"),
        }

        # PySPH NOK GIFs side by side
        col1, col2 = st.columns(2)
        for col, key in zip([col1, col2], ["NOK_1", "NOK_3"]):
            path = sph_gifs[key]
            if os.path.exists(path):
                with col:
                    with open(path, "rb") as f:
                        data = base64.b64encode(f.read()).decode()
                    st.markdown(
                        f'<img src="data:image/gif;base64,{data}" '
                        f'style="width:100%; border: 3px solid red; border-radius: 8px;">',
                        unsafe_allow_html=True,
                    )
                    st.caption(f"✗ {sph_captions[key]}")

        # SPlisHSPlasH - full width
        path = sph_gifs["geyser"]
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            st.markdown(
                f'<img src="data:image/gif;base64,{data}" '
                f'style="width:100%; border: 3px solid dodgerblue; border-radius: 8px;">',
                unsafe_allow_html=True,
            )
            st.caption(sph_captions["geyser"])


def page_conclusion():
    annex_pages = t("annex_pages")
    st.title(annex_pages[0])
    st.markdown("---")
    st.markdown(load_file_content("conclusion/conclusion.md"))


def page_lexique():
    annex_pages = t("annex_pages")
    st.title(annex_pages[1])
    st.markdown("---")
    st.markdown(load_file_content("lexique/lexique.md"))


def page_equations():
    annex_pages = t("annex_pages")
    st.title(annex_pages[2])
    st.markdown("---")
    st.markdown(load_file_content("equations/equations_clef.md"))


def page_histoire():
    annex_pages = t("annex_pages")
    st.title(annex_pages[3])
    st.markdown("---")
    st.markdown(load_file_content("histoire/histoire.md"))


def page_biblio():
    annex_pages = t("annex_pages")
    st.title(annex_pages[4])
    st.markdown("---")
    st.markdown(load_file_content("biblio/biblio.md"))


# =====================================================================
# Sidebar + Navigation
# =====================================================================

# Sélecteur de langue avec conservation de la page
old_lang = st.session_state.get('lang', 'fr')
lang_selection = st.sidebar.radio(
    "Language",
    ["Français", "English"],
    horizontal=True,
    label_visibility="collapsed",
    index=0 if old_lang == "fr" else 1
)
new_lang = "fr" if "Français" in lang_selection else "en"

# Si la langue change, simplement rerun (les url_path sont stables)
if new_lang != old_lang:
    st.session_state.lang = new_lang
    st.rerun()

st.session_state.lang = new_lang

st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown("---")

# Listes de titres de pages (traduites)
gen_pages = t("gen_pages")
model_pages = t("model_pages")
annex_pages = t("annex_pages")

# Construction des objets st.Page (url_path stable pour survie au changement de langue)
_GEN_PAGES = [
    st.Page(func, title=title, url_path=url, default=(url == "home"))
    for func, title, url in zip(
        [page_home, page_introduction, page_comparison],
        gen_pages,
        ["home", "introduction", "comparison"],
    )
]
_MODEL_PAGES = [
    st.Page(func, title=title, url_path=url)
    for func, title, url in zip(
        [page_vof, page_lbm, page_sph],
        model_pages,
        ["vof", "lbm", "sph"],
    )
]
_ANNEX_PAGES = [
    st.Page(func, title=title, url_path=url)
    for func, title, url in zip(
        [page_conclusion, page_lexique, page_equations, page_histoire, page_biblio],
        annex_pages,
        ["conclusion", "glossary", "equations", "history", "bibliography"],
    )
]

# Routing via st.navigation (caché - sidebar custom ci-dessous)
nav = st.navigation(
    {
        t("gen_header"): _GEN_PAGES,
        t("models_header"): _MODEL_PAGES,
        t("annex_header"): _ANNEX_PAGES,
    },
    position="hidden",
)

# Sidebar custom avec st.page_link (fiable avec st.navigation)
_GROUPS = [
    (t("gen_header"), _GEN_PAGES),
    (t("models_header"), _MODEL_PAGES),
    (t("annex_header"), _ANNEX_PAGES),
]

for header, pages in _GROUPS:
    st.sidebar.subheader(header)
    for page in pages:
        is_active = page is nav
        st.sidebar.page_link(
            page,
            label=f"**{page.title}**" if is_active else page.title,
            icon=":material/arrow_right:" if is_active else None,
            use_container_width=True,
        )
    st.sidebar.markdown("---")

# Sidebar extras
if is_chatbot_enabled():
    render_chatbot()
    st.sidebar.markdown("---")

st.sidebar.markdown(t("version_info"))
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("© 2025 Eric QUEAU - [MIT License](https://opensource.org/licenses/MIT)")

# --- Forcer l'accueil à chaque nouvelle session ---
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True
    if nav != _GEN_PAGES[0]:
        st.switch_page(_GEN_PAGES[0])

# --- Exécution de la page sélectionnée ---
nav.run()

# --- Ancre de fin de page pour bouton scroll-to-bottom ---
st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
