import tkinter as tk
from src.windows.login_page import LoginPage
from src.windows.home_page import HomePage
from src.utils.auth import is_logged_in
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("C:/python/chudk/images/favicon.ico")
        self.geometry(f"1200x800")
        # Titre de la fenêtre principale
        self.title("SoigneMoi")

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
