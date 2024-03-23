import tkinter as tk
from tkinter import ttk, Scrollbar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.windows.patient_page import PatientPage
from pathlib import Path


PATH = Path(__file__).parent.parent.parent / 'images'

class HomePage(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=BOTH, expand=True)

        # --------------------------------------
        # HEADER
        # --------------------------------------
        # application images
        self.images = [
            tk.PhotoImage(name='logo', file=PATH / 'logoBlack.png', height=100),
        ]

        # Create and pack the title label
        headFrame = ttk.Frame(self, padding=20, bootstyle=SECONDARY)
        headFrame.grid(row=0, column=0, columnspan=3, sticky=EW)
        hdr_label = ttk.Label(
            master=headFrame,
            image='logo',
            bootstyle=(INVERSE, SECONDARY)
        )
        hdr_label.pack(side=LEFT)
        logo_text = ttk.Label(
            master=headFrame,
            text='Patients du jour',
            font=('TkDefaultFixed', 30),
            bootstyle=(INVERSE, SECONDARY)
        )
        logo_text.pack(side=LEFT, padx=10)
        self.columnconfigure(0, weight=1)
        # --------------------------------------
        # BODY
        # --------------------------------------
        # Create a parent frame for patients list, details, and prescriptions
        bodyFrame = ttk.Frame(self)
        bodyFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW, padx=30, pady=30)
        bodyFrame.columnconfigure((0, 1, 2), minsize=250)
        bodyFrame.rowconfigure(0, weight=1)

       # Configure column 0 to resize with the window
        self.columnconfigure(0, weight=1)

        self.list_frame = ttk.Frame(bodyFrame, relief="sunken")
        # Crée une barre de défilement
        scrollbar = Scrollbar(self.list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.detail_frame = ttk.Frame(bodyFrame, borderwidth=2, relief="sunken")
        self.prescription_frame = ttk.Frame(bodyFrame)

        # Grid the frames within the parent frame
        self.list_frame.grid(row=0, column=0, sticky=NSEW, padx=10, pady=10)
        self.detail_frame.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)
        self.prescription_frame.grid(row=0, column=2, sticky=NSEW, padx=10, pady=10)
        
        # Fetch and display patients
        self.show_patients_list()

    def show_patients_list(self):
        patient_page = PatientPage(self.list_frame, self)
        patient_page.pack(fill="both", expand=True)
        patient_page.detail_frame = self.detail_frame
        patient_page.prescription_frame = self.prescription_frame
        patient_page.show_patients_list()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style("darkly")

    # new approach
    root = ttk.Window(themename="sandstone")
    root.title("Page d'accueil")
    home_page = HomePage(root)
    home_page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
