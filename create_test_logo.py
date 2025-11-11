#!/usr/bin/env python3
"""
Script pour créer un logo Medilec de test
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_medilec_logo():
    # Créer une image 200x60 avec fond blanc
    width, height = 200, 60
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Dessiner un rectangle bleu pour simuler un logo
    draw.rectangle([10, 10, width-10, height-10], fill='#0066CC', outline='#003399', width=2)
    
    # Ajouter le texte "MEDILEC"
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        # Police par défaut si Arial n'est pas trouvée
        font = ImageFont.load_default()
    
    # Calculer la position pour centrer le texte
    text = "MEDILEC"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Dessiner le texte en blanc
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    # Sauvegarder le logo
    logo_path = "/Users/malik/Documents/PDF modif/Medilec-Logo.jpg"
    img.save(logo_path, 'JPEG', quality=95)
    print(f"✅ Logo créé: {logo_path}")
    return logo_path

if __name__ == "__main__":
    create_medilec_logo()