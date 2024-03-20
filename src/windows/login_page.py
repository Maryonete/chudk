import tkinter as tk
from src.windows.styles import styles, set_primary_button_style, set_entry_style

from tkinter import ttk 
from PIL import Image, ImageTk
from src.utils.constants import IMG_LOGO
from tkinter import messagebox

class LoginPage(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=styles["background_color"])
    
    # Configuration des styles
    self.style = ttk.Style()
    set_primary_button_style(self.style)
    set_entry_style(self.style)

    # Chargez l'image du logo
    logo_image = Image.open("images/logo.png")
    logo_image.thumbnail((200, 200))

    self.logo_photoimage = ImageTk.PhotoImage(logo_image)
    self.logo_label = tk.Label(self, image=self.logo_photoimage, bg=styles["background_color"])
    
    # Créez le label pour le logo
    self.logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
    
    # Création du titre pour la page de connexion
    self.title_label = tk.Label(self, text="Hospital SoigneMoi \n -\n Administration", font=("Arial", 18), bg=styles["background_color"])
    self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

    # Création des champs pour les informations de connexion
    self.label_username = tk.Label(self, text="Email:", font=styles["font"], bg=styles["background_color"])
    self.label_password = tk.Label(self, text="Mot de passe:", font=styles["font"], bg=styles["background_color"])
    self.entry_username = ttk.Entry(self, style="EntryStyle.TEntry")
    self.entry_password = ttk.Entry(self, show="*", style="EntryStyle.TEntry")
    self.button_login = ttk.Button(self, text="Connexion", command=self.login, style="PrimaryButton.TButton")

    # Mise en place des champs de manière centrée et harmonieuse
    self.label_username.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="e")
    self.entry_username.grid(row=2, column=1, padx=20, pady=(20, 5), sticky="w")
    self.label_password.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="e")
    self.entry_password.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="w")
    self.button_login.grid(row=4, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")

    # Configuration de la mise en page pour centrer les composants
    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)



  def login(self):
    username = self.entry_username.get()
    password = self.entry_password.get()

    # Ajoutez votre logique de vérification de l'identification ici
    # Par exemple, comparer avec une base de données d'utilisateurs enregistrés

    # Ici, nous allons simplement afficher un message de réussite ou d'échec
    if username == "utilisateur" and password == "motdepasse":
      messagebox.showinfo("Connexion réussie", "Bienvenue, {} !".format(username))
    else:
      messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
