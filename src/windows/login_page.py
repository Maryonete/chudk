import tkinter as tk
import json
from tkinter import ttk , Tk
from PIL import Image, ImageTk
from src.utils.constants import IMG_LOGO
from tkinter import messagebox
from src.api_manager import login_to_api
from src.utils.auth import set_logged_in
from src.utils.functions import decode_jwt
import ttkbootstrap as ttk
# Import module threading pour exécuter l'appel API dans un thread séparé
import threading  
from src.windows.styles import AppStyle

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=AppStyle().background_color)
        self.stylettk = ttk.Style()
        self.style = AppStyle()

        # Chargez l'image du logo
        logo_image = Image.open("C:/python/chudk/images/logo.png")
        logo_image.thumbnail((200, 200))
        self.logo_photoimage = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(self, image=self.logo_photoimage)
        
        # Créez le label pour le logo
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # Création du titre pour la page de connexion
        self.title_label = tk.Label(self, text="Hospital SoigneMoi \n -\n Administration", font=self.style.h1_font, bg=self.style.bg_color)
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Création des champs pour les informations de connexion
        self.label_username = tk.Label(self, text="Email:", font=self.style.h3_font, bg=self.style.bg_color)
        self.label_password = tk.Label(self, text="Mot de passe:", font=self.style.h3_font, bg=self.style.bg_color)
        self.entry_username = ttk.Entry(self, font = (self.style.body_font))
        self.entry_password = ttk.Entry(self, show="*", font = (self.style.body_font))
        
        # #TODO
        self.entry_username.insert(0, "staff@studi.fr")
        self.entry_password.insert(0, "test")
        
        # Mise en place des champs de manière centrée et harmonieuse
        self.label_username.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="e")
        self.entry_username.grid(row=2, column=1, padx=20, pady=(20, 5), sticky="w")
        self.label_password.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="e")
        self.entry_password.grid(row=3, column=1, padx=20, pady=(5, 20), sticky="w")

        # Création du bouton de connexion
        self.style.set_primary_button_style(self.stylettk)
        self.style.set_hover_button_color(self.stylettk)
        self.button_login = ttk.Button(self, text="Connexion", command=self.login, width=12, style="Button.TButton")
        self.button_login.grid(row=4, column=1, padx=20, pady=(20, 5), sticky="w")

        # Progress Bar pour afficher le spinner
        self.progressbar = ttk.Progressbar(self, mode="indeterminate")
        self.progressbar.grid(row=5, column=1, padx=20, pady=(20, 5), sticky="w")
        self.progressbar.stop()
        self.progressbar.grid_remove() 
        
        # Configuration de la mise en page pour centrer les composants
        self.grid_columnconfigure(0, weight=1) # Centrer horizontalement la première colonne
        self.grid_columnconfigure(1, weight=1) # Centrer horizontalement la deuxième colonne
    
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        # Désactiver le bouton pendant l'appel API
        self.button_login.config(state="disabled")
        
        # Afficher le spinner
        self.progressbar.grid() 
        self.progressbar.start()
        # Fonction pour exécuter l'appel API dans un thread séparé
        def api_call():
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
            
            # Réactiver le bouton et arrêter le spinner après l'appel API
                self.button_login.config(state="normal")
                self.progressbar.stop()
                self.progressbar.grid_remove()  # Masquer la barre de progression après l'appel API

        # Démarrer le thread pour exécuter l'appel API
        api_thread = threading.Thread(target=api_call)
        api_thread.start()

   
