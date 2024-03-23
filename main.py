import tkinter as tk
from src.utils.constants import ICONE_APLI
from src.windows.login_page import LoginPage
from src.windows.home_page import HomePage
from src.utils.auth import is_logged_in
import ttkbootstrap as ttk
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wm_iconbitmap(ICONE_APLI)  # Définit l'icône de l'application
        # Récupère les dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Définit la géométrie de la fenêtre pour la moitié de l'écran en largeur et toute la hauteur
        half_screen_width = screen_width // 2
        half_screen_height = (2 * screen_height) // 3 
        self.geometry(f"{half_screen_width}x{half_screen_height}")
        
        self.title("SoigneMoi")  # Titre de la fenêtre principale

        if is_logged_in:
            self.show_home_page()
        else:
            self.show_login_page()

    def show_home_page(self):
        self.title("Hospital SoigneMoi")
        self.home_page = HomePage(self)
        self.home_page.pack(fill=tk.BOTH, expand=True)

    def show_login_page(self):
        self.title("Hospital SoigneMoi - Connexion")
        self.login_page = LoginPage(self)
        self.login_page.pack(fill=tk.BOTH, expand=True)

def main():
    app = MyApp()
    app.mainloop()

if __name__ == "__main__":
    main()
