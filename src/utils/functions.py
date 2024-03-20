import jwt
from config import SECRET_KEY

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
