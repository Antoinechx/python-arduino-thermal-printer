import tkinter as tk
from datetime import datetime

# Définir les icônes Unicode pour l'importance
importance_icons = {
    "Normal": "\u25CF",    # ●
    "Important": "\u26A0", # ⚠
    "Urgent": "\u2716"     # ✖
}

class TicketApp:
    def __init__(self, root):
        self.root = root
        root.title("Créateur de Ticket Dynamique")

        # Polices
        self.titre_font = ("Helvetica", 16, "bold")
        self.section_font = ("Helvetica", 14, "bold")
        self.tache_font = ("Courier", 12)
        self.icon_font = ("Helvetica", 48, "bold")  # super gros pour l'icône

        # Nom du projet
        tk.Label(root, text="Nom du projet", font=self.titre_font).grid(row=0, column=0, sticky="w")
        self.projet_entry = tk.Entry(root, width=30, font=self.titre_font, justify="center")
        self.projet_entry.grid(row=0, column=1, sticky="w")

        # Frame pour les sections
        self.sections = []
        self.sections_frame = tk.Frame(root)
        self.sections_frame.grid(row=1, column=0, columnspan=2, sticky="w")
        self.ajouter_section()

        # Boutons gérer sections
        tk.Button(root, text="Ajouter section", command=self.ajouter_section).grid(row=2, column=0)
        tk.Button(root, text="Supprimer section", command=self.supprimer_section).grid(row=2, column=1)

        # Commentaire
        tk.Label(root, text="Commentaire").grid(row=3, column=0, sticky="w")
        self.comment_entry = tk.Entry(root, width=30)
        self.comment_entry.grid(row=3, column=1, sticky="w")

        # Choix d'importance
        self.importance_var = tk.StringVar(value="Normal")
        tk.Label(root, text="Importance").grid(row=4, column=0, sticky="w")
        tk.OptionMenu(root, self.importance_var, "Normal", "Important", "Urgent").grid(row=4, column=1, sticky="w")

        # Bouton générer ticket
        tk.Button(root, text="CREATE", command=self.generer_ticket).grid(row=5, column=0, columnspan=2)

    # --- Sections et tâches ---
    def ajouter_section(self):
        section_frame = tk.Frame(self.sections_frame, bd=2, relief="groove", padx=5, pady=5)
        row = len(self.sections)
        section_frame.grid(row=row, column=0, pady=5, sticky="w")

        tk.Label(section_frame, text="Section", font=self.section_font).grid(row=0, column=0, sticky="w")
        titre_entry = tk.Entry(section_frame, width=20, font=self.section_font, justify="center")
        titre_entry.grid(row=0, column=1, sticky="w")

        section = {"titre": titre_entry, "taches": [], "frame": section_frame}

        tk.Button(section_frame, text="+", command=lambda s=section: self.ajouter_tache(s)).grid(row=0, column=2)
        tk.Button(section_frame, text="-", command=lambda s=section: self.supprimer_tache(s)).grid(row=0, column=3)

        for _ in range(3):
            self.ajouter_tache(section)

        self.sections.append(section)

    def supprimer_section(self):
        if self.sections:
            s = self.sections.pop()
            s["frame"].destroy()

    def ajouter_tache(self, section):
        i = len(section["taches"])
        t_label = tk.Label(section["frame"], text=f"Tâche {i+1}", font=self.tache_font)
        t_entry = tk.Entry(section["frame"], width=30, font=self.tache_font)
        section["taches"].append((t_label, t_entry))
        self.repositionner_taches(section)

    def supprimer_tache(self, section):
        if section["taches"]:
            t_label, t_entry = section["taches"].pop()
            t_label.destroy()
            t_entry.destroy()
            self.repositionner_taches(section)

    def repositionner_taches(self, section):
        for idx, (label, entry) in enumerate(section["taches"]):
            label.config(text=f"Tâche {idx+1}")
            label.grid(row=idx+1, column=0, sticky="w")
            entry.grid(row=idx+1, column=1, sticky="w")

    # --- Générer ticket ---
    def generer_ticket(self):
        projet = self.projet_entry.get()
        maintenant = datetime.now().strftime("%d %b %y %Hh%M")
        largeur = 32

        # Nouvelle fenêtre pour prévisualisation
        preview = tk.Toplevel(self.root)
        preview.title("Aperçu du ticket")
        text_widget = tk.Text(preview, width=largeur+4, height=25)
        text_widget.pack(padx=10, pady=10)

        # Définir les polices et tags
        text_widget.tag_configure("titre", font=self.titre_font, justify="center")
        text_widget.tag_configure("section", font=self.section_font, justify="center")
        text_widget.tag_configure("normal", font=self.tache_font)
        text_widget.tag_configure("icon", font=self.icon_font, justify="center")

        # Projet et date
        text_widget.insert("end", f"{projet}\n", "titre")
        text_widget.insert("end", f"{maintenant}\n", "normal")
        text_widget.insert("end", "\u2500"*largeur + "\n", "normal")  # ligne continue

        # Sections et tâches
        for sec in self.sections:
            titre = sec["titre"].get().strip()
            if titre:
                text_widget.insert("end", f"{titre}\n", "section")
            for _, t_entry in sec["taches"]:
                t_val = t_entry.get().strip()
                if t_val:
                    text_widget.insert("end", f"\u2610 {t_val}\n", "normal")  # case Unicode
            text_widget.insert("end", "\u2500"*largeur + "\n", "normal")  # ligne continue après section

        # Commentaire
        commentaire = self.comment_entry.get().strip()
        if commentaire:
            text_widget.insert("end", f"Commentaire: {commentaire}\n", "normal")
            text_widget.insert("end", "\u2500"*largeur + "\n", "normal")

        # Icône d'importance en super gros
        icon = importance_icons.get(self.importance_var.get(), "")
        text_widget.insert("end", "\n", "normal")
        text_widget.insert("end", f"{icon}\n", "icon")
        text_widget.config(state="disabled")  # lecture seule


root = tk.Tk()
app = TicketApp(root)
root.mainloop()
