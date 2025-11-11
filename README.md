# 🧩 PDF ID Replacer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/install-%20pip%20install%20--r%20requirements.txt-success)
![By Malik Karaoui](https://img.shields.io/badge/By-Malik%20Karaoui-10B981)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


Script Python permettant de remplacer automatiquement les numéros patients (ex: `10002530`) dans des rapports PDF par leur **Nom** et **Prénom**, à partir d'un fichier **Excel** de correspondance. Le script ajoute également un **logo Medilec** et le **nom du docteur** sur chaque rapport.

---

## 🚀 Fonctionnalités

✅ Remplace les ID patients (comme `1000-2530` ou `1000 2530` ou `10002530`) par le **nom et prénom**  
✅ Masque automatiquement les anciens identifiants (zone blanche propre)  
✅ Ajoute le **logo Medilec** avec mise à l'échelle et préservation des proportions  
✅ Affiche le **nom du docteur** assigné au patient  
✅ Gère les fichiers **PDF multipages**  
✅ Lecture automatique d'un fichier **Excel** (noms / prénoms / ID unique / docteur)  
✅ **Traitement en masse** : traite automatiquement tous les PDFs d'un dossier  
✅ Compatible **macOS**, **Windows**, et **Linux**

---

## 🧠 Exemple de fonctionnement

### Avant traitement
```
Fichier PDF original:
┌─────────────────────────────────────┐
│ Rapport Médical                     │
│                                     │
│ Nom : 10002530                      │
│ Prénom : 10002530                   │
│                                     │
│ Patient : 10002530 10002530         │
│                                     │
└─────────────────────────────────────┘
```

### Après traitement
```
Fichier PDF anonymisé:
┌─────────────────────────────────────┐
│ Rapport Médical    [Logo Medilec]  │
│                    Docteur : Paulo  │
│ Nom : Simon                         │
│ Prénom : Ethan                      │
│                                     │
│ Patient : Simon Ethan               │
│                                     │
└─────────────────────────────────────┘
```

### Tableau récapitulatif

| Avant | Après |
|-------|-------|
| `10002530 10002530` | `Simon Ethan` |
| `Nom : 10002530` | `Nom : Simon` |
| `Prénom : 10002530` | `Prénom : Ethan` |
| *(zone vide en haut à droite)* | Logo Medilec + `Docteur : Paulo` |

---

## 📂 Structure du projet

```
PDF modif/
├── replace_patient_id.py      ← Script principal
├── parametres.py              ← Configuration centralisée (positions, couleurs, chemins)
├── app_gui.py                 ← Interface graphique (optionnelle)
├── patients.xlsx              ← Fichier Excel avec correspondance
├── Medilec-Logo.png           ← Logo à intégrer dans les PDFs
├── PDF/                       ← Dossier contenant les PDF à traiter
│   ├── Exemple-1.pdf
│   ├── Exemple-2.pdf
│   └── ...
└── requirements.txt           ← Dépendances Python
```

---

## ⚙️ Installation

### Étape 1. Installer **Python 3**
1. Télécharger depuis [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Cocher ✅ **"Add Python to PATH"** à l'installation  
3. Ouvrir une fenêtre **Terminal (macOS/Linux)** ou **Invite de commandes (Windows)**  
4. Vérifier l'installation :
   ```bash
   python --version
   ```
   (doit afficher Python 3.x.x)

---

### Étape 2. Installer les dépendances
Placez-vous dans le dossier du script :

```bash
cd "/chemin/vers/PDF modif"
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install pdfplumber reportlab pypdf pandas openpyxl Pillow
```

---

### Étape 3. Lancer le script

**Traitement automatique de tous les PDFs :**
```bash
python replace_patient_id.py
```

Le script analysera tous les PDF du dossier `PDF/`, puis créera les versions modifiées avec le suffixe `_anonymisé.pdf`.

**OU via l'interface graphique :**
```bash
python app_gui.py
```

---

## 🎨 Personnalisation

Tous les paramètres sont centralisés dans le fichier **`parametres.py`** :

### Chemins des fichiers
```python
PDF_FOLDER = "PDF"              # Dossier contenant les PDFs
EXCEL_FILE = "patients.xlsx"    # Fichier Excel
OUTPUT_SUFFIX = "_anonymisé"    # Suffixe ajouté aux fichiers de sortie
```

### Logo Medilec
```python
LOGO_PATH = "Medilec-Logo.png"
LOGO_SCALE = 2                  # Facteur d'agrandissement (1 = taille normale)
LOGO_POSITION_X_RATIO = 0.52    # Position horizontale (52% de la largeur)
LOGO_POSITION_Y_OFFSET = 133    # Position verticale (pixels depuis le haut)
```

### Texte Docteur
```python
DOCTEUR_FONT_SIZE = 12
DOCTEUR_POSITION_X_RATIO = 0.55
DOCTEUR_POSITION_Y_OFFSET = 58
DOCTEUR_PREFIX = "Docteur : "
```

### Couleurs et masques
```python
MASK_COLOR_R = 1.0              # Blanc (RGB)
MASK_COLOR_G = 1.0
MASK_COLOR_B = 1.0
```

---

## 📋 Format du fichier Excel (patients.xlsx)

| ID_unique | Nom     | Prénom | docteur_nom |
| --------- | ------- | ------ | ----------- |
| 10002530  | Simon   | Ethan  | Paulo       |
| 10002527  | Richard | Lucas  | Eric        |

**Colonnes requises :**
- `ID_unique` : Numéro patient (ex: 10002530)
- `Nom` : Nom de famille
- `Prénom` : Prénom
- `docteur_nom` : Nom du docteur assigné (optionnel)

---

## 💡 Exemple d'utilisation

### Traitement en masse
```bash
python replace_patient_id.py
```

**Résultat :**
```
🏥 TRAITEMENT AUTOMATIQUE DE TOUS LES PDFs
================================================================================
📂 Traitement du dossier: /Users/malik/Documents/PDF modif/PDF
📊 Fichier Excel: /Users/malik/Documents/PDF modif/patients.xlsx
================================================================================
📋 2 fichier(s) PDF trouvé(s)

[1/2] 🔄 Traitement de: Exemple-1.pdf
✅ 10002530 → Simon Ethan
🏥 Docteur: Paulo
✅ Fichier modifié enregistré : PDF/Exemple-1_anonymisé.pdf

[2/2] 🔄 Traitement de: Exemple-2.pdf
✅ 10002527 → Richard Lucas
🏥 Docteur: Eric
✅ Fichier modifié enregistré : PDF/Exemple-2_anonymisé.pdf

================================================================================
📊 RÉSUMÉ DU TRAITEMENT
================================================================================
✅ Fichiers traités avec succès: 2
❌ Erreurs: 0
📁 Total: 2
```

---

## 🏥 Fonctionnalités avancées

### Traitement Local 1 & 2 : Remplacement des IDs
- Détection intelligente des numéros patients (avec ou sans séparateurs)
- Masquage blanc des anciens identifiants
- Remplacement par nom/prénom selon le contexte (entête ou corps du document)

### Traitement Local 3 : Logo + Docteur
- **Logo Medilec** : redimensionné avec préservation des proportions
- **Nom du docteur** : positionné indépendamment avec masque blanc
- **Positions configurables** : chaque élément peut être placé précisément

### Architecture modulaire
- `parametres.py` : tous les paramètres modifiables
- `replace_patient_id.py` : logique métier
- `app_gui.py` : interface graphique (Tkinter)

---

## 🔧 Dépendances

- **pdfplumber** : extraction de texte des PDFs
- **reportlab** : génération de calques PDF
- **pypdf** : fusion de pages PDF
- **pandas** : lecture des fichiers Excel
- **openpyxl** : support Excel (.xlsx)
- **Pillow** : manipulation d'images (logo)

---

## 👨‍💻 Auteur

**Malik Karaoui**  
Projet open-source – pour automatiser l'anonymisation et le renommage de rapports médicaux PDF.  
GitHub : [@malikkaraoui](https://github.com/malikkaraoui)

---

## 🧱 Licence

Ce projet est sous licence MIT — libre d'utilisation et de modification.

---

## 📝 Changelog

### v2.0 - Ajout Logo & Docteur
- ✅ Ajout automatique du logo Medilec avec mise à l'échelle
- ✅ Affichage du nom du docteur assigné
- ✅ Positions indépendantes et configurables pour logo et docteur
- ✅ Traitement en masse de tous les PDFs d'un dossier
- ✅ Centralisation des paramètres dans `parametres.py`
- ✅ Génération automatique du nom de fichier avec suffixe `_anonymisé`

### v1.0 - Version initiale
- ✅ Remplacement des IDs patients par nom/prénom
- ✅ Lecture Excel et correspondance automatique
- ✅ Support PDF multipage