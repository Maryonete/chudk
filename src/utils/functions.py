import jwt
from config import SECRET_KEY, GET_DATA_FROM_FILE
from src.api_manager import api_patients_of_the_day
import json

def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token,  options={"verify_signature": False})
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token expiré.")
        return None
    except jwt.InvalidTokenError:
        print("Token invalide.")
        return None

def fetch_patients():
    if GET_DATA_FROM_FILE:
        # Chemin d'accès au fichier datas.py
        file_path = 'C:\python\chudk\patients_data.json'
        # Charger les données depuis le fichier
        with open(file_path, 'r') as file:
            raw_data = file.read()

        # Convertir les données JSON en un dictionnaire Python
        return json.loads(raw_data)  or []

    else:
        patients_data=api_patients_of_the_day()
        save_to_file(patients_data, 'C:\python\chudk\patients_data.json')

        # Call the API function to fetch patients of the day
        return patients_data or []
    
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)