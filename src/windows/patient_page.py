import tkinter as tk
from tkinter import ttk
from src.utils.functions import fetch_patients
from datetime import datetime
import ttkbootstrap as ttk
from ttkbootstrap.icons import Icon
from ttkbootstrap.constants import *

class DetailButton(ttk.Frame):
    def __init__(self, master, image, command=None, style=None, **kwargs):
        super().__init__(master, **kwargs)
        
        if style:
            self.image_button = ttk.Button(self, image=image, command=command, style=style, cursor="hand2")
        else:
            self.image_button = ttk.Button(self, image=image, command=command, cursor="hand2")
            
        self.image_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class PatientPage(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.patients_data = fetch_patients()

        # Create the frame to display the patient list
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True)
        
        self.notebook = ttk.Notebook(self.list_frame)
        self.notebook.pack(fill='both', expand=True)

        # Create separate frames for entries and exits
        self.entries_frame = ttk.Frame(self.notebook)
        self.exits_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entries_frame, text='Entrées')
        self.notebook.add(self.exits_frame, text='Sorties')

        # Define detail_frame and prescription_frame as attributes
        self.detail_frame = tk.Frame(self)
        self.prescription_frame = tk.Frame(self)
    
        # Accéder à l'icône d'avertissement
        self.image_loupe = tk.PhotoImage(data=Icon.info)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.scrollable_frame, width=event.width)

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
    
    # frame à remplacer par canvas
    def display_patients(self, frame, text, data):
        # Create a canvas widget within the frame
        canvas = tk.Canvas(frame, height=600)
        canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to contain the patient details
        patients_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=patients_frame, anchor="nw")
        # Create labels for the headers
        ttk.Label(patients_frame, text="ID", bootstyle="inverse-dark", anchor="center", justify="center").grid(row=0, column=1, pady=10, sticky="ew")
        ttk.Label(patients_frame, text="Nom prénom", bootstyle="inverse-dark", anchor="center", justify="center").grid(row=0, column=2, pady=10, sticky="ew")
        ttk.Label(patients_frame, text="Heure", bootstyle="inverse-dark").grid(row=0, column=3, pady=10, sticky="ew")
        ttk.Label(patients_frame, text="", bootstyle="inverse-dark").grid(row=0, column=4, pady=10, sticky="ew")
       
        # Display patients' data in the patients_frame
        for i, patient_info in enumerate(data):
            # Calculate the row index
            row_index = i + 1
            # Insert data into the table
            ttk.Label(patients_frame, text=patient_info[0], padding=(10, 5)).grid(row=row_index, column=1, sticky="ew")
            ttk.Label(patients_frame, text=patient_info[1], padding=(10, 5)).grid(row=row_index, column=2, sticky="ew")
            ttk.Label(patients_frame, text=patient_info[2], padding=(10, 5)).grid(row=row_index, column=3, sticky="ew")
            # Add "Détail" button at the end of each row
            detail_button = DetailButton(patients_frame, image=self.image_loupe, command=lambda i=i: self.show_patient_details(i), style='Link.TButton')
            detail_button.grid(row=row_index, column=4, sticky="ew")   
            # Adjust column weights
            for j in range(5):
                patients_frame.grid_columnconfigure(j, weight=1)

        # Update the scroll region of the canvas
        patients_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
 
       
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
    
    def create_scrollable_frame(self, parent_frame):
        """
        Crée un frame avec une barre de défilement et retourne le frame de contenu.

        Args:
            parent_frame: Le frame parent dans lequel le frame scrollable sera inséré.

        Returns:
            Le frame de contenu créé.
        """

        canvas = tk.Canvas(parent_frame, height=600)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        return content_frame, canvas


    def show_prescriptions(self, patient, prescription_frame):
        print('show_prescriptions')
        # Effacer le contenu existant dans le cadre de prescription
        for widget in prescription_frame.winfo_children():
            widget.destroy()
            
        scrollable_frame, canvas = self.create_scrollable_frame(prescription_frame)
 
        # Cadre pour afficher les prescriptions
        title_label = ttk.Label(scrollable_frame, text="Prescriptions", font=("Helvetica", 14, "bold"))
        title_label.pack(fill=tk.X, padx=5, pady=10)
        
        # Afficher les prescriptions
        for prescription in patient['patient_infos']['prescriptions']:
            start_date = datetime.strptime(prescription['start_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            end_date = datetime.strptime(prescription['end_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            prescriptions_frame = ttk.LabelFrame(scrollable_frame, text=f"Prescription {start_date} -- {end_date}", padding=10)
            prescriptions_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            label = ttk.Label(prescriptions_frame, text=f"Médecin: {prescription['medecin_firstname']} {prescription['medecin_lastname']}")
            label.pack(anchor="w", padx=5, pady=2)
            label.config(font="TkDefaultFont 10 bold")

             # Afficher les médicaments prescrits sous forme de liste
            medications_list = []
            for medication in prescription['medications']:
                medications_list.append(f"{medication['drug_name']} : {medication['dosage']}")

            medications_text = "\n".join(medications_list)
            ttk.Label(prescriptions_frame, text=medications_text).pack(anchor="w", padx=5, pady=2)
        
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def show_opinions(self, patient, prescription_frame):
        print('show_opinions')
        # Clear existing content in the left frame
        for widget in prescription_frame.winfo_children():
            widget.destroy()

        scrollable_frame, canvas = self.create_scrollable_frame(prescription_frame)

        # Tri des avis par date décroissante (plus récent en premier)
        sorted_opinions = sorted(patient['patient_infos']['opinions'], key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=True)

        title_label = ttk.Label(scrollable_frame, text="Avis des médecins", font=("Helvetica", 14, "bold"))  # Définir une police plus grande et en gras
        title_label.pack(fill=tk.X, padx=5, pady=10)
        
        # Afficher les avis
        for opinion in sorted_opinions:

            date = datetime.strptime(opinion['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
       
            opinion_frame = ttk.LabelFrame(scrollable_frame, text=f"{date}", padding=10)
            opinion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            label  = ttk.Label(opinion_frame, text=f"Médecin: {opinion['medecin_firstname']} {opinion['medecin_lastname']}")
            label.pack(anchor="w", padx=5, pady=2)
            label.config(font="TkDefaultFont 10 bold")

            ttk.Label(opinion_frame, text=f"Titre: {opinion['title']}").pack(anchor="w", padx=5, pady=2)
            ttk.Label(opinion_frame, text=f"Description: {opinion['description']}", wraplength=400, justify=tk.LEFT, padding=(5, 2),anchor="w").pack()
        
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def showStays(self, patient, prescription_frame):
        print('showStays')
        # Clear existing content in the left frame
        for widget in prescription_frame.winfo_children():
            widget.destroy()
        
        scrollable_frame, canvas = self.create_scrollable_frame(prescription_frame)
        
        title_label = ttk.Label(scrollable_frame, text="Séjours", font=("Helvetica", 14, "bold"))
        title_label.pack(fill=tk.X, padx=5, pady=10)
        
        # Afficher les séjours effectués
        for stay in patient['patient_infos']['stays']:

            start_date = datetime.strptime(stay['start_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            end_date = datetime.strptime(stay['end_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            etat = stay['etat']
            # Appliquez le style en fonction de l'état
            if etat == "encours":
                border_color = "blue"
            elif etat == "avenir":
                border_color = "green"
            else:
                border_color = "gray"
            
            # Créez un objet Style et configurez le style
            s = ttk.Style()
            s.configure('clam.TLabelframe', bordercolor=border_color, borderwidth=8,background='white')
            s.configure('clam.TLabelframe.Label', foreground='blue',background='white')
            s.configure('clam.TLabelframe.border', background=border_color, borderwidth=10)
            # Créez un cadre d'étiquette en utilisant le style configuré
            opinion_frame = ttk.LabelFrame(scrollable_frame, text=f"Séjour du {start_date} au {end_date} - {etat}", padding=10, style="clam.TLabelframe")
            
            opinion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            
            label = ttk.Label(opinion_frame, text=f"Médecin: {stay['medecin_firstname']} {stay['medecin_lastname']}", anchor="w", justify=tk.LEFT, padding=(5, 2))
            label.pack(fill='x')
            label.config(font="TkDefaultFont 10 bold")
            label = ttk.Label(opinion_frame, text=f"Spécialité: {stay['speciality_lib']}", wraplength=400, justify=tk.LEFT, anchor="w", padding=(5, 2))
            label.pack(fill='x')
            label.config(font="TkDefaultFont 10 bold")
            ttk.Label(opinion_frame, text=f"Reason: {stay['reason']}", anchor="w", justify=tk.LEFT, padding=(5, 2)).pack(fill='x')
            ttk.Label(opinion_frame, text=f"Description: {stay['description']}", wraplength=400, justify=tk.LEFT, anchor="w", padding=(5, 2)).pack(fill='x')
        
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))


