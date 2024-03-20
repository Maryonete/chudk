import tkinter as tk
from src.windows.styles import styles, set_primary_button_style, set_entry_style

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        print('HomePage')
        self.title_label = tk.Label(self, text="Hospital SoigneMoi \n -\n Administration", font=("Arial", 18), bg=styles["background_color"])
        # Ajoutez ici le contenu de votre page d'accueil, par exemple :
        self.label = tk.Label(self, text="Bienvenue sur la page d'accueil !")
        self.label.pack(padx=20, pady=20)

        # Vous pouvez ajouter d'autres widgets ou fonctionnalités ici
