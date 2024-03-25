import tkinter as tk
from tkinter import *
from src.utils.functions import fetch_patients, save_to_file
from src.utils.constants import DetailButton
from datetime import datetime
from config import GET_DATA_FROM_FILE
import ttkbootstrap as ttk
from ttkbootstrap.icons import Icon
from ttkbootstrap.constants import *

class PatientPage(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.patients_data = fetch_patients()

        # Create the frame to display the patient list
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True)
        canvas = Canvas(self.list_frame, bg = 'red')

        # start of Notebook (multiple tabs)
        self.notebook = ttk.Notebook(canvas)
        self.notebook.pack(fill='both', expand=True)

        # Create separate frames for entries and exits
        self.entries_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entries_frame, text='Entrées')
       
        self.exits_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.exits_frame, text='Sorties')
        
        # Define detail_frame and prescription_frame as attributes
        self.detail_frame = tk.Frame(self)
        self.prescription_frame = tk.Frame(self)
    
        # Accéder à l'icône d'avertissement
        self.image_loupe = tk.PhotoImage(data=Icon.info)

        self.show_patients_list()

    def show_patients_list(self):
        print('show_patients_list')
        # Display patients data in the list frame
  
        self.patients_data = self.formate_patients_data()
        
        entries_data = []
        exits_data = []

        for patient in self.patients_data:
            if patient['type'] == 'in':
                nom_complet = f"{patient['patient_infos']['firstname']} {patient['patient_infos']['lastname']}"
                entry_info = (patient['id'], nom_complet, patient['heure'])
                entries_data.append(entry_info)
            elif patient['type'] == 'out':
                exit_info = (patient['id'], f"{patient['patient_infos']['firstname']} {patient['patient_infos']['lastname']}", patient['heure'])
                exits_data.append(exit_info)
                    
        # Display entries
        self.display_patients(self.entries_frame, "Entrée", entries_data)

        # Display exits
        self.display_patients(self.exits_frame, "Sortie", exits_data)
    
    def display_patients(self, frame, text, data):
        
        # Create labels for the headers
        ttk.Label(frame, text="ID", bootstyle="inverse-dark", anchor="center", justify="center").grid(row=0, column=1, pady=10, sticky="ew")
        ttk.Label(frame, text="Nom prénom", bootstyle="inverse-dark", anchor="center", justify="center").grid(row=0, column=2, pady=10, sticky="ew")
        ttk.Label(frame, text="Heure", bootstyle="inverse-dark").grid(row=0, column=3, pady=10, sticky="ew")
        ttk.Label(frame, text="", bootstyle="inverse-dark").grid(row=0, column=4, pady=10, sticky="ew")
        
        for i, patient_info in enumerate(data):
            # Calculate the row index
            row_index = i + 1

            # Insert data into the table
            # ttk.Label(frame, text=text, padding=(10, 5)).grid(row=row_index, column=0, sticky="ew")  # Adjust padding values as needed
            ttk.Label(frame, text=patient_info[0], padding=(10, 5)).grid(row=row_index, column=1, sticky="ew")
            ttk.Label(frame, text=patient_info[1], padding=(10, 5)).grid(row=row_index, column=2, sticky="ew")
            ttk.Label(frame, text=patient_info[2], padding=(10, 5)).grid(row=row_index, column=3, sticky="ew")

            # Add "Détail" button at the end of each row
            detail_button = DetailButton(frame, image=self.image_loupe, command=lambda i=i: self.show_patient_details(i), style='Link.TButton')
            detail_button.grid(row=row_index, column=4, sticky="ew")
        
            # Adjust column weights
            for i in range(5):
                frame.grid_columnconfigure(i, weight=1)

        
       
    def show_patient_details(self, i):
        # Clear existing content in the detail and prescription frames
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        for widget in self.prescription_frame.winfo_children():
            widget.destroy()

        patient = self.patients_data[i]
        print('Page detail_patient')
   
        # Cadre pour les informations générales du patient
        general_frame = ttk.Frame(self.detail_frame, padding=20)
        general_frame.pack(fill=tk.BOTH, expand=True)

        # Afficher les informations générales du patient
        general_labels = [ "Patient","ID", "Adresse", "Code postal", "Ville", "Pays"]
        for i, label in enumerate(general_labels):
            ttk.Label(general_frame, text=label, font=("Helvetica", 12, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            
            firstname = patient['patient_infos']['firstname']
            lastname = patient['patient_infos']['lastname']
            full_name = f"{firstname} {lastname}"
            ttk.Label(general_frame, text=full_name, font=("Helvetica", 12, "bold"), style='info.TLabel').grid(row=0, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['id']).grid(row=1, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adlibelle']).grid(row=2, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcp']).grid(row=3, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcity']).grid(row=4, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcountry']).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Ajout des boutons pour les prescriptions et les avis
        prescription_button = ttk.Button(general_frame, text="Prescriptions", command=lambda: self.show_prescriptions(patient, self.prescription_frame))
        opinion_button = ttk.Button(general_frame, text="Avis", command=lambda: self.show_opinions(patient, self.prescription_frame))
        stay_button = ttk.Button(general_frame, text="Séjours", command=lambda: self.showStays(patient, self.prescription_frame))

        prescription_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew", columnspan=3)
        opinion_button.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=3)
        stay_button.grid(row=8, column=0, padx=5, pady=5, sticky="ew", columnspan=3)

    
    def formate_patients_data(self):
        current_date = datetime.now().date()
        for patient in self.patients_data:
            if 'start' in patient and 'end' in patient:
                start_datetime = datetime.strptime(patient['start'], '%Y-%m-%d %H:%M')
                end_datetime = datetime.strptime(patient['end'], '%Y-%m-%d %H:%M')
                if start_datetime.date() == current_date:
                    patient['heure'] = start_datetime.strftime('%H:%M')
                    patient['type'] = "in"
                elif end_datetime.date() == current_date:
                    patient['heure'] = end_datetime.strftime('%H:%M')
                    patient['type'] = "out"
        patients_data = sorted(self.patients_data, key=lambda x: x['heure'])
        return patients_data
    
    def show_prescriptions(self, patient, prescription_frame):
        print('show_prescriptions')
        # Effacer le contenu existant dans le cadre de prescription
        for widget in prescription_frame.winfo_children():
            widget.destroy()

        # Cadre pour afficher les prescriptions
        title_label = ttk.Label(prescription_frame, text="Prescriptions", font=("Helvetica", 14, "bold"))
        title_label.pack(fill=tk.X, padx=5, pady=10)
        
        # Afficher les prescriptions
        for prescription in patient['patient_infos']['prescriptions']:
            start_date = datetime.strptime(prescription['start_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            end_date = datetime.strptime(prescription['end_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            prescriptions_frame = ttk.LabelFrame(prescription_frame, text=f"Prescription {start_date} -- {end_date}", padding=10)
            prescriptions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            ttk.Label(prescriptions_frame, text=f"Médecin: {prescription['medecin_firstname']} {prescription['medecin_lastname']}").pack(anchor="w", padx=5, pady=2)

             # Afficher les médicaments prescrits sous forme de liste
            medications_list = []
            for medication in prescription['medications']:
                medications_list.append(f"{medication['drug_name']} : {medication['dosage']}")

            medications_text = "\n".join(medications_list)
            ttk.Label(prescriptions_frame, text=medications_text).pack(anchor="w", padx=5, pady=2)

    def show_opinions(self, patient, prescription_frame):
        print('show_opinions')
        # Clear existing content in the left frame
        for widget in prescription_frame.winfo_children():
            widget.destroy()

        title_label = ttk.Label(prescription_frame, text="Avis du patient", font=("Helvetica", 14, "bold"))  # Définir une police plus grande et en gras
        title_label.pack(fill=tk.X, padx=5, pady=10)

        
        # Afficher les avis
        for opinion in patient['patient_infos']['opinions']:

            date = datetime.strptime(opinion['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            opinion_frame = ttk.LabelFrame(prescription_frame, text=f"{date}", padding=10)
            opinion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            ttk.Label(opinion_frame, text=f"Titre: {opinion['title']}").pack(anchor="w", padx=5, pady=2)
            ttk.Label(opinion_frame, text=f"Description: {opinion['description']}", wraplength=400, justify=tk.LEFT, padding=(5, 2),anchor="w").pack()
            ttk.Label(opinion_frame, text=f"Médecin: {opinion['medecin_firstname']} {opinion['medecin_lastname']}").pack(anchor="w", padx=5, pady=2)
    
    def showStays(self, patient, prescription_frame):
        print('showStays')
        # Clear existing content in the left frame
        for widget in prescription_frame.winfo_children():
            widget.destroy()
        
        title_label = ttk.Label(prescription_frame, text="Séjours", font=("Helvetica", 14, "bold"))  # Définir une police plus grande et en gras
        title_label.pack(fill=tk.X, padx=5, pady=10)

        # Afficher les séjours effectués
        for stay in patient['patient_infos']['stays']:

            start_date = datetime.strptime(stay['start_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            end_date = datetime.strptime(stay['end_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            opinion_frame = ttk.LabelFrame(prescription_frame, text=f"Séjour du  {start_date} au {end_date} - stays['etat']", padding=10)
            opinion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            ttk.Label(opinion_frame, text=f"Reason: {stay['reason']}", anchor="w", justify=tk.LEFT, padding=(5, 2)).pack(fill='x')
            ttk.Label(opinion_frame, text=f"Description: {stay['description']}", wraplength=400, justify=tk.LEFT, anchor="w", padding=(5, 2)).pack(fill='x')
            ttk.Label(opinion_frame, text=f"Médecin: {stay['medecin_firstname']} {stay['medecin_lastname']}", anchor="w", justify=tk.LEFT, padding=(5, 2)).pack(fill='x')
            ttk.Label(opinion_frame, text=f"Spécialité: {stay['speciality_lib']}", wraplength=400, justify=tk.LEFT, anchor="w", padding=(5, 2)).pack(fill='x')


