"""
📋 FICHIER DE PARAMÈTRES - Configuration centralisée du projet PDF
Tous les paramètres modifiables sont regroupés ici pour faciliter les ajustements
"""

# ====================================================================
# 📊 PARAMÈTRES EXCEL
# ====================================================================

# Nom de la feuille Excel contenant les données patients
EXCEL_SHEET_NAME = "feuille1"  # Attention à la casse !

# Noms des colonnes dans le fichier Excel
COLONNE_ID = "ID_unique"           # Colonne contenant l'identifiant patient (ex: 10002530)
COLONNE_NOM = "Nom"                # Colonne contenant le nom de famille
COLONNE_PRENOM = "Prénom"          # Colonne contenant le prénom
COLONNE_DOCTEUR = "docteur_nom"    # Colonne contenant le nom du docteur


# ====================================================================
# 🏥 PARAMÈTRES LOGO MEDILEC (Position indépendante)
# ====================================================================

# Chemin du fichier logo
LOGO_PATH = "Medilec-Logo.png"

# Dimensions du logo (en pixels)
LOGO_WIDTH = 180
LOGO_HEIGHT = 66

# Facteur d'agrandissement du logo (1 = taille normale, 2 = x2, etc.)
LOGO_SCALE = 2

# === POSITION INDÉPENDANTE DU LOGO ===
# Position X du logo (pourcentage de la largeur de page)
LOGO_POSITION_X_RATIO = 0.52  # 52% de la largeur de page

# Position Y du logo (distance depuis le haut de la page)
LOGO_POSITION_Y_OFFSET = 133  # Distance depuis le haut

# Hauteur du logo dans le rectangle (réduite)
LOGO_HEIGHT_DANS_RECT = 25

# Le logo sera centré horizontalement dans sa zone


# ====================================================================
# 👨‍⚕️ PARAMÈTRES TEXTE DOCTEUR (Position indépendante)
# ====================================================================

# Taille de la police du texte docteur
DOCTEUR_FONT_SIZE = 12

# Police utilisée pour le texte docteur
DOCTEUR_FONT_NAME = "Helvetica"  # Sans gras

# Préfixe du texte docteur
DOCTEUR_PREFIX = "Docteur : "

# === POSITION INDÉPENDANTE DU DOCTEUR ===
# Position X du docteur (pourcentage de la largeur de page)
DOCTEUR_POSITION_X_RATIO = 0.55  # 52% de la largeur de page

# Position Y du docteur (distance depuis le haut de la page)
DOCTEUR_POSITION_Y_OFFSET = 58  # Distance depuis le haut (au-dessus du logo)

# Marge gauche du texte docteur (en pixels)
DOCTEUR_MARGE_GAUCHE = 3

# Masque sous le texte docteur pour cacher l'ancien contenu
DOCTEUR_MASK_PADDING_X = 5  # marge horizontale ajoutée à gauche
DOCTEUR_MASK_PADDING_Y = 2  # marge verticale autour du texte
# Couleur du masque docteur (blanc opaque RGBA 0-1)
DOCTEUR_MASK_COLOR_R = 1.0
DOCTEUR_MASK_COLOR_G = 1.0
DOCTEUR_MASK_COLOR_B = 1.0
DOCTEUR_MASK_COLOR_A = 1.0  # transparence (0=transparent, 1=opaque)


# ====================================================================
# 📐 PARAMÈTRES ZONE DE MASQUAGE (Rectangle rose)
# ====================================================================

# Position X de la zone (pourcentage de la largeur de page)
ZONE_POSITION_X_RATIO = 0.51

# Position Y de la zone (distance depuis le haut de la page)
ZONE_POSITION_Y_OFFSET = 48

# Hauteur de la zone du rectangle rose
ZONE_HEIGHT = 90

# Marge droite de la zone (distance du bord droit)
ZONE_MARGE_DROITE = 100


# ====================================================================
# 📄 PARAMÈTRES TRAITEMENT LOCAL 1 & 2 (Remplacement ID)
# ====================================================================

# Tolérance de recherche pour détecter les étiquettes "Nom:" et "Prénom:"
# (distance maximale en pixels)
LABEL_TOLERANCE_X = 80   # Tolérance horizontale
LABEL_TOLERANCE_Y = 15   # Tolérance verticale

# Marge pour le masquage blanc des IDs
ID_MASK_MARGIN_X = 2     # Marge horizontale
ID_MASK_MARGIN_Y = 2     # Marge verticale

# Taille de police pour les remplacements
REPLACEMENT_FONT_SIZE = 10
REPLACEMENT_FONT_NAME = "Helvetica"


# ====================================================================
# 🔍 PARAMÈTRES DÉTECTION PATIENT
# ====================================================================

# Expression régulière pour détecter les numéros patients
# Format attendu : 1000 suivi de 4 chiffres (avec ou sans espace/tiret)
PATIENT_ID_REGEX = r'1000[\s\-]?\d{4}'


# ====================================================================
# 🎨 PARAMÈTRES COULEURS
# ====================================================================

# Couleur du masque blanc (RGB, valeurs entre 0 et 1)
MASK_COLOR_R = 1.0
MASK_COLOR_G = 1.0
MASK_COLOR_B = 1.0

# Couleur du masque (tuple RGB)
REDACT_COLOR = (MASK_COLOR_R, MASK_COLOR_G, MASK_COLOR_B)

# Couleur du texte noir (RGB, valeurs entre 0 et 1)
TEXT_COLOR_R = 0.0
TEXT_COLOR_G = 0.0
TEXT_COLOR_B = 0.0


# ====================================================================
# 📁 PARAMÈTRES FICHIERS
# ====================================================================

# Dossier contenant les PDFs à traiter
PDF_FOLDER = "PDF"

# Fichier Excel contenant les données patients
EXCEL_FILE = "patients.xlsx"

# Extension des fichiers PDF de sortie
OUTPUT_SUFFIX = "_anonymisé"

# Dossier par défaut pour les PDF (si non spécifié)
DEFAULT_PDF_FOLDER = "PDF"

# Seuil (en %) de hauteur de page considérée comme "entête"
HEADER_Y_THRESHOLD = 0.25
