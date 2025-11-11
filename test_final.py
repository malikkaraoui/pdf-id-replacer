#!/usr/bin/env python3
"""
Test simple pour la correction zone blanche
"""
import sys
sys.path.append("/Users/malik/Documents/PDF modif")

from replace_patient_id import run_replace_from_gui
import os

# Paramètres
excel_path = "/Users/malik/Documents/PDF modif/patients.xlsx"
pdf_path = "/Users/malik/Documents/PDF modif/PDF/Exemple-1-PDF1.4-02-03-2025-_10002530 10002530_27022025.pdf"
output_path = "/Users/malik/Documents/PDF modif/PDF/FINAL_ZONE_BLANCHE.pdf"

print("🎯 Test final - Zone blanche + Logo + Docteur")
print(f"📂 Source: {os.path.basename(pdf_path)}")
print(f"📄 Sortie: {os.path.basename(output_path)}")
print()

try:
    result = run_replace_from_gui(excel_path, pdf_path, output_path)
    print(result)
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"📊 Fichier final créé: {size:,} bytes")
        print("✅ SUCCÈS! Vérifiez le PDF généré")
        
        # Nettoyage des anciens fichiers tests
        test_files = [
            "/Users/malik/Documents/PDF modif/PDF/TEST_AVEC_LOGO_Exemple-1.pdf",
            "/Users/malik/Documents/PDF modif/PDF/TEST_AVEC_LOGO_Exemple-2.pdf",
        ]
        for f in test_files:
            if os.path.exists(f):
                os.remove(f)
                print(f"🗑️ Supprimé: {os.path.basename(f)}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")