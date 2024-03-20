import tkinter as tk
from src.utils.constants import ICONE_APLI
from src.windows.login_page import LoginPage

class MyApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.wm_iconbitmap(ICONE_APLI)  # Définit l'icône de l'application
        self.geometry("800x600")  # Taille fixe de la fenêtre principale
        self.title("SoigneMoi")  # Titre de la fenêtre principale
    
        # Création de la page de connexion
        self.login_page = LoginPage(self)
        self.login_page.pack(fill=tk.BOTH, expand=True)

    
def main():
    app = MyApp()
    app.mainloop()

if __name__ == "__main__":
  main()
