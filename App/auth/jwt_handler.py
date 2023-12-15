import jwt
import secrets
import time
from decouple import config

JWT_SECRET = config("secret")
JWT_ALORITHM = config("algorithm")

def token_respone(token: str):
    return {
        "access token": token,
    }
def signJWT(userID: str, userType: str):
    payload = {
        "userID": userID,
        "userType": userType,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALORITHM)
    return token_respone(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALORITHM)
        return decode_token
    except Exception:
        return None