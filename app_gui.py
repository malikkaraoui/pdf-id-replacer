#!/usr/bin/env python3
"""
app_gui.py - Interface graphique pour PDF ID Replacer

Interface simple utilisant tkinter (inclus avec Python) pour remplacer
automatiquement les numéros patients par Nom + Prénom.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from replace_patient_id import run_replace_from_gui

class PDFReplacerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF ID Replacer")
        self.root.geometry("600x500")
        
        # Variables
        self.excel_path = tk.StringVar()
        self.pdf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Valeurs par défaut
        base_dir = "/Users/malik/Documents/PDF modif"
        self.excel_path.set(os.path.join(base_dir, "patients.xlsx"))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration des poids
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titre
        title = ttk.Label(main_frame, text="PDF ID Replacer", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Fichier Excel
        ttk.Label(main_frame, text="Fichier Excel patients:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.excel_path, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Parcourir", command=self.browse_excel).grid(row=1, column=2, pady=5)
        
        # Fichier PDF
        ttk.Label(main_frame, text="Fichier PDF à traiter:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.pdf_path, width=40).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Parcourir", command=self.browse_pdf).grid(row=2, column=2, pady=5)
        
        # Fichier de sortie
        ttk.Label(main_frame, text="PDF de sortie:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=40).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(main_frame, text="Parcourir", command=self.browse_output).grid(row=3, column=2, pady=5)
        
        # Boutons d'action
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Traiter le PDF", command=self.process_pdf, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Analyser PDF", command=self.analyze_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Quitter", command=self.root.quit).pack(side=tk.LEFT, padx=5)
        
        # Zone de log
        ttk.Label(main_frame, text="Logs:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, width=70, height=15)
        self.log_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Configuration du redimensionnement
        main_frame.rowconfigure(6, weight=1)
        
    def log(self, message):
        """Ajoute un message au log."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def browse_excel(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner le fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.excel_path.set(filename)
            
    def browse_pdf(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner le fichier PDF",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            # Auto-générer le nom du fichier de sortie
            if filename:
                dir_path = os.path.dirname(filename)
                base_name = os.path.splitext(os.path.basename(filename))[0]
                output_name = f"MODIFIE_{base_name}.pdf"
                self.output_path.set(os.path.join(dir_path, output_name))
                
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder le PDF modifié",
            defaultextension=".pdf",
            filetypes=[("Fichiers PDF", "*.pdf"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
            
    def analyze_pdf(self):
        """Analyse le PDF pour détecter le numéro patient."""
        pdf_path = self.pdf_path.get()
        
        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF valide.")
            return
            
        try:
            self.log("🔍 Analyse du PDF en cours...")
            
            import pdfplumber
            import re
            import pandas as pd
            
            def extract_patient_number(text: str):
                match = re.search(r"1000[\s\-]?\d{4}", text)
                return re.sub(r"[\s\-]", "", match.group()) if match else None
            
            with pdfplumber.open(pdf_path) as pdf:
                self.log(f"📄 PDF ouvert: {os.path.basename(pdf_path)}")
                self.log(f"📊 Nombre de pages: {len(pdf.pages)}")
                
                # Extraire le texte de la première page
                page_text = pdf.pages[0].extract_text() or ""
                numero_patient = extract_patient_number(page_text)
                
                if numero_patient:
                    self.log(f"🎯 Numéro patient détecté: {numero_patient}")
                    
                    # Vérifier dans Excel
                    excel_path = self.excel_path.get()
                    if os.path.exists(excel_path):
                        df = pd.read_excel(excel_path, sheet_name="feuille1")
                        df['ID_unique'] = df['ID_unique'].astype(str).str.replace(r"[\s\-]", "", regex=True)
                        
                        row = df[df['ID_unique'] == numero_patient]
                        if not row.empty:
                            nom = row['Nom'].values[0]
                            prenom = row['Prénom'].values[0]
                            self.log(f"✅ Correspondance trouvée: {nom} {prenom}")
                        else:
                            self.log("❌ Aucune correspondance trouvée dans Excel")
                    else:
                        self.log("❌ Fichier Excel non trouvé")
                else:
                    self.log("❌ Aucun numéro patient détecté")
                    
        except Exception as e:
            self.log(f"❌ Erreur lors de l'analyse: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse:\n{e}")
            
    def process_pdf(self):
        """Traite le PDF en remplaçant les numéros par les noms."""
        excel_path = self.excel_path.get()
        pdf_path = self.pdf_path.get()
        output_path = self.output_path.get()
        
        # Validation
        if not excel_path or not os.path.exists(excel_path):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier Excel valide.")
            return
            
        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier PDF valide.")
            return
            
        if not output_path:
            messagebox.showerror("Erreur", "Veuillez spécifier un fichier de sortie.")
            return
            
        try:
            self.log("🚀 Traitement en cours...")
            self.log(f"📂 PDF source: {os.path.basename(pdf_path)}")
            self.log(f"📊 Excel: {os.path.basename(excel_path)}")
            self.log(f"📄 Sortie: {os.path.basename(output_path)}")
            
            # Appel de la fonction de traitement
            result = run_replace_from_gui(excel_path, pdf_path, output_path)
            self.log(result)
            
            # Vérifier que le fichier a été créé
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.log(f"📊 Taille du fichier: {file_size:,} bytes")
                messagebox.showinfo("Succès", f"PDF traité avec succès!\n\nFichier créé: {os.path.basename(output_path)}")
            else:
                messagebox.showerror("Erreur", "Le fichier de sortie n'a pas été créé.")
                
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du traitement:\n{e}")

def main():
    root = tk.Tk()
    app = PDFReplacerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
