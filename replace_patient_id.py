#!/usr/bin/env python3
"""
replace_patient_id.py

Script pour remplacer automatiquement les numéros patients (ex: 1000-3628)
par leur nom et prénom à partir d'un fichier Excel.

Dépendances :
  pip install pdfplumber reportlab pypdf pandas openpyxl

Usage :
  python replace_patient_id.py
"""

import os
import re
import pandas as pd
import pdfplumber
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from pypdf import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader  # NOUVEAU - Pour gestion des images (Traitement local 3)

# ============================
# ==== IMPORT DES PARAMÈTRES ====
# ============================
from parametres import *

# ============================
# ==== CHEMINS PAR DÉFAUT ====
# ============================

# Construction des chemins à partir du répertoire du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(SCRIPT_DIR, EXCEL_FILE)  # Chemin vers le fichier Excel
PDF_FOLDER_PATH = os.path.join(SCRIPT_DIR, PDF_FOLDER)  # Dossier contenant les PDF

# ============================
# ==== FIN DES PARAMÈTRES ====
# ============================


# --- Motifs pour reconnaître les IDs patients et les étiquettes ---
ID_SINGLE = re.compile(r"1000\d{4}$")
ID_WITH_SEP = re.compile(r"1000[-–—\s]\d{4}$")
FOUR_DIGITS = re.compile(r"^\d{4}$")

LBL_NOM = re.compile(r"^nom:?$", re.IGNORECASE)
LBL_PRENOM = re.compile(r"^pr[ée]nom:?$", re.IGNORECASE)


def extract_patient_number(text: str):
    """🔍 Extrait un numéro patient du texte (ex: 10002530 ou 1000-2530)."""
    match = re.search(r"1000[\s\-]?\d{4}", text)
    return re.sub(r"[\s\-]", "", match.group()) if match else None


def find_labels(page):
    """📍 Trouve les positions des étiquettes 'Nom :' et 'Prénom :' sur la page."""
    words = page.extract_words() or []
    out_nom, out_prenom = [], []
    for w in words:
        t = (w.get("text") or "").strip()
        if LBL_NOM.fullmatch(t):
            out_nom.append({
                "x0": float(w["x0"]), "x1": float(w["x1"]),
                "top": float(w["top"]), "bottom": float(w["bottom"]),
                "mid_y": (float(w["top"]) + float(w["bottom"])) / 2.0
            })
        elif LBL_PRENOM.fullmatch(t):
            out_prenom.append({
                "x0": float(w["x0"]), "x1": float(w["x1"]),
                "top": float(w["top"]), "bottom": float(w["bottom"]),
                "mid_y": (float(w["top"]) + float(w["bottom"])) / 2.0
            })
    return out_nom, out_prenom


def find_id_candidates(page):
    """🔢 Repère les coordonnées des identifiants (ex: 10002530) dans la page."""
    words = page.extract_words() or []
    cands = []
    for i, w in enumerate(words):
        t = w["text"]
        if ID_SINGLE.fullmatch(t) or ID_WITH_SEP.fullmatch(t):
            cands.append({
                "x0": float(w["x0"]), "x1": float(w["x1"]),
                "top": float(w["top"]), "bottom": float(w["bottom"]),
                "mid_y": (float(w["top"]) + float(w["bottom"])) / 2.0
            })
        elif t == "1000" and i + 1 < len(words) and FOUR_DIGITS.fullmatch(words[i + 1]["text"]):
            # Cas où le PDF sépare "1000" et "2530"
            w2 = words[i + 1]
            cands.append({
                "x0": float(w["x0"]), "x1": float(w2["x1"]),
                "top": min(float(w["top"]), float(w2["top"])),
                "bottom": max(float(w["bottom"]), float(w2["bottom"])),
                "mid_y": ((float(w["top"]) + float(w["bottom"])) +
                          (float(w2["top"]) + float(w2["bottom"]))) / 4.0
            })
    return cands


def assign_replacements_for_page(page, full_name, nom, prenom):
    """
    🧩 Associe à chaque identifiant patient le bon texte à insérer.
    Ajoute un flag 'is_header' = True pour les éléments situés dans l'entête.
    """
    H = float(page.height)
    ids = find_id_candidates(page)
    lbl_nom, lbl_prenom = find_labels(page)
    results, ambiguous = [], []

    VERT_TOL, HORZ_TOL = 6.0, 50.0

    # --- Étape 1 : correspondance directe avec "Nom:" ou "Prénom:" ---
    for cand in ids:
        assigned = None
        for lab in lbl_nom:
            if lab["x1"] <= cand["x0"] + HORZ_TOL and abs(lab["mid_y"] - cand["mid_y"]) <= VERT_TOL:
                assigned = nom
                break
        if assigned is None:
            for lab in lbl_prenom:
                if lab["x1"] <= cand["x0"] + HORZ_TOL and abs(lab["mid_y"] - cand["mid_y"]) <= VERT_TOL:
                    assigned = prenom
                    break

        if assigned is None:
            ambiguous.append(cand)
        else:
            results.append((cand["x0"], H - cand["bottom"], cand["x1"], H - cand["top"], assigned, False))

    # --- Étape 2 : gestion des cas ambigus (ex: entête ou nom manquant) ---
    if ambiguous:
        HEAD_THRESH = H * HEADER_Y_THRESHOLD
        header_ids = [c for c in ambiguous if c["top"] < HEAD_THRESH]
        body_ids = [c for c in ambiguous if c["top"] >= HEAD_THRESH]

        # → Entête : premier = nom, deuxième = prénom
        if len(header_ids) >= 2:
            header_ids.sort(key=lambda x: x["x0"])
            assign_seq = [nom, prenom]
            for i, cand in enumerate(header_ids[:2]):
                results.append((cand["x0"], H - cand["bottom"], cand["x1"], H - cand["top"], assign_seq[i], True))
        elif len(header_ids) == 1:
            cand = header_ids[0]
            results.append((cand["x0"], H - cand["bottom"], cand["x1"], H - cand["top"], full_name, True))

        # → Corps : alterner nom / prénom
        toggle = True
        for cand in body_ids:
            text = nom if toggle else prenom
            toggle = not toggle
            results.append((cand["x0"], H - cand["bottom"], cand["x1"], H - cand["top"], text, False))

    # --- Padding léger pour recouvrir correctement le texte d'origine ---
    padded = []
    for (x0, y0, x1, y1, txt, is_header) in results:
        pad = 1.5
        padded.append((x0 - pad, y0 - pad, x1 + pad, y1 + pad, txt, is_header))
    return padded


def create_overlay(page_width, page_height, items):
    """
    ✍️ Génère un calque PDF contenant les remplacements :
    - Masque blanc sur les anciens numéros
    - Texte ajusté et aligné
    - Police selon contexte (gras ou non)
    """
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    for (x0, y0, x1, y1, replacement, is_header) in items:
        w, h = x1 - x0, y1 - y0

        # 🩶 Masque blanc (efface l'ancien identifiant)
        c.setFillColorRGB(MASK_COLOR_R, MASK_COLOR_G, MASK_COLOR_B)
        c.rect(x0, y0, w, h, fill=1, stroke=0)

        # --- Choix de la police ---
        font_name = "Helvetica-Bold" if is_header else REPLACEMENT_FONT_NAME

        # --- Ajustement automatique de la taille ---
        base_size = max(7, int(h * 0.8))
        c.setFillColorRGB(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B)
        size = base_size
        max_width = w * 0.95
        text_width = pdfmetrics.stringWidth(replacement, font_name, size)
        while text_width > max_width and size > 5:
            size -= 0.5
            text_width = pdfmetrics.stringWidth(replacement, font_name, size)
        c.setFont(font_name, size)

        # --- Centrage vertical précis ---
        ascent = pdfmetrics.getAscent(font_name) / 1000.0 * size
        descent = abs(pdfmetrics.getDescent(font_name)) / 1000.0 * size
        text_h = ascent + descent
        baseline_y = y0 + (h - text_h) / 2.0 + descent - 1.0

        # --- Alignement gauche (corrige le vide avant le texte) ---
        left_offset = -1.2
        text_x = x0 + left_offset
        c.drawString(text_x, baseline_y, replacement)

    c.save()
    packet.seek(0)
    return packet


def create_medilec_overlay(page_width, page_height, docteur_nom):
    """
    🏥 TRAITEMENT LOCAL 3 - Génère un calque avec logo Medilec + nom du docteur
    
    POSITIONS INDÉPENDANTES:
    - Le docteur a sa propre position (X, Y)
    - Le logo a sa propre position (X, Y)
    - Ils ne sont plus liés l'un à l'autre
    
    Args:
        page_width: Largeur de la page PDF
        page_height: Hauteur de la page PDF  
        docteur_nom: Nom du docteur à afficher
        
    Returns:
        BytesIO: Calque PDF avec logo et docteur
    """
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # === ZONE DE MASQUAGE (Rectangle rose) ===
    zone_x = page_width * ZONE_POSITION_X_RATIO
    zone_y = page_height - ZONE_POSITION_Y_OFFSET - ZONE_HEIGHT
    zone_width = page_width - zone_x - ZONE_MARGE_DROITE
    zone_height = ZONE_HEIGHT
    
    # Masquage blanc du rectangle rose
    print(f"🎯 Rectangle rose: x={zone_x:.1f}, y={zone_y:.1f}, w={zone_width:.1f}, h={zone_height}")
    c.setFillColorRGB(MASK_COLOR_R, MASK_COLOR_G, MASK_COLOR_B)
    c.rect(zone_x, zone_y, zone_width, zone_height, fill=1, stroke=0)
    
    # === POSITION INDÉPENDANTE DU DOCTEUR ===
    docteur_x = page_width * DOCTEUR_POSITION_X_RATIO + DOCTEUR_MARGE_GAUCHE
    docteur_y = page_height - DOCTEUR_POSITION_Y_OFFSET

    # Masque local derrière le texte docteur pour effacer l'ancien contenu (rose transparent)
    mask_x = max(0, docteur_x - DOCTEUR_MASK_PADDING_X)
    mask_y = max(0, docteur_y - DOCTEUR_MASK_PADDING_Y)
    mask_w = page_width - mask_x - ZONE_MARGE_DROITE
    mask_h = DOCTEUR_FONT_SIZE + 2 * DOCTEUR_MASK_PADDING_Y
    c.saveState()
    c.setFillColorRGB(DOCTEUR_MASK_COLOR_R, DOCTEUR_MASK_COLOR_G, DOCTEUR_MASK_COLOR_B)
    c.setFillAlpha(DOCTEUR_MASK_COLOR_A)
    c.rect(mask_x, mask_y, mask_w, mask_h, fill=1, stroke=0)
    c.restoreState()
    print(f"🟪 Masque docteur (rose alpha) : x={mask_x:.1f}, y={mask_y:.1f}, w={mask_w:.1f}, h={mask_h:.1f}")
    
    # === POSITION INDÉPENDANTE DU LOGO (avec conservation des proportions) ===
    # Détermine la taille du logo à l'intérieur d'un cadre (max largeur/hauteur)
    logo_zone_start_x = page_width * LOGO_POSITION_X_RATIO
    logo_zone_width = page_width - logo_zone_start_x - ZONE_MARGE_DROITE

    # Limites de taille autorisées pour le logo (supporte agrandissement)
    max_logo_w = min(LOGO_WIDTH * LOGO_SCALE, logo_zone_width)
    max_logo_h = LOGO_HEIGHT_DANS_RECT * LOGO_SCALE

    # Récupérer la taille d'origine du logo et calculer un redimensionnement qui conserve le ratio
    try:
        _img = ImageReader(LOGO_PATH)
        orig_w, orig_h = _img.getSize()
        # Eviter division par zéro
        if orig_w <= 0 or orig_h <= 0:
            raise ValueError("Logo size invalid")
        scale = min(max_logo_w / orig_w, max_logo_h / orig_h)
        logo_width_dans_rect = orig_w * scale
        logo_height_dans_rect = orig_h * scale
    except Exception:
        # Fallback: utilise les dimensions max si la lecture échoue
        logo_width_dans_rect = max_logo_w
        logo_height_dans_rect = max_logo_h

    # Logo centré horizontalement dans sa zone, même si sa largeur change
    logo_x = logo_zone_start_x + (logo_zone_width - logo_width_dans_rect) / 2
    logo_y = page_height - LOGO_POSITION_Y_OFFSET
    
    # === APPEL DES FONCTIONS SÉPARÉES (positions indépendantes) ===
    add_docteur_text(c, docteur_x, docteur_y, docteur_nom)
    add_medilec_logo(c, logo_x, logo_y, logo_width_dans_rect, logo_height_dans_rect)
    
    c.save()
    packet.seek(0)
    return packet


def add_docteur_text(c, docteur_x, docteur_y, docteur_nom):
    """
    👨‍⚕️ FONCTION SÉPARÉE - Ajoute le texte du docteur sur le calque
    
    Args:
        c: Canvas reportlab
        docteur_x: Position X du texte
        docteur_y: Position Y du texte
        docteur_nom: Nom du docteur à afficher
    """
    if docteur_nom and str(docteur_nom).strip() and str(docteur_nom).strip().lower() != 'nan':
        c.setFillColorRGB(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B)  # Texte noir
        c.setFont(DOCTEUR_FONT_NAME, DOCTEUR_FONT_SIZE)  # Police du docteur
        docteur_text = f"{DOCTEUR_PREFIX}{str(docteur_nom).strip()}"
        c.drawString(docteur_x, docteur_y, docteur_text)
        print(f"👨‍⚕️ Docteur: '{docteur_text}' à x={docteur_x:.1f}, y={docteur_y:.1f}")


def add_medilec_logo(c, logo_x, logo_y, logo_width, logo_height):
    """
    🏥 FONCTION SÉPARÉE - Ajoute le logo Medilec sur le calque
    
    Args:
        c: Canvas reportlab
        logo_x: Position X du logo
        logo_y: Position Y du logo
        logo_width: Largeur du logo
        logo_height: Hauteur du logo
    """
    img_reader = ImageReader(LOGO_PATH)
    # preserveAspectRatio=True pour éviter l'écrasement du logo
    c.drawImage(img_reader, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True)
    print(f"📋 Logo: x={logo_x:.1f}, y={logo_y:.1f} (taille: {logo_width:.0f}x{logo_height:.0f}) — proportions conservées")


def anonymize_pdf(pdf_path, nom, prenom, docteur_nom, output_path):
    """🧾 Ouvre le PDF, applique les calques (remplacement + logo), et enregistre la version modifiée."""
    full_name = f"{nom} {prenom}"
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            base_page = reader.pages[i]
            
            # === TRAITEMENT LOCAL 1 & 2 - Remplacement des numéros patients (CONSERVÉ) ===
            items = assign_replacements_for_page(page, full_name, nom, prenom)
            if items:
                overlay_stream = create_overlay(page.width, page.height, items)
                overlay_pdf = PdfReader(overlay_stream)
                base_page.merge_page(overlay_pdf.pages[0])
            
            # === TRAITEMENT LOCAL 3 - Ajout logo Medilec + docteur (NOUVEAU) ===
            # Seulement sur la première page pour éviter la redondance
            if i == 0:
                medilec_stream = create_medilec_overlay(page.width, page.height, docteur_nom)
                medilec_pdf = PdfReader(medilec_stream)
                base_page.merge_page(medilec_pdf.pages[0])
                print(f"🏥 Traitement local 3 appliqué: Logo + Dr. {docteur_nom}")
            
            writer.add_page(base_page)

    with open(output_path, "wb") as f:
        writer.write(f)

def run_replace_from_gui(excel_path, pdf_path, output_path=None):
    """
    Fonction appelée depuis l'interface graphique.
    Remplace le numéro patient par Nom + Prénom + ajoute logo Medilec + docteur.
    Si output_path n'est pas fourni, utilise le nom d'origine avec OUTPUT_SUFFIX.
    """
    df = pd.read_excel(excel_path, sheet_name=EXCEL_SHEET_NAME)
    df.columns = [col.strip() for col in df.columns]
    df[COLONNE_ID] = df[COLONNE_ID].astype(str).str.replace(r"[\s\-]", "", regex=True)

    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    numero = extract_patient_number(text)

    if not numero:
        raise ValueError("Aucun numéro patient trouvé dans le PDF")

    row = df[df[COLONNE_ID] == numero]
    if row.empty:
        raise ValueError(f"Pas de correspondance trouvée pour {numero}")

    nom = str(row[COLONNE_NOM].values[0])
    prenom = str(row[COLONNE_PRENOM].values[0])
    
    # === NOUVEAU - Récupération du docteur (Traitement local 3) ===
    docteur_nom = None
    if COLONNE_DOCTEUR in df.columns:
        docteur_val = row[COLONNE_DOCTEUR].values[0] if not row[COLONNE_DOCTEUR].empty else None
        if docteur_val and str(docteur_val).strip() and str(docteur_val).strip().lower() != 'nan':
            docteur_nom = str(docteur_val).strip()
    
    print(f"✅ {numero} → {nom} {prenom}")
    if docteur_nom:
        print(f"🏥 Docteur: {docteur_nom}")
    else:
        print("⚠️ Pas de docteur assigné pour ce patient")

    # === Génération automatique du nom de fichier avec suffixe ===
    if output_path is None:
        # Extraire le dossier et le nom de base du PDF d'entrée
        pdf_dir = os.path.dirname(pdf_path)
        pdf_basename = os.path.basename(pdf_path)
        # Séparer nom et extension
        name_without_ext, ext = os.path.splitext(pdf_basename)
        # Ajouter le suffixe
        output_path = os.path.join(pdf_dir, f"{name_without_ext}{OUTPUT_SUFFIX}{ext}")

    # Appel de la fonction modifiée avec le paramètre docteur
    anonymize_pdf(pdf_path, nom, prenom, docteur_nom, output_path)
    return f"✅ Fichier modifié enregistré : {output_path}"


def process_all_pdfs_in_folder(excel_path, pdf_folder):
    """
    📁 Traite automatiquement tous les fichiers PDF d'un dossier.
    
    Args:
        excel_path: Chemin vers le fichier Excel contenant les données patients
        pdf_folder: Chemin vers le dossier contenant les PDFs à traiter
        
    Returns:
        dict: Résumé du traitement (succès, erreurs)
    """
    print(f"📂 Traitement du dossier: {pdf_folder}")
    print(f"📊 Fichier Excel: {excel_path}")
    print("=" * 80)
    
    # Vérifier que le dossier existe
    if not os.path.exists(pdf_folder):
        raise ValueError(f"Le dossier {pdf_folder} n'existe pas")
    
    if not os.path.exists(excel_path):
        raise ValueError(f"Le fichier Excel {excel_path} n'existe pas")
    
    # Récupérer tous les fichiers PDF du dossier (sauf ceux déjà anonymisés)
    pdf_files = [
        f for f in os.listdir(pdf_folder)
        if f.lower().endswith('.pdf') and OUTPUT_SUFFIX not in f
    ]
    
    if not pdf_files:
        print("⚠️ Aucun fichier PDF à traiter dans ce dossier")
        return {"success": 0, "errors": 0, "skipped": 0}
    
    print(f"📋 {len(pdf_files)} fichier(s) PDF trouvé(s)\n")
    
    success_count = 0
    error_count = 0
    results = []
    
    for i, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"\n[{i}/{len(pdf_files)}] 🔄 Traitement de: {pdf_file}")
        print("-" * 80)
        
        try:
            result = run_replace_from_gui(excel_path, pdf_path)
            print(result)
            success_count += 1
            results.append({"file": pdf_file, "status": "success"})
        except Exception as e:
            print(f"❌ Erreur lors du traitement de {pdf_file}: {e}")
            error_count += 1
            results.append({"file": pdf_file, "status": "error", "error": str(e)})
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DU TRAITEMENT")
    print("=" * 80)
    print(f"✅ Fichiers traités avec succès: {success_count}")
    print(f"❌ Erreurs: {error_count}")
    print(f"📁 Total: {len(pdf_files)}")
    
    if error_count > 0:
        print("\n⚠️ Fichiers en erreur:")
        for r in results:
            if r["status"] == "error":
                print(f"  - {r['file']}: {r.get('error', 'Erreur inconnue')}")
    
    return {
        "success": success_count,
        "errors": error_count,
        "total": len(pdf_files),
        "details": results
    }


# --- si lancé en direct depuis le terminal, on garde l'ancien comportement ---
if __name__ == "__main__":
    print("🏥 TRAITEMENT AUTOMATIQUE DE TOUS LES PDFs")
    print("=" * 80)
    
    # Utiliser les chemins par défaut définis en haut du fichier
    try:
        process_all_pdfs_in_folder(EXCEL_PATH, PDF_FOLDER_PATH)
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()


# --- si lancé en direct depuis le terminal, on garde l’ancien comportement ---
if __name__ == "__main__":
    print("Ce script est destiné à être utilisé via app_gui.py")
