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

# ============================
# ==== PARAMÈTRES À MODIFIER ====
# ============================

EXCEL_PATH = r"/Users/malik/Documents/PDF modif/patients.xlsx"  # Chemin vers le fichier Excel
SHEET_NAME = "feuille1"  # Nom de la feuille
COL_NUMERO = "ID_unique"  # Nom de la colonne des IDs
COL_NOM = "Nom"           # Colonne du nom
COL_PRENOM = "Prénom"     # Colonne du prénom

PDF_FOLDER = r"/Users/Malik/Documents/PDF modif/PDF"  # Dossier contenant les PDF
REDACT_COLOR = (1, 1, 1)  # Couleur du masque (blanc)
HEADER_Y_THRESHOLD = 0.25  # Seuil (en %) de hauteur de page considérée comme "entête"

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
        c.setFillColorRGB(*REDACT_COLOR)
        c.rect(x0, y0, w, h, fill=1, stroke=0)

        # --- Choix de la police ---
        font_name = "Helvetica-Bold" if is_header else "Helvetica"

        # --- Ajustement automatique de la taille ---
        base_size = max(7, int(h * 0.8))
        c.setFillColorRGB(0, 0, 0)
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


def anonymize_pdf(pdf_path, nom, prenom, output_path):
    """🧾 Ouvre le PDF, applique le calque, et enregistre la version modifiée."""
    full_name = f"{nom} {prenom}"
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            base_page = reader.pages[i]
            items = assign_replacements_for_page(page, full_name, nom, prenom)
            if items:
                overlay_stream = create_overlay(page.width, page.height, items)
                overlay_pdf = PdfReader(overlay_stream)
                base_page.merge_page(overlay_pdf.pages[0])
            writer.add_page(base_page)

    with open(output_path, "wb") as f:
        writer.write(f)


def main():
    """🚀 Point d'entrée principal : lecture Excel + traitement des PDF."""
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    df.columns = [col.strip() for col in df.columns]
    df[COL_NUMERO] = df[COL_NUMERO].astype(str).str.replace(r"[\s\-]", "", regex=True)

    print(f"Excel détecté et chargé ({len(df)} entrées).")
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    for pdf_name in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, pdf_name)
        print(f"\nAnalyse du fichier PDF : {pdf_name}")

        with pdfplumber.open(pdf_path) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)

        numero = extract_patient_number(text)
        if not numero:
            print("⚠️ Aucun numéro patient trouvé.")
            continue

        row = df[df[COL_NUMERO] == numero]
        if row.empty:
            print(f"⚠️ Pas de correspondance trouvée pour {numero}")
            continue

        nom = str(row[COL_NOM].values[0])
        prenom = str(row[COL_PRENOM].values[0])
        print(f"✅ Correspondance : {numero} → {nom} {prenom}")

        base_name, ext = os.path.splitext(pdf_name)
        output_pdf = os.path.join(PDF_FOLDER, f"{base_name}-NEW{ext}")

        anonymize_pdf(pdf_path, nom, prenom, output_pdf)
        print(f"💾 Fichier modifié enregistré : {output_pdf}")

    print("\n🎉 Traitement terminé avec succès !")


if __name__ == "__main__":
    main()
