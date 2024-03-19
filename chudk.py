import tkinter as tk

# Fonction pour gérer un clic sur un bouton
def ma_fonction():
  # Code à exécuter lors du clic
  print("Bouton cliqué !")

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Chudk")

# Créer un label
label = tk.Label(fenetre, text="Bienvenue dans Chudk !")
label.pack()

# Créer un bouton
bouton = tk.Button(fenetre, text="Cliquer ici", command=ma_fonction)
bouton.pack()

# Démarrer la boucle principale
fenetre.mainloop()
