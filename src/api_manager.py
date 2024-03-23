import requests
from src.utils.constants import URL_API
from tkinter import messagebox

def login_to_api(username, password):
    api_url = URL_API + "login_check"
    print('api_url : ',api_url)
    data = {
        "username": username,
        "password": password
    }
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    try:
        response = requests.post(api_url, json=data, headers=headers)
        
        # Vérifiez si la requête a réussi (code de statut HTTP 200)
        if response is not None and response.status_code == 200:
            print("Requête réussie !")

        # Affichez le contenu de la réponse
        # print("Contenu de la réponse :", response.text)

        # Affichez le code de statut HTTP
        print("Code de statut HTTP :", response.status_code)

        # Affichez les en-têtes de la réponse
        # print("En-têtes de la réponse :", response.headers)

        # Affichez le contenu binaire de la réponse (utile pour les fichiers binaires)
        # print("Contenu binaire de la réponse :", response.content)
        return response
    except requests.RequestException as e:
        # Gérez l'erreur comme vous le souhaitez
        return None

def api_patients_of_the_day():
    # Define the API endpoint URL
    api_url = URL_API + "getAllPatientsOfDay"
    print('api_url : ',api_url)
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    try:
        # Make a GET request to the API
        response = requests.get(api_url, headers=headers)
        print('response.status_code : ',response.status_code )
        # Check if the request was successful
        if response.status_code == 200:
            # Extract data from the response
            return response.json()
            # print('API : patients_of_the_day ',patients_of_the_day)
            
        else:
            # Show an error message if the request failed
            messagebox.showerror("API Error", f"Failed to retrieve patients of the day: {response.status_code}")
    except Exception as e:
        # Show an error message if an exception occurred during the request
        messagebox.showerror("Error", f"An error occurred: {str(e)}")