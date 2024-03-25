import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

IMG_LOGO = "src/windows/images/logo.png"
URL_API = "https://soignemoi-chu-19a585dde838.herokuapp.com/api/"

class DetailButton(ttk.Frame):
    def __init__(self, master, image, command=None, style=None, **kwargs):
        super().__init__(master, **kwargs)
        
        if style:
            self.image_button = ttk.Button(self, image=image, command=command, style=style, cursor="hand2")
        else:
            self.image_button = ttk.Button(self, image=image, command=command, cursor="hand2")
            
        self.image_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
