from tkinter import ttk  # Pour les éléments Bootstrap

styles = {
    "label_bg": "#f0f0f0",
    "label_bg": "#ffffff",
    "background_color": "#f0f0f0",  # Couleur de fond de l'application
    "font": ("Arial", 12),  # Police par défaut pour les composants
}

# Couleurs Bootstrap
primary_color = "#007bff"
secondary_color = "#6c757d"
light_color = "#f8f9fa"
dark_color = "#343a40"
white_color = "#fff"

# Police claire
font_family = "Arial"
font_color = "#212529"

# Définir les éléments de style communs
label_font = ("Arial", 12)
entry_font = ("Arial", 14)
button_font = ("Arial", 14, "bold")

# Définir le style pour le bouton principal
def set_primary_button_style(style):
    style.configure("PrimaryButton.TButton",
                    background  = "Black" , 
                    fg = "White" , 
                    font=label_font,
                    padding=(10, 5))

# Définir le style pour les champs d'entrée
def set_entry_style(style):
    style.configure("EntryStyle.TEntry",
                    font=label_font,
                    padding=5)


