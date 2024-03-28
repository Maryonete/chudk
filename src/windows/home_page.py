import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.windows.patient_page import PatientPage
from pathlib import Path
from src.windows.styles import AppStyle

PATH = Path(__file__).parent.parent.parent / 'images'
class HomePage(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill=BOTH, expand=True)
        
        self.stylettk = ttk.Style()
        self.style = AppStyle()
        self.style.set_headframe_style(self.stylettk)
        # --------------------------------------
        # HEADER
        # --------------------------------------
        # application images
        self.images = [
            tk.PhotoImage(name='logo', file="C:/python/chudk/images/logoBlack.png", height=100),
        ]

        # Create and pack the title label
        headFrame = ttk.Frame(self,style="HeadFrame.TFrame")
        headFrame.pack(side=TOP, fill=X)  # Pack header at the top
        hdr_label = ttk.Label(
            master=headFrame,
            image='logo',
            bootstyle=(INVERSE, SECONDARY)
        )
        hdr_label.pack(side=LEFT)
        
        header_text = tk.Label(
            master=headFrame,
            text='Patients du jour',
            font=("Georgia", 30),
        )
        header_text.pack(side=LEFT, padx=10)
        header_text.config(background=self.style.blue_color,
            fg=self.style.bg_color)
        
        self.style.set_left_button_style(self.stylettk)
        self.style.set_hover_button_color(self.stylettk)
        
        # Add the Quit button on the right side
        quit_button = ttk.Button(
            master=headFrame,
            text='Quitter',
            command=self.master.destroy, 
            style="LeftButton.TButton", 
            width=12,
        )
        quit_button.pack(side=RIGHT, padx=10)

        # --------------------------------------
        # BODY
        # --------------------------------------

        # Create a parent frame for patients list, details, and prescriptions
        bodyFrame = ttk.Frame(self)
        bodyFrame.pack(fill=BOTH, expand=True)  # Fill entire available space

        # Frame liste patients
        self.list_frame = ttk.Frame(bodyFrame, relief="sunken")
        self.list_frame.pack(side=LEFT, fill=Y)

        list_content_frame = ttk.Frame(self.list_frame)
        list_content_frame.pack(side=LEFT, fill=BOTH, expand=True) 

        list_frame_width = int(bodyFrame.winfo_width() / 4)
        self.list_frame.config(width=list_frame_width)

        
        self.detail_frame = ttk.Frame(bodyFrame)
        self.detail_frame.pack(fill=Y, side=LEFT)  
        # Taille des frames
        list_frame_width = int(bodyFrame.winfo_width() / 3)
        self.detail_frame.config(width=list_frame_width)

        self.prescription_frame = ttk.Frame(bodyFrame)
        self.prescription_frame.pack(fill=BOTH, side=LEFT, expand=True)  # Fill within detail_and_prescription_frame

        # Fetch and display patients
        self.show_patients_list()

    def show_patients_list(self):
        patient_page = PatientPage(self.list_frame, self)
        patient_page.pack(fill="both")
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
