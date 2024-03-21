import tkinter as tk
from tkinter import * 
from tkinter import ttk

from src.windows.patient_page import PatientPage

import tkinter as tk
from tkinter import ttk
from src.utils.functions import fetch_patients, save_to_file
from datetime import datetime
from config import GET_DATA_FROM_FILE
import json


class HomePage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Create frames
        self.list_frame = ttk.Frame(self, borderwidth=2)
        self.list_frame.pack(side=LEFT, padx=30, pady=30)

        self.detail_frame = ttk.Frame(self)
        self.prescription_frame = ttk.Frame(self)

        # Grid configuration
        self.list_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.detail_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.prescription_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Calculate and set prescription frame width
        window_width = self.winfo_reqwidth()
        self.prescription_frame_width = (window_width - 40) // 3
        self.prescription_frame.config(width=self.prescription_frame_width)

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
    root.title("Page d'accueil")
    home_page = HomePage(root)
    home_page.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
