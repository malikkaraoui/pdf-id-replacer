# 🧩 PDF ID Replacer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/install-%20pip%20install%20--r%20requirements.txt-success)
![By Malik Karaoui](https://img.shields.io/badge/By-Malik%20Karaoui-10B981)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


Script Python permettant de remplacer automatiquement les numéros patients (ex: `10002530`) dans des rapports PDF par leur **Nom** et **Prénom**, à partir d’un fichier **Excel** de correspondance.

---

## 🚀 Fonctionnalités

✅ Remplace les ID patients (comme `1000-2530` ou `1000 2530` ou `10002530`) par le **nom et prénom**  
✅ Masque automatiquement les anciens identifiants (zone blanche propre)  
✅ Gère les fichiers **PDF multipages**  
✅ Lecture automatique d’un fichier **Excel** (noms / prénoms / ID unique)  
✅ Compatible **macOS**, **Windows**, et **Linux**

---

## 🧠 Exemple de fonctionnement

| Avant | Après |
|-------|-------|
| `10002530 10002530` | `Simon Ethann` |
| `Nom : 10002530` | `Nom : Simon` |
| `Prénom : 10002530` | `Prénom : Ethann` |

---

## 📂 Structure du projet

PDF modif/
├── replace_patient_id.py ← Script principal
├── patients.xlsx ← Fichier Excel avec correspondance
└── PDF/
├── Exemple-1.pdf
├── Exemple-2.pdf
└── ...

---

## ⚙️ Installation (Windows)

### Étape 1. Installer **Python 3**
1. Télécharger depuis [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Cocher ✅ **“Add Python to PATH”** à l’installation  
3. Ouvrir une fenêtre **Invite de commandes (CMD)**  
4. Vérifier l’installation :
   ```bash
   python --version
   
(doit afficher Python 3.x.x)

---

### Étape 2. Installer les dépendances
Placez-vous dans le dossier du script :

cd "C:\Users\<VotreNom>\Documents\PDF modif"

pip install pdfplumber reportlab pypdf pandas openpyxl

---

### Étape 3. Lancer le script
Toujours dans le dossier :

python replace_patient_id.py

Le script analysera les PDF présents dans le dossier PDF/, puis créera les versions modifiées (suffixe -NEW.pdf).

---

### 🧾 Personnalisation

Dans le script replace_patient_id.py, ces lignes définissent les chemins (ex pour MacOS):

EXCEL_PATH = r"/Users/malik/Documents/PDF modif/patients.xlsx"
PDF_FOLDER = r"/Users/malik/Documents/PDF modif/PDF"

👉 Pour l’utiliser sous Windows, il faut :
soit recréer la même structure (Documents\PDF modif\PDF)
soit modifier ces deux chemins pour correspondre à son environnement.

---

### 📋 Exemple de fichier Excel (patients.xlsx)

| ID_unique | Nom     | Prénom |
| --------- | ------- | ------ |
| 10002530  | Simon   | Ethann |
| 10002527  | Richard | Lucas  |

---

### 💡 Astuce

Pour vérifier rapidement si tout fonctionne :

Placer un seul fichier PDF dans PDF/

Lancer le script

Vérifier la création du fichier *-NEW.pdf avec les champs remplacés

---

👨‍💻 Auteur
Malik Karaoui
Projet open-source – pour automatiser l’anonymisation et le renommage de rapports médicaux PDF.
GitHub : @malikkaraoui

---

🧱 Licence
Ce projet est sous licence MIT — libre d’utilisation et de modification.

---
