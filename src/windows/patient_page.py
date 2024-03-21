import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils.functions import fetch_patients, save_to_file
from datetime import datetime
from config import GET_DATA_FROM_FILE
from tkinter import Button


class PatientPage(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.patients_data = fetch_patients()

        # Create the frame to display the patient list
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True)

        # Add a title to list_frame
        ttk.Label(self.list_frame, text="Liste des Patients", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        # Create separate frames for entries and exits
        self.entries_frame = ttk.LabelFrame(self.list_frame, text="Entrées")
        self.entries_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.exits_frame = ttk.LabelFrame(self.list_frame, text="Sorties")
        self.exits_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)


        # Define detail_frame and prescription_frame as attributes
        self.detail_frame = tk.Frame(self)
        self.prescription_frame = tk.Frame(self)
    
      
    def show_patients_list(self):
        print('show_patients_list')
        # Display patients data in the list frame
        
  
        self.patients_data = self.formate_patients_data()
        
        entries_data = []
        exits_data = []

        for patient in self.patients_data:
            if patient['type'] == 'in':
                entry_info = (patient['id'], f"{patient['patient_infos']['firstname']} {patient['patient_infos']['lastname']}", patient['heure'])
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
        ttk.Label(frame, text="Type").grid(row=0, column=0, sticky="ew")
        ttk.Label(frame, text="ID").grid(row=0, column=1, sticky="ew")
        ttk.Label(frame, text="Nom").grid(row=0, column=2, sticky="ew")
        ttk.Label(frame, text="Heure").grid(row=0, column=3, sticky="ew")

        # Insert data into the table
        for i, patient_info in enumerate(data):
            # Calculate the row index
            row_index = i + 1

            # Insert data into the table
            ttk.Label(frame, text=text).grid(row=row_index, column=0, sticky="ew")
            ttk.Label(frame, text=patient_info[0]).grid(row=row_index, column=1, sticky="ew")
            ttk.Label(frame, text=patient_info[1]).grid(row=row_index, column=2, sticky="ew")
            ttk.Label(frame, text=patient_info[2]).grid(row=row_index, column=3, sticky="ew")

            # Add "Détail" button at the end of each row
            detail_button = ttk.Button(frame, text="Détail", command=lambda i=i: self.show_patient_details(i))
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
            ttk.Label(general_frame, text=full_name, font=("Helvetica", 12, "bold")).grid(row=0, column=1, sticky="w", padx=5, pady=5)

            ttk.Label(general_frame, text=patient['id']).grid(row=1, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adlibelle']).grid(row=2, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcp']).grid(row=3, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcity']).grid(row=4, column=1, sticky="w", padx=5, pady=5)
            ttk.Label(general_frame, text=patient['patient_infos']['adcountry']).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Ajout des boutons pour les prescriptions et les avis
        prescription_button = ttk.Button(general_frame, text="Prescriptions", command=lambda: self.show_prescriptions(patient, self.prescription_frame))
        opinion_button = ttk.Button(general_frame, text="Avis", command=lambda: self.show_opinions(patient, self.prescription_frame))
        prescription_button.grid(row=6, column=0, padx=5, pady=5)
        opinion_button.grid(row=6, column=1, padx=5, pady=5)
    
    
    

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
        prescriptions_frame = ttk.LabelFrame(prescription_frame, text="Prescriptions du patient", padding=20)
        prescriptions_frame.pack(fill=tk.BOTH, expand=True)

        # Afficher les prescriptions
        for prescription in patient['patient_infos']['prescriptions']:
            start_date = datetime.strptime(prescription['start_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            end_date = datetime.strptime(prescription['end_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            prescription_frame = ttk.LabelFrame(prescriptions_frame, text=f"Prescription {start_date} -- {end_date}", padding=10)
            prescription_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            ttk.Label(prescription_frame, text=f"Médecin: {prescription['medecin_firstname']} {prescription['medecin_lastname']}").pack(anchor="w", padx=5, pady=2)

             # Afficher les médicaments prescrits sous forme de liste
            medications_list = []
            for medication in prescription['medications']:
                medications_list.append(f"{medication['drug_name']} : {medication['dosage']}")

            medications_text = "\n".join(medications_list)
            ttk.Label(prescription_frame, text=medications_text).pack(anchor="w", padx=5, pady=2)

    def show_opinions(self, patient, prescription_frame):
        print('show_opinions')
        # Clear existing content in the left frame
        for widget in prescription_frame.winfo_children():
            widget.destroy()

        # Cadre pour afficher les avis
        opinions_frame = ttk.LabelFrame(prescription_frame, text="Avis du patient", padding=20)
        opinions_frame.pack(fill=tk.BOTH, expand=True)

        # Afficher les avis
        for opinion in patient['patient_infos']['opinions']:
            opinion_frame = ttk.LabelFrame(opinions_frame, text=f"Avis {opinion['id']}", padding=10)
            opinion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            ttk.Label(opinion_frame, text=f"Titre: {opinion['title']}").pack(anchor="w", padx=5, pady=2)
            ttk.Label(opinion_frame, text=f"Date: {opinion['date']}").pack(anchor="w", padx=5, pady=2)
            ttk.Label(opinion_frame, text=f"Description: {opinion['description']}", wraplength=400, justify=tk.LEFT, padding=(5, 2),anchor="w").pack()

            ttk.Label(opinion_frame, text=f"Médecin: {opinion['medecin_firstname']} {opinion['medecin_lastname']}").pack(anchor="w", padx=5, pady=2)
        

    


