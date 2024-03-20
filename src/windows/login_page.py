import tkinter as tk
import json
from src.windows.styles import styles, set_primary_button_style, set_entry_style
from tkinter import ttk , Tk
from PIL import Image, ImageTk
from src.utils.constants import IMG_LOGO
from tkinter import messagebox
from src.api_manager import login_to_api
from src.utils.auth import set_logged_in
from src.utils.functions import decode_jwt


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
      #  pour TEST #TODO
      self.entry_username.insert(0, "staff@studi.fr")
      self.entry_password.insert(0, "test")
      
      # Mise en place des champs de manière centrée et harmonieuse
      self.label_username.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="e")
      self.entry_username.grid(row=2, column=1, padx=20, pady=(20, 5), sticky="w")
      self.label_password.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="e")
      self.entry_password.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="w")

      # Ajout du bouton "Se souvenir de moi"
      self.remember_me_var = tk.BooleanVar()  # Variable pour stocker l'état du bouton
      self.remember_me_checkbutton = ttk.Checkbutton(self, text="Se souvenir de moi", variable=self.remember_me_var, style="Checkbutton.TCheckbutton")
      self.remember_me_checkbutton.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=20, sticky="w")

      # Configuration du style pour le bouton "Se souvenir de moi"
      self.style.configure("Checkbutton.TCheckbutton", font=styles["font"], background=styles["background_color"])
      
      # Création du bouton de connexion
      self.button_login = ttk.Button(self, text="Connexion", command=self.login, style="PrimaryButton.TButton")
      self.button_login.grid(row=5, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")

      # Configuration de la mise en page pour centrer les composants
      self.grid_columnconfigure(0, weight=1)
      self.grid_columnconfigure(1, weight=1)





  def login(self):
    username = self.entry_username.get()
    password = self.entry_password.get()
    response = login_to_api(username, password)

    if response is not None:
        if response.status_code == 200:
            try:
                jsonResponse = response.json()
                user_data = decode_jwt(jsonResponse['token'])
                # Vérification du rôle de l'utilisateur
                if 'ROLE_STAFF' not in user_data.get('roles', []):
                    error_message = "Vous n'avez pas les droits nécessaires pour accéder à cette page."
                    messagebox.showerror("Erreur de connexion", error_message)
                    return
            except json.JSONDecodeError:
                messagebox.showerror("Erreur de connexion", "Erreur lors de l'analyse de la réponse JSON.")
                return
            except KeyError:
                messagebox.showerror("Erreur de connexion", "Clé manquante dans la réponse JSON.")
                return
            
            set_logged_in(True)
            self.destroy()
            self.master.show_home_page()
        else:
            messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        messagebox.showerror("Erreur", "Une erreur s'est produite lors de la connexion à l'API.")
