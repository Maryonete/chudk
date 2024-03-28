class AppStyle:
    def __init__(self):
        self.background_color = "#FFFFFF"  # Couleur de fond par défaut en blanc
        self.h1_font = ('Georgia', 24, 'bold')  # Style H1
        self.h2_font = ('Georgia', 18, 'bold')  # Style H2
        self.h3_font = ('Georgia', 14, 'bold')  # Style H3
        self.body_font = ('Segoe UI', 12)  # Style du corps de l'application

        self.bg_color = 'white'  # Couleur de fond
        self.fg_color = 'black'  # Couleur de premier plan
        self.blue_color = '#124660'  # Couleur du titre
        self.hover_color = '075D6B'

        self.entry_padding = 5

        self.label_font = ("Georgia", 12)

        self.InputTextStyle = "InputTextStyle"

    def apply_h1_style(self, widget):
        widget.config(font=self.h1_font, bg=self.bg_color, fg=self.blue_color)

    def apply_h2_style(self, widget):
        widget.config(font=self.h2_font, bg=self.bg_color, fg=self.blue_color)

    def apply_h3_style(self, widget):
        widget.config(font=self.h3_font, bg=self.bg_color, fg=self.blue_color)

    def apply_body_style(self, widget):
        widget.config(font=self.body_font, bg=self.bg_color, fg=self.fg_color)

    def set_headframe_style(self, style):
        style.configure("HeadFrame.TFrame",
                        background=self.blue_color,
                        padding=20)

        
    # style du bouton principal
    def set_primary_button_style(self, style):
        style.configure("Button.TButton",
                        background=self.blue_color,
                        fg="white",
                        justify="center",
                        font=self.label_font,
                        padding=(10, 5)) 
        
    def set_left_button_style(self, style):
        style.configure("LeftButton.TButton",
                        background="white",
                        foreground=self.blue_color,
                        justify="center",
                        font=self.label_font,
                        padding=(10, 5)) 
    # couleur du bouton lorsque la souris passe dessus
    def set_hover_button_color(self, style):
        style.map("PrimaryButton.TButton",
                  background=[('active', self.hover_color)],
                  foreground=[('active', 'white')])

    # Méthode pour définir le style des champs d'entrée
    def set_entry_style(self, style):
        style.configure(self.InputTextStyle,
                        font=self.label_font,
                        padding=self.entry_padding)
