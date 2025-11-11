# 📋 Guide des Paramètres - PDF Modification

Ce document explique tous les paramètres configurables dans le fichier `parametres.py`.

---

## 📊 Paramètres Excel

### `EXCEL_SHEET_NAME`
- **Valeur actuelle** : `"feuille1"`
- **Description** : Nom de la feuille Excel contenant les données patients
- **Important** : Respecter la casse exacte (majuscules/minuscules)

### `COLONNE_ID`
- **Valeur actuelle** : `"ID_unique"`
- **Description** : Nom de la colonne contenant l'identifiant patient (ex: 10002530)

### `COLONNE_NOM`
- **Valeur actuelle** : `"Nom"`
- **Description** : Nom de la colonne contenant le nom de famille

### `COLONNE_PRENOM`
- **Valeur actuelle** : `"Prénom"`
- **Description** : Nom de la colonne contenant le prénom

### `COLONNE_DOCTEUR`
- **Valeur actuelle** : `"docteur_nom"`
- **Description** : Nom de la colonne contenant le nom du docteur assigné au patient

---

## 🏥 Paramètres Logo Medilec

### `LOGO_PATH`
- **Valeur actuelle** : `"Medilec-Logo.png"`
- **Description** : Chemin du fichier logo (relatif au dossier du projet)
- **Format supporté** : PNG

### `LOGO_WIDTH` et `LOGO_HEIGHT`
- **Valeurs actuelles** : `180` x `54` pixels
- **Description** : Dimensions originales du logo

### `LOGO_POSITION_X_RATIO`
- **Valeur actuelle** : `0.52` (52% de la largeur)
- **Description** : Position horizontale du logo en pourcentage de la largeur de page
- **Plage** : Entre 0.0 (bord gauche) et 1.0 (bord droit)
- **⚠️ INDÉPENDANT** : Cette position n'affecte PAS le texte docteur

### `LOGO_POSITION_Y_OFFSET`
- **Valeur actuelle** : `142` pixels
- **Description** : Distance depuis le haut de la page jusqu'au logo
- **Effet** : Plus la valeur est grande, plus le logo monte
- **⚠️ INDÉPENDANT** : Cette position n'affecte PAS le texte docteur

### `LOGO_HEIGHT_DANS_RECT`
- **Valeur actuelle** : `25` pixels
- **Description** : Hauteur du logo après redimensionnement

---

## 👨‍⚕️ Paramètres Texte Docteur

### `DOCTEUR_FONT_SIZE`
- **Valeur actuelle** : `12`
- **Description** : Taille de la police pour le nom du docteur
- **Unité** : Points typographiques

### `DOCTEUR_FONT_NAME`
- **Valeur actuelle** : `"Helvetica"`
- **Description** : Police utilisée pour le texte docteur
- **Options** : `"Helvetica"`, `"Helvetica-Bold"`, `"Times-Roman"`, etc.

### `DOCTEUR_PREFIX`
- **Valeur actuelle** : `"Docteur : "`
- **Description** : Préfixe affiché avant le nom du docteur
- **Exemple** : Avec `"Dr. "`, affichera "Dr. Paulo"

### `DOCTEUR_POSITION_X_RATIO`
- **Valeur actuelle** : `0.52` (52% de la largeur)
- **Description** : Position horizontale du texte docteur en pourcentage de la largeur de page
- **Plage** : Entre 0.0 (bord gauche) et 1.0 (bord droit)
- **⚠️ INDÉPENDANT** : Cette position n'affecte PAS le logo

### `DOCTEUR_POSITION_Y_OFFSET`
- **Valeur actuelle** : `127` pixels
- **Description** : Distance depuis le haut de la page jusqu'au texte docteur
- **Effet** : Plus la valeur est grande, plus le texte monte
- **⚠️ INDÉPENDANT** : Cette position n'affecte PAS le logo

### `DOCTEUR_MARGE_GAUCHE`
- **Valeur actuelle** : `3` pixels
- **Description** : Marge gauche ajoutée au texte docteur

---

## 📐 Paramètres Zone de Masquage

### `ZONE_POSITION_X_RATIO`
- **Valeur actuelle** : `0.52`
- **Description** : Position horizontale de la zone de masquage blanc

### `ZONE_POSITION_Y_OFFSET`
- **Valeur actuelle** : `142` pixels
- **Description** : Distance depuis le haut de la page jusqu'à la zone

### `ZONE_HEIGHT`
- **Valeur actuelle** : `50` pixels
- **Description** : Hauteur de la zone rectangulaire de masquage
- **Important** : Doit être assez grande pour couvrir le logo et le docteur

### `ZONE_MARGE_DROITE`
- **Valeur actuelle** : `15` pixels
- **Description** : Marge entre la zone et le bord droit du PDF

---

## 📄 Paramètres Traitement Local 1 & 2 (Remplacement ID)

### `LABEL_TOLERANCE_X` et `LABEL_TOLERANCE_Y`
- **Valeurs actuelles** : `80` et `15` pixels
- **Description** : Distance maximale pour détecter les étiquettes "Nom:" et "Prénom:"
- **Ajustement** : Augmenter si les étiquettes ne sont pas détectées

### `ID_MASK_MARGIN_X` et `ID_MASK_MARGIN_Y`
- **Valeurs actuelles** : `2` pixels chacune
- **Description** : Marge autour du masquage blanc des IDs
- **Effet** : Plus grande = zone blanche plus large

### `REPLACEMENT_FONT_SIZE`
- **Valeur actuelle** : `10`
- **Description** : Taille de police pour les remplacements de texte

### `REPLACEMENT_FONT_NAME`
- **Valeur actuelle** : `"Helvetica"`
- **Description** : Police pour les textes de remplacement

---

## 🔍 Paramètres Détection Patient

### `PATIENT_ID_REGEX`
- **Valeur actuelle** : `r'1000[\s\-]?\d{4}'`
- **Description** : Expression régulière pour détecter les numéros patients
- **Format détecté** : 
  - `10002530` (sans séparateur)
  - `1000-2530` (avec tiret)
  - `1000 2530` (avec espace)

---

## 🎨 Paramètres Couleurs

### `MASK_COLOR_R`, `MASK_COLOR_G`, `MASK_COLOR_B`
- **Valeurs actuelles** : `1.0`, `1.0`, `1.0` (blanc)
- **Description** : Couleur du masque de remplacement (RGB)
- **Plage** : Entre 0.0 (noir) et 1.0 (blanc)

### `TEXT_COLOR_R`, `TEXT_COLOR_G`, `TEXT_COLOR_B`
- **Valeurs actuelles** : `0.0`, `0.0`, `0.0` (noir)
- **Description** : Couleur du texte de remplacement (RGB)

---

## 📁 Paramètres Fichiers

### `OUTPUT_SUFFIX`
- **Valeur actuelle** : `"_anonymisé"`
- **Description** : Suffixe ajouté aux noms de fichiers de sortie
- **Non utilisé actuellement** : Nom de sortie spécifié manuellement

### `DEFAULT_PDF_FOLDER`
- **Valeur actuelle** : `"PDF"`
- **Description** : Dossier par défaut pour les PDF (si non spécifié)

### `HEADER_Y_THRESHOLD`
- **Valeur actuelle** : `0.25` (25%)
- **Description** : Seuil de hauteur de page considérée comme "entête"
- **Effet** : Modifie la détection des zones de texte

---

## 💡 Comment Modifier les Paramètres

1. Ouvrir le fichier `parametres.py`
2. Modifier la valeur souhaitée
3. Sauvegarder le fichier
4. Relancer le script - les changements sont automatiques !

**Exemple 1** : Pour déplacer le logo plus haut :
```python
# Avant
LOGO_POSITION_Y_OFFSET = 142

# Après (plus haut)
LOGO_POSITION_Y_OFFSET = 130
```

**Exemple 2** : Pour déplacer le docteur indépendamment :
```python
# Le docteur peut être déplacé sans affecter le logo
DOCTEUR_POSITION_Y_OFFSET = 115  # Plus haut que le logo

# Le logo reste à sa position
LOGO_POSITION_Y_OFFSET = 142  # Position inchangée
```

**Exemple 3** : Pour inverser docteur/logo (logo au-dessus) :
```python
# Logo plus haut
LOGO_POSITION_Y_OFFSET = 120

# Docteur plus bas
DOCTEUR_POSITION_Y_OFFSET = 140
```

---

## 🎯 Positionnement Indépendant

**IMPORTANT** : Le docteur et le logo ont maintenant des positions **totalement indépendantes** !

- ✅ Vous pouvez déplacer le logo sans que le docteur bouge
- ✅ Vous pouvez déplacer le docteur sans que le logo bouge
- ✅ Vous pouvez même mettre le logo au-dessus du docteur si besoin
- ✅ La zone de masquage blanc est également indépendante

**Paramètres indépendants** :
- `DOCTEUR_POSITION_Y_OFFSET` → Position du texte docteur
- `LOGO_POSITION_Y_OFFSET` → Position du logo
- `ZONE_POSITION_Y_OFFSET` → Position de la zone de masquage

---

## ⚠️ Avertissements

- **Toujours sauvegarder** une copie du fichier `parametres.py` avant modifications
- **Tester** les changements sur un PDF de test avant traitement en masse
- **Respecter les types** : nombres pour les tailles, texte entre guillemets pour les noms
- **Attention à la casse** : "Feuil1" ≠ "feuil1"

---

## 🔧 Dépannage

### Le logo ne s'affiche pas
→ Vérifier que `LOGO_PATH` pointe vers le bon fichier PNG

### Le texte docteur est coupé
→ Augmenter `LOGO_ZONE_HEIGHT` et/ou `DOCTEUR_FONT_SIZE`

### Les IDs ne sont pas détectés
→ Vérifier `PATIENT_ID_REGEX` correspond au format des IDs dans vos PDFs

### Erreur "Worksheet not found"
→ Vérifier `EXCEL_SHEET_NAME` correspond exactement au nom dans Excel
